import pygame
from characters import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (127, 127, 127)
RED = (223, 120, 97)
BLUE = (19, 148, 135)
PURPLE = (224, 77, 176)
FIRSTLINE, SECONDLINE = 450, 550
LINESPACE = 150
BUTTON = pygame.image.load("assets/Interface/startButton.png")

def ChooseChracters():
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("MortalKombat")
    running=True
    characters = []
    outstanding = dict()
    outstanding={
        "Itachi":pygame.image.load("assets/Interface/CharOutstanding/Itachi.png").convert_alpha(),
        "Sasuke":pygame.image.load("assets/Interface/CharOutstanding/Sasuke.png").convert_alpha(),
        "Madara":pygame.image.load("assets/Interface/CharOutstanding/Madara.png").convert_alpha(),
        "Pain":pygame.image.load("assets/Interface/CharOutstanding/Pain.png").convert_alpha(),
        "Goku":pygame.image.load("assets/Interface/CharOutstanding/Goku.png").convert_alpha(),
        "Luffy":pygame.image.load("assets/Interface/CharOutstanding/Luffy.png").convert_alpha(),
        "Sakura":pygame.image.load("assets/Interface/CharOutstanding/Sakura.png").convert_alpha()
    }

    def setUpCharacts():
        characters.append(Itachi(0,0))
        characters.append(Sasuke(0,0))
        characters.append(Madara(0,0))
        characters.append(Pain(0,0))
        characters.append(Goku(0,0))
        characters.append(Luffy(0,0))
        characters.append(Sakura(0,0))
        centerX, centerY = 0,0
        for i in range(len(characters)):
            if (i%2==0): centerX, centerY = FIRSTLINE, centerY+LINESPACE
            else: centerX = SECONDLINE
            characters[i].posX, characters[i].posY = centerX, centerY

    def setUpCursor(mx, my):
        if (mx>=400 and mx<=600 and my>=18 and my<=82):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return -1
        cenX, cenY = 0,0
        for i in range(len(characters)):
            if (i%2==0): cenX, cenY = FIRSTLINE, cenY+LINESPACE
            else: cenX = SECONDLINE
            if (mx>cenX-45 and mx<cenX-45+90 and my>cenY-45 and my<cenY-45+90):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return i
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return -1

    def drawBLock(screen, selectorA, selectorB, mx, my):
        hover = setUpCursor(mx, my)
        centerX, centerY = 0,0
        for i in range(len(characters)):
            if (i%2==0): centerX, centerY = FIRSTLINE, centerY+LINESPACE
            else: centerX = SECONDLINE
            if (i==selectorA and i==selectorB):
                pygame.draw.rect(screen, PURPLE, (centerX-45, centerY-45, 90, 90))
            elif (i==selectorA):
                pygame.draw.rect(screen, RED, (centerX-45, centerY-45, 90, 90))
            elif (i==selectorB):
                pygame.draw.rect(screen, BLUE, (centerX-45, centerY-45, 90, 90))
            elif (i==hover):
                pygame.draw.rect(screen, WHITE, (centerX-45, centerY-45, 90, 90))
            else: 
                pygame.draw.rect(screen, GRAY, (centerX-45, centerY-45, 90, 90))
            pygame.draw.rect(screen, BLACK, (centerX-42, centerY-42, 84, 84))
            characters[i].DrawCharacter(screen)

    def selection(mx, my):
        selector = setUpCursor(mx, my)
        bg="none"
        if (selector==-1): return selector, bg
        for i in range(len(characters)):
            if (i==selector):
                name = characters[i].__class__.__name__ 
                bg=outstanding[name]
                characters[i].Aura()
                return selector, bg

    def StartBtn(screen, mx, my):
        screen.blit(BUTTON, BUTTON.get_rect(center=(500,50)))

    setUpCharacts()
    selectorA, selectorB = -1, -1
    bg1, bg2 = 'none', 'none'
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and (mouse_x>=400 and mouse_x<=600 and mouse_y>=18 and mouse_y<=82):
                    pygame.quit()
                    return characters[selectorA].__class__.__name__, characters[selectorB].__class__.__name__
                if event.button == 3:
                    selectorA, bg1 = selection(mouse_x, mouse_y)
                elif event.button == 1:
                    selectorB, bg2 = selection(mouse_x, mouse_y)
        if (bg1!='none'):
            screen.blit(bg1, (50,0))
        if (bg2!='none'):
            screen.blit(pygame.transform.flip(bg2, True, False), (-50,0))
        StartBtn(screen, mouse_x, mouse_y)
        drawBLock(screen, selectorA, selectorB, mouse_x, mouse_y)
        #print(f"{mouse_x}:{mouse_y}")
        pygame.display.flip()
    pygame.quit()

def ChooseMaps():
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("MortalKombat")
    running=True
    rightBtn = pygame.image.load("assets/Interface/arrow.png")
    leftBtn = pygame.transform.flip(rightBtn,True,False)
    Map = []
    Name = []
    for i in range(100):
        try: 
            Map.append(
                pygame.transform.scale(
                    pygame.image.load("assets/Maps/Map"+str(i+1)+"/MapImg/frame_00_delay-0.1s.png"),
                    (500,375))
                )
            ifs = open("assets/Maps/Map"+str(i+1)+"/MapName.txt", mode='r')
            text = ifs.read()
            Name.append(text)
        except: break

    def setUpCursor(mx, my):
        if ((mx>=150 and mx<=190 and my>=375 and my<415)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return 'left'
        if (mx>=800 and mx<=840 and my>=375 and my<415):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return 'right'
        if (mx>=400 and mx<=600 and my>=620 and my<=680):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return 'start'
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return 'none'

    def ArrowBtn(screen):
        screen.blit(rightBtn, (800,375))
        screen.blit(leftBtn, (150, 375))
    currentMap = 0
    currentName = 0
    font = pygame.font.SysFont('impact', 100)
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(BLACK)
        ArrowBtn(screen)
        setUpCursor(mouse_x, mouse_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and setUpCursor(mouse_x, mouse_y)=='right':
                    currentMap+=1
                    currentName+=1
                    if (currentMap>=len(Map)): currentName, currentMap=0,0
                elif event.button == 1 and setUpCursor(mouse_x, mouse_y)=='left':
                    currentMap-=1
                    currentName-=1
                    if (currentMap<0): 
                        currentName,currentMap=len(Name)-1,len(Map)-1
                elif event.button == 1 and setUpCursor(mouse_x, mouse_y)=='start':
                    pygame.quit()
                    return Name[currentName]
        screen.blit(Map[currentMap], Map[currentMap].get_rect(center=(500,375)))
        text=font.render(str(Name[currentName]), True, WHITE)
        screen.blit(text, text.get_rect(center=(500, 100)))
        screen.blit(BUTTON, BUTTON.get_rect(center=(500, 650)))
        #print(f"{mouse_x}:{mouse_y}")
        pygame.display.flip()
    pygame.quit()