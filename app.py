from flask import Flask,request, render_template, redirect,url_for
import TableClass
import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///C:\\dev\\db\\mydb.db')
# mysql+mysqlconnector://chaeyoung:l!ch!y!0413@Mysql 디비주소:3306/mydbcharset=utf8
Session = sessionmaker(bind=engine)
#DB table  생성
TableClass.create_tb(engine)
#단일 모듈
#패키지 형태 일 때는 app = Flask('application 이름')
app = Flask(__name__)


@app.route('/hello') 
def hellohtml(): 
    return render_template("hello.html")

@app.route('/')
def base():
    return 'Hello, World!'

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

@app.route('/getinfo') 
def getinfo(): 
    # info = dbdb.select_all() 
    # .all() 전체데이터
    # filter(), filter_by 검색

    session = Session() 
    info = session.query(TableClass.Students.num, TableClass.Students.name).all() 
    return render_template("info.html", data=info)


# 페이지 요청 시 오류가 나면
#abort(404) -> 404 오류 일으킴
@app.errorhandler(404) 
def page_not_found(error): 
    return "페이지가 없습니다. URL를 확인 하세요", 404


if __name__ == '__main__': 

    # debug = True로 하면 작업들이 자동으로 하게 된다.
    app.run(debug=True)

