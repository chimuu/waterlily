from urllib import request
from http import cookiejar

import logging


from account.constants import WAYTOSMS_SEND_SMS_URL, WAYTOSMS_SEND_SMS_FORMAT, \
    WAYTOSMS_LOGIN_DATA_FORMAT, WAYTOSMS_USERAGENT_HEADER, WAYTOSMS_REFERER_HEADER_FORMAT, WAYTOSMS_LOGIN_URL


logger = logging.getLogger('main')


class WayToSMSHelper:

    def __init__(self, username, password):
        # logging into the sms site
        login_data = WAYTOSMS_LOGIN_DATA_FORMAT.format(username, password).encode('utf-8')

        # For cookies
        cj = cookiejar.CookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(cj))

        # Adding header details
        self.opener.addheaders = [WAYTOSMS_USERAGENT_HEADER]
        try:
            self.opener.open(WAYTOSMS_LOGIN_URL, login_data)
        except IOError:
            logger.error("IOError while login to waytsms")
            return
        self.session_id = str(cj).split('~')[1].split(' ')[0]
        self.opener.addheaders = [('Referer', WAYTOSMS_REFERER_HEADER_FORMAT.format(self.session_id))]

        logger.info("success! logged into waytosms")

    def send_sms(self, number, message):
        message = "+".join(message.split(' '))
        send_sms_data = WAYTOSMS_SEND_SMS_FORMAT.format(self.session_id, number, message).encode('utf-8')
        try:
            self.opener.open(WAYTOSMS_SEND_SMS_URL, send_sms_data)
        except IOError:
            logger.error("IOError while sending sms using waytsms")
