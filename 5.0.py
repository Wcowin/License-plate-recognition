import tkinter as tk
from tkinter import filedialog, messagebox
from aip import AipOcr
import tkinter.messagebox as mb
import sys
import cv2
# from PIL import Image, ImageTk
sys.setrecursionlimit(2000)
# 显示用户使用须知
# mb.showinfo('用户使用须知','请点击‘选择图片’来输入车牌图片，点击‘退出程序’即可退出界面\n')

while True:
    # 显示是否启动程序的提示框
    result = mb.askyesno('确认', '是否启动程序？')
    if result:
        break
    else:
        # 显示是否退出程序的提示框
        result = mb.askyesno('提示', '您确定要退出程序吗？')
        if result:
            sys.exit()

APP_ID = '30484744'
API_KEY = '09Hrd2L9Mq7OjPrkierenEzq'
SECRET_KEY = 'VqsvmcaAfQaxPSWqnKc0mqsmY5AT550E'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
client.setConnectionTimeoutInMillis(5000)
client.setSocketTimeoutInMillis(5000)

root = tk.Tk()
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 20))
root.title("车牌识别程序")
root.geometry("800x600")

img = None  # 声明全局变量

def open_file_dialog():
    global img  # 使用全局变量
    f_path = filedialog.askopenfilename(filetypes=[('image files', ('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
    if f_path:
        print('\n获取的文件地址:', f_path)
        image = get_file_content(f_path)
        try:
            res = client.licensePlate(image)
            a = res['words_result']['number']
            b = res['words_result']['color']
            img = tk.PhotoImage(file=f_path)
            tk.Label(root, image=img).grid(row=0, column=0, columnspan=2, padx=20, pady=10)  # 显示图片
            tk.Label(root, text="车牌号：", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky=tk.E, padx=20, pady=10)
            tk.Label(root, text=a, font=("Arial", 16)).grid(row=1, column=1, sticky=tk.W, padx=20, pady=10)
            tk.Label(root, text="车牌颜色：", font=("Arial", 16, "bold")).grid(row=2, column=0, sticky=tk.E, padx=20, pady=10)
            tk.Label(root, text=b, font=("Arial", 16)).grid(row=2, column=1, sticky=tk.W, padx=20, pady=10)
        except Exception as e:
            print('车牌识别出现异常：', e)
            messagebox.showerror("错误", "车牌识别失败，请检查您的网络连接或图片格式。")
            return

def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

def exit_program():
    if messagebox.askyesno("提示", "您确定要退出程序吗？"):
        root.destroy()

tk.Label(root, text="选择要识别的图片：", font=("Arial", 16, "bold")).grid(row=3, column=0, sticky=tk.W, padx=20, pady=20)
def show_feedback():
    feedback_info = """意见反馈：
1. 团队负责人微信:153 3458 5195
2. 官方网址:https://v6.chat/pHzNr
3. 技术小哥邮箱:\n wangkewen821@gmail.com
"""
    mb.showinfo('反馈渠道', feedback_info)

feedback_button = tk.Button(root, text="意见反馈", font=("Arial", 16), command=show_feedback)
feedback_button.grid(row=4, column=1, sticky=tk.W, padx=20, pady=20)

def show_feedback1():
    feedback_info = """
请点击‘选择图片’来导入需要识别的车牌图片 \n 点击意见反馈以反馈您的宝贵意见 \n 点击拍摄照片即可拍照识别车牌
"""
    mb.showinfo('用户须知', feedback_info)

feedback_button = tk.Button(root, text="用户须知", font=("Arial", 16), command=show_feedback1)
feedback_button.grid(row=4, column=2, sticky=tk.W, padx=20, pady=20)

open_button = tk.Button(root, text="选择图片", font=("Arial", 16), command=open_file_dialog)
open_button.grid(row=3, column=1, sticky=tk.W, padx=20, pady=20)

# exit_button = tk.Button(root, text="退出程序", font=("Arial", 16), command=exit_program)
# exit_button.grid(row=3, column=2, sticky=tk.W, padx=20, pady=20)
def get_file_content22():
    # with open(filePath, 'rb') as fp:
    #     return fp.read()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
            
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("image.jpg", frame)
            image = get_file_content("image.jpg")
            res = client.licensePlate(image)
            print(res)
            if res.get("words_result"):
                result = res["words_result"]["number"]
                result_var.set(result)
            else:
                result_var.set("未能识别车牌号")
            root.update()  
            cap.release()
            break
    mb.showinfo('结果显示', res["words_result"]["number"])

    
    cv2.destroyAllWindows()
    
open_button = tk.Button(root, text="拍摄图片", font=("Arial", 16), command=get_file_content22)
open_button.grid(row=3, column=2, sticky=tk.W, padx=20, pady=20)    

root.mainloop()

# Written by [Wcowin](https://wcowin.work/) and Yaoshuang
