#!/usr/bin/env python
'''
Created on Apr 19, 2012
@author: dan, Faless

    GNU GENERAL PUBLIC LICENSE - Version 3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    http://www.gnu.org/licenses/gpl-3.0.txt

'''
#encoding=utf8
import os.path as pt
import sys
import libtorrent as lt
from time import sleep
import os
import shutil
import time
import pickle

tmp_dir_name = "torrent_dir"
pickle_data = "data_total.pickle"

def magnet2torrent(magnet, output_name=None):
    if not pt.exists(tmp_dir_name):
        os.mkdir(tmp_dir_name)

    tempdir = tmp_dir_name
    ses = lt.session()
    params = {
        #'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2),
    }
    handle = lt.add_magnet_uri(ses, magnet, params)

    print("Downloading Metadata (this may take a while)")
    waiting_count = 0
    while (not handle.has_metadata()):
        try:
            sleep(1)
            waiting_count += 1
            if waiting_count > 150:
                print("{} can not be downloaded!".format(magnet))
                return
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            sys.exit(0)
    ses.pause()
    print("Done")

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    #output = pt.abspath(torinfo.name() + tempdir + ".torrent")
    output = torinfo.name() + ".torrent"
    output = os.path.join(tempdir, output)

    print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    torrent_content = lt.bencode(torfile.generate())
    f.write(torrent_content)
    f.close()
    try:
        shutil.rmtree(torinfo.name())
    except:
        print("No need to delete {}".format(torinfo.name()))
    ses.remove_torrent(handle)
    return output


total_list = {}
f_pickle = open(pickle_data, "rb")
total_list = pickle.load(f_pickle)
f_pickle.close()

for link_index in total_list:
    if total_list[link_index][1][:6] == "magnet":
        print(total_list[link_index][1])
        magnet2torrent(total_list[link_index][1])


#magnet2torrent("magnet:?xt=urn:btih:de3fd61487d7c0d2b7fe77b2dbb0f05c3b0a8162")
