
# coding: utf-8

# In[ ]:


import pymysql


# In[ ]:


connection = pymysql.connect(
        host = 'astronaut.snu.ac.kr',
        user = 'BDE-2018-03',
        password = 'e10ee29cc86f',
        db = 'BDE-2018-03',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor)


# In[ ]:


def main():
    print("="*70)
    print("1. print all buildings")
    print("2. print all performances")
    print("3. print all audiences")
    print("4. insert a new building")
    print("5. remove a bulidng")
    print("6. insert a new performances")
    print("7. remove a performances")
    print("8. insert a new audience")
    print("9. remove an audience")
    print("10. assign a performances to a building")
    print("11. book a performances")
    print("12. print all performances assigned to a building")
    print("13. print all audiences who booked for a performances")
    print("14. print ticket booking status of a performances")
    print("15. exit")
    print("="*70)

def action():
    number = 0
    main()
    while(number != 15):
        number = input("Select your action : ")
        eval("f%s()" %number)  
        
def f1():
    with connection.cursor() as cursor:
        sql = "select * from building"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("-"*70)
        print('%-5s %-20s %-10s %-10s %-10s' % ('id', 'name', 'location', 'capacity', 'assigned'))
        print("-"*70)
        for i in result:
            print('%-5s %-20s %-10s %-10s %-10s' % (i['id'], i['name'], i['location'], i['capacity'], i['assigned']))
        print("-"*70)

def f2():
    with connection.cursor() as cursor:
        sql = "select * from perform"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("-"*70)
        print('%-5s %-20s %-10s %-10s %-10s' % ('id', 'name', 'type', 'price', 'booked'))
        print("-"*70)
        for i in result:
            print('%-5s %-20s %-10s %-10s %-10s' % (i['id'],i['name'] , i['type'] , i['price'] , i['booked']))
        print("-"*70)

def f3():
    with connection.cursor() as cursor:
        sql = "select * from audience"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("-"*70)
        print('%-5s %-20s %-10s %-10s' % ("id" , "name", "gender" , "age"))
        print("-"*70)
        for i in result:
            print('%-5s %-20s %-10s %-10s' % (i['id'],i['name'] ,i['gender'] , i['age']))
        print("-"*70)

def f4():
    with connection.cursor() as cursor:
        name = input("Builidng name: ")
        location = input("Building location: ")
        capacity = input("Building capacity: ")

        sql = "insert into building (name, location, capacity) values(%s, %s, %s)" 
        cursor.execute(sql, (name, location, int(capacity)))
        connection.commit()

        print("A building is successfully inserted")
        

def f5():
    with connection.cursor() as cursor:
        id = int(input("building id: "))
        sql = 'select id from building where id = %s' % id
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) != 0:
            sql = "delete from building where id = %s" % id
            cursor.execute(sql)
            connection.commit()
            print("A building is successfully deleted")
        else:
            print("No building")


def f6():
    with connection.cursor() as cursor:
        name = input("performances name: ")
        type = input("performances type: ")
        price = int(input("performances price: "))

        sql = 'insert into perform(name, type,  price) values(%s, %s, %s)' 
        cursor.execute(sql, (p_name,p_type,p_price))
        connection.commit()

        print("A performances is successfully inserted")


def f7():
    with connection.cursor() as cursor:
        p_id = int(input("performances id: "))
        sql = 'select id from perform where id = %s' % p_id
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) != 0:
            sql = 'delete from perform where id = %s' % p_id
            cursor.execute(sql)
            connection.commit()
            print("A performances is successfully deleted")
        else:
                 print("No performances")

def f8():
    with connection.cursor() as cursor:
        name = input("Audience name: ")
        gender = input("Audience gender: ")
        age = int(input("Audience age: "))

        sql = 'insert into audience(name, gender, age) values(%s, %s, %s)'
        cursor.execute(sql, (name,gender,age))
        connection.commit()

        print("A Audience is successfully inserted")

def f9():
    with connection.cursor() as cursor:
        id = int(input("audience id: "))
        sql = 'select id from audience where id = %s' % id
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) != 0:
            sql = 'delete from audience where id = %s ' % id
            cursor.execute(sql)
            connection.commit()
            print("A Audience is successfully deleted")
        else:
            print("No audience")


def f10():
    with connection.cursor() as cursor:
        b_id = int(input('Building id : '))
        p_id = int(input('performances id: '))

        sql = 'select id from perform  where id = %s' % p_id
        cursor.execute(sql)
        result = cursor.fetchall()

        if str(result) in str(p_id):
            print("Already assigned.")
        else:
            sql = "update perform set b_id = %s where id = %s " % (b_id, p_id)
            sql1 = "update building set assigned = assigned + 1 where id = %s" % b_id
            cursor.execute(sql)
            cursor.execute(sql1)
            connection.commit()
            print('Successfully assigned a performances')

            
def f11():
    with connection.cursor() as cursor:
        p_id = int(input('performances id : '))
        a_id = int(input('Audience_id : '))
        seat_number = input('Seat number : ')
        seat_number1 = list(map(int, seat_number.split(',')))
        b_id = int(input('Building id : '))
        
        sql = "select capacity from building b, perform p where b.id = p.b_id and b.id = %s" % b_id
        cursor.execute(sql)
        result1 = cursor.fetchall()
        
        seat_capacity = result1[0]['capacity']

        for l in seat_number1:
            if l > seat_capacity:
                print('Not in range')                   
                
        sql1 = "select seat_number from book where p_id=%s "  % p_id
        cursor.execute(sql1)
        result2 = cursor.fetchall()
        
        if result2 != ():
            print("Already booked")
                
        else:
            for k in seat_number1:
                sql = 'insert into book (a_id, p_id, seat_number) values (%s, %s, %s)' % (a_id, p_id, k)
                cursor.execute(sql)
                sql1 = 'update perform set booked = booked+1 where id = %s' % p_id
                cursor.execute(sql1)
                sql2 = 'update audience set p_id = %s where id = %s and p_id is null' % (p_id, a_id)
                cursor.execute(sql2)
                connection.commit()


            sql3 = 'select count(seat_number) as s_num from book where a_id = %s'% a_id
            cursor.execute(sql3)
            seat_num = cursor.fetchall()[0]["s_num"]
            sql4 = 'select price from perform where id = %s'%  p_id
            cursor.execute(sql4)
            s_price = cursor.fetchall()[0]["price"]

        print("Successfully booked a performances")
        print("Total ticke price is : ", seat_num * s_price)

def f12():
    with connection.cursor() as cursor:
        b_id = int(input("Building ID: "))
        sql = "select id from building"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        for i in range(len(result)):
            if result[i]['id'] == b_id:
                sql = "select p.id, p.name, type, price, booked from perform p, building b where b.id = p.b_id and b.id = %s"% b_id
                cursor.execute(sql)
                result1 = cursor.fetchall()
                
                if result1 != ():
                    print('%-5s %-15s %-10s %-5s %-10s' % ('id', 'name', 'type', 'price', 'booked'))
                    for j in result1:
                        print('%-5d %-15s %-10s %-5s %-10d' % (
                            j['id'], j['name'], j['type'], j['price'], j['booked']))
                else:
                    print("No building")
                    
                    
def f13():
    with connection.cursor() as cursor:
        p_id = int(input("performances ID: "))
        sql = "select id from perform"
        cursor.execute(sql)
        result = cursor.fetchall()

        for i in range(len(result)):
            if  result[i]['id'] == p_id:
                sql = "select distinct id, name, gender, age from audience a, book b where b.a_id=a.id and b.p_id=%s" % p_id
                cursor.execute(sql)
                result1 = cursor.fetchall()
                print('%-5s %-15s %-10s %-5s' % ('id', 'name', 'gender', 'age'))
                for j in result1:
                    print('%-5d %-15s %-10s %-5d' % (j['id'],j['name'],j['gender'],j['age']))
            else:
                print("no building")

                                                  
def f14():
    with connection.cursor() as cursor:
        try:
            p_id =int(input('performances ID: '))
            sql = "select id from perform where id=%s" % p_id
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                print("No performances")

            sql1 = "select assigned from building b , perform p  where p.b_id = b.id and p.id=%s" %  p_id
            cursor.execute(sql1)
            result1 = cursor.fetchall()
            if result1 is () or result1[0]['assigned'] == 0:
                print("Not assigned perfomance")                  

            sql2 = "select capacity from building b , perform p  where p.b_id = b.id and p.id = %s"% p_id
            cursor.execute(sql2)
            result2 = cursor.fetchall()[0]['capacity']
            p_capacity = result2[0]['capacity']

            sql3 = "select seat_number ,a_id from book where p_id = %d"% p_id
            cursor.execute(sql3)
            result3 = cursor.fetchall()
            seated = [i['seat_number'] for i in result3]
            print('%-10s%-10s' % ('seat_num','aud_id'))

            for seat_num in range(1,p_capacity+1):
                for row in result3:

                    if seat_num in seated:
                        print('%-10s%-10s'%(seat_num, row['a_id']))
                        
                    else:
                        print(seat_num, "")
        
        except IndexError:   # assign 추출 문제
            pass
def f15():
    connection.close()
    print("Bye!")


# In[ ]:


action()

