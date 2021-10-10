import subprocess


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


DoCMD("pyinstaller -F -N %s ./ECY/cli.py" % GetCurrentOS())
