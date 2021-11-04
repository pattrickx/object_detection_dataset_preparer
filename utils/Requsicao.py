import requests
import glob
import os

imgs_path = "./guias_com_json/"
out_path = "./guias_com_json/"

url = "http://0.0.0.0:5000/raw_text"

headers = {}
print('start')
if not os.path.exists(out_path):
    os.makedirs(out_path)
for n,img_path in enumerate(glob.glob(imgs_path+"*.pdf")):
    if os.path.isfile(img_path[:-4]+'.json'):
        continue
    print(f"{n}:{img_path}")
    payload = {'data':""}
    if os.path.isfile(img_path[:-4]+'.txt'):
        with open(img_path[:-4]+'.txt', 'r') as file:
            payload['data'] = file.read().replace('\n', '')
        
    print(payload)
    files=[
    ('file',(os.path.basename(img_path),open(img_path,'rb'),'image/jpeg'))
    ]

    response = requests.post( url, data=payload, files=files)
    print(response.text)
    with open(f"{out_path}{os.path.basename(img_path)[:-4]}.json", 'w') as f:
        f.write(response.text)
    

