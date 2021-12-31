# -*- coding: utf-8 -*-
"""
Snake 贪吃蛇
"""

from abc import ABC, abstractmethod  # 导入抽象类型和抽象方法属性
from random import randint  # 导入随机整数方法

from pygame import init  # 导入游戏引擎初始化方法
from pygame.color import THECOLORS  # 导入游戏引擎自带的常用 RGB 颜色
from pygame.constants import QUIT, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_f, KEYDOWN  # 导入游戏引擎的常量
from pygame.display import set_mode, set_caption, update  # 导入游戏引擎中有关 GUI 的方法
from pygame.draw import rect  # 导入游戏引擎的矩形绘制方法
from pygame.event import get, Event  # 导入游戏引擎中有关事件的方法
from pygame.font import Font, get_default_font  # 导入游戏引擎用有关字体的方法
from pygame.font import init as font_init  # 导入游戏引擎的字体初始化方法
from pygame.rect import Rect  # 导入游戏引擎提供的矩形区域对象
from pygame.surface import Surface  # 导入游戏引擎提供的平面对象
from pygame.time import Clock  # 导入游戏引擎提供的时钟对象

CAPTION = 'Snake'  # 窗口标题
# CAPTION = '贪吃蛇'  # 窗口标题（中文）
WIDTH = 15  # 地图宽度
BLOCK_WIDTH = 50  # 方块边长
FRAMERATE = 60  # FPS
KEY_BLACK = 'black'  # 黑色
KEY_GREENYELLOW = 'greenyellow'  # 黄绿色
KEY_DARKGREEN = 'darkgreen'  # 深绿色
KEY_ORANGE3 = 'orange3'  # 橘色
KEY_WHITE = 'white'  # 白色
ORIENTATION_UP = 1  # 向上转向
ORIENTATION_LEFT = 2  # 向左转向
ORIENTATION_DOWN = 3  # 向下转向
ORIENTATION_RIGHT = 4  # 向右转向
SNAKE_INTERVAL = 0.25  # 游戏刻间隔时间（秒）
ONE_SECOND = 1  # 一秒（
SNAKE_GAME_SPEED = SNAKE_INTERVAL / (ONE_SECOND / FRAMERATE)  # 计算在当前 FPS 下游戏刻之间的等待次数
HORIZONTAL_ALLOWED = (ORIENTATION_UP, ORIENTATION_DOWN)  # 水平方向转向白名单
VERTICAL_ALLOWED = (ORIENTATION_LEFT, ORIENTATION_RIGHT)  # 垂直方向转向白名单
HORIZONTAL = (K_LEFT, K_RIGHT)  # 横向转向热键
VERTICAL = (K_UP, K_DOWN)  # 纵向转向热键
MAP = {
    K_UP: ORIENTATION_UP,  # 向上转向
    K_LEFT: ORIENTATION_LEFT,  # 向左转向
    K_DOWN: ORIENTATION_DOWN,  # 向下转向
    K_RIGHT: ORIENTATION_RIGHT  # 向右转向
}  # 热键到转向方向映射
SNAKE_INITIAL = (
    (8, 7),
    (7, 7),
    (6, 7)
)  # 初始蛇身
SNAKE_START_LENGTH = len(SNAKE_INITIAL)  # 初始蛇长
MINUS = (
    ORIENTATION_UP,
    ORIENTATION_LEFT
)  # 上、左加
PLUS = (
    ORIENTATION_DOWN,
    ORIENTATION_RIGHT
)  # 右、下减
FONT_SIZE = int(BLOCK_WIDTH / 1.5)  # 相对字体大小
ANTIALIAS = True  # 抗锯齿
font_init()  # 初始化游戏引擎中与字体相关的组件
FONT = Font(get_default_font(), FONT_SIZE)  # 创建系统默认字体
GAME_OVER_TEXT = 'You\'re dead. Press F to get fucked...'  # 游戏结束文字
# GAME_OVER_TEXT = '你已经死了。按下 F 来承认自己搞砸了...'  # 游戏结束文字（中文）
FONT_COLOR = THECOLORS.get(KEY_WHITE)  # 字体颜色
GAME_OVER = FONT.render(GAME_OVER_TEXT, ANTIALIAS, FONT_COLOR)  # 渲染游戏结束文字
SCREEN_WIDTH = WIDTH * BLOCK_WIDTH  # 实际屏幕宽度
SURFACE_SIZE = (SCREEN_WIDTH, SCREEN_WIDTH)  # 实际窗口大小
GAME_OVER_WIDTH, GAME_OVER_HEIGHT = GAME_OVER.get_width(), GAME_OVER.get_height()  # 取得游戏结束文字长宽
GAME_OVER_X = (SCREEN_WIDTH - GAME_OVER_WIDTH) / 2  # 游戏结束文字居中时的横坐标
GAME_OVER_Y = (SCREEN_WIDTH - GAME_OVER_HEIGHT) / 2  # 游戏结束文字居中时的纵坐标
GAME_OVER_POS = (
    GAME_OVER_X,
    GAME_OVER_Y
)  # 横纵坐标合成坐标元组
SCORE_PREFIX = 'Score: %d pt(s)'  # 分数文字前缀
# SCORE_PREFIX = '分数: %d 点'  # 分数文字前缀（中文）
SCORE_POS = (0, 0)  # 分数文字位置
SCORE_STEP = 1  # 分数步长


class _GameWrapper(ABC):  # 游戏包装器
    def __init__(self, _surface: Surface):  # 构造函数
        self.running = False  # 游戏运行状态
        self.surface = _surface  # 所在平面

    def _handle_event(self, _event: Event) -> bool:  # 事件处理器
        if _event.type == QUIT:  # 如果收到退出事件
            self.running = False  # 标记游戏停止状态
            return True  # 阻止继续执行

    def _paint(self):  # 绘制事件
        self.surface.fill(THECOLORS.get(KEY_BLACK))  # 将平面填充为黑色

    @abstractmethod
    def _calc(self):  # 计算事件
        pass  # 抽象方法

    def _main(self):  # 主循环
        clock = Clock()  # 创建时钟
        while self.running:  # 无限循环
            self._paint()  # 绘制图像
            for event in get():  # 从队列获取事件
                self._handle_event(event)  # 回调事件处理器
            update()  # 更新 GUI
            self._calc()  # 回调计算事件
            clock.tick(FRAMERATE)  # 使用时钟来控制帧率

    def launch(self):  # 启动游戏
        """
        Launch the game
        """
        self.running = True  # 标记游戏运行状态
        self._main()  # 进入主循环


def _rand_pos() -> int:  # 获取随机坐标
    return randint(0, WIDTH - 1)  # 返回一个 0 到地图宽度的随机整数


class _SnakeGame(_GameWrapper):  # 贪吃蛇游戏类
    def __init__(self, _surface: Surface):  # 构造函数
        _GameWrapper.__init__(self, _surface)  # 调用父类的构造函数
        self._reset()  # 重置游戏

    def _reset(self):  # 重置游戏方法
        self.snake_length = SNAKE_START_LENGTH  # 蛇长
        self.snake_x = []  # 蛇身横坐标列表
        self.snake_y = []  # 蛇身纵坐标列表
        for x, y in SNAKE_INITIAL:  # 遍历初始的蛇身
            self.snake_x.append(x)  # 向蛇身横坐标列表中追加初始蛇身
            self.snake_y.append(y)  # 向蛇身纵坐标列表中追加初始蛇身
        self._new_food()  # 创建新食物
        self.orientation = ORIENTATION_RIGHT  # 默认面向右侧行动
        self.score = 0  # 分数归零
        self.clock = 0  # 时钟调零
        self.game_running = True  # 标记游戏运行状态
        self.key_event_allowed = True  # 允许键盘事件

    def _get_snake_pos(self) -> tuple:  # 获取蛇身坐标元组
        return tuple(zip(self.snake_x, self.snake_y))  # 横纵坐标列表合成坐标元组

    def _get_snake_separated(self) -> ((int, int), tuple):  # 获取分开的蛇头和蛇身坐标元组
        snake = self._get_snake_pos()  # 获取整个蛇身
        head = snake[0]  # 掐头
        body = snake[1:]  # 除了头是蛇身
        return head, body

    def _get_food_pos(self) -> (int, int):  # 获取新的食物坐标
        food_x, food_y = _rand_pos(), _rand_pos()  # 随机横纵坐标
        for snake_x, snake_y in self._get_snake_pos():  # 遍历蛇身坐标
            if food_x == snake_x and food_y == snake_y:  # 如果重合
                return self._get_food_pos()  # 递归
        return food_x, food_y

    def _new_food(self):  # 新建食物
        self.food_x, self.food_y = self._get_food_pos()  # 生成并设置食物坐标

    def _handle_event(self, _event: Event) -> bool:  # 重写事件处理方法
        if _GameWrapper._handle_event(self, _event):  # 回调父对象事件处理器
            return True  # 如果游戏已经停止就立即返回
        _type = _event.type  # 事件类型
        if _type != KEYDOWN:  # 如果不是键盘按下事件
            return False  # 直接返回
        _key = _event.key  # 按键 ID
        if self.game_running and self.key_event_allowed:  # 如果贪吃蛇游戏正在运行并且允许接受键盘事件
            if _key in HORIZONTAL:  # 如果按键属于横向转向热键
                check = HORIZONTAL_ALLOWED  # 横向转向检查
            elif _key in VERTICAL:  # 如果案件属于纵向转向热键
                check = VERTICAL_ALLOWED  # 纵向转向检查
            else:  # 如果不属于有效按键
                return False  # 直接返回
            if self.orientation in check:  # 如果检查通过
                self.orientation = MAP.get(_key, ORIENTATION_LEFT)  # 根据按键从字典中查找新的方向，并设置
                self.key_event_allowed = False  # 在下一次计算前不要再接受键盘事件
        elif _key == K_f:  # 如果游戏结束，并且 F 键按下
            self._reset()  # 重置游戏

    def _draw_block(self, color: (int, int), x: int, y: int):  # 画方块
        rect(
            self.surface,  # 游戏平面
            color,  # 前景色
            Rect(
                (x * BLOCK_WIDTH, y * BLOCK_WIDTH),
                (BLOCK_WIDTH, BLOCK_WIDTH)
            )  # 笔坐标和矩形边长
        )  # 画矩形

    def _calc(self):  # 计算事件
        global SCORE_STEP  # 获取全局变量 SCORE_STEP
        _GameWrapper._calc(self)  # 回调父对象计算事件
        if self.game_running:  # 如果游戏运行中
            if self.clock < SNAKE_GAME_SPEED:  # 如果等待游戏刻的循环次数不足
                self.clock += 1  # 时钟继续计数
                return  # 结束计算
            self.clock = 0  # 否则时钟归零
            step = -1 if self.orientation in MINUS else 1 if self.orientation in PLUS else 0  # 上、左加，右、下减
            new_x = self.snake_x[0]  # 复制蛇头横坐标
            new_y = self.snake_y[0]  # 复制蛇头纵坐标
            if self.orientation % 2 == 0:  # 如果是水平移动
                new_x += step  # 横坐标加减
            else:  # 否则就是垂直运动
                new_y += step  # 纵坐标加减
            self.snake_x.insert(0, new_x)  # 插入新蛇头横坐标
            self.snake_y.insert(0, new_y)  # 插入新蛇头纵坐标
            if new_x == self.food_x and new_y == self.food_y:  # 如果碰到食物
                self.score += SCORE_STEP  # 加分
                SCORE_STEP *= 2  # 分数步长成倍增加
                self._new_food()  # 创建新食物
            else:  # 如果只是空气
                self.snake_x.pop()  # 末尾横坐标出栈，蛇长守恒
                self.snake_y.pop()  # 末尾横坐标出栈，蛇长守恒
            overflow = new_x not in range(WIDTH) or new_y not in range(WIDTH)  # 蛇头撞墙判定
            head, body = self._get_snake_separated()  # 分别获取蛇头、蛇身坐标
            ouch = head in body  # 蛇头撞入蛇身判定
            if overflow or ouch:  # 以上任何一个条件满足
                self.game_running = False  # 结束游戏
            self.key_event_allowed = True  # 计算完毕，继续接受键盘事件

    def _paint(self):  # 绘图事件
        _GameWrapper._paint(self)  # 回调父对象的绘图事件
        self._draw_block(
            THECOLORS.get(KEY_ORANGE3),  # 某橙色
            self.food_x,
            self.food_y
        )  # 画食物
        head, body = self._get_snake_separated()  # 获得蛇头和蛇身坐标元组
        for block_x, block_y in body:  # 遍历蛇身
            self._draw_block(
                THECOLORS.get(KEY_GREENYELLOW),  # 黄绿色
                block_x,
                block_y
            )  # 画蛇身
        self._draw_block(
            THECOLORS.get(KEY_DARKGREEN),  # 深绿色
            head[0],
            head[1]
        )  # 画蛇头
        score = FONT.render(SCORE_PREFIX % self.score, ANTIALIAS, FONT_COLOR)  # 渲染分数文字
        self.surface.blit(score, SCORE_POS)  # 画分数文字
        if not self.game_running:  # 如果游戏结束
            self.surface.blit(GAME_OVER, GAME_OVER_POS)  # 画游戏结束文字


if __name__ == '__main__':  # 主函数
    init()  # 初始化游戏引擎
    set_caption(CAPTION)  # 设置窗口标题
    surface = set_mode(SURFACE_SIZE)  # 设置窗口大小
    snake_game = _SnakeGame(surface)  # 实例化贪吃蛇游戏
    snake_game.launch()  # 启动游戏
