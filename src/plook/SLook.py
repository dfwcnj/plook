
#! env python

import os
import sys

class SLook():
    #def __init__(self, key, file='c:/program files/uwin/usr/share/dict/words'):
    def __init__(self):
        """ SLook

        file binary search somewhat like the Unix/Linux look command
        """
        self.punt = 1024 # switch to linear search when lo and hi this close

    def search(self, fp, key, file, fold):
        """ search()

        perform a file binary search
        """

        if fold: key = key.lower()

        found = -1
        lo = 0
        hi = os.path.getsize(file)

        while lo < hi:

            mid = int(lo + (hi - lo) / 2)
            fp.seek(mid, os.SEEK_SET)

            # ensure that we are at line start
            if mid != 0:
                #ln = fp.readline().strip().decode('latin1')
                ln = fp.readline().strip()
                if fold == True: ln = ln.lower()
                if ln.startswith(key):
                    found = mid
                    # continue searching for the first
                    hi = mid -1
                    continue
                else:
                    mid = fp.tell()
            #ln = fp.readline().strip().decode('latin1')
            ln = fp.readline().strip()
            if fold == True: ln = ln.lower()

            # punt to linear search
            if (hi - lo) < self.punt:
                fp.seek(lo, os.SEEK_SET)
                while lo < hi:
                    mid = fp.tell()
                    #ln = fp.readline().strip().decode('latin1')
                    ln = fp.readline().strip()
                    if fold == True:
                        ln = ln.lower()
                    if found > mid and ln.startswith(key):
                        # should be the first
                        found = mid
                        break
                break

            # find the first line that starts with key
            if key > ln:
                lo = mid + 1
            else:
                if ln.startswith(key):
                    found = mid
                # continue searching for the first
                hi = mid - 1

        return found

    def lookiter(self, fp, key, file, fold):
        """ lookiter()

        return looked for lines
        """
        lines = []
        off = self.search(fp, key, file, fold)
        if off >= 0:
            fp.seek(off)
            while 1 == 1:
                try:
                    #line = fp.readline().strip().decode('latin1')
                    line = fp.readline().strip()
                except Exception as e:
                    print(e)
                ln = line
                if fold == True:
                    ln = ln.lower()
                if ln.startswith(key):
                    lines.append(ln)
                else: break 
        return lines

    def look(self, key, file, fold):
        """ look()

        top level look function
        """
        with open(file, 'r') as fp:
            li = self.lookiter(fp, key, file, fold)
            for l in li:
                try:
                    print(l, file=sys.stdout)
                except Exception as e:
                    print('%s %s %s' % (key, file, e), file=sys.stderr)

def main():
    import argparse
    argp = argparse.ArgumentParser(description='file binary search')
    argp.add_argument('--file', default='/usr/share/dict/words',
        help='sorted text file to search')
    argp.add_argument('--key', required=True,
        help='word to search')
    argp.add_argument('--fold', action='store_true', default=False,
        help='fold case - case independent search')

    args = argp.parse_args()

    slk = SLook()
    slk.look(args.key, args.file, args.fold)


if __name__ == '__main__':
    main()
