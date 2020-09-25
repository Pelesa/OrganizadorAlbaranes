import organiza
import gmailAPI_pdf
import os


pathPDFS="email_pdfs"
#Metodo llamada a readmail (Futuro bucle cada dia por ejemplo)
gmailAPI_pdf.main(pathPDFS)


#Metodo llama a organiza.py por cada pdf en "email_pdf" 
#Manda el nombre del pdf como arg

pdfs = os.listdir(pathPDFS)
for pdf in pdfs:
    print("Leyendo "+os.path.join(pathPDFS, pdf))

    organiza.main(os.path.join(pathPDFS, pdf))
    pathleidos=os.path.join(pathPDFS,"leidos")
    if not os.path.exists(pathleidos): os.mkdir(pathleidos)
    print("Leido, moviendo a "+pathleidos)
    os.replace(os.path.join(pathPDFS, pdf),os.path.join(pathleidos, pdf))





