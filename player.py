from utils import *
from attacks import *
#working on restructuring sprite, player, and enemy classes

#main character class
class player(sprite):
	def __init__(self, init_pos, init_velocity, init_image,spin_attack):
		#image width and height for a sections of bigger image
		self.IMG_H=150
		self.IMG_W=263
		sprite.__init__(self, init_pos, init_velocity, init_image, (self.IMG_W, self.IMG_H))
		self.spin_attack = pygame.image.load( spin_attack ).convert_alpha()
		#player attributes
		#health at full capacity
		self.full_health = 100
		#current max health available
		self.max_health = self.full_health
		#current health
		self.health = self.max_health
		self.shield = 0

		#animation variables
		self.middle_attack = middle_attack()
		self.top_attack=up_attack()
		self.bottom_attack=down_attack()
		#variable to check shich direction image is
		self.right=True
		self.frame=0
		self.time_since_last_frame=0
		self.time_between_frames=100
		self.frame_ct=4

	#used to reset player
	def reset(self, new_pos, new_vel):
		self.pos = vector2(new_pos[0], new_pos[1])
		self.velocity = vector2(new_vel[0], new_vel[1])
		self.health = self.max_health
		self.shield = 0

	#health functions
	def increase_health(self, amount):
		self.health += amount
		if self.health > self.max_health:
			self.health = self.max_health
		
	def decrease_health(self, amount):
		self.health -= amount
		if self.health < 0:
			self.health = 0
			
	def is_dead(self):
		return self.health == 0
		
	def is_full_health(self):
		return self.health >= self.max_health
		
	def full_health(self):
		self.health = self.max_health
		
	def zero_health(self):
		self.health = 0

	#separate draw function
	def draw(self, surface):
		#img=None
		#clip=None
		#pdb.set_trace()
		if self.middle_attack.attacking==True:
			clip = pygame.Rect(self.middle_attack.img_W*self.middle_attack.frame, 0, self.middle_attack.img_W, self.middle_attack.img_H )
			img = self.spin_attack
		else:
			clip = pygame.Rect(self.IMG_W*self.frame, 0, self.IMG_W, self.IMG_H )
			if self.velocity.x<0 and self.right==True:
					self.img=pygame.transform.flip(self.img,True,False)
					self.right=False
			elif self.velocity.x>0 and self.right==False:
					self.img=pygame.transform.flip(self.img,True,False)
					self.right=True
			img=self.img
		sprite.draw_G(self, img, surface, clip)

	#update player character
	def update(self, time_diff, keys, platform_list):
		#get direction from user input(change in velocity for x)
		change = vector2(0,0)
		self.middle_attack.update(time_diff)
		self.top_attack.update(time_diff)
		self.bottom_attack.update(time_diff)
		
		if keys[0][pygame.K_LEFT] or keys[0][pygame.K_RIGHT]or self.middle_attack.attacking==True:
			if self.top_attack.attacking==False and self.bottom_attack.attacking==False:
				self.middle_attack.attack()
		if keys[0][pygame.K_UP] or self.top_attack.attacking==True:
			if self.middle_attack.attacking==False and self.bottom_attack.attacking==False:
				self.top_attack.attack()
		if keys[0][pygame.K_DOWN] or self.bottom_attack.attacking==True:
			if self.top_attack.attacking==False and self.middle_attack.attacking==False:
				self.bottom_attack.attack()

		#here we make the variable attacking true if any attacks are true
		attacking=False
		if self.middle_attack.attacking==True or self.top_attack.attacking==True or self.bottom_attack.attacking==True:
			attacking=True
		if keys[0][pygame.K_a] :
			change.x += -1
			self.time_since_last_frame+=time_diff
			if self.time_between_frames<=self.time_since_last_frame and not(attacking):
				self.frame=(self.frame+1)%self.frame_ct
				self.time_since_last_frame=0
		elif keys[0][pygame.K_d] :
			change.x += 1
			self.time_since_last_frame+=time_diff
			if self.time_between_frames<=self.time_since_last_frame and not(attacking):
				self.frame=(self.frame+1)%self.frame_ct
				self.time_since_last_frame=0
		self.velocity.x = change.x

		on_platform = False
		
		#loop through platform list to check if the player is on a platform
		for obj in platform_list:
			#check if player is on platform
			if (self.pos.x+self.dim[0] > obj.pos.x) and (self.pos.x < obj.pos.x+obj.width):
				if (self.pos.y+self.dim[1]) > (obj.pos.y-1) and (self.pos.y+self.dim[1]) < (obj.pos.y+1):
					on_platform = True
					break
		
		#apply gravity where appropriate
		if on_platform:
			#jump if pressed
			if keys[1]:
				self.velocity.y = -1.5
			self.accel = vector2(0, 0)
		else:
			self.accel = vector2(0, 0.004)
		sprite.update_vel(self, time_diff)

	def handle_collision(self,time_diff, platform_list,enemies):
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
						enemies.remove(enemy)
			if self.top_attack.attacking==True:
				for enemy in enemies:
					if enemy.get_hitbox().colliderect(top_hitbox):
						enemies.remove(enemy)
			if self.bottom_attack.attacking==True:
				for enemy in enemies:
					if enemy.get_hitbox().colliderect(bottom_hitbox):
						enemies.remove(enemy)
