import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def cellautomaton(l_bit, rule, padding=0):
    # pattern: 周期的境界条件, padding: 枠外のセルの値
    l_bit_new = np.zeros(200)

    l_bit = [l_bit[-1]] + l_bit
    l_bit.append(l_bit[1])
    for i in range(1, len(l_bit)-1):
        l_bit_new[i] = (next_state(l_bit[i-1],l_bit[i],l_bit[i+1], rule))
    return l_bit_new

def next_state(l, x, r, rule):
    # 次のセルの状態を決定
    bin_str = format(rule, '08b')
    bin_num = int(str(l)+str(x)+str(r), 2)
    return int(bin_str[-(bin_num+1)])

def main():
    result = []
    ims = []
    loop = 200
    rule = 254 # ルール番号(0~255)
    fig = plt.figure()
    plt.title("rule{}".format(rule))
    
    
    ## リストxで初期状態を指定

    result = np.zeros(loop,200)
    print(result)
    result[0][30] = 1
    print(result)

    for i in range(loop-1):
        x = cellautomaton(result[i], rule)
        result[i+1] = x
        im = plt.imshow(result, cmap="binary",animated=True)
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
    plt.show()

main()