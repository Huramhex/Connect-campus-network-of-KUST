'''
Author: Huramhex
Auto connect campus network of Kunming university of science and technology
Need Firefox browser
Download geckodriver firefox kernel
https://github.com/mozilla/geckodriver/releases
Put geckodriver.exe into .\Python39\Scripts
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from selenium.webdriver import Firefox, FirefoxOptions


username_str = "******" # 你的校园网登陆用户名
password_str = "******" # 你的校园网登陆密码

can_connect = True


def login():
    try:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get("http://222.197.192.59:9090/zportal/loginForWeb?wlanuserip=728887bb0994f03bb5fa6ef2487d0b59&wlanacname=7717b8c143d93e3a1fdcfa4aa07d37a9&ssid=bfd0fd2d574e31c6ba728e0a908cdb8f&nasip=1223114e4ff3cad74a2437106670b0eb&snmpagentip=&mac=14231e3ed6d9356c8b418e666b0b7a2e&t=wireless-v2&url=d4985c1eb88f0cfdb5825733b7731ab1291298f53526e958e8cae5e588442a033e8a214f8d4c299e447cf6fed598eba8&apmac=&nasid=7717b8c143d93e3a1fdcfa4aa07d37a9&vid=e8732bfaf26d2608&port=7c8a459801e925a5&nasportid=b8007b401a20ea61a02daa3f7cd048ada9b65f775e71710f14fc9d29b71fc4a3") # 校园网登陆地址
        # time.sleep(3)
        username_input = driver.find_element_by_id("user_name") # 校园网登陆用户名的输入控件ID
        password_input = driver.find_element_by_id("tx") # 校园网登陆密码的点击激活控件ID
        print('Searching connect')
        login_button = driver.find_element_by_id("login_submit") # 校园网登陆连接的点击控件ID
        print('Find connect successfully')
        username_input.send_keys(username_str)
        time.sleep(1)
        password_input.click()
        subpassword_input = driver.find_element_by_id("password") # 校园网登陆密码的输入控件ID
        subpassword_input.send_keys(password_str)
        print('Input user info')
        login_button.click()
        print('Connect')
    except:
        print(getCurrentTime(), u"登陆函数异常")

    driver.close()


#获取当前时间
def getCurrentTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))


#判断当前是否可以连网
def handler():
    try:
        global can_connect
        can_connect = False # 默认判断连接为失败状态
        # 需要设置timeout是因为断网时request会堵住程序, 设置timeout后最多等待10s，如果没有request成功, can_connect为False
        baidu_request=requests.get("http://www.baidu.com", timeout = 10)
        if(baidu_request.status_code==200):
            baidu_request.encoding = 'utf-8'
            baidu_request_bsObj = BeautifulSoup(baidu_request.text, 'html.parser')
            baidu_input = baidu_request_bsObj.find(value="百度一下")
            if baidu_input==None:
                return False
            can_connect = True # 只有可以request 到百度的网址，并且页面中含有“百度一下”这几个字符，才判断连接成功
            return True
        else:
            print('Offline')
            return False
    except:
        print ('error')
        return False


#主函数
def main():
    print (getCurrentTime(), u"昆明理工大学校园网自动登陆运行中......")
    while True:
        while True:
            start_time = time.time()
            handler()
            end_time = time.time()
            print(end_time - start_time)
            global can_connect
            # print(can_connect)
            if not can_connect:
                print (getCurrentTime(),u"网络断开连接！")
                try:
                    login()
                except:
                    print(getCurrentTime(), u"浏览器存在问题")
            else:
                print (getCurrentTime(), u"网络正常")
                time.sleep(30)
            time.sleep(10)
        time.sleep(10)


main()
