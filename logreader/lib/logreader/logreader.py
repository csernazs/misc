
import re
from os import SEEK_END, SEEK_SET, SEEK_CUR
import datetime

class LogReaderError(Exception):
    pass
    
class LogReader(object):
    def __init__(self, file, line_regexp):
        if isinstance(file, basestring):
            self.file = open(file, "rU")
        else:
            self.file = file
            
        self.line_regexp = line_regexp

    
    def seek_to_timestamp(self, timestamp):

        self.file.seek(0)
        self.file.seek(0, SEEK_END)

        fmin = 0
        fmax = self.file.tell()
        fmid = fmin + (fmax-fmin)/2
        while True:
            self.file.seek(fmid)
            self.file.readline() # skip to the next \n
            line = self.file.readline().rstrip("\n") # read a whole line
            line_ts = self.get_timestamp(line)
            
            if line_ts < timestamp:
                fmax = fmid
            elif line_ts > timestamp:
                fmin = fmid
                
        
        
    def get_timestamp(self, line):
        m = self.line_regexp.match(line)
        if m:
            if m.groups():
                args = [int(x) for x in m.groups()[:6]]
                retval = datetime.datetime(*args)
            elif m.groupdict():
                kwargs = {k:int(v) for k, v in m.groupdict() if k in ("year", "month", "day", "hour", "minute", "second")}
                retval = datetime.datetime(**kwargs)
            else:
                raise LogReaderError("Invalid regexp, no groups found")
        else:
            raise LogReaderError("Invalid line, regexp not matching: %s" % repr(line))
            
        return retval                    


    
    def get_line_regexp(self):
        return self._line_regexp

    def set_line_regexp(self, value):
        if isinstance(value, basestring):
            self._line_regexp = re.compile(value)
        else:
            self._line_regexp = value

    line_regexp = property(get_line_regexp, set_line_regexp)        