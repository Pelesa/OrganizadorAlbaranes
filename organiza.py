# Import libraries 
from PIL import Image
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import re
import PyPDF2 as pdf2
import json
from types import SimpleNamespace

with open('configuration.json') as f:
  config = json.load(f)
  config = SimpleNamespace(**config)


def guardar(fecha,matricula,imagen):
    fecha = "/".join(fecha)
    au="au.pdf"
    nombre=matricula+".pdf"
    path = "/".join((config.invoice_path, fecha, nombre))
    au_path = "/".join((config.invoice_path, fecha, au))
    page.save(au_path,'PDF') 
    print("Existe carpeta?"+ str(os.path.exists(path)))
    if os.path.exists(path):
        merger = pdf2.PdfFileMerger()
        foo=open(au_path, 'rb')
        merger.append(pdf2.PdfFileReader(open(path, 'rb')))
        merger.append(pdf2.PdfFileReader(foo))
        merger.write(path)
        foo.close()
        os.remove(au_path)
    else:
        print("Nueva Matricula " + path )
        os.rename(au_path,path) 

# Path of the pdf 
PDF_file = "example.pdf"
  
''' 
Part #1 : Converting PDF to images 
'''
if os.name == 'nt': pytesseract.pytesseract.tesseract_cmd = config.tesseract
# Store all the pages of the PDF in a variable 
pages = convert_from_path(PDF_file, 600) 

# Counter to store images of each page of PDF to image 
image_counter = 1


# Iterate through all the pages stored above 
for page in pages: 
    err=False
    imageMatricula = "page_"+str(image_counter)+"matricula"+".jpg"
    imageFecha = "page_"+str(image_counter)+"fecha"+".jpg"
    width, height = page.size
    matricula = page.crop((0, height*0.461933, width*0.6773, height*0.513259)) 
    fecha = page.crop((width*0.854862,0,width,height*0.06843456))

    # Increment the counter to update filename 
    image_counter = image_counter + 1
          
    # Recognize the text as string in image using pytesserct 
    text = str(((pytesseract.image_to_string(matricula))
                + "\n" +((pytesseract.image_to_string(fecha))
            ))) 
    
    #Busca fecha
    match=re.search(r'(\d+/\d+/\d+)',text)
    date=match.group(1)
    date = date.split("/")
    print(date)
    rev_date = date
    rev_date.reverse()

    try:
        path = config.invoice_path
        if not os.path.exists(path): os.mkdir(path)
        for dig in rev_date:
            path = "/".join((path, dig))
            if not os.path.exists(path):os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    
    try:
        match=re.search(r'(\s+\d+\d+\d+\d+[A-Z]+[A-Z]+[A-Z])',text)
        matricula=match.group(1)
        print(matricula)
    except AttributeError:
        err = True
        matricula="errores"
             
    print("Matricula: %s" % matricula)
    guardar(date,matricula,page)
