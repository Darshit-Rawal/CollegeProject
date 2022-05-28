import pymysql.cursors

# Connect to the database
def getConnection():
    connection = pymysql.connect(host='localhost',
                             user='root',   
                             password='',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection