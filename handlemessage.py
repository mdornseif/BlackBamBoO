import os, os.path, time
import types
import logging
from config import config
from mailparse import mailparse
from checkextensions import checkextensions
from sendwarning import sendwarning

logging.basicConfig()

log = logging.getLogger("bbbo")


def rmdirandcontents(dirname):
    """remove a directrory hieraachy a la rm -Rf"""

    files = os.listdir(dirname)
    if files:
        for x in [os.path.join(dirname, y) for y in files]:
            if os.path.isdir(x):
                rmdirandcontents(x)
            else:
                os.unlink(x)
    os.rmdir(dirname)


# todo: empty reserve path

def dispose(msgFile, workDir, disposeDir):
    "Removes cruft and put a message into a dir for further processing"

    # move message to disposal dir
    disposeFile = os.path.join(disposeDir, 'new', os.path.split(msgFile)[1]) 
    os.rename(msgFile, disposeFile)
    # TODO add headers
    # delete workdir
    rmdirandcontents(workDir)
    

def handleMessage(origMsg, sender, recipient):
    # create id
    bbboid = hex(long(time.time() * os.getpid()))[2:-1]
    log.info("Id: [%s]handling message from %r to %r in %r", bbboid, sender, recipient, origMsg)
    try:
        msgFile = os.path.join(config.workPath, os.path.split(origMsg)[1])
        msgDir = os.path.join(config.workPath, bbboid)
        # move message to work area
        os.rename(origMsg, msgFile)
        # create unpack dir
        os.makedirs(msgDir, 0700)

        # unpack / parse
        (parts, headers, problem) = mailparse(msgFile, msgDir)
        if problem:
            log.info('[%s] blocking because of parsing problem extensions: %s', bbboid, problem.name)
            sendwarning(open(msgFile),
                        sender, recipient, bbboid,
                        'blocked-report',
                        {'problem': problem.getInfoDict()})
            dispose(msgFile, msgDir, config.quarantainePath)
            return

        # TODO: virusscan

        # check for unwanted extensions 
        problem = checkextensions(parts)
        if problem:
            log.info('[%s] blocking because of unwanted extensions: %s', bbboid, problem.info['usedextension'])
            sendwarning(open(msgFile),
                        sender, recipient, bbboid,
                        'blocked-report',
                        {'problem': problem.getInfoDict()})
            dispose(msgFile, msgDir, config.quarantainePath)
            return
        # check for unwanted filetypes
        # check for unwanted encodings

        # put in outqueue
        log.info('[%s] passing', bbboid)
        dispose(msgFile, msgDir, config.outqueuePath)

        # TODO: check for left over messages
    except Exception, e:
        #raise
        log.exception("[%s] unhandled exception", bbboid)
                

if __name__ == '__main__':
    handleMessage('/Users/md/Desktop/code/bbbo/testmails/virus-20011207-005751-81929',
                  'md-sender@hudora.de',
                  'md-recipient@hudora.de')
