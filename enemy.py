from utils import *

#enemy class
class enemy(sprite):
	def __init__(self, pos, vel, image):
		sprite.__init__(self, pos, vel, image, (40, 56))

		#enemy attributes
		self.life_timer = 4500

		#frame variables
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

		self.life_timer -= time_diff

	def draw(self, surface, screenpos):
		clip = pygame.Rect(self.dim[0] * self.frame, 0, self.dim[0], self.dim[1] )
		sprite.draw_G(self, screenpos, self.img, surface, clip)