#!/usr/bin/python3

# Quick and dirty script to get username, email and phone number from a udetails oab file
# grnbeltwarrior (https://www.github.com/grnbeltwarrior)

import sys
import re
import fnmatch
import string
from progressbar import ProgressBar

# get the domain to search on
domain = '@domain.com'

# dictionary of things to search and replace on - makes for easier adding and removing these down the line
replaceMe = {
'SMTP:': ';SMTP:',
'smtp:': ';smtp:',
'SIP:': ';SIP:',
'sip:': ';sip:',
'X500:': ';X500:',
domain:'@domain;',
';;;': ';',
';;': ';',
'  ': ' '
}
def main(argv):
        # Progress bars because if you run into 100k entries like I did, you start to wonder what the frick actual is happening.
        pbar = ProgressBar()
        progress = ProgressBar()
        inputfile = './udetails.txt' 
        # read in file
        f = open(inputfile,"r", errors='ignore')
        myStr = f.read()
        # Contacts may be in different Exchange locations, so you may or may not have more than 1 entry for the SMTP/X500/SIP entries.
        myStr = myStr.replace('X500:/o=<REDACTED>/cn=Recipients/cn=',';X500:')
        # The redacted part can usually be seen in the udetails.oab file using something like VIM. This will be the entry that is separating the address book entries themselves.
        userSplit = myStr.split('/o=<REDACTED>/cn=Recipients/cn=')
        # The length of userSplit gives you an indication of how many entries there are within the OAB file.
        print('Number of user strings found:',len(userSplit))
        # Probably a horrible job of trying to get a CSV file, YMMV. Mainly using it to split the email entries to iterate through each one to get what I want.
        for user in userSplit:
                # Run through the dictionary and make the changes needed
                for k, v in replaceMe.items():
                        if k in user:
                        user = user.replace(k,v)
        myList = myStr.split(';')
        print('Count of split items to inventory:',len(myList))
        smtpList = []
        usernameList = []
        comboList = []
        for thing in pbar(myList):
                # Find matching email addresses
                match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', thing)
                for entry in match:
                        if domain in entry:
                                if entry not in smtpList:
                                        smtpList.append(entry)
                                        temp = entry.split('@', 1)[0]
                                        # How I found usernames: observered username from phished end user, formulated a length standard. 
                                        # Then observed SMTP address of that username standard in the udetails file: gbwarr2@domain.com
                                        if len(temp) == 7:
                                                usernameList.append(temp)
        # Look for phone numbers too
        # format as I observed: 111/222-3333
        phoneList = []
        regex_phone = "\w{3}/\w{3}-\w{4}"
        print('smtpList:',len(smtpList))
        print('usernameList:', len(usernameList))
        with open('./8_SMTP_List.txt', 'w') as f_smtp:
                for smtp in smtpList:
                        f_smtp.write("%s\n" % smtp)
        with open('./8_Username_List.txt', 'w') as f_username:
                for username in usernameList:
                        f_username.write("%s\n" % username)
        # Need to split up the first.last@domain.com and the username@domain.com
        # match up username and email:
        for username in progress(usernameList):
                smtp = ''
                phone = ''
                result = [i for i in userSplit if username in i]
                tempLine = str(result)
                lineSplitter = tempLine.split(';')
                for thing in lineSplitter:
                        if smtp == '':
                                # Gets the smtp addresses
                                smtpMatch = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', thing)
                                # Get smtp with firstname.lastname@domain.com
                                for entry in smtpMatch:
                                        if (domain in entry) and (entry.count('.') > 1):
                                                smtp = entry
                        # Gets the phone numbers matching (standard US) 333/333-4444
                        phoneMatch = re.findall(regex_phone, thing)
                        if len(phoneMatch) > 0:
                                for num in phoneMatch:
                                        phone = str(phoneMatch)
                comboString = username + ";" + smtp + ";" + phone
                comboList.append(comboString)
        with open('./8_User_SMTP_List.txt', 'w') as f_list:
                for line in comboList:
                        f_list.write("%s\n" % line)
        f.close()

if __name__ == "__main__":
        main(sys.argv[1:])
