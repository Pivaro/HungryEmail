# pylint: disable=invalid-name
"""Defines email settings and calls Hungry.Hungry
"""
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
