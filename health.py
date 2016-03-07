import pygame as pyg
from level import power_up
from utils import vector2
import math

class HUD(object):
	def __init__(self, screen, player, image_source, powerup_img):
		self.screen = screen
		self.image = pyg.image.load(image_source)
		screendim = self.screen.get_size()
		self.location = vector2(screendim[0]/2-300, screendim[1]-200)
		self.up_cooldown = pyg.image.load("Assets/Up_text.png").convert_alpha()
		self.down_cooldown = pyg.image.load("Assets/Down_text.png").convert_alpha()
		self.middle_cooldown = pyg.image.load("Assets/Middle_text.png").convert_alpha()
		self.up_cooldown2 = pyg.image.load("Assets/Up_text2.png").convert_alpha()
		self.down_cooldown2 = pyg.image.load("Assets/Down_text2.png").convert_alpha()
		self.middle_cooldown2 = pyg.image.load("Assets/Middle_text2.png").convert_alpha()
		self.low_health = pyg.image.load("Assets/Inject/low.png").convert_alpha()
		self.boss_text = {	'boss_found':	pyg.image.load("Assets/Inject/boss_found.png").convert_alpha(),
							'survive':		pyg.image.load("Assets/Inject/survive.png").convert_alpha(),
							'go_inject':	pyg.image.load("Assets/Inject/go_inject.png").convert_alpha(),
							'inject':		pyg.image.load("Assets/Inject/inject_now.png").convert_alpha()	}
		self.found_text_timer = 4000

		self.player = player
		
		self.top_left     = (self.location.x+7, self.location.y+11)
		self.top_right    = (self.top_left[0]+126, self.top_left[1])
		self.bottom_left  = (self.top_left[0], self.location.y+21)
		self.bottom_right = (self.top_right[0], self.bottom_left[1])
		self.height       = abs(self.top_left[1] - self.bottom_left[1])
		self.width        = abs(self.top_left[0] - self.top_right[0])
		self.color        = (0, 255, 0)

		self.font = pyg.font.SysFont("monospace", 15)

		#killcount display
		self.box = pyg.Rect(25, 25, self.width*4/5, self.height*2)
		#deathcount display
		self.box2 = pyg.Rect(self.box.left, self.box.top+self.box.height+1, self.width*4/5, self.height*2)
		#powerups display
		self.shieldpos = (self.top_left[0], self.bottom_left[1]+1+self.box.height)
		self.healpos = (self.shieldpos[0], self.shieldpos[1]+35)
		self.shield = power_up(self.shieldpos, 2, powerup_img)
		self.heals = power_up(self.healpos, 1, powerup_img)
		#display text center
		text_pos = (screendim[0]/2, 30)
		dim1 = self.boss_text['boss_found'].get_size()
		dim2 = self.boss_text['survive'].get_size()
		dim3 = self.boss_text['inject'].get_size()
		dim4 = self.boss_text['go_inject'].get_size()
		dim5 = self.low_health.get_size()
		self.boss_text_pos = {	'boss_found':	(text_pos[0]-dim1[0]/2, text_pos[1]),
								'survive':		(text_pos[0]-dim2[0]/2, text_pos[1]),
								'go_inject':	(text_pos[0]-dim4[0]/2, text_pos[1]),
								'inject':		(text_pos[0]-dim3[0]/2, text_pos[1])	}
		self.low_health_pos = (text_pos[0]-dim5[0]/2, text_pos[1]+70)

	def update_display(self, time_diff):
		self.shield.update(time_diff)
		self.heals.update(time_diff)

		if self.player.found_boss:
			if self.player.boss_moving:
				self.found_text_timer -= time_diff
		
	def display(self):
		# first draw our image.
		screendim = self.screen.get_size()
		textpos1 = (screendim[0]/2, screendim[1]-150)
		textpos2 = (textpos1[0]-100, textpos1[1])
		textpos3 = (textpos1[0]+90, textpos1[1])

		self.screen.blit(self.image, (self.location.x, self.location.y))
		if self.player.top_attack.time_between_attacks<=0:
			self.screen.blit(self.up_cooldown, textpos2)
		else:
			self.screen.blit(self.up_cooldown2, textpos2)
		if self.player.middle_attack.time_between_attacks<=0:
			self.screen.blit(self.middle_cooldown, textpos1)
		else:
			self.screen.blit(self.middle_cooldown2, textpos1)
		if self.player.bottom_attack.time_between_attacks<=0:
			self.screen.blit(self.down_cooldown, textpos3)
		else:
			self.screen.blit(self.down_cooldown2, textpos3)
   
		bar = pyg.Rect(self.top_left[0], 
					   self.top_left[1], 
					   self.width * self.player.health / self.player.full_health, # now we draw it only as long as health.
					   self.height)

		#display boss text
		if self.player.found_boss:
			if self.player.boss_moving:
				if self.found_text_timer > 0:
					#draw found text
					self.screen.blit(self.boss_text['boss_found'], self.boss_text_pos['boss_found'])
				elif self.player.can_inject:
					#draw inject text
					self.screen.blit(self.boss_text['inject'], self.boss_text_pos['inject'])
				else:
					self.screen.blit(self.boss_text['go_inject'], self.boss_text_pos['go_inject'])
			else:
				#draw survive text
				self.screen.blit(self.boss_text['survive'], self.boss_text_pos['survive'])

		#display low health
		if self.player.health <= self.player.full_health * 1/3:
			self.screen.blit(self.low_health, self.low_health_pos)

		#kill count text
		killct = self.font.render("Kills: " + str(self.player.enemies_killed), 1, (255,255,255) )
		#death count text
		deathct = self.font.render("Deaths: " + str(self.player.deaths), 1, (255,255,255) )
		#powerups count text
		shieldct = self.font.render("Shields: " + str(self.player.shields), 1, (255,255,255))
		healct = self.font.render("Heals: " + str(self.player.healths), 1, (255,255,255))

		# draw our rectangle on top of the image
		# 0 width means fill rectangle.
		pyg.draw.rect(self.screen, self.color, bar, 0)
		#draw killcount
		self.screen.blit(killct, (int(self.box.left+5), int(self.box.top+2)))
		self.screen.blit(deathct, (int(self.box2.left+5), int(self.box2.top+2)))
		#draw power up displays
		self.shield.draw(self.screen, vector2(0,0))
		self.heals.draw(self.screen, vector2(0,0))
		self.screen.blit(shieldct, (int(self.shieldpos[0]+30), int(self.shieldpos[1]+15)))
		self.screen.blit(healct, (int(self.healpos[0]+30), int(self.healpos[1]+15)))