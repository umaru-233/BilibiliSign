# -*- coding: utf8 -*-
import sys
import json
import time
from typing import Dict
import requests
import os
from pathlib import Path
NowTime = str("["+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"]")
print(NowTime+"[INFO]哔哩哔哩直播签到脚本")
print(NowTime+"[INFO]开发者：umaru-233,项目地址：https://github.com/umaru-233/BilibiliSign")
print(NowTime+"[INFO]正在读取配置文件...")
#判断配置文件是否存在
ConfingPathAlive = os.path.exists("config.ini")
if ConfingPathAlive == False:
   print(NowTime+"[ERR]Config不存在！请在main.py同级创建config.ini配置文件。")
   print(NowTime+"[INFO]因为没有找到配置文件，程序结束。")
   sys.exit(0)
#读取配置文件，生成字典
with open('config.ini','r') as file:
    l=file.readlines() 
    Dict={}
    for i in l:
        s=i.replace('\n','') 
        s0=s.split(sep='=') 
        if '"' in s0[1]:
            s0[1]=s0[1].replace('"','') 
        else:
            s0[1]=str(s0[1]) 
        Dict[s0[0]]=s0[1] 
#变量从字典里取值
sessdata = str(Dict['sessdata'])
pushtoken = str(Dict['pushtoken'])
#登录及签到逻辑
print(NowTime+"[INFO]读取配置文件成功。")
def main_handler(event, context):
    pushplusURL = "https://www.pushplus.plus/"
    print(NowTime+"[INFO]正在获取Cookie为"+sessdata+"的用户信息")
    GetUserInfo = json.loads(requests.get("https://api.bilibili.com/x/web-interface/nav", cookies={"SESSDATA":sessdata}).text)
    if GetUserInfo["data"]["isLogin"] == False:
        print(NowTime+"[ERR]登录失败")
        print(NowTime+"[INFO]因为登录失败，程序结束。请检查Cookie是否正确。")
        return("Login Failed")
    UserName = GetUserInfo["data"]["uname"]
    UID = str(GetUserInfo["data"]["mid"])
    UserInfo = ("用户名："+UserName+"，UID:"+UID)
    print(NowTime+"[INFO]获取成功，"+UserInfo)
    print(NowTime+"[INFO]正在签到...")
    sign = requests.get("https://api.live.bilibili.com/sign/doSign", cookies={"SESSDATA":sessdata})
    sign_info = json.loads(sign.text)
    if sign_info["code"] == 0:
        print(NowTime+"[INFO]今日收获: "+sign_info["data"]["text"])
        print(NowTime+"[INFO]"+sign_info["data"]["specialText"])
        SucceedTitle = UserName+" B站签到成功"
        SucceedContent = ("签到成功！今日收获"+sign_info["data"]["text"])
        SucceedURL = pushplusURL+"send?token="+pushtoken+"&&title="+SucceedTitle+"&content="+SucceedContent
        requests.get(SucceedURL)
    else:
        FailedTitle = UserName+" B站签到失败"
        FailedContent = "错误原因是："+sign_info["message"]
        FailedLog = "[WARN]"+"签到失败！"+FailedContent
        print(NowTime+FailedLog)
        FailedURL = pushplusURL+"send?token="+pushtoken+"&&title="+FailedTitle+"&content="+FailedContent
        print(NowTime+"[INFO]正在推送结果至PlshPlus，token为"+pushtoken)
        requests.get(FailedURL)
        print(NowTime+"[INFO]推送完毕，程序正在退出")
        return "Sign Failed"
    return("Finish")



main_handler("", "")