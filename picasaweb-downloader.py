#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import urllib
import urllib2
import os
import sys


def get_urls(album_page):
    urls = re.search(r"feedPreload: ({.*)}", album_page).group(1)
    urls = json.loads(urls)
    get_one_url = lambda i: urls["feed"]["entry"][i]["media"]["content"][0]["url"]
    photos_count = len(urls["feed"]["entry"])
    return [get_one_url(i) for i in range(photos_count)]


def download_photos(urls, path):
    print("Downloading {} photos".format(len(urls)))
    for i, url in enumerate(urls):
        filename = os.path.split(url)[1].replace("%", " ")
        urllib.urlretrieve(url, os.path.join(path, filename))
        print("{}: {} downloaded".format(i + 1, filename))


def main(url, path=os.getcwd()):
    sock = urllib2.urlopen(url)
    page = sock.read()
    download_photos(get_urls(page), path)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit("picasaweb-downloader.py <album_url> [path]")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(sys.argv[1], os.path.expanduser(sys.argv[2]))
