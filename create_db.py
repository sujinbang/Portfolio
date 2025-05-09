import sqlite3
 
conn = sqlite3.connect('database.db')
print('데이터베이스 생성 성공!')
 
conn.execute(
    '''
    create table issue (name text, addr text, city text, pin text)
    '''
)
print('테이블 생성 성공!')
 
conn.close()