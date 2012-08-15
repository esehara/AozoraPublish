# -*- coding: utf-8 -*-

import nose
import os
from aozorapublish.manager import *

class TestRunner:
    def TestisRunning(self):
        assert 1 == 1

class TestManager:
    def Test_Path_is_have(self):
        manager = PublishManager("/hoge")
        assert manager.path == "/hoge/"

    def Test_Path_is_not_have(self):
        manager = PublishManager()
        assert manager.path is not None
        assert manager.path[-1] is "/"

    def Test_Working_Directory_make(self):
        manager = PublishManager()
        manager.make_workdir()
        assert os.path.exists(manager.workspace)
        manager.delete_workdir()
        assert not os.path.exists(manager.workspace)

    def Test_Initialize_Directory(self):
        manager = PublishManager()
        manager.initialize_directory()
        assert os.path.exists(manager.workspace + "/META-INF")
        assert os.path.exists(manager.workspace + "/OEBPS")
        manager.clear_directory()
        assert not os.path.exists(manager.workspace)

    def Test_Generate_Page(self):
        manager = PublishManager()
        manager.generate_page("http://www.aozora.gr.jp/cards/000879/card42.html")
        assert manager.__pages__[0].title == u"鼻"

    def Test_Download_Page(self):
        manager = PublishManager()
        manager.initialize_directory()
        manager.generate_page("http://www.aozora.gr.jp/cards/000879/card42.html")
        manager.download_page()
        assert os.path.exists(manager.workspace + "/OEBPS/42_15228.html")
        os.remove(manager.workspace + "/OEBPS/42_15228.html")
        manager.clear_directory()

    def Test_Generate_Container(self):
        manager = helper_generate_manager()
        manager.generate_container()
        assert os.path.exists(manager.workspace + "/META-INF/container.xml")
        os.remove(manager.workspace + "/META-INF/container.xml")
        helper_clear_manager(manager)

    def Test_Generate_Container(self):
        manager = helper_generate_manager()
        manager.generate_content()
        assert os.path.exists(manager.workspace + "/OEBPS/content.opf")
        os.remove(manager.workspace + "/OEBPS/content.opf")
        helper_clear_manager(manager)

    def Test_Generate_Toc(self):
        manager = helper_generate_manager()
        manager.generate_toc()
        assert os.path.exists(manager.workspace + "/OEBPS/toc.ncx")
        os.remove(manager.workspace + "/OEBPS/toc.ncx")
        helper_clear_manager(manager)

#Helper
def helper_generate_manager():
    manager = PublishManager()
    manager.set_infomation(u"ほげほげ")
    manager.initialize_directory()
    manager.generate_page("http://www.aozora.gr.jp/cards/000879/card42.html")
    manager.download_page()
    return manager

def helper_clear_manager(manager):
    os.remove(manager.workspace + "/OEBPS/42_15228.html")
    manager.clear_directory()

