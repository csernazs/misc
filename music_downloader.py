#!/usr/bin/env python2

from __future__ import print_function

import os
import sys
import argparse
import json
import time
import string
import urllib2
import shutil

import logging
logging.basicConfig(level=logging.ERROR)

import pdb

from gmusicapi import Mobileclient
from texttable import Texttable
import eyed3
import unidecode

pjoin = os.path.join

DEBUG = False

CACHE_TTL = 3600

FORMAT_JSON = "json"
FORMAT_PLAIN = "plain"

def debug(msg, *args):
    if DEBUG:
        if args:
            print(msg.format(*args))
        else:
            print(msg)
            
def terminate(msg, exitstatus=1):
    sys.stderr.write(str(msg)+"\n")
    sys.exit(exitstatus)

def create_table(**kwargs):
    table = Texttable(int(os.environ.get("COLUMNS", 130)))
    for key, value in kwargs.items():
        method = getattr(table, key)
        method(value)
    
    return table
    

def string_keep(text, keep, target):
    retval = []
    for char in text:
        if char in keep:
            retval.append(char)
        else:
            retval.append(target)
    
    return "".join(retval)
    
    
def short(text, max_width, suffix="..."):
    if len(text) <= max_width:
        return text
    
    return text[:max_width-len(suffix)] + suffix
    
class Application(object):
    def __init__(self):
        self.api = None
        
    def parse_args(self):
        global DEBUG
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-d", "--debug", action="store_true", help="Enable debug")
        parser.add_argument("-c", "--config", default=os.path.expanduser("~/.music_downloader.conf"), help="Config file")
        parser.add_argument("-f", "--force", action="store_true", help="Non-interactive mode")
        parser.add_argument("--cache-dir", default=os.path.expanduser("~/.cache/music_downloader"), help="Cache dir to store data")
        
        subparsers = parser.add_subparsers(dest="command")
        subparsers.required = True
        
        p_list = subparsers.add_parser("list")
        p_list.add_argument("-s", "--short-by", default="album", choices=("album", "artist"), help="Sort output by column")

        p_shell = subparsers.add_parser("shell")
        
        p_download = subparsers.add_parser("download")
        p_download.add_argument("album", help="Album to download (ID or substring)")
        p_download.add_argument("-o", "--output", help="Output directory")
        p_download.add_argument("-n", "--naming", default="{album}/{track_no:02}-{song}.mp3", help="Naming scheme")
        p_download.add_argument("--simplify", default="spaces,shorten,nonalpha,unidecode", help="Simplify filename by making conversions")
        p_download.add_argument("-q", "--quality", default="med", choices=("hi", "med", "low"), help="Quality of the mp3")

        p_clear = subparsers.add_parser("clear")
        
        args = parser.parse_args()    
        if args.debug:
            DEBUG = True
            
        return args

    def login(self):
        if self.api is not None:
            return self.api
        
        debug("logging in as {}", self.config["email"])
        
        api = Mobileclient(debug_logging=DEBUG)
        api.login(self.config["email"], self.config["password"], Mobileclient.FROM_MAC_ADDRESS)

        self.api = api
        
        return api

    
    def get_cache_entry(self, basename, format=FORMAT_JSON, ttl=CACHE_TTL, default=None):
        cache_path = os.path.join(self.cache_dir, basename)

        if os.path.isfile(cache_path) and os.path.getmtime(cache_path) > time.time() - ttl:
            debug("cache hit {}", basename)
            with open(cache_path) as cache_file:
                if format == FORMAT_JSON:
                    return json.load(cache_file)
                elif format == FORMAT_PLAIN or format is None:
                    return cache_file.read()
        else:
            debug("cache miss {}", basename)
            return default

        
    def store_cache_entry(self, basename, data, format=FORMAT_JSON):
        cache_path = os.path.join(self.cache_dir, basename)
        debug("cache store {}", basename)
        
        with open(cache_path, "w") as cache_file:
            if format == FORMAT_JSON:
                json.dump(data, cache_file)
            elif format == FORMAT_PLAIN or format is None:
                cache_file.write(data)

    def clear_cache_entry(self, basename):
        cache_path = os.path.join(self.cache_dir, basename)
        debug("cache clear {}", basename)

        if os.path.isfile(cache_path):
            os.unlink(cache_path)
            
    def get_all_songs(self):
        """
{u'album': u'Live In Europe',
 u'albumArtRef': [{u'kind': u'sj#imageRef',
                   u'url': u'http://lh4.ggpht.com/pWDoKpzBTeuGiZAqfs1jb9BZlNXpZu_TwXE4Z89i9R0ALaJtZfLzg8brt3wcUdajSuQXgmhu-g'}],
 u'albumArtist': u'Flying Colors',
 u'albumId': u'Bbyfgzcnrx6pyz3bq6n3lm65vmi',
 u'artist': u'Flying Colors',
 u'artistArtRef': [{u'aspectRatio': u'2',
                    u'autogen': True,
                    u'kind': u'sj#imageRef',
                    u'url': u'http://lh3.googleusercontent.com/P4ZdDmBKhU6OSV0lBtv7K7JvJu6zdSAThJ6qpOMBHvdlsUldPu3xYw-yMBKd2dDSo-1ryrbAcrA'}],
 u'artistId': [u'Ahnhtzuyt25q3nrvihpnav3sfdm'],
 u'clientId': u'/DvjCIQwtmyRTVpgPpYcPQ==Tteftdxqz2hb6v727yxguieqoti',
 u'creationTimestamp': u'1391116736139838',
 u'deleted': False,
 u'discNumber': 1,
 u'durationMillis': u'424068',
 u'estimatedSize': u'47510187',
 u'explicitType': u'2',
 u'genre': u'Rock',
 u'id': u'5e51b45f-b303-38d8-bfe2-82425876bd2e',
 u'kind': u'sj#track',
 u'lastModifiedTimestamp': u'1391187601000142',
 u'nid': u'Tteftdxqz2hb6v727yxguieqoti',
 u'playCount': 5,
 u'recentTimestamp': u'1401402310167000',
 u'storeId': u'Tteftdxqz2hb6v727yxguieqoti',
 u'title': u'Kayla',
 u'totalDiscCount': 1,
 u'totalTrackCount': 17,
 u'trackNumber': 10,
 u'trackType': u'4'}
"""
        all_songs = self.get_cache_entry("all_songs.json")
        if not all_songs:
            self.login()
            all_songs = self.api.get_all_songs()
            self.store_cache_entry("all_songs.json", all_songs)
        
        return all_songs
                
    def get_all_albums(self):
        albums = set()
        for song in self.get_all_songs():
            if "albumId" not in song:
                continue

            albums.add((song["albumId"], song["albumArtist"], song["album"]))
            
        return albums

    def get_stream_url(self, *args, **kwargs):
        self.login()
        return self.api.get_stream_url(*args, **kwargs)
        
    def cmd_list(self):
        if self.args.short_by == "album":
            short_column_id = 2
        elif self.args.short_by == "artist":
            short_column_id = 1
        else:
            raise ValueError("Invalid short_by: {}".format(self.args.short_by))

        table = create_table(header=("ID", "Artist", "Album"), set_deco=Texttable.HEADER, set_cols_align=["l", "l", "l"])
        
        albums = [(x[0], short(x[1], 40).encode("utf8"), short(x[2], 40).encode("utf8")) for x in self.get_all_albums()]
        
        table.add_rows(sorted(albums, key=lambda x: x[short_column_id].lower()), header=False)

        print(table.draw().encode("utf8"))        

    def cmd_shell(self):
        self.login()
        api = self.api
        import IPython; IPython.embed()

    def download_song(self, songid, quality, target):
        if os.path.isfile(target):
            return
        
        target_dir = os.path.dirname(target)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        
        stream_url = self.get_stream_url(songid, quality=quality)

        tmp_file = target+".tmp"
        try:
            urlinfo = urllib2.urlopen(stream_url)
            outfile = open(tmp_file, "wb")
            shutil.copyfileobj(urlinfo, outfile, 64*1024)
            outfile.close()
            urlinfo.close()
        except:
            if os.path.isfile(tmp_file):
                os.unlink(tmp_file)
            raise

        os.rename(tmp_file, target)
        
                    
        
    def cmd_download(self):
        args = self.args
        album = args.album
        simplify = set([x.strip() for x in args.simplify.split(",")])
        
        albums = self.get_all_albums()
        
        found = [x for x in albums if x[0] == album]
        
        if not found:
            found = [x for x in albums if album in x[2]]

        if len(found) > 1:
            terminate("Ambiguous album substring: '{}'".format(album))
        if not found:
            terminate("No album found: '{}'".format(album))

        found = found[0]
        album_id = found[0]

        all_songs = self.get_all_songs()
        album_songs = sorted([x for x in all_songs if x.get("albumId") == album_id], key=lambda x: (x["discNumber"], x["trackNumber"]))
        
        print("Found album")
        print("ID: {}".format(album_id))
        print("Artist: {}".format(found[1].encode("utf8")))
        print("Album: {}".format(found[2].encode("utf8")))
        print("Number of songs: {}".format(len(album_songs)))
        print()
        
        for song in album_songs:
            print("{0:02} {1}".format(song["trackNumber"], song["title"].encode("utf8")))
            
        output_dir = args.output
        if not output_dir:
            output_dir = self.config.get("output_dir", os.path.expanduser("~/Downloads"))
        
        print()
        print("Quality: {}".format(args.quality))
        
        if not args.force:
            print()
            if raw_input("Download to {} ? [n] ".format(output_dir)) != "y":
                terminate("User abort.")
        else:
            print("Downloading album to {}".format(output_dir))
        

        for track_idx, song in enumerate(album_songs):
            track_no = track_idx + 1
            
            part_album = song["album"].strip()
            part_song = song["title"].strip()
            part_artist = song["albumArtist"].strip()

            if "spaces" in simplify:
                part_artist = part_artist.replace(" ", "_")
                part_album = part_album.replace(" ", "_")
                part_song = part_song.replace(" ", "_")

            if "unidecode" in simplify:
                part_artist = unidecode.unidecode(part_artist)
                part_album = unidecode.unidecode(part_album)
                part_song = unidecode.unidecode(part_song)
            
            if "nonalpha" in simplify:
                part_artist = string_keep(part_artist, string.letters + string.digits + "-_", "_")
                part_album = string_keep(part_album, string.letters + string.digits + "-_", "_")
                part_song = string_keep(part_song, string.letters + string.digits + "-_", "_")
            
            if "shorten" in simplify:
                part_artist = part_artist[:10]
                part_album = part_album[:10]
                part_song = part_song[:10]
            
            output_basename = args.naming.format(album=part_album, song=part_song, track_no=track_no)
            output_filename = os.path.join(output_dir, output_basename)
            
            if os.path.isfile(output_filename) and os.path.getsize(output_filename) > 0:
                print("Skipping track {} as it is already downloaded to {}".format(track_no, output_filename))
            else:
                print("Downloading track {} to {}".format(track_no, output_filename))
            
            self.download_song(song["id"], args.quality, output_filename)

            mp3 = eyed3.load(output_filename)
            mp3.initTag()
            
            mp3.tag.album_artist = song["albumArtist"]
            mp3.tag.artist = song["artist"]
            mp3.tag.album = song["album"]
            mp3.tag.track_num = track_no
            mp3.tag.title = song["title"]
            mp3.tag.save()
            

    def cmd_clear(self):
        self.clear_cache_entry("all_songs.json")

    def run(self):
        args = self.parse_args()
        self.args = args
        
        try:
            self.config = json.load(open(args.config))
        except IOError as err:
            terminate("Unable to open config file '{}': {}".format(args.config, str(err)))
        
        if not os.path.isdir(args.cache_dir):
            os.mkdir(args.cache_dir, 0700)
        
        self.cache_dir = args.cache_dir
        
        method = getattr(self, "cmd_"+args.command)
        method()
        
        return 0

if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())
    