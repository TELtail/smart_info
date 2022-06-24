import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import copy
import random
class Map():
    def __init__(self):
        self.mymap = np.zeros((9,9)) #人がいるかどうかのマップ 

class Human():
    def __init__(self,x,y,mymap_con,ax):
        self.x = x
        self.y = y
        self.mymap = mymap_con.mymap
        self.ax = ax
    
    def move(self):
        past_x,past_y = copy.copy(self.x),copy.copy(self.y)
        print(self.select_toilet())

        if self.mymap[self.y+1][self.x] == 0 and self.y != 7:
            self.y += 1
        

        self.mymap[past_y][past_x] = 0
        self.mymap[self.y][self.x] = 1
        self.draw()

    
    def draw(self):
        c = patches.Circle(xy=(self.ac_posi()), radius=0.5, fc='g', ec='r')
        self.ax.add_patch(c)
    
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
            return target_toilet #0,2,4,6,8のどれか
        
        else: #一個でも使われていたら
            null_toilets_list.insert(0,True) #端っこの比較用に追加
            null_toilets_list.insert(-1,True) #端っこの比較用に追加
            target_toilet_candidate = []
            for j,to in enumerate(null_toilets_list[1:-1]):
                if (null_toilets_list[j] == True) and (to == True) and (null_toilets_list[j+2] == True): #対象と両隣が空いていたら
                    target_toilet_candidate.append(j*2)
            if len(target_toilet_candidate) != 0:
                target_toilet = random.choice(target_toilet_candidate) #トイレ候補が見つかったらランダムで決定
                return target_toilet
            else:
                return False

                    

        
        return target_toilet


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
    ax = fig.add_subplot(111)
    mymap_con = Map()
    humans = []
    humans.append(Human(0,0,mymap_con,ax))
    humans.append(Human(2,0,mymap_con,ax))
    humans.append(Human(6,0,mymap_con,ax))


    def plot(data):
        ax.cla()
        plot_init(ax)
        set_ax_lim(ax)
        for h in humans:
            h.move()

        ax.plot(np.random.rand(500))





    ani = animation.FuncAnimation(fig, plot, interval=500,frames=5)
    ax.tick_params( bottom=False,
                    left=False,
                    right=False,
                    top=False)
    plt.show()

if __name__ == "__main__":
    main()