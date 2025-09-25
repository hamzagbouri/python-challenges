from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    priorite = Column(Enum("P1", "P2", "P3", name="priorite_enum"), nullable=False)
    status = Column(Enum("En cours", "Terminé", name="status_enum"), nullable=False, default="En cours")

    def __str__(self):
        return f"{self.id}, {self.description}"

engine = create_engine("postgresql://postgres:Hamza2004@localhost:5432/todolist")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
def get_session():
    return Session()
def get_all_tasks():
    tasks = get_session().query(Task).all()
    return (tasks)
def add_task(task):
    session = get_session()      
    session.add(task)            
    session.commit()            
    session.refresh(task)        
    return task 
def get_task_by_id(id):
    session = get_session()
    task  = session.query(Task).get(id)
    return task
def terminer_task(task):
    session = get_session()
    t = session.query(Task).filter(Task.id == task.id).first()
    if t:
        t.status = "Terminé"
        session.commit()
        return t
    else:
        return False
def supprimer_task(id):
    session=get_session()
    t = session.query(Task).get(id)
    session.delete(t)
    session.commit()
    return True
def modify_task(task):
    session=get_session()
    t=session.query(Task).get(task.id)
    t.description=task.description
    t.priorite = task.priorite
    session.commit()
    return t
