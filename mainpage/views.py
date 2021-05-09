# -*- coding:utf-8 -*-
from django.shortcuts import render
from datetime import datetime
import json
import reserve
import endecode
from django.http import HttpResponse
from django.template import Template ,context as tc
# 交互代码
# def msgproc(request):
#     datalist=[]
#     if request.method=="POST":
#         userA =request.POST.get("userA",None)
#         userB =request.POST.get("userB",None)
#         msg=request.POST.get("msg",None)
#         time=datetime.now()
#         with open('msgdata.txt','a+') as f:
#             f.write("{}--{}--{}--{}--\n".format(userA,userB,msg,time.strftime("%Y-%m-%d %H:%M:%S")))
#     if request.method == "GET":
#         userC= request.GET.get("userC",None)
#         if userC != None:
#             with open("msgdata.txt","r") as f:
#                 cnt=0
#                 for line in f:
#                     linedata = line.split('--')
#                     # if linedata[0]==userC:
#                     cnt+=1
#                     d = {"userA": line, "msg": line, "time": line}
#                     datalist.append(d)
#                     # if cnt >= 10:
#                     #     break
#     return render(request, "mainpage.html", {"data": datalist})
# data:{{1},{2},{3}}
# a={"data":{"network":"ok|error","reserveinfo":{"1":{"date":"512-04-29-08","condition":"allow|disallow|name"}}}}
def operate(request):
    info=[]
    if request.method=="POST":
        usr=request.POST.get("usr",None)
        room = request.POST.get("room", None)
        month = request.POST.get("month", None)
        day = request.POST.get("day", None)
        hour = request.POST.get("hour", None)
        length = request.POST.get("length", None)
        usrcancel = request.POST.get("usrcancel", None)
        usrrefresh = request.POST.get("usrrefresh", None)
        usrenter = request.POST.get("usrenter", None)
        stuid = request.POST.get("stuid", None)
        password = request.POST.get("password", None)
        cardno=request.POST.get("cardno", None)
        usrleave = request.POST.get("usrleave", None)
        usrback=request.POST.get("usrback", None)
        if usr!=None:
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            memberlist = ["王彬丞", "姚景龙", "温键伟", "刘海鑫", "李澍晖", "陈怡菲"]
            condition=reserve.reserve(usr,room,month,day,hour,length,memberlist)
            with open('log.json','a+') as f:
                js = json.dumps(
                    {"time":time,"usr":usr,"room":room,"month":month,"day":day,"hour":hour,"length":length,"condition":condition},ensure_ascii=False)
                f.write(js)
        if usrcancel!=None:
            condition = reserve.cancel(usrcancel)
            with open('log.json', 'a+') as f:
                js = json.dumps(
                    {"usrcancel": usrcancel, "condition": condition}, ensure_ascii=False)
                f.write(js)
        if usrrefresh!=None:
            condition = reserve.refresh(usrrefresh)
            with open('log.json', 'a+') as f:
                js = json.dumps(
                    {"usrrefresh": usrrefresh, "condition": condition}, ensure_ascii=False)
                f.write(js)
        if usrenter!=None:
            endecode.encode(usrenter,stuid,password,cardno)
        if usrleave!=None:
            endecode.leavepool(usrleave)
        if usrback!=None:
            endecode.backpool(usrback)
    return render(request, "mainpage3.html",None)
    # if request.method=="GET":
    #     usrcheck= request.GET.get("usrcheck", None)
    #     info[0]=reserve.check(usrcheck)
    # return render(request, "mainpage3.html", {"data":info})
def index(request):
    check=[]
    network=[]
    network.append(reserve.checknetwork())
    with open(endecode.path + "reservetext.json", 'r') as f:
        rlist = json.load(f)
    if request.method=="GET":
        usrcheck = request.GET.get("usrcheck", None)
        if usrcheck != None:
            info=reserve.check(usrcheck)
            check.append(info)
    with open("log.json", 'r') as f:
        rlist2 = f.read()
    return render(request,'oldtemplates/mainpage2.html',{"data":{"check":check,"network":network,"list":rlist,"list2":rlist2}})


