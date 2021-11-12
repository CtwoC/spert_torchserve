from ts.torch_handler.base_handler import BaseHandler

from transformers import AutoTokenizer
from transformers import AutoConfig

import torch
from entities import Dataset
from torch.utils.data import DataLoader
import prediction
import sampling
import input_reader

import models
import os
import logging
from abc import ABC
logger = logging.getLogger(__name__)

class ModelHandler(object):
    """
    A custom model handler implementation.
    """

    def __init__(self):
        #init input reader
        super(ModelHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        """
        Invoke by torchserve for loading a model
        :param context: context contains model server system properties
        :return:
        """

        #  load the model
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        model_path = os.getcwd
        print(model_dir)
        print(os.listdir(model_dir))
        #load tokenizer from Huggingface
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        
        #load types_file
        types_path=os.path.join(model_dir, "types.json")
        if os.path.isfile(types_path):
            self.types_path=types_path
        else:
            logger.warning("Missing the setup_config.json file.")
        
        #load input_reader
        input_reader_cls=input_reader.SentenceInputReader
        self.input_reader = input_reader_cls(self.types_path, 
                                        self.tokenizer,
                                        max_span_size=10,
                                        spacy_model="en_core_web_sm")
        #load model class
        model_class = models.SpERT
        #load config
        config = AutoConfig.from_pretrained(model_dir)
        config.spert_version = model_class.VERSION
        #load model
        self.model = model_class.from_pretrained(model_dir,
                                            config=config,
                                            # SpERT model parameters
                                            cls_token=self.tokenizer.convert_tokens_to_ids(
                                                '[CLS]'),
                                            relation_types=self.input_reader.relation_type_count - 1,
                                            entity_types=self.input_reader.entity_type_count,
                                            max_pairs=1000,
                                            prop_drop=0.1,
                                            size_embedding=25,
                                            freeze_transformer=True)
        self.model.eval()
        self.initialized = True


    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        for data in enumerate(data):
            logger.info(data)
            #problem:input is a tupple
            logger.info(data[1]["body"])
            input_dic=data[1]["body"]
            input_text=[]
            for sentence in input_dic['sentences']:
                input_text.append(sentence)
            # input_text = data[1].get("data")
            # if input_text is None:
            #     input_text = data.get("body")
            # if isinstance(input_text, (bytes, bytearray)):
            #     input_text = input_text.decode('utf-8')
            logger.info("Received texts: '%s'", input_text)
        # Take the input data and make it inference ready
        preprocessed_data = input_text
        model_input = self.input_reader.read(preprocessed_data, 'dataset')
        model_input.switch_mode(Dataset.EVAL_MODE)
        data_loader = DataLoader(model_input, batch_size=1, shuffle=False, drop_last=False,
                                    num_workers=0, collate_fn=sampling.collate_fn_padding)

        pred_entities = []
        pred_relations = []

        def to_device(batch, device):
            converted_batch = dict()
            for key in batch.keys():
                converted_batch[key] = batch[key].to(device)
            return converted_batch

        with torch.no_grad():
            # iterate batches
            for batch in data_loader:
                # move batch to selected device
                batch = to_device(batch, "cpu")
                # run model (forward pass)
                result = self.model(encodings=batch['encodings'], context_masks=batch['context_masks'],
                                entity_masks=batch['entity_masks'], entity_sizes=batch['entity_sizes'],
                                entity_spans=batch['entity_spans'], entity_sample_masks=batch['entity_sample_masks'],
                                inference=True)
                entity_clf, rel_clf, rels = result
                # convert predictions
                predictions = prediction.convert_predictions(entity_clf, rel_clf, rels,
                                                                batch, 0.4,
                                                                self.input_reader)

                batch_pred_entities, batch_pred_relations = predictions
                pred_entities.extend(batch_pred_entities)
                pred_relations.extend(batch_pred_relations)

        model_output = prediction.store_predictions(model_input.documents, pred_entities, pred_relations)
        return [model_output]