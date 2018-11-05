import pymysql

connection = pymysql.connect(host="localhost",db="finger",user="root",password="123456")
cursor = connection.cursor()

def adduser(name):
    cursor.execute("insert into user (`name`,`auth`) values (%s,'1')",name)
    id = connection.insert_id()
    connection.commit()
    return id

def getusers():
    users = []
    cursor.execute("select * from user")
    for rs in cursor.fetchall():
        user = {}
        user["id"] = rs[0]
        user["name"] = rs[1]
        users.append(user)
    return users

def delteuser(id):
    cursor.execute("delete from user where id = %s",id)
    connection.commit()
