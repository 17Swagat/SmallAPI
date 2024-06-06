from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime


class Post(Base):
    __tablename__ = "posts"

    id = Column("post_id", Integer, primary_key=True, nullable=False)
    title = Column(name="post_title", type_=String(50), nullable=False)
    content = Column("post_content", String(100), nullable=False)
    published = Column("post_published", Boolean, default= True, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), nullable=False)
