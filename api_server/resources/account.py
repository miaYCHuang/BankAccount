from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback


#Only accept these fields
parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')
parser.add_argument('deleted')

# http://localhost:5000/user/<user_id>/account/<id>
class Account(Resource):
    def db_init(self):
        db=pymysql.connect(host='db_mysql',user='root',password='12345678',db='api')
        cursor=db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    #[GET]取得使用者的一個帳戶
    def get(self,user_id,id):
        db, cursor=self.db_init()
        sql="""SELECT * FROM api.accounts WHERE user_id = '{}' AND id = '{}' AND deleted is not True""".format(user_id,id)
        cursor.execute(sql)
        db.commit()
        account=cursor.fetchone()#return one row
        db.close()
        print(account)
        if account!=None:
            return jsonify({'data':account})
        else:
            return jsonify({'data':"Incorrect! Check the accounts"})

    #[PATCH]修改使用者的一個帳戶資訊
    def patch(self,user_id, id):
        db, cursor=self.db_init()
        arg=parser.parse_args()
        account={
            'balance':arg['balance'],
            'account_number':arg['account_number'],
            'user_id':arg['user_id']
            #'deleted':arg['deleted'],
        }     
        query=[]
        for key, value in account.items():
            if value != None:
                query.append(key+ "=" + " '{}' ".format(value))
        query = ",".join(query) 
        sql= """
            UPDATE `api`.`accounts` SET {} WHERE (`user_id` = '{}' AND `id` = '{}');
        """.format(query,user_id,id)                    
        response = {}
        try:
            cursor.execute("""SELECT * FROM api.accounts WHERE user_id = '{}' AND id = '{}' AND deleted is not True""".format(user_id,id))
            account=cursor.fetchall()
            if len(account)>0:
                cursor.execute(sql)
                response['msg']= 'success'
            else:
                response['msg'] = 'Incorrect! Check the accounts'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)
    
    #[GET]刪除使用者的一個帳戶
    def delete(self,user_id, id):
        db, cursor=self.db_init()
        # tinyint(1) -> 1=TRUE, 0=FALSE; 默認=0
        sql=""" UPDATE `api`.`accounts` SET deleted = True WHERE (user_id = '{}' AND `id`='{}') """.format(user_id,id) #Soft delete
        response={}
        try:
            cursor.execute("""SELECT * FROM api.accounts WHERE user_id = '{}' AND id = '{}' AND deleted is not True""".format(user_id,id))
            account=cursor.fetchall()
            if len(account)>0:
                cursor.execute(sql)
                response['msg']= 'success'
            else:
                response['msg'] = 'Incorrect! Check the accounts'
        except:
            traceback.print_exc()
            response['msg']='failed'
        db.commit()
        db.close        
        return jsonify(response)


# http://localhost:5000//user/<user_id>/accounts
class Accounts(Resource):
    def db_init(self):
        db=pymysql.connect(host='db_mysql',user='root',password='12345678',db='api')
        cursor=db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    #[GET]取得使用者的所有帳戶 
    def get(self,user_id):
        db, cursor=self.db_init()
        #sql='SELECT * FROM api.account WHERE deleted is not True'
        sql='SELECT * FROM api.accounts WHERE user_id = "{}" AND deleted is not True'.format(user_id)
        cursor.execute(sql)
        db.commit()
        accounts=cursor.fetchall()#return rows
        db.close()
        return jsonify({'data':accounts})
    
    #[POST]新增一個使用者的帳戶
    def post(self,user_id):
        db, cursor=self.db_init()
        arg=parser.parse_args()
        user={
            'balance':arg['balance'],
            'account_number':arg['account_number'],
            'user_id':arg['user_id'],
        }
        sql="""
            INSERT INTO `api`.`accounts`(`balance`,`account_number`,`user_id`) VALUES('{}','{}','{}');
        """.format(user['balance'], user['account_number'], user_id)   
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

