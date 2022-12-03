# 数据库相关操作

# -*- coding: utf-8 -*-
import os
import pandas as pd
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

from store.entity import HistData5, HistDataD, HistDataW, HistDataM, HistData15, HistData30, HistData60
from config import config

current_dir = sys.path[0]
db_config = config.load_db_config(current_dir)
engine = create_engine(db_config.get('connect_url'))

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()


def insert(base):
    """
    插入数据
    :param base:
    :return:
    """
    session.add(base)
    session.flush()
    session.commit()


# 查询
def query_hist_data_5(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistData5).order_by(desc(HistData5.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]


def query_hist_data_d(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistDataD).order_by(desc(HistDataD.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]


def query_hist_data_w(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistDataW).order_by(desc(HistDataW.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]


def query_hist_data_m(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistDataM).order_by(desc(HistDataM.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]


def query_hist_data_15(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistData15).order_by(desc(HistData15.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]


def query_hist_data_30(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistData30).order_by(desc(HistData30.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]


def query_hist_data_60(older=0):
    older = int(older)
    session.begin(subtransactions=True)
    hist = session.query(HistData60).order_by(desc(HistData60.date))[older:older + 1]
    if len(hist) == 0:
        return None
    # session.close()
    return hist[0]
