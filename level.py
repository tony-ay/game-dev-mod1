from enemy import *
from random import randint

class Platform():
	#constructor
	def __init__(self, init_pos,width,height):
		self.pos = vector2(init_pos[0],init_pos[1])
		self.width=width
		self.height=height
		self.rect=pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)
	def update(self,changex,changey):
		self.pos.x=self.pos.x+changex
		self.rect.x=self.pos.x
		self.pos.y=self.pos.y+changey
		self.rect.y=self.pos.y
	def draw(self,screen):
		pygame.draw.rect(screen,(255,255,255),self.rect,0)

class Level():
	#constructor
	def __init__(self, player, platformz, img, DIM):
		#player sprite
		self.player=player
		#list of platform
		self.platforms=platformz
		#list of enemies
		self.enemy_image = "Assets/enemy_image_set.png"
		self.enemies = []
		#left/right movement
		self.background=img
		self.background_pos=vector2(0,0)
		self.screen_size=DIM

	def random_spawn(self, num):
		spawn_pos = [	(self.player.pos.x, self.player.pos.y-500), (self.player.pos.x+150, self.player.pos.y-500),
						(self.player.pos.x+300, self.player.pos.y-500), (self.player.pos.x+450, self.player.pos.y-500),
						(self.player.pos.x+600, self.player.pos.y-500), (self.player.pos.x+750, self.player.pos.y-500)	]

		for x in xrange(num):
			self.enemies.append( enemy(spawn_pos[randint(0,5)], (0,0), self.enemy_image))

	def update(self, time_dif):
		#this is basic premise of scrolling
		#we can fiddle with the multiplier to make it feel right

		#update all enemies and check if attacking player
		for enemy in self.enemies:
			enemy.update(time_dif, self.player)
			if enemy.life_timer <= 0:
				self.enemies.remove(enemy)
			elif enemy.get_center().subtract(self.player.get_center()).magnitude() <= self.player.dim[1]/2:
				self.player.health -= 8
				self.enemies.remove(enemy)

		#deal with platform collision and check if attacks hit enemies
		self.player.handle_collision(time_dif,self.platforms,self.enemies)	

		bgsize = self.background.get_size()
		#player dies, if going out of background bounds
		if self.player.pos.y >= bgsize[1]:
			self.player.health = 0
		
	def draw(self, screen):
		bg = self.background.copy()

		#draw all the platforms
		for obj in self.platforms:
			obj.draw(bg)
		#draw player
		self.player.draw(bg)
		#draw enemies
		for enemy in self.enemies:
			enemy.draw(bg)

		bgsize = bg.get_size()
		playerpos = self.player.get_center()

		screenposx = playerpos.x - self.screen_size[0]/2
		screenposy = playerpos.y - self.screen_size[1]/2

		if screenposx + self.screen_size[0] >= bgsize[0]:
			screenposx = bgsize[0] - self.screen_size[0]
		elif screenposx <= 0:
			screenposx = 0
		if screenposy + self.screen_size[1] >= bgsize[1]:
			screenposy = bgsize[1] - self.screen_size[1]
		elif screenposy <= 0:
			screenposy = 0

		screen.blit(bg, (-screenposx, -screenposy))

		#del(bg)