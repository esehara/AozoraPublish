# -*- coding: utf-8 -*-
import nose
from aozorapublish.pages import *

class TestPage:

    def TestPageCanCreate(self):
        page = Page()
        assert page.title is None

    def TestAozoraCardCreate(self):
        page = AozoraPage()
        assert page.title is None

    def TestAozoraCardParse(self):
        page = AozoraPage()
        page.set_card("http://www.aozora.gr.jp/cards/000879/card42.html")
        assert page.title == u"鼻"
        assert page.author == u"芥川 竜之介"
        assert page.path == u"http://www.aozora.gr.jp/cards/000879/files/42_15228.html"
        assert page.filename == u"42_15228.html"
