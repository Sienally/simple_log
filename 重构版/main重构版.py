import sqlite3
import os
import os.path
import time
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import threading
import json
import webbrowser
import requests
from PIL import Image, ImageTk
from ctypes import windll

import behind重构版

windll.gdi32.AddFontResourceW(os.path.join(os.getcwd(), "data_file/font/YuWoErYanNiZuiKeAi/YuWoErYanNiZuiKeAi-2.ttf"))



weekdays = {
            1: "周一", 
            2: "周二", 
            3: "周三", 
            4: "周四", 
            5: "周五", 
            6: "周六", 
            7: "周日"
            }

class log_page:
    
    # 初始化登录界面
    def __init__(self):

        # 变量
        self.root = tk.Tk()
        self.root.title("log_in")
        self.root_width, self.root_height = 900, 700
        self.root.geometry(f"{self.root_width}x{self.root_height}")
        self.center_window(self.root_width, self.root_height)
        
        self.after_id = None
        self.current_location = 1  # 用于判断当前在登录界面还是注册界面, 1为登录界面, 2为注册界面, 3为游客登录界面, 4为找回密码界面
        self.statue = 0  # 用于判断登陆是否成功的值
        self.account = 0  #用于存账号的值
        self.password = 0  #用于存密码的值
        self.name = None


        
        # 函数
        self.widgets()
        self.reset_time()
        # 叉掉窗口会立即执行的函数
        self.root.protocol("WM_DELETE_WINDOW", self.ask_quit)
        # 砍掉屏幕的标题栏、图标、边框、白边
        # 暂不适用, 会把放大, 关闭等功能全删除, 并且不能移动窗口
        # self.root.overrideredirect(True)




    
    # 询问是否退出
    def ask_quit(self):
        if messagebox.askokcancel("退出", "登录操作未完成, 确定要退出吗？", default="cancel"):
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)   
            # 卸载字体
            windll.gdi32.RemoveFontResourceW(os.path.join(os.getcwd(), "data_file/font/YuWoErYanNiZuiKeAi/YuWoErYanNiZuiKeAi-2.ttf")) 
            self.root.destroy()
     


    # 将窗口居中显示
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    
    # 清除窗口上所有组件, 但不销毁窗口, 用于在登录界面和注册界面之间切换时清除组件, 以免组件重叠
    def clear_all_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    # 登陆界面布局
    def widgets(self):
        
        # 以防万一, 先清屏后布局
        self.current_location = 1
        self.clear_all_widgets()

        # 背景图片
        bg_image = Image.open(os.path.join(os.getcwd(), "data_file/image/登录背景图.png"))

        tk_bg_image = ImageTk.PhotoImage(image=bg_image)
        bg_label = tk.Label(self.root, image=tk_bg_image)
        bg_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        bg_label.image = tk_bg_image  # 保持对图像的引用, 防止被垃圾回收


        # 竖向分割横线
        # line2 = ttk.Separator(left_frame, orient="vertical").pack(side="right", fill="y")


        # 组件框架
        label_frame_color = "#ffffff"

        label_frame = tk.Frame(self.root, bg=label_frame_color)
        label_frame.place(anchor="center", relx=0.42, rely=0.5, relheight=0.93, relwidth=0.45)

        tk.Label(label_frame, text="欢迎回来", font=("于我而言你最可爱", 25), bg=label_frame_color).pack(pady=(20, 0))

        # 背景设微笑图片
        img = Image.open(os.path.join(os.getcwd(), "data_file/image/微笑.gif"))
        new_img = img.resize((240, 240))
        new_img.save(os.path.join(os.getcwd(), "data_file/image/small_smile.gif"))

        img_data = Image.open(os.path.join(os.getcwd(), "data_file/image/small_smile.gif"))

        img = ImageTk.PhotoImage(image=img_data)
        label_img = tk.Label(label_frame, image=img, bg="blue")
        label_img.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.4, relheight=0.3)
        # 保持对图像的引用, 防止被垃圾回收
        label_img.image = img


        my_font = font.Font(family="黑体", size=11, underline=True)


        # 账号框架----
        account_frame = tk.Frame(label_frame, bg="#D4DFAC", width=400)
        account_frame.pack(pady=(250, 10))

        tk.Label(account_frame, text="账号：", font=("黑体", 17), bg=label_frame_color).pack(side="left", fill=tk.Y, expand=True)
        
        self.account_entry = tk.Entry(account_frame, font=("黑体", 17), relief="solid", border=1)
        self.account_entry.pack(side="right", expand=True, fill=tk.Y)
        



        # 鼠标进入账号框触发事件, 弹出已有账号框
        def cursor_in_account(self, e):


            # 读取已有帐号
            account_list = behind重构版.LOG().auto_account()
            # 创建列表框架
            self.all_account_frame = tk.Frame(label_frame, height=10, width=34, bg="#FFFFFF")
            self.all_account_frame.place(relx=0.292, rely=0.536, anchor="nw")
            

            self.cursor_in = False
            def a(e):
                self.cursor_in = True
            def b(e):
                self.cursor_in = False

            self.all_account_frame.bind("<Enter>", a)
            self.all_account_frame.bind("<Leave>", b)


            # 把账号逐个做成label放进去
            for account in account_list:
                all_account_list = tk.Label(self.all_account_frame, text=account, font=("黑体", 15), bg="#FFFFFF")
                all_account_list.pack(side="top", anchor="w")



        def check_account_frame(self):

            if  self.cursor_in == False:
                self.all_account_frame.destroy()


        # 鼠标离开帐号框
        def cursor_out_account(self, e):

            self.root.after(100, lambda : check_account_frame(self))
        
        self.account_entry.bind("<Enter>", lambda e: cursor_in_account(self, e))
        self.account_entry.bind("<Leave>", lambda e: cursor_out_account(self, e))



        # 密码框架----
        password_frame = tk.Frame(label_frame, bg="#D4DFAC", width=400)
        password_frame.pack()

        tk.Label(password_frame, text="密码：", font=("黑体", 17), bg=label_frame_color).pack(side="left", expand=True, fill=tk.Y)
        
        self.password_entry = tk.Entry(password_frame,show="*", font=("黑体", 17), relief="solid", border=1)
        self.password_entry.pack(side="right", expand=True, fill=tk.Y)
        

        # 忘记密码文本
        forget_password = tk.Label(label_frame, text="忘记密码？", font=my_font, fg="blue", bg=label_frame_color, cursor="hand2")
        forget_password.place(rely=0.6, relx=0.92, anchor="ne")


        # 按钮框架----
        button_frame = tk.Frame(label_frame, bg=label_frame_color)
        button_frame.pack(pady=(50, 10))
        # 按钮框架下直接放游客登陆按钮
        
        
        # 登录按钮
        self.sign_in_button = tk.Button(button_frame, width=24, bg="#F97A74", fg="white", relief="flat", cursor="hand2", text="登录", font=("于我而言你最可爱", 18, "bold"), command=self.log_in_page)
        self.sign_in_button.pack(fill=tk.X, expand=True)


        # 注册提示文本框架
        no_account_frame = tk.Frame(label_frame)
        no_account_frame.pack(pady=(13, 0))

        tk.Label(no_account_frame, text="还没有账号？", bg="#FFFFFF", font=("宋体", 11)).pack(side="left")
        no_account = tk.Label(no_account_frame, text="立即注册", font=my_font, fg="blue", bg=label_frame_color, cursor="hand2")
        no_account.pack(side="right")

        tk.Label(label_frame, text="—————————— 或 ——————————", font=("黑体", 12), bg=label_frame_color).pack(pady=(10, 0))


        # 游客登陆按钮
        self.visitor_button = tk.Button(label_frame, width=20, bg="white", fg="#9E9ACA", relief="solid", bd=1, cursor="hand2", pady=5, text="游客登陆", font=("于我而言你最可爱", 15), command=self.visitor_login)
        self.visitor_button.pack(side="bottom", pady=(0, 20))
        

        # 左侧快速导航栏

        # 登录界面
        self.login_nav_frame = tk.Frame(self.root, bg="#FBF9FD")
        self.login_nav_frame.place(relx=0.02, rely=0.07, anchor="nw", relheight=0.06, relwidth=0.15)

        img1 = Image.open(os.path.join(os.getcwd(), "data_file/image/矢量图库/个人信息.png"))
        img1 = img1.resize((25, 25))
        tk_img1 = ImageTk.PhotoImage(img1)
        login_nav_label = tk.Label(self.login_nav_frame, image=tk_img1, bg="#FBF9FD")
        login_nav_label.pack(side="left", padx=10)
        login_nav_label.image = tk_img1  # 保持对图像的引用, 防止被垃圾回收

        label1 = tk.Label(self.login_nav_frame, text="登录", font=("黑体", 12), bg="#FBF9FD")
        label1.pack(side="left")
        
        # 命令绑定
        def move_to_login_page(e, self):

            if self.current_location != 1:
                self.current_location = 1

                self.login_nav_frame.config(bg="#F86A9A")
                label1.config(bg="#F86A9A")
                label1.config(fg="#9188AE")
                login_nav_label.config(bg="#F86A9A")
                self.clear_all_widgets()
                self.widgets()
                

        self.login_nav_frame.bind("<Button-1>", lambda e: move_to_login_page(e, self))
        label1.bind("<Button-1>", lambda e: move_to_login_page(e, self))
        login_nav_label.bind("<Button-1>", lambda e: move_to_login_page(e, self))


        # 交互设计绑定
        def on_enter1(e):
            if self.current_location != 1:
                self.login_nav_frame.config(bg="#F86A9A")
                self.login_nav_frame.bg = "#F86A9A"
                label1.config(bg="#F86A9A")
                login_nav_label.config(bg="#F86A9A")

        
        self.login_nav_frame.bind("<Enter>", lambda e: on_enter1(e))
        label1.bind("<Enter>", lambda e: on_enter1(e))
        login_nav_label.bind("<Enter>", lambda e: on_enter1(e))

        def on_leave1(e):
            if self.current_location != 1:
                self.login_nav_frame.config(bg="#FBF9FD")
                label1.config(bg="#FBF9FD")
                login_nav_label.config(bg="#FBF9FD")

        self.login_nav_frame.bind("<Leave>", lambda e: on_leave1(e))
        label1.bind("<Leave>", lambda e: on_leave1(e))
        login_nav_label.bind("<Leave>", lambda e: on_leave1(e))


        # 注册界面
        self.sign_up_nav_frame = tk.Frame(self.root, bg="#FBF9FD")
        self.sign_up_nav_frame.place(relx=0.02, rely=0.15, anchor="nw", relheight=0.06, relwidth=0.15)

        img2 = Image.open(os.path.join(os.getcwd(), "data_file/image/矢量图库/群体.png"))
        img2 = img2.resize((25, 25))
        tk_img2 = ImageTk.PhotoImage(img2)
        sign_up_nav_label = tk.Label(self.sign_up_nav_frame, image=tk_img2, bg="#FBF9FD")
        sign_up_nav_label.pack(side="left", padx=10)
        sign_up_nav_label.image = tk_img2  # 保持对图像的引用, 防止被垃圾回收

        label2 = tk.Label(self.sign_up_nav_frame, text="注册", font=("黑体", 12), bg="#FBF9FD")
        label2.pack(side="left")

        # 点击命令绑定
        def move_to_sign_up_page(e, self):

            if self.current_location != 2:
                self.current_location = 2
                self.sign_up_nav_frame.config(bg="#F86A9A")
                label2.config(bg="#F86A9A")
                sign_up_nav_label.config(bg="#F86A9A")
                self.widgets_on_sign_up()
                

        self.sign_up_nav_frame.bind("<Button-1>", lambda e: move_to_sign_up_page(e, self))
        label2.bind("<Button-1>", lambda e: move_to_sign_up_page(e, self))
        sign_up_nav_label.bind("<Button-1>", lambda e: move_to_sign_up_page(e, self))

        # 交互设计绑定
        def on_enter2(e):
            if self.current_location != 2:
                self.sign_up_nav_frame.config(bg="#F86A9A")
                label2.config(bg="#F86A9A")
                sign_up_nav_label.config(bg="#F86A9A")

        self.sign_up_nav_frame.bind("<Enter>", lambda e: on_enter2(e))
        label2.bind("<Enter>", lambda e: on_enter2(e))
        sign_up_nav_label.bind("<Enter>", lambda e: on_enter2(e))
        
        def on_leave2(e):
            if self.current_location != 2:
                self.sign_up_nav_frame.config(bg="#FBF9FD")
                label2.config(bg="#FBF9FD")
                sign_up_nav_label.config(bg="#FBF9FD")

        self.sign_up_nav_frame.bind("<Leave>", lambda e: on_leave2(e))
        label2.bind("<Leave>", lambda e: on_leave2(e))
        sign_up_nav_label.bind("<Leave>", lambda e: on_leave2(e))



        # 右侧内容布局

        # 右上时间框架
        time_frame = tk.Frame(self.root, height=70, width=170, bg="#F9F1FE")
        time_frame.place(relx=0.77, rely=0.07, anchor="nw")
        time_frame.pack_propagate(False)

        # 时间显示
        st = time.localtime()
        self.time_info_1 = tk.StringVar()
        self.time_info_2 = tk.StringVar()
        tk.Label(time_frame, textvariable=self.time_info_1, bg="#F9F1FE", font=("黑体", 11)).pack(side="top", anchor="e", pady=(10, 5))
        tk.Label(time_frame, textvariable=self.time_info_2, bg="#F9F1FE", fg="#E694BF", font=("于我而言你最可爱", 17, "bold")).pack(side="right", anchor="n", pady=(5, 10))        


        # 右中
        log_img_smile_right = Image.open(os.path.join(os.getcwd(), "data_file/image/image2.png"))
        log_img_smile_right = log_img_smile_right.resize((180, 180))
        
        tk_log_img_smile_right = ImageTk.PhotoImage(log_img_smile_right)
        label_log_img_smile_right = tk.Label(self.root, image=tk_log_img_smile_right, bg="#F8F0FB")
        label_log_img_smile_right.place(relx=0.70, rely=0.2)
        label_log_img_smile_right.image = tk_log_img_smile_right  # 永久保存图片


        # 右下角文本

        tk.Label(self.root, text="“", font=("黑体", 50), bg="#F2EEFD", fg="#F86A9A").place(relx=0.7, rely=0.7, anchor="center")
        tk.Label(self.root, text="每一次登录，", font=("于我而言你最可爱", 15), bg="#F0E8FD").place(relx=0.7, rely=0.71, anchor="nw")
        tk.Label(self.root, text="都是全新的开始！", font=("于我而言你最可爱", 15), bg="#F0E8FD").place(relx=0.7, rely=0.77, anchor="nw")
        

        # 微信收款码框架-----------------
        WEIXIN_frame = tk.Frame(self.root, bg="#EEE6FD", height=100, width=240)
        WEIXIN_frame.place(relx=1, rely=1, anchor="se")
        WEIXIN_frame.pack_propagate(False)

        if not os.path.exists(os.path.join(os.getcwd(), "data_file/image/微信收款码.png")):
            my_img = Image.open(os.path.join(os.getcwd(), "data_file/image/收款码.jpg"))
            my_img = my_img.resize((100, 100))
            my_img.save(os.path.join(os.getcwd(), "data_file/image/微信收款码.png"))

        my_img = Image.open(os.path.join(os.getcwd(), "data_file/image/微信收款码.png"))
        tk_my_img = ImageTk.PhotoImage(my_img)

        my_label = tk.Label(WEIXIN_frame, image=tk_my_img)
        my_label.pack(side="right")
        my_label.image = tk_my_img  # 保存图片不被清理


        # 请我喝奶茶文本
        tk.Label(WEIXIN_frame, text="请他喝奶茶", bg="#EEE6FB", font=(13)).pack(side="left")

        img3 = Image.open(os.path.join(os.getcwd(), "data_file/image/矢量图库/指向.png"))
        img3 = img3.resize((30, 30))
        tk_img3 = ImageTk.PhotoImage(img3)
        label_in_WEIXIN = tk.Label(WEIXIN_frame, image=tk_img3, bg="#EEE6FD")
        label_in_WEIXIN.pack(side="left", padx=10)
        label_in_WEIXIN.image = tk_img3


        if self.current_location == 1:
            self.login_nav_frame.config(bg="#F86A9A")
            label1.config(bg="#F86A9A")
            login_nav_label.config(bg="#F86A9A")



        # 对文本的功能实现

        # 绑定左键点击(<Button-1>)
        no_account.bind("<Button-1>", lambda e: self.widgets_on_sign_up())
        forget_password.bind("<Button-1>", self.find_password)


        # 登录窗口不许放大
        self.root.resizable(False, False)
    




    # 注册界面布局
    def widgets_on_sign_up(self):

        # 以防万一, 先清屏后布局
        self.clear_all_widgets()
        # 进入注册界面后会立马更新当前状态2
        self.current_location = 2

        # 背景图片
        bg_image = Image.open(os.path.join(os.getcwd(), "data_file/image/登录背景图.png"))

        tk_bg_image = ImageTk.PhotoImage(image=bg_image)
        bg_label = tk.Label(self.root, image=tk_bg_image)
        bg_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        bg_label.image = tk_bg_image  # 保持对图像的引用, 防止被垃圾回收



        # 左上角返回按钮
        def back_to_login(e, self):
            self.current_location = 1
            self.clear_all_widgets()
            self.widgets()
            
        back = tk.Label(self.root, text="<  返回", font=("黑体", 13), bg="#FECBEC", cursor="hand2")
        back.place(relx=0.01, rely=0.01, anchor="nw")
        back.bind("<Button-1>", lambda e: back_to_login(e, self))


        # 右侧内容布局

        # 时间框架
        time_frame = tk.Frame(self.root, height=70, width=170, bg="#F9F1FE")
        time_frame.place(relx=0.77, rely=0.07, anchor="nw")
        time_frame.pack_propagate(False)

        # 时间显示
        st = time.localtime()
        self.time_info_1 = tk.StringVar()
        self.time_info_2 = tk.StringVar()
        tk.Label(time_frame, textvariable=self.time_info_1, bg="#F9F1FE", font=("黑体", 11)).pack(side="top", anchor="e", pady=(10, 5))
        tk.Label(time_frame, textvariable=self.time_info_2, bg="#F9F1FE", fg="#E694BF", font=("于我而言你最可爱", 17, "bold")).pack(side="right", anchor="n", pady=(5, 10))
        
        # 竖向分割横线
        # line2 = ttk.Separator(left_frame, orient="vertical").pack(side="right", fill="y")


        # 组件框架
        label_frame_color = "#ffffff"

        label_frame = tk.Frame(self.root, bg=label_frame_color)
        label_frame.place(anchor="center", relx=0.42, rely=0.5, relheight=0.93, relwidth=0.45)

        tk.Label(label_frame, text="创建新账号", font=("微软雅黑", 20), bg=label_frame_color).pack(pady=(20, 0))
        tk.Label(label_frame, text="欢迎加入我们！", font=("微软雅黑", 10), bg=label_frame_color).pack(pady=(0, 20))

        # 背景设微笑图片

        img_data = Image.open("data_file/image/small_smile.gif")

        img = ImageTk.PhotoImage(image=img_data)
        label = tk.Label(label_frame, image=img, bg="blue")
        label.place(relx=0.5, rely=0.15, anchor="n", relwidth=0.4, relheight=0.3)
        # 保持对图像的引用, 防止被垃圾回收
        label.image = img


        my_font = font.Font(family="黑体", size=11, underline=True, slant="italic")


        # 昵称框架----
        name_frame = tk.Frame(label_frame, bg="#D4DFAC", width=400)
        name_frame.pack(pady=(200, 10))
        
        tk.Label(name_frame, text="    昵称: ", font=("黑体", 17), bg=label_frame_color).pack(side="left")
        self.sign_up_name = tk.Entry(name_frame,  font=("黑体", 17), relief="solid")
        self.sign_up_name.pack(side="right", expand=True, fill=tk.Y)


        # 账号框架----
        account_frame = tk.Frame(label_frame, bg="#D4DFAC", width=400)
        account_frame.pack(pady=(0, 10))

        tk.Label(account_frame, text="    账号：", font=("黑体", 17), bg=label_frame_color).pack(side="left", fill=tk.Y, expand=True)
        
        self.sign_up_account_entry = tk.Entry(account_frame, font=("黑体", 17), relief="solid")
        self.sign_up_account_entry.pack(side="right", expand=True, fill=tk.Y)
        


        # 密码框架----
        password_frame = tk.Frame(label_frame, bg="#D4DFAC", width=400)
        password_frame.pack(pady=(0, 10))
        tk.Label(password_frame, text="    密码：", font=("黑体", 17), bg=label_frame_color).pack(side="left", expand=True, fill=tk.Y)
        
        self.sign_up_password = tk.Entry(password_frame,show="*", font=("黑体", 17), relief="solid", border=1)
        self.sign_up_password.pack(side="right", expand=True, fill=tk.Y)


        
        # 确认密码框架----
        self.ensure_sign_up_password_frame = tk.Frame(label_frame, bg="#C8EBAA")
        self.ensure_sign_up_password_frame.pack(pady=(0, 10))

        tk.Label(self.ensure_sign_up_password_frame, text="确认密码：", font=("黑体", 17), bg=label_frame_color).pack(side="left")
        self.ensure_sign_up_password = tk.Entry(self.ensure_sign_up_password_frame, show="*", font=("黑体", 17), relief="solid")
        self.ensure_sign_up_password.pack(side="right", expand=True, fill=tk.Y)
        
        

        # 二级密码框架----
        second_password_frame = tk.Frame(label_frame, bg="#C8EBAA")
        second_password_frame.pack()

        tk.Label(second_password_frame, text="二级密码：", font=("黑体", 17), bg=label_frame_color).pack(side="left")
        self.sign_up_second_password = tk.Entry(second_password_frame, font=("黑体", 17), relief="solid")
        self.sign_up_second_password.pack(side="right", expand=True, fill=tk.Y)


        # 按钮框架----
        button_frame = tk.Frame(label_frame, bg=label_frame_color)
        button_frame.pack(pady=(50, 0))
        # 按钮框架下直接放游客登陆按钮
        
        
        # 登录按钮
        self.sign_in_button = tk.Button(button_frame, width=30, bg="#F97A74", fg="white", relief="flat", cursor="hand2", pady=5, text="注册", font=("黑体", 15, "bold"), command=self.commit_user_info)
        self.sign_in_button.pack(fill=tk.X, expand=True)

        
        # 跳到登录界面文本
        bottom_frame = tk.Frame(label_frame, bg=label_frame_color)
        bottom_frame.pack(side="bottom", pady=(0, 30))

        tk.Label(bottom_frame, text="已有账号？", font=("黑体", 10), bg=label_frame_color).pack(side="left")
        have_account = tk.Label(bottom_frame, text="立即登录", font=("黑体", 10), fg="blue", bg=label_frame_color, cursor="hand2")
        have_account.pack(side="right")

        # 跳转到登陆界面函数
        def move_to_login_page(e, self):

            if self.current_location != 1:
                self.current_location = 1
                self.login_nav_frame.config(bg="#F86A9A")
                label1.config(bg="#F86A9A")
                login_nav_label.config(bg="#F86A9A")
                self.clear_all_widgets()
                self.widgets()
                
        have_account.bind("<Button-1>", lambda e: move_to_login_page(e, self))


        # 左侧快速导航栏------------------------------

        # 登录界面
        self.login_nav_frame = tk.Frame(self.root, bg="#FBF9FD")
        self.login_nav_frame.place(relx=0.02, rely=0.07, anchor="nw", relheight=0.06, relwidth=0.15)

        img1 = Image.open("data_file/image/矢量图库/个人信息.png")
        img1 = img1.resize((25, 25))
        tk_img1 = ImageTk.PhotoImage(img1)
        login_nav_label = tk.Label(self.login_nav_frame, image=tk_img1, bg="#FBF9FD")
        login_nav_label.pack(side="left", padx=10)
        login_nav_label.image = tk_img1  # 保持对图像的引用, 防止被垃圾回收

        label1 = tk.Label(self.login_nav_frame, text="登录", font=("黑体", 12), bg="#FBF9FD")
        label1.pack(side="left")
        
        # 命令绑定
        def move_to_login_page(e, self):

            if self.current_location != 1:
                self.login_nav_frame.config(bg="#F86A9A")
                label1.config(bg="#F86A9A")
                login_nav_label.config(bg="#F86A9A")
                self.clear_all_widgets()
                self.widgets()
                self.current_location = 1

        self.login_nav_frame.bind("<Button-1>", lambda e: move_to_login_page(e, self))
        label1.bind("<Button-1>", lambda e: move_to_login_page(e, self))
        login_nav_label.bind("<Button-1>", lambda e: move_to_login_page(e, self))
        

        # 交互设计绑定
        def on_enter1(e):
            self.login_nav_frame.config(bg="#F86A9A")
            label1.config(bg="#F86A9A")
            login_nav_label.config(bg="#F86A9A")

        self.login_nav_frame.bind("<Enter>", lambda e: on_enter1(e))
        label1.bind("<Enter>", lambda e: on_enter1(e))
        login_nav_label.bind("<Enter>", lambda e: on_enter1(e))
        
        def on_leave1(e):
            self.login_nav_frame.config(bg="#FBF9FD")
            label1.config(bg="#FBF9FD")
            login_nav_label.config(bg="#FBF9FD")

        self.login_nav_frame.bind("<Leave>", lambda e: on_leave1(e))
        label1.bind("<Leave>", lambda e: on_leave1(e))
        login_nav_label.bind("<Leave>", lambda e: on_leave1(e))


        # 注册界面
        self.sign_up_nav_frame = tk.Frame(self.root, bg="#FBF9FD")
        self.sign_up_nav_frame.place(relx=0.02, rely=0.15, anchor="nw", relheight=0.06, relwidth=0.15)

        img2 = Image.open("data_file/image/矢量图库/群体.png")
        img2 = img2.resize((25, 25))
        tk_img2 = ImageTk.PhotoImage(img2)
        sign_up_nav_label = tk.Label(self.sign_up_nav_frame, image=tk_img2, bg="#FBF9FD")
        sign_up_nav_label.pack(side="left", padx=10)
        sign_up_nav_label.image = tk_img2  # 保持对图像的引用, 防止被垃圾回收

        label2 = tk.Label(self.sign_up_nav_frame, text="注册", font=("黑体", 12), bg="#FBF9FD")
        label2.pack(side="left")

        # 点击命令绑定
        def move_to_sign_up_page(e, self):

            if self.current_location != 2:
                self.current_location = 2
                self.sign_up_nav_frame.config(bg="#F86A9A")
                label2.config(bg="#F86A9A")
                sign_up_nav_label.config(bg="#F86A9A")
                self.widgets_on_sign_up()
                

        self.sign_up_nav_frame.bind("<Button-1>", lambda e: move_to_sign_up_page(e, self))
        label2.bind("<Button-1>", lambda e: move_to_sign_up_page(e, self))
        sign_up_nav_label.bind("<Button-1>", lambda e: move_to_sign_up_page(e, self))

        # 交互设计绑定
        def on_enter2(e):
            if self.current_location != 2:
                self.sign_up_nav_frame.config(bg="#F86A9A")
                label2.config(bg="#F86A9A")
                sign_up_nav_label.config(bg="#F86A9A")

        self.sign_up_nav_frame.bind("<Enter>", lambda e: on_enter2(e))
        label2.bind("<Enter>", lambda e: on_enter2(e))
        sign_up_nav_label.bind("<Enter>", lambda e: on_enter2(e))
        
        def on_leave2(e):
            if self.current_location != 2:
                self.sign_up_nav_frame.config(bg="#FBF9FD")
                label2.config(bg="#FBF9FD")
                sign_up_nav_label.config(bg="#FBF9FD")

        self.sign_up_nav_frame.bind("<Leave>", lambda e: on_leave2(e))
        label2.bind("<Leave>", lambda e: on_leave2(e))
        sign_up_nav_label.bind("<Leave>", lambda e: on_leave2(e))


        # 微信收款码框架-----------------
        WEIXIN_frame = tk.Frame(self.root, bg="#EEE6FD", height=100, width=240)
        WEIXIN_frame.place(relx=1, rely=1, anchor="se")
        WEIXIN_frame.pack_propagate(False)

        if not os.path.exists("data_file/image/微信收款码.png"):
            my_img = Image.open("data_file/image/收款码.jpg")
            my_img = my_img.resize((100, 100))
            my_img.save("data_file/image/微信收款码.png")

        my_img = Image.open("data_file/image/微信收款码.png")
        tk_my_img = ImageTk.PhotoImage(my_img)

        my_label = tk.Label(WEIXIN_frame, image=tk_my_img)
        my_label.pack(side="right")
        my_label.image = tk_my_img  # 保存图片不被清理


        # 请我喝奶茶文本
        tk.Label(WEIXIN_frame, text="请他喝奶茶", bg="#EEE6FB", font=(13)).pack(side="left")

        img3 = Image.open("data_file/image/矢量图库/指向.png")
        img3 = img3.resize((30, 30))
        tk_img3 = ImageTk.PhotoImage(img3)
        label_in_WEIXIN = tk.Label(WEIXIN_frame, image=tk_img3, bg="#EEE6FD")
        label_in_WEIXIN.pack(side="left", padx=10)
        label_in_WEIXIN.image = tk_img3


        if self.current_location == 2:
            self.sign_up_nav_frame.config(bg="#F86A9A")
            sign_up_nav_label.config(bg="#F86A9A")
            label2.config(bg="#F86A9A")



        # 登录窗口不许放大
        self.root.resizable(False, False)


    # 找回密码
    def find_password(self, v):

        if tk.messagebox.askyesno("寻回密码", "确定找回密码？"):
            # 创建找回密码页面
            find_password_page = tk.Toplevel()
            find_password_page.title("找回密码")

            # 将找回密码窗口大小和摆放位置与主窗口一致
            width = self.root_width // 2
            height = self.root_height // 2

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            def center_window_in_root(find_password_page, width, height, screen_width, screen_height):
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2
                find_password_page.geometry(f"{width}x{height}+{x}+{y}")
            center_window_in_root(find_password_page, width, height, screen_width, screen_height)
            


    # 实时刷新时间
    def reset_time(self):
        st = time.localtime()
        self.time_info_1.set("{:02d}年{:02d}月{:02d}日 {}".format(st[0], st[1], st[2], weekdays[st.tm_wday+1]))
        self.time_info_2.set(f"{st[3]:02d}:{st[4]:02d}:{st[5]:02d}")
        self.after_id = self.root.after(1000, self.reset_time)



    # 登录功能
    def log_in_page(self):
        self.account = str(self.account_entry.get())
        self.password = str(self.password_entry.get())

        # 登录逻辑判断交给后端模块数据处理
        # behind后端模块
        log_statue = behind重构版.LOG(account=self.account, password=self.password, time_info=time.strftime("%Y-%m-%d %H:%M:%S"))
        

        # 如果账号框为空
        if self.account == "":
            tk.messagebox.showerror("账号错误", "账号不能为空！")
            # 中断, 不让后续语句执行
            return 0
        # 如果密码框为空
        elif self.password == "":
            tk.messagebox.showerror("密码错误！", "密码不能为空！")
            # 中断, 不让后续语句执行
            return 0
        

        if log_statue.is_true_account_statues != 1:
            show_account_warning = tk.messagebox.showerror("账号错误", "账号不存在！")
            self.password_entry.delete(0, "end")
        
        
        # 账号正确
        else:    
            # 判断密码是否正确

            if log_statue.is_true_password_statues == 1:

                # 登录成功
                self.name = log_statue.log_in_name
                self.statue = 1

            else:
                show_password_warning = tk.messagebox.showerror("密码错误", "密码错误, 请重试！")
                self.password_entry.delete(0, "end")


        # 登陆成功后先关闭after命令, 后销毁主窗口
        if self.statue == 1:
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
            self.root.destroy()



        

    # 游客登陆功能
    def visitor_login(self):

        if tk.messagebox.askyesno("游客登陆", "游客模式下部分功能受限") == False:
            return 0

        # 游客信息初始化
        self.account = "visitor111"
        self.password = "111"
        self.name = "游客"

        visitor = behind重构版.LOG(account=self.account, time_info=time.strftime("%Y-%m-%d %H:%M:%S"), password=None)
        self.statue = visitor.visitor_login()

        # 游客登陆成功
        if self.statue == 1:
            
            # 游客登陆成功后, 需关闭各个after命令
            if self.after_id is not None:

                self.root.after_cancel(self.after_id) 
            self.root.destroy()

        else:
            tk.messagebox.showerror("错误！", "游客登陆发生异常错误！")
            


    # 提交数据给后端处理
    def commit_user_info(self):
        name = str(self.sign_up_name.get())
        account = str(self.sign_up_account_entry.get())
        password = str(self.sign_up_password.get())
        ensure_password = str(self.ensure_sign_up_password.get())
        second_password = str(self.sign_up_second_password.get())
        
        if account == "" or password == "" or ensure_password == "" or name == "":
            tk.messagebox.showinfo("提示", "请填写完必须信息", icon="error", parent=self.root)
        
        else:
            # 如果二级密码为空
            if second_password == "":

                # 提醒设置二级密码
                is_continue = tk.messagebox.askokcancel("二级密码设置", "确定不设置二级密码吗？二级密码是您找回账号的唯一方式, 后续可能会导致账号永久无法寻回", icon="warning", parent=self.root)
                
                # 仍然不设置二级密码, 继续下一步
                if is_continue == True:
                    
                    # 验证两次密码是否一致
                    if ensure_password != password:
                        tk.messagebox.showwarning("错误！", "密码不一致！", icon="error", parent=self.root)
                    
                    # 两次密码一致
                    else:
                        sign_up_statue = behind重构版.LOG(account=account, sign_up_name=name, password=password, time_info=time.strftime("%Y-%m-%d %H:%M:%S"), second_password=second_password)
                        statue = sign_up_statue.sign_up()
                        
                        # 判断账号格式
                        if  statue == 0:
                            tk.messagebox.showerror("账号格式错误！", "账号长度长度不得低于11位！", parent=self.root)
                    
                        # 账号已存在
                        elif statue == -2:
                            tk.messagebox.showerror("错误！", "该账号已存在", parent=self.root)    

                        # 账号格式正确
                        else:
                           
                            # 判断密码格式
                            if statue == -1:
                                tk.messagebox.showerror("密码格式错误！", "密码长度应在6-15之间", parent=self.root)
                            
                            # 密码格式正确
                            else:
                                
                                # 注册成功
                                tk.messagebox.showinfo("注册成功！", "恭喜您已完成账号注册", parent=self.root)
                                self.clear_all_widgets()
                                self.widgets()

                


            # 如果二级密码不为空
            else:
                # 验证两次密码是否一致
                if ensure_password != password:
                    tk.messagebox.showwarning("错误！", "密码不一致！", icon="error", parent=self.root)
                    
                # 两次密码一致
                else:
                    sign_up_statue = behind重构版.LOG(account=account, sign_up_name=name, password=password, time_info=time.strftime("%Y-%m-%d %H:%M:%S"), second_password=second_password)
                    statue = sign_up_statue.sign_up()
                        
                    # 判断账号格式
                    if  statue == 0:
                        tk.messagebox.showerror("账号格式错误！", "账号长度不得低于11位！", parent=self.root)
                    
                    # 账号已存在
                    elif statue == -2:
                        tk.messagebox.showerror("错误！", "该账号已存在", parent=self.root)    

                    # 账号格式正确
                    else:
                           
                        # 判断密码格式
                        if statue == -1:
                            tk.messagebox.showerror("密码格式错误！", "密码长度应在6-15之间", parent=self.root)
                            
                        # 密码格式正确
                        else:
                                
                            # 注册成功
                            tk.messagebox.showinfo("注册成功！", "恭喜您已完成账号注册", parent=self.root)
                            self.clear_all_widgets()
                            self.widgets()





class App:
    
    # 初始化应用程序
    def __init__(self, account, password, name):
        self.name = name
        self.account = account
        self.password = password
        self.root = tk.Tk()
        self.root.title("YZA")
        self.root_width, self.root_height = 1200, 900    
        self.root.geometry(f"{self.root_width}x{self.root_height}")
        self.after_id = None
        self.after_id2 = None


        # 函数
        self.center_window(self.root_width, self.root_height)
        self.create_widgets()
        self.reset_time()
        self.root.protocol("WM_DELETE_WINDOW", self.break_after)
        

    # 实时刷新时间
    def reset_time(self):
        st = time.localtime()
        self.time_strvar.set("{}年{}月{}日  {}\n\t  {:02d}:{:02d}:{:02d}".format(st[0], st[1], st[2], weekdays[st.tm_wday+1], st[3], st[4], st[5]))
        self.after_id = self.root.after(1000, self.reset_time)


    # 关闭after进程
    def break_after(self):

        # 关闭时间刷新进程
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        # 关闭登陆成功弹窗进程
        if self.after_id2 is not None:
            self.root.after_cancel(self.after_id2)
            self.after_id2 = None
        
        self.root.destroy()


    # 将窗口居中显示
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")


    # 更多设置界面
    def more_settings_page(self):

        showinfo = tk.Toplevel(self.root)

        # 设置窗口背景色
        showinfo.configure(bg="#1A1A2E")

        # 窗口居中
        showinfo.title("更多设置")
        def center_window_top_on_root(showinfo, width, height):
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            showinfo.geometry(f"{width}x{height}+{x}+{y}")

        center_window_top_on_root(showinfo, width=self.root_width//3*2, height=self.root_height//3*2)
        showinfo.resizable(False, False)
        showinfo.attributes("-topmost", True)

        # 砍掉屏幕的标题栏、图标、边框、白边
        showinfo.overrideredirect(True)

        # 标题栏设置
        title_frame = tk.Frame(showinfo, bg="#7B6666")
        title_frame.pack(fill=tk.X)
        

        tk.Label(title_frame, text="更多设置", font=("黑体", 20), bg="#7B6666").pack(side="left", fill=tk.Y, padx=10)
        lab = tk.Label(title_frame, text="x", font=("黑体", 20), width=3, height=1, bg="#7B6666", fg="#f0f0f0")
        lab.pack(side="right", fill=tk.Y)

        # 鼠标悬停在关闭按钮上时改变颜色
        def on_enter(event):
            lab.config(bg="#F41010", fg="#f0f0f0")
        def on_leave(event):
            lab.config(bg="#7B6666", fg="#f0f0f0")
        def on_click(event):
            showinfo.destroy()

        # 移动窗口功能
        def start_move(event):
            global x, y
            x = event.x
            y = event.y
        def on_move(event):
            new_x = showinfo.winfo_x() + event.x - x
            new_y = showinfo.winfo_y() + event.y - y
            showinfo.geometry(f"+{new_x}+{new_y}")

        # 绑定事件
        lab.bind("<Enter>", on_enter)
        lab.bind("<Leave>", on_leave)
        lab.bind("<Button-1>", on_click)
        title_frame.bind("<Button-1>", start_move)
        title_frame.bind("<B1-Motion>", on_move)


        # 分割线
        ttk.Separator(showinfo, orient="horizontal").pack(fill=tk.X)

        # 左侧框架
        left_frame = tk.Frame(showinfo, bg="#1A1A31")
        left_frame.place(relheight=0.94, relwidth=0.25, relx=0.25, rely=0.08, anchor="ne")

        # 右侧框架
        right_frame = tk.Frame(showinfo, bg="#3636AB")
        right_frame.place(relheight=0.94, relwidth=0.75, relx=0.25, rely=0.08, anchor="nw")



    # 创建界面组件
    def create_widgets(self):

        # 菜单栏
        menubar = tk.Menu(self.root)
        
        # 账号菜单
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="账号", menu=account_menu)
        
        def account_settings():
            tk.messagebox.showinfo("个人信息", f"用户名: {self.name}\n账号: {self.account}\n密码: {'*' * len(self.password)}")
        
        account_menu.add_command(label="个人信息", command=account_settings)
        


        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="设置", menu=settings_menu)

        def set_privacy():
            tk.messagebox.showinfo("隐私设置", "隐私设置功能正在开发中，敬请期待！")
        
        settings_menu.add_command(label="隐私设置", command=set_privacy)
        settings_menu.add_command(label="更多设置", command=self.more_settings_page)
        


        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)

        def about_us():
            tk.messagebox.showinfo("关于我们", "YZA是一款由Sienally开发的桌面应用程序，旨在为用户提供便捷的服务和功能。我们致力于不断改进和优化用户体验，欢迎您使用YZA！")
        def version_info():
            tk.messagebox.showinfo("版本信息", "当前版本：YZA 1.0.0\n发布日期：2026年6月\n开发者：Sienally\n官方网站：https://example.com")
        def usage_help():
            tk.messagebox.showinfo("使用帮助", "欢迎使用YZA！\n\n1. 账号信息：在主界面顶部，您可以查看您的用户名和账号信息。\n\n2. 时间显示：主界面顶部右侧会实时显示当前日期和时间。\n\n3. 菜单栏：点击菜单栏中的选项可以访问账号设置、隐私设置、使用帮助等功能。\n\n4. 内容区域：主界面中部将展示不同的内容和功能，敬请期待后续更新！\n\n如果您有任何问题或需要帮助，请随时联系我们的客服团队。")
        
        help_menu.add_command(label="使用帮助", command=usage_help)
        help_menu.add_command(label="关于我们", command=about_us)
        help_menu.add_command(label="版本信息", command=version_info)
        
        


        # 把菜单栏加到主窗口上
        self.root.config(menu=menubar)


        # 标题和日期标签框架------------------------------
        top_frame = tk.Frame(self.root, bg="#D05454")
        top_frame.pack(fill=tk.X)

        # 时间标签
        st = time.localtime()
        self.time_strvar = tk.StringVar()
        self.time_strvar.set("{}年{:02d}月{:02d}日  {}\n\t   {:02d}:{:02d}:{:02d}".format(st[0], st[1], st[2], weekdays[st.tm_wday+1], st[3], st[4], st[5]))
        
        # 自定义用户字体
        user_font = font.Font(family="黑体", size=12, weight="bold", underline=True)
        
        # 用户信息框架
        user_info_frame = tk.Frame(top_frame, bg="#D05454", width=200, height=50)
        user_info_frame.pack(side="left")
        tk.Label(user_info_frame, text=f"用户：{self.name}", font=user_font, bg="#D05454").place(relx=0, rely=0.27, anchor="w")
        tk.Label(user_info_frame, text=f"账号：{self.account}", font=user_font, bg="#D05454").place(relx=0, rely=0.73, anchor="w")

        tk.Label(top_frame, text="欢  迎  使  用  YZA！", font=("正楷", 24, "italic"), bg="#D05454", fg="white").place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(top_frame, textvariable=self.time_strvar, font=("Arial", 12), bg="#D05454", fg="white").pack(side="right")


        #中间内容框架
        mid_frame = tk.Frame(self.root, bg="#2bb0d8")
        mid_frame.pack(fill=tk.BOTH, expand=True)
        
        #添加分支框架
        branch_frame = tk.Frame(mid_frame, bg="#add82b")
        branch_frame.pack(fill=tk.BOTH, expand=True, side="left")
        tk.Label(branch_frame, text="待开发框架...").place(relx=0.5, rely=0.5, anchor="center")

        #添加分支框架2
        branch_frame2 = tk.Frame(mid_frame, bg="#b82bd8")
        branch_frame2.pack(fill=tk.BOTH, expand=True, side="right")
        tk.Label(branch_frame2, text="待开发框架...").place(relx=0.5, rely=0.5, anchor="center")


        # 底部框架
        bottom_frame = tk.Frame(self.root, bg="#585151")
        bottom_frame.pack(fill=tk.X, side="bottom")

        nav_frame = tk.Frame(bottom_frame, bg="#585151")
        nav_frame.pack(padx=10, expand=True, fill=tk.BOTH)
        
        call_us_font = font.Font(family="Arial", size=10, slant="italic", underline=True)
        call_us = tk.Label(nav_frame, text="联系我们", font=call_us_font, bg="#585151", fg="white", cursor="hand2")
        call_us.pack(side="left", padx=30, expand=True)
        
        user_privacy_policy_font = font.Font(family="Arial", size=10, slant="italic", underline=True)
        user_privacy_policy = tk.Label(nav_frame, text="用户协议", font=user_privacy_policy_font, bg="#585151", fg="white", cursor="hand2")
        user_privacy_policy.pack(side="left", padx=30, expand=True)
        
        privacy_policy_font = font.Font(family="Arial", size=10, slant="italic", underline=True)
        privacy_policy = tk.Label(nav_frame, text="隐私政策", font=privacy_policy_font, bg="#585151", fg="white", cursor="hand2")
        privacy_policy.pack(side="left", padx=30, expand=True)

        tk.Label(bottom_frame, text="Copyright    ©    2026    YZA.    All    rights    reserved.", font=("Arial", 8, "italic"), bg="#585151", fg="white").pack()
        


        # 登录成功提示框----------------------
        showinfo = tk.Toplevel(self.root)
        showinfo.title("登陆成功")
        tk.Label(showinfo, text=f"欢迎用户：{self.name}", font=("黑体", 16, "bold"), bg="#dbb4b4").pack()
        

        def center_window_top_on_root(showinfo, width=500, height=100):
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            showinfo.geometry(f"{width}x{height}+{x}+{y-300}")

        center_window_top_on_root(showinfo)
        showinfo.resizable(False, False)



        # 登陆成功提示记住密码框
        
        # 游客登录除外
        if self.account != "visitor111":

            if tk.messagebox.askokcancel("提示", "是否允许系统记住密码？下次登陆更方便！"):
                behind重构版.LOG().save_password(self.account, self.password)



        # 屏幕强制置顶
        showinfo.attributes("-topmost", True)
        # 屏幕设置背景色
        showinfo.configure(bg="#f0f0f0")
        # 把屏幕上所有和背景色一样的颜色变透明
        showinfo.attributes("-transparentcolor", "#f0f0f0")
        # 砍掉屏幕的标题栏、图标、边框、白边
        showinfo.overrideredirect(True)

        # 三秒后自动关闭
        self.after_id2 = showinfo.after(3000, showinfo.destroy)
        #-----------------------------------



        # 对所有可点击文本的功能实现

        def call_us_click(v):
            tk.messagebox.showinfo("联系我们", "如果您有任何问题或需要帮助，请通过以下方式联系我们：\n\n邮箱: example@email.com")
            webbrowser.open("https://douyin.com")

        def server_terms_click(v):
            tk.messagebox.showinfo("用户协议", "这里是服务条款的内容。")
            webbrowser.open("https://bilibili.com")

        def privacy_policy_click(v):
            tk.messagebox.showinfo("隐私政策", "这里是隐私政策的内容。")
            webbrowser.open("https://kuaishou.com")

        # 绑定鼠标左键点击(<Button-1>)
        call_us.bind("<Button-1>", call_us_click)
        user_privacy_policy.bind("<Button-1>", server_terms_click)
        privacy_policy.bind("<Button-1>", privacy_policy_click)


      


def main():

    parama = {}
    parama["log"] = {}
    parama["main"] = {}

    # 提前创建数据文件夹
    if not os.path.exists(os.path.join(os.getcwd(), "data_file")):
        os.mkdir("data_file")
    
    # 创建存数据库的子文件
    if not os.path.exists(os.path.join(os.getcwd(), "data_file/a&p_data.db")):
        with open(os.path.join(os.getcwd(), "data_file/a&p_data.db"), "w") as f:
            pass

    if not os.path.exists(os.path.join(os.getcwd(), "data_file/image")):
        os.mkdir("data_file/image")


    # 登录界面---------------------------------
    
    login = log_page()

    # 技术文档-log参数
    parama["log"] = login.__dict__
    

    login.root.mainloop()
    
    # 提取给主页的数据
    account = login.account
    password = login.password
    name = login.name



    # 主界面---------------------------------
    if login.statue == 1:

        # 创建app对象
        app = App(account, password, name)

        # 技术文档-main参数
        parama["main"] = app.__dict__

        app.root.mainloop()

    
    if not parama["log"] or not parama["main"]:

        # 创建文件路径
        json_file = os.path.join(os.getcwd(), "data_file/parama.json")


        # 修改字典格式
        for i in parama:
            for n in parama[i]:
                parama[i][n] = str(parama[i][n])
            
        # 写入文件
        with open(json_file, "w+", encoding="utf-8")as f:
            json.dump(parama, f)




if __name__ == "__main__":
    main()