#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import msvcrt
import copy

global turn
turn=True#Turn is the current stone.True=〇,False=●.
global count1#The number of 〇 stone
global count2#The number of ● stone
count1=count2=cnt=0
########################################
#Display the board on the screen.
def display(osero):
    global count1,count2
    os.system("cls")
#Firstly, show the current stone color.
    print("Current:",end="")
    if turn==0:
        print("●")
    elif turn==1:
        print("○")
#Then, show the board.
    for x in range(0,8):
        print(" ----+----+----+----+----+----+----+----")
        for y in range(0,8):
            if osero[x][y]==0:
                print("|    ",end="")
            elif osero[x][y]==1:
                print("| 〇 ", end="")
            elif osero[x][y]==2:
                print("| ● ", end="")
            elif osero[x][y]==3:
                print("| ★ ", end="")
            elif osero[x][y]==4:
                print("| ・ ", end="")
        print("|")
    print(" ----+----+----+----+----+----+----+----")
    print("〇:",count1,"●:",count2)
#########################################
def reverse(turn):
    pos=copy.deepcopy(lis)
    for i in range(-1,2):#左右一個ずつ
        for j in range(-1,2):#上下一個ずつ
            if lis[y+j][x+i]==(turn+1):#もし隣り合う石が自分と違う場合
                for k in range(1,min(8-(i*x)%7,8-(j*y)%7)):#その方向の石を全て調べる
                    if lis[y+j*k][x+i*k]==0:
                        break
                    elif lis[y+j*k][x+i*k]==(not turn)+1:#その方向に自分と同じ石を見つけたら
                        for l in range(0,k):
                            lis[y+j*l][x+i*l]=(not turn)+1#その石まですべてを自分の石にする
    if pos!=lis:
        return True
#########################################
#石を置ける位置を表示する
def prediction(turn):
    global pos
    for x in range(8):#まず、盤のすべての石を調べる
        for y in range(8):
            if lis[y][x]==turn+1:#もし敵の石があったら
                for i in range(-1,2):#その石の隣8個の石を調べる
                    for j in range(-1,2):
                        if lis[y+j][x+i]==0:#空いてる目があり、かつその反対側が埋まっていたら
                            for k in range(1,min(8-(-i*x)%8,8-(-j*y)%8)):
                                if lis[y-j*k][x-i*k]==0:
                                    break
                                elif lis[y-j*k][x-i*k]==(not turn)+1:#自分の石だったら
                                    pos[y+j][x+i]=4
#########################################
def save():
    global turn
    f=open("board.csv","w")
    f.write(str(int(turn)))
    f.write("\n")
    for i in range(9):
        f.write(",".join(map(str,lis[i])))
        f.write("\n")
    f.close()
#########################################
def load():
    global turn
    f=open("board.csv","r")
    data=f.readline()
    turn=int(data)
    for i in range(9):
        data=f.readline()
        data=data.rstrip("\n")#最後の改行を消す
        lis[i]=data.split(",")#文字列をリストに変換
        lis[i]=[int(j) for j in lis[i]]#リストの中のstringをintに変換
    f.close()    
#########################################
#初期設定
lis = [[0 for i in range(9)] for j in range(9)]#8×8の盤を用意
load()
lis[3][3]=1
lis[3][4]=2
lis[4][3]=2
lis[4][4]=1#初期の石の位置
pos=copy.deepcopy(lis)#盤をいじるためにlisをposにコピー
x=y=0
pos[y][x]=3#カーソルの位置は3とする
display(pos)

#ここから繰り替えし
while 1:
    if msvcrt.kbhit():
        load()
        inp=msvcrt.getwch()
        pos[y][x]=0
        if inp=="à":
            inp=msvcrt.getwch()
            if inp=="H":#↑
                y-=1
            elif inp=="P":#↓
                y+=1
            elif inp=="M":#→
                x+=1
            elif inp=="K":#←
                x-=1
            if x<0 or x>=8:#枠を超えたら最初に戻す
                x=x%8
            elif y<0 or y>=8:#枠を超えたら最初に戻す
                y=y%8
        elif inp=="\r":#エンターを押した場合
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
        display(pos)#盤を表示
        count1=count2=cnt=0
