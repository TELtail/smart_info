import matplotlib.pyplot as plt
import matplotlib.animation as animation

def cellautomaton(l_bit, rule, pattern=False, padding=0):
    # pattern: 周期的境界条件, padding: 枠外のセルの値
    l_bit_new = []
    if not pattern:
        l_bit = [padding] + l_bit
        l_bit.append(padding)
    else:
        l_bit = [l_bit[-1]] + l_bit
        l_bit.append(l_bit[1])
    for i in range(1, len(l_bit)-1):
        l_bit_new.append(next_state(l_bit[i-1],l_bit[i],l_bit[i+1], rule))
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
    rule = 110 # ルール番号(0~255)
    fig = plt.figure()
    plt.title("rule{}".format(rule))
    
    
    ## リストxで初期状態を指定

    result = [[0]*200]*loop
    result[0][40] = 1

    for i in range(loop-1):
        x = cellautomaton(result[i], rule, pattern=False)
        result[i+1] = x
        im = plt.imshow(result, cmap="binary",animated=True)
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
    plt.show()

main()