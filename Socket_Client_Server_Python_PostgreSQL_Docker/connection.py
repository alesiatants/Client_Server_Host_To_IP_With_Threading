from sqlalchemy import create_engine, Column, Integer, String, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Установка уровня логирования и формата сообщений
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

# Создание базового класса для моделей SQLAlchemy
Base = declarative_base()

# Определение модели для таблицы socket_log в схеме socket
class SocketLog(Base):
    __tablename__ = 'socket_log'
    __table_args__ = {'schema': 'socket'} 
    
    id = Column(Integer, primary_key=True)
    domen = Column(String)
    ip = Column(String)
    timelive = Column(Integer)

class Connection:
    def __init__(self):
        self.username = 'postgres'
        self.password = 'postgres'
        self.hostnameport = 'localhost:5432'
        self.database = 'socket_db'
        # Создание подключения к БД
        self.engine = self.create_engine()
        # Создание сессии работы с БД
        self.Session = sessionmaker(bind=self.engine)

    def create_engine(self):
        '''Подключение к Postgresql, согласно параметрам, прописанным в docker-compose'''
        while True:
            try:
                engine = create_engine(f'postgresql+psycopg2://{self.username}:{self.password}@{self.hostnameport}/{self.database}')
                return engine
            except Exception as ex:
                LOGGER.warning(f"Ошибка установки соединения с БД - {str(ex)}")

    def insert_new_record(self, domen, ip, ttl):
        session = self.Session()
        new_record = SocketLog(domen=domen, ip=ip, timelive=ttl)
        session.add(new_record)
        # Фиксация изменений в БД
        session.commit()
        session.close()

    def check_records(self, domen):
        session = self.Session()
        # Удаление старых записей, функция описана в init.sql
        session.execute(text('SELECT socket.delete_old_rows_before_select()'))
        # Проверка наличия записей в БД с соответствующим доменом
        count = session.query(SocketLog).filter(SocketLog.domen == domen).count()
        session.close()
        return count

    def find_value(self, domen):
        session = self.Session()
        # Получение ip по домену
        ip_value = session.query(SocketLog.ip).filter(SocketLog.domen == domen).scalar()
        session.close()
        return ip_value
    def select_all(self):
        session = self.Session()
        session.execute(text('SELECT socket.delete_old_rows_before_select()'))
        stmt = session.query(*[getattr(SocketLog, field) for field in ['domen', 'ip']])
        res =stmt.all()
        session.close()
        return res
