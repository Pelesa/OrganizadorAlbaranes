# Import libraries 
from PIL import Image
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import re
import PyPDF2 as pdf2

def guardar(fecha,matricula,imagen):
    au="au.pdf"
    nombre=matricula+".pdf"
    os.chdir("./"+fecha)

    page.save(au,'PDF') 
    output = pdf2.PdfFileWriter()
    
    print("Existe carpeta?"+ str(os.path.exists(nombre)))

    if os.path.exists(nombre):
        merger = pdf2.PdfFileMerger()
        foo=open(au, 'rb')
        merger.append(pdf2.PdfFileReader(open(nombre, 'rb')))
        merger.append(pdf2.PdfFileReader(foo))
        merger.write(nombre)
        
        foo.close()
        os.remove(au)
    else:
        print("Nueva Matricula " + nombre )
        os.rename(au,nombre) 

    
    os.chdir("..")



# Path of the pdf 
PDF_file = "example.pdf"
  
''' 
Part #1 : Converting PDF to images 
'''
pytesseract.pytesseract.tesseract_cmd = 'C:/Users/jlf799/AppData/Local/Tesseract-OCR/tesseract.exe'
# Store all the pages of the PDF in a variable 
pages = convert_from_path(PDF_file, 500) 

# Counter to store images of each page of PDF to image 
image_counter = 1
  

# Iterate through all the pages stored above 
for page in pages: 
    err=False

    imageMatricula = "page_"+str(image_counter)+"matricula"+".jpg"
    imageFecha = "page_"+str(image_counter)+"fecha"+".jpg"
    
    width, height = page.size
    matricula = page.crop((0, 2700, 2800, 3000)) 
    fecha = page.crop((width-600,0,width,400))  


    # Increment the counter to update filename 
    image_counter = image_counter + 1
          
    # Recognize the text as string in image using pytesserct 
    text = str(((pytesseract.image_to_string(matricula))
                + "\n" +((pytesseract.image_to_string(fecha))
            ))) 
    
    #Busca fecha
    match=re.search(r'(\d+/\d+/\d+)',text)
    date=match.group(1)
    date=date.replace('/', '')
    print("Fecha: "+ date)


    path="./" + date
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    

    try:
        match=re.search(r'(\s+\d+\d+\d+\d+[A-Z]+[A-Z]+[A-Z])',text)
        matricula=match.group(1)
    except AttributeError:
        err = True
        matricula="errores"
        
        
    print("Matricula: %s" % matricula)

    guardar(date,matricula,page)
