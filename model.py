from sqlalchemy import Column, Integer, VARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, TEXT, LONGTEXT

Base = declarative_base()


class Posts(Base):
    __tablename__ = 'wp_posts'
    ID = Column(BIGINT(20), primary_key=True)
    post_author = Column(BIGINT(20))
    post_date = Column(DateTime)
    post_date_gmt = Column(DateTime)
    post_content = Column(LONGTEXT)
    post_title = Column(TEXT)
    post_excerpt = Column(TEXT)
    post_status = Column(VARCHAR(20))
    comment_status = Column(VARCHAR(20))
    ping_status = Column(VARCHAR(20))
    post_password = Column(VARCHAR(255))
    post_name = Column(VARCHAR(200))
    to_ping = Column(TEXT)
    pinged = Column(TEXT)
    post_modified = Column(DateTime)
    post_modified_gmt = Column(DateTime)
    post_content_filtered = Column(LONGTEXT)
    post_parent = Column(BIGINT(20))
    guid = Column(VARCHAR(255))
    menu_order = Column(Integer(11))
    post_type = Column(VARCHAR(20))
    post_mime_type = Column(VARCHAR(100))
    comment_count = Column(BIGINT(20))