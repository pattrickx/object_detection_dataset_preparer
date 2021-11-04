import pandas as pd
import os
import glob
import shutil
import xml.etree.ElementTree as ET
files_path = glob.glob('./train/train old/*.jpg')
# files_path = glob.glob('C:/Users/pattr/OneDrive - Fundação Edson Queiroz - Universidade de Fortaleza/Área de Trabalho/train iaggo/*.jpg')

img_boxes_dataframe = pd.DataFrame(columns=['class','x1','y1','x2','y2'])
for img_path in files_path:

    if os.path.isfile(img_path):
        root = ET.parse(img_path[:-4]+'.xml').getroot()
        objs = root.findall('object')
        reactangles=[]
        
        for obj in objs:
            # for subelem in elem:
            try:
                img_boxes_dataframe=img_boxes_dataframe.append({'class':obj.find('name').text.split('.')[-1],
                    'x1':int(int(obj.find('bndbox').find('xmin').text)),
                    'y1':int(int(obj.find('bndbox').find('ymin').text)),
                    'x2':int(int(obj.find('bndbox').find('xmax').text)),
                    'y2':int(int(obj.find('bndbox').find('ymax').text))},
                    ignore_index=True)
                # if(obj.find('name').text.split('.')[-1]=="ScrollView"):
                #     _ ,tail = os.path.split(img_path)
                #     print(f"imagem: {tail}")

            except:
                _ ,tail = os.path.split(img_path)
                print(f"imagem: {tail} marcação sem tipo")

            

final = img_boxes_dataframe.groupby("class").count().sort_values(by=['x1'],ascending=False).x1


print("Quantidade de marcações por tipo:")
print(final)
print()
print(f"numero de imagens: {len(files_path)}")
print(f"Numero de marcações: {final.sum()}")
_ = input("Fim")