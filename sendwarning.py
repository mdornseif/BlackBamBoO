import os, os.path, time, smtplib, rfc822
from Cheetah.Template import Template
from config import config

# size

def sendwarning(originalMessage, sender, recipient, bbboid, reportName, otherInfo):
    """Send a warning message to the Sender of a message and the intended recipient.

    * originalMessage should be a file-like object pointing to the original message
    * sender is the envelope sender of the originalMessage
    * recipient is the envelope recipient of the priginalMessage
    * bbboid is a bbboid internal for the original message
    * reportName is the mane of the report to be send. is used to locate the templates
    * otherInfo contains other info which is to be passed to the template
    """


    # parse originalHeaders

    originalMessageObj = rfc822.Message(originalMessage)
    # this is an undocumented feature of rfc822
    headers = originalMessageObj.dict
    # add standard headers if needed
    if not headers.has_key('to'):
        headers['to'] = '<no To-Header set>'
    if not headers.has_key('from'):
        headers['from'] = '<no Form-Header set>'
    if not headers.has_key('subject'):
        headers['subject'] = '<no Subject-Header set>'
    if not headers.has_key('date'):
        headers['date'] = '<no Date-Header set>'
    if not headers.has_key('message-id'):
        headers['message-id'] = '<no Message-Id-Header set>'
    
    nameSpace = {'messageid': 'bbbo-s-%s@%s' % (bbboid, config.myFqdn),
                 'mailheader': headers,
                 'date': time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),
                 'config': config,
                 'sender': sender,
                 'recipient': recipient,
                 'bbboid': bbboid,
                 'originalheaders': 'originalHeaders'}
    # send message to onverlope sender
    templateObj = Template(file=os.path.join(config.templatePath, '%s-sender.txt' % reportName),
                           searchList = [nameSpace, otherInfo])
    server = smtplib.SMTP(config.smtpServer)
    server.set_debuglevel(config.smtpDebugLevel)
    server.sendmail(config.reportSender, sender, str(templateObj))
    # send message to intended recipient
    nameSpace['messageid'] = 'bbbo-r-%s@%s' % (bbboid, config.myFqdn)
    templateObj = Template(file=os.path.join(config.templatePath, '%s-recipient.txt' % reportName),
                           searchList = [nameSpace, otherInfo])
    server.sendmail(config.reportSender, recipient, str(templateObj))
    # done
    server.quit()

if __name__ == '__main__':
    import StringIO
    sendwarning(StringIO.StringIO(r"""Return-Path: <ZJqq@tcts1.seed.net.tw>
Delivered-To: log@gate.hudora.de
Received: (qmail 93834 invoked by uid 53); 11 May 2002 15:50:56 -0000
Date: 11 May 2002 15:50:56 -0000
Received: from cm61-15-246-80.hkcable.com.hk(61.15.246.80), claiming to be "pavilion"
 via SMTP by gate.hudora.de, id smtpdLBCsW5; Sat May 11 17:50:54 2002
Received: from gcn
	by iris.seed.net.tw with SMTP id nGzf4iEJtbLs73ngBP2n;
	Sun, 12 May 2002 00:33:13 +0800
Message-ID: <Ava4v@yahoo.com>
From: 852-2602@gate.hudora.de, 8368@gate.hudora.de
To: Hk032@gate.hudora.de
Subject:852-2602 8368
X-Mailer: hM429d5XAdd43hpfG1KRTg4sZE9k
Content-Type: text/plain;
Content-Transfer-Encoding: Quoted-Printable
X-Priority: 3
X-MSMail-Priority: Normal

=A7K=BB3=E6..=A8=EE=A7@=A4=BD=A5q=C2=F8=BBx=A1K=AE=D1=A5Z=A1K..=BA=F4=AD=B6=B3]=ADp=A1K=A1K
"""),
                'md-sender@hudora.de',
                'md-recipient@hudora.de',
                "%f-%d" % (time.time(), os.getpid()),
                'blocked-report',
                {'name': 'name', 'description': 'reason', 'explanation': 'longreason'}
                )
