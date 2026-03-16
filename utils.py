def read_htmlFile(html_file):
    with open(html_file,'r',encoding='utf=8') as f:
        return f.read()