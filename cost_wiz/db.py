from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from cost_wiz.config.settings import env

engine = create_engine(env.get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    access_key = Column(String)
    secret_key = Column(String)
    region = Column(String)
    session_key = Column(String)

    has_account_setup = Column(Boolean)


class Instance(Base):
    __tablename__ = "instance"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    instance_id = Column(String)
    instance_type = Column(String)
    cpu = Column(String)
    ram = Column(String)
    status = Column(String)
    hourly_rate = Column(Float)

    account_id = Column(Integer, ForeignKey("account.id"))


class InstanceStat(Base):

    __tablename__ = "instance_stats"

    id = Column(Integer, primary_key=True)
    instance_id = Column(String)

    mem_used_percent_max = Column(Float)
    cpu_usage_user_max = Column(Float)

    cpu_usage_iowait_max = Column(Float)
    cpu_usage_idle_max = Column(Float)
    cpu_usage_system_max = Column(Float)
    diskio_reads_max = Column(Float)

    disk_used_percent_max = Column(Float)
    swap_used_percent_max = Column(Float)

    mem_used_percent_min = Column(Float)
    cpu_usage_user_min = Column(Float)

    cpu_usage_iowait_min = Column(Float)
    cpu_usage_idle_min = Column(Float)
    cpu_usage_system_min = Column(Float)
    diskio_reads_min = Column(Float)

    disk_used_percent_min = Column(Float)
    swap_used_percent_min = Column(Float)

    timestamp = Column(DateTime)


class Recommendation(Base):

    __tablename__ = "recommendation"

    id = Column(Integer, primary_key=True)

    current_instance = Column(Integer, ForeignKey("instance.id"))

    sug_1_instance_type = Column(String)
    sug_1_reason = Column(String)
    sug_1_cost_per_hour = Column(Float)
    sug_1_diff_cost_per_hour = Column(Float)

    sug_2_instance_type = Column(String)
    sug_2_reason = Column(String)
    sug_2_cost_per_hour = Column(Float)
    sug_2_diff_cost_per_hour = Column(Float)

    account_id = Column(Integer, ForeignKey("account.id"))
