#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import msvcrt
import copy
import GUI


global turn
turn=True#Turn is the current stone.True=〇,False=●.
global count1#The number of 〇 stone
global count2#The number of ● stone
count1=count2=cnt=0
    #########################################
    #初期設定
#ここから繰り替えし
if __name__=="__aaaa__":
    while 1:
            if inp=="\r":#エンターを押した場合
                if lis[y][x]==0:#押した場所に何もないとき
                    if reverse(turn)==True:
                        turn = not turn#もし石をひっくり返した場合、交代する
                        save()
            elif inp=="\x1b":#ESCキーで中断
                save()
                sys.exit()
            elif inp==" ":#スペースでパス
                turn=not turn
            elif inp=="r":#盤をリセットする
                while 1:
                    print("Would you like to initialize??\nYES:y\nNo:n\n")
                    inp=msvcrt.getwch()
                    if inp=="y":
                        lis = [[0 for i in range(9)] for j in range(9)]#8×8の盤を用意
                        lis[3][3]=1
                        lis[3][4]=2
                        lis[4][3]=2
                        lis[4][4]=1#初期の石の位置
                        turn=1
                        save()
                        break
                    elif inp=="n":
                        break
                    else:
                        continue
            pos=copy.deepcopy(lis)
            prediction(turn)#石を置ける位置を探す
            pos[y][x]=3#現在のカーソル位置を表示
            for i in range(8):
                count1+=lis[i].count(1)#〇の数を数える
                count2+=lis[i].count(2)#●の数を数える
                cnt+=pos[i].count(4)#石を置ける位置の数
            if cnt==0:#
                turn=not turn#どこにも置けない場合、自動的にパスをする
            a=GUI.Load(turn,lis)
            a.initialize()
            a.draw(pos,self.turn)
            print(a.control())
            display(pos)#盤を表示
            count1=count2=cnt=0
class Process(GUI.Load):
    def __init__(self):
        super().__init__()
        self.x=0
        self.y=0
        self.lis=[[0 for i in range(9)] for j in range(9)]
        self.pos=[[0 for i in range(9)] for j in range(9)]
        self.turn=0
        self.draw(self.load())
        self.indicate(self.turn)
        
    def command(self,comm):
        if comm=="Right":
            self.x+=1
        elif comm=="Left":
            self.x-=1
        elif comm=="Up":
            self.y-=1
        elif comm=="Down":
            self.y+=1
        elif comm=="Return":
            if self.lis[self.y%8][self.x%8]==0:
                if self.reverse(self.turn)==True:
                    self.turn= not self.turn
                    self.indicate(self.turn)
        elif comm=="Escape":
            self.save()
            self.root.destroy()
            exit()
        elif comm=="r":
            self.reset()
        self.game.delete("star","dot","white","black")
        self.prediction(self.turn)
        self.pos[self.y%8][self.x%8]=3
        return self.pos

    def reverse(self,turn):
        pos=copy.deepcopy(self.lis)
        for i in range(-1,2):#左右一個ずつ
            for j in range(-1,2):#上下一個ずつ
                if self.lis[self.y+j][self.x+i]==(turn+1):#もし隣り合う石が自分と違う場合
                    for k in range(1,min(8-(i*self.x)%7,8-(j*self.y)%7)):#その方向の石を全て調べる
                        if self.lis[self.y+j*k][self.x+i*k]==0:
                            break
                        elif self.lis[self.y+j*k][self.x+i*k]==(not turn)+1:#その方向に自分と同じ石を見つけたら
                            for l in range(0,k):
                                self.lis[self.y+j*l][self.x+i*l]=(not turn)+1#その石まですべてを自分の石にする
                            break
                            
        if pos!=self.lis:
            self.pos=copy.deepcopy(self.lis)
            self.draw(self.pos)
            return True

    #石を置ける位置を表示する
    def prediction(self,turn):
        for x in range(8):#まず、盤のすべての石を調べる
            for y in range(8):
                if self.lis[y][x]==turn+1:#もし敵の石があったら
                    for i in range(-1,2):#その石の隣8個の石を調べる
                        for j in range(-1,2):
                            if self.lis[y+j][x+i]==0:#空いてる目があり、かつその反対側が埋まっていたら
                                for k in range(1,min(8-(-i*x)%8,8-(-j*y)%8)):
                                    if self.lis[y-j*k][x-i*k]==0:
                                        break
                                    elif self.lis[y-j*k][x-i*k]==(not turn)+1:#自分の石だったら
                                        self.pos[y+j][x+i]=4
    #盤面の初期化
    def reset(self):
        self.lis = [[0 for i in range(9)] for j in range(9)]#8×8の盤を用意
        self.lis[3][3]=1
        self.lis[3][4]=2
        self.lis[4][3]=2
        self.lis[4][4]=1#初期の石の位置
        self.pos=copy.deepcopy(self.lis)#盤をいじるためにlisをposにコピー
        self.x=self.y=0
        self.pos[self.y][self.x]=3#カーソルの位置は3とする
        self.turn=1
        self.game.delete("black","white","star","dot")
        self.draw(self.pos)
        self.indicate(self.turn)
    #盤面の保存
    def save(self):
        f=open("board.csv","w")
        f.write(str(int(self.turn)))
        f.write("\n")
        for i in range(9):
            f.write(",".join(map(str,self.lis[i])))
            f.write("\n")
        f.close()
    #盤面の読み出し
    def load(self):
        global turn
        f=open("board.csv","r")
        data=f.readline()
        self.turn=int(data)
        for i in range(9):
            data=f.readline()
            data=data.rstrip("\n")#最後の改行を消す
            self.lis[i]=list(map(int,data.split(",")))#文字列をリストに変換
        self.pos=copy.deepcopy(self.lis)
        f.close()
        self.prediction(self.turn)
        self.pos[self.y][self.x]=3
        return self.pos
    #-----------入力操作-----------------------------
    def callback(self,event):
        self.pos=copy.deepcopy(self.lis)
        pos=self.command(event.keysym)
        self.draw(self.lis)
        self.draw(pos)
        self.game.update()
    
    def control(self):
        self.game.bind("<Key>",self.callback)
        self.game.focus_set()
        
if __name__=="__main__":
    pro=Process()
    pro.control()
    pro.root.mainloop()
#--------initialize------------
    
