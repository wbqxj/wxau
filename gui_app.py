import tkinter as tk
from tkinter import scrolledtext
import random
import time
import datetime
from wxauto import *
from zhipuai import ZhipuAI

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.output_text = ""
        
        # 初始密码生成和显示
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)
        self.c = random.randint(1, 9)
        self.d = random.randint(1, 9)
        self.e = random.randint(1, 9)
        self.append_output(f"初始密码为 {self.a} {self.b} {self.c} {self.d} {self.e} 请将该密码发送给到QQ'2589511829'获取验证码")
        self.append_output("请登录微信后运行程序")
        
    def create_widgets(self):
        # 输出显示区域
        self.output_area = scrolledtext.ScrolledText(self, width=90, height=20)
        self.output_area.pack(side="top")
        
        # 输入框
        self.input_label = tk.Label(self, text="请输入验证码:")
        self.input_label.pack(side="left")
        
        self.input_entry = tk.Entry(self)
        self.input_entry.pack(side="left")
        
        # 运行按钮
        self.run_button = tk.Button(self, text="运行", command=self.run_program)
        self.run_button.pack(side="bottom", anchor="sw", padx=200, pady=10)
        
        # 退出按钮
        self.exit_button = tk.Button(self, text="退出", command=self.exit_program)
        self.exit_button.pack(side="bottom", expand=True)
        
    def append_output(self, text):
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)
        
    def exit_program(self):
        self.master.destroy()
        
    def run_program(self):
        v = self.input_entry.get()
        try:
            v = int(v)
            self.process_verification(v)
        except ValueError:
            self.append_output("请输入有效的数字验证码")
            
    def process_verification(self, v):
        
        # 加密随机密码
        v_calc = self.a+self.e
        b_calc = v_calc*self.d
        n = v_calc*self.a+b_calc
        p = v_calc+b_calc+n
        o = n*b_calc
        m = self.a*self.c+10+v_calc+b_calc*n+p+v_calc+b_calc+n*o/8
        integer_part = int(m)
        
        self.append_output("提示: 窗口关闭后验证码失效需从新获取验证码")
        # self.append_output(str(integer_part))
        
        if v == integer_part:
            self.append_output("验证成功")
            self.append_output("此程序使用了glm-4-Flash模型 API接口")
            
            import threading
            def message_listener():
                wx = WeChat()
                star_time = datetime.datetime.now()
                while True:
                    try:
                        aa = wx.GetAllNewMessage()
                        time.sleep(2)
                        for p in aa:
                            b_msg = aa[p]
                            if len(b_msg) == 2:
                                b_msg = b_msg[1]
                            else:
                                b_msg = b_msg[0]
                            self.append_output(f'你的好友 {p} 发来消息说 {b_msg}')
                            
                            client = ZhipuAI(api_key="79b0e97cbc4b54ea079d512d48b24236.oDLDBH0PubpCNwTW")
                            user_input = str(b_msg)
                            response = client.chat.completions.create(
                                model="GLM-4-Flash",
                                messages=[
                                    {"role": "system", 
                                     "content": "你的身份是李明华，口头禅是吴果颠埋斯和太八涨呐跌无，你负责和用户聊天让用户感到无语说话要高冷回复简短显得不耐烦"},
                                    {"role": "user", 
                                     "content": user_input}
                                ]
                            )
                            reply = response.choices[0].message.content
                            self.append_output(f'回复 {reply}')
                            wx.SendMsg(reply, p)
                            wx.ChatWith(who="文件传输助手")
                        
                        current_time = datetime.datetime.now()
                        runtime = current_time - star_time
                        self.append_output(f'时间 {current_time} 程序运行时长：{runtime} 监听中暂无消息........')
                    except Exception as e:
                        self.append_output(f"发生错误: {str(e)}")
                        break
            
            thread = threading.Thread(target=message_listener, daemon=True)
            thread.start()
        else:
            self.append_output("验证失败，验证码错误")

root = tk.Tk()
root.title("版本号: 1.0，开发者: W冰清")
app = Application(master=root)
app.mainloop()