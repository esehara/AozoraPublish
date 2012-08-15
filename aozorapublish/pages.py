from BeautifulSoup import BeautifulSoup
import urllib

class Page:
    def __init__(self):
        self.title = None
        self.author = None
        self.path = None

class AozoraPage(Page):
    def set_card(self,urlpath):
        source = urllib.urlopen(urlpath).read()
        soup = BeautifulSoup(source)
        self.title = soup.tr.font.text
        self.author = soup.findAll("tr")[2].a.text
        self.path = soup.findAll("div",{"align":"right"})[1].findAll("a")[1].get("href")
        urlpath = "/".join(urlpath.split("/")[:-1])
        self.path = urlpath + self.path[1:]
        self.filename = self.path.split("/")[-1]
