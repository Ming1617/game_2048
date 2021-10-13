"""
    游戏逻辑控制器，负责处理游戏核心算法
"""
from model import DirectionModel,Location
import random
class GameCoreController:

    def __init__(self):
        self.__list_merge=None
        self.__map=[
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                    ]
        self.__list_empty_location = []

    @property
    def map(self):
        return self.__map

    def __zero_to_end(self):
        """
            零元素移动到末尾
        :return:
        """
        # 从后往前，如果发现0元素，删除并追加
        # -1 -2 -3 -4
        for i in range(-1, -len(self.__list_merge) - 1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    def __merge(self):
        """
            合并
        :return:
        """
        #先将中间的零元素移到末尾
        #再合并相邻元素
        # print(list_merge)
        self.__zero_to_end()
        for i in range(len(self.__list_merge)-1):
            # if list_merge[i]==0 or list_merge[i+1]==0:
            #     break
            if self.__list_merge[i]==self.__list_merge[i+1]:
                self.__list_merge[i]+=self.__list_merge[i+1]
                del self.__list_merge[i+1]
                self.__list_merge.append(0)

    def __move_left(self):
        """
            左移
        :return:
        """
        # 思想：从二维列表中每行交给merge函数进行操作
        # global map
        for line in self.__map:
            self.__list_merge = line
            # print(line)
            self.__merge()

    def __move_right(self):
        """
            向右移动
        :return:
        """
        # 思想:将二维列表的没行（从右向左）交给merge函数操作
        for line in self.__map:
            # 从右向左取出数据 形成新列表
            self.__list_merge = line[::-1]
            # print(list_merge)
            self.__merge()
            # 从右向左接受 合并后的数据
            line[::-1] = self.__list_merge

    def __matrix_transposition(self,matrix):
        """
        方阵转置
        :param matrix: 二维方阵
        :return:
        """
        for c in range(1, len(matrix)):
            for r in range(c, len(matrix)):
                matrix[r][c - 1], matrix[c - 1][r] = matrix[c - 1][r], matrix[r][c - 1]

    def __move_up(self):
        """
            向上移动
        :return:
        """
        self.__matrix_transposition(self.__map)
        self.__move_left()
        self.__matrix_transposition(self.__map)

    def __move_down(self):
        """
            向下移动
        :return:
        """
        self.__matrix_transposition(self.__map)
        self.__move_right()
        self.__matrix_transposition(self.__map)

    def move(self,dir):
        """
            移动
        :param dir: 方向，DirectionModel
        :return:
        """
        if dir == DirectionModel.UP:
            self.__move_up()
        elif dir == DirectionModel.DOWN:
            self.__move_down()
        elif dir == DirectionModel.LEFT:
            self.__move_left()
        elif dir == DirectionModel.RIGHT:
            self.__move_right()

    def generate_new_number(self):
        """
                   生成新数字
        """
        #确定空白位置 1 0
        #思路：选出所有的空白位置(行/列)，在随机挑选一个
        self.get_empty_location()
        if len(self.__list_empty_location)==0:
            return
        loc = random.choice(self.__list_empty_location)
        self.__map[loc.r_index][loc.c_index]= 4 if random.randint(1,10)==1 else 2
       # 因为在该位置生产了新数字，所以该位置就不是空位置了
        self.__list_empty_location.remove(loc)
        #
        # if random.randint(1,10)==1:
        #     self.__map[loc.r_index][loc.c_index]=4
        # else:
        #     self.__map[loc.r_index][loc.c_index] = 2

    def get_empty_location(self):
        #每次统计空位置，都先清空之前的
        self.__list_empty_location.clear()
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])):
                if self.__map[r][c] == 0:
                    self.__list_empty_location.append(Location(r,c))

    def is_game_over(self):
        """
            游戏是否结束
        :return: False表示没有结束 True 表示结束
        """
        #是否具有空位置
        if len(self.__list_empty_location)>0:
            return False

        #判断横向竖向有没有相同的元素
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r]-1)):#0,1,2
                if self.__map[r][c]==self.__map[r][c+1] or self.__map[c][r]==self.__map[c][r+1]:
                    return  False

        return True

# --------测试代码--------
if __name__=="__main__":
    controller=GameCoreController()
    # controller.move_left()
    # print(controller.map)
    # controller.__move_down()
    # print(controller.map)0
    controller.generate_new_number()
    controller.generate_new_number()
    controller.generate_new_number()
    controller.generate_new_number()

    controller.is_game_over()
    print(controller.map)
