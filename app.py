from flask import Flask,request, render_template, redirect,url_for, session, abort
import TableClass
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import dbdb
"""
engine = sqlalchemy.create_engine('sqlite:///C:\\dev\\db\\mydb.db')
# mysql+mysqlconnector://chaeyoung:l!ch!y!0413@Mysql 디비주소:3306/mydbcharset=utf8
Session = sessionmaker(bind=engine)
#DB table  생성
TableClass.create_tb(engine)
"""
#단일 모듈
#패키지 형태 일 때는 app = Flask('application 이름')
app = Flask(__name__)
app.secret_key = b'aaa!111/'

@app.route('/')
def base():
    return 'Hello, World!'

#로그인 사용자만 접근 가능으로 
@app.route('/form') 
def form(): 
    if 'user' in session:
        return render_template("test.html")
    return redirect(url_for('login'))

@app.route('/senddate') 
def senddate(): 
    name = 'world'
    return render_template("senddate.html", data=name)

@app.route('/hello/<name>')
def hello(name):
    return 'hello {}'.format(name)

@app.route('/input/<int:num>') 
def input(num): 
    name = '' 
    if num == 1: 
        name = '도라에몽' 
    elif num == 2: 
        name = '진구' 
    elif num == 3: 
        name = '퉁퉁이' 
    return "hello {}".format(name)

@app.route('/image') 
def image(): 
    return render_template("image1.html")

#리다이렉션
@app.route('/daum')
def daum():
    return redirect("https://www.daum.net/")

#GET, POST 함수 사용
@app.route('/method', methods=['GET', 'POST']) 
def method(): 
    if request.method == 'GET': 
        #num, name은 html에서 name=으로 받아지는 거
        #http://127.0.0.1:5000/method?num=123
        num = request.args['num']
        #num = request.args.get('num')
        name = request.args.get('name')
        return "GET으로 전달된 데이터({} {})".format(num, name) 
    else: 
        num = request.form['num']
        name = request.form['name']
        dbdb.insert_data(num,name)
        #with open("static/save.txt", 'w', encoding='utf-8') as f:
            #f.write("%s, %s " %(num, name))
        return "POST로 전달된 데이터({} {})".format(num, name) 
"""
        #db에 저장
        session = Session() 
        st_data = TableClass.Students(num, name) 
        try: 
            session.add(st_data) 
            session.commit() 
        except Exception as e: 
            #error 발생시 저장 안됩
            session.rollback () 
            abort (500, 'Error. 데이터 저장 실패')

        return "POST로 전달된 데이터({} {})".format(num, name) 
"""

#로그인
@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'GET': 
        return render_template('login.html') 
    else: 
        userid = request.form['id'] 
        pw = request.form['pw'] 
        # id와 pw가 임의로 정한 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다 
        if userid == 'abc' and pw == '1234': 
            session['user'] = userid 
            return ''' 
                <script> alert("안녕하세요~ {}님"); 
                location.href="/form" 
                </script> 
            '''.format(userid) 
            # return redirect(url_for('form')) 
        else: 
            return "아이디 또는 패스워드를 확인 하세요."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('form'))

@app.route('/char') 
def char(): 
    import json
    name = 'world'
    character = { 
        "name": name, 
        "lv": 1, 
        "hp": 100,
        "items": ["대나무헬리콥터", "빅라이트", "어디로든 문"], 
        "skill": ["펀치", "핵펀치", "피하기"] 
    } 
    with open("static/save.txt", 'w', encoding='utf-8') as f:
        json.dump(character, f, ensure_ascii = False)
    
    with open("static/save.txt", 'r', encoding='utf-8') as f:
        data = f.read()
        chara = json.loads(data)
    return render_template('view.html', items=character['items'])

@app.route('/getinfo') 
def getinfo(): 
    info = dbdb.select_all()
    return render_template("info.html", data=info)   
    # 파일 입력
    #with open("static/save.txt", 'r', encoding='utf-8') as file:
        #student = file.read().split(',')
    #return '번호: {} 이름: {}'.format(student[0], student[1])
    

    # info = dbdb.select_all() 
    # .all() 전체데이터
    # filter(), filter_by 검색

    """session = Session() 
    info = session.query(TableClass.Students.num, TableClass.Students.name).all() 
    return render_template("info.html", data=info)"""


# 페이지 요청 시 오류가 나면
#abort(404) -> 404 오류 일으킴
@app.errorhandler(404) 
def page_not_found(error): 
    return "페이지가 없습니다. URL를 확인 하세요", 404


if __name__ == '__main__': 
    dbdb.create_table()
    # debug = True로 하면 작업들이 자동으로 하게 된다.
    app.run(debug=True)

