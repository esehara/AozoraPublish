# -*- coding:utf-8 -*-
from aozorapublish.manager import PublishManager
import urllib
from BeautifulSoup import BeautifulSoup

def get_all_link(target_url):
    xmldata = urllib.urlopen(target_url).read()
    soup = BeautifulSoup(xmldata)
    links = soup.ol.findAll('a')
    result_array = []
    for link in links:
        not_parse = link.get('href')
        not_parse = not_parse.replace("../","")
        parsed = "http://www.aozora.gr.jp/" + not_parse
        result_array.append(parsed)
    return result_array
