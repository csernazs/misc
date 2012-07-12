#!/usr/bin/python

import pdb

import os, sys, tempfile, atexit, shutil, glob, fnmatch

import pyexiv2 as exif

from optparse import OptionParser


os.chmod = lambda x, y: True

pjoin = os.path.join
DEBUG = False

class UsageError(Exception):
    pass
    
def debug(msg):
    if DEBUG:
        print msg
    

def execute(cmd):
    debug("Executing command %s" % cmd)
    return os.system(cmd)

def copy(src, dst):
    debug("Copying file %s to %s" % (src, dst))
    shutil.copy(src, dst)

def move(src, dst):
    debug("Moving file %s to %s" % (src, dst))
    shutil.move(src, dst)
    
class WorkDir(object):
    def __init__(self, *args, **kwargs):
        self.dir = tempfile.mkdtemp(*args, **kwargs)
        debug("Created tmp dir %s" % self.dir)
        atexit.register(self.remove_dir)
        
    def remove_dir(self):
        debug("Removing dir %s" % self.dir)
        shutil.rmtree(self.dir)

class Application(object):
    def align_images(self, images):
        ret = []
        skip_file = True
        for img in images:
            img_dir = os.path.dirname(img)
            fn_parts = os.path.basename(img).split(".")
            
            dst_file = pjoin(img_dir, fn_parts[0]+"_aligned.tif")
            ret.append(dst_file)
            if not (os.path.isfile(dst_file) and os.path.getmtime(dst_file) > os.path.getmtime(img)):
                skip_file = False
                break
        
        if skip_file:
            debug("Skipping files %s" % " ".join(images))
            return ret
            
        ret = []
        execute("align_image_stack -c 5 -a %s/aligned_ %s" % (self.wd, " ".join(images)))

        idx = 0
        for img in images:
            img_dir = os.path.dirname(img)
            fn_parts = os.path.basename(img).split(".")
            dst_file = pjoin(img_dir, fn_parts[0]+"_aligned.tif")
            src_file = pjoin(self.wd, "aligned_%s.tif" % (str(idx).zfill(4)))
            move(src_file, dst_file)
            ret.append(dst_file)
            idx = idx + 1
        
        return ret

    def render_hdr(self, images, dst_file):
        if os.path.isfile(dst_file):
            skip_file = True
            dst_mtime = os.path.getmtime(dst_file)
            for img in images:
                if dst_mtime < os.path.getmtime(img):
                    skip_file = False
                    break

            if skip_file:
                debug("Skipping creation of %s" % dst_file)
                return

        tmp_file = pjoin(self.wd, "hdr.jpg")
                            
        execute("enfuse -o %s %s" % (tmp_file, " ".join(images)))
        debug("Moving file %s to %s" % (tmp_file, dst_file))
        shutil.copyfile(tmp_file, dst_file)
        os.unlink(tmp_file)
        
    def get_hdr_images(self, dir):
        filelist = []
        for fn in os.listdir(dir):
            full_path = pjoin(dir, fn)
            if fnmatch.fnmatch(fn.lower(), self.opts.mask) and os.path.isfile(full_path):
                filelist.append(full_path)
        
        filelist.sort()

        cur_ts = None        
        hdr_tmp_list = []

        hdr_list = []
        for cur_fn in filelist:
            info = exif.ImageMetadata(cur_fn)
            info.read()
            if cur_ts is None:
                cur_ts = info["Exif.Image.DateTime"]
                old_fn = cur_fn
                continue
                
            new_ts = info["Exif.Image.DateTime"]
#            pdb.set_trace()
            delta = new_ts.value - cur_ts.value
            cur_ts = new_ts
            
            if delta.seconds < self.opts.threshold:
                if len(hdr_tmp_list) == 0:
                    hdr_tmp_list.append(old_fn)
                if len(hdr_tmp_list) < self.opts.levels:
                    hdr_tmp_list.append(cur_fn)
                
                if len(hdr_tmp_list) == self.opts.levels:
                    hdr_list += hdr_tmp_list
                    hdr_tmp_list = []
            else:
                hdr_tmp_list = []
                
            old_fn = cur_fn
        
        return hdr_list
                    
    def main(self):
        global DEBUG
        parser = OptionParser()

        parser.add_option("--nosort", action="store_true", default=False, help="Don't sort filenames")
        parser.add_option("-l", "--levels", default="3", help="Number of files belolging to a singe hdr image")
        parser.add_option("-d", "--debug", action="store_true", default=False, help="Show debug messages")
        parser.add_option("-p", "--prefix", default="hdr_", help="Prefix of the hdr images")
        parser.add_option("-m", "--mask", default="img_*.jpg", help="Mask for searching images, case insensitive")
        parser.add_option("-t", "--threshold", default="3", help="Threshold between the images, in seconds")
        parser.add_option("--moveto", default=None, help="Move files to a directory before creating hdr images")

        opts, args = parser.parse_args()
        opts.levels = int(opts.levels)
        opts.threshold = int(opts.threshold)
        
        DEBUG = opts.debug
        files = args
        self.opts = opts
        
        opts.mask = opts.mask.lower()
        
        remove_files = []
        new_files = []
        for fn in files:
            if os.path.isdir(fn):
                remove_files.append(fn)
                new_files += self.get_hdr_images(os.path.abspath(fn))
        
        files += new_files

#        print "\n".join(files)
#        sys.exit(0)

        for fn in remove_files:
            files.remove(fn)


        if opts.moveto != None:
            if not os.path.isdir(opts.moveto):
                raise UsageError, "No such directory: %s" % opts.moveto                

            new_files = []
            for fn in files:
                debug("Moving file %s to %s" % (fn, opts.moveto))
                
                shutil.move(fn, opts.moveto)
                new_files.append(pjoin(opts.moveto, os.path.basename(fn)))
                
            files = new_files
                
        if not opts.nosort:
            files.sort()

        if (len(files) % opts.levels) != 0:
            print "Invalid number of files specified, check levels parameter"
            sys.exit(1)

        self.wd = wd = WorkDir(prefix="render_hdr_").dir

        groups = [files[n:n+opts.levels] for n in xrange(0, len(files), opts.levels)]    
        
        for group in groups:
            aligned_files = self.align_images(group)
            dst_file = opts.prefix + os.path.basename(group[0])
            self.render_hdr(aligned_files, dst_file)
            
                        
if __name__ == "__main__":
    try:
        Application().main()
    except UsageError, err:
        sys.stderr.write(str(err)+"\n")
        sys.exit(1)
        