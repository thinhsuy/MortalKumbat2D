import pygame

def IntroScreen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("MortalKombat")
    BLACK = (0,0,0)
    GRAY = (229, 227, 201)
    GREEN = (148, 180, 159)
    RED = (223, 120, 97)
    BLUE = (19, 148, 135)
    running, warning, introduce = True, False, False
    screen.fill(BLACK)
    spritesScreen = []
    currentScreen = 0

    def WarningTable(screen):
        font=pygame.font.SysFont('impact', 25)
        text1 = font.render('This section is not available right now', True, BLACK)
        text2 = font.render('Please comeback latter', True, BLACK)
        pygame.draw.rect(screen, GREEN, (100, 275, 800, 200), 0, 15)
        pygame.draw.rect(screen, GRAY, (110, 285, 780, 180), 0, 15)
        screen.blit(text1, (300, 350))
        screen.blit(text2, (375, 380))
    def Intoroduction(screen):
        font=pygame.font.SysFont('impact', 25)
        text = "Hello heroes, to control your champion, just follow these:" 
        text2 = "Player1: Right(D)  Left(A)  Jump(W)  Fight(F)  Range(G)  Skill(G)"
        text3 = "Player2: Right(arrow)  Left(arrow)  Jump(arrow)  Fight(P)  Range(O)  Skill(I)"
        text = font.render(text, True, BLACK)
        pygame.draw.rect(screen, GREEN, (100, 275, 800, 200), 0, 15)
        pygame.draw.rect(screen, GRAY, (110, 285, 780, 180), 0, 15)
        screen.blit(text, (200, 300))
        screen.blit(font.render(text2, True, BLUE), (200, 350))
        screen.blit(font.render(text3, True, RED), (130, 400))
    
    for i in range(1):
        spritesScreen.append(pygame.image.load('assets/Interface/MortalKumbat1.png').convert())
    
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (int(currentScreen)==len(spritesScreen)-1): currentScreen=0

        if ((mouse_x>580 and mouse_x<880 and mouse_y>450 and mouse_y<510)
        or
        (mouse_x>580 and mouse_x<880 and mouse_y>540 and mouse_y<610)
        or
        (mouse_x>580 and mouse_x<880 and mouse_y>640 and mouse_y<710)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and (warning or introduce):
                    warning=False
                    introduce=False
                elif event.button == 1 and (mouse_x>580 and mouse_x<880 and mouse_y>450 and mouse_y<510):
                    pygame.quit()
                    return True
                elif event.button == 1 and (mouse_x>580 and mouse_x<880 and mouse_y>540 and mouse_y<610):
                    warning=True
                elif event.button == 1 and (mouse_x>580 and mouse_x<880 and mouse_y>640 and mouse_y<710):
                    introduce=True
                
        object = spritesScreen[int(currentScreen)]
        screen.blit(object, (0,0))
        currentScreen+=0.5
        #print(f"{mouse_x}:{mouse_y}")
        if (warning):
            WarningTable(screen)
        if (introduce):
            Intoroduction(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()