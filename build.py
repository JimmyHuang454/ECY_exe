import subprocess
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')


def DoCMD(cmd):
    print('\n\n==', cmd, '\n')
    subprocess.Popen(cmd, cwd=BASE_DIR, shell=True).wait()


def GetCurrentOS():
    temp = sys.platform
    if temp == 'win32':
        return 'Windows'
    if temp == 'cygwin':
        return 'Cygwin'
    if temp == 'darwin':
        return 'Mac'
    return "Linux"


DoCMD("pyinstaller -F -n ECY_%s.exe --specpath %s ./cli.py" %
      (GetCurrentOS(), BASE_DIR))

DoCMD("pyinstaller -F -n jedi_%s.exe --specpath %s ./jedi_cli.py" %
      (GetCurrentOS(), BASE_DIR))

cmd = "nexe -t x64-12.9.1 ./typescript-language-server/lib/cli.js"
DoCMD("%s -o ts_%s.exe" % (cmd, GetCurrentOS()))

cmd = "nexe -t x64-12.9.1 ./node_modules/vim-language-server/bin/index.js"
DoCMD("%s -o viml_%s.exe" % (cmd, GetCurrentOS()))
