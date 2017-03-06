'''

    This is going to be written in Python 3.6

'''
from html.parser import HTMLParser
import sys, os

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.docDic = {}
        self.docDic["pageContent"] = [[]]
        self.currentItem = None
        self.currentTag = None
        self.parentTag = None


    def handle_starttag(self, tag, attrs):
        if tag.lower() != "center" and tag.lower() != "a":
            if tag == "ol"  or tag == "ul" and self.parentTag == None:
                self.parentTag = tag
                if tag == "ol":
                    self.currentItem = {"ordered_list": []}
                else:
                    self.currentItem = {"unordered_list": []}
            elif tag == "li":
                self.currentTag = "li"
            else:
                self.currentTag = tag.lower()
                self.currentItem = { str(tag.lower()) : []}
                if len(attrs) == 0:
                    self.currentItem[str(tag.lower())].append("None")
                else:
                    attrDic = {}
                    for i in attrs:
                        attrDic[str(i[0])] = str(i[1])
                    self.currentItem[str(tag.lower())].append(attrDic)

    def handle_endtag(self, tag):
        if self.currentItem != None:
            self.docDic["pageContent"][0].append(self.currentItem)
        self.currentItem = None
        self.currentTag = None

    def handle_data(self, data):
        if self.parentTag != None:
            if self.currentTag == "li":
                if self.parentTag == "ol":
                    key = "ordered_list"
                else:
                    key = "unordered_list"
                if key in self.currentItem.keys():
                    self.currentItem[key].append(data.rstrip())
        elif self.currentTag != None:
            if data != "":
                self.currentItem[ self.currentTag ].append(data)
            else:
                self.currentItem[ self.currentTag ].append("None")

    def exportData(self, fileName):
        dataString = "{\n'pageContent':\n\t[\n\t\t[\n"
        for i in self.docDic["pageContent"][0]:
            dataString += "\t\t\t" + str(i) + ",\n"
        dataString += "\t\t]\n\t]\n}"
        file = open(fileName, 'w')
        file.write(dataString)

if len(sys.argv) == 3:
    if os.path.isfile(sys.argv[1]):
        file = open(sys.argv[1], 'r')
        data = file.read()
    else:
        raise Exception("Input File does not exist")

    parser = MyHTMLParser()
    parser.feed(data)
    parser.exportData(sys.argv[2])
else:
    print("Aborting. Inputs are 'input file' and 'desired file name'")
