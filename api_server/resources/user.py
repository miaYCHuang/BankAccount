from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

#Only accept these fields
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

#http://localhost:5000/user/<id>
class User(Resource):
    def db_init(self):
        db=pymysql.connect(host='db_mysql',user='root',password='12345678',db='api')
        cursor=db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    #[GET]取得一筆使用者
    def get(self,id):
        db, cursor=self.db_init()
        sql="""SELECT * FROM api.users WHERE id = '{}' AND deleted is not True""".format(id)
        cursor.execute(sql)
        db.commit()
        user=cursor.fetchone()#return one row
        db.close()
        return jsonify({'data':user})
    
    #[PATCH]修改一筆使用者資料
    def patch(self, id):
        db, cursor=self.db_init()
        arg=parser.parse_args()
        user={
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'],
            'note':arg['note'],
        }     
        query=[]
        for key, value in user.items():
            if value != None:
                query.append(key+ "=" + " '{}' ".format(value))
        query = ",".join(query)#name= 'Mia' ,birth= '2023-05-05' 
        sql= """
            UPDATE `api`.`users` SET {} WHERE (`id` = '{}');
        """.format(query,id)                    
        response = {}
        try:
            cursor.execute(sql)
            response['msg']= 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)

    #[DELETE]刪除一筆使用者資料
    def delete(self, id):
        db, cursor=self.db_init()
        #sql=""" DELETE FROM `api`.`users` WHERE (`id` = '{}') """.format(id) #Hard delete
        # tinyint(1) - 1=TRUE, 0=FALSE; 默認=0
        sql=""" UPDATE `api`.`users` SET deleted = True WHERE (`id`='{}') """.format(id) #Soft delete  True(1)=已刪除
        response={}
        try:
            #db.session.delete(user)
            #db.session.commit()
            cursor.execute(sql)
            response['msg']='success'
        except:
            traceback.print_exc()
            response['msg']='failed'
        db.commit()
        db.close        
        return jsonify(response)


#http://localhost:5000/users
class Users(Resource):
    def db_init(self):
        db=pymysql.connect(host='db_mysql',user='root',password='12345678',db='api')#MySQL Workbench
        cursor=db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    #[GET]取得所有使用者
    def get(self):   
        db, cursor=self.db_init()
        arg = parser.parse_args()
        sql='SELECT * FROM api.users WHERE deleted is not True'
        if arg['gender'] != None:
            sql += ' and gender = "{}" '.format(arg['gender'])
        cursor.execute(sql)
        db.commit()
        users=cursor.fetchall()
        db.close()
        return jsonify({'data':users})
    
    #[POST]增加一筆使用者
    def post(self): 
        db, cursor=self.db_init()
        arg=parser.parse_args()
        user={
            'name':arg['name'],
            'gender':arg['gender'] or 0,
            'birth':arg['birth'] or '1990-01-01',
            'note':arg['note']
        }
        sql="""
            INSERT INTO `api`.`users`(`name`,`gender`,`birth`, `note`) VALUES('{}','{}','{}','{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])   

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

