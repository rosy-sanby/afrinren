import sys
import os
from subprocess import call

folder = sys.argv[1]

for filename in os.listdir(folder):
    call(['python','fetch_results.py',folder+'/'+filename])
