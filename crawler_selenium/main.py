from selenium import webdriver
import time
import bs4 as bs
import pickle
import os
from selenium.webdriver.common.keys import Keys

max_nocode_count = 2031

base_no_code_url = "http://t66y.com/thread0806.php?fid=2&search=&page="
login_url = "http://t66y.com/login.php"
base_url = "http://t66y.com"

def analysis_website():
    total_dic_map = {}
    total_err_list = []
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

    if os.path.exists("data_total.pickle"):
        f_data_pickle = open("data_total.pickle", "rb")
        total_dic_map = pickle.load(f_data_pickle)
        f_data_pickle.close()

    for page_index in range(max_nocode_count):
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
                if item_link in total_dic_map:
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
                    f_error_list = open("error.txt", "w")
                    f_error_list.writelines(total_err_list)
                    f_error_list.close()
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
                total_dic_map[item_link] = [title, torrent_link["href"]]
                if len(total_dic_map) % 10 == 0:
                    f_pickle = open("data_total.pickle", "wb")
                    pickle.dump(total_dic_map, f_pickle)
                    f_pickle.close()
            except:
                print("{} has some error in it!".format(item_link))
                total_err_list.append(item_link + "\n")

while True:
    analysis_website()
    #time.sleep(10)