
"""This program gets an XML file exported by Final Cut Pro X, gets the markers and their timecodes
 from the file and outputs a new file in a clear an concise format. Then, it sends an e-mail backup to yourself. """
# Need to read the file X
# Need to write data to a new one X
# Need to get the <marker start part, format it and put the name first.
# Convert what is after start=" and before /" to 00:00:00 format (find formula)
# Send email to me in the right format
#Changetest for git
#Regular expressions are case sensitive!

import datetime
import os
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText

#Email information input
username= raw_input(("Enter your email\n"))
yourname = raw_input("Enter your name\n")
personName = raw_input("Enter their name\n")
password = raw_input("Enter your password\n")

#Opens the FCPXML file

directory = "/Users/alvaros/Desktop/"
file = "Main Export"
tree = ET.parse(directory + file + ".fcpxml")
root = tree.getroot()


#Create the email file
OutputFile = open(directory + 'E-mail.txt','w+')

#Goes down the element tree and initializes startValue
video = root.find('project').find('sequence').find('spine').find('video')
startValue =  eval(video.get('start').replace('s',''))

#Find markers and marker names. Keep them in right order
tempmarkers = []
markersNames = []
projectName = root.find('project').get('name')

#Enter the tree, append markers and names
for marker in video.findall('marker'):
	tempmarkers.append(marker.get('start')), markersNames.append(marker.get('value'))


#Clean up marker values (get rid of the S and do the operation) and delete tempmarkers
cleanMarkers = []
for i in tempmarkers:
    i = i.replace('s','')
    cleanMarkers.append(eval(i))
del tempmarkers


#But first, write the usual stuff
OutputFile.write("Hello  " + personName +  "here\'s " + projectName +  "\'s project." + "\n\n")

#Makes a new list with the marker names and timecodes.
stufftoWrite = []
for i in range(len(cleanMarkers)):
    stufftoWrite.append(((markersNames[i])) +  " :  " + ((str(datetime.timedelta(seconds=(cleanMarkers[i]-startValue))))))


#Goes through the list and writes it, line by line.
for i in range(len(stufftoWrite)):
    OutputFile.write(str(stufftoWrite[i]+ "\n"))
OutputFile.write("\n\nThanks, " + yourname)

OutputFile.close()


#Send the email
fp = open(directory + 'E-mail.txt', 'r')
msg = MIMEText(fp.read())
fp.close()


#The email on itself
msg['Subject'] =  projectName
msg['From'] = username
msg['To'] = username
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(username,username,msg.as_string())
server.quit()

print "Email sent... I think"


#Write the tempfile into a new file (this is the method, but it should only write what is necessary and not the rest)
#OutputFile = open((directory + "/E-mail.txt" ), 'w')
#OutputFile.write(tempfile)
