class middle_attack:
    def __init__(self):
        self.attacking=False
        self.frame=0
        self.time_between_attacks=0
        self.time_between_frames=50
        self.time_since_last_frame=0
        self.frame_ct=7
        self.img_W=300
        self.img_H=180
    def update(self,time_diff):
        self.time_between_attacks+=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks>=1000 :
            self.attacking=True
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                     self.attacking=False
                     self.time_between_attacks=0
class up_attack:
    def __init__(self):
        self.attacking=False
        self.frame=0
        self.time_between_attacks=0
        self.time_between_frames=50
        self.time_since_last_frame=0
        self.frame_ct=7
        self.img_W=300
        self.img_H=180
    def update(self,time_diff):
        self.time_between_attacks+=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks>=850:
            self.attacking=True
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                     self.attacking=False
                     self.time_between_attacks=0
class down_attack:
    def __init__(self):
        self.attacking=False
        self.frame=0
        self.time_between_attacks=0
        self.time_between_frames=50
        self.time_since_last_frame=0
        self.frame_ct=7
        self.img_W=300
        self.img_H=180
    def update(self,time_diff):
        self.time_between_attacks+=time_diff
        self.time_since_last_frame+=time_diff
    def attack(self):
        if self.time_between_attacks>=450:
            self.attacking=True
            if self.time_between_frames<=self.time_since_last_frame:
                self.frame=(self.frame+1)%self.frame_ct
                self.time_since_last_frame=0
                if self.frame==0:
                     self.attacking=False
                     self.time_between_attacks=0
