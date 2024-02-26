#! env python

import os
import sys
import mmap

class Look:
    #def __init__(self, key, file='c:/program files/uwin/usr/share/dict/words'):
    def __init__(self, key, fold=False, file='/usr/share/dict/words'):
        """ Look

        file binary search somewhat like the Unix/Linux look command
        """
        self.key = key
        self.file = file
        self.fold = fold
        self.punt = 2048 # switch to linear search when lo and hi are this close
        try:
            self.size = os.path.getsize(file)
            self.fp = open(file, 'r')
            self.map = mmap.mmap(self.fp.fileno(),
                                 self.size, access=mmap.ACCESS_READ)
        except Exception as e:
            sys.stderr.write('%s: %s\n' % (' '.join(sys.argv), e.strerror) )
            sys.exit()

    def search(self):
        """ search()

        perform a file binary search
        uses mmap
        """
        if self.fold:
            self.key = self.key.lower()
        found = -1
        lo = 0
        hi = self.size

        while lo < hi:
            mid = int(lo + (hi - lo) / 2)
            self.map.seek(mid, os.SEEK_SET)

            # ensure that we are at line start
            if mid != 0:
                ln = self.map.readline().strip().decode('latin1')
                if self.fold == True: ln = ln.lower()
                if ln.startswith(self.key):
                    found = mid
                    hi = mid -1
                    continue
                else:
                    mid = self.map.tell()
            ln = self.map.readline().strip().decode('latin1')
            if self.fold == True: ln = ln.lower()

            # punt to linear search
            if (hi - lo) < self.punt:
                self.map.seek(lo, os.SEEK_SET)
                while mid < hi:
                    mid = self.map.tell()
                    ln = self.map.readline().strip().decode('latin1')
                    if self.fold == True:
                        ln = ln.lower()
                    if ln.startswith(self.key):
                        found = mid
                        break
                break

            # find the first line that starts with key
            if self.key > ln:
                lo = mid + 1
            else:
                if ln.startswith(self.key):
                    found = mid
                hi = mid - 1

        return found

    def lookiter(self):
        """ lookiter()

        return looked for lines
        """
        off = self.search()
        if off > 0:
            self.map.seek(off)
            while 1 == 1:
                try:
                    line = self.map.readline().strip().decode('latin1')
                except Exception as e:
                    print(e)
                ln = line
                if self.fold == True:
                    ln = ln.lower()
                if ln.startswith(self.key):
                    yield line
                else: break 

    def look(self):
        """ look()

        top level look function
        """
        li = self.lookiter()
        for l in li:
            try:
                print(l)
            except Exception as e:
                pass

def main():
    import optparse

    optp = optparse.OptionParser()
    optp.add_option('-f', '--fold', dest='fold',
                    help='ignore case', action='store_true',
                    default=False)
    (opts, args) = optp.parse_args()

    lk = None
    fld = False
    if opts.fold == True:
        fld = True
    if len(args) == 2:
        lk = Look(key=args[0], fold=fld, file=args[1])
    elif len(args) == 1:
        lk = Look(key=args[0], fold=fld)
    else:
        sys.stderr.write('Usage: look [-f] key (file)\n')
        sys.exit()
    if opts.fold == True:
        lk.fold = True

    lk.look()


if __name__ == '__main__':
    main()
