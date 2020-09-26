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
    def __init__(self,matricula,fecha,hora,page):
        self.matricula = matricula
        self.fecha = fecha
        self.hora = hora
        self.page = page
 
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

    au="au.pdf"
    nombre=albaran.matricula+".pdf"
    datajson = "data.json"

    path = "/".join((config.invoice_path, fecha, nombre))
    au_path = "/".join((config.invoice_path, fecha, au))
    json_path = "/".join((config.invoice_path, fecha,datajson))

    albaran.page.save(au_path,'PDF') 
    
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
            os.remove(au_path)
    else:
        data[albaran.matricula] = {"horas": [albaran.hora]}
        #print("Nueva Matricula " + path )
        os.rename(au_path,path) 

    with open(json_path,"r+") as file:
        json.dump(data, file)




def main(PDF_file):
    ''' 
    Part #1 : Converting PDF to images 
    '''


    if os.name == 'nt': pytesseract.pytesseract.tesseract_cmd = config.tesseract
    # Store all the pages of the PDF in a variable 
    page = convert_from_path(PDF_file, 600) 
    page=page[0]


    err=False

    width, height = page.size
    matricula = page.crop((0, height*0.461933, width*0.6773, height*0.513259)) 
    fecha = page.crop((width*0.854862,0,width,height*0.06843456))
    hora = page.crop((width*0.88,height*0.063,width,height*0.09))
        
    # Recognize the text as string in image using pytesserct 

    fechaTXT=str(pytesseract.image_to_string(fecha))
    matriculaTXT=str(pytesseract.image_to_string(matricula))
    horaTXT=str(pytesseract.image_to_string(hora))

    #Busca fecha
    try:
        match=re.search(r'(\d+/\d+/\d+)',fechaTXT)
        date=match.group(1)
        date = date.split("/")
        rev_date = date
        rev_date.reverse()
    except AttributeError:
        date = "00/00/00"
        date = date.split("/")
        rev_date = date
        rev_date.reverse()

    #Busca Hora
    try:
        match=re.search(r'(\d+:\d+:\d+)',horaTXT)
        hora=match.group(1)
    except AttributeError:
        hora= "00:00:00"

    #Busca Matricula
    try:
        match=re.search(r'(\s+\d+\d+\d+\d+[A-Z]+[A-Z]+[A-Z])',matriculaTXT)
        matricula=match.group(1).split(" ")[1]
        
    except AttributeError:
        err = True
        matricula="errores"
        try:
            match=re.search(r'(\s+[O]+[0]+\d+\d+\d+[A-Z]+[A-Z]+[A-Z])',matriculaTXT)
            matricula=match.group(1).split("O")[1]
            err = False
        except AttributeError:
            err = True
            #print("Error matricula :"+" : \n" + matriculaTXT)
            matricula="errores"

    #Escalamos la imagen
    basewidth = 600
    wpercent = (basewidth/float(page.size[0]))
    hsize = int((float(page.size[1])*float(wpercent)))
    page = page.resize((basewidth,hsize),Image.ANTIALIAS )
            
    
    albaran = Albaran(matricula,date,hora,page)
    #if err:
    #    print(albaran)

    #Creamos las carpetas
    try:
        path = config.invoice_path
        if not os.path.exists(path): os.mkdir(path)
        for dig in rev_date:
            path = "/".join((path, dig))
            if not os.path.exists(path):os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    # else:
    #     print ("Successfully created the directory %s " % path)
    
    guardar(albaran)

