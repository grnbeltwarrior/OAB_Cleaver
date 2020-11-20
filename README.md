# OAB_Cleaver

Situation:
  Phished an end user. Once landing on the end user system, started looking for evidence of Outlook being installed and checked if Outlook had been setup on the system. A trove of information can be gathered from the Offline Address Book files (OAB). 
  
  Location of OAB files: C:\Users\<username>\AppData\Local\Microsoft\Outlook\Offline Address Books\identifier\, I'm looking for the udetails.oab file.

Grabbed a copy of the file and started digging in.

Found an old github that says it could parse the udetails.oab file but coughed up an error when attempting to run: https://github.com/antimatter15/boa. It's also in Python2 so there is that as well. I did "hack" the errors to get valuable output after I made this script. Perhaps if I find time, I'll rewrite it in Python3.

OAB_Cleaver.py yields the following as written:
Username; email@address.com; phone

Caveats:
  Username, this is organization dependent. Enumeration of the phished end user and the layout of the smtp addresses, I found a 7 character string could get me the username from the smtp entry.
  Email Address, there are a number of smtp, sip and such entries that could match the email address regex. I only wanted those that matched first.last@domain.com for my output.
  Phone, some folks have business phones in Outlook, some don't.

To generate a udetails.txt file, I first opened the udetails.oab file with VIM. Replacing all the control characters and such using this: /[^[:alnum:][:punct:][:space:]]/, then saving the file as udetails.txt, preserving the original oab file.
