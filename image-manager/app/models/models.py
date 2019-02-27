# coding:utf8

from datetime import datetime
from app import db
from app.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False, comment=u'类别名称')
    create_time = db.Column(db.DateTime, default=datetime.now, comment=u'创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment=u'更新时间')


class Image(BaseModel):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(60), nullable=False, comment=u'图片名称')
    image_src = db.Column(db.String(120), nullable=False, comment=u'图片地址')
    category_id = db.Column(db.Integer, nullable=True, default=0, comment=u'类别ID')
    is_deleted = db.Column(db.Boolean, nullable=True, default=False, comment=u'删除标志')
    create_time = db.Column(db.DateTime, default=datetime.now, comment=u'创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment=u'更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'image_src': 'http://192.168.1.211:5001/'+self.image_src,
            'category_id': self.category_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class Recommendation(BaseModel):
    __tablename__ = 'recommendation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False, comment=u'标题')
    description = db.Column(db.Text, nullable=False, comment=u'描述')
    recommend_date = db.Column(db.DateTime, nullable=False, comment=u'推荐日期')
    is_deleted = db.Column(db.Boolean, nullable=True, default=False, comment=u'删除标志')
    create_time = db.Column(db.DateTime, default=datetime.now, comment=u'创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment=u'更新时间')

    def get_images(self):
        images = Image.query.join(RecommendationImageRelation, RecommendationImageRelation.image_id == Image.id).filter(
            RecommendationImageRelation.recommendation_id == self.id,
            Image.is_deleted == False
        )
        return images


class RecommendationImageRelation(BaseModel):
    __tablename__ = 'recommendation_image_relation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recommendation_id = db.Column(db.Integer, nullable=False, comment=u'推荐ID')
    image_id = db.Column(db.Integer, nullable=False, comment=u'图片ID')
    create_time = db.Column(db.DateTime, default=datetime.now, comment=u'创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment=u'更新时间')
