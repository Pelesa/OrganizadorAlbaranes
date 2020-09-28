import re


data ="PRPS et EE PE Oe ee ee ee \n Tractora 1234ABC \n Remolque O01234A"
print(data)
match=re.search(r'(\s+\d+\d+\d+\d+[A-Z]+[A-Z]+[A-Z]+\s)',data)
matricula=match.group(1).split(" ")[1]
print(matricula)