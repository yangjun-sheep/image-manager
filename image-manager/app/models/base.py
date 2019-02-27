# coding:utf8

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def bulk_create(self):
        db.session.add_all(self)
        db.session.commit()

    def to_dict(self):
        useless_columns = [
            'password',
            'is_deleted',
        ]
        datetime_columns = [
            'create_time',
            'update_time',
            'recommend_date',
        ]
        data = {}
        for c in self.__table__.columns:
            value = None
            if c.name in useless_columns:
                continue
            elif c.name in datetime_columns:
                value = getattr(self, c.name)
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                value = getattr(self, c.name)
            data[c.name] = value
        return data

    def delete(self):
        db.session.delete(self)
        db.session.commit()
