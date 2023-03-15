from flask import Flask, render_template, request, redirect
from flask_restful import Api,Resource,reqparse
import pymysql
import json

app = Flask(__name__)
from flask_cors import CORS, cross_origin
CORS(app) 


api=Api(app)

@app.before_first_request
def connection():
    s = 'localhost' #Your server(host) name , can use 127.0.0.1
    d = 'book-hive' 
    u = 'root' #Your login user
    p = '1234' #Your login password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn

#classes is for Admin :-
class Admin_AllBooks(Resource):
    def get(self):
        books=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("SELECT * FROM book_tbl")
        data=cursor.fetchall()
        for row in data:
            books.append({"id": row[0], "book_name": row[1], "genre": row[2], "price": row[3], "author":row[4], "published_year": row[5], "img_url": row[6], "availability": row[7]})
        return books
    
#Add A Book in Admin_page    
    def post(self):
        data = request.get_json()
        book_name = data["book_name"]
        genre = data["genre"]
        price = data["price"]
        author = data["author"] 
        published_year = data["published_year"] 
        img_url = data["img_url"] 
        availability = data["availability"] 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO book_tbl ( book_name, genre, price, author, published_year, img_url, availability) VALUES (%s, %s, %s, %s, %s, %s, %s)", ( book_name, genre, price,  author, published_year, img_url, availability))
        conn.commit()
        conn.close()
        return "Book Inserted Sucessfully"

#class is for Admin :-
class Admin_SingleBook(Resource):
#Delete book in Admin_page
    def delete(self,id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM book_tbl WHERE book_id = %s", (id))
        conn.commit()
        conn.close()
        return "Book Deleted"
    
    
#Get single book in Admin_page
    def get(self,id):
        books = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_tbl WHERE book_id = %s", (id))
        data=cursor.fetchall()
        for row in data:
           books.append({"id": row[0], "book_name": row[1], "genre": row[2], "price": row[3], "author":row[4], "published_year": row[5], "img_url": row[6], "availability": row[7]})
        return books[0]
    
    
#Update single book in Admin_page
    def put(self,id):
        data = request.get_json()
        br = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_tbl WHERE book_id = %s", (id))
        for row in cursor.fetchall():
            br.append({"id": row[0], "book_name": row[1], "genre": row[2], "price": row[3], "author":row[4], "published_year": row[5], "img_url": row[6], "availability": row[7]})
        book_name = data["book_name"]
        genre = data["genre"]
        price = data["price"]
        author = data["author"] 
        published_year = data["published_year"] 
        img_url = data["img_url"] 
        availability = data["availability"] 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE book_tbl SET book_name = %s, genre = %s, price = %s, author = %s, published_year = %s, img_url = %s, availability = %s WHERE book_id = %s", (book_name, genre, price, author, published_year, img_url, availability, id))
        conn.commit()
        conn.close()
        return "Book updated Sucessfully"
        
#class is for Admin :-
class Admin_Orders(Resource):
#Get all orders in Admin_page
    def get(self):
        orders=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("SELECT * FROM user_orders")
        data=cursor.fetchall()
        for row in data:
            orders.append({"order_id": row[0], "status": row[1], "user_id": row[2], "book_id": row[3]})
        return orders
 
#Add Order in Admin_page
    def post(self,userId,bookId):
        data = request.get_json()
        status = "Pending"
        #user_id = data["user_id"]
        #book_id = data["book_id"] 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_orders ( order_status, user_id, book_id) VALUES ( %s, %s, %s)", (status, userId, bookId))
        conn.commit()
        conn.close()
        return "Order Inserted Sucessfully"

##class is for Admin :-
class Admin_Single_Order(Resource):
#Delete Order in Admin_page
    def delete(self,id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_orders WHERE order_id = %s", (id))
        conn.commit()
        conn.close()
        return "Order Deleted"
    
#Get single Order in Admin_page
    def get(self,id):
        orders = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_orders WHERE order_id = %s", (id))
        data=cursor.fetchall()
        for row in data:
           orders.append({"order_id": row[0], "order_status": row[1], "user_id": row[2], "book_id": row[3]})
        return orders[0]

    
#Update Order in Admin_page
    def put(self,id):
        data = request.get_json()
        odr = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_orders WHERE order_id = %s", (id))
        for row in cursor.fetchall():
            odr.append({"order_id": row[0], "order_status": row[1], "user_id": row[2], "book_id": row[3]})
        order_status = data["order_status"]
        #user_id = data["user_id"]
        #book_id = data["book_id"] 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_orders SET  order_status = %s  WHERE order_id = %s", (order_status, id))
        conn.commit()
        conn.close()
        return "Order updated Sucessfully"
#End of Admin Classes


#classes is for Customer :-
class Customer_AllBooks(Resource):
   def get(self):
       books=[]
       objconn = connection()
       cursor = objconn.cursor()
       cursor.execute("SELECT * FROM book_tbl")
       data=cursor.fetchall()
       for row in data:
           books.append({"id": row[0], "book_name": row[1], "genre": row[2], "price": row[3], "author":row[4], "published_year": row[5], "img_url": row[6], "availability": row[7]})
       return books
    
class Customer_SingleBook(Resource):   
#Get single book in Customer_page
    def get(self,id):
        books = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_tbl WHERE book_id = %s", (id))
        data=cursor.fetchall()
        for row in data:
           books.append({"id": row[0], "book_name": row[1], "genre": row[2], "price": row[3], "author":row[4], "published_year": row[5], "img_url": row[6], "availability": row[7]})
        return books[0]


class User_table(Resource):
#get all users from  user_table
    def get(self):
        users=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("SELECT * FROM user_tbl")
        data=cursor.fetchall()
        for row in data:
            users.append({"user_id": row[0], "user_email": row[1], "user_password": row[2], "user_role": row[3], "user_register_date":row[4]})
        return users

#Add user to  user_table
    def post(self):
        data = request.get_json()
        user_email = data["user_email"]
        user_password = data["user_password"]
        user_role = data["user_role"]  
        user_register_date = data["user_register_date"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_tbl ( user_email, user_password, user_role, user_register_date) VALUES ( %s, %s, %s, %s)", (user_email, user_password, user_role, user_register_date))
        conn.commit()
        conn.close()
        return "User Added Sucessfully"

class Single_User_tbl(Resource):
#get Single user from  user_table
     def get(self,id):
         users = []
         conn = connection()
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM user_tbl WHERE user_id = %s", (id))
         data=cursor.fetchall()
         for row in data:
            users.append({"user_id": row[0], "user_email": row[1], "user_password": row[2], "user_role": row[3], "user_register_date":row[4]})
         return users[0]
     
#Delete User from user_table
     def delete(self,id):
         conn = connection()
         cursor = conn.cursor()
         cursor.execute("DELETE FROM user_tbl WHERE user_id = %s", (id))
         conn.commit()
         conn.close()
         return "User Deleted"
     
#Update User from user_table
     def put(self,id):
         data = request.get_json()
         ur = []
         conn = connection()
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM user_tbl WHERE user_id = %s", (id))
         for row in cursor.fetchall():
             ur.append({"user_id": row[0], "user_email": row[1], "user_password": row[2], "user_role": row[3], "user_register_date":row[4]})
         user_email = data["user_email"]
         user_password = data["user_password"]
         user_role = data["user_role"] 
         user_register_date = data["user_register_date"]
         conn = connection()
         cursor = conn.cursor()
         cursor.execute("UPDATE user_tbl SET  user_email = %s, user_password = %s, user_role = %s, user_register_date = %s  WHERE user_id = %s", (user_email, user_password, user_role,user_register_date, id))
         conn.commit()
         conn.close()
         return "User updated Sucessfully"
    
    
#Classes For User_Data table
class User_data(Resource):
#get all user_data from user_data_table
     def get(self):
         usrdata=[]
         objconn = connection()
         cursor = objconn.cursor()
         cursor.execute("SELECT * FROM user_data")
         data=cursor.fetchall()
         for row in data:
             usrdata.append({"user_data_id": row[0], "name": row[1], "address": row[2], "city": row[3], "state": row[4], "pincode":row[5], "user_id": row[6]})
         return usrdata
     
   
#Add Single user_data from user_data_table   
     def post(self):
        data = request.get_json()
        name = data["name"]
        address = data["address"]
        city = data["city"]
        state = data["state"]
        pincode = data["pincode"] 
        user_id = data["user_id"] 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_data ( name, address, city, state, pincode, user_id) VALUES ( %s, %s, %s, %s, %s, %s)", ( name, address, city, state,  pincode, user_id))
        conn.commit()
        conn.close()
        return "User-Data Inserted Sucessfully"


class Single_User_data(Resource):
#Delete Single user_data from user_data_table 
    def delete(self,id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_data WHERE user_data_id = %s", (id))
        conn.commit()
        conn.close()
        return "User-Data Deleted"
    
    
#Get Single user_data from user_data_table
    def get(self,id):
        user = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (id))
        data=cursor.fetchall()
        for row in data:
           user.append({"user_data_id": row[0], "name": row[1], "address": row[2], "city": row[3], "state": row[4], "pincode":row[5], "user_id": row[6]})
        return user[0]
    
    
#Update  Single user_data from user_data_table
    def put(self,id):
        data = request.get_json()
        br = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (id))
        for row in cursor.fetchall():
            br.append({"user_data_id": row[0], "name": row[1], "address": row[2], "city": row[3], "state": row[4], "pincode":row[5], "user_id": row[6]})
        name = data["name"]
        address = data["address"]
        city = data["city"]
        state = data["state"]
        pincode = data["pincode"] 
        user_id = data["user_id"] 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET name = %s, address = %s, city = %s, state = %s, pincode = %s, user_id = %s WHERE user_id = %s", (name, address, city, state, pincode, user_id, id))
        conn.commit()
        conn.close()
        return "User_Data updated Sucessfully"
    
    
    
    
    
class User_Orders(Resource):
#Get all orders of user
    def get(self,id,):
        orders=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("SELECT * FROM user_orders WHERE user_id = %s",(id))
        data=cursor.fetchall()
        for row in data:
            orders.append({"order_id": row[0], "status": row[1], "user_id": row[2], "book_id": row[3]})
        return orders
    
#End of Customer Classes

# Category calsses
class Fiction_Books(Resource):
    def get(self,genre):
        Fbook=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("SELECT * FROM book_tbl WHERE genre = %s",(genre))
        data=cursor.fetchall()
        for row in data:
           Fbook.append({"id": row[0], "book_name": row[1], "genre": row[2], "price": row[3], "author":row[4], "published_year": row[5], "img_url": row[6], "availability": row[7]})
        return Fbook

class User_Id(Resource):
    def get(self,user_email, user_password):
        UserID_Role=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("SELECT user_id, user_role FROM user_tbl WHERE user_email = %s and user_password = %s",(user_email, user_password))
        data=cursor.fetchall()
        for row in data:
           UserID_Role.append({"user_id": row[0], "user_role": row[1]})
        return UserID_Role[0]
    
class aadmin_orders(Resource):
    def get(self):
        admin_Orders=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("select user_orders.order_id, user_orders.user_id, user_data.name, book_tbl.book_name,  book_tbl.img_url, user_data.pincode, user_orders.order_status from ((( user_orders inner join user_tbl on user_orders.user_id= user_tbl.user_id) inner join book_tbl on user_orders.book_id= book_tbl.book_id) inner join user_data on user_orders.user_id= user_data.user_id)")
        data=cursor.fetchall()
        for row in data:
            admin_Orders.append({"order_id": row[0], "user_id": row[1], "name": row[2], "book_name": row[3],  "img_url":row[4], "pincode": row[5], "order_status":row[6]})
        return admin_Orders
    
class aadim_single_orders(Resource):
    def get(self,user_id):
        single_order=[]
        objconn = connection()
        cursor = objconn.cursor()
        cursor.execute("select user_orders.order_id, user_orders.user_id, user_data.name, book_tbl.book_name,  book_tbl.img_url, user_data.pincode, user_orders.order_status from ((( user_orders inner join user_tbl on user_orders.user_id= user_tbl.user_id) inner join book_tbl on user_orders.book_id= book_tbl.book_id) inner join user_data on user_orders.user_id= user_data.user_id) where user_tbl.user_id = %s",(user_id))
        data=cursor.fetchall()
        for row in data:
           single_order.append({"order_id": row[0], "user_id": row[1], "name": row[2], "book_name": row[3],  "img_url":row[4], "pincode": row[5], "order_status":row[6]})
        return single_order
        
  
     
  
    
 
    
  
    
api.add_resource(Admin_AllBooks, '/admin/books') 
api.add_resource(Admin_SingleBook, '/admin/books/<int:id>')

api.add_resource(Admin_Orders, '/admin/orders/<int:userId>/<int:bookId>')
api.add_resource(Admin_Single_Order, '/admin/orders/<int:id>')

api.add_resource(Customer_AllBooks, '/user/books')
api.add_resource(Customer_SingleBook, '/user/books/<int:id>')

api.add_resource(User_table, '/admin/user-table')
api.add_resource(Single_User_tbl, '/admin/user-table/<int:id>')

api.add_resource(User_data, '/users-data')
api.add_resource(Single_User_data, '/users-data/<int:id>')

api.add_resource(User_Orders, '/user/orders/<int:id>')

api.add_resource(Fiction_Books, '/user/Fbooks/<string:genre>')

api.add_resource(User_Id, '/user/<string:user_email>/<string:user_password>')

api.add_resource(aadmin_orders, '/orders')
api.add_resource(aadim_single_orders, '/orders/<int:user_id>')


app.debug=True

if __name__ == '__main__' :
    app.run(host='localhost', port=7000)
        
    