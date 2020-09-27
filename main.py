from __future__ import print_function
import organiza
import gmailAPI_pdf
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from glob import glob
from progress.bar import Bar
from PIL import Image
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import re
import json
from types import SimpleNamespace
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


if __name__ == '__main__':
    pathPDFS="email_pdfs"
    #Metodo llamada a readmail (Futuro bucle cada dia por ejemplo)
    gmailAPI_pdf.main(pathPDFS)


    pdfs = glob(os.path.join(pathPDFS,"*.{}".format("pdf")))
    print(pdfs)
    #Dividir todos los PDF importados en pdf de 1 hoja
    for pdf in pdfs:
        
        with open(pdf,"rb") as pdfabierto:
            pdfdivide=PdfFileReader(pdfabierto)
            for i in range(pdfdivide.numPages):
                output = PdfFileWriter()
                output.addPage(pdfdivide.getPage(i))
                with open(pdf.split(".")[0]+ "_%s" % i +".pdf", "wb") as outputStream:
                    output.write(outputStream)

        pathleidos=os.path.join(pathPDFS,"leidos")
        if not os.path.exists(pathleidos): os.mkdir(pathleidos)
        print("Leido, moviendo a "+pathleidos)
        os.replace(pdf,os.path.join(pathleidos, pdf.split(os.sep)[1]))




    pdfs = glob(os.path.join(pathPDFS,"*.{}".format("pdf")))
    #print(pdfs)

    bar = Bar("Ordenando:", max=len(pdfs))
    #Metodo llama a organiza.py por cada pdf en "email_pdf" 
    #Manda el nombre del pdf como arg
    for pdf in pdfs:
        #print("Leyendo "+os.path.join(pdf))
        bar.next()
        organiza.main(os.path.join(pdf))
        os.remove(os.path.join(pdf))
    bar.finish()

    for leidos in os.listdir(pathleidos):
        os.remove(os.path.join(pathleidos, leidos))
    os.rmdir(pathleidos)