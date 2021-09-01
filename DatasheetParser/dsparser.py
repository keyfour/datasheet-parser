import spacy

class DatasheetParser:

    def __init__(self, model="en_core_web_lg"):
        self._nlp = spacy.load(model)
    
    def get_entities(self, text):
        doc = self._nlp(text)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)