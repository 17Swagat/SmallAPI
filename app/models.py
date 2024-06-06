from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column("post_id", Integer, primary_key=True, nullable=False)
    title = Column(name="post_title", type_=String(50), nullable=False)
    content = Column("post_content", String(100), nullable=False)
    published = Column("post_published", Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('NOW()'))
