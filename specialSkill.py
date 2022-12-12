from hashlib import pbkdf2_hmac
from turtle import update
import pygame

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

def drawItems(screen, object, x, y):
    screen.blit(object, object.get_rect(center=(x,y)))

def increaseFrame(frame, lenframe, value):
    if (frame<=lenframe-1): return value
    else: return 0

class Special(metaclass=Singleton):
    def __init__(self, isTrans, linkBG, user, opponents):
        self.time = 0
        if (isTrans): self.trans = 50
        else: self.trans = -1
        self.user = user
        self.opponents = opponents
        self.bg = linkBG
        self.SingleCall = True
    def SingletonCall(self):
        if (self.SingleCall):
            self.SingleCall = False
            for opponent in self.opponents: 
                opponent.canControl = False
    def Endtask(self):
        self.user.SpecialSkill = 'off'
        for opponent in self.opponents: 
            opponent.canControl = True
        self.user.canControl = True
    def Update(self, screen):
        self.time+=1
        if (self.trans==-1): pass
        else: 
            if (self.trans>=1): self.trans-=1
            s = pygame.Surface((1000,750))
            s.set_alpha(128) 
            if (self.trans!=0): self.trans-=1
            s.fill((self.trans,self.trans,self.trans))
            screen.blit(s, (0,0))
        if (self.bg=='none'): pass
        else: screen.blit(self.bg, self.bg.get_rect(center=(500,375)))
    def setBack(self):
        self.time = 0
        if (self.trans==0): self.trans=50

class Sharingan(Special):
    def __init__(self, isTrans, linkBG, user, opponents):
        super().__init__(isTrans, linkBG, user, opponents)
    def Update(self, screen):
        super().Update(screen)
        if (self.SingleCall):
            self.user.speed, self.user.jump_speed = 2, 1.5
            self.user.speeed_fire = 3
            self.user.thread_run_animation=1
            self.user.speed_thread_animation = 0.1
            for opponent in self.opponents: 
                if (opponent!=self.user):
                    opponent.canControl = False
            self.user.damageFight = 100
            self.SingleCall = False
        if (self.time==800): 
            self.user.vocals[1].stop()
            self.user.vocals[2].play()
            return True
        elif (self.time==3000):
            self.user.vocals[2].stop()
            self.user.SpecialSkill = 'off'
            self.user.dameFight = 20
            self.user.time, self.user.transparent = 0, 50
            self.user.speed, self.user.jump_speed = 0.8, 1
            self.user.speeed_fire, self.user.speed_thread_animation = 1.5, 0.01
            self.user.speed_run_animation = 0.05
            for opponent in self.opponents: 
                if (opponent!=self.user):
                    opponent.canControl = True
            self.SingleCall = True
            return False
        else: return True

class ChidoriPunch(Special):
    def __init__(self, isTrans, linkBG, user, opponents, frame, noFrameMove):
        super().__init__(isTrans, linkBG, user, opponents)
        self.currentFrame = 0
        self.frame = frame
        self.command = 'wait'
        self.frameMove = noFrameMove
        self.delay = 0.5
        self.SingleCall = True
        self.damge = 3
        self.frameDamage = self.frameMove
    def checkHit(self):
        for opponent in self.opponents:
            if (self.currentFrame>=self.frameMove and
                self.command!='wait' and
                self.user!=opponent and
                self.user.main.get_rect(center=(self.user.posX, self.user.posY)).
                colliderect(
                    opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                opponent.GetHit(self.damge,self.user,self.delay,'fight')
    def PressAttack(self):
        self.user.isFighting = False
        self.user.canControl = False
        if (self.user.mainDirect=='left'):
            self.command = 'fightLeft'
        else: self.command = 'fightRight'
        self.user.vocals[1].stop()
        self.user.vocals[2].play()
    def SingletonCall(self):
        if (self.SingleCall):
            self.SingleCall = False
            for opponent in self.opponents: 
                opponent.canControl = False
        else: return
    def Endtask(self):
        self.user.SpecialSkill = 'off'
        for opponent in self.opponents: 
            opponent.canControl = True
        self.user.canControl = True
        self.SingleCall = True
        self.user.StandBack()
    def Action(self):
        if (self.command=='fightLeft'): 
            self.user.main = self.frame[int(self.currentFrame)]
            if (self.currentFrame>=self.frameMove):
                self.user.posX -= 1
        else: 
            self.user.main = pygame.transform.flip(self.frame[int(self.currentFrame)], True, False)
            if (self.currentFrame>=self.frameMove):
                self.user.posX += 1
        self.currentFrame+=0.05
    def Update(self, screen):
        super().Update(screen)
        self.checkHit()
        self.SingletonCall()
        if (self.user.isFighting): 
            self.PressAttack()
            return True
        elif (self.command=='end' or self.user.isAlive()==False):
            self.Endtask()
            return False
        elif (int(self.currentFrame)==len(self.frame)):
            self.command = 'end'
            return True
        elif (self.command=='fightLeft' or self.command=='fightRight'):
            self.Action()
            return True
        else: return True
    def setBack(self):
        self.currentFrame = 0
        self.command = 'wait'
        return super().setBack()

class GaintPistol(ChidoriPunch):
    def __init__(self, isTrans, linkBG, user, opponents, frame, noFrameDame):
        super().__init__(isTrans, linkBG, user, opponents, frame, 10000000)
        self.movement = 0
        self.delay = 5
        self.damge = 10
        self.frameDamage = noFrameDame
    def checkHit(self):
        for opponent in self.opponents:
            if (self.currentFrame>=self.frameDamage and
                self.command!='wait' and
                self.user!=opponent and
                self.user.main.get_rect(center=(self.user.posX, self.user.posY)).
                colliderect(
                    opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                opponent.GetHit(self.damge,self.user,self.delay,'fight')
    def PressAttack(self):
        return super().PressAttack()
    def Update(self, screen):
        return super().Update(screen)
    def setBack(self):
        return super().setBack()

class Sussano(GaintPistol):
    def __init__(self, isTrans, linkBG, user, opponents, frame, noFrameDame):
        super().__init__(isTrans, linkBG, user, opponents, frame, noFrameDame)
        self.delay = 0
    def checkHit(self):
        for opponent in self.opponents:
            if ((
                (self.currentFrame>=10 and self.currentFrame<=12) or
                (self.currentFrame>=21 and self.currentFrame<=22) or
                (self.currentFrame>=32 and self.currentFrame<=33)
                ) and
                opponent.isFront(self.user) and
                self.command!='wait' and
                self.user!=opponent and
                self.user.main.get_rect(center=(self.user.posX, self.user.posY)).
                colliderect(
                    opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                opponent.GetHit(self.damge,self.user,self.delay,'fight')
    def setBack(self):
        self.user.vocals[2].stop()
        return super().setBack()

class SummonWindy(Special):
    def __init__(self, isTrans, linkBG, user, opponents, frame, fire):
        super().__init__(isTrans, linkBG, user, opponents)
        self.currentFrame = 0
        self.frame = frame
        self.frameSpeed = 0.05
        self.command = 'wait'
        self.delay = 0.5
        self.SingleCall = True
        self.ultraFire = fire
        self.isFire = False
        self.fireX = 0
        self.fireY = 0
        self.fireDirect = 'fightLeft'
        self.FrameFire = 8
        self.FireSpeed =1.5
        self.damage = 3
    def checkHit(self):
        for opponent in self.opponents:
            if (self.currentFrame>=self.frameMove and
                self.command!='wait' and
                self.user!=opponent and
                self.user.main.get_rect(center=(self.user.posX, self.user.posY)).
                colliderect(
                    opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                opponent.GetHit(2,self.user,self.delay,'fight')
    def PressAttack(self):
        self.user.isFighting = False
        self.user.canControl = False
        if (self.user.mainDirect=='left'):
            self.command = 'fightLeft'
        else: self.command = 'fightRight'
        self.user.vocals[1].stop()
        self.user.vocals[2].play()
    def SingletonCall(self):
        if (self.SingleCall):
            self.SingleCall = False
            for opponent in self.opponents: 
                if (opponent!=self.user):
                    opponent.canControl = False
        else: return
    def Endtask(self):
        self.user.SpecialSkill = 'off'
        for opponent in self.opponents: 
            opponent.canControl = True
        self.user.canControl = True
        self.SingleCall = True
        self.user.StandBack()
    def checkHit(self):
        for opponent in self.opponents:
            if (opponent.isCollision(self.ultraFire, self.fireX, self.fireY)):
                opponent.GetHit(self.damage, self.user, self.delay, 'fire')
            else: pass
    def Action(self):
        # current Frame move
        if (int(self.currentFrame)==self.FrameFire and self.isFire==False):
            if (self.command!=self.fireDirect):
                self.ultraFire = pygame.transform.flip(self.ultraFire, True, False)
                self.fireDirect=self.command
            self.fireX, self.fireY = self.user.posX, self.user.posY
            self.isFire = True
        if (int(self.currentFrame)>=int(len(self.frame))):
            self.user.StandBack()
        elif (self.command=='fightLeft'): 
            self.user.main = self.frame[int(self.currentFrame)]
        else: 
            self.user.main = pygame.transform.flip(self.frame[int(self.currentFrame)], True, False)
        self.currentFrame+=self.frameSpeed
    def Update(self, screen):
        super().Update(screen)
        if (self.isFire):
            #fire move
            screen.blit(self.ultraFire, self.ultraFire.get_rect(center=(self.fireX, self.fireY)))
            if (self.command=='fightLeft'): 
                self.fireX-=self.FireSpeed
            else: self.fireX+=self.FireSpeed
        self.checkHit()
        self.SingletonCall()
        if (self.user.isFighting): 
            self.PressAttack()
            return True
        elif (self.command=='end' or self.user.isAlive()==False):
            self.Endtask()
            return False
        elif (self.fireX<0 or self.fireX>1000):
            self.command = 'end'
            return True
        elif (self.command=='fightLeft' or self.command=='fightRight'):
            self.Action()
            return True
        else: return True
    def setBack(self):
        self.currentFrame = 0
        self.command = 'wait'
        self.isFire = False
        self.fireX = 0
        self.fireY = 0
        return super().setBack()

class KamePower(SummonWindy):
    def __init__(self, isTrans, linkBG, user, opponents, frame, fire):
        super().__init__(isTrans, linkBG, user, opponents, frame, fire)
        self.FrameFire = 17
        self.FireSpeed = 1
        self.frameSpeed = 0.02
        self.damage = 2

class SummonWoodDragon(Special):
    def __init__(self, isTrans, linkBG, user, opponents, frame, skill):
        super().__init__(isTrans, linkBG, user, opponents)
        self.frame = frame
        self.skill = skill
        self.currentFrame = 0
        self.currentSkill = 0
        self.spaceDist = 170
        self.command = 'wait'
        self.damage = 1
        self.delay = 0
    def checkHit(self, object):
        for opponent in self.opponents:
            for i in range(0,100,20):
                if (self.user.mainDirect=='left' and
                    self.currentSkill>=6 and
                    self.command!='wait' and
                    object.get_rect(center=(self.user.posX-self.spaceDist-i, self.user.posY)).
                    colliderect(
                        opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                    opponent.GetHit(self.damage,self.user,self.delay,'fight')
                elif (self.user.mainDirect=='right' and
                    self.currentSkill>=6 and
                    self.command!='wait' and
                    object.get_rect(center=(self.user.posX+self.spaceDist+i, self.user.posY)).
                    colliderect(
                        opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                    opponent.GetHit(self.damage,self.user,self.delay,'fight')
    def PressAttack(self):
        if self.user.isFighting and self.command=='wait':
            self.user.canControl = False
            self.command = 'fight'
            self.user.vocals[1].stop()
            self.user.vocals[2].play()
    def FrameMove(self):
        if (int(self.currentFrame)>=len(self.frame)-1): return
        if self.user.mainDirect == 'left':
            self.user.main = self.frame[int(self.currentFrame)]
        else:
            self.user.main = pygame.transform.flip(self.frame[int(self.currentFrame)], True, False)
        self.currentFrame+=increaseFrame(self.currentFrame, len(self.frame), 0.01)
    def SkillMove(self, screen):
        if (int(self.currentFrame)<len(self.frame)-1): return
        for i in range(0,100,20):
            if self.user.mainDirect == 'left':
                drawItems(screen, self.skill[int(self.currentSkill)], self.user.posX-self.spaceDist-i, self.user.posY)
                object = pygame.transform.flip(self.skill[int(self.currentSkill)], True, False)
                drawItems(screen, object, self.user.posX-self.spaceDist-i, self.user.posY)
            else:
                drawItems(screen, self.skill[int(self.currentSkill)], self.user.posX+self.spaceDist+i, self.user.posY)
                object = pygame.transform.flip(self.skill[int(self.currentSkill)], True, False)
                drawItems(screen, object, self.user.posX+self.spaceDist+i, self.user.posY)
        self.currentSkill+=increaseFrame(self.currentSkill, len(self.skill), 0.04)
    def Update(self, screen):
        super().Update(screen)
        self.SingletonCall()
        self.PressAttack()
        if (int(self.currentSkill)==len(self.skill)-1):
            self.Endtask()
            return False
        if (self.command=='fight'):
            self.FrameMove()
            self.SkillMove(screen)
            self.checkHit(self.skill[int(self.currentSkill)])
        return True
    def setBack(self):
        self.currentFrame = 0
        self.currentSkill = 0
        self.command = 'wait'
        return super().setBack()

class AlmightyPush(Sussano):
    def __init__(self, isTrans, linkBG, user, opponents, frame, noFrameDame):
        super().__init__(isTrans, linkBG, user, opponents, frame, noFrameDame)
        self.damge = 2
        self.delay = 0
        self.pressure = 0
    def checkHit(self):
        for opponent in self.opponents:
            if ((self.currentFrame>=4 and self.currentFrame<=24)
                and
                opponent.isFront(self.user) and
                self.command!='wait' and
                self.user!=opponent and
                self.user.main.get_rect(center=(self.user.posX, self.user.posY)).
                colliderect(
                    opponent.main.get_rect(center=(opponent.posX,opponent.posY)))):
                opponent.GetHit(self.damge,self.user,self.delay,'fight')
    def Update(self, screen):
        if (self.command != 'wait'):
            for enemy in self.opponents:
                if (enemy.posX>self.user.posX): self.pressure = -0.5
                else: self.pressure = 0.5
                enemy.posX += self.pressure
        return super().Update(screen)