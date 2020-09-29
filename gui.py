# tkinter モジュールのインポート
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import messagebox

# データベースアクセスクラスの読み込み
import maintain_db

class Application(ttk.Frame):

  def __init__(self, master = None):
    tk.Frame.__init__(self, master)

    self.search_window = None
    self.insert_window = None
    self.delete_window = None
    self.update_window = None
    
    self.pack()
    dbpath = './electronic_parts.db'
    self.db = maintain_db.MaintainDB(dbpath)
    self.init()
    self.createTree()

  def init(self):
    ttk.Button(self,text="再読み込み", command =self.reload).grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    ttk.Button(self,text="検索", command =self.search).grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    ttk.Button(self,text="入力", command =self.insert).grid(column=2, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    ttk.Button(self,text="変更", command =self.update).grid(column=3, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    ttk.Button(self,text="削除", command =self.delete).grid(column=4, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Frame自身もトップレベルウィジェットに配置
    self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    
    # 各列の引き伸ばし設定
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)
    self.columnconfigure(3, weight=1)
    self.columnconfigure(4, weight=1)

    # 各行の引き伸ばし設定
    self.rowconfigure(0, weight=0)
    self.rowconfigure(1, weight=1)

    # トップレベルのウィジェットも引き伸ばしに対応させる
    self.master.columnconfigure(0, weight=1)
    self.master.rowconfigure(0, weight=1)

  def createTree(self):
    self.tree = ttk.Treeview(self)
    # 各列の設定(インデックス,オプション(今回は幅を指定))
    # 列インデックスの作成
    self.tree["columns"] = (1,2,3,4,5,6)
    # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
    self.tree["show"] = "headings"
    self.tree.column(1,width=75)
    self.tree.column(2,width=150)
    self.tree.column(3,width=150)
    self.tree.column(4,width=150)
    self.tree.column(5,width=100)
    self.tree.column(6,width=250)
    # 各列のヘッダー設定(インデックス,テキスト)
    self.tree.heading(1,text="id")
    self.tree.heading(2,text="type")
    self.tree.heading(3,text="name")
    self.tree.heading(4,text="package")
    self.tree.heading(5,text="stock")
    self.tree.heading(6,text="update date")

    #self.tree.insert("","end",values=(1, 0, "MPU6500", "QFN24_3*3", 20,"today"))

    # treeを作るときに初期化
    self.id_counter = 0
    
    # データベースのデータを読み込んで表に書き出し
    data_list = []
    data_list = self.db.getAllData()
    for data in data_list:
      self.tree.insert("","end",values=(data[0], data[1], data[2], data[3], data[4], data[5]))
      self.id_counter += 1 

    #print(self.id_counter) 

    self.tree.grid(column=0, row=1, columnspan=5, sticky=(tk.N, tk.S, tk.E, tk.W))

  # ボタンが押されたときの関数
  def createListTree(self, data_list):
    self.tree = ttk.Treeview(self)
    # 各列の設定(インデックス,オプション(今回は幅を指定))
    # 列インデックスの作成
    self.tree["columns"] = (1,2,3,4,5,6)
    # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
    self.tree["show"] = "headings"
    self.tree.column(1,width=75)
    self.tree.column(2,width=150)
    self.tree.column(3,width=150)
    self.tree.column(4,width=150)
    self.tree.column(5,width=100)
    self.tree.column(6,width=250)
    # 各列のヘッダー設定(インデックス,テキスト)
    self.tree.heading(1,text="id")
    self.tree.heading(2,text="type")
    self.tree.heading(3,text="name")
    self.tree.heading(4,text="package")
    self.tree.heading(5,text="stock")
    self.tree.heading(6,text="update date")

    #self.tree.insert("","end",values=(1, 0, "MPU6500", "QFN24_3*3", 20,"today"))

    # データベースのデータを読み込んで表に書き出し
    for data in data_list:
      self.tree.insert("","end",values=(data[0], data[1], data[2], data[3], data[4], data[5]))

    self.tree.grid(column=0, row=1, columnspan=5, sticky=(tk.N, tk.S, tk.E, tk.W))

  # 再読み込み
  def reload(self):
    self.grid_forget()
    self.init()
    self.createTree()

  def search(self):
    if not self.search_window:
      self.search_window = tk.Toplevel(self)
      self.search_window.title("Search")
      self.search_window.resizable(0,0)

      font_label = tk.font.Font(family='Times', size=20)

      ttk.Label(self.search_window,text="serarch DB", font=font_label).grid(column=0, row=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.search_entry = ttk.Entry(self.search_window, font=font_label)
      self.search_entry.grid(column=0, row=1, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.search_window, text="name検索", command=self.searchName).grid(column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.search_window, text="package検索", command=self.searcPackage).grid(column=1, row=2,sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.search_window, text="quit", command=self.destorySearchWindow).grid(column=1, row=3,sticky=(tk.N, tk.S, tk.E, tk.W) )

  def destorySearchWindow(self):
    self.search_window.destroy()
    self.search_window = None

  def searchName(self):
    data_list = []
    entry_str = self.search_entry.get()

    if entry_str == "":
      messagebox.showerror("error", "There is no search word data")
    
    order_str = maintain_db.getSearchNamePartListSEntense(entry_str)
    data_list = self.db.receiveCommand(order_str)

    if not data_list:
      messagebox.showerror("error", "There is no search word data")
      return False
    else:
      messagebox.showinfo("Success", "Show tree data")
    
    self.grid_forget()
    self.init()
    self.createListTree(data_list)
    return True

  def searcPackage(self):
    data_list = []
    entry_str = self.search_entry.get()
    order_str = maintain_db.getSearchPackagePartListSEntense(entry_str)
    data_list = self.db.receiveCommand(order_str)

    if not data_list:
      messagebox.showerror("error", "There is no search word data")
      return False
    else:
      messagebox.showinfo("Success", "Check the table")
    
    self.grid_forget()
    self.init()
    self.createListTree(data_list)
    return True

  def insert(self):
    if not self.insert_window:
      self.insert_window = tk.Toplevel(self)
      self.insert_window.title("Insert")
      self.insert_window.resizable(0,0)

      font_label = tk.font.Font(family='Times', size=20)

      ttk.Label(self.insert_window,text="Insert DB", font=font_label).grid(column=0, row=0, columnspan=6, sticky=(tk.N, tk.S, tk.E, tk.W)) 

      font_label = tk.font.Font(family='Times', size=10)

      ttk.Label(self.insert_window,text="id(int)", font=font_label).grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.insert_window,text="type(int)", font=font_label).grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.insert_window,text="name(str)", font=font_label).grid(column=2, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.insert_window,text="package(str)", font=font_label).grid(column=0, row=3, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.insert_window,text="stock(int)", font=font_label).grid(column=1, row=3, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      
      self.insert_entry = []
      self.insert_entry.append(ttk.Entry(self.insert_window, font=font_label))
      self.insert_entry.append(ttk.Entry(self.insert_window, font=font_label))
      self.insert_entry.append(ttk.Entry(self.insert_window, font=font_label))
      self.insert_entry.append(ttk.Entry(self.insert_window, font=font_label))
      self.insert_entry.append(ttk.Entry(self.insert_window, font=font_label))
      self.insert_entry[0].insert(tk.END, str(self.id_counter+1))
      self.insert_entry[0].configure(state='disabled')
      self.insert_entry[0].grid(column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.insert_entry[1].grid(column=1, row=2, sticky=(tk.N, tk.S, tk.E, tk.W))
      self.insert_entry[2].grid(column=2, row=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.insert_entry[3].grid(column=0, row=4, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.insert_entry[4].grid(column=1, row=4, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      
      ttk.Button(self.insert_window, text="DBに入力", command=self.insertProcess).grid(column=0, row=5, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.insert_window, text="クリア", command=self.clearInsertEntry).grid(column=1, row=5, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.insert_window, text="quit", command=self.destroyInsertWindow).grid(column=2, row=6,sticky=(tk.N, tk.S, tk.E, tk.W) )

  def destroyInsertWindow(self):
    self.insert_window.destroy()
    self.insert_window = None

  def clearInsertEntry(self):
    self.insert_entry[1].delete(0, tk.END)
    self.insert_entry[2].delete(0, tk.END)
    self.insert_entry[3].delete(0, tk.END)
    self.insert_entry[4].delete(0, tk.END)

  def insertProcess(self):
    error = False
    type_str = self.insert_entry[1].get()
    if not type_str.isdecimal():
      error = True
    name_str = self.insert_entry[2].get()
    package_str = self.insert_entry[3].get()
    stock_str = self.insert_entry[4].get()
    if not stock_str.isdecimal():
      error = True

    if not error:
      messagebox.showinfo("Success", "Check the table")
      self.id_counter = int(self.insert_entry[0].get())
      order_str = maintain_db.getInsertPartListSentense(self.id_counter, type_str, name_str, package_str, stock_str)
      self.db.command(order_str)
      self.clearInsertEntry()
      self.insert_entry[0].configure(state='normal')
      self.insert_entry[0].delete(0, tk.END)
      self.insert_entry[0].insert(tk.END, str(self.id_counter+1))
      self.insert_entry[0].configure(state='disabled')
      self.grid_forget()
      self.init()
      self.createTree()
      return True
    else:
      messagebox.showerror("error", "There is no search word data")
      return False

  def delete(self):
    if not self.delete_window:
      self.delete_window = tk.Toplevel(self)
      self.delete_window.title("Delete")
      self.delete_window.resizable(0,0)

      font_label = tk.font.Font(family='Times', size=20)

      ttk.Label(self.delete_window,text="delete DB", font=font_label).grid(column=0, row=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.delete_window,text="input delete id", font=font_label).grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.delete_entry = ttk.Entry(self.delete_window, font=font_label)
      self.delete_entry.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.delete_window, text="delete", command=self.deleteProcess).grid(column=0, row=2,sticky=(tk.N, tk.S, tk.E, tk.W) )
      ttk.Button(self.delete_window, text="quit", command=self.destroyDeleteWindow).grid(column=1, row=3,sticky=(tk.N, tk.S, tk.E, tk.W) )

  def destroyDeleteWindow(self):
    self.delete_window.destroy()
    self.delete_window = None

  def deleteProcess(self):
    res = messagebox.askokcancel("Confirmation", "Do you really want to delete this?")
    if res:
      id_str = self.delete_entry.get()
      if not id_str.isdecimal():
        messagebox.showerror("error", "Id is wrong")
        return False
      else:
        # データがあるかどうかのチェック
        order_str = maintain_db.getSearchIDPartListSEntense(id_str)
        data = self.db.receiveCommand(order_str)
        if not data:
          messagebox.showerror("error", "select id is not exist")
          return False
        
        messagebox.showinfo("success", "Success delete")
        order_str = maintain_db.getDeletePartListSentense(id_str)
        self.db.command(order_str)
        self.delete_entry.delete(0, tk.END)
        self.grid_forget()
        self.init()
        self.createTree()
        return True

    else:
      messagebox.showinfo("Cancel", "You canncel delete process")
      return False

  def update(self):
    if not self.update_window:
      self.update_window = tk.Toplevel(self)
      self.update_window.title("Update")
      self.update_window.resizable(0,0)

      font_label = tk.font.Font(family='Times', size=20)

      ttk.Label(self.update_window,text="Update DB", font=font_label).grid(column=0, row=0, columnspan=6, sticky=(tk.N, tk.S, tk.E, tk.W)) 

      font_label = tk.font.Font(family='Times', size=10)

      ttk.Label(self.update_window,text="id(int)", font=font_label).grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.update_window,text="type(int)", font=font_label).grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.update_window,text="name(str)", font=font_label).grid(column=2, row=1, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.update_window,text="package(str)", font=font_label).grid(column=0, row=3, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Label(self.update_window,text="stock(int)", font=font_label).grid(column=1, row=3, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      
      self.update_entry = []
      self.update_entry.append(ttk.Entry(self.update_window, font=font_label))
      self.update_entry.append(ttk.Entry(self.update_window, font=font_label))
      self.update_entry.append(ttk.Entry(self.update_window, font=font_label))
      self.update_entry.append(ttk.Entry(self.update_window, font=font_label))
      self.update_entry.append(ttk.Entry(self.update_window, font=font_label))
      self.update_entry[0].grid(column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.update_entry[1].grid(column=1, row=2, sticky=(tk.N, tk.S, tk.E, tk.W))
      self.update_entry[2].grid(column=2, row=2, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.update_entry[3].grid(column=0, row=4, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      self.update_entry[4].grid(column=1, row=4, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      
      ttk.Button(self.update_window, text="IDのデータを取得", command=self.setElemetToUpdateEntry).grid(column=0, row=5, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.update_window, text="クリア", command=self.clearUpdateEntry).grid(column=2, row=5, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.update_window, text="DBを更新", command=self.updateProcess).grid(column=0, row=7, sticky=(tk.N, tk.S, tk.E, tk.W)) 
      ttk.Button(self.update_window, text="quit", command=self.destroyUpdateWindow).grid(column=2, row=8,sticky=(tk.N, tk.S, tk.E, tk.W) )

  def destroyUpdateWindow(self):
    self.update_window.destroy()
    self.update_window = None

  def clearUpdateEntry(self):
    self.update_entry[0].delete(0, tk.END)
    self.update_entry[1].delete(0, tk.END)
    self.update_entry[2].delete(0, tk.END)
    self.update_entry[3].delete(0, tk.END)
    self.update_entry[4].delete(0, tk.END)

  def setElemetToUpdateEntry(self):
    id_str = self.update_entry[0].get()
    if not id_str.isdecimal():
      messagebox.showerror("error", "ID is not number")
      return False
    
    # データがあるかどうかのチェック
    order_str = maintain_db.getSearchIDPartListSEntense(id_str)
    data_list = self.db.receiveCommand(order_str)
    if not data_list:
      messagebox.showerror("error", "select id is not exist")
      return False 
    else:
      for data in data_list:
        self.clearUpdateEntry()
        self.update_entry[0].insert(tk.END, data[0])
        self.update_entry[1].insert(tk.END, data[1])
        self.update_entry[2].insert(tk.END, data[2])
        self.update_entry[3].insert(tk.END, data[3])
        self.update_entry[4].insert(tk.END, data[4])
      return True

  def updateProcess(self):
    error = False
    id_str = self.update_entry[0].get()
    if not id_str.isdecimal():
      error = True
    type_str = self.update_entry[1].get()
    if not type_str.isdecimal():
      error = True
    name_str = self.update_entry[2].get()
    package_str = self.update_entry[3].get()
    stock_str = self.update_entry[4].get()
    if not stock_str.isdecimal():
      error = True

    if error:
      messagebox.showerror("error", "Update data is wrong")
      return False

    res = messagebox.askokcancel("Confirmation", "Do you really want to update this?")

    if res:      
      # データがあるかどうかのチェック
      order_str = maintain_db.getSearchIDPartListSEntense(id_str)
      data = self.db.receiveCommand(order_str)
      if not data:
        messagebox.showerror("error", "select id is not exist")
        return False
        
      messagebox.showinfo("success", "Success update")
      order_str = maintain_db.getUpdatePartListSEntense(id_str, type_str, name_str, package_str, stock_str)
      self.db.command(order_str)
      self.clearUpdateEntry()
      self.grid_forget()
      self.init()
      self.createTree()
      return True

    else:
      messagebox.showinfo("Cancel", "You canncel delete process")
      return False

