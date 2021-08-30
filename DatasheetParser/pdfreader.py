from PyPDF2 import PdfFileReader


class PDFReader:

    def __init__(self, path):
        self._path = path

    def read(self):
        text = ""
        try:
            input = PdfFileReader(open(self._path, "rb"))
            for page in input.pages:
                text = text + page.extractText().replace('\\n', "")
        except Exception as ex:
            print(ex)
        return text
