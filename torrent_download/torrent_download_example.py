import libtorrent as lt
import urllib2
import sys
import time

public_torrent = 'http://releases.ubuntu.com/14.04.3/ubuntu-14.04.3-desktop-amd64.iso.torrent'

def downloadTorrent(torrent_url):
    """
    Download torrent using libtorrent library.
    Torrent will be stored at the current directory.
    """
    ses = lt.session()
    ses.listen_on(6881, 6891)

    # read torrent file as bytes
    torrent = lt.bdecode(urllib2.urlopen(torrent_url, 'rb').read())

    info = lt.torrent_info(torrent)
    h = ses.add_torrent({'ti': info, 'save_path': './'})
    ses.start_dht()
    print 'starting', h.name()

    while (not h.is_seed()):
        s = h.status()

        state_str = ['queued', 'checking', 'downloading metadata', \
          'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s\n' % \
          (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
          s.num_peers, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(5)

    print h.name(), 'complete'

downloadTorrent(public_torrent)
