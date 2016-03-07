from utils import *
from attacks import *
#working on restructuring sprite, player, and enemy classes

#main character class
class player(sprite):
	def __init__(self, init_velocity, image_dict, sounds, difficulty):
		sprite.__init__(self, difficulty['player_spawn'], init_velocity, image_dict['walk'], (263, 150))
		#attack image sets
		self.spin_attack = image_dict['spin']
		#print(self.spin_attack.get_height() * self.spin_attack.get_width() *self.spin_attack.get_bytesize())
		self.up_attack_ani = image_dict['up']
		#print(self.up_attack_ani.get_height() * self.up_attack_ani.get_width() *self.up_attack_ani.get_bytesize())
		self.down_attack_ani = image_dict['down']
		#print(self.down_attack_ani.get_height() *self.down_attack_ani.get_width() *self.down_attack_ani.get_bytesize())
		self.injection_ani= image_dict['injection']
		self.shield_ani= image_dict['shield']
		self.hurt_ani = image_dict['hurt']
		self.hurt_timer = 0
		#print(self.shield_ani.get_height() * self.shield_ani.get_width() *self.shield_ani.get_bytesize())
		#player attributes
		self.difficulty = difficulty
		self.sounds = sounds
		#health at full capacity
		self.full_health = difficulty['player_health']
		#current max health available
		self.max_health = self.full_health
		#current health
		self.deaths = 0
		self.health = self.max_health
		self.healths = 0
		self.shields = 0
		self.immune=0
		self.shield=shield()
		#jump image and boolean
		self.jump_ani = image_dict['jump']
		self.jump=jump()
		#animation variables
		self.middle_attack = middle_attack()
		self.top_attack=up_attack()
		self.bottom_attack=down_attack()
		self.injection=injection()
		#variable to check shich direction image is
		self.right=True
		#image width and height for a sections of bigger image
		self.frame=0
		self.time_since_last_frame=0
		self.time_between_frames=100
		self.frame_ct=4

		self.enemies_killed = 0
		self.fell = False
		#boss area variables
		self.boss_moving = False
		self.found_boss = False
		self.can_inject = False
		self.num_injects = 0
		self.won = False
		self.failed = False

	#used to reset player
	def reset(self, new_pos, new_vel):
		self.deaths += 1
		self.enemies_killed = 0
		self.pos = vector2(new_pos[0], new_pos[1])
		self.velocity = vector2(new_vel[0], new_vel[1])
		self.health = self.max_health
		self.middle_attack.reset()
		self.top_attack.reset()
		self.bottom_attack.reset()
		self.shield.reset()
		self.num_injects = 0

	#separate draw function
	def draw(self, surface, screenpos):
		img=None
		clip=None
		#pdb.set_trace()
		if self.velocity.x<0 and self.right==True:
			self.right=False
		elif self.velocity.x>0 and self.right==False:
			self.right=True
		if self.immune==1:
			clip = pygame.Rect(self.shield.img_W*self.shield.frame, 0, self.shield.img_W, self.shield.img_H )
			img = self.shield_ani
			sprite.draw_G_offset(self, screenpos, img, surface,50, clip)
		if self.middle_attack.attacking==True:
			clip = pygame.Rect(self.middle_attack.img_W*self.middle_attack.frame, 0, self.middle_attack.img_W, self.middle_attack.img_H )
			img = self.spin_attack
			sprite.draw_G(self, screenpos, img, surface, clip)
		elif self.top_attack.attacking==True:
			clip = pygame.Rect(self.top_attack.img_W*self.top_attack.frame, 0, self.top_attack.img_W, self.top_attack.img_H )
			img = self.up_attack_ani
			sprite.draw_G_offset(self, screenpos, img, surface, 100,clip)
		elif self.bottom_attack.attacking==True:
			clip = pygame.Rect(self.bottom_attack.img_W*self.bottom_attack.frame, 0, self.bottom_attack.img_W, self.bottom_attack.img_H )
			img = self.down_attack_ani
			sprite.draw_G(self, screenpos, img, surface, clip)
		elif self.jump.jumping==True:
			if self.right == True:
				img = self.jump_ani
			else:
				img = pygame.transform.flip(self.jump_ani,True,False)
			clip=pygame.Rect(self.jump.img_W*self.jump.frame,0,self.jump.img_W,self.jump.img_H)
			sprite.draw_G(self, screenpos, img, surface, clip)
		elif self.injection.attacking ==True:
			clip = pygame.Rect(self.injection.img_W*self.injection.frame, 0, self.injection.img_W, self.injection.img_H )
			img = self.injection_ani
			sprite.draw_G_offset(self, screenpos, img, surface,80, clip)
		else:
			clip = pygame.Rect(self.dim[0]*self.frame, 0, self.dim[0], self.dim[1] )
			if self.right == True:
				img = self.img
			else:
				img = pygame.transform.flip(self.img,True,False)
			#print(self.jump.frame)
			sprite.draw_G(self, screenpos, img, surface, clip)
		
	#update player character
	def update(self, time_diff, keys, platform_list, boss_area):
		#get direction from user input(change in velocity for x)
		change = vector2(0,0)

		on_platform = False
		on_inject_platform = False
		#loop through platform list to check if the player is on a platform
		for obj in platform_list:
			#check if player is on platform
			if (self.pos.x+self.dim[0] > obj.pos.x) and (self.pos.x < obj.pos.x+obj.width):
				if (self.pos.y+self.dim[1]) > (obj.pos.y-1) and (self.pos.y+self.dim[1]) < (obj.pos.y+1):
					on_platform = True
					if obj.inject:
						if obj.inj_rect.colliderect(sprite.get_hitbox(self)):
							on_inject_platform = True
					break
		if on_inject_platform:
			self.can_inject = True
		else:
			self.can_inject = False

		self.middle_attack.update(time_diff)
		self.top_attack.update(time_diff)
		self.bottom_attack.update(time_diff)
		self.jump.update(time_diff)
		self.shield.update(time_diff)
		self.injection.update(time_diff)

		if keys[0][pygame.K_LEFT] or keys[0][pygame.K_RIGHT]or self.middle_attack.attacking==True:
			if self.top_attack.attacking==False and self.bottom_attack.attacking==False:
				self.middle_attack.attack()
		if keys[0][pygame.K_UP] or self.top_attack.attacking==True:
			if self.middle_attack.attacking==False and self.bottom_attack.attacking==False:
				self.top_attack.attack()
		if keys[0][pygame.K_DOWN] or self.bottom_attack.attacking==True:
			if self.top_attack.attacking==False and self.middle_attack.attacking==False and on_platform == False:
				self.bottom_attack.attack()
		if  keys[0][pygame.K_s] or self.injection.attacking==True:
			if not self.jump.jumping and on_platform and self.top_attack.attacking==False and self.bottom_attack.attacking==False and self.middle_attack.attacking==False:
				if self.can_inject and self.boss_moving:
					if self.injection.attack():
						self.num_injects += 1
						self.injection.reset()
						if self.num_injects >= self.difficulty['num_injects']:
							self.won = True

		if keys[0][pygame.K_q] and self.healths>0:
			self.healths-=1
			self.sounds['health'].play()
			if self.max_health < self.full_health-self.difficulty['heal_amount']:
				self.max_health+=self.difficulty['heal_amount']
				self.health=self.max_health
			else:
				self.max_health=self.full_health
				self.health=self.max_health
		if (keys[0][pygame.K_e] and self.shields>0) or self.immune==1:
			if self.immune==0:
				self.shields-=1
			self.immune=1
			self.shield.use()
			if self.shield.frame==0 and self.shield.amount==self.difficulty['shield_amount']:
				self.immune=0
				self.shield.amount=0
				self.shield.shield_sound.stop()
		#here we make the variable attacking true if any attacks are true
		attacking=False
		if self.middle_attack.attacking==True or self.top_attack.attacking==True or self.bottom_attack.attacking==True:
			attacking=True
		if keys[0][pygame.K_a] :
			change.x += -1
			self.time_since_last_frame+=time_diff
			if self.time_between_frames<=self.time_since_last_frame and not(attacking):
				self.sounds['step'].play()
				self.frame=(self.frame+1)%self.frame_ct
				self.time_since_last_frame=0
		if keys[0][pygame.K_d] :
			change.x += 1
			self.time_since_last_frame+=time_diff
			if self.time_between_frames<=self.time_since_last_frame and not(attacking):
				self.frame=(self.frame+1)%self.frame_ct
				self.time_since_last_frame=0
				self.sounds['step'].play()
		self.velocity.x = change.x

		self.jump.jumping=False
		#apply gravity where appropriate
		if on_platform:
			#jump if pressed
			self.bottom_attack.reset()
			if keys[1]:
				self.sounds['jump'].play()
				self.velocity.y = -1.8
			self.accel.y = 0
		else:
			self.accel.y = 0.004
			self.jump.jumping = True

		if self.jump.jumping or not self.boss_moving:
			if self.injection.frame is not 0:
				self.injection.reset()

		sprite.update_vel(self, time_diff)
		if self.jump.jumping:
			self.jump.jump()

		#damage splash timer
		if self.hurt_timer > 0:
			self.hurt_timer -= time_diff

	def handle_collision(self,time_diff, platform_list,enemies,power_ups):
		#handle platform collision
		self.pos.x = self.pos.x + (self.velocity.x * time_diff)
		hitbox = sprite.get_hitbox(self)
		for obj in platform_list:
			if hitbox.colliderect(obj):
				if self.velocity.x > 0 :
					self.pos.x =obj.pos.x - self.dim[0]
				if self.velocity.x < 0:
					self.pos.x = obj.pos.x + obj.width

		self.pos.y = self.pos.y + (self.velocity.y * time_diff)
		hitbox = sprite.get_hitbox(self)
		for obj in platform_list:
			if hitbox.colliderect(obj):
				if self.velocity.y > 0:
					self.pos.y = obj.pos.y - self.dim[1]
				elif self.velocity.y < 0:
					self.pos.y = obj.pos.y + obj.height
				self.velocity.y = 0

		#handle enemy collision
		if self.middle_attack.attacking==True or self.top_attack.attacking==True or self.bottom_attack.attacking==True:
			hitbox=sprite.get_hitbox(self)
			top_hitbox=sprite.get_rect(self,hitbox.left-50,hitbox.top-100,hitbox.width+100,hitbox.height-50)
			middle_hitbox=sprite.get_rect(self,hitbox.left-25,hitbox.top,hitbox.width+25,hitbox.height)
			bottom_hitbox=sprite.get_rect(self,hitbox.left-50,hitbox.top+150,hitbox.width+100,hitbox.height-50)
			if self.middle_attack.attacking==True:
				for enemy in enemies:
					if enemy.get_hitbox().colliderect(middle_hitbox):
						if not (enemy.despawn or enemy.killed):
							enemy.killed = True
							self.enemies_killed += 1
			if self.top_attack.attacking==True:
				for enemy in enemies:
					if enemy.get_hitbox().colliderect(top_hitbox):
						if not (enemy.despawn or enemy.killed):
							enemy.killed = True
							self.enemies_killed += 1
			if self.bottom_attack.attacking==True:
				for enemy in enemies:
					if enemy.get_hitbox().colliderect(bottom_hitbox):
						if not (enemy.despawn or enemy.killed):
							enemy.killed = True
							self.enemies_killed += 1
		#handle power_up collision
		for power in power_ups:
			if hitbox.colliderect(power.rect):
				power.destroy=1
				self.sounds['powerup'].play()
				if power.power_up_type==2:
					self.shields+=1
				else:
					self.healths+=1