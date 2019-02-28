"""Defines email settings and calls Hungry.Hungry
"""
# pylint: disable=C0103
from Hungry import Hungry

# EMAIL SETTINGS
FromAddress = '?@gmail.com'
ToAddressList = ['?@?.?']
CcAddressList = []
BccAddressList = []
Login = '?@gmail.com'
Password = '???'
SmtpServer = 'smtp.gmail.com:587'

Hungry(FromAddress, ToAddressList, CcAddressList,
       BccAddressList, Login, Password, SmtpServer)
