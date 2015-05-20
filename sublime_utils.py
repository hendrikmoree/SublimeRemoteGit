from .classes.gitstatus import GitStatus
from .constants import ST_VIEW_NAME, VIEW_PREFIX, COMMIT_EDITMSG_VIEW_NAME
from sublime import Region

def currentLineNo(view):
    currentLineNo, _ = view.rowcol(view.sel()[0].a)
    return currentLineNo

def currentLineText(view):
    return view.substr(view.line(view.sel()[0]))

def findFilenameAndCommands(view):
    row, col = view.rowcol(view.sel()[0].a)
    gitStatus = GitStatus.fromMessage(view.substr(Region(0, view.size())))
    return gitStatus.fileAndCommandsForLine(row)

def gotoLine(view, lineno, atTop=False):
    if lineno is None:
        return
    textPoint = view.text_point(lineno, 0)
    pointRegion = Region(textPoint, textPoint)
    view.sel().clear()
    view.sel().add(pointRegion)
    if not atTop:
        view.show(pointRegion)
    else:
        top_offset = (lineno - 1) * view.line_height()
        view.set_viewport_position((0, top_offset), True)

def createView(window, name=ST_VIEW_NAME):
    view = window.new_file()
    view.set_name(name)
    view.set_scratch(True)
    view.settings().set('line_numbers', False)
    view.set_read_only(True)
    view.set_syntax_file('Packages/SublimeRemoteGit/%s.tmLanguage' % name)
    return view

def maybeCreateView(view, name=ST_VIEW_NAME):
    if not view.name().startswith(VIEW_PREFIX) or name == COMMIT_EDITMSG_VIEW_NAME:
        view = createView(view.window(), name=name)
    return view

def replaceView(view, edit, content, name=ST_VIEW_NAME):
    view = maybeCreateView(view, name=name)
    view.set_name(name)
    view.set_read_only(False)
    view.erase(edit, Region(0, view.size()))
    view.insert(edit, 0, content)
    view.set_read_only(True)
    view.set_syntax_file('Packages/SublimeRemoteGit/%s.tmLanguage' % name)
    return view