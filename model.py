from sqlalchemy import Column, INTEGER, VARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, TEXT, LONGTEXT

Base = declarative_base()


class Posts(Base):
    __tablename__ = 'wp_posts'
    ID = Column(BIGINT(20), primary_key=True)
    post_author = Column(BIGINT(20), default=5)
    post_date = Column(DateTime)
    post_date_gmt = Column(DateTime)
    post_content = Column(LONGTEXT)
    post_title = Column(TEXT)
    post_excerpt = Column(TEXT, default='')
    post_status = Column(VARCHAR(20), default='publish')
    comment_status = Column(VARCHAR(20), default='closed')
    ping_status = Column(VARCHAR(20), default='closed')
    post_password = Column(VARCHAR(255), default='')
    post_name = Column(VARCHAR(200))
    to_ping = Column(TEXT, default='')
    pinged = Column(TEXT, default='')
    post_modified = Column(DateTime)
    post_modified_gmt = Column(DateTime)
    post_content_filtered = Column(LONGTEXT, default='')
    post_parent = Column(BIGINT(20), default=0)
    guid = Column(VARCHAR(255))
    menu_order = Column(INTEGER, default=0)
    post_type = Column(VARCHAR(20), default='post')
    post_mime_type = Column(VARCHAR(100), default='')
    comment_count = Column(BIGINT(20), default=0)
