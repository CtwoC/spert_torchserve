#%%
from pytz import utc
import time
import os
import boto3
import shutil
import subprocess
import time
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

bucketname = "modelbucket1"
access_key = "AKIA5TAGCAKW2EDMS2UF"
access_sercret = "Y1QYoj78gbRoCvfJrp4SzLYDfQIxERmE9B1iWddy"

s3 = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=access_sercret)



def version_check():
    s3.download_file('modelbucket1', 'registory.json', 'registory_cache.json')

    with open('registory_cache.json') as json_file:
        data = json.load(json_file)

    latest_version=data["relation-extraction"]["version"]

    with open('registory.json') as json_file:
        data = json.load(json_file)

    last_version=data["relation-extraction"]["version"]

    print("check_version")

    #update service if new version found
    if latest_version!=last_version:
        print("New version found, update from "+last_version+" to "+latest_version)
        #update registory
        shutil.copy2('registory_cache.json', 'registory.json') # complete target filename given

        #download latest model
        s3.download_file('modelbucket1', 'model_store/'+latest_version+'.mar', 'model_store/'+latest_version+'.mar')

        #stop the serve
        subprocess.run("torchserve --stop".split())

        #start a new serve
        command='torchserve --start --model-store model_store --models spert=' + latest_version + '.mar --ncs'
        subprocess.run(command.split())
    
    else:
        print("version: "+last_version)


if __name__ == '__main__':
    #initialize service
    if not os.path.exists('model_store'):
        print("Model first served")
        os.makedirs('model_store')

        # download latest registory json from s3
        s3.download_file('modelbucket1', 'registory.json', 'registory_cache.json')
        
    else:
        print("Continue last serve")

    #load version information
    with open('registory_cache.json') as json_file:
        data = json.load(json_file)

    latest_version=data["relation-extraction"]["version"]
    shutil.copy2('registory_cache.json', 'registory.json') 
    #download model
    s3.download_file('modelbucket1', 'model_store/'+latest_version+'.mar', 'model_store/'+latest_version+'.mar')
    command='torchserve --start --model-store model_store --models spert=' + latest_version + '.mar --ncs'
    subprocess.run(command.split())
    
    #check and serve new version
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(version_check, 'interval', seconds=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


# %%
from pytz import utc
import time
import os
import boto3
import shutil
import subprocess
import time
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

bucketname = "modelbucket1"
access_key = "AKIA5TAGCAKW2EDMS2UF"
access_sercret = "Y1QYoj78gbRoCvfJrp4SzLYDfQIxERmE9B1iWddy"

s3 = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=access_sercret)

class spert_serve():
    def __init__(self,bucketname,s3):
        self.bucketname=bucketname
        self.s3=s3
        #initialize service
        if not os.path.exists('model_store'):
            print("Model first served")
            os.makedirs('model_store')

            # download latest registory json from s3
            s3.download_file(bucketname, 'registory.json', 'registory_cache.json')
            
        else:
            print("Continue last serve")

        #load version information
        with open('registory_cache.json') as json_file:
            data = json.load(json_file)

        latest_version=data["relation-extraction"]["version"]
        shutil.copy2('registory_cache.json', 'registory.json') 
        #download model
        s3.download_file('modelbucket1', 'model_store/'+latest_version+'.mar', 'model_store/'+latest_version+'.mar')
        command='torchserve --start --model-store model_store --models spert=' + latest_version + '.mar --ncs'
        subprocess.run(command.split())

    def version_check(self):
        self.s3.download_file(self.bucketname, 'registory.json', 'registory_cache.json')

        with open('registory_cache.json') as json_file:
            data = json.load(json_file)

        latest_version=data["relation-extraction"]["version"]

        with open('registory.json') as json_file:
            data = json.load(json_file)

        last_version=data["relation-extraction"]["version"]

        print("check_version")

        #update service if new version found
        if latest_version!=last_version:
            print("New version found, update from "+last_version+" to "+latest_version)
            #update registory
            shutil.copy2('registory_cache.json', 'registory.json') # complete target filename given

            #download latest model
            self.s3.download_file('modelbucket1', 'model_store/'+latest_version+'.mar', 'model_store/'+latest_version+'.mar')

            #stop the serve
            subprocess.run("torchserve --stop".split())

            #start a new serve
            command='torchserve --start --model-store model_store --models spert=' + latest_version + '.mar --ncs'
            subprocess.run(command.split())
        
        else:
            print("version: "+last_version)

if __name__ == '__main__':
    #init
    serve1=spert_serve(bucketname,s3)
    time.sleep(10)
    
    #check and serve new version
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(serve1.version_check, 'interval', seconds=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
# %%
serve1.version_check()
# %%
