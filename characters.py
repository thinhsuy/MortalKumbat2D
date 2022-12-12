import pygame
import threading
import time
from specialSkill import *
from CollabSkill import *
from AICreator import *
isUsingSkill = False

class Character(pygame.sprite.Sprite):
    def __init__(self): pass
    def __init__(self, paraX, paraY):
        super().__init__()
        self.damgeFight = 30
        self.damgeFire = 50
        self.isCollabing = False
        #sprites init
        self.specialBG = 'none'
        self.avatar = 'none'
        self.spritesRun = []
        self.spritesFight = []
        self.spritesHurt = []
        self.spritesAura = []
        self.spritesFire = []
        self.spritesIndle = []
        self.vocals = []
        self.currentRunRight,self.currentRunLeft = 0, 0
        self.currentFightRight, self.currentFightLeft = 0, 0
        self.currentHurtRight, self.currentHurtLeft = 0, 0
        self.currentAuraRight, self.currentAuraLeft = 0, 0
        self.currentIndleRight, self.currentIndleLeft = 0, 0
        #sound animation
        self.SoundHit = pygame.mixer.Sound('assets/SoundEffects/FightHit.wav')
        self.SoundFight = pygame.mixer.Sound('assets/SoundEffects/Fight.wav')
        self.SoundThrow = pygame.mixer.Sound('assets/SoundEffects/Throw.wav')
        self.SoundJump = pygame.mixer.Sound('assets/SoundEffects/Jump.wav')
        #movement init
        self.posX, self.posY = paraX, paraY
        self.jump_height = 150
        self.jump_speed = 1.2
        self.speed = 0.8
        self.gapGravity = 40
        self.oldX, self.oldY = paraX, paraY
        #fire unit
        self.speeed_fire = 1.5
        self.fireX, self.fireY = -10000, -10000
        self.mainDirect, self.fireDirect = "left", "none"
        #special variables
        self.isJumping, self.canJump, self.isFiring = False, True, False
        self.isFighting, self.isHurting, self.isAuring = False, False, False
        self.isHit, self.isSpecial = False, False
        self.canControl = True
        self.fireRotate = 0
        #animation effect
        self.speed_run_animation = 0.01
        self.speed_thread_animation = 0.001
        self.SpecialSkill = 'off'
        self.FramePerFight = 2
        self.SecPerFight = 0.2 
        self.SingletonCall = True
        self.isMoving = False
    def VirtualSpecialSkill(self, screen, team, players): pass
    def Gravity(self, mapblock):
        for i in range(len(mapblock)):
            if (int(self.posY)==mapblock[i][2]-self.gapGravity and int(self.posX)>=mapblock[i][0] and int(self.posX)<=mapblock[i][1]):
                self.canJump = True
                return
        if (self.isJumping==False):
            self.posY += self.jump_speed
    def Animation(self, screen, team, players, MapBlock):
        global isUsingSkill
        #Singleton init
        if (self.SingletonCall):
            self.SingletonCall = False
            self.currentFightRight = len(self.spritesFight)/2
            self.currentFightLeft = 0
            self.currentHurtRight = len(self.spritesHurt)/2
            self.currentHurtLeft = 0
            self.currentIndleRight = len(self.spritesIndle)/2
            self.currentIndleLeft = 0
            self.fire = self.spritesFire[0]
            self.main = self.spritesRun[self.currentRunLeft]
        #Special Skill jump on
        if (self.SpecialSkill=='on'): 
            self.VirtualSpecialSkill(screen,team, players)
        #Gravity
        self.Gravity(MapBlock)
        if (self.posY>750): self.HP = 0
        #Jumping
        if (self.isJumping and self.oldY-self.posY<self.jump_height):
            self.posY-=self.jump_speed
        if (self.oldY-self.posY>=self.jump_height-1):
            self.isJumping = False
        #firing
        if (self.isFiring):
            screen.blit(self.fire, self.fire.get_rect(center=(self.fireX,self.fireY)))
            if (self.fireDirect=="right"): self.fireX+=self.speeed_fire
            else: self.fireX-=self.speeed_fire
            if (self.fireX<0 or self.fireX>1000): 
                self.isFiring=False
                self.fireX, self.fireY = -1000, -1000
                self.isSpecial = False
            self.fire = pygame.transform.rotate(self.fire, 90)  
    def StandBack(self):
        if (self.mainDirect=="right"): self.main = self.spritesRun[int(len(self.spritesRun)/2)]
        else: self.main = self.spritesRun[0]
    def MoveRight(self):
        if(self.isControllable()==False): return
        self.DestroyAura()
        self.posX += self.speed
        if (self.posX>1000): self.posX=0
        if (self.mainDirect=='left'): self.currentRunRight = len(self.spritesRun)/2
        else: 
            self.currentRunRight+=self.speed_run_animation
            if (int(self.currentRunRight)>=len(self.spritesRun)): self.currentRunRight = len(self.spritesRun)/2
        self.main = self.spritesRun[int(self.currentRunRight)]
        self.mainDirect = "right"  
        self.isMoving = True  
    def MoveLeft(self):
        if(self.isControllable()==False): return
        self.DestroyAura()
        self.posX -= self.speed
        if (self.posX<0): self.posX=1000
        if (self.mainDirect=='right'): self.currentRunLeft = 0
        else: 
            self.currentRunLeft+=self.speed_run_animation
            if (int(self.currentRunLeft)==len(self.spritesRun)/2): self.currentRunLeft = 0
        self.main = self.spritesRun[int(self.currentRunLeft)]
        self.mainDirect = "left"  
        self.isMoving = True
    def Jump(self):
        if(self.isControllable()==False): return
        if (self.canJump==True):
            self.SoundJump.play()
            self.canJump = False
            self.isJumping = True
            self.oldY = self.posY
        else: pass   
    def Fire(self):
        if (self.isFiring==False and self.isControllable()):
            if (self.isSpecial): self.fire = self.spritesFire[1]
            else: self.fire = self.spritesFire[0]
            self.fireX, self.fireY = self.posX, self.posY
            self.fireDirect = self.mainDirect
            self.isFiring = True
            self.SoundThrow.play()
        else: pass
    def Fight(self):
        if(self.isControllable()==False): return
        self.isFighting = True
        self.SoundFight.play()
        countTime = threading.Thread(target=self.ThreadFight, args=())
        countTime.start() 
    def ThreadFight(self):
        for i in range(self.FramePerFight):
            if (self.mainDirect=='right'):
                self.main = self.spritesFight[int(self.currentFightRight)]
                self.currentFightRight+=1
                if (int(self.currentFightRight)>=len(self.spritesFight)):
                    self.currentFightRight=int(len(self.spritesFight)/2)
            else:
                self.main = self.spritesFight[int(self.currentFightLeft)]
                self.currentFightLeft+=1
                if (int(self.currentFightLeft)>=len(self.spritesFight)/2):
                    self.currentFightLeft = 0
            time.sleep(self.SecPerFight)
        self.isFighting = False
        self.StandBack()
    def ThreadHurt(self, opponent):
        self.currentHurtRight = len(self.spritesHurt)/2
        self.currentHurtLeft = 0
        side = 'none'
        if (opponent.mainDirect=='left'):
            self.main = self.spritesHurt[int(self.currentHurtRight)]
            self.currentHurtRight+=1
            if (int(self.currentHurtRight)>=len(self.spritesHurt)):
                self.currentHurtRight=int(len(self.spritesHurt)/2)
            side = 'right'
        else:
            self.main = self.spritesHurt[int(self.currentHurtLeft)]
            self.currentHurtLeft+=1
            if (int(self.currentHurtLeft)>=len(self.spritesHurt)/2):
                self.currentHurtLeft = 0
            side = 'left'
        time.sleep(0.5)
        self.isHurting = False
        if (side=='right'): self.main = self.spritesRun[int(len(self.spritesRun)/2)]
        else:   self.main = self.spritesRun[0]
    def DestroyAura(self):
        self.isAuring = False
        self.isSpecial = False
        self.vocals[0].stop()
    def ThreadAura(self):
        totalSprites = int(len(self.spritesAura)/2)
        for i in range(totalSprites):
            if (self.isAuring==False): return
            if (self.mainDirect=='right'):
                self.main = self.spritesAura[int(self.currentAuraRight)]
                self.currentAuraRight+=1
                if (int(self.currentAuraRight)>=len(self.spritesAura)):
                    self.currentAuraRight=int(len(self.spritesAura)/2)
            else:
                self.main = self.spritesAura[int(self.currentAuraLeft)]
                self.currentAuraLeft+=1
                if (int(self.currentAuraLeft)>=len(self.spritesAura)/2):
                    self.currentAuraLeft = 0
            time.sleep(0.1)
        self.isAuring = False
        self.isSpecial = True
        self.Fire()
        self.StandBack()
    def Aura(self): 
        global isUsingSkill
        if (self.isControllable()==False or isUsingSkill or self.isAuring): return
        self.currentAuraRight = len(self.spritesAura)/2
        self.currentAuraLeft = 0
        self.isAuring = True
        self.vocals[0].play()
        countTime = threading.Thread(target=self.ThreadAura, args=())
        countTime.start()
    def isCollision(self, target, tposX, tposY):
        if (self.main.get_rect(center=(self.posX, self.posY)).colliderect(target.get_rect(center=(tposX,tposY)))):
            return True
        else: return False 
    def isFront(self, opponent):
        if (opponent.mainDirect=='right' and self.posX>=opponent.posX): return True
        elif (opponent.mainDirect=='left' and self.posX<=opponent.posX): return True
        else: return False
    def isControllable(self):
        if (self.isAlive()==False): return False
        if (self.canControl==False): return False
        if (self.isHurting or self.isFighting): return False
        else: return True
    def isAlive(self):
        if self.posY>=750: return False
        elif self.HP>0: return True
        else: return False
    def GetHit(self, damage, opponent, delay, type):
        self.isHurting = True
        countTime = threading.Thread(target=self.ThreadHurt, args=(opponent,))
        countTime.start()
        self.HP -= damage
        if (type=='fight'):
            if (opponent.mainDirect=="right"): self.posX += delay
            else: self.posX -= delay
        elif (type=='fire'):
            if (opponent.fireDirect=="right"): self.posX += delay
            else: self.posX -= delay
        self.SoundHit.play()
    def deleteFire(self):
        self.fireX, self.fireY = -10000, -10000
    def SetUpSpecialSkill(self):
        global isUsingSkill
        self.isSpecial = False
        self.SpecialSkill = 'on'
        isUsingSkill = True
        self.vocals[0].stop()
        self.vocals[1].play()
    def CheckHit(self, players):
        global isUsingSkill
        for opponent in players:
            if (opponent!=self):
                if (self.isHurting==False and
                    self.isCollision(opponent.fire, opponent.fireX, opponent.fireY) 
                    and self.isAlive()):
                        self.GetHit(self.damgeFire, opponent, 20, 'fire')
                        if opponent.isSpecial and isUsingSkill==False: 
                            opponent.SetUpSpecialSkill()
                            opponent.deleteFire()
                        self.DestroyAura()
                elif (self.isHurting==False and
                    self.isFront(opponent)==True and
                    self.isCollision(opponent.main, opponent.posX, opponent.posY)
                    and opponent.isFighting
                    and self.isAlive()):
                        self.GetHit(self.damgeFight, opponent, 10, 'fight')
                        #opponent.deleteFight()
                        self.DestroyAura()
    def Indle(self):
        if (self.isFighting or 
            self.isHurting or 
            self.isMoving or 
            self.isAuring or
            self.isCollabing or
            self.SpecialSkill=='on'): 
                self.isMoving = False
                self.currentIndleRight = len(self.spritesIndle)/2
                self.currentIndleLeft = 0
                return
        if (self.mainDirect=='right'): 
            self.main = self.spritesIndle[int(self.currentIndleRight)]
            self.currentIndleRight+=0.005
            if (int(self.currentIndleRight)==len(self.spritesIndle)):
                self.currentIndleRight = len(self.spritesIndle)/2
        else: 
            self.main = self.spritesIndle[int(self.currentIndleLeft)]
            self.currentIndleLeft+=0.005
            if (int(self.currentIndleLeft)==int(len(self.spritesIndle)/2)):
                self.currentIndleLeft = 0
    def DrawCharacter(self, screen):
        if (self.isAlive()):
            self.Indle()
            screen.blit(self.main, self.main.get_rect(center=(self.posX,self.posY)))
    def Control_Taping(self, event, btnJump, btnFight, btnFire):
        if event.key == btnJump: 
            self.Jump()
            return 'Jump'
        elif event.key == btnFire: 
            self.Fire()
            return 'Fire'
        elif event.key == btnFight: 
            self.Fight()
            return 'Fight'
        else:
            return 'none'
    def Control_Pressing(self, keys, btnLeft, btnRight, btnAura):
        if keys[btnRight]: 
            self.MoveRight()
            return 'Move Right'
        elif keys[btnLeft]: 
            self.MoveLeft()
            return 'Move Left'
        elif keys[btnAura]: 
            self.Aura()
            return 'Aura'
        else: return 'none'


class MonoCharacter(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.skill=[]
        for i in range(0,4,1):
            extend = str(i+1)
            text = 'assets/Madara/Skill/'+extend+'.png'
            self.skill.append(pygame.image.load(text))
        self.dragon=[]
        for i in range(0,15,1):
            extend = str(i+1)
            text = 'assets/Madara/GroundDragon/'+extend+'.png'
            self.dragon.append(pygame.image.load(text))

    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        isUsingSkill = False
        self.SpecialSkill = 'off'
        print(f'This is {self.__class__.__name__} special !')
        
class Itachi(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.HP = 2000
        self.speed_run_animation = 0.05
        self.avatar = pygame.image.load('assets/Itachi/avatar.png').convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (40,40))
        self.spritesFire.append(pygame.image.load('assets/Itachi/Shuriken.png').convert_alpha())
        self.spritesFire.append(pygame.image.load('assets/Itachi/Mangekyou.png').convert_alpha())
        for i in range(4):
            text = 'assets/Itachi/Itachi_run' + str(i+1) + '.png'
            self.spritesRun.append(pygame.image.load(text).convert_alpha())
        for i in range(4):
            self.spritesRun.append(pygame.transform.flip(self.spritesRun[i], True, False))
        for i in range(6):
            text = 'assets/Itachi/Itachi_fight' + str(i+1) + '.png'
            self.spritesFight.append(pygame.image.load(text).convert_alpha())
        for i in range(6):
            self.spritesFight.append(pygame.transform.flip(self.spritesFight[i], True, False))
        for i in range(6):
            text = 'assets/Itachi/Itachi_aura' + str(i+1) + '.png'
            self.spritesAura.append(pygame.image.load(text).convert_alpha())
        for i in range(6):
            self.spritesAura.append(pygame.transform.flip(self.spritesAura[i], True, False))
        for i in range(5):
            text = 'assets/Itachi/Itachi_indle' + str(i+1) + '.png'
            self.spritesIndle.append(pygame.image.load(text).convert_alpha())
        for i in range(5):
            self.spritesIndle.append(pygame.transform.flip(self.spritesIndle[i], True, False))
        self.spritesHurt.append(pygame.image.load('assets/Itachi/Itachi_left_hurt.gif').convert_alpha()) 
        self.spritesHurt.append(pygame.transform.flip(self.spritesHurt[0], True, False))
        self.vocals.append(pygame.mixer.Sound('assets/Itachi/VocalAura.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Itachi/VocalItachi.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Itachi/VocalItachi2.mp3'))
        self.specialBG = pygame.image.load('assets/Itachi/SpecialBG.png').convert_alpha()
        pygame.mixer.Sound.set_volume(self.vocals[0], 0.5)
        self.skill=[]
        for i in range(0,36,1):
            extend = str(i+1)
            text = 'assets/Itachi/Skill/'+extend+'.png'
            self.skill.append(pygame.image.load(text))
        # Collabration skills
        self.CollabSet = []
        self.SharinganSprites = []
        for i in range(0,31,1):
            if (i<10): text = 'assets/CollabrationSkill/UchihaUnbond/Sharingan/frame_0'+str(i)+'_delay-0.1s.png' 
            else: text = 'assets/CollabrationSkill/UchihaUnbond/Sharingan/frame_'+str(i)+'_delay-0.1s.png' 
            self.SharinganSprites.append(pygame.image.load(text).convert_alpha())
        self.UchihaSetSprites = []
        for i in range(0,36,1):
            text = 'assets/CollabrationSkill/UchihaUnbond/ItachiSet/'+str(i+1)+'.png' 
            self.UchihaSetSprites.append(pygame.image.load(text).convert_alpha())
        self.BlackfireSprites = []
        for i in range(0,21,1):
            if (i<10): text = 'assets/CollabrationSkill/UchihaUnbond/BlackFire/frame_0'+str(i)+'_delay-0.2s.png' 
            else: text = 'assets/CollabrationSkill/UchihaUnbond/BlackFire/frame_'+str(i)+'_delay-0.2s.png' 
            self.BlackfireSprites.append(pygame.image.load(text).convert_alpha())
        self.SasukeSetSprites = []
        for i in range(0,20,1):
            text = 'assets/CollabrationSkill/UchihaUnbond/SasukeSet/'+str(i+1)+'.png' 
            self.SasukeSetSprites.append(pygame.image.load(text).convert_alpha())
        self.SuperChidoriSprites = []
        for i in range(3,24,1):
            text = 'assets/CollabrationSkill/UchihaUnbond/SuperChidori/'+str(i+1)+'.png' 
            self.SuperChidoriSprites.append(pygame.image.load(text).convert_alpha())
        self.CollabImg = pygame.image.load('assets/CollabrationSkill/UchihaUnbond/Brother-bond.png').convert_alpha()
        self.CollabSet.append(self.SharinganSprites) #0
        self.CollabSet.append(self.UchihaSetSprites) #1
        self.CollabSet.append(self.BlackfireSprites) #2
        self.CollabSet.append(self.SasukeSetSprites) #3
        self.CollabSet.append(self.SuperChidoriSprites) #4
        self.typeSkill = 'Normal'

    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        if (self.typeSkill=='Normal'):
            for partner in team:
                if (partner.__class__.__name__=='Sasuke' and partner.isAuring):
                    self.typeSkill = 'Collab'
        if (self.typeSkill=='Normal'):
            Sharin = Sussano(False, self.specialBG, self, players, self.skill, 10)
            if (Sharin.Update(screen)): pass
            else: 
                isUsingSkill = False
                Sharin.setBack()
        else:
            BrotherBond = UchihaUnbond(self.CollabImg, team, players, self.CollabSet)
            if (BrotherBond.Update(screen)): pass
            else:
                isUsingSkill = False
                self.typeSkill = 'Normal'
                BrotherBond.setBack()

class Sasuke(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.gapGravity = 30
        self.HP = 2000
        self.avatar = pygame.image.load('assets/Sasuke/avatar.png').convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (40,40))
        self.spritesFire.append(pygame.image.load('assets/Sasuke/ThunderSuriken.png').convert_alpha())
        self.spritesFire.append(pygame.image.load('assets/Sasuke/Chidori.png').convert_alpha())
        for i in range(5):
            text = 'assets/Sasuke/Sasuke_run' + str(i+1) + '.png'
            self.spritesRun.append(pygame.image.load(text).convert_alpha())
        for i in range(5):
            self.spritesRun.append(pygame.transform.flip(self.spritesRun[i], True, False))
        for i in range(6):
            text = 'assets/Sasuke/Sasuke_fight' + str(i+1) + '.png'
            self.spritesFight.append(pygame.image.load(text).convert_alpha())
        for i in range(6):
            self.spritesFight.append(pygame.transform.flip(self.spritesFight[i], True, False))
        for i in range(10):
            text = 'assets/Sasuke/Sasuke_Aura' + str(i+1) + '.png'
            self.spritesAura.append(pygame.image.load(text).convert_alpha())
        for i in range(10):
            self.spritesAura.append(pygame.transform.flip(self.spritesAura[i], True, False))
        for i in range(5):
            text = 'assets/Sasuke/Indle/' + str(i+1) + '.png'
            self.spritesIndle.append(pygame.image.load(text).convert_alpha())
        for i in range(5):
            self.spritesIndle.append(pygame.transform.flip(self.spritesIndle[i], True, False))
        self.spritesHurt.append(pygame.image.load('assets/Sasuke/Sasuke_hurt.png').convert_alpha()) 
        self.spritesHurt.append(pygame.transform.flip(self.spritesHurt[0], True, False))
        self.vocals.append(pygame.mixer.Sound('assets/Sasuke/VocalAura.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Sasuke/VocalSasuke.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Sasuke/VocalSasuke2.mp3'))
        self.specialBG = pygame.image.load('assets/Sasuke/SpecialBG.png').convert_alpha()
        self.skill = []
        for i in range(33,80,1):
            text = 'assets/Sasuke/Skill/frame_' + str(i) + '_delay-0.1s.gif'
            self.skill.append(pygame.image.load(text))
        # Collabration skills
        self.CollabSet = []
        self.SharinganSprites = []
        for i in range(0,31,1):
            if (i<10): text = 'assets/CollabrationSkill/UchihaUnbond/Sharingan/frame_0'+str(i)+'_delay-0.1s.png' 
            else: text = 'assets/CollabrationSkill/UchihaUnbond/Sharingan/frame_'+str(i)+'_delay-0.1s.png' 
            self.SharinganSprites.append(pygame.image.load(text).convert_alpha())
        self.UchihaSetSprites = []
        for i in range(0,36,1):
            text = 'assets/CollabrationSkill/UchihaUnbond/ItachiSet/'+str(i+1)+'.png' 
            self.UchihaSetSprites.append(pygame.image.load(text).convert_alpha())
        self.BlackfireSprites = []
        for i in range(0,21,1):
            if (i<10): text = 'assets/CollabrationSkill/UchihaUnbond/BlackFire/frame_0'+str(i)+'_delay-0.2s.png' 
            else: text = 'assets/CollabrationSkill/UchihaUnbond/BlackFire/frame_'+str(i)+'_delay-0.2s.png' 
            self.BlackfireSprites.append(pygame.image.load(text).convert_alpha())
        self.SasukeSetSprites = []
        for i in range(0,20,1):
            text = 'assets/CollabrationSkill/UchihaUnbond/SasukeSet/'+str(i+1)+'.png' 
            self.SasukeSetSprites.append(pygame.image.load(text).convert_alpha())
        self.SuperChidoriSprites = []
        for i in range(3,24,1):
            text = 'assets/CollabrationSkill/UchihaUnbond/SuperChidori/'+str(i+1)+'.png' 
            self.SuperChidoriSprites.append(pygame.image.load(text).convert_alpha())
        self.CollabImg = pygame.image.load('assets/CollabrationSkill/UchihaUnbond/Brother-bond.png').convert_alpha()
        self.CollabSet.append(self.SharinganSprites) #0
        self.CollabSet.append(self.UchihaSetSprites) #1
        self.CollabSet.append(self.BlackfireSprites) #2
        self.CollabSet.append(self.SasukeSetSprites) #3
        self.CollabSet.append(self.SuperChidoriSprites) #4
        self.typeSkill = 'Normal'

    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        if (self.typeSkill=='Normal'):
            for partner in team:
                if (partner.__class__.__name__=='Itachi' and partner.isAuring):
                    self.typeSkill = 'Collab'
        if (self.typeSkill=='Normal'):
            ThunderPunch = ChidoriPunch(False, self.specialBG, self, players, self.skill, 32)
            if (ThunderPunch.Update(screen)): pass
            else: 
                isUsingSkill = False
                ThunderPunch.setBack()
        else:
            BrotherBond = UchihaUnbond(self.CollabImg, team, players, self.CollabSet)
            if (BrotherBond.Update(screen)): pass
            else:
                isUsingSkill = False
                self.typeSkill = 'Normal'
                BrotherBond.setBack()

class Luffy(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.gapGravity = 30
        self.SecPerFight = 0.1
        self.FramePerFight = 3
        self.HP = 2000
        self.avatar = pygame.image.load('assets/Luffy/avatar.png').convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (40,40))
        self.spritesFire.append(pygame.image.load('assets/Luffy/LuffyHat.png').convert_alpha())
        self.spritesFire.append(pygame.image.load('assets/Luffy/CloudHat.png').convert_alpha())
        for i in range(8):
            text = 'assets/Luffy/Luffy_run' + str(i+1) + '.png'
            self.spritesRun.append(pygame.image.load(text).convert_alpha())
        for i in range(8):
            self.spritesRun.append(pygame.transform.flip(self.spritesRun[i], True, False))
        for i in range(9):
            text = 'assets/Luffy/Luffy_fight' + str(i+1) + '.png'
            self.spritesFight.append(pygame.image.load(text).convert_alpha())
        for i in range(9):
            self.spritesFight.append(pygame.transform.flip(self.spritesFight[i], True, False))
        for i in range(14):
            text = 'assets/Luffy/Aura/Luffy_aura' + str(i+1) + '.png'
            self.spritesAura.append(pygame.image.load(text).convert_alpha())
        for i in range(14):
            self.spritesAura.append(pygame.transform.flip(self.spritesAura[i], True, False))
        for i in range(4):
            text = 'assets/Luffy/Indle/' + str(i+1) + '.png'
            self.spritesIndle.append(pygame.image.load(text).convert_alpha())
        for i in range(4):
            self.spritesIndle.append(pygame.transform.flip(self.spritesIndle[i], True, False))
        self.spritesHurt.append(pygame.image.load('assets/Luffy/Luffy_hurt.png').convert_alpha()) 
        self.spritesHurt.append(pygame.transform.flip(self.spritesHurt[0], True, False))
        self.vocals.append(pygame.mixer.Sound('assets/Luffy/VocalAura.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Luffy/VocalLuffy.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Luffy/VocalLuffy1.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Luffy/VocalLuffy2.mp3'))
        self.specialBG = pygame.image.load('assets/Luffy/SpecialBG.png').convert_alpha()
        self.skill = []
        for i in range(0,22,1):
            if (i<10): extend = '0' + str(i)
            else: extend = str(i)
            text = 'assets/Luffy/Skill/frame_' + extend + '_delay-0.1s.png'
            self.skill.append(pygame.image.load(text))
    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        GumoGumo = GaintPistol(False, self.specialBG, self, players, self.skill, 18)
        if (GumoGumo.Update(screen)): pass
        else: 
            isUsingSkill = False
            GumoGumo.setBack()

class Sakura(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.gapGravity = 30
        self.SecPerFight = 0.1
        self.FramePerFight = 3
        self.HP = 2000
        self.avatar = pygame.image.load('assets/Sakura/avatar.png').convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (40,40))
        self.spritesFire.append(pygame.image.load('assets/Sakura/TheMistCard.png').convert_alpha())
        self.spritesFire.append(pygame.image.load('assets/Sakura/Kero.png').convert_alpha())
        for i in range(4):
            text = 'assets/Sakura/Move/' + str(i+1) + '.png'
            self.spritesRun.append(pygame.image.load(text).convert_alpha())
        for i in range(4):
            self.spritesRun.append(pygame.transform.flip(self.spritesRun[i], True, False))
        for i in range(len(self.spritesRun)): self.spritesRun[i] = pygame.transform.scale(self.spritesRun[i], (75,75))
        for i in range(9):
            text = 'assets/Sakura/Fight/' + str(i+1) + '.png'
            self.spritesFight.append(pygame.image.load(text).convert_alpha())
        for i in range(9):
            self.spritesFight.append(pygame.transform.flip(self.spritesFight[i], True, False))
        for i in range(len(self.spritesFight)): self.spritesFight[i] = pygame.transform.scale(self.spritesFight[i], (75,75))
        for i in range(20):
            text = 'assets/Sakura/Aura/' + str(i+1) + '.png'
            self.spritesAura.append(pygame.image.load(text).convert_alpha())
        for i in range(20):
            self.spritesAura.append(pygame.transform.flip(self.spritesAura[i], True, False))
        for i in range(len(self.spritesAura)): self.spritesAura[i] = pygame.transform.scale(self.spritesAura[i], (75,75))
        for i in range(4):
            text = 'assets/Sakura/Indle/' + str(i+1) + '.png'
            self.spritesIndle.append(pygame.image.load(text).convert_alpha())
        for i in range(4):
            self.spritesIndle.append(pygame.transform.flip(self.spritesIndle[i], True, False))
        for i in range(len(self.spritesIndle)): self.spritesIndle[i] = pygame.transform.scale(self.spritesIndle[i], (75,75))
        self.spritesHurt.append(pygame.image.load('assets/Sakura/Sakura_hurt.png').convert_alpha()) 
        self.spritesHurt.append(pygame.transform.flip(self.spritesHurt[0], True, False))
        for i in range(len(self.spritesHurt)): self.spritesHurt[i] = pygame.transform.scale(self.spritesHurt[i], (75,75))
        self.vocals.append(pygame.mixer.Sound('assets/Sakura/VocalAura.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Sakura/VocalSakura1.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Sakura/VocalSakura2.mp3'))
        self.skill = []
        for i in range(0,32,1):
            extend = str(i+1)
            text = 'assets/Sakura/Skill/'+extend+'.png'
            self.skill.append(pygame.image.load(text))
        for i in range(len(self.skill)): self.skill[i] = pygame.transform.scale(self.skill[i], (75,95))
        self.Windy = pygame.image.load('assets/Sakura/Windy.png').convert_alpha()
        self.specialBG = pygame.image.load('assets/Sakura/SpecialBG.png').convert_alpha()
    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        Windy = SummonWindy(False,self.specialBG, self, players, self.skill, self.Windy)
        if (Windy.Update(screen)): pass
        else: 
            isUsingSkill = False
            Windy.setBack()

class Goku(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.gapGravity = 30
        self.SecPerFight = 0.15
        self.FramePerFight = 3
        self.HP = 2000
        self.avatar = pygame.image.load('assets/Goku/avatar.png').convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (40,40))
        self.spritesFire.append(pygame.image.load('assets/Goku/smallball.png').convert_alpha())
        self.spritesFire.append(pygame.image.load('assets/Goku/dragonBall.png').convert_alpha())
        for i in range(4):
            text = 'assets/Goku/Move/' + str(i+1) + '.png'
            self.spritesRun.append(pygame.image.load(text).convert_alpha())
        for i in range(4):
            self.spritesRun.append(pygame.transform.flip(self.spritesRun[i], True, False))
        for i in range(9):
            text = 'assets/Goku/Fight/' + str(i+1) + '.png'
            self.spritesFight.append(pygame.image.load(text).convert_alpha())
        for i in range(9):
            self.spritesFight.append(pygame.transform.flip(self.spritesFight[i], True, False))
        for i in range(12):
            text = 'assets/Goku/Aura/' + str(i+1) + '.png'
            self.spritesAura.append(pygame.image.load(text).convert_alpha())
        for i in range(12):
            self.spritesAura.append(pygame.transform.flip(self.spritesAura[i], True, False))
        for i in range(3):
            text = 'assets/Goku/Indle/' + str(i+1) + '.png'
            self.spritesIndle.append(pygame.image.load(text).convert_alpha())
        for i in range(3):
            self.spritesIndle.append(pygame.transform.flip(self.spritesIndle[i], True, False))
        self.spritesHurt.append(pygame.image.load('assets/Goku/Goku_hurt.png').convert_alpha()) 
        self.spritesHurt.append(pygame.transform.flip(self.spritesHurt[0], True, False))
        self.vocals.append(pygame.mixer.Sound('assets/Goku/GokuAura.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Goku/VocalGoku.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Goku/VocalGoku1.mp3'))
        self.skill = []
        for i in range(0,30,1):
            extend = str(i+1)
            text = 'assets/Goku/Skill/'+extend+'.png'
            self.skill.append(pygame.image.load(text))
        for i in range(len(self.skill)): self.skill[i] = pygame.transform.scale(self.skill[i], (75,95))
        self.PowerBall = pygame.image.load('assets/Goku/PowerBall.png').convert_alpha()
        self.specialBG = pygame.image.load('assets/Goku/SpecialBG.png').convert_alpha()
    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        Kamekameha = KamePower(False,self.specialBG, self, players, self.skill, self.PowerBall)
        if (Kamekameha.Update(screen)): pass
        else: 
            isUsingSkill = False
            Kamekameha.setBack()

class Madara(Character):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        self.HP = 2000
        self.speed_run_animation = 0.01
        self.FramePerFight = 4
        self.SecPerFight = 0.1
        self.avatar = pygame.image.load('assets/Madara/avatar.png').convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (40,40))
        self.spritesFire.append(pygame.image.load('assets/Madara/Gunbai.png').convert_alpha())
        self.spritesFire.append(pygame.image.load('assets/Madara/Matsuki.png').convert_alpha())
        for i in range(6):
            text = 'assets/Madara/Move/' + str(i+1) + '.png'
            self.spritesRun.append(pygame.image.load(text).convert_alpha())
        for i in range(6):
            self.spritesRun.append(pygame.transform.flip(self.spritesRun[i], True, False))
        for i in range(20):
            text = 'assets/Madara/Fight/' + str(i+1) + '.png'
            self.spritesFight.append(pygame.image.load(text).convert_alpha())
        for i in range(20):
            self.spritesFight.append(pygame.transform.flip(self.spritesFight[i], True, False))
        for i in range(11):
            text = 'assets/Madara/Aura/' + str(i+1) + '.png'
            self.spritesAura.append(pygame.image.load(text).convert_alpha())
        for i in range(11):
            self.spritesAura.append(pygame.transform.flip(self.spritesAura[i], True, False))
        for i in range(3):
            text = 'assets/Madara/Indle/' + str(i+1) + '.png'
            self.spritesIndle.append(pygame.image.load(text).convert_alpha())
        for i in range(3):
            self.spritesIndle.append(pygame.transform.flip(self.spritesIndle[i], True, False))
        self.spritesHurt.append(pygame.image.load('assets/Madara/Hurt.png').convert_alpha()) 
        self.spritesHurt.append(pygame.transform.flip(self.spritesHurt[0], True, False))
        self.vocals.append(pygame.mixer.Sound('assets/Madara/SoundAura.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Madara/VocalMadara.mp3'))
        self.vocals.append(pygame.mixer.Sound('assets/Madara/VocalMadara1.mp3'))
        self.specialBG = pygame.image.load('assets/Madara/specialBG.png').convert_alpha()
        pygame.mixer.Sound.set_volume(self.vocals[0], 0.5)
        self.skill=[]
        for i in range(0,4,1):
            extend = str(i+1)
            text = 'assets/Madara/Skill/'+extend+'.png'
            self.skill.append(pygame.image.load(text))
        self.dragon=[]
        for i in range(0,15,1):
            extend = str(i+1)
            text = 'assets/Madara/GroundDragon/'+extend+'.png'
            self.dragon.append(pygame.image.load(text))

    def VirtualSpecialSkill(self, screen,team, players):
        global isUsingSkill
        Summoning = SummonWoodDragon(False,self.specialBG, self, players, self.skill, self.dragon)
        if (Summoning.Update(screen)): pass
        else: 
            isUsingSkill = False
            self.SpecialSkill = 'off'
            Summoning.setBack()

class Pain(MonoCharacter):
    def __init__(self, paraX, paraY):
        super().__init__(paraX, paraY)
        AICreator(self, 'PainCreator.txt')
        self.skill=[]
        for i in range(0,24,1):
            extend = str(i+1)
            text = 'assets/Pain/Skill/'+extend+'.png'
            self.skill.append(pygame.image.load(text))
    def VirtualSpecialSkill(self, screen, team, players):
        global isUsingSkill
        Push = AlmightyPush(False, self.specialBG, self, players, self.skill, 4)
        if (Push.Update(screen)): pass
        else: 
            isUsingSkill = False
            Push.setBack()