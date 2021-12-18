import pygame.mouse

from init_ import *
from solve_ import GameRun_Solve
from play_ import GameRun_Play

def GameStart():

    solve = [0, 0, 0, 0]
    play = [0, 0, 0, 0]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= solve[0] and pos[0] <= solve[1] and pos[1] >= solve[2] and pos[1] <= solve[3]:
                    return 1
                if pos[0] >= play[0] and pos[0] <= play[1] and pos[1] >= play[2] and pos[1] <= play[3]:
                    return 2

        displayImage('back3.jpg', WINDOWWIDTH + 300, WINDOWHEIGHTADD, 0, 0, 0, 0, True, 0, 0)
        display(100, 'SUDOKU', color(), WINDOWWIDTH, 0, WINDOWHEIGHT, 0)
        display(30, 'Welcome to SUDOKU', color(), WINDOWWIDTH, 0, WINDOWHEIGHT, 100)

        solve = displayRect(20, 'Solve', RED, WINDOWWIDTH / 2, 0, WINDOWHEIGHT, 200)
        play = displayRect(20, 'Play', RED, WINDOWWIDTH / 2, WINDOWWIDTH / 2, WINDOWHEIGHT, 200)

        pygame.display.update()
        fpsClock.tick(FPS)

def GameEnd(name, time, bo, realtime):
    list = []
    if realtime == -1:
        pass
    else:
        changeDatabase(name, time, bo, realtime)

    data = readSqliteTableRank()
    for i in range(5):
        list.append(data[i])

    SCREEN.fill(WHITE)
    displayImage('back4.jpg', WINDOWWIDTH, WINDOWHEIGHTADD,0, 0, 0, 0, True, 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    return 1
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()
                else:
                    return 0

        display(50, 'CONGTURALATION!', color(), WINDOWWIDTH, 0, WINDOWHEIGHTADD / 4, 0)

        sepWinX = WINDOWWIDTH / 4
        sepWinY = WINDOWHEIGHTADD / 32

        color_ = color()

        display(30, 'Rank', color_, sepWinX, 0, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = i + 1
            display(30, status, choice_color(i), sepWinX, 0, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(30, 'Name', color_, sepWinX, sepWinX, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = str(list[i][1])
            display(30, status, choice_color(i), sepWinX, sepWinX, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(30, 'Time', color_, sepWinX, sepWinX * 2, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = str(list[i][2])
            display(30, status, choice_color(i), sepWinX, sepWinX * 2, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(30, 'Board', color_, sepWinX, sepWinX * 3, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = str(list[i][3])
            display(30, status, choice_color(i), sepWinX, sepWinX * 3, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(20, 'Press "A" to play again', WHITE, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 40)
        display(20, 'Press anything to continue', WHITE, WINDOWWIDTH, 0, 100, WINDOWHEIGHT)

        pygame.display.update()
        fpsClock.tick(FPS)

def main():

    while True:
        choose = GameStart()
        if choose == 1:
            GameRun_Solve()
        if choose == 2:
            name1 = name(SCREEN, color(), fpsClock, FPS, WINDOWWIDTH, WINDOWHEIGHTADD)
            a = GameRun_Play(testBo)
            GameEnd(name1, a[0], a[1], a[2])

if __name__ == '__main__':
    main()