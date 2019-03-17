import os
import sys
import glob

for dir in sys.path:
    print(dir)
    files = os.path.join (dir, "**/htmltables*")
    files_found = glob.glob(files, recursive=True)
    for file in files_found:
        print('   ', file)