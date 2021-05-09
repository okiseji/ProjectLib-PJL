# -*- coding: UTF-8 -*-
# 本库用于服务器自动运行
import reserve
import datetime
import endecode
import json
import time
memberlist = ["王彬丞", "姚景龙", "温键伟", "刘海鑫", "李澍晖", "陈怡菲"]
def checktime():
    checktime={}
    checktime["month"]=time.strftime("%m")
    checktime["day"]=time.strftime("%d")
    checktime["weekday"]=time.strftime("%A")
    checktime["hour"] = time.strftime("%H")
    checktime["minute"] = time.strftime("%M")
    return checktime
def cycle():
    while 1:
        tm=checktime()
        print(tm)
        if tm["minute"]=="55" and  int(tm["hour"]) >= 7 and int(tm["hour"]) <= 22 :
            # try:
            roll(tm)
            # except:
            #     return "failure"
        time.sleep(60.0)
def roll(time):
    # 取消的清洗
    with open(endecode.path + "reservetext.json", 'r') as f:
        reservelist = json.load(f)
    for member in reservelist.keys():
        list = reservelist[member]
        if list[4]==str(int(time["hour"])+1) and list[1]==time["month"] and list[member][2]==time["day"]:
            reserve.cancel(member)
        if list[3]==str(int(time["hour"])+1) and list[1]==time["month"] and list[member][2]==time["day"]:
            reserve.refresh(member)
        if int(list[1]) < int(time["month"]) and int(list[member][2]) < int(time["day"]):
            reserve.delete(member)
        if int(list[4]) < int(time["hour"])+1 and int(list[1]) == int(time["month"]) and int(list[member][2]) == int(time["day"]):
            reserve.delete(member)
    # 新预约的清洗
    flag = 0
    notavlist = []
    allnamelist = endecode.getnamelist()
    with open(endecode.path + "reservetext.json", 'r') as f:
        reservelist2 = json.load(f)
        for member in reservelist2.keys():
            notavlist.append(member)
    for member2 in allnamelist:
        for member3 in notavlist:
            if member2 == member3:
                flag=1
                break
        if flag ==1:
            flag=0
            continue
        if flag ==0:
            nextreserve=createnext()
            room=nextreserve[0]
            month = nextreserve[1]
            day=nextreserve[2]
            hour = nextreserve[3]
            length=str(int(nextreserve[4])-int(nextreserve[3]))
            # check 是否可以预约!
            reserve.reserve(member2,room,month,day,hour,length,memberlist)
def createnext():
    timedict={}
    reslist1=[1,2,3,4,5]
    with open(endecode.path+"reservetext.json",'r') as f:
        reservelist=json.load(f)
        for member in reservelist.keys():
            list=reservelist[member]
            # print(list)
            timedict[member]=10000*int(list[1])+100*int(list[2])+int(list[3])
    passlist=sorted(timedict.items(), key=lambda d: d[1], reverse=True)
    lastmember=passlist[0][0]
    print(lastmember)
    #only 2021
    dt_string="2021"+" "+reservelist[lastmember][1]+" "+reservelist[lastmember][2]
    dt_no=datetime.datetime.strptime(dt_string,"%Y %m %d")
    # 房间预定函数
    room_str = reservelist[lastmember][0]
    endtime_str = reservelist[lastmember][4]
    if endtime_str== "22" or "21":
        month_str = (dt_no + datetime.timedelta(days=1)).strftime("%m")
        day_str = (dt_no + datetime.timedelta(days=1)).strftime("%d")
        weekday_str = (dt_no + datetime.timedelta(days=1)).strftime("%A")
        if weekday_str=="Monday" or weekday_str=="Tuesday":
            starttime_str="12"
            endtime_str="17"
        elif weekday_str == "Friday":
            month_str=(dt_no+datetime.timedelta(days=2)).strftime("%m")
            day_str = (dt_no + datetime.timedelta(days=2)).strftime("%d")
            starttime_str="08"
            endtime_str="13"
        else:
            starttime_str = "08"
            endtime_str = "13"
    else:
        month_str = dt_no.strftime("%m")
        day_str = dt_no.strftime("%d")
        if endtime_str=="18":
            starttime_str=endtime_str
            endtime_str=str(int(endtime_str)+4)
        else:
            starttime_str = endtime_str
            endtime_str=str(int(endtime_str)+5)
    reslist1[0]=room_str
    reslist1[1]=month_str
    reslist1[2]=day_str
    reslist1[3]=starttime_str
    reslist1[4]=endtime_str
    return reslist1

