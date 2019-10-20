from pydocx import PyDocX
from docx import  Document

def parseDocx2html(filename):
      html = PyDocX.to_html('./paperPDF/' + filename)
      print(html)
      return html

def parseDocx(filename):
      document = Document('./paperPDF/' + filename)
      l = [ paragraph.text for paragraph in document.paragraphs];
      new_list = list(filter(not_empty,l))
      title = new_list[0]
      author = new_list[1]
      abstract =''
      for p in new_list:
            #rint (p)
            if 'abstract' in p or 'Abstract' in p:
                  abstract = p

      return title,author,abstract

def not_empty(s):
      return s and s.strip()


parseDocx('bitcoin.docx')