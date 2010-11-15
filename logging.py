import time, os, cPickle
from datetime import datetime
from debug import DefaultDict, Debug

Logging = DefaultDict(0)
Logging.set('USERLOG', True)

logdir = 'logs'
logbuffer = None
logfilename = ''

def getLogFilename():
    now = datetime.now()
    return '%s/log-%d-%02d-%02d.txt' % (logdir,now.year,now.month,now.day)

def openlogbuffer():
    global logbuffer, logfilename
    if logbuffer != None:
        closelogbuffer()
        
    logfilename = getLogFilename()
    logbuffer = open(logfilename, 'a')

def getlogbuffer():
    # If we've passed to the next day, switch to the next log file
    if logbuffer == None or logfilename != getLogFilename():
        openlogbuffer()
    return logbuffer

def closelogbuffer():
    global logbuffer
    logbuffer.close()
    logbuffer = None

def errordump(errorobj):
    errornum = 0
    while True:
        filename = logdir + '/errordump_' + str(errornum)
        if not os.path.exists(filename):
            break
        errornum += 1
    f = open(filename, 'wb')
    cPickle.dump(errorobj, f)
    f.close()
    return filename

def log(msg, category='', component='', closeafterwrite=False, buffer=None):
    if not Logging(category) and not Debug("VERBOSE"): return
    
    if buffer == None:
        buffer = getlogbuffer()

    fullmsg = component
    if component and component != '':
        fullmsg += ': '
    fullmsg += msg
    
    fullmsg = time.strftime('%c') + ": " + fullmsg
    if Debug("PRINT_LOG"):
        print fullmsg

    buffer.write(fullmsg + '\n')
    buffer.flush()

    if closeafterwrite:
        closelogbuffer(buffer)
