import pygame

from init_ import *

class Board_Play():

    def __init__(self):
        self.status = ''
        self.select = [None, None]
        self.time_ = ''
        self.mask = ''
        self.time_fault = 0
        self.color = EMPTY

    def draw(self, time_, type_, win_lose):

        if win_lose != 0:
            self.status = ''

        SCREEN.fill(WHITE)
        displaySurface((WINDOWWIDTH, WINDOWHEIGHT), BLACK, SCREEN, 0, 0, True, 0, 0)

        for j in range(int(NUM_Y / 3)):
            for i in range(int(NUM_X / 3)):
                displaySurface((WIDTH * 3 + BLANK * 2, HEIGHT * 3 + BLANK * 2), SILVER, SCREEN, i, j)

        for j in range(NUM_Y):
            for i in range(NUM_X):
                if i == self.select[0] or j == self.select[1]:
                    color = self.color
                else:
                    color = WHITE
                displaySurface((WIDTH, HEIGHT), color, SCREEN, i, j)

        index = 0
        for j in range(NUM_Y):
            for i in range(NUM_X):
                if self.mask != '':
                    if self.mask[index] == '1':
                        displaySurface((WIDTH, HEIGHT), RED, SCREEN, i, j)
                index += 1

        display(20, self.status, RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 30)
        display(20, 'Fault', RED, WINDOWWIDTH / 4, 0, 100, WINDOWHEIGHT)
        display(20, str(self.time_fault) + '/3', RED, WINDOWWIDTH / 4, 0, 100, WINDOWHEIGHT + 20)

        display(20, 'Time', RED, WINDOWWIDTH / 4, WINDOWWIDTH / 4, 100, WINDOWHEIGHT)
        display(20, str(time_), RED, WINDOWWIDTH / 4, WINDOWWIDTH / 4, 100, WINDOWHEIGHT + 20)

        if type_ == 0:
            display(20, 'Mode', RED, WINDOWWIDTH / 4, WINDOWWIDTH / 2, 100, WINDOWHEIGHT)
            display(20, 'Fill', RED, WINDOWWIDTH / 4, WINDOWWIDTH / 2, 100, WINDOWHEIGHT + 20)
        else:
            display(20, 'Mode', RED, WINDOWWIDTH / 4, WINDOWWIDTH / 2, 100, WINDOWHEIGHT)
            display(20, 'Note', RED, WINDOWWIDTH / 4, WINDOWWIDTH / 2, 100, WINDOWHEIGHT + 20)

        display(20, 'Reset', RED, WINDOWWIDTH / 4, WINDOWWIDTH * 3 / 4, 100, WINDOWHEIGHT)
        display(20, 'Press "R"', RED, WINDOWWIDTH / 4, WINDOWWIDTH * 3 / 4, 100, WINDOWHEIGHT + 20)

    def update(self, pos, color):
        if pos != -1:
            self.select = pos

        self.color = color

    def mask_(self, inpt):
        self.mask = str(inpt[0])
        self.status = inpt[1]
        if self.status == 'A wrong value!':
            self.time_fault += 1

    def lose_(self):

        if self.time_fault == 3:
            return True
        else:
            return False

    def out(self):
        return self.select

    def reset(self):
        self.status = ''
        self.time_ = ''
        self.mask = ''
        self.time_fault = 0
        self.color = EMPTY

class Number_Play():

    def __init__(self):
        self.position_ = ''
        self.fill = BoardBase
        self.select = []
        self.lock = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        self.mask = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        self.answer = ''
        self.fault = ''

    def selecT(self, pos):
        self.select = pos

    def start(self, bo):
        self.position_ = bo[1]
        self.answer = bo[2]

    def draw(self):

        fill = encodeBoard(self.fill)
        index = 0
        for j in range(NUM_X):
            for i in range(NUM_Y):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if fill[index] != '0':
                    display(30, fill[index], BLUE, WIDTH, x, HEIGHT, y)
                index += 1

        index = 0
        for j in range(NUM_X):
            for i in range(NUM_Y):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if self.position_[index] != '0':
                    display(30, self.position_[index], BLACK, WIDTH, x, HEIGHT, y)
                index += 1

    def update(self, num):

        index = 0
        for i in range(self.select[1]):
            index += 9
        for i in range(self.select[0]):
            index += 1

        if self.select != [] and num != None and self.lock[index] == '0' and self.position_[index] == '0':
            self.fill[self.select[1]][self.select[0]] = num
        elif self.lock[index] == '1':
            self.fault = "You can't fill a correct cell again"

        fill = encodeBoard(self.fill)
        for i in range(len(fill)):
            if fill[i] != '0' and fill[i] == self.position_[i]:
                self.fill[i] = '0'

        if fill[index] == self.answer[index] and self.lock[index] == '0' and self.position_[index] == '0':
            self.fault = 'Correct!'
        elif fill[index] != self.answer[index] and self.lock[index] == '0' and self.position_[index] == '0':
            self.fault = 'A wrong value!'

        self.mask = ''
        self.lock = ''
        for i in range(len(fill)):
            if fill[i] != '0' and fill[i] != self.answer[i]:
                self.mask += '1'
            else:
                self.mask += '0'

            if fill[i] != '0' and fill[i] == self.answer[i]:
                self.lock += '1'
            elif fill[i] == '0' and fill[i] == self.answer[i]:
                self.lock += '0'
            elif fill[i] != self.answer[i]:
                self.lock += '0'

    def win_(self):
        count = 0

        for i in range(len(self.position_)):
            if self.position_[i] != '0':
                count += 1

        fill = encodeBoard(self.fill)
        for i in range(len(fill)):
            if fill[i] != '0':
                count += 1

        count_fault = 0
        for i in range(len(self.mask)):
            if self.mask[i] != '0':
                count_fault += 1

        if count == NUM_X * NUM_Y and count_fault == 0:
            return True
        else:
            return False

    def out(self):
        return [self.mask, self.fault]

    def out_lock_position(self):

        fill = encodeBoard(self.fill)
        save_lock = self.lock
        self.lock = ''
        for i in range(len(fill)):
            if self.position_[i] != '0' or save_lock[i] == '1':
                self.lock += '1'
            else:
                self.lock += '0'
        return self.lock

    def out_process(self):
        out = ''
        fill = encodeBoard(self.fill)
        for i in range(len(fill)):
            if self.mask[i] != '1':
                if self.position_[i] != '0':
                    out += self.position_[i]
                elif fill[i] != '0':
                    out += fill[i]
                else:
                    out += '0'
            else:
                out += '0'

        return out

    def reset(self):
        self.fill = BoardBase
        self.select = []
        self.lock = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        self.mask = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        self.fault = ''

class Note_Play():

    def __init__(self):
        self.select = []
        self.element = [
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000']]

    def selecT(self, pos):
        self.select = pos

    def draw(self):
        for j in range(NUM_Y):
            for i in range(NUM_X):
                x = WIDTH * i + BLANK * (i + 1)
                y = HEIGHT * j + BLANK * (j + 1)
                self.draw_ele(y, x, self.element[i][j])

    def draw_ele(self, x, y, str1):
        ele = pygame.Surface((WIDTH, HEIGHT), SRCALPHA)
        font = pygame.font.SysFont('consolas', 15)
        index = 0
        for j in range(3):
            for i in range(3):
                if str1[index] == '1':
                    surface = font.render(str(index + 1), True, RED)
                    size = surface.get_size()
                    posx = (WIDTH / 3 - size[0]) / 2 + WIDTH / 3 * i
                    posy = (HEIGHT / 3 - size[1]) / 2 + HEIGHT / 3 * j
                    ele.blit(surface, (posx, posy))
                index += 1

        SCREEN.blit(ele, (x, y))

    def update(self, num):
        save = self.element[self.select[1]][self.select[0]]
        self.element[self.select[1]][self.select[0]] = ''
        for i in range(9):
            if i == num - 1:
                if save[i] == '0':
                    self.element[self.select[1]][self.select[0]] += '1'
                if save[i] == '1':
                    self.element[self.select[1]][self.select[0]] += '0'
            else:
                self.element[self.select[1]][self.select[0]] += str(save[i])

    def update2(self, lock_position):
        index = 0
        for j in range(NUM_Y):
            for i in range(NUM_X):
                if lock_position[index] == '1':
                    self.element[j][i] = '000000000'
                index += 1

    def change(self, strProcess):
        a = decodeBoard(strProcess)
        for i in range(NUM_X):
            for j in range(NUM_Y):
                pseudo_ele = ''
                row_ = []
                save_ele = self.element[i][j]
                around = find_around(a, i, j)
                for row in range(NUM_Y):
                    row_.append(a[row][j])
                for index in range(0, 9, 1):
                    if around.count(index + 1) != 0 or a[i].count(index + 1) != 0 or row_.count(index + 1):
                        pseudo_ele += '0'
                    else:
                        pseudo_ele += save_ele[index]

                self.element[i][j] = pseudo_ele

    def reset(self):
        self.select = []
        self.element = [
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000'],
            ['000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000', '000000000',
             '000000000']]


board_play = Board_Play()
number_play = Number_Play()
note_play = Note_Play()

def GameRun_Play(bo):

    board_play.__init__()
    number_play.__init__()
    note_play.__init__()

    number_play.start(bo)

    check_inpt = False
    per_start = True
    start_time = 0
    check_type_inpt = 0
    win_lose = 0
    time_ = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and check_inpt:
                pos = pygame.mouse.get_pos()
                if event.button == BUTTON_LEFT:
                    board_play.update(check_pos_mouse(pos), OCEAN)
                    number_play.selecT(board_play.out())
                    check_type_inpt = 0
                if event.button == BUTTON_RIGHT:
                    board_play.update(check_pos_mouse(pos), YELLOW)
                    note_play.selecT(board_play.out())
                    check_type_inpt = 1
            if event.type == KEYDOWN:
                if event.key == K_RETURN and per_start:
                    start_time = pygame.time.get_ticks()
                    check_inpt = True
                    per_start = False

                if event.key == K_SPACE and win_lose == 1:
                    return [changeTime(time_ - start_time), bo[0], time_ - start_time]
                elif event.key == K_SPACE and win_lose == 2:
                    return [-1, -1, -1]

                if check_inpt:
                    num = 10
                    if event.key == K_1:
                        num = 1
                    elif event.key == K_2:
                        num = 2
                    elif event.key == K_3:
                        num = 3
                    elif event.key == K_4:
                        num = 4
                    elif event.key == K_5:
                        num = 5
                    elif event.key == K_6:
                        num = 6
                    elif event.key == K_7:
                        num = 7
                    elif event.key == K_8:
                        num = 8
                    elif event.key == K_9:
                        num = 9
                    elif event.key == K_BACKSPACE or event.key == K_DELETE or event.key == K_0:
                        num = 0
                    else:
                        pass
                    if check_type_inpt == 0 and num != 10:
                        number_play.update(num)
                        board_play.mask_(number_play.out())
                    if check_type_inpt == 1 and num != 10:
                        note_play.update(num)

                if event.key == K_r:
                    GameRun_Play(createBoard())

        time_ = pygame.time.get_ticks()
        check_win = number_play.win_()
        check_lose = board_play.lose_()

        board_play.draw(changeTime(time_ - start_time), check_type_inpt, win_lose)
        note_play.change(number_play.out_process())
        note_play.update2(number_play.out_lock_position())
        note_play.draw()
        number_play.draw()

        if per_start:
            display(20, 'Press "ENTER" to start', RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 30)

        if win_lose == 0:
            if check_win:
                win_lose = 1
            if check_lose:
                win_lose = 2
        else:
            display(20, 'Press "SPACE" to continue', RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 30)



        pygame.display.update()
        fpsClock.tick(FPS)