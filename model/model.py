from datetime import datetime
import json
import random

from model.api_line import getProfileFromAccessToken
from model.google_mail import sendLineWebOptMail


""" 
{
    {{ userId }}:{
        'accessToken': string,
        'checkFlag': boolean,
        'email': string,
        'otp': string
    },
    .
    .
    .
}
"""
db_data = {}

CHECK_PROFILE_ERROR_MSG = '登入過期或尚未驗證，請重新登入'
OTP_TIMEOUT = 60


def getLineProfile(body):
    """ 個人身分驗證 """
    json_dict = json.loads(body)
    print(json_dict)

    re_json = getProfileFromAccessToken(json_dict['accessToken'])

    if re_json['userId'] in db_data.keys():
        user_value = db_data[re_json['userId']]
        if 'checkFlag' in user_value.keys():
            re_json['checkFlag'] = user_value['checkFlag']
    else:
        db_data[re_json['userId']] = {
            'checkFlag': False
        }
        re_json['checkFlag'] = False

    db_data[re_json['userId']]['accessToken'] = json_dict['accessToken']

    print(db_data[re_json['userId']])

    print(re_json)
    return json.dumps(re_json)


def checkAccount(body):
    """ 登入身分證、密碼確認，預設A123456789、123456 """
    json_dict = json.loads(body)
    userId = json_dict['userId']
    if not checkProfile(json_dict['userId'], json_dict['accessToken']):
        return {'checkAccountFlag': False, 'msg': CHECK_PROFILE_ERROR_MSG}
    if json_dict['account'] == 'A123456789' and json_dict['password'] == json_dict['account']:
        db_data[userId]['account'] = json_dict['account']
        # db_data['account'] = json_dict['account']
        # db_data['password'] = json_dict['password']
        return {'checkAccountFlag': True, 'msg': '登入成功'}
    else:
        return {'checkAccountFlag': False, 'msg': '帳號或密碼錯誤'}


def checkRegister(body):
    """ 註冊確認 """
    json_dict = json.loads(body)
    userId = json_dict['userId']
    if not checkProfile(json_dict['userId'], json_dict['accessToken']):
        return {'checkRegisterFlag': False, 'msg': CHECK_PROFILE_ERROR_MSG}
    if not json_dict['identity'] == db_data[userId]['account']:
        return {'checkRegisterFlag': False, 'msg': '帳號與身分證不相同'}
    # if json_dict['帳號'] == 'A123456789' and json_dict['密碼'] == '123456':
    # db_data[userId]['account'] = json_dict['account']
    db_data[userId]['password'] = json_dict['password']
    email = json_dict['email']
    db_data[userId]['email'] = email

    otp = getOtpValue()
    print('otp: %s' % otp)
    db_data[userId]['otp'] = otp
    db_data[userId]['otp_date'] = datetime.now()
    sendLineWebOptMail(email, 'OTP: %s' % otp)
    db_data[userId]['checkRegisterFlag'] = True
    return {'checkRegisterFlag': True, 'msg': '註冊成功', 'otpTimeout': OTP_TIMEOUT}
    # else:
    # return {'checkRegisterFlag': False}


def checkOtp(body):
    """ otp確認 """
    json_dict = json.loads(body)
    userId = json_dict['userId']
    if not checkProfile(json_dict['userId'], json_dict['accessToken']):
        return {'checkOtpFlag': False, 'msg': CHECK_PROFILE_ERROR_MSG}
    
    now = datetime.now()
    dif = now - db_data[userId]['otp_date']
    if dif.seconds > OTP_TIMEOUT:
        return {'checkOtpFlag': False, 'msg': 'OTP逾時，請重新發送驗證碼'}

    if json_dict['otp'] == db_data[userId]['otp']:
        
        db_data[userId]['checkFlag'] = True
        db_data[userId]['checkOtpFlag'] = True
        return {'checkOtpFlag': True, 'msg': 'OTP驗證成功'}
    else:
        return {'checkOtpFlag': False, 'msg': 'OTP驗證失敗'}


def checkProfile(userId, accessToken):
    """ 確認已獲取userId、accessToken，且為同一次登入使用 """
    if userId in db_data.keys():
        user_data = db_data[userId]
        if user_data['accessToken'] == accessToken:
            return True
    return False


def getOtpValue():
    """ 獲取隨機6位數號碼 """
    return str(random.randint(1, 999999)).zfill(6)
