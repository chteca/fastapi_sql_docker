from datetime import datetime
from models import Base, Comment, Post
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database import create_all_tables, get_async_session
import random

num_posts = 10
num_comments = 20

def main():
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(num_posts):
        content = f'Контент статьи {i+1}'
        title = f'Статья {i+1}'
        post = Post(title=title, content=content)
        session.add(post)
    session.commit()

    for _ in range(num_comments):
        comment_text = f'Комментарий {_+1}'
        post = session.query(Post).order_by(func.random()).first()
        comment = Comment(post=post, content=comment_text)
        session.add(comment)
    session.commit()


if __name__ == "__main__":
    DATABASE_URL = "sqlite:///sqlalchemy.db"
    engine = create_engine(DATABASE_URL)
    main()

