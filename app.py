from flask import request, jsonify, render_template
from flask import redirect
from flask import Flask, url_for
from scrapy.http import response

import sql
import pymysql
app = Flask(__name__)
# 登录注册模块
@app.route('/')
def hello_world():
    return render_template("login.html")
@app.route('/regis')
def regis():
    return render_template("regitser.html")
@app.route('/reset')
def reset():
    return render_template("resetpass.html")
# 登录注册模块
#主页面
@app.route('/show')
def hello_world_show():
    return render_template("show.html")

#查询部分
#详情页面（web）查询
@app.route('/movie_page')
def hello_world_movie_page():
    title=request.values.get("title")
    scorenum=request.values.get("scorenum")
    str_s=sql.find_by_title_and_scorenum(title,scorenum)
    #获取所有查询到的带星级电影库 腾讯、爱奇艺、IMDB、1905、搜狐
    str_three=sql.find_all_movies(title)

    return render_template("moviepage.html", title=str_s[0], star=str_s[1],
                           director=str_s[2], type_movie=str_s[3], area=str_s[4]
                           , date_time=str_s[5], summary=str_s[6], score=str_s[7]
                           , language_movie=str_s[8], img=str_s[9], scorenum=str_s[10]
                           , timelen=str_s[11], str_one=str_three[0], str_two=str_three[1]
                           , str_three=str_three[2], str_four=str_three[3], str_five=str_three[4])
#详情页面（app）查询
@app.route('/android_query')
def android_query():
    title = request.values.get("title")
    scorenum = request.values.get("scorenum")
    str_s = []
    str_s = sql.find_by_title_and_scorenum(title, scorenum)
    str_s_flag = []  # 将元组转为数组
    for i in str_s:
        str_s_flag.append(i)
    str_three = sql.find_all_movies(title)
    # 腾讯视频
    if (str_three[0] != ""):
        str_s_flag.append(str_three[0][1])
        str_s_flag.append(str_three[0][3])
        str_s_flag.append(str_three[0][2])
    else:
        str_s_flag.append("0")
        str_s_flag.append("0")
        str_s_flag.append("0")
    # 爱奇艺
    if (str_three[1] != ""):
        str_s_flag.append(str_three[1][1])
        str_s_flag.append(str_three[1][3])
        str_s_flag.append(str_three[1][2])
    else:
        str_s_flag.append("0")
        str_s_flag.append("0")
        str_s_flag.append("0")
    # 搜狐视频
    if (str_three[4] != ""):
        str_s_flag.append(str_three[2][1])
        str_s_flag.append(str_three[2][3])
        str_s_flag.append(str_three[2][2])
    else:
        str_s_flag.append("0")
        str_s_flag.append("0")
        str_s_flag.append("0")
    # 1905电影网
    if (str_three[3] != ""):
        str_s_flag.append(str_three[3][1])
        str_s_flag.append(str_three[3][3])
        str_s_flag.append(str_three[3][2])
    else:
        str_s_flag.append("0")
        str_s_flag.append("0")
        str_s_flag.append("0")
    print(str_s_flag)
    return jsonify({"data": str_s_flag})
#分类排序查询
@app.route('/query_tag')
def query_tag():
    str_s=[]
    str_s.append(request.values.get("type"))
    str_s.append(request.values.get("date"))
    str_s.append(request.values.get("area"))
    str_s.append(request.values.get("first"))
    str_s.append(request.values.get("num"))
    if (str_s[3] == "热门(正序)"):
        str_s[3]="hot_1"
    if (str_s[3] == "热门(倒序)"):
        str_s[3]="hot_0"
    if (str_s[3] == "评分(正序)"):
        str_s[3]="star_1"
    if (str_s[3] == "评分(倒序)"):
        str_s[3]="star_0"
    if (str_s[3] == "时间(正序)"):
        str_s[3]="time_1"
    if (str_s[3] == "时间(倒序)"):
        str_s[3]="time_0"
    if(str_s[0]=="全部"):
        str_s[0]=""
    if(str_s[1]=="全部"):
        str_s[1]=""
    if(str_s[2]=="全部"):
        str_s[2]=""
    if(str_s[0]==None):
        str_s[0]=""
    if(str_s[1]==None):
        str_s[1]=""
    if(str_s[2]==None):
        str_s[2]=""
    if(str_s[3]==None):
        str_s[3]=""
    print(str_s)
    data=[]
    for i in sql.find_class_order(str_s):
        data.append(i)
    return jsonify({"data": data})
#获取top
@app.route('/get_top')
def get_top():
    toplist=[]
    temptoplist=sql.get_top()
    dataRes=[]
    # print("这里是路由get_top")
    for item in temptoplist:
        dataRes.append({"topname":item[1],"topscore":item[8],"toptime":item[12],"toprank":item[0]})
    return jsonify({"data":dataRes})
#查询部分

#用户部分
#用户注册（app）
@app.route('/android_register')
def android_register():
    name = request.values.get("name")
    phone = request.values.get("phone")
    password = request.values.get("password")
    sql.android_register(name,phone,password)
    print("用户注册（app）成功")
    data=1
    return jsonify({"data": data})
#用户（app）查询
@app.route('/android_query_user')
def android_query_user():
    phone = request.values.get("phone")
    str_s=sql.android_query(phone);
    return jsonify({"data": str_s})
#用户（app）收藏添加
@app.route('/android_like')
def android_like():
    userphone = request.values.get("userphone")
    usermovie=request.values.get("usermovie")
    usertype=request.values.get("usertype")
    scorenum=request.values.get("scorenum")
    url=request.values.get("url")
    score=request.values.get("score")
    sql.android_like(userphone,usermovie,usertype,scorenum,url,score);
    print("收藏（app）成功")
    data=1
    return jsonify({"data": data})
#用户（app）收藏查询
@app.route('/android_like_query')
def android_like_query():
    userphone=request.values.get("userphone")
    usertype=request.values.get("usertype")
    data=sql.android_like_query(userphone,usertype)
    return jsonify({"data": data})
#用户（app）收藏删除
@app.route('/android_delete')
def android_delete():
    userphone = request.values.get("userphone")
    usertype = request.values.get("usertype")
    usermovie = request.values.get("usermovie")
    scorenum = request.values.get("scorenum")
    flag=sql.android_delete(userphone,usertype,usermovie,scorenum)
    return jsonify({"data": flag})
#用户（app）收藏转移
@app.route('/android_user_like_trans')
def android_user_like_trans():
    userphone = request.values.get("userphone")
    usertype = request.values.get("usertype")
    usermovie = request.values.get("usermovie")
    scorenum = request.values.get("scorenum")
    usertype_new = request.values.get("usertype_new")
    flag=sql.android_user_like_trans(userphone,usertype,usermovie,scorenum,usertype_new)
    return jsonify({"data": flag})
#用户部分
@app.route('/user_pager')
def user_pager():
    return render_template("usermain.html")
#用户部分
#网页登陆注册部分
@app.route('/web_register', methods=['GET', 'POST'])
def web_register():
    phoneNumber = request.form.get('phoneNumber')
    password =request.form.get('password')
    email = request.form.get('email')
    username = request.form.get('username')
    print("这是网页注册路由！")
    print(phoneNumber+" "+password+" "+email+" "+username)
    sql.web_register(phoneNumber,password,email,username)
    return redirect(url_for('hello_world_show'),code=302)
@app.route('/web_login/',methods=['GET', 'POST'])
def web_login():
    userphone = request.values.get('userphone')
    password=request.values.get('password')
    print("账号："+userphone+"   "+"密码："+password)
    res=sql.web_login(userphone,password)
    if(res==True):
        return jsonify({"data":1})
    else:
        return jsonify({"data":0})
#用户修改密码
@app.route('/resetpass',methods=['GET', 'POST'])
def resetpass():
    userphone=request.values.get('userphone')
    resetpass=request.values.get('resetpass')
    print("路由获得手机号："+userphone+"\n")
    print("路由获得新密码：" + resetpass + "\n")
    flag=sql.reset_pass(userphone,resetpass)
    if(flag==1):
        return jsonify({"data":1})
    else:
        return jsonify({"data":0})
if __name__ == '__main__':
    host="127.0.0.1"
    port=5000
    app.run(host,port)
