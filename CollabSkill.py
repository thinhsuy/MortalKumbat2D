import pygame

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

def checkName(object):
    return object.__class__.__name__

def drawItems(screen, object, x, y):
    screen.blit(object, object.get_rect(center=(x,y)))

def increaseFrame(frame, lenframe, value):
    if (frame<=lenframe-1): return value
    else: return 0


class CollabSpecial(metaclass=Singleton):
    def __init__(self, linkBG, team, opponents, set):
        self.time = 0
        self.team = team
        self.opponents = opponents
        self.bg = linkBG
        self.SingleCall = True
        self.set = set
    def SingletonCall(self):
        if (self.SingleCall):
            self.SingleCall = False
            for opponent in self.opponents: 
                opponent.canControl = False
            for user in self.team:
                user.canControl = False
                user.isCollabing = True
    def EndTask(self):
        for user in self.team: 
            user.SpecialKill = 'off'
            user.canControl = True
            user.StandBack()
            user.isCollabing = False
        for opponent in self.opponents: 
            opponent.canControl = True
        for user in self.team:
            user.canControl = True
    def Update(self, screen):
        self.SingletonCall()
        self.time+=1
        if (self.bg=='none'): pass
        else: screen.blit(self.bg, self.bg.get_rect(center=(500,375)))
    def setBack(self):
        self.time = 0
        self.SingleCall = True
        for user in self.team:
            user.SpecialSkill = 'off'

class UchihaUnbond(CollabSpecial):
    def __init__(self, linkBG, team, opponents, set):
        super().__init__(linkBG, team, opponents, set)
        self.frameUser1 = 0
        self.sharinganEffect = 0
        self.blackfireEffect = 0
        self.frameUser2 = 0
        self.chidoriEffect = 0
        self.nextAction = False
    def checkHit(self, frame, value, delay):
        for enemy in self.opponents:
            if (enemy.main.get_rect(center=(enemy.posX, enemy.posY)).colliderect(
                frame.get_rect(center=(enemy.posX, enemy.posY))
            )):
                for user in self.team: 
                    if (checkName(user)=='Itachi'):
                        enemy.GetHit(value, user, delay, 'fight')
    def AdditionalEffectForCharacter(self, screen, user):
        if (int(self.frameUser1)>=5):
            self.sharinganEffect+=increaseFrame(self.sharinganEffect,int(len(self.set[0])), 0.05)
        drawItems(screen, self.set[0][int(self.sharinganEffect)], user.posX, user.posY-50)
    def Flameflare(self, screen):
        if (int(self.sharinganEffect)>=len(self.set[0])-1 and int(self.blackfireEffect)<len(self.set[2])-1):
            for enemy in self.opponents:
                drawItems(screen, self.set[2][int(self.blackfireEffect)], enemy.posX, enemy.posY)
            self.checkHit(self.set[2][int(self.blackfireEffect)], 2, 0)
            self.blackfireEffect+=increaseFrame(self.blackfireEffect, len(self.set[2]), 0.05)
        elif (int(self.blackfireEffect)==len(self.set[2])-1): self.nextAction = True
    def ChidoriNet(self, screen):
        if (int(self.frameUser2)>=15):
            drawItems(screen, self.set[4][int(self.chidoriEffect)], 500,325)
            self.checkHit(self.set[4][int(self.chidoriEffect)], 1.5, 0.2)
            self.chidoriEffect+=increaseFrame(self.chidoriEffect, len(self.set[4]), 0.05)
    def EndTask(self):
        for user in self.team:
            if (int(self.chidoriEffect)==len(self.set[4])-1 or user.isAlive()==False):
                super().EndTask()
                return True
        return False
    def Action(self, screen):
        for partner in self.team:
            if (checkName(partner)=='Itachi' and self.nextAction==False):
                if (partner.mainDirect=='left'):
                    partner.main = self.set[1][int(self.frameUser1)]
                    self.frameUser1+= increaseFrame(self.frameUser1, len(self.set[0]), 0.01)
                elif (partner.mainDirect=='right'):
                    partner.main = pygame.transform.flip(self.set[1][int(self.frameUser1)], True, False)
                    self.frameUser1+= increaseFrame(self.frameUser1, len(self.set[0]), 0.01)
                self.AdditionalEffectForCharacter(screen, partner)
            if (checkName(partner)=='Sasuke' and self.nextAction):
                partner.posX = 500
                partner.main = self.set[3][int(self.frameUser2)]
                self.frameUser2+=increaseFrame(self.frameUser2, len(self.set[3]), 0.05)
        return True
    def Update(self, screen):
        super().Update(screen)
        if (self.EndTask()): return False
        self.Flameflare(screen)
        self.ChidoriNet(screen)
        if(self.Action(screen)): return True
    def setBack(self):
        self.frameUser1 = 0
        self.sharinganEffect = 0
        self.blackfireEffect = 0
        self.frameUser2 = 0
        self.chidoriEffect = 0
        self.nextAction = False
        return super().setBack()

