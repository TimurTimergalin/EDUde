import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("filename required")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"connecting {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    print(engine)
    __factory = orm.sessionmaker(bind=engine)
    if not __factory:
        raise Exception('her\'')

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


if __name__ == '__main__':
    global_init('db/edu.sqlite')