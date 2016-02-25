from utils import *

#enemy class
class enemy(sprite):
	def __init__(self, pos, vel, image):
		sprite.__init__(self, pos, vel, image)

		#enemy attributes
		self.life_timer = 2000

		#frame variables
		self.img_w = 40
		self.img_h = 56
		self.frame = 0
		self.last_frame_time = 0
		self.time_delay = 100
		self.frame_ct = 3

	#update enemy position
	def update(self, time_diff, player):
		#get vector from enemy to player
		direction = player.get_center().subtract(self.get_center())
		if direction.magnitude() > 300:
			#home in on player if too far
			self.accel = direction.normalized().scale(0.008)

		sprite.update_vel(self, time_diff)
		self.velocity = self.velocity.normalized().scale(0.5)
		sprite.update_pos(self, time_diff)

		self.last_frame_time += time_diff
		if self.time_delay <= self.last_frame_time:
			self.frame=(self.frame+1)%self.frame_ct
			self.last_frame_time=0

		self.life_timer -= 1

	def draw(self, surface):
		clip = pygame.Rect(self.img_w * self.frame, 0, self.img_w, self.img_h )
		sprite.draw_G(self, self.img, surface, clip)