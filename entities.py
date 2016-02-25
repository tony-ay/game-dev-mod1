from utils import *
#working on restructuring sprite, player, and enemy classes

#main character class
class player(sprite1):
	def __init__(self, init_pos, init_velocity, init_image):
		#image width and height for a sections of bigger image
		self.IMG_H=150
		self.IMG_W=263
		sprite1.__init__(self, init_pos, init_velocity, init_image, (self.IMG_W, self.IMG_H))
		#player attributes
		#health at full capacity
		self.full_health = 100
		#current max health available
		self.max_health = self.full_health
		#current health
		self.health = self.max_health
		self.shield = 0
		#animation variables
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
	def draw(self,surface):
		clip = pygame.Rect(self.IMG_W*self.frame, 0, self.IMG_W, self.IMG_H )
		sprite1.draw_G(self, surface, clip)

	#update player character
	def update(self, time_diff, keys, platform_list):
		#get direction from user input(change in velocity for x)
		change = vector2(0,0)
		if keys[0][pygame.K_a]:
			change.x += -1
			self.time_since_last_frame+=time_diff
			if self.time_between_frames<=self.time_since_last_frame:
				self.frame=(self.frame+1)%self.frame_ct
				self.time_since_last_frame=0
		if keys[0][pygame.K_d]:
			change.x += 1
			self.time_since_last_frame+=time_diff
			if self.time_between_frames<=self.time_since_last_frame:
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
		sprite1.update_vel(self, time_diff)

		#handle platform collision
		self.pos.x = self.pos.x + (self.velocity.x * time_diff)
		hitbox = sprite1.get_hitbox(self)
		for obj in platform_list:
			if hitbox.colliderect(obj):
				if self.velocity.x > 0:
					self.pos.x = obj.pos.x - self.dim[0]
				elif self.velocity.x < 0:
					self.pos.x = obj.pos.x + obj.width

		self.pos.y = self.pos.y + (self.velocity.y * time_diff)
		hitbox = sprite1.get_hitbox(self)
		for obj in platform_list:
			if hitbox.colliderect(obj):
				if self.velocity.y > 0:
					self.pos.y = obj.pos.y - self.dim[1]
				elif self.velocity.y < 0:
					self.pos.y = obj.pos.y + obj.height
				self.velocity.y = 0

#basic class for enemies
#class enemy(sprite1):