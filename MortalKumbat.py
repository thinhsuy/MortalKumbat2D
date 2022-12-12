import pygame
from characters import *
import socket
from IntroInterface import *
from WaitingInterface import *

# online = False
# cs = input('Online/Offline: ')
# if (cs=='on'): 
#     online = True
#     HOST = socket.gethostbyname(socket.gethostname())
#     PORT = 5600
#     FORMAT = 'ascii'
#     ADDR = (HOST, PORT)
#     SIZE = 1024

#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR)

#     def ReceiveMess(role):
#         return role.recv(SIZE).decode(FORMAT)
#     def SendMess(role, msg):
#         role.send(msg.encode(FORMAT))
# else: 
#     online = False



def onGame(Map, *list):
    #Set it up
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("MortalKombat")
    BLACK = (0,0,0)
    running=True
    currentBG = 0
    players = []
    screen.fill(BLACK)
    pygame.time.set_timer(pygame.USEREVENT, 500)

    #Generate Important Functions
    def Factory(name):
        switcher={
            'Itachi': Itachi(350,400),
            'Madara': Madara(500,400),
            'Sasuke': Sasuke(350,400),
            'Luffy': Luffy(500,400),
            'Sakura': Sakura(350,400),
            'Goku': Goku(500,400),
            'Pain': Pain(350,400),
            'DawnTown':'assets/Maps/Map1/',
            'JapanTown':'assets/Maps/Map2/',
            'ShinyForest': 'assets/Maps/Map3/',
            'SuperMarine': 'assets/Maps/Map4/'
        }
        return switcher.get(name, 'none')

    def CreateMap(nameMap):
        MapPath = Factory(nameMap)
        MapCoor = MapPath+'MapCoor.txt'
        alist = [line.rstrip() for line in open(MapCoor)]
        MapBlock = []
        lengthFrame = int(alist[0])
        for i in range(1,len(alist),1):
            MapBlock.append((
                int(alist[i].split(' ')[0]), 
                int(alist[i].split(' ')[1]), 
                int(alist[i].split(' ')[2]))
            )
        MapImage = []
        for i in range(lengthFrame):
            if (i<10): value = '0'+str(i)
            else: value = str(i)
            text = MapPath + 'MapImg/frame_' + value + '_delay-0.1s.png'
            MapImage.append(pygame.image.load(text).convert())
        return MapPath, MapBlock, MapImage, lengthFrame

    def DrawMap(screen, MapImg):   
        bg = MapImg[int(currentBG)]
        screen.blit(bg, bg.get_rect(center=(500,375)))
        return 0.05

    def DrawHP(screen):
        RED = (179, 48, 48)
        BLUE = (134,198,244)
        HPbarPath = MapPath + 'HPbar.png'
        bar = pygame.image.load(HPbarPath).convert_alpha()
        barGap = 1000/len(players)
        posX, posY=(barGap-200)/2, 15
        avaX, avaY = posX+75, posY+10
        for i in range(len(players)):
            currentHP=players[i].HP*180/2000
            rectHP = (posX+9, posY+10,currentHP, 42)
            if (checkTeam(players[i])=='Red'):
                pygame.draw.rect(screen, RED, rectHP)
            else:
                pygame.draw.rect(screen, BLUE, rectHP)
            screen.blit(players[i].avatar, players[i].avatar.get_rect(topleft=(avaX,avaY)))
            screen.blit(bar, bar.get_rect(topleft=(posX,posY)))
            posX=barGap*(i+1) + (barGap-200)/2
            avaX = posX+75

    def checkTeam(target):
        for blue in blueTeam:
            if blue.__class__.__name__ == target.__class__.__name__:
                return 'Blue'
        return 'Red'
    
    #Create Important Variables
    MapPath, MapBlock, MapImage, lengthFrame = CreateMap(Map)
    
    for i in range(len(list)):
        players.append(Factory(list[i]))
    blueTeam = []
    redTeam = []
    if (len(players)==2):
        blueTeam.append(players[0])
        redTeam.append(players[1])
    else:
        for i in range(len(players)):
            if (i<int(len(players)/2)):
                blueTeam.append(players[i])
            else:
                redTeam.append(players[i])

    try: 
        text = MapPath+'extra.png'
        ExtraMap = pygame.image.load(text).convert_alpha()
    except:
        ExtraMap = 'none'

    #Running Game
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if (int(currentBG)==lengthFrame): currentBG = 0
        currentBG += DrawMap(screen, MapImage)

        for player in players:
            if (checkTeam(player)=='Red'): 
                player.Animation(screen, redTeam, blueTeam, MapBlock)
            else: player.Animation(screen, blueTeam, redTeam, MapBlock)

        keys=pygame.key.get_pressed()
        players[0].Control_Pressing(keys, pygame.K_a, pygame.K_d, pygame.K_h)
        command = (
            players[1].Control_Pressing(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_i)
        ) 
        # if (online): SendMess(client, command)
        # players[2].Control_Pressing(keys, pygame.K_h, pygame.K_k,pygame.K_RIGHTBRACKET)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                # if (online): SendMess(client, 'close')
                return
            elif event.type == pygame.KEYDOWN:
                players[0].Control_Taping(event, pygame.K_w, pygame.K_f, pygame.K_g)
                command = (
                    players[1].Control_Taping(event, pygame.K_UP, pygame.K_p, pygame.K_o)
                )
                # if (online): SendMess(client, command)
                # players[2].Control_Taping(event, pygame.K_u, pygame.K_p, pygame.K_LEFTBRACKET)
        
        for player in players:
            if (checkTeam(player)=='Red'): opponents = blueTeam
            else: opponents = redTeam
            player.CheckHit(opponents)
            player.DrawCharacter(screen)
        DrawHP(screen)
        # if (online): respon = ReceiveMess(client)
        #print(f"{mouse_x}:{mouse_y}")
        if (ExtraMap!='none'): screen.blit(ExtraMap,(0,0))
        clock.tick(1000)
        pygame.display.flip()
    pygame.quit()

# if (online==True):pass
# else: 
if(IntroScreen()):
    playerA, playerB = ChooseChracters()
    MapName = ChooseMaps()
    onGame(MapName,*(playerB, playerA))
else: pass
