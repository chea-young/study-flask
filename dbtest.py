import sqlite3

conn = sqlite3.connect('mydb.db') 

# Cursor 객체 생성 
c = conn.cursor()

# 테이블 생성
c.execute("CREATE TABLE student (num varchar(50), name varchar(50))") 

# 데이터 삽입
c.execute("INSERT INTO student VALUES ('201802919', '파이썬')")

# 데이터 불러 와서 출력
for row in c.execute('SELECT * FROM student'):
    print(row)

# 학번을 검색해서 정보 출력
num = ('201802919' ,)
c.execute('SELECT * FROM student WHERE num = ?', num)
print(c.fetchone())
data = ('201802919', '파이썬')
c.execute('SELECT * FROM student WHERE num = ? and name = ?', num)

# execute 에 db 에 적용 
conn.commit() 

#접속한 db 닫기 
conn.close()
