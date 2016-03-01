import pygame as pyg
from level import power_up
from utils import vector2
import math

class HUD(object):
	def __init__(self, screen, player, image_source, location, powerup_img):
		self.screen   = screen
		self.image    = pyg.image.load(image_source)
		self.location = location
		self.up_cooldown=pyg.image.load("Assets/Up_text.png").convert_alpha()
		self.down_cooldown=pyg.image.load("Assets/Down_text.png").convert_alpha()
		self.middle_cooldown=pyg.image.load("Assets/Middle_text.png").convert_alpha()
		self.up_cooldown2=pyg.image.load("Assets/Up_text2.png").convert_alpha()
		self.down_cooldown2=pyg.image.load("Assets/Down_text2.png").convert_alpha()
		self.middle_cooldown2=pyg.image.load("Assets/Middle_text2.png").convert_alpha()

		self.player = player
		
		self.top_left     = (location.x+7, location.y+11)
		self.top_right    = (self.top_left[0]+126, self.top_left[1])
		self.bottom_left  = (self.top_left[0], location.y+21)
		self.bottom_right = (self.top_right[0], self.bottom_left[1])
		self.height       = abs(self.top_left[1] - self.bottom_left[1])
		self.width        = abs(self.top_left[0] - self.top_right[0])
		self.color        = (255, 0, 0)

		self.font = pyg.font.SysFont("monospace", 15)

		#killcount display
		self.box = pyg.Rect(self.bottom_left[0], self.bottom_left[1]+1, self.width*4/5, self.height*2)
		#powerups display
		self.shieldpos = (self.box.left, self.box.top+self.box.height)
		self.healpos = (self.shieldpos[0], self.shieldpos[1]+35)
		self.shield = power_up(self.shieldpos, 2, powerup_img)
		self.heals = power_up(self.healpos, 1, powerup_img)

	def update_display(self, time_diff):
		self.shield.update(time_diff)
		self.heals.update(time_diff)
		
	def display(self):
		# first draw our image.
		self.screen.blit(self.image, (self.location.x, self.location.y))
		if self.player.top_attack.time_between_attacks<=0:
			self.screen.blit(self.up_cooldown, (self.location.x+180, self.location.y))
		else:
			self.screen.blit(self.up_cooldown2, (self.location.x+180, self.location.y))
		if self.player.middle_attack.time_between_attacks<=0:
			self.screen.blit(self.middle_cooldown, (self.location.x+260, self.location.y))
		else:
			self.screen.blit(self.middle_cooldown2, (self.location.x+260, self.location.y))
		if self.player.bottom_attack.time_between_attacks<=0:
			self.screen.blit(self.down_cooldown, (self.location.x+340, self.location.y))
		else:
			self.screen.blit(self.down_cooldown2, (self.location.x+340, self.location.y))
   
		bar = pyg.Rect(self.top_left[0], 
					   self.top_left[1], 
					   self.width * self.player.health / self.player.full_health, # now we draw it only as long as health.
					   self.height)

		#kill count text
		killct = self.font.render("Kills: " + str(self.player.enemies_killed), 1, (255,255,255) )
		#powerups count text
		shieldct = self.font.render("Shields: " + str(self.player.shields), 1, (255,255,255))
		healct = self.font.render("Heals: " + str(self.player.healths), 1, (255,255,255))

		# draw our rectangle on top of the image
		# 0 width means fill rectangle.
		pyg.draw.rect(self.screen, self.color, bar, 0)
		#pyg.draw.rect(self.screen, (0,0,0), box, 0)
		#draw killcount
		self.screen.blit(killct, (int(self.box.left+5), int(self.box.top+2)))
		#draw power up displays
		self.shield.draw(self.screen, vector2(0,0))
		self.heals.draw(self.screen, vector2(0,0))
		self.screen.blit(shieldct, (int(self.shieldpos[0]+30), int(self.shieldpos[1]+15)))
		self.screen.blit(healct, (int(self.healpos[0]+30), int(self.healpos[1]+15)))