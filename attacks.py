import pygame

class middle_attack:
    def __init__(self):
        self.sound = pygame.mixer.Sound("Assets/Sounds/mid_attack.wav")
        self.attacking=False
        self.frame=0
        self.time_between_attacks=1000
        self.time_between_frames=75
        self.time_since_last_frame=0
        self.frame_ct=7
        self.img_W=300
        self.img_H=180
    def update(self,time_diff):
        self.time_between_attacks-=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks<=0 :
            self.attacking=True
	    self.sound.play()
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                     self.attacking=False
                     self.time_between_attacks=1000
    def reset(self):
        self.attacking=False
        self.frame=0
        self.time_between_attacks=1000
        self.sound.stop()
class up_attack:
    def __init__(self):
        self.attacking=False
        self.frame=0
        #up attack sound
        self.up_sound = pygame.mixer.Sound("Assets/Sounds/hit.wav")
        self.time_between_attacks=850
        self.time_between_frames=75
        self.time_since_last_frame=0
        self.frame_ct=12
        self.img_W=328
        self.img_H=271
    def update(self,time_diff):
        self.time_between_attacks-=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks<=0:
            self.attacking=True
	    self.up_sound.play()
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                     self.attacking=False
                     self.time_between_attacks=850
                     self.up_sound.stop()
    def reset(self):
        self.attacking=False
        self.frame=0
        self.time_between_attacks=850
        self.up_sound.stop()
class down_attack:
    def __init__(self):
        self.down_sound = pygame.mixer.Sound("Assets/Sounds/down.wav")
        self.attacking=False
        self.frame=0
        self.time_between_attacks=450
        self.time_between_frames=50
        self.time_since_last_frame=0
        self.frame_ct=10
        self.img_W=307
        self.img_H=295
        self.amount=0
    def update(self,time_diff):
        self.time_between_attacks-=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks<=0:
            self.attacking=True
            self.down_sound.play()
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0 :
                    self.amount+=1
                    if self.amount==1:
                        self.attacking=False
                        self.time_between_attacks=450
                        self.amount=0
    def reset(self):
        self.down_sound.stop()
        self.attacking=False
        self.frame=0
        self.amount=0
                         
class jump:
    def __init__(self):
        self.jumping=False
        self.frame=0
        self.time_between_frames=100
        self.time_since_last_frame=0
        self.frame_ct=2
        self.img_W=250
        self.img_H=180
    def update(self,time_diff):
        self.time_since_last_frame+=time_diff
    def jump(self):
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                
class shield:
    def __init__(self):
        self.frame=0
        self.time_between_frames=200
        self.time_since_last_frame=0
        self.frame_ct=13
        self.img_W=239
        self.img_H=255
        self.amount=0
        self.shield_sound = pygame.mixer.Sound("Assets/Sounds/shield.wav")
        self.shield_sound.set_volume(0.7)
    def update(self,time_diff):
        self.time_since_last_frame+=time_diff
    def use(self):
            if self.time_between_frames<=self.time_since_last_frame:
                self.shield_sound.play()
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                    self.amount+=1
    def reset(self):
        self.frame=0
        self.time_since_last_frame=0
        self.shield_sound.stop()
class injection:
    def __init__(self):
        self.attacking=False
        self.frame=0
        self.time_between_attacks=3000
        self.time_between_frames=50
        self.time_since_last_frame=0
        self.frame_ct=25
        self.img_W=211
        self.img_H=220
        self.sound = pygame.mixer.Sound("Assets/Sounds/inject.wav")
        self.sound.set_volume(0.5)
    def update(self,time_diff):
        self.time_between_attacks-=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks<=0 :
            self.attacking=True
            self.sound.play()
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                    self.attacking = False
                    self.time_between_attacks = 3000
                    return True
        return False
    def reset(self):
        self.sound.stop()
        self.attacking=False
        self.frame=0
        self.time_between_attacks = 3000
