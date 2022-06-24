import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


class Toilet():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.use = 0

class Human():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def move(self,map):
        if map[self.x][self.y+1] == 0 and self.y != 7:
            self.y += 1

    
    def draw(self,ax):
        c = patches.Circle(xy=(self.ac_posi()), radius=0.5, fc='g', ec='r')
        ax.add_patch(c)
    
    def select_toile(self,map):
        pass

    def ac_posi(self):
        act_x = float(self.x)*1.25 + 0.625
        act_y = float(self.y)*1.25 + 0.625
        return (act_x,act_y)


def plot_init(ax):
    toiles = []
    for i in range(5):
        r = patches.Rectangle(xy=(2.5*i, 10), width=1.25, height=1, ec='#000000', fill=True)
        toiles.append(r)
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


    map = np.zeros((8,9)) #人がいるかどうかのマップ
    h = Human(2,2)
    def plot(data):
        ax.cla()
        plot_init(ax)
        set_ax_lim(ax)
        
        h.move(map)
        map[h.x][h.y] = 1
        h.draw(ax)
        ax.plot(np.random.rand(500))

    ani = animation.FuncAnimation(fig, plot, interval=500,frames=5)
    ax.tick_params( bottom=False,
                    left=False,
                    right=False,
                    top=False)
    plt.show()

if __name__ == "__main__":
    main()