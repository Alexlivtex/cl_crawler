from selenium import webdriver
import time
import bs4 as bs
import pickle
import os
from selenium.webdriver.common.keys import Keys
import threading
import time
import math

max_nocode_count = 2031
max_thread_count = 5

base_no_code_url = "http://t66y.com/thread0806.php?fid=2&search=&page="
login_url = "http://t66y.com/login.php"
base_url = "http://t66y.com"

mutex = threading.Lock()

def analysis_website(sub_page_list):
    global mutex
    sub_dic_map = {}
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    driver.set_script_timeout(10)
    driver.set_page_load_timeout(10)

    while True:
        driver.get(login_url)
        soup = bs.BeautifulSoup(driver.page_source, "lxml")
        title_content = soup.findAll("title")[0].text
        if title_content == "Attention Required! | Cloudflare":
            print(title_content)
            time.sleep(30)
            continue
        else:
            elem_user_name = driver.find_element_by_name("pwuser")
            elem_user_pasword = driver.find_element_by_name("pwpwd")
            elem_user_name.send_keys("alexlivtex")
            elem_user_pasword.send_keys("heisenberg1987")
            #time.sleep(5)
            elem_login = driver.find_element_by_name("submit")
            elem_login.click()
            break

    for page_index in sub_page_list:
        url = base_no_code_url + str(page_index)
        try:
            driver.get(url)
        except:
            print("Execution time exceeded!")
        #time.sleep(2)
        page_list_content = bs.BeautifulSoup(driver.page_source).findAll("h3")
        for title_item in page_list_content:
            try:
                link = title_item.findAll("a")[0]
                title = link.text
                item_link = base_url + "/" + link['href']
                if item_link in sub_dic_map:
                    print("{} has already exists".format(item_link))
                    continue
                print(title)
                print(item_link)
                try:
                    driver.get(item_link)
                except:
                    print("Execution time exceeded!")
                #time.sleep(2)
                item_soup = bs.BeautifulSoup(driver.page_source)
                title_content = item_soup.findAll("title")[0].text
                if title_content == "Attention Required! | Cloudflare":
                    #time.sleep(10)
                    driver.quit()
                    return
                content_container = item_soup.find("div", {"class": "tpc_content do_not_catch"})
                link_torrent = content_container.findAll("a")
                torrent_link_address = ""
                for link_item in link_torrent:
                    if link_item.text[:21] == "http://www.rmdown.com":
                        break
                try:
                    driver.get(link_item.text)
                except:
                    print("Execceed the time execution time")
                print(link_item.text)
                torrent_soup = bs.BeautifulSoup(driver.page_source)
                torrent_link = torrent_soup.findAll("a")[0]
                print(torrent_link["href"])
                sub_dic_map[item_link] = [title, torrent_link["href"]]
                if len(sub_dic_map) % 10 == 0:
                    if mutex.acquire():
                        f_pickle = open("data_total.pickle", "wb")
                        total_dic = pickle.load(f_pickle)
                        z = total_dic.copy()
                        z.update(sub_dic_map)
                        pickle.dump(z, f_pickle)
                        f_pickle.close()
                        mutex.release()
            except:
                print("{} has some error in it!".format(item_link))


def list_chunks(ticker_list, sub_count):
  for i in range(0, len(ticker_list), int(sub_count)):
      yield ticker_list[i:i + int(sub_count)]


def main_function():
    toatl_list_map = []
    for i in range(max_nocode_count):
        toatl_list_map.append(i)

    sub_list = list(list_chunks(toatl_list_map, math.ceil(max_nocode_count/max_thread_count)))
    threads = []

    for i in range(max_thread_count):
        threads.append(threading.Thread(target=analysis_website, args=([sub_list[i]])))

    for t in threads:
        t.setDaemon(True)
        time.sleep(5)
        t.start()

    for thread_index in threads:
        thread_index.join()

main_function()