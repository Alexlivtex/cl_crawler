__author__ = 'Li Wei'

import urllib2
import re
from bs4 import BeautifulSoup
import lxml.builder
from lxml import etree as ET
import os
import xml
from datetime import datetime
import shutil
import xml.etree.ElementTree


ULTIMATE_PAGE_BOUNDER = 1000
page_id = 0
nocode_base_url = 'http://cl.mocl.xyz/thread0806.php?fid=7&search=&page='
base_site_url = 'http://cl.mocl.xyz/'
node_xml = 'record_technology_discuss_database.xml'

total_record_list = []


class item_node_video:
    item_title = ''
    discuss_count = ''

    def __init__(self, url, count):
        self.item_title = url
        self.discuss_count = count

def init():
    if os.path.isfile(node_xml) is True:
        tree = xml.etree.ElementTree.parse(node_xml).getroot()

        head = tree.findall('header')
        global page_id
        page_id = int(head[0].find('page_index').text)

        for items in tree.findall('item'):
            item_title = items.find('item_title').text
            discuss_counting = items.find('discuss_counting').text
            total_record_list.append(item_node_video(item_title, int(discuss_counting)))
    else:
        print('File not exist')

    return

def update_database():
    if os.path.isfile(node_xml) is True:
        os.remove(node_xml)
        print('File already exist')
    else:
        print('File not exist')


    global page_id
    root = ET.Element('root')
    header = ET.SubElement(root, 'header')
    record_type = ET.SubElement(header, 'record_type')
    update_time = ET.SubElement(header, 'update_time')
    page_index = ET.SubElement(header, 'page_index')

    record_type.text = 'technology_discuss'
    update_time.text = str(datetime.now())
    page_index.text = str(page_id)

    for index in total_record_list:
        item = ET.Element('item')
        item_title = ET.SubElement(item, 'item_title')
        discuss_count = ET.SubElement(item, 'discuss_counting')

        item_title.text = index.item_title
        discuss_count.text = str(index.discuss_count)

        root.insert(1, item)

    ET.ElementTree(root).write(node_xml, pretty_print=True)

    shutil.copy2(node_xml, r"E:\vmware_share\record_nocode_database.xml")
    return


def update_record():
    record_size_limit = 100
    total_record_list.sort(key=lambda x: x.discuss_count, reverse=True)
    # newlist = sorted(ut, key=lambda x: x.count, reverse=True)

    if len(total_record_list) < record_size_limit:
        return

    del total_record_list[record_size_limit:len(total_record_list)]
    total_record_list.sort(key=lambda x: x.discuss_count, reverse=False)
    return


def fetch_web(url):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    html = response.read().decode('gbk')
    return html

###############################################################
###############################################################
#######################Running#################################
###############################################################
###############################################################

init()

while True:
    page_index = page_id % ULTIMATE_PAGE_BOUNDER

    target_url = fetch_web(nocode_base_url + str(page_index))
    sub_url_begin_pos = target_url.find(<h3><a href="htm_data'"") + len("downloaded: ")
    sub_url_end_pos =
    try:
        soup = BeautifulSoup(fetch_web(nocode_base_url + str(page_index)), 'html.parser')
    except:
        continue


    for header_tag in soup.find_all('h3'):
        sub_url = base_site_url + header_tag.a.attrs['href']
        try:
            html_sub_title_soup = BeautifulSoup(fetch_web(sub_url), 'html.parser')
        except:
            continue
        torrent_link = html_sub_title_soup.body.findAll(text=re.compile('^http://www.rmdown.com'))

        if len(torrent_link) > 0 and len(torrent_link[0]) > len("http://www.rmdown.com"):
            try:
                target_url = fetch_web(torrent_link[0])
            except:
                continue
            download_count_begin_pos = target_url.find("downloaded:") + len("downloaded: ")
            download_count_end_pos = target_url.find("<", download_count_begin_pos)
            if download_count_end_pos > download_count_begin_pos:
                try:
                    download_count = int(target_url[download_count_begin_pos:download_count_end_pos])
                except:
                    continue
                print(nocode_base_url + str(page_index))
                print(sub_url)
                try:
                    print(torrent_link[0])
                except:
                    print('Unsupported encode type!')
                print("Downloaded " + str(download_count) + " times")

                for index in total_record_list:
                    if cmp(index.torrent_link, torrent_link[0]) == 0 and download_count >= index.download_count:
                        del total_record_list[total_record_list.index(index)]
                        break

                total_record_list.append(item_node_video(sub_url, torrent_link[0], download_count))

            else:
                continue
        else:
            continue

    page_id += 1
    update_record()
    update_database()
