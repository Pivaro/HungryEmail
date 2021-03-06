# pylint: disable=invalid-name
"""[summary]

Returns:
    [type] -- [description]
"""

import calendar
import locale
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request

from bs4 import BeautifulSoup as bs

from HTMLcompile import HTMLcompile


def Hungry(FromAddress, ToAddressList, CcAddressList, BccAddressList, Login, Password, SmtpServer):
    """[summary]

    Arguments:
        FromAddress {[type]} -- [description]
        ToAddressList {[type]} -- [description]
        CcAddressList {[type]} -- [description]
        BccAddressList {[type]} -- [description]
        Login {[type]} -- [description]
        Password {[type]} -- [description]
        SmtpServer {[type]} -- [description]
    """
    # This function gets todays courses and send them as email

    # Where in time are we?
    Today = datetime.today()
    Week = Today.isocalendar()[1]
    Weekday = Today.weekday()  # Monday=0
    # Weekday=int(input("Please enter weekday [0-6]: ")) #For testing
    if Weekday < 5:  # Don't send email on week-ends
        # TIME
        Days = list(calendar.day_name)
        Day = Days[Weekday].lower()
        # Now we want the swedish day
        # locale.setlocale(locale.LC_TIME,"sv_SE.utf8") #Linux environment
        locale.setlocale(locale.LC_TIME, "sv-SV")  # Windows environment
        Dagar = list(calendar.day_name)
        Dag = Dagar[Weekday].lower()

        # OUTPUT VARIABLES
        CourseDescription = []
        CourseType = []
        Place = []

        # PLACE URLS
        PlaceUrl = []
        PlaceUrl.append('http://www.restaurangedison.se/lunch/')
        PlaceUrl.append('http://www.bryggancafe.se/veckans-lunch/')
        PlaceUrl.append('http://www.finninn.se/lunch-meny/')
        PlaceUrl.append('http://morotenopiskan.se/lunch/')

        # EDISON
        EdisonOut = GetEdison(Day, PlaceUrl[0])
        # print(str(EdisonOut))
        CourseDescription.extend(EdisonOut[0])
        CourseType.extend(EdisonOut[1])
        Place.extend(EdisonOut[2])

        # CAFÉ BRYGGAN
        BrygganOut = GetBryggan(Weekday, PlaceUrl[1])
        # print(str(BrygganOut))
        CourseDescription.extend(BrygganOut[0])
        CourseType.extend(BrygganOut[1])
        Place.extend(BrygganOut[2])

        # FINN INN
        FinnInnOut = GetFinnInn(Weekday, PlaceUrl[2])
        # print(str(FinnInnOut))
        CourseDescription.extend(FinnInnOut[0])
        CourseType.extend(FinnInnOut[1])
        Place.extend(FinnInnOut[2])

        # MOROTEN OCH PISKAN (Mop)
        # input todays calendar day
        MopOut = GetMop(datetime.today().day, PlaceUrl[3])
        # print(str(MopOut))
        CourseDescription.extend(MopOut[0])
        CourseType.extend(MopOut[1])
        Place.extend(MopOut[2])

        # PREPARE EMAIL
        # Text and HTML version
        # Edison
        MessageText = 'Edison\n'
        BodyHTML = '<p><h2><a href='+PlaceUrl[0]+'>Edison</a></h2>'
        for i in range(len(CourseDescription)):
            if Place[i] == 1:
                MessageText += '\n' + \
                    CourseType[i] + ': ' + CourseDescription[i]
                BodyHTML += '<b>' + \
                    CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
        # Café Bryggan
        MessageText += '\nCafé Bryggan'
        BodyHTML += '<h2><a href='+PlaceUrl[1]+'>Café Bryggan</a></h2>'
        for i in range(len(CourseDescription)):
            if Place[i] == 2:
                MessageText += '\n' + CourseType[i] + CourseDescription[i]
                BodyHTML += '<b>' + \
                    CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
        # Finn Inn
        MessageText += '\nFinn Inn'
        BodyHTML += '<h2><a href='+PlaceUrl[2]+'>Finn Inn</a></h2>'
        for i in range(len(CourseDescription)):
            if Place[i] == 3:
                MessageText += '\n' + CourseType[i] + CourseDescription[i]
                BodyHTML += '<b>' + \
                    CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'
        # Moroten och piskan
        MessageText += '\nMoroten och Piskan'
        BodyHTML += '<h2><a href='+PlaceUrl[3]+'>Moroten och Piskan</a></h2>'
        for i in range(len(CourseDescription)):
            if Place[i] == 4:
                MessageText += '\n' + CourseType[i] + CourseDescription[i]
                BodyHTML += '<b>' + \
                    CourseType[i] + ':</b> ' + CourseDescription[i] + '.<br>'

        # Contribute?!
        MessageText += '\n\nMedverka: https://github.com/Pivaro/HungryEmail'

        # HTML version
        BodyHTML += '</p>'
        MessageHtml = HTMLcompile(BodyHTML)

        # Compile and send email
        Subject = 'Dagens lunch ' + Dag + ' v. ' + str(Week)
        EmailPart1 = MIMEText(MessageText, 'plain')
        EmailPart2 = MIMEText(MessageHtml, 'html')

        MM = MIMEMultipart('alternative')
        MM['Subject'] = Subject
        MM['From'] = FromAddress
        MM['To'] = ", ".join(ToAddressList)
        MM['Cc'] = ", ".join(CcAddressList)  # Bcc shouldn't be here
        SendMailTo = ToAddressList + CcAddressList + BccAddressList

        MM.attach(EmailPart1)
        MM.attach(EmailPart2)

        Server = smtplib.SMTP(SmtpServer)
        Server.starttls()
        Server.login(Login, Password)
        Problems = Server.sendmail(FromAddress, SendMailTo, MM.as_string())
        Server.quit()
        print(Problems)


def GetEdison(Day, Url):
    """[summary]

    Arguments:
        Day {[type]} -- [description]
        Url {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    try:
        CourseDescription = []
        CourseType = []
        Place = []
        # Get soup
        EdisonUrl = request.urlopen(Url)
        SoupSource = EdisonUrl.read()
        Soup = bs(SoupSource, 'lxml')

        # Tag todays weekday and its courses
        DayTag = Soup.find("div", {'id': Day})
        Course = []
        Course.append(DayTag.find("tr"))
        Course.append(Course[0].findNext("tr"))
        Course.append(Course[1].findNext("tr"))

        for c in Course:
            CourseDescription.append(
                c.find("td", {'class': 'course_description'}).getText())
            CourseType.append(c.find("td", {'class': 'course_type'}).getText())
            Place.append(1)
        list(filter(None, CourseDescription))
        list(filter(None, CourseType))
        list(filter(None, Place))
        return (CourseDescription, CourseType, Place)
    except Exception as e:
        CourseDescription = [str(e)]
        CourseType = ['Error']  # Error course type
        Place = [1]
        return (CourseDescription, CourseType, Place)


def GetBryggan(Weekday, Url):
    """[summary]

    Arguments:
        Weekday {[type]} -- [description]
        Url {[type]} -- [description]
    """
    try:
        # CAFÉ BRYGGAN
        CourseDescription = []
        CourseType = []
        Place = []
        # Get soup
        BrygganUrl = request.urlopen(Url)
        SoupSourceB = BrygganUrl.read()
        SoupB = bs(SoupSourceB, 'lxml')
        # Tag start of week menu
        BrygganTag = SoupB.find(
            'img', {'class': 'alignnone size-full wp-image-413'})
        BrygganTemp = []
        BrygganTemp.append(BrygganTag.findNext('p'))  # Disregarded <p>
        BrygganTemp.append(BrygganTemp[0].findNext('p'))  # Disregarded <p>
        BrygganP = []
        BrygganP.append(BrygganTemp[1].findNext('p'))  # Monday <p>
        # Now we do 3*Weekday+1 (or +2) p-tag steps to get the course of the day
        for i in range(0, Weekday*3+3):
            BrygganP.append(BrygganP[i].findNext('p'))
        CourseDescription.append(
            BrygganP[Weekday*3+1].getText().replace(u'\xa0', u' ').split(': ')[1])
        CourseDescription.append(
            BrygganP[Weekday*3+2].getText().replace(u'\xa0', u' ').split(': ')[1])
        CourseType.append(
            BrygganP[Weekday*3+1].getText().replace(u'\xa0', u' ').split(': ')[0])
        CourseType.append(
            BrygganP[Weekday*3+2].getText().replace(u'\xa0', u' ').split(': ')[0])
        Place.append(2)
        Place.append(2)
        list(filter(None, CourseDescription))
        list(filter(None, CourseType))
        list(filter(None, Place))
        return (CourseDescription, CourseType, Place)
    except Exception as e:
        CourseDescription = [str(e)]
        CourseType = ['Error']  # Error course type
        Place = [2]
        return (CourseDescription, CourseType, Place)


def GetFinnInn(Weekday, Url):
    """[summary]

    Arguments:
        Weekday {[type]} -- [description]
        Url {[type]} -- [description]
    """
    try:
        CourseDescription = []
        CourseType = []
        Place = []
        # Get soup
        FinnInnUrl = request.urlopen(Url)
        SoupSourceF = FinnInnUrl.read()
        SoupF = bs(SoupSourceF, 'lxml')

        # Find the menus for all days <div class="item-description-menu">
        FinnInnTags = SoupF.find_all(
            'div', {'class': 'item-description-menu'}, limit=5)
        # Todays courses as string
        FinnInnCourses = FinnInnTags[Weekday].getText()
        FinnInnCourses = FinnInnCourses.replace(
            '\t', '').replace('\r', '').strip().splitlines()

        # Split course type and description, populate output list
        for c in range(len(FinnInnCourses)):
            if FinnInnCourses[c].count(':') > 1:  # Some poor typo protection
                FinnInnCourses[c] = FinnInnCourses[c].replace(
                    ':', '', FinnInnCourses[c].count(':')-1)
            # Is there multiple courses with the same course type?
            if FinnInnCourses[c].count(':') < 1:
                CourseDescription.append(FinnInnCourses[c].strip())
                # Same course type as the previous
                CourseType.append(CourseType[c-1])
                Place.append(3)
            else:
                cSplit = FinnInnCourses[c].split(':')
                CourseDescription.append(cSplit[1].strip())
                CourseType.append(cSplit[0].strip())
                Place.append(3)
        list(filter(None, CourseDescription))
        list(filter(None, CourseType))
        list(filter(None, Place))
        return (CourseDescription, CourseType, Place)
    except Exception as e:
        CourseDescription = [str(e)]
        CourseType = ['Error']  # Error course type
        Place = [3]
        return (CourseDescription, CourseType, Place)


def GetMop(Dag, Url):
    """[summary]

    Arguments:
        Dag {[type]} -- [description]
        Url {[type]} -- [description]
    """
    try:
        CourseDescription = []
        CourseType = []
        Place = []
        # Get soup
        MopUrl = request.urlopen(Url)
        SoupSource = MopUrl.read()
        Soup = bs(SoupSource, 'lxml')

        # Tag the pretty weekdays and find todays tag
        DayTags = Soup.find_all("div", {'class': "pretty-day"})
        # FoodTags=Soup.find_all("div", {'class':"event-info text-center"})
        for d in DayTags:
            if d.text.strip() == str(Dag).zfill(2):  # Today
                Courses = d.find_parent().find_next_sibling(
                    'div', {"class": 'event-info text-center'}).getText().strip().split('\n')
                for c in Courses:
                    CourseDescription.append(c)
                    CourseType.append("Dagens")
                    Place.append(4)
                list(filter(None, CourseDescription))
                list(filter(None, CourseType))
                list(filter(None, Place))
                return (CourseDescription, CourseType, Place)
        # Well, if the day is not there it's probably close.
        CourseDescription = ["Det är kanske stängt"]
        CourseType = ['Stängt']  # Error course type
        Place = [4]
        return (CourseDescription, CourseType, Place)
    except Exception as e:
        CourseDescription = [str(e)]
        CourseType = ['Error']  # Error course type
        Place = [4]
        return (CourseDescription, CourseType, Place)
