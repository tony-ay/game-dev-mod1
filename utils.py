import pygame
import math

#2d vector class
class vector2:
	# constructor
	def __init__(self, x, y):
		self.x = x
		self.y = y

	# overload return-this-as-string for printing
	def __str__(self):
		# format allows you to replace "{}" with variable values
		return "({}, {})".format(self.x, self.y)

	# other methods here...

	def add(self, vec):
		return vector2(self.x + vec.x, self.y + vec.y)

	def subtract(self, vec):
		return vector2(self.x - vec.x, self.y - vec.y)

	def scale(self, value):
		return vector2(self.x * value, self.y * value)

	def magnitude(self):
		return math.sqrt(self.x*self.x + self.y*self.y)

	def normalized(self):
		if self.magnitude() == 0:
			return vector2(0,0)
		else:
			return vector2(self.x/self.magnitude(), self.y/self.magnitude())

#simple sprite class
class sprite:
	def __init__(self, init_pos, init_velocity, init_image=None, init_dim=None):
		#positional attributes
		self.pos = vector2(init_pos[0], init_pos[1])
		self.velocity = vector2(init_velocity[0], init_velocity[1]).normalized()
		self.accel = vector2(0,0)

		#graphic attributes
		if init_image is not None:
			self.img = pygame.image.load( init_image ).convert_alpha()
		else:
			self.img = Surface((25, 25))
		#for dim we now use the first section of the image as width and height
		#that does mean that the hitbox will only be the hitbox for the
		#first section of the image
		#so if it seems you should be hitting anything but you are that why
		if init_dim is not None:
			self.dim = (init_dim[0], init_dim[1])
		else:
			self.dim = self.img.get_size()

	#get center point of sprite
	def get_center(self):
		return vector2(self.pos.x + self.dim[0]/2, self.pos.y + self.dim[1]/2)

	#returns a Rect the same size and position as the sprite image
	def get_hitbox(self):
		return pygame.Rect(self.pos.x, self.pos.y, self.dim[0], self.dim[1])
        def get_rect(self,left,top,width,height):
                return pygame.Rect(left, top, width, height)
	#update velocity of the sprite
	def update_vel(self, time_diff):
		self.velocity = self.velocity.add( self.accel.scale( time_diff ) )
	#update position of the sprite
	def update_pos(self, time_diff):
		self.pos = self.pos.add( self.velocity.scale( time_diff ) )

	#draw sprite to the screen
	def draw_G(self, img, surface, clip=None):
		surface.blit(img, ( int(self.pos.x), int(self.pos.y) ), area=clip)
