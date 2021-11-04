from pdf2image import convert_from_bytes
import os
import glob
pdf_path = "guias_sistema/guias/"
def convert(file, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    pages = convert_from_bytes(open(file, 'rb').read(), 500)
    counter = 1
    for page in pages:
        myfile = outputDir + f"{str(counter)}_"+os.path.basename(file)[:-4] +'.jpg'
        counter = counter + 1
        page.save(myfile, "JPEG")


for File in glob.glob(pdf_path+"*.pdf"):
    convert(File, pdf_path)
    os.remove(File)
#pip install pdf2image
#sudo apt-get install -y poppler-utils