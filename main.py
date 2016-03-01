import sys
from player import *
from enemy import *
from health import *
from level import *

pygame.init()

DIM = [1600, 900]

screen = pygame.display.set_mode( (DIM[0], DIM[1]) )
pygame.display.set_caption( "Revenge of the Virus" )

start = pygame.image.load( "Assets/loading_screen.png" ).convert()
print(start.get_height() * start.get_width() *start.get_bytesize() / 1000000)
dead_screen = pygame.image.load( "Assets/dead_screen.png").convert()
print(dead_screen.get_height() * dead_screen.get_width() *dead_screen.get_bytesize() / 1000000)
controls = pygame.image.load( "Assets/controls.png" ).convert()
print(controls.get_height() * controls.get_width() *controls.get_bytesize() / 1000000)
background = pygame.image.load( "Assets/Game Background/Game Background w'out platforms update 3.png" ).convert()
print(background.get_height() * background.get_width() *background.get_bytesize() / 1000000)

#images needed
playerimg = pygame.image.load( "Assets/Character_Animation.png" ).convert_alpha()
platform_img = [	pygame.image.load("Assets/Platform covers/platform_5.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_6.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_7.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_8.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_9.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_10.png").convert_alpha()	]
powerup_img = [		pygame.image.load("Assets/Powerups/Shield.png").convert_alpha(),
					pygame.image.load("Assets/Powerups/health_up.png").convert_alpha()	]

#world and entities initialization
playerspawn = (300, 8850)
player_char = player(playerspawn, (0, 0), playerimg)
level1=Level(player_char, background, DIM, platform_img, powerup_img)
player_HUD = HUD(screen, player_char, "Assets/health_bar1.png", vector2(10,15), powerup_img)

#press any key to begin game
start_game = False
show_controls = True
while show_controls:

	while start_game is False:
		pygame.event.pump()
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				pygame.quit()
				sys.quit()
			elif evt.type == pygame.KEYDOWN:
				start_game = True
		screen.blit(start, (0,0))
		pygame.display.flip()

	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.quit()
		elif evt.type == pygame.KEYDOWN:
			show_controls = False
	screen.blit(controls, (0,0))
	pygame.display.flip()

old_time = pygame.time.get_ticks()

while True:

	#if player dies, reset
	if player_char.health <= 0:

		#wait for player input to restart
		dead = True
		while dead:
			pygame.event.pump()
			for evt in pygame.event.get():
				if evt.type == pygame.QUIT:
					pygame.quit()
					sys.quit()
				elif evt.type == pygame.KEYDOWN:
					dead = False
			screen.fill((0,0,0))
			screen.blit(dead_screen, (0,0))
			pygame.display.flip()

		#max health decreases as you die
		if player_char.max_health > player_char.full_health/2:
			player_char.max_health -= 5
		else:
			player_char.max_health = player_char.full_health/2
		player_char.reset(playerspawn, (0, 0))

		#reset enemies
		for enemy in level1.enemies:
			level1.enemies.remove(enemy)

		old_time = pygame.time.get_ticks()

	# get user events
	space_pressed = False

	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN:
			if evt.key == pygame.K_SPACE:
				space_pressed = True
		elif evt.type == pygame.KEYUP:
			if evt.key == pygame.K_a and player_char.velocity.x < 0:
				player_char.velocity.x = 0
			elif evt.key == pygame.K_d and player_char.velocity.x > 0:
				player_char.velocity.x = 0

	keys = [pygame.key.get_pressed(), space_pressed]

	# do simulation stuff
	# deal with time
	
	new_time = pygame.time.get_ticks()
	time_difference = new_time - old_time
	old_time = new_time

	# update player, enemies, level
	level1.update(time_difference, keys)

	# draw to screen and flip
	level1.draw(screen)

	# HUD stuff
	player_HUD.update_display(time_difference)
	player_HUD.display()
	
	pygame.display.flip()