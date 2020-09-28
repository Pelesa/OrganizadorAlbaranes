from PIL import Image
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import re
import PyPDF2 as pdf2
import json
from types import SimpleNamespace


PDF_file= "example.pdf"
pages = convert_from_path(PDF_file, 600)

for page in pages:

    page.save("page0.pdf","PDF")
    basewidth = 600
    wpercent = (basewidth/float(page.size[0]))
    hsize = int((float(page.size[1])*float(wpercent)))
    page = page.resize((basewidth,hsize),Image.ANTIALIAS )
    page.save("page1.pdf",'PDF')