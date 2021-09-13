import pdfdownloader

url = ['http://www.nxp.com/docs/en/data-sheet/MC34673.pdf',
'http://ww1.microchip.com/downloads/en/DeviceDoc/22036b.pdf',
'http://ww1.microchip.com/downloads/en/DeviceDoc/20001984g.pdf',
'http://www.mouser.com/ds/2/268/22090a-52174.pdf',
'http://www.silabs.com/support%20documents/technicaldocs/cp2102n-datasheet.pdf',
'https://www.silabs.com/Support%20Documents/TechnicalDocs/cp2104.pdf',
'http://www.silabs.com/Support%20Documents/TechnicalDocs/CP2112.pdf',
'https://www.silabs.com/documents/public/data-sheets/efm8bb1-datasheet.pdf',
'http://www.mouser.com/ds/2/368/si3210-38974.pdf']
# url = 'https://www.silabs.com/documents/public/data-sheets/efm8bb1-datasheet.pdf'

p = pdfdownloader.PDFDownloader(url)
p.download(url)