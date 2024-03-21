import pymysql.cursors

#Configure MySQL
def get_db_connection():
    conn = pymysql.connect(host='localhost',
                        port = 3306,
                        user='root',
                        db='roomio',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    return conn