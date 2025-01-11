import os
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    followers = relationship("Follower", foreign_keys="Follower.user_to_ID", back_populates="followed_user")
    following = relationship("Follower", foreign_keys="Follower.user_from_ID", back_populates="following_user")

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)  # Agregamos un ID único para la tabla intermedia
    user_from_ID = Column(Integer, ForeignKey('user.id'), nullable=False)  
    user_to_ID = Column(Integer, ForeignKey('user.id'), nullable=False)
    following_user = relationship("User", foreign_keys=[user_from_ID], back_populates="following")
    followed_user = relationship("User", foreign_keys=[user_to_ID], back_populates="followers")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship("Post", back_populates="media")

    def to_dict(self):
        return {}

# Generar el diagrama
try:
    render_er(Base, 'diagram.png')
    print("¡Éxito! Revisa el archivo diagram.png")
except Exception as e:
    print("Hubo un problema generando el diagrama:")
    raise e
