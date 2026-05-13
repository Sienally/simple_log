import os
import sqlite3
import sys
import time
import base64


# 图片转码函数
def img_to_base64(file_path):
    with open(file_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
        return img_data



class LOG:

    def __init__(self, **argument):

        # 重要常量

        # argument = {account, password, time_info, second_password}
        self.argument = argument
        
        # 安全获取参数, 如果不存在该参数则默认为空字符串
        self.account = self.argument.get("account", "")
        self.password = self.argument.get("password", "")
        self.time_info = self.argument.get("time_info", "")
        self.second_password = self.argument.get("second_password", "")

        self.log_in_name = None


        self.sqlite_file = os.path.join(os.getcwd(), "./data_file/a&p_data.db")

        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

        # self.cur.execute("drop table user_info")
        # self.conn.commit()
        # self.cur.execute("drop table last_login_time")
        # self.conn.commit()
        
        # 账号-密码 信息存储表
        self.cur.execute("""
                    create table if not exists user_info(
                        account text primary key,
                        name text not null,
                        password text not null,
                        identity text not null,
                        sign_up_time text not null,
                        second_password text
                    );
                    """)
        self.conn.commit()
        

        # 登录日志表
        self.cur.execute("""
                    create table if not exists last_login_time(
                        account text not null,
                        last_login_time text not null);
                    """)
        self.conn.commit()
        
        

        # 始终存管理员账号信息表

        # 管理员第一次注册时间
        admin_sign_up_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if self.cur.execute(f"select account from user_info where account = 'admin111'; ").fetchone() is None:
            self.cur.execute(f"insert into user_info values (?, ?, ?, ?, ?, ?);", ('admin111', '管理员', '11111111', 'administer', admin_sign_up_time, "YZA"))
            self.conn.commit()



        print("用户信息表: ", self.cur.execute("select * from user_info").fetchall(), "\n")
        print("上次登录时间: ", self.cur.execute("select * from last_login_time").fetchall(), "\n")



        self.conn.close()

        # 以上为初始化操作
        # 以下为账号-密码审核操作
        

        # self.is_true_account_statues = {-1:"账号不存在", 0:"账号格式错误", 1:"账号正确"}
        # self.is_true_password_statues = {-1:"密码错误", 0:"密码格式错误", 1:"密码正确"}
        self.is_true_account_statues = self.is_true_account()
        self.is_true_password_statues = self.is_true_password()



    # 判断账号
    def is_true_account(self):
            
        # 连接数据库
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()
        all_accounts = self.cur.execute("select account from user_info;").fetchall()
        self.conn.close()
            
        if len(self.account) < 11:
            
            # 管理员账号是特殊情况
            if self.account == "admin111":
                return 1

            # 格式错误返回0
            return 0
        
        elif (self.account,) not in all_accounts:
            # 账号不存在返回-1
            return -1

        else: 
            return 1
        

    # 判断密码
    def is_true_password(self):

        # 连接数据库
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()
        only_password = self.cur.execute("select password from user_info where account = ?; ", (self.account,)).fetchone()
        self.conn.close()

        # 账号正确情况下进行判断    
        if self.is_true_account_statues == 1:
        
            if len(self.password) < 6 or len(self.password) > 15:
                # 密码格式错误返回0
                return 0
        
            elif self.password != only_password[0]:
                # 密码错误返回-1
                return -1
        
            else: 
                # 每次登录都往里插登陆时间数据

                # 插数据
                self.conn = sqlite3.connect(self.sqlite_file)
                self.cur = self.conn.cursor()
                self.cur.execute("insert into last_login_time values (?,?)", (self.account, self.time_info))
                self.conn.commit()

                self.log_in_name = self.cur.execute("select name from user_info where account = ?;", (self.account, )).fetchone()[0]
                self.conn.close()
                # 密码正确, 返回1
                return 1
        
    # 注册
    def sign_up(self):

        # argument = {sign_up_account, sign_up_password, sign_up_name, sign_up_time_info, sign_up_second_password}
        
        self.sign_up_account = self.argument["account"]
        self.sign_up_password = self.argument["password"]
        self.sign_up_name = self.argument["sign_up_name"]
        self.sign_up_time_info = self.argument["time_info"]
        self.sign_up_second_password = self.argument["second_password"]
        
        # 判断账号格式
        if len(self.account) < 11:
            # 账号格式错误
            return 0
        
        else:
            # 账号格式正确
            
            # 该账号已存在
            conn = sqlite3.connect(self.sqlite_file)
            cur = conn.cursor()
            target_account = cur.execute("select account from user_info where account = ?", (self.account,)).fetchone()
            conn.commit()
            conn.close()
            if target_account is not None:
                return -2

            # 密码格式错误
            else:
                if len(self.password) < 6 or len(self.password) > 15:
                    return -1
            
                else:
                    # 密码格式正确

                    # 连接数据库
                    conn = sqlite3.connect(self.sqlite_file)
                    cur = conn.cursor()
                    cur.execute("insert into user_info values (?, ?, ?, ?, ?, ?)", (self.sign_up_account, self.sign_up_name, self.sign_up_password, "user", self.sign_up_time_info, self.sign_up_second_password))
                    conn.commit()
                    conn.close()

                    return 1
                
                
                
    def visitor_login(self):
        # 游客登陆异常
        if self.account != "visitor111" and self.password != "111":
            return 0
        
        # 正常登录

        # 插入游客登录数据
        conn = sqlite3.connect(self.sqlite_file)
        cur = conn.cursor()
        cur.execute("insert into last_login_time values (?, ?)", (self.account, self.time_info))
        conn.commit()
        conn.close()
        return 1
    

    # 保存想要自动登录的账号密码信息   
    def save_password(self, account, password):
        
        # 连接数据库
            conn = sqlite3.connect("data_file/a&p_data.db")
            cur = conn.cursor()


            # cur.execute("drop table if exists local_user_password_info")
            # conn.commit()


            # 创表
            cur.execute("""
                        create table if not exists local_user_password_info(
                            account text primary key,
                            password text not null
                        )
                        """)
            conn.commit()
            
            # 如果表里没有该账号数据, 允许插入
            if cur.execute("select * from local_user_password_info where account = ?; ", (account, )) is None:
                    
                # 插数据
                cur.execute("insert into local_user_password_info values (?, ?, ?); ", (account, password))
                conn.commit()
                conn.close()         


    # 自动填充账号
    def auto_account(self):
        conn = sqlite3.connect("data_file/a&p_data.db")
        cur = conn.cursor()

        # 以防刚开始没表, 先创表
        cur.execute("""
                    create table if not exists local_user_password_info(
                        account text primary key,
                        password text not null
                    )
                    """)
        conn.commit()

        # 查信息总表的所有账号数据
        if cur.execute("select account from user_info where account != 'visitor111' and account != 'admin111' ") is not None:
            return cur.fetchall()



        

class DATA_use:
    def __init__(self,data):
        self.data = data
