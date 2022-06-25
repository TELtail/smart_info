import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import copy
import random
import time
class Map():
    def __init__(self):
        self.mymap = np.zeros((9,9)) #人がいるかどうかのマップ 

class Human():
    def __init__(self,x,y,mymap_con,ax,amount):
        self.x = x
        self.y = y
        self.mymap = mymap_con.mymap
        self.ax = ax
        self.target = -2 #targetを見つけようともしていない状態
        self.limit = 30
        self.amount = amount
        self.delete_flag = False
        self.draw()
    
    def move(self):
        self.limit -= 1
        past_x,past_y = copy.copy(self.x),copy.copy(self.y)
        if self.y == 2 and self.amount > 0:
            self.select_toilet() #所定の位置で空いているトイレを探す
            if self.mymap[self.y+1][self.x] == 0:
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
            self.target = -3
            if targeted == 0:
                self.x += 1
            if targeted == 2 or targeted == 4 or targeted ==6:
                self.x += random.choice([-1,1])
            if targeted == 8:
                self.x -= 1
        if self.y < 0:
            self.delete_flag = True



        if self.y == 7:
            self.amount -= 1
        
        self.mymap[past_y][past_x] = 0
        self.mymap[self.y][self.x] = 1
        self.draw()

    
    def draw(self):
        if self.limit > 10:
            fc_color = "g"
        elif self.limit > 5:
            fc_color = "y"
        elif self.limit > 0:
            fc_color = "r"
        elif self.limit <= 0:
            fc_color = "k"

        c = patches.Circle(xy=(self.ac_posi()), radius=0.5, fc=fc_color, ec='r')
        self.ax.add_patch(c)
    
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
        
        else: #一個でも使われていたら
            null_toilets_list.insert(0,True) #端っこの比較用に追加
            null_toilets_list.insert(-1,True) #端っこの比較用に追加
            target_toilet_candidate = []
            for j,to in enumerate(null_toilets_list[1:-1]):
                if (null_toilets_list[j] == True) and (to == True) and (null_toilets_list[j+2] == True): #対象と両隣が空いていたら
                    target_toilet_candidate.append(j*2)
            if len(target_toilet_candidate) != 0:
                target_toilet = random.choice(target_toilet_candidate) #トイレ候補が見つかったらランダムで決定
                self.target = target_toilet
            else:
                self.target = -1 #見つからないときは-1


    def ac_posi(self):
        act_x = float(self.x)*1.25 + 0.625
        act_y = float(self.y)*1.25 + 0.625
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



def main():
    fig = plt.figure(figsize=(8,8))
    human_freq = 10
    amount = 5
    ax = fig.add_subplot(111)
    mymap_con = Map()
    humans = []

    start_time = time.time()

    def plot(data):
        delete_humans_list = []
        ax.cla()
        plot_init(ax)
        set_ax_lim(ax)
        for i,h in enumerate(humans):
            h.move()
            if h.delete_flag:
                delete_humans_list.append(i)
        
        for j in delete_humans_list:
            del humans[j]


        if int(time.time() - start_time)%human_freq == 0:
            humans.append(Human(3,0,mymap_con,ax,amount))




    ani = animation.FuncAnimation(fig, plot, interval=1000,frames=1000)
    ax.tick_params( bottom=False,
                    left=False,
                    right=False,
                    top=False)
    plt.show()

if __name__ == "__main__":
    main()