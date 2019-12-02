from pydocx import PyDocX
from docx import  Document
from dbext import db
from database import sentence
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
      sentens_list = []
      for p in new_list:
            sentens_list.append(p)
            if 'abstract' in p or 'Abstract' in p or 'ABSTRACT' in p:
                  abstract = p
      print(sentens_list)
      return title,author,abstract,sentens_list


def not_empty(s):
      return s and s.strip()

def process_sentences(paper_id, sentences):
    dbsession = DBsession()
    html_content = ''
    try:
        for pos,stc in enumerate(sentences):
            #print('pos:' + str(pos) + stc)
            if pos == 0:
                type = 'header'
                html_content+= '<h>'+stc+'</h>'
            else:
                html_content += '<p>' + stc + '</p>'
                type = 'text'
            new_sentences = sentence(pid=paper_id, pos=pos, sentence=stc, type=type)
            dbsession.add(new_sentences)
    except Exception as e:
        print('log:'+e)
        dbsession.rollback()
    dbsession.commit()
    return html_content
#parseDocx('bitcoin.docx')