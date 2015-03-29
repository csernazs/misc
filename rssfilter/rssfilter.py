#!/usr/bin/env python

"""
Example usage from crontab:

12 *	*   *   *    /usr/bin/python /home/zsolt/devel/python/rssfilter/rssfilter.py -o /home/zsolt/public_html/pypirss.xml -t 'http://sirius.dalnet.ca/~zsolt/pypirss.xml' -p lxml,ibm_db,python-sybase,ipython


"""

import feedparser # for parsing
import feedgen    # for generating
from feedgen.feed import FeedGenerator

import argparse
import re
import os

rss_url="https://pypi.python.org/pypi?:action=rss"

pkgurl_re = re.compile("https?://pypi.python.org/pypi/([^/]+)/([^/]+)")

DEBUG=False

def debug(msg):
    if DEBUG:
        print msg
    
def filter_rss(url, packages):
    rss = feedparser.parse(url)
    for entry in rss.entries:
        m = pkgurl_re.match(entry["link"])
        if m:
            pkgname, version = m.groups()
            if pkgname in packages:
                yield entry
        else:
            #print "ERR", entry["link"]
            continue
            
            
def main():
    global DEBUG
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output", default=False)
    
    parser.add_argument("-o", "--output", help="Output filename", required=True)
    parser.add_argument("-s", "--source", help="Source URL", default=rss_url)
    parser.add_argument("-t", "--target", help="Target URL", required=True)
    parser.add_argument("-p", "--packages", help="Packages separated by comma to filter", required=True)


    args = parser.parse_args()

    packages = args.packages.split(",")
    DEBUG = args.verbose
        
    if os.path.isfile(args.output) and os.path.getsize(args.output) >0:
        entries = feedparser.parse(args.output)["entries"]
        entries_urls = [x["link"] for x in entries]
    else:
        entries = []
        entries_urls = []
            
    dirty = False
    for entry in filter_rss(rss_url, packages):
        if entry["link"] not in entries_urls:
            debug("adding "+entry["link"])
            entries.append(entry)
            dirty = True

    if not dirty:
        return

    entries.sort(key=lambda x: x["published_parsed"], reverse=True)
        
    if len(entries) > 40:
        entries = entries[:40]
        

    debug("entries")
    debug("\n".join([x["link"] for x in entries]))
    
    outfeed = FeedGenerator()
    outfeed.id(args.target)
    outfeed.title("PyPI updates, filtered")
#    outfeed.author( {"name":"Zsolt Cserna","email":"cserna.zsolt@gmail.com"} )
#    outfeed.link( href="http://example.com", rel="alternate" )
#    outfeed.logo("http://ex.com/logo.jpg")
#    outfeed.subtitle("This is a cool feed!")
    outfeed.description("PyPI updates for packages %s" % ", ".join(packages))
    outfeed.link(href=args.target, rel="self" )
    outfeed.language("en")    

    for entry in entries:
        fe = outfeed.add_entry()    
        fe.title(entry["title"])
        fe.summary(entry["summary"])
        fe.published(entry["published"])
        fe.link(entry["links"][0])
    
    outrss = outfeed.rss_str(pretty=True)
    open(args.output, "w").write(outrss)
    
    
if __name__ == "__main__":
    main()
    
    