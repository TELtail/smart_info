import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    def plot(data):
        ax.cla()                      # 現在描写されているグラフを消去
        rand = np.random.randn(100)    # 100個の乱数を生成
        im = ax.plot(rand)            # グラフを生成

    ani = animation.FuncAnimation(fig, plot, interval=100,frames=10)
    ax.tick_params(labelbottom=False,
                    labelleft=False,
                    labelright=False,
                    labeltop=False,
                    bottom=False,
                    left=False,
                    right=False,
                    top=False)
    plt.show()

if __name__ == "__main__":
    main()