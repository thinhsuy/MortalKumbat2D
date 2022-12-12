import pygame

def AICreator(character, filetxt):
    name = character.__class__.__name__
    character.avatar = pygame.image.load('assets/'+name+'/avatar.png')
    character.avatar = pygame.transform.scale(character.avatar, (40,40))
    alist = [line.rstrip() for line in open('assets/'+name+'/'+filetxt)]
    character.HP = int(alist[0].split(' ')[1])
    character.gapGravity = int(alist[1].split(' ')[1])
    character.FramePerFight = int(alist[2].split(' ')[1])
    character.SecPerFight = float(alist[3].split(' ')[1]) 

    character.spritesFire.append(pygame.image.load('assets/'+name+'/'+alist[5].split(' ')[1]))
    character.spritesFire.append(pygame.image.load('assets/'+name+'/'+alist[6].split(' ')[1]))

    # Move Frame
    doubleNumb = False
    if (alist[8].split(' ')[1]=='True'): doubleNumb=True
    head=alist[10].split(' ')[1]
    if (head=='none'): head=''
    tail=alist[11].split(' ')[1]
    for i in range(int(alist[9].split(' ')[1])):
        if (doubleNumb and i<10): text = '0'+str(i)
        elif (doubleNumb==False): text = str(i+1)
        character.spritesRun.append(pygame.image.load('assets/'+name+'/Move/'+head+text+tail).convert_alpha())
    for i in range(int(alist[9].split(' ')[1])):
        character.spritesRun.append(pygame.transform.flip(character.spritesRun[i], True, False))

    # Fight Frame   
    doubleNumb = False
    if (alist[13].split(' ')[1]=='True'): doubleNumb=True
    head=alist[15].split(' ')[1]
    if (head=='none'): head=''
    tail=alist[16].split(' ')[1]
    for i in range(int(alist[14].split(' ')[1])):
        if (doubleNumb and i<10): text = '0'+str(i)
        elif (doubleNumb==False): text = str(i+1)
        character.spritesFight.append(pygame.image.load('assets/'+name+'/Fight/'+head+text+tail).convert_alpha())
    for i in range(int(alist[14].split(' ')[1])):
        character.spritesFight.append(pygame.transform.flip(character.spritesFight[i], True, False))

    # Aura Frame   
    doubleNumb = False
    if (alist[18].split(' ')[1]=='True'): doubleNumb=True
    head=alist[20].split(' ')[1]
    if (head=='none'): head=''
    tail=alist[21].split(' ')[1]
    for i in range(int(alist[19].split(' ')[1])):
        if (doubleNumb and i<10): text = '0'+str(i)
        elif (doubleNumb==False): text = str(i+1)
        character.spritesAura.append(pygame.image.load('assets/'+name+'/Aura/'+head+text+tail).convert_alpha())
    for i in range(int(alist[19].split(' ')[1])):
        character.spritesAura.append(pygame.transform.flip(character.spritesAura[i], True, False))
        

    # Indle Frame   
    doubleNumb = False
    if (alist[23].split(' ')[1]=='True'): doubleNumb=True
    head=alist[25].split(' ')[1]
    if (head=='none'): head=''
    tail=alist[26].split(' ')[1]
    for i in range(int(alist[24].split(' ')[1])):
        if (doubleNumb and i<10): text = '0'+str(i)
        elif (doubleNumb==False): text = str(i+1)
        character.spritesIndle.append(pygame.image.load('assets/'+name+'/Indle/'+head+text+tail).convert_alpha())
    for i in range(int(alist[24].split(' ')[1])):
        character.spritesIndle.append(pygame.transform.flip(character.spritesIndle[i], True, False))
    

    # Hurt Frame
    character.spritesHurt.append(pygame.image.load('assets/'+name+'/'+alist[28].split(' ')[1]).convert_alpha())
    character.spritesHurt.append(pygame.transform.flip(character.spritesHurt[0], True, False))

    # Sound track
    for i in range(30,33,1):
        character.vocals.append(pygame.mixer.Sound('assets/'+name+'/'+alist[i].split(' ')[1]))

    # Special BG
    character.specialBG = pygame.image.load('assets/'+name+'/'+alist[34].split(' ')[1]).convert_alpha()
