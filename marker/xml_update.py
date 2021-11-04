
from src.user_check import User_check
from src.training_xml_generator import Traning_xml_generator
import pandas as pd
import os
import glob
import shutil
import xml.etree.ElementTree as ET
if  not os.path.isdir("Resources"):
    os.mkdir("Resources")
    print("put your imgs in path Resources")
else:
    files_path = glob.glob('train/*.jpg')
    for img_path in files_path[0:]:

        if os.path.isfile(img_path):
            root = ET.parse(img_path[:-4]+'.xml').getroot()
            objs = root.findall('object')
            reactangles=[]
            img_boxes_dataframe = pd.DataFrame(columns=['class','x1','y1','x2','y2'])
            for obj in objs:
                # for subelem in elem:
                try:
                    

                    img_boxes_dataframe=img_boxes_dataframe.append({'class':obj.find('name').text.split('.')[-1],
                    'x1':int(int(obj.find('bndbox').find('xmin').text)),
                    'y1':int(int(obj.find('bndbox').find('ymin').text)),
                    'x2':int(int(obj.find('bndbox').find('xmax').text)),
                    'y2':int(int(obj.find('bndbox').find('ymax').text))},
                    ignore_index=True)
                except:
                    _ ,tail = os.path.split(img_path)
                    print(f"imagem: {tail} marcação sem tipo")



            
            print("################## Starting User_check  ####################\n")
            user_check= User_check(img_path,img_boxes_dataframe)

            print('Click on [d] and use the Left_Button_Mouse to draw a new box.')
            print('Click on [r] and use the Left_Button_Mouse to resize a box.')
            print('Click on [t] and use the Left_Button_Mouse to clink inside a box and change its type.')
            print('Click on [l] to delete file')
            
            img_boxes_array, img_width_resized,img_height_resized,scale_percent,background = user_check.run()
            if img_boxes_array != 0:
                print("################## generating training xml  ####################\n")
                p ,tail = os.path.split(img_path)
                output_path=f"{p}/done/"
                if  not os.path.isdir(output_path):
                    os.mkdir(output_path)
                
                Traning_xml_generator(img_path,img_boxes_array,
                                        img_width_resized,img_height_resized,
                                        scale_percent,output_path).generator()
                if os.path.isfile(f"./{img_path}"):
                    os.remove(f"./{img_path}")
                    os.remove(f"./{img_path[:-4]}.xml")
                # shutil.move(img_path, f"done/{tail}")
                # if os.path.isfile(f"{img_path[:-4]}.xml"):
                #     shutil.move(f"{img_path[:-4]}.xml", f"{p}/done/{tail[:-4]}.xml")


