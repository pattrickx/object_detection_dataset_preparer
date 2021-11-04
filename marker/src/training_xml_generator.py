import xml.etree.cElementTree as ET
import hashlib
import shutil
import os
class Traning_xml_generator:
    def __init__(self,img_path,boxes_array,img_width,img_height,scale_percent,output_path):
        self.img_path=img_path
        self.boxes_array=boxes_array
        self.img_width=img_width
        self.img_height=img_height
        self.scale_percent=scale_percent
        self.output_path=output_path
    def area(self,rec):
        xi,yi =rec[0]
        xf,yf =rec[1]
        W = xf-xi
        H = yf-yi
        return W*H
    def generator(self):
        x=int(self.img_width/self.scale_percent)
        y=int(self.img_height/self.scale_percent)

        hasher = hashlib.md5()
        Hash=''
        with open(self.img_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
            Hash = hasher.hexdigest()

        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "filename").text =  Hash+".jpg"
        size = ET.SubElement(annotation, "size")
        ET.SubElement(annotation, "segmented").text = "0"
        ET.SubElement(size, "width").text = str(x)
        ET.SubElement(size, "height").text = str(y)
        ET.SubElement(size, "depth").text = str("3")
        for i in  self.boxes_array:
           
            if self.area(i)>25 and i[2] !="":
                x1,y1=i[0] if i[0][0]<i[1][0] else i[1]
                x2,y2=i[1] if i[0][0]<i[1][0] else i[0]
                object = ET.SubElement(annotation, "object")
                ET.SubElement(object, "name").text = i[2]
                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(int(x1/self.scale_percent)) if int(x1/self.scale_percent) >0 else "1"
                ET.SubElement(bndbox, "ymin").text = str(int(y1/self.scale_percent)) if int(y1/self.scale_percent) >0 else "1"
                ET.SubElement(bndbox, "xmax").text = str(int(x2/self.scale_percent)) if int(x2/self.scale_percent) <x else str(x-1)
                ET.SubElement(bndbox, "ymax").text = str(int(y2/self.scale_percent)) if int(y2/self.scale_percent) <y else str(y-1)
        if len(annotation)>3:
            tree= ET.ElementTree(annotation)
            if not os.path.isdir(self.output_path):
                os.mkdir(self.output_path)
            tree.write(f'{self.output_path}{Hash}.xml')
            shutil.copy(self.img_path, f'{self.output_path}{Hash}.jpg')
            return True
        return False
        