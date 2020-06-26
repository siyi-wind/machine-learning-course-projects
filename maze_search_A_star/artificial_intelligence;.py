import numpy as np
import sys

if __name__ == "__main__":
    chess = np.zeros((12, 12), dtype=int)
    for i in range(12):
        chess[0][i] = -1
        chess[11][i] = -1
        chess[i][0] = -1
        chess[i][11] = -1

    chess[2][1] = chess[2][4] = chess[2][9] = -1
    chess[3][6] = -1
    chess[4][3] = chess[4][7] = chess[4][9] = -1
    chess[6][5] = -1
    chess[8][3] = chess[8][7] = -1
    chess[10][1] = chess[10][3] = chess[10][9] = -1

    move = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])

    x = 9
    y = 1
    x_goal = 5
    y_goal = 10
    w = 0
    route = np.array([x, y])

    if (chess[x_goal][y_goal]==-1):
        print("No result")
        sys.exit(1)
    while (1):
        """ selected node == goal ?"""
        if x == x_goal and y == y_goal:
            print("reach successfully!")
            print("best route:")
            for i in range(w + 1):
                print('(', route[i][0], route[i][1],')', end=' --> ')
            print(w, 'steps in total')
            break


        w = w + 1
        cost_min = 1000
        for i in range(8):
            """ have blocks? """
            x_tmp = x + move[i][0]
            y_tmp = y + move[i][1]
            if chess[x_tmp][y_tmp] == -1:
                continue

            cost_tmp = abs(x_tmp - x_goal) + abs(y_tmp - y_goal) + w  # f=h+w
            print('(', x_tmp, y_tmp, ')', cost_tmp, end='  ')
            if cost_tmp < cost_min:
                cost_min = cost_tmp
                x_min = x + move[i][0]
                y_min = y + move[i][1]
        x = x_min
        y = y_min
        print('\nselect (', x, y, ')')
        route = np.row_stack((route,[x,y]))
