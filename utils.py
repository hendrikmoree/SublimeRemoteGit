from subprocess import Popen, PIPE
from os.path import abspath, dirname
mydir = abspath(dirname(__file__))

def remoteCommand(view, command, option=None):
    args = ["bash", "remote_command.sh", projectRoot(view), '"%s"' % command]
    if option:
        args.append('"%s"' % option)
    proc = Popen(' '.join(args), cwd=mydir, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    stdout, stderr = proc.communicate(timeout=2)
    return stderr.decode('utf-8') + stdout.decode('utf-8')

def projectRoot(view):
    currentFile = view.file_name()
    if currentFile and view.window():
        for folder in view.window().folders():
            if folder in currentFile:
                return folder
    elif view.window() and view.window().folders():
        return view.window().folders()[0]
