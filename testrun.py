# -*- coding: utf-8 -*-
from aozorapublish.manager import PublishManager
from aozorapublish.manager import AozoraPage

def run():
    manager = AozoraPublishManager()
    manager.set_infomation(u"芥川の鼻")
    manager.initialize_directory()
    manager.generate_page("http://www.aozora.gr.jp/cards/000879/card42.html")
    manager.download_page()
    manager.generate_minetype()
    manager.generate_container()
    manager.generate_content()
    manager.generate_toc()
    manager.generate_epub()
    manager.clear_files()
    manager.clear_directory()

if __name__ == "__main__":
    run()
