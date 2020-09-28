
from PIL import Image 
from pdf2image import convert_from_path
import os

#Pdf to image

# PDF_file = "example.pdf"
# pages = convert_from_path(PDF_file, 600)
# page = pages[0]
# image = "page_1"+".jpg"
# page.save(image, 'JPEG')

# Opens a image in RGB mode 
im = Image.open("TEST/example.jpg")
  
width, height = im.size
# Cropped image of above dimension 
# (It will not change orginal image) 
print(width, height)
matricula = im.crop((0, height*0.461933, width*0.6773, height*0.513259)) 
fecha = im.crop((width*0.854862,0,width,height*0.06843456))

hora = im.crop((width*0.88,height*0.063,width,height*0.09))

# Shows the image in image viewer 
matricula.show() 
fecha.show()
hora.show()
#Guarda la imagen
#matricula.save("matricula.jpg",'JPEG')
#fecha.save("fecha.jpg",'JPEG')
#hora.save("hora.jpg",'JPEG')



