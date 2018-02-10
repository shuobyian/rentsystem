#-*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, request
import pymysql
import json
import sys

#from django.shortcuts import render
#from django.http import HttpResponse
#from .models import Candidate

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

conn = pymysql.connect(
        host='localhost',
        user='root',
        password='intI2017!@',
        db='intI',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

sql = 'select * from rent_log'
cursor.execute(sql)
objects = []
for data in cursor.fetchall():
    objects.append({
        "sequecne" : data['rent_sq']
    })

cursor.execute(sql)
dict = {}
dict["rent_sq"]=0
for data in cursor.fetchall():
    dict["rent_sq"] = data["rent_sq"]


jsonStr = json.dumps(dict, ensure_ascii=False).encode('utf8')
print type(jsonStr)

@app.route('/')
def hi(charset='utf-8'):
    sql2 = 'select * from rent_product'
    cursor.execute(sql2)
    products = []
    for data in cursor.fetchall():
        products.append({
            "rentnumber" : data['rent_num'],
            "product" : data['rent_name'],
            "possible" : data['rent_possible'],
            "productnumber" : data['pro_num'],
            "dueyear" : data['due_year'],
            "duemonth" : data['due_month'],
            "dueday" : data['due_day']
        })

    dict2 = {}
    for data in cursor.fetchall():
        dict2["rent_num"] = data["rent_num"]
        dict2["rent_name"] = data["rent_name"]
        dict2["rent_possible"] = data["rent_possible"]
        dict2["product_num"] = data["pro_num"]
        dict2["due_year"] = data["due_year"]
        dict2["due_month"] = data["due_month"]
        dict2["due_day"] = data["due_day"]

    jsonStr2 = json.dumps(dict2, ensure_ascii=False).encode('utf8')
    print type(jsonStr2)


    product_list=products#products라는 list넘김
    name=u'학생회 대여물품 목록'
    return render_template('rentList.html', name=name, product_list=product_list)

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/login/rent.html')
def Rent():
    return render_template('rent.html')

@app.route('/login/return.html')
def Return():
    return render_template('return.html')

@app.route('/login/dbassociationrentreturnsystem',methods=['POST'])
def db():
    sql = 'select * from rent_log'
    cursor.execute(sql)
    objects = []
    for data in cursor.fetchall():
        objects.append({
            "sequecne" : data['rent_sq'],
            "name" : data['rent_name'],
            "productnumber" : data['rent_num'],
            "studentnumber" : data['student_num'],
            "person" : data['rent_person'],
            "phonenumber" : data['phone_num'],
            "rentsa" : data['rent_sa'],
            "rentyear" : data['rent_year'],
            "rentmonth" : data['rent_month'],
            "rentday" : data['rent_day'],
            "returnsa" : data['return_sa'],
            "returnyear" : data['return_year'],
            "returnmonth" : data['return_month'],
            "returnday" : data['return_day'],
            "returnfine" : data['return_fine']
        })

    cursor.execute(sql)
    dict = {}
    dict["rent_sq"]=0
    for data in cursor.fetchall():
        dict["rent_sq"] = data["rent_sq"]
        dict["rent_name"] = data["rent_name"]
        dict["rent_num"] = data["rent_num"]
        dict["student_num"] = data["student_num"]
        dict["rent_person"] = data["rent_person"]
        dict["phone_num"] = data["phone_num"]
        dict["rent_sa"] = data["rent_sa"]
        dict["rent_year"] = data["rent_year"]
        dict["rent_month"] = data["rent_month"]
        dict["rent_day"] = data["rent_day"]
        dict["return_year"] = data["return_year"]
        dict["return_month"] = data["return_month"]
        dict["return_day"] = data["return_day"]
        dict["return_fine"] = data["return_fine"]


    jsonStr = json.dumps(dict, ensure_ascii=False).encode('utf8')
    print type(jsonStr)


    name=u'학생회 대여/반납 일지'
    product_list=objects
    return render_template('rentSystem.html',name=name, product_list=product_list)

@app.route('/login/db/resultrent',methods=['POST','GET'])
def rent_resultrent():
    snu=request.form['snu']
    rpe=request.form['rpe']
    pnu=request.form['pnu']
    rna=request.form['rna']
    rnu=request.form['rnu']
    rsa=request.form['rsa']
    ryear =request.form['rda'][:4]
    rmonth = request.form['rda'][4:6]
    rday = request.form['rda'][6:]

    if dict['rent_sq']>0:
        sq = dict['rent_sq']
    else:
        sq = 0

   # conn = pymysql.connect(host='localhost',user='root',password='intI2017!@',db='intI',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
   # cursor = conn.cursor()

    query = "INSERT INTO rent_log (rent_sq,student_num,rent_person,phone_num,rent_name,rent_num,rent_sa,rent_year,rent_month,rent_day) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    value = (sq+1,snu,rpe,pnu,rna,rnu,rsa,ryear,rmonth,rday)
    cursor.execute(query,value)
    query2 = "UPDATE rent_product SET rent_possible='X', due_year=%s, due_month=%s, due_day=%s WHERE (rent_name LIKE %s && pro_num LIKE %s)"
    value2 = (ryear,rmonth,rday,rna,rnu)
    cursor.execute(query2,value2)
    conn.commit()



    return render_template('resultrent.html',snu=snu,rpe=rpe,pnu=pnu,rna=rna,rnu=rnu,rsa=rsa,ryear=ryear,rmonth=rmonth,rday=rday)

@app.route('/login/db/resultreturn',methods=['POST','GET'])
def return_resultreturn():
    rtsa=request.form['rtsa']
    rtna=request.form['rtna']
    rtnu=request.form['rtnu']
    rtyear=request.form['rtda'][:4]
    rtmonth=request.form['rtda'][4:6]
    rtday=request.form['rtda'][6:]

    query = "UPDATE rent_log SET return_sa=%s, return_year=%s, return_month=%s, return_day=%s WHERE (rent_name LIKE %s && rent_num LIKE %s && return_year IS NULL)"

    value = (rtsa,rtyear,rtmonth,rtday,rtna,rtnu)
    cursor.execute(query,value)
    query2 = "UPDATE rent_product SET rent_possible='O', due_year='0', due_month='0', due_day='0' WHERE (rent_name LIKE %s && pro_num LIKE %s)"
    value2 = (rtna,rtnu)
    cursor.execute(query2,value2)
    conn.commit()



    return render_template('resultreturn.html',rtsa=rtsa,rtna=rtna,rtnu=rtnu,rtyear=rtyear,rtmonth=rtmonth,rtday=rtday)

@app.route('/db/resultreturn/fine')
def return_fine():
    rentday=dict["rent_day"]
    returnday=dict["return_day"]
    fine = (returnday-rentday-1)*500

    query = "UPDATE rent_log SET return_fine=%s"
    cursor.execute(query,fine)
    conn.commit()
    cursor.close()
    conn.close()
    return;

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4101)
