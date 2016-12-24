WAYTOSMS_LOGIN_DATA_FORMAT = 'username={}&password={}&Submit=Sign+in'
WAYTOSMS_LOGIN_URL = "http://site24.way2sms.com/Login1.action?"
WAYTOSMS_SEND_SMS_URL = 'http://site24.way2sms.com/smstoss.action?'
WAYTOSMS_SEND_SMS_FORMAT = 'ssaction=ss&Token={}&mobile={}&message={}&msgLen=136'
WAYTOSMS_USERAGENT_HEADER = ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')
WAYTOSMS_REFERER_HEADER_FORMAT = 'http://site25.way2sms.com/sendSMS?Token={}'
FORGOT_PASSWORD_OTP_FORMAT = "OTP for forgot password is {}. Please don't share OTP with others.\n Happy tailoring !!!"

OTP_INFO_KEYS = {
    'forgot_password': 'forgot_pass'
}

POSTGRES_JSON_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

