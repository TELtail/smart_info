import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import copy
import random
import time
class Map():
    def __init__(self):
        self.mymap = np.zeros((8,9)) #人がいるかどうかのマップ 

class Human():
    def __init__(self,x,y,mymap_con,ax,amount,limit):
        self.x = x
        self.y = y
        self.mymap = mymap_con.mymap
        self.ax = ax
        self.target = -2 #targetを見つけようともしていない状態
        self.limit = limit
        self.amount = amount
        self.delete_flag = False
        self.remain = 0
        self.draw()
    
    def move(self):
        if self.amount > 0 and self.y != 7:
            self.limit -= 1
        
        if self.limit <= 0:
            self.dead_human()
            if self.remain == 1:
                self.mymap[self.y][self.x] = 0
                self.mymap[7,self.target] = 0
            return
        


        past_x,past_y = copy.copy(self.x),copy.copy(self.y)
        if self.y == 3 and self.amount > 0:
            self.select_toilet() #所定の位置で空いているトイレを探す
            if self.mymap[self.y+1][self.x] == 0 and self.target >= 0:
                self.y += 1
        
        if self.target == -1 and self.mymap[self.y-1][self.x] == 1:
            self.select_toilet_helplessly()
            if self.target >=0:
                self.y += 1
        
        elif self.target >= 0: #targetが存在するなら
            self.go_to_target()


        elif self.target == -1: #targetを探したが、見つからなかった状態
            pass

        elif self.target == -3: #トイレ終了していたら
            self.y -= 1
        
        elif self.mymap[self.y+1][self.x] == 0 and self.y != 7: #前に誰もいない、かつトイレの前にいない場合前進
            self.y += 1

        if self.amount <= 0 and self.y == 7: #トレイを済ませたら
            self.limit = 30
            targeted = copy.copy(self.target)
            self.target = -3 #トイレを済ませたことを意味する
            if targeted == 0:
                self.x += 1
            if targeted == 2 or targeted == 4 or targeted ==6:
                self.x += random.choice([-1,1])
            if targeted == 8:
                self.x -= 1
        

        if self.y < 0:
            self.delete_flag = True
            self.mymap[past_y][past_x] = 0

        if self.y == 7:
            self.amount -= 1 #放尿
        

        
        
        if self.delete_flag == False:
            self.mymap[past_y][past_x] = 0
            self.mymap[self.y][self.x] = 1
            self.draw()

    
    def draw(self):
        if self.amount <= 0:
            fc_color = "m"
        elif self.limit > 10:
            fc_color = "g"
        elif self.limit > 5:
            fc_color = "y"
        elif self.limit > 0:
            fc_color = "r"
        elif self.limit <= 0:
            fc_color = "k"

        c = patches.Circle(xy=(self.ac_posi()), radius=0.5, fc=fc_color)
        self.ax.add_patch(c) #人間の描画
        self.ax.text(self.txt_posi()[0],self.txt_posi()[1],self.limit,size=15) #文字の描画
    
    def go_to_target(self):

        if self.x > self.target:
            self.x -= 1
            return
        
        elif self.x < self.target:
            self.x += 1
            return
        
        elif self.x == self.target and self.y != 7:
            self.y += 1
            return
    
    def select_toilet(self):
        toilets = [0,2,4,6,8]
        null_toilets_list = [0]*len(toilets)
        for i,toil in enumerate(toilets): #空いているトイレを検索
            if self.mymap[7,toil] == 0:
                null_toilets_list[i] = True #空いていたらTrue
            else:
                null_toilets_list[i] = False #空いていなかったらFalse
        
        if null_toilets_list.count(True) == len(toilets):
            target_toilet = random.choice(toilets) #トイレが全部空いてたら好きなところに入る
            self.target = target_toilet #0,2,4,6,8のどれか
            self.mymap[7,target_toilet] = 2 #トイレ予約

        else: #一個でも使われていたら
            null_toilets_list.insert(0,True) #端っこの比較用に追加
            null_toilets_list.append(True) #端っこの比較用に追加
            target_toilet_candidate = []
            for j in range(1,6):
                
                if (null_toilets_list[j-1] == True) and (null_toilets_list[j] == True) and (null_toilets_list[j+1] == True): #対象と両隣が空いていたら
                    target_toilet_candidate.append(toilets[j-1])
            if len(target_toilet_candidate) != 0:
                target_toilet = random.choice(target_toilet_candidate) #トイレ候補が見つかったらランダムで決定
                self.target = target_toilet
                self.mymap[7,target_toilet] = 2 #トレイ予約
            else:
                self.target = -1 #見つからないときは-1
    
    def select_toilet_helplessly(self):
        toilets = [0,2,4,6,8]
        null_toilets = []
        for i,toil in enumerate(toilets): #空いているトイレを検索
            if self.mymap[7,toil] == 0:
                null_toilets.append(toil)
        if len(null_toilets) != 0:
            self.target = random.choice(null_toilets)
            self.mymap[7,self.target] = 2
        else:
            self.target = -1

    def dead_human(self):
        self.remain += 1
        c = patches.Circle(xy=(self.ac_posi()), radius=0.5-self.remain*0.1, fc="k")
        self.ax.add_patch(c) #人間の描画
        if self.remain == 3:
            self.delete_flag = True
            global dead_num
            dead_num += 1



    def ac_posi(self):
        act_x = float(self.x)*1.25 + 0.625
        act_y = float(self.y)*1.25 + 0.625
        return (act_x,act_y)
    
    def txt_posi(self):
        act_x = float(self.x)*1.25 + 0.45
        act_y = float(self.y)*1.25 + 0.45
        return (act_x,act_y)


def plot_init(ax):
    toilets = []
    for i in range(5):
        r = patches.Rectangle(xy=(2.5*i, 10), width=1.25, height=1, ec='#000000', fill=True)
        toilets.append(r)
        ax.add_patch(r)

def set_ax_lim(ax):
    ax.grid(which="major",alpha=1)
    ax.grid(which="minor",alpha=0.3)
    ax.set_xticks(np.linspace(0,11.25,10))
    ax.set_yticks(np.linspace(0,11.25,10))
    ax.set_xlim(0,11.25)
    ax.set_ylim(0,11.25)
    ax.text(0,0.5,"Dead_num: "+str(dead_num),size=15)
    ax.tick_params(labelbottom=False,
                labelleft=False,
                labelright=False,
                labeltop=False)


def main():
    fig = plt.figure(figsize=(8,8))
    human_freq = 3
    
    amount = 20
    ax = fig.add_subplot(111)
    mymap_con = Map()
    humans = []
    global dead_num
    dead_num = 0
    global time_freq
    time_freq=0

    def plot(data):
        global time_freq
        time_freq += 1
        delete_humans_list = []
        ax.cla()
        plot_init(ax)
        set_ax_lim(ax)
        for i,h in enumerate(humans):
            h.move()
            if h.delete_flag:
                delete_humans_list.append(i)
        
        for j in reversed(delete_humans_list):
            del humans[j]
        

        limit = random.randint(10,25)
        amount = random.randint(15,25)
        if int(time_freq)%human_freq == 0 and mymap_con.mymap[0][4] != 1:
            humans.append(Human(4,0,mymap_con,ax,amount,limit))



    ani = animation.FuncAnimation(fig, plot, interval=1000,frames=1000)
    ani.save("plot17.mp4",writer="ffmpeg",dpi=500)
    plt.show()

if __name__ == "__main__":
    main()