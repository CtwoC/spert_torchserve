# SpERT torchserve
Spert_torchserve is the Relation Extraction model [(SpERT)Span-based Entity and Relation Transformer](https://github.com/lavis-nlp/spert) API deployed with [pytorch/serve](https://github.com/pytorch/serve).

## Install Requirements

```
pip install -r requirements.txt
```

## Get your pretrained model
Train your own model with [SpERT](https://github.com/lavis-nlp/spert) or use model trained by CoNLL04 from [Huggingface](https://huggingface.co/Zichuu/spert/tree/main). Only pytorch_model.bin is required to be archived. [Download it here](https://drive.google.com/file/d/1El0v_0xEblpSRDIQ_6lxI6ZnvxqEYVBa/view?usp=sharing) and save it into model directory.

You can also save your own model at Huggingface with large file storage.

Save your TAKE model in model directory. 

## Archive your model
Before serving model, pack the model and other configs into a .mar file.

```
torch-model-archiver --model-name spert --version 1.0 --model-file models.py --serialized-file model/pytorch_model.bin --export-path model_store --extra-files entities.py,input_reader.py,loss.py,prediction.py,sampling.py,conll04_types.json --handler spert_handler
```
This command pack all the needed files into a spert.mar file in model_store fold.

To archive your TAKE model, use command in terminal:
```
torch-model-archiver --model-name spert_TAKE --version 1.0 --model-file models.py --serialized-file model/TAKE_20201204/pytorch_model.bin --export-path model_store --extra-files entities.py,input_reader.py,loss.py,prediction.py,sampling.py,model/TAKE_20201204/types.json,model/TAKE_20201204/config.json,model/TAKE_20201204/special_tokens_map.json,model/TAKE_20201204/tokenizer_config.json,model/TAKE_20201204/vocab.txt --handler spert_handler_TAKE
```

Or use:
```
python archiver.py
```

## Serve the model
Start the service using the spert.mar with command:
```
torchserve --start --model-store model_store --models my_tc=spert.mar --ncs
```

To start TAKE model:
```
torchserve --start --model-store model_store --models my_tc=spert_TAKE.mar --ncs
```

## Test
To test model trained on CoNLL04, post the text example "In 1822, the 18th president of the United States, Ulysses S. Grant, was born in Point Pleasant, Ohio" to:

http://127.0.0.1:8080/predictions/my_tc

A prediction would be returned:
```
{ "tokens": [ "In", "1822", ",", "the", "18th", "president", "of", "the", "United", "States", ",", "Ulysses", "S.", "Grant", ",", "was", "born", "in", "Point", "Pleasant", ",", "Ohio" ], "entities": [ { "type": "Loc", "start": 8, "end": 10 }, { "type": "Peop", "start": 11, "end": 14 }, { "type": "Loc", "start": 18, "end": 22 } ], "relations": [ { "type": "Live_In", "head": 1, "tail": 2 } ] }
```

To test model trained on TAKE, post json like:
```
{"sentences":
    ["This item describes the requirement to disassemble the Port and Starboard Main Engine Clutch",
     "12K Main Engine Inspection",
     "This item describes the 12,000 hour scheduled maintenance of the starboard main propulsion diesel engines."]
     }
```




## References
```
Markus Eberts, Adrian Ulges. Span-based Joint Entity and Relation Extraction with Transformer Pre-training. 24th European Conference on Artificial Intelligence, 2020.
```
