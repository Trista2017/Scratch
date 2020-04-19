# -*- encoding: utf-8 -*- 
''' 
@File : English_words.py 
@Description: None
@Contact : 17210180033@fudan.edu.cn
@Created info: Yangsj 2020-04-17 11:29
'''

# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
from random import choice
import pandas as pd
import playsound
import tkinter.font as font
from Sql_connect import Connect
sql=Connect('English_words')
import urllib.request

count = 0
# 随机抽单词函数
def next_Random():
    global count,text,word_list,word,counter,url,ans
    count += 1
    word = choice(word_list)
    text.configure(text=word)
    counter.configure(text='第' + str(count) + '个单词')
    ans.config(text ='')
    root.update_idletasks()
    try:
        playsound.playsound(u'D:\\python\\py3\\interest\\English_words\\sound\\' + word + u'.mp3')
    except:
        pass
def search_word():
    global key,word
    word=key.get().lower()
    text.configure(text=word)
    try:
        show_Answer()
        play_sound()
    except:
        ans.config(text='未收录')


# 显示答案
def show_Answer():
    global word,ans
    l=sql.load('word_list where 单词 = \'' + word + '\'')
    if len(l)==1:
        c=l.iloc[0]
        s = c['词性'] + ' ' + c['词义']
        if c['补充信息'] is not None:
            s = s + '\n' + '\n'.join(c['补充信息'].split(';'))
    else:
        s=''
        for k,c in l.iterrows():
            s=s+str(k+1)+'. '+c['词性']+' '+c['词义']
            if c['补充信息'] is not None:
                s=s+'\n   '+'\n   '.join(c['补充信息'].split(';'))
            s+='\n'
    ans.configure(text=s)
    root.update_idletasks()

def play_sound():
    global word
    playsound.playsound(u'D:\\python\\py3\\interest\\English_words\\sound\\' + word + u'.mp3')

#导入单词
def add_words():
    global e1,e2,e3,e4,word_list
    word=e1.get().lower()
    gender=e2.get()
    meaning=e3.get()
    info=e4.get()
    if word is '':
        messagebox.showinfo("提示：", "请先输入内容！")
        return
    data = pd.DataFrame({'单词': [word], '词性': [gender], '词义': [meaning],'补充信息':[info]})
    if ' ' in word:
        urlword =word.replace(' ','%20')
    else:
        urlword=word
    urllib.request.urlretrieve(url + urlword, r'D:\python\py3\interest\English_words\sound\%s.mp3'%word)
    sql.upload(data, 'word_list', if_exists='append')
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    data = sql.load('word_list')
    word_list = list(set(data['单词']))
    return

if __name__ == '__main__':
    data = sql.load('word_list')
    word_list=list(set(data['单词']))
    url='http://dict.youdao.com/dictvoice?type=0&audio='
    root = Tk()
    root.iconbitmap('rainbow.ico')
    root.title('彩虹单词本')
    root.geometry("850x350")
    root.resizable(0, 0)
    #======背单词模块===========================================
    counter = Label(root, fg='red', anchor='se',font=('Arial', 13))
    text = Label(root,text='开始背单词吧',font=('Arial',15, 'bold'),width=20,
      height=10,wraplength = 280)
    ans = Label(root, text='', font=('Arial', 13),width=30,wraplength = 280,
        justify = 'left',height=10,anchor=W)
    Button(root,bg='#43A102',fg='white',font=font.Font(family='Helvetica',size=10,weight="bold"), text="Next", width = 15,command=next_Random).grid(row = 7,column =0)
    Button(root,bg='#A2B700',fg='white',font=font.Font(family='Helvetica',size=10,weight="bold"), text="Answer", width =15,command=show_Answer).grid(row = 7,column =1)
    counter.grid(row=1, column=0)
    text.grid(row = 3,column =0,rowspan=4)
    ans.grid(row = 3,column =1,rowspan=4,sticky=W,columnspan=2)
    Button(root, bg='#EED205',fg='white',font=font.Font(family='Helvetica',size=10,weight="bold"),text="Sound",width = 15, command=play_sound).grid(row=7, column=2)
    # =======搜索单词模块========================================
    Label(root, text="搜索单词：",anchor=E).grid(row=0, column=0)
    key = Entry(root)
    Button(root, bg='#FF8C05',fg='white',font=font.Font(family='Helvetica',size=10,weight="bold"),text="Search", width=15, command=search_word).grid(row=0, column=2)
    key.grid(row=0, column=1)
    # =======上传单词模块========================================
    Label(root, text="请输入单词：").grid(row=3, column=3)
    Label(root, text="请输入词性：").grid(row=4, column=3)
    Label(root, text="请输入词义：").grid(row=5, column=3)
    Label(root, text="请输入补充信息：").grid(row=6, column=3)

    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)
    e4 = Entry(root)
    upload=Button(root,bg='#FDD283',fg='white',font=font.Font(family='Helvetica',size=10,weight="bold") ,text="Upload",width=15,command=add_words).grid(row=7, column=3,columnspan=2)

    e1.grid(row=3, column=4)
    e2 .grid(row=4, column=4)
    e3.grid(row=5, column=4)
    e4.grid(row=6, column=4)
    # ========键盘响应模块========================================
    def eventhandler(event):
        if event.keysym == 'Up':
            add_words()
            e1.focus_set()
        elif event.keysym == 'Down':
            next_Random()
        elif event.keysym == 'Return':
            search_word()
        elif event.keysym == 'space':
            show_Answer()
    btn = Button(root, text='button')
    btn.bind_all('<KeyPress>', eventhandler)
    # =============================================================
    root.mainloop()  # 进入消息循环