# -*- coding: utf-8 -*-

import nose
from aozorapublish.util import *

class TestUtil:
    def TestLinkisGet(self):
        links = get_all_link("http://www.aozora.gr.jp/index_pages/person119.html")
        assert links[0] == "http://www.aozora.gr.jp/cards/000119/card43043.html"
