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
	Weekday=Today.weekday() #Monday=0
	#Weekday=int(input("Please enter weekday [0-6]: ")) #For testing
	if Weekday<5: #Don't send email on week-ends
		#TIME
		Days=list(calendar.day_name)
		Day=Days[Weekday].lower()
		#Now we want the swedish day
		#locale.setlocale(locale.LC_TIME,"sv_SE.utf8") #Linux environment
		locale.setlocale(locale.LC_TIME,"sv-SV") #Windows environment
		Dagar=list(calendar.day_name)
		Dag=Dagar[Weekday].lower()
		
		#OUTPUT VARIABLES
		CourseDescription=[]
		CourseType=[]
		Place=[]

		#PLACE URLS
		PlaceUrl=[]
		PlaceUrl.append('http://www.restaurangedison.se/lunch/')
		PlaceUrl.append('http://www.bryggancafe.se/veckans-lunch/')
		PlaceUrl.append('http://www.finninn.se/lunch-meny/')
		PlaceUrl.append('http://morotenopiskan.se/lunch/')

		#EDISON
		EdisonOut=GetEdison(Day,PlaceUrl[0])
		#print(str(EdisonOut))
		CourseDescription.extend(EdisonOut[0])
		CourseType.extend(EdisonOut[1]) 
		Place.extend(EdisonOut[2])

		#CAFÉ BRYGGAN
		BrygganOut=GetBryggan(Weekday,PlaceUrl[1])
		#print(str(BrygganOut))
		CourseDescription.extend(BrygganOut[0])
		CourseType.extend(BrygganOut[1]) 
		Place.extend(BrygganOut[2])

		#FINN INN
		FinnInnOut=GetFinnInn(Weekday,PlaceUrl[2])
		#print(str(FinnInnOut))
		CourseDescription.extend(FinnInnOut[0])
		CourseType.extend(FinnInnOut[1])
		Place.extend(FinnInnOut[2])

		#MOROTEN OCH PISKAN (Mop)
		MopOut=GetMop(datetime.today().day,PlaceUrl[3]) #input todays calendar day
		#print(str(MopOut))
		CourseDescription.extend(MopOut[0])
		CourseType.extend(MopOut[1])
		Place.extend(MopOut[2])

		#PREPARE EMAIL
		#Text and HTML version
		#Edison
		MessageText   = 'Edison\n'
		BodyHTML	  = '<p><h2><a href='+PlaceUrl[0]+'>Edison</a></h2>'
		for i in range(len(CourseDescription)):
			if Place[i]==1:
				MessageText += '\n' + CourseType[i] + ': ' + CourseDescription[i]
				BodyHTML += '<b>' + CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
		#Café Bryggan
		MessageText  += '\nCafé Bryggan'
		BodyHTML     += '<h2><a href='+PlaceUrl[1]+'>Café Bryggan</a></h2>'
		for i in range(len(CourseDescription)):
			if Place[i]==2:
				MessageText  += '\n' + CourseType[i] + CourseDescription[i]
				BodyHTML += '<b>' + CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
		#Finn Inn
		MessageText  += '\nFinn Inn'
		BodyHTML     += '<h2><a href='+PlaceUrl[2]+'>Finn Inn</a></h2>'
		for i in range(len(CourseDescription)):
			if Place[i]==3:
				MessageText  += '\n' + CourseType[i] + CourseDescription[i]
				BodyHTML += '<b>' + CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
		#Moroten och piskan
		MessageText  += '\nMoroten och Piskan'
		BodyHTML     += '<h2><a href='+PlaceUrl[3]+'>Moroten och Piskan</a></h2>'
		for i in range(len(CourseDescription)):
			if Place[i]==4:
				MessageText  += '\n' + CourseType[i] + CourseDescription[i]
				BodyHTML += '<b>' + CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
		
		#Contribute?!
		MessageText  += '\n\nMedverka: https://github.com/Pivaro/HungryEmail'
		
		#HTML version
		BodyHTML     += '</p>'

		# Styling from https://raw.githubusercontent.com/sendwithus/templates/master/templates/plain-jane/plain.html
		HeadHTML	 ="""
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Plain Jane Text</title>
    <style type="text/css">
      /* Based on The MailChimp Reset INLINE: Yes. */
      /* Client-specific Styles */
      #outlook a {
        padding: 0;
      }

      /* Force Outlook to provide a "view in browser" menu link. */
      body {
        width: 100% !important;
        margin: 0;
        padding: 0;
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
      }

      /* Prevent Webkit and Windows Mobile platforms from changing default font sizes.*/
      .ExternalClass {
        width: 100%;
      }

      /* Force Hotmail to display emails at full width */
      .ExternalClass,
      .ExternalClass p,
      .ExternalClass span,
      .ExternalClass font,
      .ExternalClass td,
      .ExternalClass div {
        line-height: 100%;
      }

      /* Forces Hotmail to display normal line spacing.  More on that: http://www.emailonacid.com/forum/viewthread/43/ */
      #backgroundTable {
        margin: 0;
        padding: 0;
        width: 100% !important;
        line-height: 100% !important;
      }
      /* End reset */
      /* Some sensible defaults for images
          Bring inline: Yes. */

      img {
        outline: none;
        text-decoration: none;
        -ms-interpolation-mode: bicubic;
      }

      a img {
        border: none;
      }

      .image_fix {
        display: block;
      }

      /* Yahoo paragraph fix
          Bring inline: Yes. */
      p {
        margin: 1em 0;
      }

      /* Hotmail header color reset
          Bring inline: Yes. */
      h1, h2, h3, h4, h5, h6 {
        color: black !important;
      }

      h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        color: blue !important;
      }

      h1 a:active, h2 a:active, h3 a:active, h4 a:active, h5 a:active, h6 a:active {
        color: red !important;
        /* Preferably not the same color as the normal header link color.  There is limited support for psuedo classes in email clients, this was added just for good measure. */
      }

      h1 a:visited, h2 a:visited, h3 a:visited, h4 a:visited, h5 a:visited, h6 a:visited {
        color: #000;
        color: purple !important;
        /* Preferably not the same color as the normal header link color. There is limited support for psuedo classes in email clients, this was added just for good measure. */
      }

      /* Outlook 07, 10 Padding issue fix
          Bring inline: No.*/
      table td {
        border-collapse: collapse;
      }

      /* Remove spacing around Outlook 07, 10 tables
          Bring inline: Yes */
      table {
        border-collapse: collapse;
        mso-table-lspace: 0pt;
        mso-table-rspace: 0pt;
      }


      /* Global */
      * {
        margin: 0;
        padding: 0;
      }

      body {
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
        width: 100%!important;
        height: 100%;
        font-family: Cambria, Utopia, "Liberation Serif", Times, "Times New Roman", serif;
        font-weight: 400;
        font-size: 100%;
        line-height: 1.6;
      }

      /* Styling your links has become much simpler with the new Yahoo.  In fact, it falls in line with the main credo of styling in email and make sure to bring your styles inline.  Your link colors will be uniform across clients when brought inline.
          Bring inline: Yes. */
      a {
        color: #348eda;
      }

      h1, h2, h3, h4, h5,
      p, ul, ol {
        /* This fixes Gmail's terrible text rendering  */
        font-family: Cambria, Utopia, "Liberation Serif",Times, "Times New Roman", serif;
        font-weight: 400;
      }

      h1, h2, h3, h4, h5 {
        margin: 20px 0 10px;
        color: #000;
        line-height: 1.2;
      }

      h1 { font-size: 32px; }
      h2 { font-size: 26px; }
      h3 { font-size: 22px; }
      h4 { font-size: 18px; }
      h5 { font-size: 16px; }

      p, ul, ol {
        margin-bottom: 10px;
        font-weight: normal;
        font-size: 16px;
        line-height: 1.4;
      }

      ul li,
      ol li {
        margin-left: 5px;
        list-style-position: inside;
      }

      /* Body */
      table.body-wrap {
        width: 100%;
        padding: 30px;
      }


      /* Footer */
      table.footer-wrap {
        width: 100%;
        clear: both!important;
      }

      .footer-wrap .container p {
        font-size: 12px;
        color: #666;
      }

      table.footer-wrap a {
        color: #999;
      }


      /* Give it some responsive love */
      .container {
        display: block!important;
        max-width: 600px!important;
        margin: 0 auto!important; /* makes it centered */
        clear: both!important;
      }

      /* Set the padding on the td rather than the div for Outlook compatibility */
      .body-wrap .container {
        padding: 30px;
      }

      /* This should also be a block element, so that it will fill 100% of the .container */
      .content {
        max-width: 600px;
        margin: 0 auto;
        display: block;
      }

      /* Let's make sure tables in the content area are 100% wide */
      .content table {
        width: 100%;
      }
    </style>
    <!--[if gte mso 9]>
      <style>
        /* Target Outlook 2007 and 2010 */
      </style>
    <![endif]-->
		"""
		MessageHtml="""\
		<html>
		    <head>
			{HeadHTML}
			</head>

  <body>

    <table id="backgroundTable" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td>

          <!-- body -->
          <table class="body-wrap">
            <tr>
              <td></td>
              <td class="container" bgcolor="#FFFFFF" valign="top">

                <!-- content -->
                <div class="content">
                <table>
                  <tr>
                    <td>
		        {BodyHTML}	
</td>
                  </tr>
                </table>
                </div>
                <!-- /content -->

              </td>
              <td></td>
            </tr>
          </table>
          <!-- /body -->

          <!-- footer -->
          <table class="footer-wrap" cellpadding="0" cellspacing="0" border="0" align="center" >
            <tr>
              <td></td>
              <td class="container">

                <!-- content -->
                <div class="content">
                  <table>
                    <tr>
                      <td align="center" valign="top">
                        <p>Medverka? <a href="https://github.com/Pivaro/HungryEmail"><unsubscribe>https://github.com/Pivaro/HungryEmail</unsubscribe></a>.</p>
                      </td>
                    </tr>
                  </table>
                </div>
                <!-- /content -->

              </td>
              <td></td>
            </tr>
          </table>
          <!-- /footer -->

        </td>
      </tr>
    </table>
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

def GetEdison(Day,Url):
	try:
		CourseDescription=[]
		CourseType=[]
		Place=[]
		#Get soup
		EdisonUrl = request.urlopen(Url)
		SoupSource = EdisonUrl.read()
		Soup = bs(SoupSource, 'lxml')

		#Tag todays weekday and its courses
		DayTag=Soup.find("div",{'id':Day})
		Course=[]
		Course.append(DayTag.find("tr"))
		Course.append(Course[0].findNext("tr"))
		Course.append(Course[1].findNext("tr"))

		for c in Course:
			CourseDescription.append(c.find("td", {'class': 'course_description'}).getText())
			CourseType.append(c.find("td", {'class': 'course_type'}).getText())
			Place.append(1)
		list(filter(None,CourseDescription))
		list(filter(None,CourseType))
		list(filter(None,Place))
		return (CourseDescription,CourseType,Place)
	except Exception as e:
		CourseDescription=[str(e)]
		CourseType=['Error'] #Error course type
		Place=[1]
		return (CourseDescription,CourseType,Place)

def GetBryggan(Weekday,Url):
	try:
		#CAFÉ BRYGGAN
		CourseDescription=[]
		CourseType=[]
		Place=[]
		#Get soup
		BrygganUrl = request.urlopen(Url)
		SoupSourceB = BrygganUrl.read()
		SoupB = bs(SoupSourceB, 'lxml')
		#Tag start of week menu
		BrygganTag=SoupB.find('img',{'class':'alignnone size-full wp-image-413'})
		BrygganTemp=[]
		BrygganTemp.append(BrygganTag.findNext('p')) #Disregarded <p>
		BrygganTemp.append(BrygganTemp[0].findNext('p')) #Disregarded <p>
		BrygganP=[]
		BrygganP.append(BrygganTemp[1].findNext('p')) #Monday <p>
		#Now we do 2*(Weekday+1) p-tag steps to get the course of the day
		for i in range(0,Weekday*3+3):
			BrygganP.append(BrygganP[i].findNext('p'))
		CourseDescription.append(BrygganP[Weekday*3+1].getText().replace(u'\xa0', u' ').split(': ')[1])
		CourseDescription.append(BrygganP[Weekday*3+2].getText().replace(u'\xa0', u' ').split(': ')[1])
		CourseType.append(BrygganP[Weekday*3+1].getText().replace(u'\xa0', u' ').split(': ')[0])
		CourseType.append(BrygganP[Weekday*3+2].getText().replace(u'\xa0', u' ').split(': ')[0])
		Place.append(2)
		Place.append(2)
		list(filter(None,CourseDescription))
		list(filter(None,CourseType))
		list(filter(None,Place))
		return (CourseDescription,CourseType,Place)
	except Exception as e:
		CourseDescription=[str(e)]
		CourseType=['Error'] #Error course type
		Place=[2]
		return (CourseDescription,CourseType,Place)

def GetFinnInn(Weekday,Url):
	try:
		CourseDescription=[]
		CourseType=[]
		Place=[]
		#Get soup
		FinnInnUrl = request.urlopen(Url)
		SoupSourceF = FinnInnUrl.read()
		SoupF = bs(SoupSourceF, 'lxml')

		#Find the menus for all days <div class="item-description-menu">
		FinnInnTags=SoupF.find_all('div',{'class':'item-description-menu'},limit=5)
		#Todays courses as string
		FinnInnCourses=FinnInnTags[Weekday].getText()
		FinnInnCourses=FinnInnCourses.replace('\t','').replace('\r','').strip().splitlines()

		#Split course type and description, populate output list
		for c in range(len(FinnInnCourses)):
			if FinnInnCourses[c].count(':')>1: #Some poor typo protection
				FinnInnCourses[c]=FinnInnCourses[c].replace(':','',FinnInnCourses[c].count(':')-1)
			#Is there multiple courses with the same course type?
			if FinnInnCourses[c].count(':')<1:
				CourseDescription.append(FinnInnCourses[c].strip())
				CourseType.append(CourseType[c-1]) #Same course type as the previous
				Place.append(3)
			else:
				cSplit=FinnInnCourses[c].split(':')
				CourseDescription.append(cSplit[1].strip())
				CourseType.append(cSplit[0].strip())
				Place.append(3)
		list(filter(None,CourseDescription))
		list(filter(None,CourseType))
		list(filter(None,Place))
		return (CourseDescription,CourseType,Place)
	except Exception as e:
		CourseDescription=[str(e)]
		CourseType=['Error'] #Error course type
		Place=[3]
		return (CourseDescription,CourseType,Place)

def GetMop(Dag,Url):
	try:
		CourseDescription=[]
		CourseType=[]
		Place=[]
		#Get soup
		MopUrl = request.urlopen(Url)
		SoupSource = MopUrl.read()
		Soup = bs(SoupSource, 'lxml')
		
		#Tag the pretty weekdays and find todays tag
		DayTags=Soup.find_all("div", {'class':"pretty-day"})
		#FoodTags=Soup.find_all("div", {'class':"event-info text-center"})
		for d in DayTags: 
			if d.text.strip()==str(Dag).zfill(2): #Today
				Courses=d.find_parent().find_next_sibling('div',{"class":'event-info text-center'}).getText().strip().split('\n')
				for c in Courses:
					CourseDescription.append(c)
					CourseType.append("Dagens")
					Place.append(4)
				list(filter(None,CourseDescription))
				list(filter(None,CourseType))
				list(filter(None,Place))
				return (CourseDescription,CourseType,Place)
	except Exception as e:
		CourseDescription=[str(e)]
		CourseType=['Error'] #Error course type
		Place=[4]
		return (CourseDescription,CourseType,Place)