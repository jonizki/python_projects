import math

#Start pos
x,y = 863,587

#End pos
x_to,y_to = 734,497

for i in range(1000):
    x_lul = x_to-i
    A = abs(x-x_lul)
    B = abs(y-y_to)

    length = int(math.hypot(A,B))
    print("length: " + str(length) + " " + "x_to:" + str(x_lul))
