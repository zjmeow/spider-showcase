import requests
import json


def get_pic_captcha(phone):
    url = 'https://h5.ele.me/restapi/eus/v3/captchas'
    data = {'captcha_str': phone}
    resp = requests.post(url, data=data).text
    print(resp)
    js = json.loads(resp)
    print(js['captcha_image'])
    return js['captcha_hash']


def get_phone_captcha(phone, captcha_hash):
    captcha = input('请输入图形验证码')
    data = {"mobile": phone, "captcha_value": captcha, "captcha_hash": captcha_hash}
    url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    resp = requests.post(url, data=data).text
    print(resp)
    return json.loads(resp)['validate_token']


# 登录返回 cookie

def login(phone, token):
    validate_code = input('请输入手机验证码')
    data = {"mobile": "13101411911", "validate_code": validate_code, "validate_token": token}
    url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
    resp = requests.post(url, data=data)
    print(resp.text)
    return resp.cookies.get_dict()


def get_cookie(phone):
    hash = get_pic_captcha(phone)
    token = get_phone_captcha(phone, hash)
    return login(phone, token)


def get_item():
    cookie = get_cookie('13101411911')
    print(cookie)
    url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&latitude=26.065879&limit=24&longitude=119.167706&offset=48&terminal=web'
    resp = requests.get(url, cookies=cookie).text
    print(resp)


# get_item()
get_item()
