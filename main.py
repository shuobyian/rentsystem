#-*- coding: utf-8 -*-
from flask import Flask, render_template
import pymysql

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
        "대여 순서" : data['rent_sq'],
        "대여 물품" : data['rent_name'],
        "대여 물품 번호" : data['rent_num'],
        "대여자" : data['rent_person'],
        "대여 담당" : data['rent_sa'],
        "대여 연" : data['rent_year'],
        "대여 월" : data['rent_month'],
        "대여 일" : data['rent_day'],
        "반납 담당" : data['return_sa'],
        "반납 연" : data['return_year'],
        "반납 월" : data['return_month'],
        "반납 일" : data['return_day'],
        "연체료" : data['return_fine']
    })

cursor.execute(sql)

sql2 = 'select * from rent_product'
cursor.execute(sql2)
products = []
for data in cursor.fetchall():
    products.append({
        "대여 물품 번호" : data['rent_num'],
        "대여 물품" : data['rent_name'],
        "대여 가능 여부" : data['rent_possible'],
        "반납 예정 연" : data['due_year'],
        "월" : data['due_month'],
        "일" : data['due_day']
    })


@app.route('/')
def hi(charset='utf-8'):
        name=u'학생회 대여물품 목록'
        product_list=[objects[0]]
        return render_template('rentList.html', name=name, product_list=product_list)



@app.route('/login/rent.html')
def Rent():
    return render_template('rent.html')

@app.route('/login/return.html')
def Return():
    return render_template('return.html')


@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/login/db')
def db():
        return render_template('rentSystem.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4101)
