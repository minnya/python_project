from tkinter  import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import copy

class Load:
    def __init__(self):
        self.inp=""
        self.root=Tk()
        self.root.title("ReverseGame")
        self.root.geometry("800x600")
        #make window
        Board=Image.open("Icon/board.gif")
        Black=Image.open("Icon/black.png")
        White=Image.open("Icon/white.png")
        Star=Image.open("Icon/star.png")
        Dot=Image.open("Icon/dot.png")
        #image load
        Board=Board.resize((600,600),Image.ANTIALIAS)
        Black=Black.resize((60,60),Image.ANTIALIAS)
        White=White.resize((60,60),Image.ANTIALIAS)
        Star=Star.resize((40,40),Image.ANTIALIAS)
        Dot=Dot.resize((10,10),Image.ANTIALIAS)
        #image resize
        self.board=ImageTk.PhotoImage(Board)
        self.black=ImageTk.PhotoImage(Black)
        self.white=ImageTk.PhotoImage(White)
        self.star=ImageTk.PhotoImage(Star)
        self.dot=ImageTk.PhotoImage(Dot)
        #image load complete
        self.game=Canvas(self.root,width=600,height=600)
        self.game.create_image(-1,0,image=self.board,anchor=NW)
        self.indicator=Canvas(self.root,width=200,height=100,bg="pink")
        
    def load(self):
        f=open("C:/Users/minnya/OneDrive/Document/python/ReverseGame/board.csv","r")
        data=f.readline()
        turn=int(data)
        for i in range(9):
            data=f.readline()
            data=data.rstrip("\n")#最後の改行を消す
            lis[i]=data.split(",")#文字列をリストに変換
            lis[i]=[int(j) for j in lis[i]]#リストの中のstringをintに変換
        f.close()
        return turn,lis
    
#------------描画----------------------------------
    def render(self,X,Y,canvas,Image,Tag):
        x=50+X*72
        y=50+Y*72
        return canvas.create_image(x,y,image=Image,anchor=CENTER,tag=Tag)
    
    def draw(self,lis):
        #draw board
        for i in range(8):
            for j in range(8):
                if lis[j][i]==1:
                    self.render(i,j,self.game,self.black,"black")
                elif lis[j][i]==2:
                    self.render(i,j,self.game,self.white,"white")
                elif lis[j][i]==3:
                    self.render(i,j,self.game,self.star,"star")
                elif lis[j][i]==4:
                    self.render(i,j,self.game,self.dot,"dot")
        self.game.grid(column=0,row=0)

        #self.root.mainloop()

    def indicate(self,turn):
        self.indicator.delete("black","white")
        if turn==0:
            self.indicator.create_text(50,50,text="white",font = ('FixedSys', 30),tag="white")
            self.indicator.create_image(150,50,image=self.white,tag="white")
        elif turn==1:
            self.indicator.create_text(50,50,text="black",font = ('FixedSys', 30),tag="black")
            self.indicator.create_image(150,50,image=self.black,tag="black")            
        #self.indicator.grid(column=1,row=0)
        self.indicator.place(x=600,y=50)

if __name__=="__main__":
    lis=[[""for i in range(9)] for j in range(9)]
    a=Load()
    a.draw(a.load()[1])
    a.indicate(a.load()[0])
    a.root.mainloop()
