import re
import calendar
import locale
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup as bs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def Hungry(FromAddress,ToAddressList,CcAddressList,BccAddressList,Login,Password,SmtpServer):
	#This function gets todays courses and send them as email

	#Where in time are we?
	Today=datetime.today()
	Week=Today.isocalendar()[1]
	Weekday=Today.weekday() #Monday=0!
	if Weekday<5: #Don't send email on week-ends
		Days=list(calendar.day_name)
		Day=Days[Weekday].lower()
		#Now we want the swedish day
		locale.setlocale(locale.LC_TIME, "sv_SE.utf8")
		Dagar=list(calendar.day_name)
		Dag=Dagar[Weekday].lower()
		
		#EDISON
		#Get soup
		EdisonUrl = request.urlopen("http://www.restaurangedison.se/lunch")
		SoupSource = EdisonUrl.read()
		Soup = bs(SoupSource, 'lxml')

		#Tag todays weekday and its courses
		DayTag=Soup.find("div",{'id':Day})
		Course=[]
		Course.append(DayTag.find("tr"))
		Course.append(Course[0].findNext("tr"))
		Course.append(Course[1].findNext("tr"))

		CourseDescription=[]
		CourseType=[]
		for c in Course:
			CourseDescription.append(c.find("td", {'class': 'course_description'}).getText())
			CourseType.append(c.find("td", {'class': 'course_type'}).getText())

		#CAFÉ BRYGGAN
		#Get soup
		BrygganUrl = request.urlopen("http://www.bryggancafe.se/veckans-lunch/")
		SoupSourceB = BrygganUrl.read()
		SoupB = bs(SoupSourceB, 'lxml')

		#Tag start of week menu
		BrygganTag=SoupB.find('img',{'class':'alignnone size-full wp-image-413'})
		#Now we do 2*(Weekday+1) p-tag steps to get the course of the day
		BrygganP=[]
		BrygganP.append(BrygganTag.findNext('p'))
		BrygganP.append(BrygganP[0].findNext('p')) #Mondays course
		if Weekday>0:
			for i in range(1,2*Weekday+1):
				BrygganP.append(BrygganP[i].findNext('p'))
		BrygganText=BrygganP[Weekday*2+1].getText()
		CourseDescription.append(BrygganText.split(': ')[1])
		CourseType.append(BrygganText.split(': ')[0]) #Dummy course type

		#PREPARE EMAIL
		#Text version
		#Edison
		MessageText   = 'Edison\n'
		for i in range(3):
			MessageText += '\n' + CourseType[i] + ': ' + CourseDescription[i]
		#Café Bryggan
		MessageText  += '\nCafé Bryggan\n'
		MessageText  += CourseType[3] + CourseDescription[3]
			
		#HTML version
		MessageHtml="""\
		<html>
		   <head></head>
		   <body>
		      <p><h2>Edison</h2>
		      <b>{CourseType[0]}:</b> {CourseDescription[0]}.<br>
		      <b>{CourseType[1]}:</b> {CourseDescription[1]}.<br>
		      <b>{CourseType[2]}:</b> {CourseDescription[2]}.<br>
		      <h2>Café Bryggan</h2>
		      <b>{CourseType[3]}:</b> {CourseDescription[3]}.<br>
		      </p>
		   </body>
		</html>
		""".format(**locals())

		#Compile and send email
		Subject       = 'Dagens lunch ' + Dag + ' v. ' + str(Week)
		EmailPart1=MIMEText(MessageText,'plain')
		EmailPart2=MIMEText(MessageHtml,'html')
		
		MM = MIMEMultipart('alternative')
		MM['Subject']=Subject
		MM['From']=FromAddress
		MM['To']=", ".join(ToAddressList)
		MM['Cc']=", ".join(CcAddressList) #Bcc shouldn't be here
		SendMailTo = ToAddressList + CcAddressList + BccAddressList
		
		MM.attach(EmailPart1)
		MM.attach(EmailPart2)

		Server = smtplib.SMTP(SmtpServer)
		Server.starttls()
		Server.login(Login,Password)
		Problems = Server.sendmail(FromAddress,SendMailTo,MM.as_string())
		Server.quit()
		print(Problems)