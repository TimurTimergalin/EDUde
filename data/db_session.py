import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("filename required")

    # conn_str = f'mysql+mysqldb://flask:flask@localhost:3306/{db_file.strip()}'
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"connecting {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_scoped_session() -> scoped_session:
    global __factory
    return scoped_session(__factory)


def create_session() -> Session:
    global __factory
    return __factory()


if __name__ == '__main__':
    global_init('db/edu.sqlite')