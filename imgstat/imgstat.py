#!/usr/bin/python2

import sys
import os
import pyexiv2
import argparse
import sqlite3
import traceback
import time
import hashlib

import cProfile as profile
import pstats

pjoin = os.path.join

DEBUG = False


def debug(msg):
    if DEBUG:
        funcname = traceback.extract_stack()[-2][2]
        print "[debug] %s: %s" % (funcname, str(msg))


def get_exif(fn):
    trans_table = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    img = pyexiv2.ImageMetadata(fn)
    img.read()
    ret = {}
    for key in img.exif_keys:
        if img[key].type == "Undefined":
            continue

        try:
            value = img[key].value
        except pyexiv2.exif.ExifValueError:
            continue

        if type(value) == list or type(value) == tuple:
            for idx in xrange(len(value)):
                ret[key + "." + str(idx + 1)] = value[idx]
        elif type(value) == str:
            value = value.translate(trans_table)
            if value.find("\x00") == -1:
                ret[key] = value
        elif type(value) == int or type(value) == float:
            ret[key] = value

    return ret


def create_db(fn):
    debug("Creating db %s" % fn)
    conn = sqlite3.connect(fn)
    cursor = conn.cursor()
    cursor.execute("create table files (fileid integer primary key, path text, md5sum char(32))")
    cursor.execute("create table exif (exifid integer primary key, fileid int, key text, value text)")
    cursor.execute("create unique index files_filename_idx on files (path)")
    cursor.execute("create index files_filename_md5sum on files (md5sum)")
    cursor.execute("create index exif_key_idx on exif (key)")
    cursor.execute("create unique index exif_key_fileid_idx on exif (key, fileid)")

    conn.commit()

    return conn


def init_db(fn):
    if not os.path.isfile(fn):
        return create_db(fn)
    else:
        debug("Opening database %s" % fn)
        return sqlite3.connect(fn)


def get_chksum(filename, method="md5", maxlength=64 * 1024):
    m = hashlib.new(method)
    with open(filename, "rb") as f:
        buff = f.read(maxlength)
        m.update(buff)

    return m.hexdigest()


class Application(object):

    def cmd_init(self):
        try:
            debug("Removing file %s" % self.args.dbfile)
            os.unlink(self.args.dbfile)
        except OSError:
            pass

        create_db(self.args.dbfile)

    def add_files(self, paths, force):
        args = self.args
        conn = self.conn
        cursor = conn.cursor()

        added_cnt = 0

        for full_path in paths:
            t1 = time.time()
            cursor.execute("select fileid from files where path=?", (full_path,))
            row = cursor.fetchone()
            need_insert = False
            if not row:
                need_insert = True
            else:
                if force:
                    fileid = row[0]
                    cursor.execute("delete from exif where fileid=?", (fileid,))
                    cursor.execute("delete from files where fileid=?", (fileid,))
                    need_insert = True
                else:
                    print "skip %s" % full_path

            if need_insert:
                need_insert = False
                md5sum = get_chksum(full_path)
                cursor.execute("select fileid, path from files where md5sum=?", (md5sum,))
                row = cursor.fetchone()
                if row:
                    debug("matching md5sum: %s, id:%d, path:%s" % (md5sum, row[0], row[1]))
                    if force:
                        fileid = row[0]
                        cursor.execute("delete from exif where fileid=?", (fileid,))
                        cursor.execute("delete from files where fileid=?", (fileid,))
                        need_insert = True
                else:
                    need_insert = True

                if need_insert:
                    try:
                        exif = get_exif(full_path)
                    except IOError:
                        print "error %s" % full_path
                    else:
                        cursor.execute("insert into files (path, md5sum) values (?, ?)", (full_path, md5sum))
                        fileid = cursor.lastrowid

                        for key, value in exif.iteritems():
                            cursor.execute("insert into exif (fileid, key, value) values (?, ?, ?)", (fileid, key, value))

                        print "added %s" % full_path
                        added_cnt += 1
                else:
                    print "skip %s" % full_path

        conn.commit()

        return added_cnt

    def cmd_add(self):
        args = self.args
        conn = self.conn

        added_cnt = 0
        for path in args.files:
            paths = []
            if os.path.isdir(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        paths.append(pjoin(dirpath, filename))
                    if not self.args.recursive:
                        break
            else:
                paths = [path]
            paths = map(os.path.abspath, paths)
            paths.sort()

            added_cnt += self.add_files(paths, args.force)

        print "added %d files" % added_cnt

    def cmd_query_focallength(self):
        args = self.args
        conn = self.conn

        cursor = conn.cursor()

        cursor.execute("select count(files.path), exif.value/%d from files, exif where files.fileid = exif.fileid and exif.key == 'Exif.Canon.FocalLength.2' group by exif.value/%d" % (args.resolution, args.resolution))

        data = cursor.fetchall()
        data = [map(int, row) for row in data]

        data.sort(lambda x, y: cmp(x[1], y[1]))

        print "FL   count"

        total = 0
        for row in data:
            total += row[0]
            print "%4d %5d" % (row[1] * args.resolution, row[0])

        print
        print "Total: %d" % total

    def main(self):
        global DEBUG

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("--dbfile", help="Database file (sqlite)", default=pjoin(os.environ["HOME"], ".imgstat.sqlite"))
        parser.add_argument("-d", "--debug", help="Debug messages", action="store_true", default=False)
        parser.add_argument("-p", "--profile", help="Enable profiler", action="store_true", default=False)

        subparsers = parser.add_subparsers()

        parser_add = subparsers.add_parser("add", help="Add new files to the db")
        parser_add.add_argument("files", help="Files or directories to be added", nargs="+")
        parser_add.add_argument("-r", "--recursive", help="Add files recursively", action="store_true", default=False)
        parser_add.add_argument("-f", "--force", help="Force updating existing files", action="store_true", default=False)
        parser_add.set_defaults(func=self.cmd_add)

        parser_init = subparsers.add_parser("init", help="Initializes DB (WARNING! removes all data from DB)")
        parser_init.set_defaults(func=self.cmd_init)

        parser_query = subparsers.add_parser("query", help="Query db")

        subsubparsers = parser_query.add_subparsers()

        parser_q_focallength = subsubparsers.add_parser("focallength", help="Query focallength")
        parser_q_focallength.add_argument("-r", "--resolution", type=int, help="Resolution of focal length", default=1)
        parser_q_focallength.set_defaults(func=self.cmd_query_focallength)

        args = parser.parse_args()
        DEBUG = args.debug
        conn = init_db(args.dbfile)

        self.args = args
        self.conn = conn

        if args.profile:
            profile.run("args.func()")
        else:
            args.func()


if __name__ == "__main__":
    Application().main()
