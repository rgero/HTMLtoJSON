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
        self.parentTag = None # This will only get set if it encounters a table, list or link.
        self.lastTag = None
        self.currentItem = None
        self.currentTag = None
        self.linkString = None # This... ugh. Links.

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if self.currentTag == None:
            if tag == "h3":
                self.currentTag = tag
                self.currentItem = {"heading": None}
            elif tag == "p":
                self.currentTag = tag
                self.parentTag = tag
                self.currentItem = {"paragraph": ""}
            elif tag == "img":
                self.currentItem = {"img" : [None, None]}
                for i in attrs:
                    if i[0] == "src":
                        self.currentItem["img"][1] = i[1].split("'")[1]
                    elif i[0] == "alt":
                        self.currentItem["img"][0] = i[1]
                self.docDic["pageContent"].append(self.currentItem)
                self.currentItem = None
            elif tag == "ol"  or tag == "ul" and self.parentTag == None:
                self.parentTag = tag
                if tag == "ol":
                    self.currentItem = {"ordered_list": []}
                else:
                    self.currentItem = {"unordered_list": []}
            elif tag == "li":
                self.currentTag = "li"

            elif tag == "table":
                self.parentTag = tag
                self.currentItem = {"table" : []}
            elif tag == "td":
                self.currentTag = tag
                if self.lastTag != "td":
                    self.lastTag = tag
                    self.currentItem["table"].append(["row", []])
            elif tag == "iframe":
                # we can ignore a lot of the attributes because we're going to assume they are consistent.
                link = ""
                self.currentTag = "iframe"
                for i in attrs:
                    if i[0] == "src":
                        link = i[1]
                self.currentItem = {"iframe": link}

        if tag == "a":
            link = attrs[0][1]
            self.linkString = "<a href=" + link + " target='_blank'>"




    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "td":
            self.currentTag = None
        if tag == "tr":
            self.lastTag = None
        if tag == "a":
            self.linkString += "</a>"
            if "paragraph" in self.currentItem.keys():
                self.currentItem["paragraph"] += self.linkString
            elif "table" in self.currentItem.keys():
                self.currentItem["table"][len(self.currentItem["table"])-1][1].append(self.linkString)
            self.linkString = None
        elif self.currentTag == tag or self.parentTag == tag:
            self.currentTag = None
            self.parentTag = None
            self.docDic["pageContent"][0].append(self.currentItem)
            self.currentItem = None

    def handle_data(self, data):
        if self.currentTag != None:
            if self.currentTag == "h3":
                self.currentItem["heading"] = data.rstrip()
            elif self.currentTag == "p" and self.linkString == None:
                self.currentItem["paragraph"] += data.strip()
            elif self.currentTag == "li":
                if self.parentTag == "ol":
                    key = "ordered_list"
                else:
                    key = "unordered_list"
                if key in self.currentItem.keys():
                    self.currentItem[key].append(data.rstrip())
            elif self.currentTag == "td":
                self.currentItem["table"][len(self.currentItem["table"])-1][1].append(data.rstrip())
            elif self.currentTag == "a" and self.lastTag == "td":
                self.currentItem["table"][len(self.currentItem["table"])-1][1].append(data.rstrip())
        if self.linkString != None:
            self.linkString += data.rstrip()

    def exportData(self, fileName):
        dataString = "{\n'pageContent':\n\t[\n\t\t[\n"
        for i in self.docDic["pageContent"][0]:
            dataString += "\t\t\t" + str(i) + ",\n"
        dataString += "\t\t]\n\t]\n}"
        file = open(fileName, 'w')
        file.write(dataString)



if len(sys.argv) == 3:
    try:
        file = open(sys.argv[1], 'r')
        data = file.read()

        parser = MyHTMLParser()
        parser.feed(data)

        parser.exportData(sys.argv[2])
    except Exception as e:
        print(e)
else:
    print("Aborting. Inputs are 'input file' and 'desired file name'")
