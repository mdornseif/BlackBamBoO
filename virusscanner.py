import re
import os

class Scanner:
    """Abstract class for representing a virusscanner"""

    def getVersion(self):
        raise NotImplementedError

    def getViruslist(self):
        raise NotImplementedError

    def isIUnstalled(self):
        raise NotImplementedError

    
class Nod32(Scanner):
    # List of Return Codes
    return_codes = {0: 'OK',
                    1: 'VIRUS',
                    2: 'CLEANED',
                    10: 'ERROR_INTERNAL'}

    def __init__(self):
        self.findBinary()
        self.virus_re = re.compile('^(?P<file>.*) - (?P<virus>.*)$')
        self.parameters = ['-subdir+',   # Enable the sub-directories scanning
                           '-pattern+',  # Enable pattern scanning
                           '-all',       # Scan all files regardless of extension
                           '-heur+',     # Enable heuristics
                           '-heursafe',  # Set safe sensitivity
                           '-log-'       # Disable logfile
                           # -basedir=<directory>        Load module from <directory>
                           ]
        
    def findBinary(self):
        self.binary = '/usr/local/av/nod32/nod32'

    def scanFiles(self, dir):
        '''
Sample Output:

? Loading module...OK

? Scanning log
? NOD32 Version 1.264 (20020605)

? Command line:  Maildir-virus
date: 7.6.2002  time: 12:04:44

? scanning path Maildir-virus
Maildir-virus/SEARCHURL.MP3.pif - Win32/Badtrans.29020.A worm
Maildir-virus/SETUP.DOC.scr - Win32/Badtrans.29020.A worm
number of diagnosed files: 162
number of viruses found: 2
termination time: 12:04:44 total time: 0 sec (00:00:00)
'''
        outlist = {}
        fd = os.popen(' '.join([self.binary] + self.parameters + [dir]), 'r')
        for l in fd.xreadlines():
            for x in l.split('\r'):
                m = self.virus_re.match(x)
                if m:
                    outlist[m.group('file')] = [m.group('virus')]
        ret = fd.close()
        if ret:
            ret = ret >> 8
        else:
            ret = 0
        if ret in self.return_codes:
            ret = self.return_codes[ret]
        else:
            ret = '(unknow status)'
        return (ret, outlist)


class Rav(Scanner):
    # List of Return Codes
    return_codes = {0: 'OK',
                    # List of Return Codes
                    #FILE_OK              1
                    #FILE_INFECTED        2
                    #FILE_SUSPICIOUS      3
                    #FILE_CLEANED         4
                    #FILE_CLEAN_FAIL      5
                    #FILE_DELETED         6
                    #FILE_DELETE_FAIL     7
                    #FILE_COPIED          8
                    #FILE_COPY_FAIL       9
                    #FILE_MOVED           10
                    #FILE_MOVE_FAIL       11
                    #FILE_RENAMED         12
                    #FILE_RENAMED_FAIL    13
                    
                    #NO_FILES             20
                    
                    #ENG_ERROR            30
                    #SINTAX_ERR           31
                    #HELP_MSG             32
                    #VIR_LIST             33
                    1: 'VIRUS',
                    2: 'CLEANED',
                    10: 'INTERNAL_ERROR'}

    def __init__(self):
        self.findBinary()
        # /usr/ho...dir-virus/cur/virus-20011207-013847-86597->(part0000:ACCSTAT.EXE) Infected: Win32/Magistr.A@mm
        self.virus_re = re.compile('^(?P<file>.*) Infected: (?P<virus>.*)$')
        self.parameters = ['--all --archive --mail',
                           '--all',                # scan all files (DEFAULT).
                           '--heuristics=off',     # enable/disable heuristics.
                           '--integrity_check=on', # enable/disable integrity checker.
                           '--archive',            # scan inside archives.
                           '--mail'                # scan mail files.
                           ]
        
    def findBinary(self):
        self.binary = '/usr/local/av/rav8/bin/ravav'

    def scanFiles(self, dir):
        outlist = {}
        fd = os.popen(' '.join([self.binary] + self.parameters + [dir]), 'r')
        for l in fd.xreadlines():
            for x in l.split('\r'):
                m = self.virus_re.match(x)
                if m:
                    outlist[m.group('file')] = [m.group('virus')]
                #for x in l.split('\r'):
                #    m = self.virus_re.match(x)
                #    if m:
                #        outlist[m.group('file')] = [m.group('virus')]
        ret = fd.close()
        if ret:
            ret = ret >> 8
        else:
            ret = 0
        return (ret, outlist)

        #if ($errval && $errval > 1) {
	#if ($errval == 2 || $errval == 3) {
	#    @virusname = ($output =~ /Infected: (.+)/g);
	#    do_virus($output);
	#} else {
	#    do_log(0,"Virus scanner failure: $rav (error code: $errval)");


from pprint import pprint
c = Rav()
pprint(c.scanFiles('/usr/home/drt/Maildir-virus/cur'))
