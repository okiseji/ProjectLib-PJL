# -*- coding: UTF-8 -*-
# 本库用于数据库管理
import os
import json
import random
import shutil
path='./database/'
dir_path='./database/info/'
target_path='./database/waitlist/'
# 加密并存入数据库
def getnamelist():
    namelist=[]
    for file in os.listdir(dir_path):
        with open(dir_path+file,'r') as f:
            stu=json.load(f)
            name=stu["usrinfo"]["name"]
            namelist.append(name)
    print(namelist)
    return namelist
def encode(name,stuid,psw,card_num):
    with open(dir_path +stuid+".json",'w') as f:
        words = ''
        wordso = ''
        for word in psw:
            wordso += str(ord(word))
            words += str(ord(word) - 23)
            wordnum = int(words)
            tag = random.randint(10, 99)
        password = str(wordnum * tag) + str(tag)
        jsessionid="xxx"
        js = json.dumps({"cookie": {"JSESSIONID": jsessionid},"usrinfo": {"name": name, "card": card_num, "stuid": stuid, "password": password}},ensure_ascii=False)
        f.write(js)
# 解密用户密码
def decode(name):
    password=int(stuinfo(name)["password"])
    tag = str(password)[-2:]
    code = str(int(str(password)[:-2])//int(tag))
    psw = ''
    for i in range(0, len(code), 2):
        psw += chr(int(str(code)[i:i + 2]) + 23)
    return psw
# 获取用户信息
def stuinfo(name):
    for file_name in os.listdir(dir_path):
        with open(dir_path + file_name, 'r') as f:
            stu = json.load(f)
            if stu["usrinfo"]["name"] == name:
                stuinfo = stu["usrinfo"]
    return stuinfo
def leavepool(name):
    stuid=stuinfo(name)["stuid"]
    shutil.move(dir_path +stuid+".json",target_path +stuid+".json")
def backpool(name):
    stuid = stuinfo(name)["stuid"]
    shutil.move( target_path + stuid + ".json",dir_path + stuid + ".json")
