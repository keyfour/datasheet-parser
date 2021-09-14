import pdfdownloader
import importlib.util
import sys
import os.path
import re
import manuf

path = 'data/downloads/'


def get_urls():
    lines = []
    with open("data/kicad_datasheets_list.txt", "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


spec = importlib.util.spec_from_file_location(
    'DatasheetParser.pdfreader', 'DatasheetParser/pdfreader.py')
module = importlib.util.module_from_spec(spec)
sys.modules['pdfreader'] = module
spec.loader.exec_module(module)
dir(module.PDFReader)

urls = get_urls()

# print(url)
url = urls[1]
filename = path + url.split('/')[-1]
if not os.path.isfile(filename):
    p = pdfdownloader.PDFDownloader(url)
    p.download(path)
reader = module.PDFReader(filename)
text = reader.read()
text = re.sub(r'[^\x00-\x7F]+', ' ', text)
sentences = [sentence for sentence in text.split(
    '\n') if sentence != '' and len(sentence.split()) > 3]

manufacturers = list(
    set(manuf.read_html('data/https _ru.mouser.com_manufacturer-category_.html')))

# TODO: replace with spaCy Matcher
for sentence in sentences:
    for manufacturer in manufacturers:
        if manufacturer in sentence:
            print("\n{0}\n{1}\n\n".format(manufacturer, sentence))
