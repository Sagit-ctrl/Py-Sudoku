from init_ import *

class Board_Solve():

    def __init__(self):
        self.select = [None, None]
        self.time_ = ''
        self.time__ = ''
        self.status = 'Input question!'

    def draw(self):
        SCREEN.fill(WHITE)
        displaySurface((WINDOWWIDTH, WINDOWHEIGHT), BLACK, SCREEN, 0, 0, True, 0, 0)

        for j in range(int(NUM_Y / 3)):
            for i in range(int(NUM_X / 3)):
                displaySurface((WIDTH * 3 + BLANK * 2, HEIGHT * 3 + BLANK * 2), SILVER, SCREEN, i, j)

        for j in range(NUM_Y):
            for i in range(NUM_X):
                if i == self.select[0] or j == self.select[1]:
                    color = OCEAN
                else:
                    color = WHITE
                displaySurface((WIDTH, HEIGHT), color, SCREEN, i, j)

        display(20, self.status, RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 30)
        display(20, 'Problem solving time is: ' + self.time_ + ' = ' + str(self.time__) + ' ticks', RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT)

    def update(self, pos):
        if pos != -1:
            self.select = pos

    def updateStatus(self, status):
        if status == 0:
            pass
        if status == 1:
            self.status = 'Solving'
        if status == 2:
            self.status = 'Complete problem solving!'
        if status == 3:
            self.status = 'Press "Enter" to solve'


    def timeSolve(self, time_):
        self.time__ = time_
        self.time_ = changeTime(time_)

    def out(self):
        return self.select

class Number_Solve():

    def __init__(self):
        self.position = BoardBase
        self.answer = BoardBase
        self.select = []

    def selecT(self, pos):
        self.select = pos

    def draw(self):
        for j in range(NUM_X):
            for i in range(NUM_Y):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if self.answer[j][i] != 0:
                    display(30, self.answer[j][i], BLUE, WIDTH, x, HEIGHT, y)

        for j in range(NUM_X):
            for i in range(NUM_Y):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if self.position[j][i] != 0:
                    display(30, self.position[j][i], BLACK, WIDTH, x, HEIGHT, y)

    def update(self, num):
        if self.select != [] and num != None:
            self.position[self.select[1]][self.select[0]] = num
            for i in range(9):
                print(self.position[i])
            print('\n')

    def solve_v1(self):
        find = find_empty(self.position)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.position, i, (row, col)):
                self.position[row][col] = i

                if solve(self.position):
                    return True

                self.position[row][col] = 0
        return False

    def reset(self):
        for i in range(NUM_X):
            for j in range(NUM_Y):
                self.position[i][j] = 0

    def out(self):
        return self.position

board_solve = Board_Solve()
number_solve = Number_Solve()

def GameRun_Solve():

    board_solve.__init__()
    number_solve.__init__()
    number_solve.reset()
    board_solve.draw()

    start_time_solve = 0
    stop_time_solve = 0
    check_inpt = True
    check_again = False
    check_empty = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                board_solve.update(check_pos_mouse(pos))
                number_solve.selecT(board_solve.out())
            if event.type == KEYDOWN:
                if check_inpt:
                    num = None
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
                    number_solve.update(num)
                if event.key == K_RETURN and not check_empty:
                    check_inpt = False
                    source = encodeBoard(number_solve.out())
                    start_time_solve = pygame.time.get_ticks()
                    board_solve.updateStatus(1)
                    board_solve.draw()
                    number_solve.solve_v1()
                    board_solve.updateStatus(2)
                    stop_time_solve = pygame.time.get_ticks()
                    answer = encodeBoard(number_solve.out())
                    addSource2Databas(source, answer)
                    check_again = True
                if event.key == K_SPACE and check_again:
                    number_solve.reset()
                    return

        a = encodeBoard(number_solve.out())
        for i in range(len(a)):
            if a[i] != '0':
                check_empty = False

        if not check_empty:
            board_solve.updateStatus(3)

        board_solve.timeSolve(stop_time_solve - start_time_solve)
        board_solve.draw()
        number_solve.draw()

        pygame.display.update()
        fpsClock.tick(FPS)