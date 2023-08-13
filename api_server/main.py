from flask import Flask,request, jsonify,send_from_directory
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts,Account
from flask_swagger_ui import get_swaggerui_blueprint
import pymysql
import traceback

app= Flask(__name__)
api=Api(app)

api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
api.add_resource(Accounts,'/user/<user_id>/accounts')
api.add_resource(Account,'/user/<user_id>/account/<id>')

#swagger
#http://localhost/swagger/
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python API - Swagger"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

#[POST]使用者一個帳戶存錢
@app.route('/user/<user_id>/account/<id>/deposit',methods=['POST'])    
def deposit(user_id,id):
    db, cursor, account=get_account(user_id,id)
    if account == None:
        return jsonify({'msg' : 'Incorrect! Check the accounts'})
    money =request.get_json()['money']
    balance=account['balance']+int(money)
    sql='UPDATE api.accounts SET balance={} WHERE id ={} AND deleted is not True'.format(balance,id)
    response={}
    try:
        cursor.execute(sql)
        response['msg']='success'
    except:
        traceback.print_exc()
        response['msg']='failed'
    db.commit()
    db.close()
    return jsonify(response)

#[POST]使用者一個帳戶領錢
@app.route('/user/<user_id>/account/<id>/withdraw',methods=['POST'])
def withdraw(user_id,id):
    db, cursor, account=get_account(user_id,id)
    if account == None:
        return jsonify({'msg' : 'Incorrect! Check the accounts'})
    money =request.get_json()['money']
    balance=account['balance']-int(money)
    if balance < 0:
        return jsonify({'msg' : 'Not having enough money'})
    sql='UPDATE api.accounts SET balance={} WHERE id ={} AND deleted is not True'.format(balance,id)
    response={}
    try:
        cursor.execute(sql)
        response['msg']='success'
    except:
        traceback.print_exc()
        response['msg']='failed'
    db.commit()
    db.close()
    return jsonify(response) 

def get_account(user_id,id):#取得所有 id=n 的資料
    db=pymysql.connect(host='db_mysql',user='root',password='12345678',db='api')
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql=""" SELECT * FROM api.accounts WHERE user_id = '{}' AND id ='{}' AND deleted is not True""".format(user_id,id)
    cursor.execute(sql)
    return db, cursor,cursor.fetchone()

#測試資料庫
@app.route('/test')
def inedx():
    db=pymysql.connect(host='db_mysql',user='root',password='12345678',db='api')
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql=""" SELECT * FROM api.users"""
    cursor.execute(sql)
    db.commit()
    data=cursor.fetchall()#return rows
    db.close()
    return jsonify({'data':data})

#測試API
@app.route('/')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', debug=True, threaded=True, port=3000)
