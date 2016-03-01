from enemy import *
from random import randint
from ani_vars import *

#general platform class
class platform():
	def __init__(self, pos, width, height):
		#platform rect attributes
		self.pos = vector2(pos[0], pos[1])
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

	def get_rect(self):
		imgdim = self.img.get_size()
		return pygame.Rect(self.imgpos.x, self.imgpos.y, imgdim[0], imgdim[1])

	def draw(self, screen, screenpos):
		drawpos = self.imgpos.subtract(screenpos)
		screen.blit(self.img, (drawpos.x, drawpos.y))

#specific platform classes
class platform5(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 1800, 73)
		self.img = img[0]
		self.imgpos = vector2(self.pos.x-43, self.pos.y-78)

class platform6(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 820, 110)
		self.img = img[1]
		self.imgpos = vector2(self.pos.x-35, self.pos.y-100)
class platform7(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 1060, 45)
		self.img = img[2]
		self.imgpos = vector2(self.pos.x-40, self.pos.y-75)

class platform8(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 478, 44)
		self.img = img[3]
		self.imgpos = vector2(self.pos.x-42, self.pos.y-39)

class platform9(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 478, 44)
		self.img = img[4]
		self.imgpos = vector2(self.pos.x-42, self.pos.y-39)

class platform10(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 293, 55)
		self.img = img[5]
		self.imgpos = vector2(self.pos.x-27, self.pos.y-25)

class power_up():
		def __init__(self,init_pos, power_up_type, img):
			self.power_up_type=power_up_type
			if self.power_up_type==2:
				self.img = img[0]
				self.width=35
				self.height=35
				self.ani_var=ani_var(5,self.width,self.height,150)
			else:
				self.img = img[1]
				self.width=25
				self.height=46
				self.ani_var=ani_var(7,self.width,self.height,150)
			self.pos = vector2(init_pos[0], init_pos[1])
			self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
			self.destroy=0

		def get_rect(self):
			return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

		def update(self,time_diff):
			self.ani_var.update(time_diff)
			if self.ani_var.time_between_frames<=self.ani_var.time_since_last_frame:
				self.ani_var.frame=(self.ani_var.frame+1)%self.ani_var.frame_ct
				self.ani_var.time_since_last_frame=0

		def draw(self,screen,screenpos):
			drawpos = self.pos.subtract(screenpos)
			clip = pygame.Rect(self.width*self.ani_var.frame, 0, self.width, self.height )
			screen.blit(self.img, ( int(drawpos.x), int(drawpos.y)), area=clip)

#class for world environment
class Level():
	#constructor
	def __init__(self, player, img, DIM, platform_img, powerup_img):
		#player sprite
		self.player=player
		self.platform_img = platform_img
		self.powerup_img = powerup_img
		#platform setup for world
		self.platforms = [	platform7((50, 9104), platform_img), platform7((1500, 9100), platform_img),
							platform7((3000, 9150), platform_img), platform7((4500, 9050), platform_img),
							platform7((6100, 9000), platform_img), platform7((7600, 8950), platform_img),
							platform7((9200, 9050), platform_img), platform7((10000, 8800), platform_img),
							platform7((450, 8750), platform_img), platform7((1800, 8450), platform_img),
							platform7((3200, 8250), platform_img), platform7((4500, 8000), platform_img),
							platform7((4950, 8400), platform_img), platform7((6350, 8100), platform_img),
							platform7((7700, 7850), platform_img), platform7((6350, 7500), platform_img),
							platform7((5000, 7200), platform_img), platform7((3700, 6950), platform_img),
							platform7((2350, 7300), platform_img), platform7((1000, 7000), platform_img),
							platform7((-400, 6700), platform_img), platform7((-950, 8900), platform_img)	]
		#list of enemies
		self.enemy_image = pygame.image.load("Assets/enemy_image_set.png").convert_alpha()
		self.enemies = []
		self.MAX_ENEMIES = 15
		self.ENEMY_SPAWN_TIMER = 0
		#list of power ups
		self.power_ups=[power_up((600,8900),1, powerup_img), power_up((900,8900),2, powerup_img)]
		#left/right movement
		self.background=img
		self.background_pos=vector2(0,0)
		self.screen_size=DIM

	def random_spawn(self):
		spawn_pos = [	(self.player.pos.x, self.player.pos.y-500), 
						(self.player.pos.x+150, self.player.pos.y-500),
						(self.player.pos.x+300, self.player.pos.y-500), 
						(self.player.pos.x+450, self.player.pos.y-500),
						(self.player.pos.x+600, self.player.pos.y-500), 
						(self.player.pos.x+750, self.player.pos.y-500)	]

		self.enemies.append( enemy(spawn_pos[randint(0,5)], (0,0), self.enemy_image))

	def update(self, time_dif, keys):
		self.player.update(time_dif, keys, self.platforms)

		#if not enough enemies, spawn enemies on timer
		if self.ENEMY_SPAWN_TIMER > 800:
			if len(self.enemies) < self.MAX_ENEMIES:
				for x in xrange(randint(1,4)):
					self.random_spawn()
			self.ENEMY_SPAWN_TIMER = 0
		self.ENEMY_SPAWN_TIMER += time_dif

		#update all enemies and check if attacking player
		for enemy in self.enemies:
			enemy.update(time_dif, self.player)
			if enemy.life_timer <= 0:
				self.enemies.remove(enemy)
			elif enemy.get_center().subtract(self.player.get_center()).magnitude() <= self.player.dim[1]/2:
				if self.player.immune==0:
					self.player.health -= 5
				self.enemies.remove(enemy)

		#deal with platform or power up collision and check if attacks hit enemies 
		self.player.handle_collision(time_dif,self.platforms,self.enemies,self.power_ups)	

		bgsize = self.background.get_size()
		
		#update power ups
		for powers in self.power_ups:
			if powers.destroy==1:
				self.power_ups.remove(powers)
			else: 
				powers.update(time_dif)

		#player dies, if going out of background bounds
		if self.player.pos.y >= bgsize[1]:
			self.player.health = 0
		
	def draw(self, screen):

		bgsize = self.background.get_size()
		playerpos = self.player.get_center()

		#calculate position of camera relative to player
		screenpos = vector2(playerpos.x - self.screen_size[0]/2, playerpos.y - self.screen_size[1]/2)

		#keep camera within bounds of background image
		if screenpos.x + self.screen_size[0] >= bgsize[0]:
			screenpos.x = bgsize[0] - self.screen_size[0]
		elif screenpos.x <= 0:
			screenpos.x = 0
		if screenpos.y + self.screen_size[1] >= bgsize[1]:
			screenpos.y = bgsize[1] - self.screen_size[1]
		elif screenpos.y <= 0:
			screenpos.y = 0

		#clip of screen size
		screenrect = pygame.Rect(screenpos.x, screenpos.y, self.screen_size[0], self.screen_size[1])
		#screen.blit(self.background, (-screenpos.x, -screenpos.y))
		screen.blit(self.background, (0,0), area=screenrect)

		#draw all the platforms in screen
		for obj in self.platforms:
			if screenrect.colliderect(obj.get_rect()):
				obj.draw(screen, screenpos)
		#draw player
		self.player.draw(screen, screenpos)
		#draw enemies in screen
		for enemy in self.enemies:
			if screenrect.colliderect(enemy.get_hitbox()):
				enemy.draw(screen, screenpos)
		#draw power_ups in screen
		for powers in self.power_ups:
			if screenrect.colliderect(powers.get_rect()):
				powers.draw(screen,screenpos)
