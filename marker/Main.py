from src.user_check import User_check
from src.training_xml_generator import Traning_xml_generator
import pandas as pd
import os
import glob
import shutil

done = 0
delet = 0
data = {"done":[done],"delet":[delet]}
df = pd.DataFrame.from_dict(data)
if os.path.isfile("./train/results.csv"):
    df = pd.read_csv("./train/results.csv")
    done = df.loc[0].done
    delet = df.loc[0].delet

if  not os.path.isdir("Resources"):
    os.mkdir("Resources")
    print("put your imgs in path Resources")
else:
    files_path = glob.glob('Resources\*.jpg')
    for img_path in files_path[0:]:

        if os.path.isfile(img_path):
            img_boxes_dataframe = pd.DataFrame()
            print("################## Starting User_check  ####################\n")
            user_check= User_check(img_path,img_boxes_dataframe)

            print('Click on [d] and use the Left_Button_Mouse to draw a new box.')
            print('Click on [r] and use the Left_Button_Mouse to resize a box.')
            print('Click on [t] and use the Left_Button_Mouse to clink inside a box and change its type.')
            print('Click on [l] to delete file')
            
            img_boxes_array, img_width_resized,img_height_resized,scale_percent,background = user_check.run()
            if img_boxes_array != 0:
                print("################## generating training xml  ####################\n")
                output_path='train/'
                generat = Traning_xml_generator(img_path,img_boxes_array,
                                        img_width_resized,img_height_resized,
                                        scale_percent,output_path).generator()
                _ ,tail = os.path.split(img_path)
                if  not os.path.isdir("done/"):
                    os.mkdir("done")
                if generat:
                    shutil.move(img_path, f"done/{tail}")
                    if os.path.isfile(f"{img_path[:-4]}.json"):
                        shutil.move(f"{img_path[:-4]}.json", f"done/{tail[:-4]}.json")
                    done+=1
            else :
                delet+=1

        data = {"done":[done],"delet":[delet]}
        df = pd.DataFrame.from_dict(data)
        df.to_csv("./train/results.csv")
        print(f"done: {done}")
        print(f"delet: {delet}")

_ = input("FIM")

