import docx
import os

doc = docx.Document('mytable.docx')
username = "ThomasTopuz"

c = 0
doc.paragraphs[9].text = username
for i in doc.paragraphs:
    print(i.text, c)
    c += 1

doc.save('mytable.docx')
