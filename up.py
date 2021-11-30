import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')


def DoCMD(cmd, cwd=None):
    if cwd is None:
        cwd = BASE_DIR
    print('\n\n==', cmd, '\n')
    subprocess.Popen(cmd, cwd=cwd, shell=True).wait()


def NewDir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def NewArchieve(platform: str, exe: str) -> str:
    arch_dir = BASE_DIR + '/pypi/ECY_%s_%s_dir' % (platform, exe)
    NewDir(arch_dir)

    arch = arch_dir + '/ECY_%s_%s' % (platform, exe)
    NewDir(arch)

    exe_dir = arch + '/ECY_exe'
    NewDir(exe_dir)

    ##############
    #  MANIFEST  #
    ##############
    with open(BASE_DIR + '/pypi/MANIFEST_template.in', 'r') as f:
        content = f.read()
        f.close()

    with open(arch + '/ECY_exe/__init__.py', 'w') as f:
        f.close()

    with open(arch + '/MANIFEST.in', 'w') as f:
        f.write(content)
        f.close()

    ###########
    #  setup  #
    ###########
    with open(BASE_DIR + '/pypi/setup_template.py', 'r') as f:
        content = f.read()
        content = content.format(platform=platform, exe=exe)
        f.close()

    with open(arch + '/setup.py', 'w') as f:
        f.write(content)
        f.close()

    return arch


arch = NewArchieve('Windows', 'main')
arch = NewArchieve('Linux', 'main')
arch = NewArchieve('macOS', 'main')

DoCMD('python -m build', cwd=arch)
