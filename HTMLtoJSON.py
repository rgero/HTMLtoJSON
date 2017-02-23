'''

    This is going to be written in Python 3.6

'''
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.docDic = {}
        self.docDic["pageContent"] = []
        self.parentTag = None # This will only get set if it encounters a table, list or link.
        self.currentItem = None
        self.currentTag = None

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
                print("found list")
                self.parentTag = tag
                if tag == "ol":
                    self.currentItem = {"ordered_list": []}
                else:
                    self.currentItem = {"unordered_list": []}
            elif tag == "li":
                self.currentTag = "li"




    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.currentTag == tag or self.parentTag == tag:
            self.currentTag = None
            self.parentTag = None
            self.docDic["pageContent"].append(self.currentItem)
            print(self.currentItem)
            self.currentItem = None

    def handle_data(self, data):
        if self.currentTag != None:
            if self.currentTag == "h3":
                self.currentItem["heading"] = data.rstrip()
            elif self.currentTag == "p":
                self.currentItem["paragraph"] += data.strip()
            elif self.currentTag == "li":
                if self.parentTag == "ol":
                    key = "ordered_list"
                else:
                    key = "unordered_list"
                if key in self.currentItem.keys():
                    self.currentItem[key].append(data.rstrip())


    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

file = open('guitar-trainer.html', 'r')
data = file.read()

parser = MyHTMLParser()
parser.feed(data)
