from init_ import *

def creatColor():

    listcolor = []
    for i in range(0, 255, 5):
        for j in range(0, 255, 5):
            for k in range(0, 255, 5):
                color = [i, j, k]
                x = tuple(color)
                listcolor.append(x)
    print(listcolor)

    return listcolor

def choiceC(i, listC):
    return listC[i]


def test():

    i = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        color1 = choiceC(i, creatColor())
        display(50, 'Test', color1, WINDOWWIDTH, 0, WINDOWHEIGHTADD, 0)
        print('ok')
        i += 1

        pygame.display.update()
        fpsClock.tick(10)

creatColor()