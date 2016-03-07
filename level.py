from enemy import *
from random import randint
from ani_vars import *
from boss import *

#general platform class
class platform():
	def __init__(self, pos, width, height):
		#platform rect attributes
		self.pos = vector2(pos[0], pos[1])
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
		self.inject = False

	def get_rect(self):
		imgdim = self.img.get_size()
		return pygame.Rect(self.imgpos.x, self.imgpos.y, imgdim[0], imgdim[1])

	def draw(self, screen, screenpos):
		drawpos = self.imgpos.subtract(screenpos)
		screen.blit(self.img, (drawpos.x, drawpos.y))

#specific platform classes
class platform5(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 1800, 70)
		self.img = img[0]
		self.imgpos = vector2(self.pos.x-43, self.pos.y-91)

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

class platformI(platform):
	def __init__(self, pos, img):
		platform.__init__(self, pos, 293, 55)
		self.img = img[6]
		self.imgpos = vector2(self.pos.x-27, self.pos.y-25)
		self.inject = True
		inj_dim = (self.rect.width, 300)
		self.inj_rect = pygame.Rect(self.pos.x, self.pos.y-inj_dim[1], inj_dim[0], inj_dim[1])

#powerup class - shield == type 2, heal == type 1
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
			if self.ani_var.time_between_frames <= self.ani_var.time_since_last_frame:
				self.ani_var.frame=(self.ani_var.frame+1)%self.ani_var.frame_ct
				self.ani_var.time_since_last_frame = 0

		def draw(self,screen,screenpos):
			drawpos = self.pos.subtract(screenpos)
			clip = pygame.Rect(self.width*self.ani_var.frame, 0, self.width, self.height )
			screen.blit(self.img, ( int(drawpos.x), int(drawpos.y)), area=clip)

#class for world environment
class Level():
	#constructor
	def __init__(self, player, img, screen_dim, image_dict, difficulty):
		#player sprite
		self.player=player
		#images needed
		self.image_dict = image_dict
		self.background=img
		self.screen_size = screen_dim
		#boss area
		self.boss_area_pos = (5600, 2200)
		self.boss_area = boss_area(self.boss_area_pos, self.image_dict['boss'])
		#platform setup for world
		self.platforms = [	platform7((200, 9104), self.image_dict['platform']),
							platform5((2000, 9100), self.image_dict['platform']),
							platform7((4500, 9050), self.image_dict['platform']),
							platform7((6100, 9000), self.image_dict['platform']), 
							platform7((7600, 8800), self.image_dict['platform']),
							platform7((9200, 9050), self.image_dict['platform']), 
							platform8((10300, 8700), self.image_dict['platform']),
							platform10((9600, 8350), self.image_dict['platform']),
							platform10((9100, 8000), self.image_dict['platform']),
							platform8((700, 8700), self.image_dict['platform']),
							platform7((1700, 8450), self.image_dict['platform']),
							platform7((3400, 8150), self.image_dict['platform']), 
							platform10((5150, 7950), self.image_dict['platform']),
							platform10((5800, 7750), self.image_dict['platform']),
							platform7((4950, 8400), self.image_dict['platform']), 
							platform7((6350, 8100), self.image_dict['platform']),
							platform7((7700, 7850), self.image_dict['platform']), 
							platform7((6350, 7500), self.image_dict['platform']),
							platform6((5000, 7200), self.image_dict['platform']), 
							platform7((3700, 6950), self.image_dict['platform']),
							platform7((2350, 7300), self.image_dict['platform']), 
							platform7((1000, 7000), self.image_dict['platform']),
							platform7((-400, 6700), self.image_dict['platform']), 
							#end lower area platforms
							#boss area platforms
							platform5((5400, 2300), self.image_dict['platform']),
							platform7((7800, 2650), self.image_dict['platform']),
							platform8((4650, 2700),	self.image_dict['platform']),
							platformI((7100, 1550), self.image_dict['platform']),
							platformI((6750, 1550), self.image_dict['platform']),
							platformI((7450, 1550), self.image_dict['platform']),
							platform8((8800, 2300), self.image_dict['platform']),
							platform6((9200, 1950), self.image_dict['platform']),
							platform10((9750, 1600), self.image_dict['platform']),
							platform8((9200, 1250), self.image_dict['platform']),
							platform9((9800, 900), self.image_dict['platform']),
							platform7((8400, 550), self.image_dict['platform']),
							platform8((7000, 700), self.image_dict['platform']),
							platform10((7700, 350), self.image_dict['platform']),
							platform10((6500, 300), self.image_dict['platform']),
							platform8((5500, 650), self.image_dict['platform']),
							platform10((4800, 1000), self.image_dict['platform']),
							platform7((4000, 1400), self.image_dict['platform']),
							platform8((4550, 2000), self.image_dict['platform']),
							platform10((5300, 1650), self.image_dict['platform']),
							#end boss area platforms
							#path to lower platforms
							platform7((3100, 3100), self.image_dict['platform']),#<-leading left
							platform10((4200, 3500), self.image_dict['platform']),
							platform6((4800, 3850), self.image_dict['platform']),
							platform8((5900, 4150), self.image_dict['platform']),
							platform10((6700, 4500), self.image_dict['platform']),
							platform5((6300, 4900), self.image_dict['platform']),
							platform7((5000, 5250), self.image_dict['platform']),
							platform6((4300, 5650), self.image_dict['platform']),
							platform8((5600, 6000), self.image_dict['platform']),
							platform10((3600, 5300), self.image_dict['platform']),
							platform10((4950, 6350), self.image_dict['platform']),
							platform8((4000, 6550), self.image_dict['platform']),
							platform8((8500, 4600), self.image_dict['platform']),
							platform7((9400, 4350), self.image_dict['platform']),
							platform10((10000, 4000), self.image_dict['platform']),
							platform8((9300, 3700), self.image_dict['platform']),
							platform10((10250, 3500), self.image_dict['platform']),
							platform10((9300, 5000), self.image_dict['platform']),
							#end path platforms
							#start of up-left platforms
							platform9((3000, 5000), self.image_dict['platform']),
							platform8((2000, 4600), self.image_dict['platform']),
							platform5((250, 5200), self.image_dict['platform']),
							platform6((500, 4200), self.image_dict['platform']),
							platform8((750, 3500), self.image_dict['platform']),
							platform10((250, 3100), self.image_dict['platform']),
							platform7((350, 2800), self.image_dict['platform']),
							platform10((20, 3800), self.image_dict['platform']),
							platform8((2000, 4600), self.image_dict['platform']) ]
		#list of enemies
		self.enemies = []
		self.MAX_ENEMIES = difficulty['enemy_ct']
		self.ENEMY_SPAWN_TIMER = 0
		self.initial_spawn_delay = 4500

		#difficulty dictionary
		self.difficulty = difficulty

		#list of power ups - type2 == sheild, type1 == heal
		self.power_ups=[	power_up((3060,8950), 2, self.image_dict['powerup']),
							power_up((920,8550), 1, self.image_dict['powerup']),
							power_up((4200, 6400), 1, self.image_dict['powerup']),
							power_up((100, 6550), 2, self.image_dict['powerup']),
							power_up((3670, 5150), 2, self.image_dict['powerup']),
							power_up((9410, 4850), 1, self.image_dict['powerup']),
							power_up((10350, 3350), 1, self.image_dict['powerup']),
							power_up((9310, 3550), 2, self.image_dict['powerup']),
							power_up((10650, 8550), 1, self.image_dict['powerup']),
							power_up((250, 5100), 1, self.image_dict['powerup']),
							power_up((350, 5100), 2, self.image_dict['powerup']),
							power_up((0, 3650), 1, self.image_dict['powerup']),
							power_up((1600, 2650), 1, self.image_dict['powerup']),
							power_up((1700, 2700), 2, self.image_dict['powerup'])]

		self.boss_powerups = [	power_up((9900, 1800), 2, self.image_dict['powerup']),
								power_up((7770, 200), 1, self.image_dict['powerup']),
								power_up((4100, 1250), 1, self.image_dict['powerup']),
								power_up((6600, 150), 2, self.image_dict['powerup'])	]

		for powerup in self.boss_powerups:
				if powerup not in self.power_ups:
					self.power_ups.append(powerup)

	def reset(self):
		#reset enemies
		self.enemies = []
		self.boss_area = boss_area(self.boss_area_pos, self.image_dict['boss'])
		if self.player.found_boss:
			spawn = self.difficulty['boss_spawn']
		else:
			spawn = self.difficulty['player_spawn']
		self.player.reset(spawn, (0,0))
		if not self.player.found_boss:
			self.initial_spawn_delay = 3500
		if self.difficulty['powerup_respawn']:
			if self.player.deaths > 15:
				for powerup in self.boss_powerups:
						if powerup not in self.power_ups:
							self.power_ups.append(powerup)

	def random_spawn(self):
		#enemy spawn positions
		pos = self.player.get_center()
		DIM = self.screen_size
		spawn_pos = []
		halfx = DIM[0]/2
		halfy = DIM[1]/2
		xstep = DIM[0]/8
		ystep = DIM[1]/4
		for x in xrange(0, 8):
			spawn_pos.append( (pos.x+(-halfx+x*xstep), pos.y-halfy-100) )
			spawn_pos.append( (pos.x+(-halfx+x*xstep), pos.y+halfy+100) )
		for y in xrange(0, 4):
			spawn_pos.append( (pos.x-halfx-100, pos.y+(-halfy+y*ystep)) )
			spawn_pos.append( (pos.x+halfx+100, pos.y+(-halfy+y*ystep)) )
		ran = randint(0,len(spawn_pos)-1)
		self.enemies.append( enemy(spawn_pos[ran], (0,0), self.image_dict['enemy'], self.difficulty))

	def update(self, time_dif, keys):
		#platforms in vicinity
		v_platforms = []
		#calculate screen rect around player
		bgsize = self.background.get_size()
		playerpos = self.player.get_center()
		screenpos = vector2(playerpos.x - self.screen_size[0]/2, playerpos.y - self.screen_size[1]/2)
		if screenpos.x + self.screen_size[0] >= bgsize[0]:
			screenpos.x = bgsize[0] - self.screen_size[0]
		elif screenpos.x <= 0:
			screenpos.x = 0
		if screenpos.y + self.screen_size[1] >= bgsize[1]:
			screenpos.y = bgsize[1] - self.screen_size[1]
		elif screenpos.y <= 0:
			screenpos.y = 0
		screenrect = pygame.Rect(screenpos.x, screenpos.y, self.screen_size[0], self.screen_size[1])

		#get list of platforms within screen rect
		for platform in self.platforms:
			if screenrect.colliderect(platform.get_rect()):
				v_platforms.append(platform)

		#update player
		self.player.update(time_dif, keys, v_platforms, self.boss_area)

		#if not enough enemies, spawn enemies on timer
		if self.initial_spawn_delay <= 0:
			if self.ENEMY_SPAWN_TIMER > self.difficulty['enemy_spawn_time']:
				if len(self.enemies) < self.MAX_ENEMIES:
					for x in xrange(randint(1,4)):
						self.random_spawn()
				self.ENEMY_SPAWN_TIMER = 0
			self.ENEMY_SPAWN_TIMER += time_dif
		else:
			self.initial_spawn_delay -= time_dif

		#update all enemies and check if attacking player
		for enemy in self.enemies:
			enemy.update(time_dif, self.player)
			if enemy.remove:
				self.enemies.remove(enemy)
			elif enemy.get_center().subtract(self.player.get_center()).magnitude() <= self.player.dim[1]/2:
				if self.player.immune==0:
					if not (enemy.killed or enemy.despawn):
						self.player.health -= self.difficulty['enemy_dmg']
						self.player.hurt_timer = 150
						enemy.despawn = True

		#deal with platform or power up collision and check if attacks hit enemies 
		self.player.handle_collision(time_dif,v_platforms,self.enemies,self.power_ups)
		
		#update power ups
		for powers in self.power_ups:
			if powers.destroy==1:
				self.power_ups.remove(powers)
			else: 
				powers.update(time_dif)

		#player dies, if going out of background bounds
		if self.player.pos.y >= bgsize[1]:
			self.player.fell = True
			self.player.health = 0

		#update boss area
		self.boss_area.update(time_dif, self.player)
		if(self.player.found_boss):
			self.MAX_ENEMIES = self.difficulty['enemy_ct_boss']
		else:
			self.MAX_ENEMIES = self.difficulty['enemy_ct']
		
	def draw(self, screen, window):

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
		self.screen_size = screen.get_size()
		screenrect = pygame.Rect(screenpos.x, screenpos.y, self.screen_size[0], self.screen_size[1])
		#screen.blit(self.background, (-screenpos.x, -screenpos.y))
		screen.blit(self.background, (0,0), area=screenrect)

		#draw boss area
		for part in self.boss_area.boss_part:
			if screenrect.colliderect(part.get_hitbox()):
				if part.event_trigger:
					part.draw_G(screenpos, part.img, screen)
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

		#scale down render screen to display screen and draw
		DIM = window.get_size()
		render_size = screen.get_size()
		if DIM is not render_size:
			scale_args = (screen, DIM)
			#scaled_surf = pygame.transform.scale(*scale_args)
			scaled_surf = pygame.transform.smoothscale(*scale_args)
			window.blit(scaled_surf, (0, 0))
		else:
			window.blit(screen, (0, 0))

		#draw damage splash
		if self.player.hurt_timer > 0:
			window.blit(self.player.hurt_ani, (0,0))

		print ("player pos", self.player.pos.x, self.player.pos.y)

		#for testing#
		mousepos = pygame.mouse.get_pos()
		ratio = screen.get_size()[0]/window.get_size()[0]
		showx = int(mousepos[0]*ratio) + screenpos.x
		showy = int(mousepos[1]*ratio) + screenpos.y
		showpos = (showx, showy)
		print showpos
