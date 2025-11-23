from sqlalchemy import create_engine, String, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine(url="sqlite:///posts.db")

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', content='{self.content}')>"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    post = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', password='{self.password}')>"
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
