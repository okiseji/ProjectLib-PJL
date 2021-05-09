# -*- coding: UTF-8 -*-
# 本库用于网页相关功能
from selenium import webdriver
import time
import json
import endecode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from dingtalkchatbot.chatbot import DingtalkChatbot
login_url="https://icas.jnu.edu.cn/cas/login"
transition_url="https://info.jnu.edu.cn/"
target_url="https://libsouthic.jnu.edu.cn/ic?id=3"
list_url="https://libsouthic.jnu.edu.cn/user/myreservelist"
webhook="https://oapi.dingtalk.com/robot/send?access_token=dff6b9d4cc3206bcd27535568008bb4a113a425a71c8d5be64a68ea6b0aee06e"
memberlist = ["王彬丞", "姚景龙", "温键伟", "刘海鑫", "李澍晖", "陈怡菲"]
# 登录网页
def passwordlogin(name,driver):
    stuid=endecode.stuinfo(name)["stuid"]
    password = endecode.decode(name)
    driver.get(login_url)
    driver.execute_script('$("#captcha").hide()')
    time.sleep(1.0)
    driver.execute_script("""$("input[name='NECaptchaValidate']").val("aaa")""")
    time.sleep(1.0)
    driver.find_element_by_xpath('//*[@id="un"]').send_keys(stuid)
    driver.find_element_by_xpath('//*[@id="pd"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="index_login_btn"]/input').click()
# 刷新某人预约
def refresh(name):
    driver = webdriver.Chrome()
    try:
        passwordlogin(name, driver)
        driver.get(list_url)
        driver.find_element_by_link_text("[成员管理]").click()
        driver.find_element_by_xpath('//*[@id="delete"]').click()
        driver.find_element_by_xpath('//*[@id="yui-gen0-button"]').click()
        stuid = endecode.stuinfo("王彬丞")["stuid"]
        cardno = endecode.stuinfo("王彬丞")["card"]
        time.sleep(1.0)
        driver.find_element_by_xpath('//*[@id="userid"]').send_keys(stuid)
        driver.find_element_by_xpath('//*[@id="username"]').send_keys("王彬丞")
        driver.find_element_by_xpath('//*[@id="cardno"]').send_keys(cardno)
        driver.find_element_by_xpath('//*[@id="joinform"]/div[5]/div/button').click()
        print("成功刷新")
        driver.close()
        return "success"
    except:
        driver.close()
        print("刷新失败")
        return "failure"
# 取消某人预约
def cancel(name):
    driver = webdriver.Chrome()
    try:
        passwordlogin(name,driver)
        driver.get(list_url)
        driver.find_element_by_link_text("[取消预约]").click()
        driver.find_element_by_xpath('//*[@id="yui-gen0-button"]').click()
        driver.close()
        print("成功取消")
        delete(name)
        return "success"
    except:
        driver.close()
        print("取消失败")
        return "failure"
# 检查某人预约情况
def check(name):
    driver = webdriver.Chrome()
    try:
        passwordlogin(name,driver)
        driver.get(list_url)
        infos=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/table/tbody/tr[1]').text
        info=infos[:75]
        print("成功确认 "+name+" "+info)
        driver.close()
        return info
    except:
        driver.close()
        print(name+" 确认失败")
        return "嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐嘉然向晚贝拉乃琳珈乐"
# 制造预约链接
def linkcreate(room,month,day,hour):
    "https://libsouthic.jnu.edu.cn/user/reserve/173/1615209192040/16"
    # only for 2021
    tss1 = "2021-"+month+"-"+day+" "+hour+":13:12"
    time1= time.mktime(time.strptime(tss1, "%Y-%m-%d %H:%M:%S"))
    link="https://libsouthic.jnu.edu.cn/user/reserve/"+str(int(room)-511+173)+"/"+str(time1)[:-2]+"040/"+hour
    return link
# 预约房间
# 有bug
def reserve(usr,room,month,day,hour,length,memberlist):
    driver = webdriver.Chrome()
    try:
        passwordlogin(usr,driver)
        link=linkcreate(room,month,day,hour)
        driver.get(link)
        # only for 2021
        endtime = "2021-" + month + "-" + day + " "+str(int(hour)+int(length))+":0:0"
        driver.find_element_by_xpath('//*[@id="enddate"]').send_keys(endtime)
        driver.find_element_by_xpath('//*[@id="submit_0"]').click()
        WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.LINK_TEXT, '[成员管理]')))
        driver.find_element_by_link_text('[成员管理]').click()
        for member in memberlist:
            stuid = endecode.stuinfo(member)["stuid"]
            cardno = endecode.stuinfo(member)["card"]
            time.sleep(1.0)
            driver.find_element_by_xpath('//*[@id="userid"]').send_keys(stuid)
            driver.find_element_by_xpath('//*[@id="username"]').send_keys(member)
            driver.find_element_by_xpath('//*[@id="cardno"]').send_keys(cardno)
            driver.find_element_by_xpath('//*[@id="joinform"]/div[5]/div/button').click()
        print("成功预约")
        add(usr,room,month,day,hour,str(int(hour)+int(length)))
        driver.close()
        return "success"
    except:
        driver.close()
        print("预约失败")
        return "failure"
def checknetwork():
    f=0
    try:
        driver=webdriver.Chrome()
        driver.get(target_url)
        driver.close()
    except:
        f+=10
    try:
        requests.get(target_url,timeout=10)
    except:
        f+=5
    if f==0:
        print("一切运作良好")
        return "一切运作良好"
    if f==5:
        sendwarring()
        print("校园网桥接出现问题")
        return "校园网桥接出现问题"
    if f==10:
        sendwarring()
        print("webdriver存在问题")
        return "webdriver存在问题"
    if f==15:
        sendwarring()
        print("都tm有问题")
        return "服务器remake吧"
def save():
    list = endecode.getnamelist()
    reservelist={}
    for member in list:
        str=check(member)
        room = str[11:14]
        month = str[40:42]
        day = str[43:45]
        starttime = str[46:48]
        endtime = str[66:68]
        reservelist[member] = []
        reservelist[member].append(room)
        reservelist[member].append(month)
        reservelist[member].append(day)
        reservelist[member].append(starttime)
        reservelist[member].append(endtime)
    print(reservelist)
    with open(endecode.path+"reservetext.json",'w') as f:
        f.truncate(0)
        js=json.dumps(reservelist,ensure_ascii=False)
        f.write(js)
def delete(name):
    with open(endecode.path+"reservetext.json",'r') as f:
        reservelist = json.load(f)
        for member in reservelist.keys():
            if member == name:
                reservelist.pop(member)
    with open(endecode.path+"reservetext.json",'w') as f:
        f.truncate(0)
        js=json.dumps(reservelist,ensure_ascii=False)
        f.write(js)
def add(name,room,month,day,starthour,endhour):
    with open(endecode.path + "reservetext.json", 'r') as f:
        reservelist = json.load(f)
        reservelist[name]=[room,month,day,starthour,endhour]
    with open(endecode.path + "reservetext.json", 'w') as f:
        f.truncate(0)
        js = json.dumps(reservelist, ensure_ascii=False)
        f.write(js)
def sendwarring():
    libbot = DingtalkChatbot(webhook)
    libbot.send_text(msg="botmessage : 网络或selenium出问题了", is_at_all=False)
save()



