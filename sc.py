import time
from selenium import webdriver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class Watcher:
    DIRECTORY_TO_WATCH = "c:\\attach"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        print("created: " + event.src_path)

    def on_deleted(self, event):
        print("deleted: " + event.src_path)

    def on_modified(self, event):
        print("modified: " + event.src_path)

    def on_moved(self, event):
        print("renamed: " + event.dest_path)
        collection = ['mp4', 'mkv', 'avi']
        duration = ''
        genre = ''
        for type in collection :

            if event.dest_path.find(type) > -1 and event.dest_path.find('movie') > -1:
                # daum
                daum_url = 'http://movie.daum.net'
                point = event.dest_path.rfind("\\")
                filename = event.dest_path[(point + 1):]
                point = filename.rfind(".")
                filename = filename[:point]
                url = 'http://movie.daum.net/search/main?returnUrl=http%3A%2F%2Fmovie.daum.net%2Fmain%2Fnew&searchText='+filename+'#searchType=movie&page=1&sortType=acc'
                driver = webdriver.PhantomJS("C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
                # driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
                driver.implicitly_wait(1)
                driver.get(url)
                element = driver.find_element_by_xpath("//a[@class='link_join']")
                element.click()
                time.sleep(2)

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                thumb = soup.find("img", {"class": 'img_summary'}).get('src')
                title = soup.find('strong', {'class':'tit_movie'}).get_text()
                title_orig = soup.find('span', {'class':'txt_origin'}).get_text()

                for dl in soup.find_all('dl', {'class':'list_main'}) :
                    dd = dl.find_all('dd')
                    genre = dd[0].get_text()
                    duration = dd[3].get_text()


                person = []
                for txt in soup.find_all('a', {'class': 'link_person'}):
                    person.append(txt.get_text())

                story = soup.find('div', {'class':'desc_movie'})

                print(thumb)
            elif event.dest_path.find(type) > -1 and event.dest_path.find('ani') > -1:
                # anidb
                ani_url = 'http://anidb.net/'
                url = 'http://anidb.net/perl-bin/animedb.pl?show=search&do=fulltext&adb.search=Shin+Atashinchi&entity.animetb=1&field.titles=1&do.fsearch=Search'
                #driver = webdriver.PhantomJS("C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
                driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
                driver.implicitly_wait(1)
                driver.get(url)
                element = driver.find_element_by_xpath('//td[@class="relid"]/a')
                element.click()
                time.sleep(2)

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                for tr in soup.find_all('tr',{'itemprop':'episode'}) :
                    td = tr.find('abbr', {'itemprop':'episodeNumber'})
                    if event.dest_path.find(td.get_text().strip()) > -1 :
                        a_href = tr.find('a',{'itemprop':'url'}).get('href')
                        print(a_href)

                        element = driver.find_element_by_xpath('//a[@href="'+a_href+'"]');
                        element.click()
                        time.sleep(2)
                        break

if __name__ == '__main__':
    w = Watcher()
    w.run()