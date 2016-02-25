import sys
from player import *
from enemy import *
from health import *
from level import *

pygame.init()

DIM = [1024, 768]

screen = pygame.display.set_mode( (DIM[0], DIM[1]) )
pygame.display.set_caption( "Revenge of the Virus" )

background = pygame.image.load( "Assets/Game Background preview2.png" ).convert()

platforms = [	Platform((300, 670), 1000, 100), Platform((1700, 610), 300, 200),
				Platform((1255, 330), 100,10), Platform((2350, 430), 550, 20), 
				Platform((1333, 150), 300, 20)	]

player_char = player((300,100), (0, 0), "Assets/Character_Animation.png","Assets/Animation_side_attack.png")

level1=Level(player_char, platforms, background, DIM)

health = HealthBar(screen, player_char, "Assets/health_bar1.png", vector2(10,15))

old_time = pygame.time.get_ticks()

MAX_ENEMIES = 10
ENEMY_SPAWN_TIMER = 0

while True:

	#if player dies, reset
	if player_char.health <= 0:
		old_time = pygame.time.get_ticks()
		platforms =	[	Platform((300, 670), 1000, 100), Platform((1700, 610), 300, 200),
						Platform((1255, 330), 100, 10), Platform((2350, 430), 550, 20), 
						Platform((1333, 150), 300, 20)	]

		#max health decreases as you die
		if player_char.max_health > player_char.full_health/2:
			player_char.max_health -= 5
		else:
			player_char.max_health = player_char.full_health/2
		player_char.reset((300, 100), (0, 0))

		level1 = Level(player_char, platforms, background, DIM)

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
	

	#if not enough enemies, spawn enemies on timer
	if ENEMY_SPAWN_TIMER > 300:
		if len(level1.enemies) < MAX_ENEMIES:
			level1.random_spawn(randint(2,5))
		ENEMY_SPAWN_TIMER = 0
	ENEMY_SPAWN_TIMER += 1

	# update player, enemies, level
	player_char.update(time_difference, keys, level1.platforms)
	level1.update(time_difference)

	# draw to screen and flip
	screen.fill( (181,109,109) )
	level1.draw(screen)

	# health stuff
	health.display()
	
	pygame.display.flip()