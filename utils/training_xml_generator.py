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
        
    def generator(self):
        x=int(self.img_width)
        y=int(self.img_height)

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
        for n,r in  self.boxes_array.iterrows():
        
            object = ET.SubElement(annotation, "object")
            ET.SubElement(object, "name").text = r['class']
            bndbox = ET.SubElement(object, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(r["xmin"])
            ET.SubElement(bndbox, "ymin").text = str(r["ymin"])
            ET.SubElement(bndbox, "xmax").text = str(r["xmax"])
            ET.SubElement(bndbox, "ymax").text = str(r["ymax"])

        
        tree= ET.ElementTree(annotation)
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        tree.write(f'{self.output_path}{Hash}.xml')
        shutil.copy(self.img_path, f'{self.output_path}{Hash}.jpg')
        return True
        