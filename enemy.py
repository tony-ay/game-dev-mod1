from ani_vars import *

#enemy class
class enemy(sprite):
	def __init__(self, pos, vel, image, difficulty):
		sprite.__init__(self, pos, vel, image[0], (40, 56))

		#enemy attributes
		self.life_timer = difficulty['enemy_life_time']

		#frame variables
		self.frame = 0
		self.last_frame_time = 0
		self.time_delay = 200
		self.frame_ct = 3
		self.kill_ani = image[1]
		self.despawn_ani = image[2]
		self.kill_ani_var = ani_var(3, 36, 70, 200)
		self.despawn_ani_var = ani_var(3, 70, 82, 75)

		self.despawn = False
		self.killed = False

		self.remove = False

	#update enemy position
	def update(self, time_diff, player):
		if self.despawn:
			self.despawn_ani_var.update(time_diff)
			if self.despawn_ani_var.time_between_frames <= self.despawn_ani_var.time_since_last_frame:
				self.despawn_ani_var.frame=(self.despawn_ani_var.frame+1)%self.despawn_ani_var.frame_ct
				self.despawn_ani_var.time_since_last_frame = 0
				if self.despawn_ani_var.frame == 0:
					self.remove = True
		elif self.killed:
			self.kill_ani_var.update(time_diff)
			if self.kill_ani_var.time_between_frames <= self.kill_ani_var.time_since_last_frame:
				self.kill_ani_var.frame=(self.kill_ani_var.frame+1)%self.kill_ani_var.frame_ct
				self.kill_ani_var.time_since_last_frame = 0
				if self.kill_ani_var.frame == 0:
					self.remove = True
		else:
			#handle frames
			self.last_frame_time += time_diff
			if self.time_delay <= self.last_frame_time:
				self.frame=(self.frame+1)%self.frame_ct
				self.last_frame_time=0

			self.life_timer -= time_diff
			if self.life_timer <= 0:
				self.despawn = True

			#get vector from enemy to player
			direction = player.get_center().subtract(self.get_center())
			if direction.magnitude() > 300:
				#home in on player if too far
				self.accel = direction.normalized().scale(0.008)

		sprite.update_vel(self, time_diff)
		self.velocity = self.velocity.normalized().scale(0.5)
		sprite.update_pos(self, time_diff)

	def draw(self, surface, screenpos):
		if not self.remove:
			if self.despawn:
				w = self.despawn_ani_var.img_W
				h = self.despawn_ani_var.img_H
				frame = self.despawn_ani_var.frame
				img = self.despawn_ani
			elif self.killed:
				w = self.kill_ani_var.img_W
				h = self.kill_ani_var.img_H
				frame = self.kill_ani_var.frame
				img = self.kill_ani
			else:
				w = self.dim[0]
				h = self.dim[1]
				frame = self.frame
				img = self.img
			offset = vector2(self.dim[0]-w, self.dim[1]-h)
			clip = pygame.Rect(w * frame, 0, w, h)
			sprite.draw_G_o(self, screenpos, img, surface, offset, clip)
