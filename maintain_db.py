# SQL用
import sqlite3

# 時間の取得用
from datetime import datetime

class MaintainDB:
  # コンストラクタ
  def __init__(self, _dbpath):
    self.dbpath = _dbpath

  # 挿入 
  # データインプット
  def command(self,sql_sentense):
    connection = sqlite3.connect(self.dbpath)
    cursor = connection.cursor()

    try:
      # tableの作成(パーツリスト)
      cursor.execute('CREATE TABLE IF NOT EXISTS partslist(id integer, type integer, name text, package text, stock integer, date text)')
      
      cursor.execute(sql_sentense)
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])
      return False
    
    # 保存を実行（忘れると保存されないので注意）
    connection.commit()
    # コネクションを閉じる
    connection.close()
    return True

  def receiveCommand(self,sql_sentense):
    connection = sqlite3.connect(self.dbpath)
    cursor = connection.cursor()

    out_str = []

    try:
      # tableの作成(パーツリスト)
      cursor.execute('CREATE TABLE IF NOT EXISTS partslist(id integer, type integer, name text, package text, stock integer, date text)')
      
      cursor.execute(sql_sentense)
      out_str = cursor.fetchall()
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])
      return out_str
  
    # 保存を実行（忘れると保存されないので注意）
    connection.commit()
    # コネクションを閉じる
    connection.close()
    return out_str

  def getAllData(self):
    connection = sqlite3.connect(self.dbpath)
    cursor = connection.cursor()
    data_list = []
    
    try:
      cursor.execute('SELECT * FROM  partslist')
      data_list = cursor.fetchall()

    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])
      return False

    # コネクションを閉じる
    connection.close()
    return data_list

def getInsertPartListSentense(_id, _type, _name, _package, _stock):
  p_id = str(_id) + ","
  p_type = str(_type) + ","
  p_name =  '"' + _name + '"' + ","
  p_package = '"' + _package + '"' + ","
  p_stock = str(_stock) + ","

  # 現在の時間を取得
  date_str = '"' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '"'
  order_str = 'INSERT INTO partslist VALUES(' + p_id + p_type + p_name + p_package + p_stock + date_str + ')'
  return order_str

def getDeletePartListSentense(_id):
  order_str = "DELETE FROM partslist WHERE id =" + str(_id)
  return order_str

def getSearchNamePartListSEntense(_name):
  order_str = "SELECT * FROM partslist WHERE name like '%" + _name + "%'"
  return order_str

def getSearchPackagePartListSEntense(_package):
  order_str = "SELECT * FROM partslist WHERE package like '%" + _package + "%'"
  return order_str

def getSearchIDPartListSEntense(_id):
  order_str = "SELECT * FROM partslist WHERE id =" + str(_id)
  return order_str

def getUpdatePartListSEntense(_id, _type, _name, _package, _stock):
  p_id = str(_id) + ","
  p_type = "type =" + str(_type) + ","
  p_name =  "name =" + '"' + _name + '"' + ","
  p_package = 'package="' + _package + '"' + ","
  p_stock = 'stock=' + str(_stock) + ","

  # 現在の時間を取得
  date_str = 'date ="' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '"'
  order_str = 'UPDATE partslist SET ' + p_type + p_name + p_package + p_stock + date_str + " WHERE id = " + str(_id) + ";"
  return order_str