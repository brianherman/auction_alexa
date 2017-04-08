import datetime
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

#https://github.com/johnwheeler/flask-ask/issues/4
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import psycopg2

class Authentication:
    #session.user.userId
    def get_token(self, uid):
        if uid:
            engine = create_engine(
                "postgresql+psycopg2://root:Insw0eifAn4wtbt@ebay.cbmefdfxkvkf.us-east-1.rds.amazonaws.com:5432/ebay"
            )
            Base = automap_base()

            Base.prepare(engine, reflect=True)
            Session = sessionmaker(bind=some_engine)

            # create a Session
            session = Session()
            try:
                result = session.query(User).filter_by(uid=uid).one()
                return result['token']
            except:
                return {'error': 'Multiple login tokens.'}
        else:
            return {'error': 'Null Token.'}

if __name__ == '__main__':
    a = Authentication()
    a.get_token(1)