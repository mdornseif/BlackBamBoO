import email.Parser
import mimetypes
import os, os.path
import sys

import partinfo
import problems

class MimeProblem(problems.Problem):
        def __init__(self, name = 'broken mime',
                     description = "Your message's MIME encoding is broken",
                     explanation = "Messages in the Internet are usually encoded via a standart called\nMIME. The Message was MIME encoded, but the MIME ancoding was\nincorrect so our mailsystem was not able to parse and process your\nmessage. This usually indicates a major problem in the sender's email\nsoftware. The exact error was:\n%(mimeexception)s %(mimeerror)s",
                     level = problems.REJECT):
            problems.Problem.__init__(self, name, description, explanation, level)



mimet = {'text/plain': 'txt',
         'text/html': 'html'}

def my_guess_extension(type):
  ext = mimetypes.guess_extension(type, None) 
  # we have our own additionallist, since I often dislike guess_extensions suggestions 
  if type in mimet:
    ext = '.' + mimet[type]
  return ext

def clean_filename(name):
  """removes all characters from a filename which might become dangerous and shortens it to no more than 64 characters.

  print clean_filename('../../../got!$root&%/test')
  '_________got__root___test'
  """

  return name.translate(r"___________________________________________+_-._0123456789______@ABCDEFGHIJKLMNOPQRSTUVWXYZ______abcdefghijklmnopqrstuvwxyz_____________________________________________________________________________________________________________________________________").replace('..', '__')[:64]



def mailparse(mailFile, unpackDir):
  return mimeunpack(mailFile, unpackDir)

def mimeunpack(mailFile, unpackDir):
  mailFile=open(mailFile, "rb")
  p=email.Parser.Parser()
  try:
    msg=p.parse(mailFile)
  except email.Errors.BoundaryError, msg:
    return (None, None, MimeProblem().addinfo({'mimeexception': 'Boundary Error:', 'mimeerror': msg}))
  except email.Errors.HeaderParseError, msg:
    return (None, None, MimeProblem().addinfo({'mimeexception': 'Header Error:', 'mimeerror': msg}))
  except email.Errors.MessageParseError, msg:
    return (None, None, MimeProblem().addinfo({'mimeexception': 'Parsing Error:', 'mimeerror': msg}))
  mailFile.close()

  partcounter=1
  partlist = []
  for part in msg.walk():
    if part.get_main_type()=="multipart":
      continue
    name = part.get_filename(None)
    if name == None:
      name = part.get_param("name")
    if name==None:
      ext = my_guess_extension(part.get_type('text/plain'))
      if ext == None:
        ext = '.bin'
      name = "noname%s" % ext
    name = clean_filename("p%i-%s" %(partcounter, name))
    partcounter+=1
    # In real life, make sure that name is a reasonable
    # filename on your OS.
    f=open(os.path.join(unpackDir, name), "wb")
    f.write(part.get_payload(decode=1))
    f.close()
    partlist.append(partinfo.MessagePart(name, part.get_type('unknown'), part.get_filename(None), os.path.getsize(os.path.join(unpackDir, name))))
    del(part)

  # normalize headers
  headers = {}
  for k in msg.keys():
    headers['-'.join([x.capitalize() for x in k.split('-')])] = msg[k] 
  
  return (partlist, headers, None)

if __name__=="__main__":
  main()
