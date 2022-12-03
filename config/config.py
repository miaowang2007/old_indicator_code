# -*- coding: utf-8 -*-
import configparser
import os

import sys

config_file = 'app.conf'
stock_list_file = 'stock_lists.txt'


def get_config_dir(home_dir):
    # current_dir = sys.path[0]
    # home_dir = current_dir[0:current_dir.rfind(os.sep)]
    return home_dir + os.sep + 'config' + os.sep


def load_db_config(home_dir):
    """
    获取DB连接配置信息
    :return:
    """
    cp = configparser.ConfigParser()
    cp.read(get_config_dir(home_dir) + config_file)

    return {
        'host': cp.get('db', 'host'),
        'port': cp.get('db', 'port'),
        'database': cp.get('db', 'database'),
        'user': cp.get('db', 'user'),
        'password': cp.get('db', 'pass'),
        'charset': cp.get('db', 'charset'),
        'connect_url': cp.get('db', 'connect_url'),
        'use_unicode': True,
        'get_warnings': True,
    }


def load_system_config(home_dir):
    """
    配置系统信息
    :return:
    """
    cp = configparser.ConfigParser()
    cp.read(get_config_dir(home_dir) + config_file)
    return {
        'stock_points': cp.get('system', 'stock_points'),
        'log_path': cp.get('system', 'log_path'),
    }


def load_email_config(home_dir):
    cp = configparser.ConfigParser()
    cp.read(get_config_dir(home_dir) + config_file)
    return {
        'smtp.server': cp.get('email', 'smtp.server'),
        'port': cp.get('email', 'port'),
        'user': cp.get('email', 'user'),
        'password': cp.get('email', 'password'),
        'sender': cp.get('email', 'sender'),
        'reveiver': cp.get('email', 'reveiver'),
        'subject': cp.get('email', 'subject'),
    }


def read_stock_lists(home_dir):

    stock_lists = get_config_dir(home_dir) + stock_list_file
    f = open(stock_lists, "r")
    print('load stock list file:' + stock_lists)
    file_data = []
    line = f.readline()
    while line:
        file_data.append(line)
        line = f.readline()
    f.close()
    return file_data
