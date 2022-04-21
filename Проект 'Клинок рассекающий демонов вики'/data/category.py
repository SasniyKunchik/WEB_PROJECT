import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('hashiras', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('hashiras.id')),
    sqlalchemy.Column('demons', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('demons.id')),
    sqlalchemy.Column('others', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('others.id')),
    sqlalchemy.Column('suzhet', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('suzhet.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('category.id'))
)


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)