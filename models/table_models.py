from sqlalchemy.orm import declarative_base, relationship
import sqlalchemy.dialects.postgresql as pg_type
from sqlalchemy import Column, ForeignKey, Table

Base = declarative_base()


# joining tables
service_master_table = Table('service_master', Base.metadata,
                             Column('service', ForeignKey("service.service_id")),
                             Column('master', ForeignKey("master.master_id")))

schedule_master_table = Table('schedule_master', Base.metadata,
                              Column('time', ForeignKey("schedule.schedule_id")),
                              Column('master', ForeignKey("master.master_id")),
                              Column('is_free', pg_type.BOOLEAN(), default=True))


class Service(Base):
    __tablename__ = "service"
    service_id = Column(pg_type.INTEGER(), primary_key=True)
    service_name = Column(pg_type.VARCHAR(length=64), nullable=False)
    price = Column(pg_type.MONEY(), nullable=False)
    service_master = relationship("Master", secondary=service_master_table)
    service_order = relationship("Order")


class Master(Base):
    __tablename__ = "master"
    master_id = Column(pg_type.INTEGER(), primary_key=True)
    master_name = Column(pg_type.VARCHAR(length=64), nullable=False)
    master_schedule = relationship('Schedule', secondary=schedule_master_table)
    master_order = relationship("Order", backref="master")


class Schedule(Base):
    __tablename__ = "schedule"
    schedule_id = Column(pg_type.INTEGER(), primary_key=True)
    schedule_time = Column(pg_type.TIMESTAMP(), nullable=False)
    schedule_order = relationship("Order", backref="schedule")


class Client(Base):
    __tablename__ = "client"
    client_id = Column(pg_type.INTEGER(), primary_key=True)
    client_name = Column(pg_type.VARCHAR(length=128), nullable=False)
    client_tel = Column(pg_type.VARCHAR(length=15), nullable=False)
    is_regular = Column(pg_type.BOOLEAN(), default=False)
    client_order = relationship("Order", backref="client")


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(pg_type.INTEGER(), primary_key=True)
    order_service = Column(pg_type.INTEGER(), ForeignKey('service.service_id'))
    order_client = Column(pg_type.INTEGER(), ForeignKey('client.client_id'))
    order_master = Column(pg_type.INTEGER(), ForeignKey('master.master_id'))
    order_time = Column(pg_type.INTEGER(), ForeignKey('schedule.schedule_id'))
