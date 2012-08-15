# -*- coding: utf-8 -*-
import os
import urllib
import xml.etree.ElementTree as ET
import zipfile
from time import time
from aozorapublish.pages import AozoraPage

class PublishManager(object):
    def __init__(self,workpath=None):
        if workpath == None:
            self.path = os.getcwd()
        else:
            self.path = workpath

        if self.path[-1] is not "/":
            self.path = self.path + "/"
        self.workfile  = str(int(time()))
        self.workspace = self.path + self.workfile
        self.download_path = self.workspace + "/" + "OEBPS"
        self.__pages__ = []

    def set_infomation(self,title=None,
        identifer="http://github.com/esehara",
        language="ja"):
        self.title=title
        self.identifer=identifer
        self.language=language

    def make_workdir(self):
        os.makedirs(self.workspace)

    def delete_workdir(self):
        os.removedirs(self.workspace)

    def initialize_directory(self):
        self.make_workdir()
        os.makedirs(self.workspace + "/" + "META-INF")
        os.makedirs(self.download_path)

    def clear_directory(self):
        os.removedirs(self.workspace + "/" + "META-INF")
        os.removedirs(self.download_path)

    def clear_files(self):
        os.remove(self.workspace + "/META-INF/container.xml")
        os.remove(self.workspace + "/minetype")
        for fileitem in os.listdir(self.workspace + "/OEBPS"):
            os.remove(self.workspace + "/OEBPS/" + fileitem)

    def generate_page(self,path):
        page = AozoraPage()
        page.set_card(path)
        self.__pages__.append(page)

    def generate_container(self):
        container_file = open(self.workspace + "/META-INF/container.xml", "w")
        root = ET.Element(
            'container',
            attrib={
                "version":"1.0",
                "xmlns":"urn:oasis:names:tc:opendocumnent:xmlns:cotainer",})
        rootfiles = ET.SubElement(root,'rootfiles')
        rootfile = ET.SubElement(
            rootfiles, 'rootfile',
            attrib={
                "full-path": "OEBPS/content.opf",
                "media-type": "application/oebps-package+xml",
                })
        container_file.write(ET.tostring(root))
        container_file.close()

    def generate_toc(self):
        toc_file = open(self.workspace + "/OEBPS/toc.ncx","w")
        root = ET.Element(
            'ncx',
            attrib={
                "xmlns":"http://www.daisy.org/x3986/2005/ncx/",
                "version":"2005-1"
                })
        head = ET.SubElement(root,"head")
        uid = ET.SubElement(head,"meta",attrib={
                "name": "dtb:uid",
                "content": self.identifer
            })
        depth = ET.SubElement(head,"meta",attrib={
                "name":"dtb:depth",
                "content": "1"
            })
        totalPageCount = ET.SubElement(head,"meta",attrib={
            "name":"dtb:totalPageCount",
                "content": "0"
            })
        maxPageNumber = ET.SubElement(head,"meta",attrib={
                "name": "dtb:maxPageNumber",
                "content": "0"
            })
        docTitle = ET.SubElement(root,"docTitle")
        Titletext = ET.SubElement(docTitle,"text")
        Titletext.text = self.title

        navMap = ET.SubElement(root,"navMap")
        for number,page in enumerate(self.__pages__):
            navPoint = ET.SubElement(navMap,"navPoint",attrib={
                    "id":str(number),
                    "palyOrder":str(number)
                })
            navLabel = ET.SubElement(navPoint,"navLabel")
            navText  = ET.SubElement(navLabel,"text")
            navText.text = page.author + u"『" + page.title + u"』"
            contentSource = ET.SubElement(navPoint,"content"
               ,attrib={"src":page.filename})
        
        toc_file.write(ET.tostring(root))
        toc_file.close()

    def generate_content(self):
        content_file = open(self.workspace + "/OEBPS/content.opf","w")
        root = ET.Element('package',attrib={
            "xmlns":"http://www.idpf.org/2007/opf",
            "unique-identifier":"BookId",
            "version":"2.0"})
        metadata = ET.SubElement(root,'metadata',attrib={
            "xmlns:dc":"http://purl.org/dc/elements/1.1",
            "xmlns:opf":"http://www.idpf.org/2007/opf"})
        title = ET.SubElement(metadata,'dc:title')
        title.text = self.title
        identifer = ET.SubElement(metadata,'dc:identifier',attrib={
            "id":"BookID",
            "opf:scheme": "URL"
            })
        identifer.text = self.identifer
        language = ET.SubElement(metadata,'dc:language')
        language.text = self.language

        manifest = ET.SubElement(root,'manifest')
        for number,page in enumerate(self.__pages__):
            item = ET.SubElement(manifest,'item',attrib={
                "id":"text" + str(number),
                "href":page.filename,
                "media-type":"application/xhtml+xml"})
        toc = ET.SubElement(manifest,'item',attrib={
                "id":"ncx",
                "href":"toc.ncx",
                "media-type":"text/xml"
            })
        spine = ET.SubElement(root,"spine",
            attrib={"toc": "ncx"})
        
        for number,page in enumerate(self.__pages__):
            itemref = ET.SubElement(spine,"itemref",
                attrib={"idref":"text" + str(number)})

        content_file.write('<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root))
        content_file.close()

    def generate_minetype(self):
        minetype_file = open(self.workspace + "/minetype","w")
        minetype_file.write("application/epub+zip")
        minetype_file.close()

    def generate_epub(self):
        epubfile = zipfile.ZipFile(
            self.workspace + "/../" + self.workfile + ".epub",
            "w",zipfile.ZIP_DEFLATED)
        epubfile.write(self.workspace + "/META-INF/","META-INF/")
        epubfile.write(self.workspace + "/META-INF/container.xml","META-INF/container.xml")
        epubfile.write(self.workspace + "/OEBPS/","OEBPS/")
        for fileitem in os.listdir(self.workspace + "/OEBPS/"):
            epubfile.write(self.workspace + "/OEBPS/" + fileitem,"OEBPS/" + fileitem)
        epubfile.close()
        epubfile = zipfile.ZipFile(
            self.workspace + "/../" + self.workfile + ".epub",
            "a",zipfile.ZIP_STORED)
        epubfile.write(self.workspace + "/minetype","minetype")
        epubfile.close()

    def download_page(self):
        for page in self.__pages__:
            urllib.urlretrieve(page.path,self.download_path + "/" + page.filename)

class AozoraPublishManger(PublishManager):
    def to_utf8(self,page):
        conv = file(self.download_path + "/" + page.filename).read()
        conv = conv.decode("shift_jis").encode("utf-8")
        conv = conv.replace('<?xml version="1.0" encoding="Shift_JIS"?>',
            '<?xml version="1.0" encoding="UTF-8"?>')
        conv = conv.replace('<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS" />',
            '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />')
        go_conv = file(self.download_path + "/" + page.filename,"w")
        go_conv.write(conv)
        go_conv.close()

    def download_page(self):
        for page in self.__pages__:
            urllib.urlretrieve(page.path,self.download_path + "/" + page.filename)
            self.to_utf8(page)
