import  json

paper = [{'id':231},{'id':2312}]
papers_json = {'title':'sdfs','papers':paper}
t=json.dumps(papers_json)
print(type(t))
print(t)