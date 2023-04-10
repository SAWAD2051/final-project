import mysql.connector
from datetime import datetime, date, time,timedelta

def create_database():
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456"
    )
    c=conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS budgetify")
    print("Database created successfully")



def create_user_records_table():
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    c.execute('''CREATE TABLE  IF NOT EXISTS USER_RECORD
         (User_ID int PRIMARY KEY AUTO_INCREMENT,
         First_name VARCHAR(50),
         Last_name  VARCHAR(50),
         Email      VARCHAR(50),
         Password   VARCHAR(50),
         Gender     VARCHAR(50),
         DOB        DATE,
         Job_title  VARCHAR(30),
         City       VARCHAR(35))''')
    print("Table created successfully")
    conn.commit()
    conn.close()




def createAccount(firstname, lastname, email, password, gender,dob, jobtitle, city):
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    c.execute("INSERT INTO USER_RECORD (First_name,Last_name,Email,Password,Gender,DOB,Job_title,City) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(firstname, lastname, email, password, gender,dob, jobtitle, city))
    c.execute("SELECT User_ID,Last_name from USER_RECORD WHERE Email=(%s) LIMIT 0,1",(email,))
    item=c.fetchone()
    uid=str(item[1])
    lname=str(item[0])
    print("inserted succefully")
    conn.commit()
    conn.close()
    return uid,lname


def check_password(email):
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    c.execute("SELECT Password,User_ID,Last_name from USER_RECORD WHERE Email=(%s)",(email,))
    item=c.fetchone()
    conn.commit
    conn.close()
    if item ==None:
        return None
    else:
        return(item)
    

def check_email(email):
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c= conn.cursor()
    sql = "SELECT * FROM USER_RECORD WHERE email = %s"
    c.execute(sql, (email,))
    result = c.fetchall()
    conn.close()
    if len(result) > 0:
        return True
    else:
        return False




def create_user_expense_table(uid,lname):
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    usertablename=lname+"_"+uid
    print(usertablename)
    query = "CREATE TABLE {} (Trans_ID INT,Date DATETIME,Category VARCHAR(50),Amount INT)".format(usertablename)
    c.execute(query)
    print("transaction table created for "+usertablename)
    conn.commit
    conn.close()

def sumOfExpenseForDate():
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    current_date = date.today()
    new_date = current_date - timedelta(days=30)
    print("New date:", new_date.strftime("%Y-%m-%d"))
    c.execute("SELECT Category,SUM(Amount) FROM test_1 WHERE Date BETWEEN (%s) AND (%s) GROUP BY Category;",(new_date,current_date))
    item=c.fetchall()
    print(item)
    conn.commit
    conn.close()


def insert_value_trans(transid,date,cat,amo,lastname,userid):
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    usertablename=str(userid)+"_"+lastname
    sql=("INSERT INTO {} (Trans_ID,Date,Category,Amount) VALUES (%s,%s,%s,%s)".format(usertablename))
    c.execute(sql,(transid,date,cat,amo))
    print("inserted succefully")
    conn.commit()
    conn.close()


def test():
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    c.execute("SELECT user_id, Last_name FROM user_record;")
    item=c.fetchall()

    today = datetime.date.today()
    # date_str = "2022-01-10"
    # today = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    if today.month == 1:
        first_day_of_month = datetime.date(today.year - 1, 12, 1)
    else:
        first_day_of_month = datetime.date(today.year, today.month - 1, 1)

    last_day_of_month = first_day_of_month.replace(day=28) + datetime.timedelta(days=4)
    last_day_of_month = last_day_of_month - datetime.timedelta(days=last_day_of_month.day)


    for i in range(len(item)):
        tablename=str(item[i][0])+'_'+str(item[i][1])
        print(tablename)
        sql="SELECT Category,SUM(Amount) FROM {} WHERE Date BETWEEN (%s) AND (%s) GROUP BY Category;".format(tablename)
        c.execute(sql,(first_day_of_month,last_day_of_month))
        dar=c.fetchall()
        print(dar)
    conn.commit
    conn.close()


def delete_value_trans(transid,lastname,userid):
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="budgetify"
    )
    print("connection established")
    c=conn.cursor()
    usertablename=str(userid)+"_"+lastname
    sql=("DELETE FROM {} WHERE Trans_ID = (%s)".format(usertablename))
    c.execute(sql,(str(transid),))
    print("T_ID ",transid+"of table",usertablename,"deleted succefully")
    conn.commit()
    conn.close()