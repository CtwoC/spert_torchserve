
#%%
#windows system
# import sys
# import subprocess
# def call(command:str, shell=True):
#     PLATFORM = str(sys.platform).lower()
#     shell = 'win32' in PLATFORM

#     _command = command.split()
#     return subprocess.run(_command, check=True, shell=shell, stdout=subprocess.PIPE,capture_output=False)
# if __name__=='__main__':
#     call('torch-model-archiver --model-name spert_TAKE --version 1.0 --model-file models.py --serialized-file model/TAKE_20201204/pytorch_model.bin --export-path model_store --extra-files entities.py,input_reader.py,loss.py,prediction.py,sampling.py,types.json --handler spert_handler_TAKE')

#mac

import subprocess
def call(command:str):
    _command = command.split()
    return subprocess.run(_command)
if __name__=='__main__':
    call('torch-model-archiver --model-name spert_TAKE --version 1.0 --model-file models.py --serialized-file model/TAKE_20201204/pytorch_model.bin --export-path model_store --extra-files entities.py,input_reader.py,loss.py,prediction.py,sampling.py,model/TAKE_20201204/types.json,model/TAKE_20201204/config.json,model/TAKE_20201204/special_tokens_map.json,model/TAKE_20201204/tokenizer_config.json,model/TAKE_20201204/vocab.txt --handler spert_handler_TAKE')

# %%
# import click
# import sys
# import subprocess
# import os
# from os import path

# @click.command()
# @click.option("--model_dir", prompt="Model directory")
# @click.option("--model_name", prompt="Model directory")
# @click.option("--model_version", prompt="Model directory")
# @click.option("--handler", prompt="Model directory")
# @click.option("--types_file", prompt="Model directory")


# def call(model_name,model_version,model_dir,types_file,handler):
#     #check components
#     components=["entities.py","models.py","prediction.py","sampling.py","models.py","input_reader.py"]
#     for component in components:
#         report="components prepared"
#         if not path.exists(component):
#             report=component+" "+"missing"
#             print(report)
#             break
#     print(report)
#     #check export path
#     if not path.isdir("model_store"):
#         os.mkdir("model_store")
#     #arguments
#     model_name = f"{model_name}"
#     model_dir = f"{model_dir}" + "/pytorch_model.bin"
#     model_version= f"{model_version}"
#     types_file=f"{types_file}"
#     handler=f"{handler}"

#     _command=["torch-model-archiver",
#               "--model-name",
#               model_name,
#               "--version",
#               model_version,
#               "--model-file",
#               "models.py",
#               "--serialized-file", 
#               model_dir,
#               "--export-path",
#               "model_store",
#               "--extra-files",
#               "entities.py,input_reader.py,loss.py,prediction.py,sampling.py"+types_file,
#               "--handler",
#               handler]

#     return subprocess.run(_command)

# if __name__ == '__main__':
#     call()
#%%

# %%
