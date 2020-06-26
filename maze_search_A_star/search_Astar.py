"""使用A star 算法搜索迷宫的最短路径
"""

import math,os,random,sys
import numpy as np


# 地图设置
gameMapWidth = 10     #地图宽
gameMapHeight = 10    #地图高
gameMap = []

# 地图障碍物坐标  (y,x)
obstacle=[[1,0],
          [1,3],
          [1,8],
          [2,5],
          [3,2],
          [3,6],
          [3,8],
          [5,4],
          [7,2],
          [7,6],
          [9,0],
          [9,2],
          [9,8]]

#块状态
ITEM_STAT_NOMAL = 0  #空点
ITEM_STAT_OBSTACLE = 1  #障碍物
ITEM_STAT_START = 2    #开始点
ITEM_STAT_END = 3     #目标点
ITEM_STAT_PATH = 8   #通路

# 起点和终点由用户输入
snum = 0
enum = 0


# 块属性
class Item:
    def __init__(self,x,y,status):
        self.x = x         #注意矩阵中是（x,y）
        self.y = y
        self.status = status
        self.mf = -1  #启发函数
        self.mg = 0  #代价函数
        self.mh = -1    #差异函数
        self.mparent = None  #父节点
        self.ispath = 0   #是否是通路的一部分
        # self.deep = 0    #搜索深度

# 初始化地图
def initMap(point_start,point_end):
    global snum
    global enum
    for w in range(gameMapWidth):       #注意是从0-9  w是x he是y
        for he in range(gameMapHeight):
            if [w,he] in obstacle:
                gameMap.append(Item(w,he,ITEM_STAT_OBSTACLE))  #确定状态为障碍物
            elif [w,he] == point_start:
                gameMap.append(Item(w,he,ITEM_STAT_START))
                snum = w*gameMapHeight+he
            elif [w,he] == point_end:
                gameMap.append(Item(w,he,ITEM_STAT_END))
                enum = w*gameMapHeight+he
            else:
                gameMap.append(Item(w,he,ITEM_STAT_NOMAL))    #状态为空点

# 输出地图信息
def printMap():
    map=np.zeros([gameMapWidth,gameMapHeight])
    for itemc in range(len(gameMap)):
        if gameMap[itemc].status == ITEM_STAT_START:
            map[gameMap[itemc].x,gameMap[itemc].y] = ITEM_STAT_START
        elif gameMap[itemc].status == ITEM_STAT_END:
            map[gameMap[itemc].x,gameMap[itemc].y] = ITEM_STAT_END
        elif gameMap[itemc].ispath == 1:
            map[gameMap[itemc].x,gameMap[itemc].y] = ITEM_STAT_PATH
        else:
            map[gameMap[itemc].x,gameMap[itemc].y] = gameMap[itemc].status

    print(map)

# 寻路
def findPath():
    global snum
    global enum

    #open表
    openPointList = []
    #close表
    closePointList = []

    # 开启列表插入起始点
    openPointList.append(gameMap[snum])
    print(gameMap[snum].y,gameMap[snum].x)
    count = 1
    while(len(openPointList)>0):   #如果open表不是空表
        #选择f值最小的节点min
        minFpoint = findPointWithMinF(openPointList)
        print(minFpoint.y,minFpoint.x)
        #将节点min从open表移除放到close表
        openPointList.remove(minFpoint)
        closePointList.append(minFpoint)
        #扩展节点min
        surroundList = findSurroundPoint(minFpoint)
        print('第',count,'次扩展\n')


        #处理扩展后的节点
        for sp in surroundList:
            #若扩展节点在open表中,计算扩展节点的f值，与表中的f值比较
            if sp in openPointList:
                newPathG = CalcG(minFpoint)  #因为h值都一样 所以只用比较g 计算新的g值
                if newPathG < sp.mg:         #比较open表中g和现在的g
                    sp.mg = newPathG         #更新
                    sp.mf = sp.mg+sp.mh
                    sp.mparent = minFpoint    #更改父节点
            elif sp in closePointList:
                newPathG = CalcG(minFpoint)  #因为h值都一样 所以只用比较g 计算新的g值
                if newPathG < sp.mg:         #比较open表中g和现在的g
                    sp.mg = newPathG         #更新
                    sp.mf = sp.mg+sp.mh
                    sp.mparent = minFpoint    #更改父节点
                openPointList.append(sp)  #移回open表
                closePointList.remove(sp)
            else:
                sp.mparent = minFpoint  #全新的节点
                CalcF(sp, minFpoint, gameMap[enum])
                openPointList.append(sp)

        if gameMap[enum] in openPointList:
            gameMap[enum].mparent = minFpoint
            break

        count = count+1

    curp = gameMap[enum]
    while True:
        curp.ispath = 1
        curp = curp.mparent
        if curp == None:
            break
    print('\n')
    print('搜索完成\n')
    print('一共扩展',count,'次\n')
    printMap()

def CalcG(minp):
    return minp.mg+1

def CalcF(point, minp, endp):
    h = abs(endp.x-point.x)+abs(endp.y-point.y)
    g = 0
    if point.mparent == None:
        g = 0
    else:
        g = minp.mg+1
    point.mg = g
    point.mh = h
    point.mf = g+h
    return

# 不能是障碍块
def notObstacle(point):
    if point.status != ITEM_STAT_OBSTACLE:
        return True
    return False


# 查找周围块
def findSurroundPoint(point):
    surroundList = []
    up = None
    down = None
    left = None
    right = None

    leftUp = None
    leftDown = None
    rightUp = None
    rightDown = None

    #上边点存在
    if point.x > 0:
        up = gameMap[gameMapHeight*(point.x-1)+point.y]
        if notObstacle(up):
            surroundList.append(up)

    #下边点存在
    if point.x < gameMapWidth-1:
        down = gameMap[gameMapHeight*(point.x+1)+point.y]
        if notObstacle(down):
            surroundList.append(down)

    #左边点存在
    if point.y > 0:
        left = gameMap[gameMapHeight*point.x+point.y-1]
        if notObstacle(left):
            surroundList.append(left)

    #右面点存在
    if point.y < gameMapHeight-1:
        right = gameMap[gameMapHeight*point.x+point.y+1]
        if notObstacle(right):
            surroundList.append(right)

    #左上点存在
    if point.x > 0 and point.y > 0:
        leftUp = gameMap[gameMapHeight*(point.x-1)+point.y-1]
        if notObstacle(leftUp):
            surroundList.append(leftUp)

    #右上点存在
    if point.y < gameMapHeight-1 and point.x > 0:
        rightUp = gameMap[gameMapHeight*(point.x-1)+point.y+1]
        if notObstacle(rightUp):
            surroundList.append(rightUp)

    #左下点存在
    if point.y > 0 and point.x < gameMapWidth-1:
        leftDown = gameMap[gameMapHeight*(point.x+1)+point.y-1]
        if notObstacle(leftDown):
            surroundList.append(leftDown)

    #右下点存在
    if point.x < gameMapWidth-1 and point.y < gameMapHeight-1:
        rightDown = gameMap[gameMapHeight*(point.x+1)+point.y+1]
        if notObstacle(rightDown):
            surroundList.append(rightDown)

    return  surroundList


# 查找列表中的f最小的节点
def findPointWithMinF(openPointList):
    f = 100000
    temp = None
    for pc in openPointList:
        if pc.mf < f:
            temp = pc
            f = pc.mf
    return temp



#入口
if __name__ == '__main__':
    while True:
        x1 = input('请输入起始点x')
        y1 = input('请输入起始点y')
        x2 = input('请输入目标点x')
        y2 = input('请输入目标点y')
        point_start = [int(y1)-1, int(x1)-1]
        point_end = [int(y2)-1, int(x2)-1]
        if point_start in obstacle :
            print('起始点输入错误')
            break
        if point_start in obstacle:
            print('结束点输入错误')
            break
        initMap(point_start,point_end)  #初始化地图
        printMap()       #输出初始化地图信息
        findPath()   #寻找最优路径
        break


































