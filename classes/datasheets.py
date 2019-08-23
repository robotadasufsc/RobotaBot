from googlesearch import search

#from classes.types import ComponentDatasheet

class Datasheets:
    def __init__(self, component):
        self.google_url = 'http://www.google.com/search?q={0}&num=100&hl=en&start=0'

        self.sheets = self.get_datasheets(component)


    def get_datasheets(self, component):
        sheets = []
        results = search('filetype:pdf datasheet ' + component, stop=5)

        for result in results:
            print(result)
            sheets.append(result)

        return sheets

