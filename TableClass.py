from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, String 

# Base 를 마드는 데이터 모델 클래스로 상속
Base = declarative_base() 
class Students(Base): 
    
    # tablename이 table 이름이 된다.
    __tablename__ = 'students' 
    # String(50) 길이 지정
    num = Column(String(50), primary_key=True) 
    name = Column(String(50)) 
    
    def __init__(self, num, name): 
        self.num = num 
        self.name = name 
        
    def __repr__(self): 
        return "<Students('%s', '%s')>" % (self.num, self.name)
