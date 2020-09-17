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

class Albaran:
    def __init__(self,matricula,fecha,hora):
        self.matricula = matricula
        self.fecha = fecha
        self.hora = hora
 
    def __str__(self):
        return str(self.matricula+", "+str(self.fecha)+", "+str(self.hora))
    
    def __dict__(self):
        dictio={
            self.matricula: 
                { 
                    "horas": [self.hora]
                }
            }
        return dictio


def guardar(albaran):

    fecha = "/".join(albaran.fecha)
    matricula = albaran.matricula

    au="au.pdf"
    nombre=albaran.matricula+".pdf"
    datajson = "data.json"

    path = "/".join((config.invoice_path, fecha, nombre))
    au_path = "/".join((config.invoice_path, fecha, au))
    json_path = "/".join((config.invoice_path, fecha,datajson))

    page.save(au_path,'PDF') 
    
    if os.path.isfile(json_path)==False:
        f= open(json_path,"w+")
        f.write("{}")
        f.close()

    #JSON -> Python
    with open(json_path) as json_file:
        data = json.load(json_file)
    
    if albaran.matricula in data.keys() and os.path.exists(path):
        if albaran.hora not in data[albaran.matricula]["horas"]:
            data[albaran.matricula]["horas"].append(albaran.hora)

            merger = pdf2.PdfFileMerger()
            foo=open(au_path, 'rb')
            merger.append(pdf2.PdfFileReader(open(path, 'rb')))
            merger.append(pdf2.PdfFileReader(foo))
            merger.write(path)
            foo.close()
            os.remove(au_path)

    else:
        data[albaran.matricula] = {"horas": [albaran.hora]}
        print("Nueva Matricula " + path )
        os.rename(au_path,path) 

    with open(json_path,"r+") as file:
        json.dump(data, file)       



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

    width, height = page.size
    matricula = page.crop((0, height*0.461933, width*0.6773, height*0.513259)) 
    fecha = page.crop((width*0.854862,0,width,height*0.06843456))
    hora = page.crop((width*0.88,height*0.063,width,height*0.09))

    # Increment the counter to update filename 
    image_counter = image_counter + 1
          
    # Recognize the text as string in image using pytesserct 


    fechaTXT=str(pytesseract.image_to_string(fecha))
    matriculaTXT=str(pytesseract.image_to_string(matricula))
    horaTXT=str(pytesseract.image_to_string(hora))
   
    #Busca fecha
    match=re.search(r'(\d+/\d+/\d+)',fechaTXT)
    date=match.group(1)
    date = date.split("/")
    rev_date = date
    rev_date.reverse()

    #Busca Matricula
    try:
        match=re.search(r'(\s+\d+\d+\d+\d+[A-Z]+[A-Z]+[A-Z])',matriculaTXT)
        matricula=match.group(1)
        
    except AttributeError:
        err = True
        matricula="errores"    
    
    
    #TODO Excepciones hora y fecha??

    #Busca Hora
    match=re.search(r'(\d+:\d+:\d+)',horaTXT)
    hora=match.group(1)
        

    albaran = Albaran(matricula,date,hora)
    print(albaran)

    #Creamos las carpetas
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
    
    guardar(albaran)

