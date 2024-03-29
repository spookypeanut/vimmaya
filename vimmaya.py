import vim
import string
import time
import os
import tempfile
from threading import Thread
import socket

_scratchname = "~/mayascratch.mel"
_scratchbuffer = None
_buffername = "MayaOutput"
_init = False
_maya = None
_buffer = None
_listenthread = None
_hostname = "localhost"
_portnumarray = [7092, 7093, 7094, 7095]
_portnum = 7092
_buffersize = 4096 
_sleeptime = 0.1 # in seconds


class PortListener(Thread):
    def __init__ (self):
        Thread.__init__(self)
    def run(self):
        global _init
        global _sleeptime
        while _init:
            MayaRefreshBuffer()
            time.sleep(_sleeptime)

def MayaQuit():
    global _init
    _init = False

def MayaJinit():
    # So I don't have to swap back and forth between failed attempts at multi-port and single port
    global _maya
    global _init
    global _portnum
    global _portnumarray
    global _hostname

    _maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for eachport in _portnumarray:
        print "Trying" + str(eachport)
        try:
            _maya.connect((_hostname, eachport))
        except socket.error, e:
            continue
        teststring = "vimmayaPortTest"
        _maya.send("print \"" + teststring + "\"")
        time.sleep(.1)
        tempbuffer = _maya.recv(64)
        if teststring == tempbuffer.split()[2].strip():
            _portnum = eachport
            break
    _init = True

def MayaInit():
    global _maya
    global _init
    global _portnum
    global _portnumarray
    global _hostname

    _maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        _maya.connect((_hostname, _portnum))
    except socket.error, e:
        return

    # I know, horrible hacky way to do multi-line comments...
    '''
    for eachport in _portnumarray:
        #print "Trying" + str(eachport)
        try:
            _maya.connect((_hostname, eachport))
        except socket.error, e:
            continue
        teststring = "vimmayaPortTest"
        _maya.send("print \"" + teststring + "\"")
        time.sleep(.1)
        tempbuffer = _maya.recv(64)
        if teststring == tempbuffer.split()[2].strip():
            _portnum = eachport
            break'''
            
    _init = True

def MayaSubmitIt(txt):
    if not _init:
        return
    CreateMayaBuffer()
    _maya.send(txt)

def SwitchWindow(newbuffer):
    newname = newbuffer.name
    for i in range(0, len(vim.windows)):
        if vim.windows[i].buffer == newbuffer:
            cmd = "exe " + str(i + 1) + " . \"wincmd w\""
            vim.command(cmd)
            break

def MayaRefreshBuffer():
    if not _init or not _buffer:
        return

    global _buffersize
    tempbuffer = _maya.recv(_buffersize)
    if tempbuffer:
        cleanbuffer = CleanOutput(tempbuffer)
        if cleanbuffer:
            oldbuff = vim.current.buffer
            SwitchWindow(_buffer)

            vim.command("setlocal modifiable")
            vim.current.buffer.append(cleanbuffer)
            vim.command("setlocal nomodifiable")

            MayaFindBufferEnd()
            SwitchWindow(oldbuff)
            vim.command("redraw")

def CleanOutput(dirtyoutput):
    global _hostname
    global _portnum

    mylist = string.split(dirtyoutput.replace('\0', '\n'), '\n')
    mylist[len(mylist) - 1] = mylist[len(mylist) - 1][:-1]
    returnlist = []
    for line in mylist:
        if line == '' or line == "// WARNING: unknown result type" or line == "// ERROR: unknown maya error" or line == ";":
            continue

        portnumstart = "(" + _hostname + ":" + str(_portnum) + ") "
        if line.startswith(portnumstart):
            line = line[len(portnumstart):]
        
        if line.startswith(": "):
            line = line[2:]

        if line.startswith("<vimcmd>"):
            vim.command(line[8:-9])     # TODO Should really use regexp, but i'm too lazy
            continue
        
        returnlist.append(line)

    return returnlist

def MayaFindBufferEnd():
    global _buffer
    for i in vim.windows:
        if i.buffer == _buffer:
            window = i

    if not window:
        return

    window.cursor = (len(_buffer),0)
    vim.command("redraw")

def CreateMayaBuffer():
    global _buffer
    global _buffername
    global _listenthread
    
    if not _buffer:
        vim.command("split " + _buffername)
        vim.command("setlocal buftype=nofile")
        vim.command("setlocal nomodifiable")
        vim.command("setlocal bufhidden=hide")
        vim.command("setlocal noswapfile")
        _buffer = vim.current.buffer
        _listenthread = PortListener()
        _listenthread.start()
        vim.command("redraw!")


    mayawindow = None
    for i in vim.windows:
        if i.buffer == _buffer:
            mayawindow = i

    if mayawindow == None:
        vim.command("sbuffer " + _buffername)
        vim.command("redraw!")

    if mayawindow.height < 10:
        mayawindow.height = 10

def MayaTest():
    message = "Maya is correctly connected to vim"
    MayaSubmitIt("print \"" + message + "\";")
    MayaSubmitIt("confirmDialog -title \"Test from vim\" -message \"" + message + "\" -button \"OK\" -defaultButton \"OK\" -cancelButton \"OK\";")

def MayaScratch():
    global _scratchname
    global _scratchbuffer

    if not _scratchbuffer:
        vim.command("split " + _scratchname)
        _scratchbuffer = vim.current.buffer

    mayawindow = None
    for i in vim.windows:
        if i.buffer == _scratchbuffer:
            mayawindow = i

    if mayawindow == None:
        vim.command("sbuffer " + _scratchname)
        vim.command("redraw!")

def MayaLine():
    line = vim.current.line + "\n"
    MayaSubmitIt(line)

def MayaClear():
    global _buffer
    oldbuff = vim.current.buffer
    SwitchWindow(_buffer)

    vim.command("setlocal modifiable")
    _buffer[:] = None
    vim.command("setlocal nomodifiable")

    SwitchWindow(oldbuff)

def MayaSourceCurrent():
    global _scratchbuffer
    global _buffer
    if vim.current.buffer != _buffer and vim.current.buffer != _scratchbuffer:
        filename = vim.current.buffer.name
        MayaSubmitIt("print (\"Sourcing " + filename + "\\n\");")
        MayaSubmitIt("source \"" + filename + "\";")

def MayaRange():
    range = vim.current.range
    lines = ""
    for line in range:
        lines += line + "\n"
    tempnum, tempname = tempfile.mkstemp()
    os.write(tempnum, lines)
    MayaSubmitIt("source \"" + tempname + "\";")
    # We have to do it this way, otherwise the file is gone before Maya gets it
    MayaSubmitIt("print \"<vimcmd>python os.unlink(\\\"" + tempname + "\\\")</vimcmd>\"")

