from utils import *

class boss_part(sprite):
	def __init__(self, pos, img):
		sprite.__init__(self, pos, (0,0), img)
		self.destination = self.pos
		self.event_trigger = False
		self.event_done = False
		self.started = False

	def start_event(self, dest):
		if not self.event_trigger:
			self.event_trigger = True
			self.started = True
			self.destination = dest

	def update(self, time_diff):
		if self.event_trigger and not self.event_done:
			self.velocity = self.destination.subtract(self.pos).normalized().scale(0.15)
			self.update_pos(time_diff)
			hrange = 10
			if self.pos.y < self.destination.y+hrange and self.pos.y > self.destination.y-hrange:
				if self.pos.x < self.destination.x+hrange and self.pos.x > self.destination.y-hrange:
					self.finish()
		if self.pos.equals(self.destination):
			self.event_done = True

	#for testing purposes
	def finish(self):
		self.pos = self.destination

	def draw(self, screen, screenpos):
		sprite.draw_G(self, screenpos, self.img, screen)

#main class to handle boss area
class boss_area:
	def __init__(self, pos, img):
		# moving sound
		self.sound = pygame.mixer.Sound("Assets/Sounds/boss_move.wav")
		self.pos = vector2(pos[0], pos[1])
		#images needed
		mainimg = img[0]
		part1 = img[1]
		part2 = img[2]
		part3 = img[3]
		part4 = img[4]
		#parts to boss area
		self.boss_part = [	boss_part(pos, part4), 
							boss_part(pos, part3),
							boss_part(pos, part2), 
							boss_part(pos, part1),
							boss_part(pos, mainimg)	]
		self.boss_part[4].event_trigger = True
		#area to begin triggers
		self.main_dim = mainimg.get_size()
		self.area_rect = pygame.Rect(self.pos.x-50, self.pos.y-500, self.main_dim[0]+100, 1000)

		#timer variables
		self.time_between = 10000
		self.timer_started = False
		self.timer = 0

	def start_timer(self):
		self.timer = self.time_between
		self.timer_started = True

	def update(self, time_diff, player):
		dest1 = self.pos.add(vector2(2000,-1000))
		dest2 = self.pos.add(vector2(1700,-1850))
		dest3 = self.pos.add(vector2(1020,-1400))
		dest4 = self.pos.add(vector2(850,-1550))

		if self.timer > 0:
			self.timer-=time_diff
			player.boss_moving = False
		else:
			self.timer_started = False
			player.boss_moving = True

		if not self.boss_part[3].started:
			if self.area_rect.colliderect(player.get_hitbox()):
				player.found_boss = True
				self.boss_part[3].pos = self.pos.add(vector2(500, 100))
				self.boss_part[3].start_event(dest1)
				self.sound.play()

		if self.boss_part[3].event_trigger:
			if self.boss_part[3].event_done:
				if not self.boss_part[2].started:
					if not self.boss_part[2].event_done:
						if not self.timer_started:
							self.start_timer()
					if self.timer <= 0:
						self.boss_part[2].pos = self.boss_part[3].destination.add(vector2(200, 200))
						self.boss_part[2].start_event(dest2)
						self.sound.play()
			else:
				self.boss_part[3].update(time_diff)

		if self.boss_part[2].event_trigger:
			if self.boss_part[2].event_done:
				if not self.boss_part[1].started:
					if not self.boss_part[1].event_done:
						if not self.timer_started:
							self.start_timer()
					if self.timer <= 0:
						self.boss_part[1].pos = self.boss_part[2].destination.add(vector2(80, 100))
						self.boss_part[1].start_event(dest3)
						self.sound.play()
			else:
				self.boss_part[2].update(time_diff)

		if self.boss_part[1].event_trigger:
			if self.boss_part[1].event_done:
				if not self.boss_part[0].started:
					if not self.boss_part[0].event_done:
						if not self.timer_started:
							self.start_timer()
					if self.timer <= 0:
						self.boss_part[0].pos = self.boss_part[1].destination.add(vector2(80,100))
						self.boss_part[0].start_event(dest4)
						self.sound.play()
			else:
				self.boss_part[1].update(time_diff)

		if self.boss_part[0].event_trigger:
			if self.boss_part[0].event_done:
				#game ends
				player.health = 0
				#ask player to restart
				player.failed = True
			else:
				self.boss_part[0].update(time_diff)
