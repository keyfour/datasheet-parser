import pdfdownloader
import importlib.util
import sys
import os.path
import re
import manuf
import spacy
from spacy.matcher import PhraseMatcher
import time
startTime = time.time()

path = 'data/downloads/'

def tracktime(msg):
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime), msg)

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

tracktime("Modules are imported")

urls = get_urls()

tracktime("Got urls")

# print(url)
url = urls[1]
filename = path + url.split('/')[-1]
if not os.path.isfile(filename):
    p = pdfdownloader.PDFDownloader(url)
    p.download(path)
reader = module.PDFReader(filename)
text = reader.read()
text = re.sub(r'[^\x00-\x7F]+', ' ', text)
# sentences = [sentence for sentence in text.split(
#     '\n') if sentence != '' and len(sentence.split()) > 3]
tracktime("Got text")

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab)

tracktime("SpaCy initialized")

manufacturers = list(
    set(manuf.read_html('data/https _ru.mouser.com_manufacturer-category_.html')))

tracktime("Got vendors")

patterns = [nlp.make_doc(text) for text in manufacturers]
matcher.add("VENDOR", patterns)

tracktime("Matcher initialized")

doc = nlp(text)
sentences = doc.sents
# TODO: replace with spaCy Matcher
vendors = []
for sentence in sentences:
    sent = nlp(sentence.text)
    matches = matcher(sent)
    for match_id, start, end in matches:
        span = sent[start:end]
        vndr = (sent.text, [(span.start_char, span.end_char, nlp.vocab.strings[match_id])])
        vendors.append(vndr)
        tracktime("Found vendor")

print(vendors)

    # for manufacturer in manufacturers:
        # if manufacturer in sentence:
            # print("\n{0}\n{1}\n\n".format(manufacturer, sentence))
