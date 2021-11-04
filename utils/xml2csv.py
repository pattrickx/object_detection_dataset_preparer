from os import lseek
import pandas  as pd
import xmltodict
my_xml =""
with open('79df5927-236b-48fe-b144-ff7e89casa7_jpg.rf.350b12c0c1927d7fd70109094f921f40.xml','r') as f:
    for line in f:
        my_xml+=line.strip()

# print(my_xml)

json_box = xmltodict.parse(my_xml)

list_box =[]
w_template = int(json_box["annotation"]["size"]["width"])
h_template = int(json_box["annotation"]["size"]["height"])
for box in json_box["annotation"]["object"]:
    id =int(box['name'].split("-")[0])
    x1 = int(box["bndbox"]["xmin"])
    y1 = int(box["bndbox"]["ymin"])
    x2 = int(box["bndbox"]["xmax"])
    y2 = int(box["bndbox"]["ymax"])
    w = x2-x1
    h = y2-y1

    x1 /= w_template
    y1 /= h_template
    x2 /= w_template
    y2 /= h_template
    w /= w_template
    h /= h_template


    list_box.append([box['name'],x1,y1,x2,y2,w,h,id])

df_box = pd.DataFrame(columns=["tag","x1","y1","x2","y2","w","h","id"],data=list_box)
df_box.to_csv('box_tamanho_posicao_relativo.csv', index=False)
print(df_box)

# sudo pip3 install pandas
# sudo pip3 install xmltodict
# sudo apt install python-xmltodict