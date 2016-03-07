import sys
from player import *
from enemy import *
from health import *
from level import *
pygame.mixer.pre_init( 44100, -16, 2 )
pygame.init()

#render/display dimensions
tester = [7680, 4320]
res2160 = [3840, 2160]
res1440	= [2560, 1440]
res1080 = [1920, 1080]
res900	= [1600, 900]
res768	= [1366, 768]
res720	= [1280, 720]

#display resolution
DIM = res1080

#render resolution
render_size = res1440

#fullscreen check
fullscreen_check = True

#music flag
music_on = True

screen = pygame.display.set_mode( (DIM[0], DIM[1]) )
pygame.display.set_caption( "Revenge of the Virus" )
if fullscreen_check:
	pygame.display.set_mode(DIM, pygame.FULLSCREEN)

#background = pygame.Surface((11000,11000))
background = pygame.image.load( "Assets/Game Background/Background_Final.png" ).convert()

start = pygame.image.load( "Assets/Start Screen 2.png" ).convert()
dead_screen = [	pygame.image.load( "Assets/death_screen1.png").convert(),
				pygame.image.load( "Assets/death_screen2.png").convert(),
				pygame.image.load( "Assets/death_screen3.png").convert()	]
controls = pygame.image.load( "Assets/Instructions Screen.png" ).convert()
instruction = pygame.image.load( "Assets/Instructions Screen2.png" ).convert()
you_win = pygame.image.load( "Assets/you_win.png").convert()
credits = pygame.image.load( "Assets/credits_screen.png").convert()
hurt = pygame.image.load( "Assets/bloodshot_green.png").convert_alpha()
transparent = pygame.image.load("Assets/transparent.png").convert_alpha()

intro = [	pygame.image.load("Assets/Intro/frame_1.png").convert(),
			pygame.image.load("Assets/Intro/frame_2.png").convert(),
			pygame.image.load("Assets/Intro/frame_3.png").convert(),
			pygame.image.load("Assets/Intro/frame_4.png").convert(),
			pygame.image.load("Assets/Intro/frame_5.png").convert(),
			pygame.image.load("Assets/Intro/frame_6.png").convert(),
			pygame.image.load("Assets/Intro/frame_7.png").convert(),
			pygame.image.load("Assets/Intro/frame_8.png").convert(),
			pygame.image.load("Assets/Intro/frame_9.png").convert(),
			pygame.image.load("Assets/Intro/frame_10.png").convert(),
			pygame.image.load("Assets/Intro/frame_11.png").convert(),
			pygame.image.load("Assets/Intro/frame_12.png").convert(),	]

#scale appropriately
if DIM is not res1080:
	start = pygame.transform.smoothscale(start, DIM)
	dead_screen[0] = pygame.transform.smoothscale(dead_screen[0], DIM)
	dead_screen[1] = pygame.transform.smoothscale(dead_screen[1], DIM)
	dead_screen[2] = pygame.transform.smoothscale(dead_screen[2], DIM)
	controls = pygame.transform.smoothscale(controls, DIM)
	instruction = pygame.transform.smoothscale(instruction, DIM)
	you_win = pygame.transform.smoothscale(you_win, DIM)
	hurt = pygame.transform.smoothscale(hurt, DIM)

#images needed
playerimg = pygame.image.load( "Assets/Character_Animation.png" ).convert_alpha()

player_images = {	'walk': pygame.image.load( "Assets/Character_Animation.png" ).convert_alpha(),
					'spin': pygame.image.load( "Assets/Animation_side_attack.png" ).convert_alpha(),
					'up': pygame.image.load( "Assets/Up_attack(better).png" ).convert_alpha(),
					'down': pygame.image.load( "Assets/Down-Attack.png" ).convert_alpha(),
					'shield': pygame.image.load( "Assets/Powerups/Shield_ani.png" ).convert_alpha(),
					'hurt': hurt,
					'jump': pygame.image.load("Assets/Jump.png").convert_alpha(),
					'injection': pygame.image.load("Assets/Ingection.png").convert_alpha()	}

platform_img = [	pygame.image.load("Assets/Platform covers/platform_5.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_6.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_7.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_8.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_9.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_10.png").convert_alpha(),
					pygame.image.load("Assets/Platform covers/platform_inject.png").convert_alpha()	]

powerup_img = [		pygame.image.load("Assets/Powerups/Shield.png").convert_alpha(),
					pygame.image.load("Assets/Powerups/health_up.png").convert_alpha()	]

boss_img = [	pygame.image.load("Assets/Boss/Boss main platform.png").convert_alpha(),
				pygame.image.load("Assets/Boss/Boss divide.png").convert_alpha(),
				pygame.image.load("Assets/Boss/Boss divide 2.png").convert_alpha(),
				pygame.image.load("Assets/Boss/Boss divide 3.png").convert_alpha(),
				pygame.image.load("Assets/Boss/Boss divide 4.png").convert_alpha()	]

enemy_img = [ 	pygame.image.load("Assets/enemy_image_set.png").convert_alpha(),
				pygame.image.load("Assets/enemy_killed.png").convert_alpha(),
				pygame.image.load("Assets/enemy_despawn.png").convert_alpha()	]

image_dict = {	'platform':	platform_img,
				'powerup':	powerup_img,
				'boss':		boss_img,
				'enemy':	enemy_img	}

#sounds for game
sounds = {	'jump':		pygame.mixer.Sound("Assets/Sounds/jump.wav"),
			'step':		pygame.mixer.Sound("Assets/Sounds/step.wav"),
			'health':	pygame.mixer.Sound("Assets/Sounds/health_bump.wav"),
			'powerup':	pygame.mixer.Sound("Assets/Sounds/powerup.wav"),
			'inject':	pygame.mixer.Sound("Assets/Sounds/inject.wav")	}

#variables for difficulty of game
difficulty = {	'enemy_ct':			15,
				'enemy_ct_boss':	25,
				'enemy_dmg':		8,
				'enemy_life_time':	6000,
				'enemy_spawn_time':	800,
				'player_health':	100,
				'death_penalty':	5,
				'num_injects':		2,
				'heal_amount':		35,
				'shield_amount':	2,
				'powerup_respawn':	True,
				'boss_spawn':		(5600, 2000),
				'player_spawn':		(300, 8700)	}

#world and entities initialization
player_char = player((0, 0), player_images, sounds, difficulty)
level1=Level(player_char, background, render_size, image_dict, difficulty)
player_HUD = HUD(screen, player_char, "Assets/health_bar1.png", powerup_img)

#win screen fade timer
fade_timer = 100
fade_ct = 40
win_screen_timer = 5000
no_win = True

#music for game
world_music = "Assets/Sounds/lightout.ogg"
boss_music = "Assets/Sounds/lightin.ogg"
boss_music_playing = False

#start music
if music_on:
	pygame.mixer.music.load( world_music )
	pygame.mixer.music.set_volume(.5)
	pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(16)

#press any key to begin game
start_game = False
show_controls = True
show_instruction = True
show_last_frame = True

while start_game is False:
	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN:
			start_game = True
	screen.blit(start, (0,0))
	pygame.display.flip()

frame = 0
while frame < 12:
	screen.blit(intro[frame], (0,0))
	pygame.display.flip()
	frame += 1
	timer = 6000
	if frame==2 or frame==5 or frame==6 or frame==7 or frame==9:
		timer=3500
	if frame == 11:
		timer = 2000
	old_time = pygame.time.get_ticks()
	while timer >= 0:
		new_time = pygame.time.get_ticks()
		time_difference = new_time - old_time
		old_time = new_time
		timer -= time_difference
		pygame.event.pump()
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif evt.type == pygame.KEYDOWN:
				timer = 0

while show_last_frame:
	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN:
			show_last_frame = False
	screen.blit(intro[11], (0,0))
	pygame.display.flip()

while show_controls:
	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN:
			show_controls = False
	screen.blit(controls, (0,0))
	pygame.display.flip()

while show_instruction:
	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN:
			show_instruction = False
	screen.blit(instruction, (0,0))
	pygame.display.flip()

old_time = pygame.time.get_ticks()

while True:

	#screen to render on
	scale_screen = pygame.Surface(render_size)

	#deal with time
	new_time = pygame.time.get_ticks()
	time_difference = new_time - old_time
	old_time = new_time

	#did the player win?
	if no_win:

		if player_char.found_boss and not boss_music_playing and music_on:
			boss_music_playing = True
			pygame.mixer.music.stop()
			pygame.mixer.music.load( boss_music )
			pygame.mixer.music.set_volume(.5)
			pygame.mixer.music.play(-1)

		#if player dies, reset
		if player_char.health <= 0:

			#max health decreases as you die
			if player_char.max_health > player_char.full_health/2:
				player_char.max_health -= difficulty['death_penalty']
			else:
				player_char.max_health = player_char.full_health/2
			level1.reset()

			#wait for player input to restart
			dead = True
			while dead:
				if music_on:
					pygame.mixer.music.pause()
				pygame.event.pump()
				for evt in pygame.event.get():
					if evt.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
						dead = False
				screen.fill((0,0,0))
				if player_char.fell:
					screen.blit(dead_screen[1], (0,0))
				elif player_char.failed:
					screen.blit(dead_screen[2], (0,0))
				else:
					screen.blit(dead_screen[0], (0,0))
				pygame.display.flip()
			if music_on:
				pygame.mixer.music.unpause()

			player_char.failed = False
			player_char.fell = False

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
				if evt.key == pygame.K_SPACE or evt.key == pygame.K_w:
					space_pressed = True
			elif evt.type == pygame.KEYUP:
				if evt.key == pygame.K_a and player_char.velocity.x < 0:
					player_char.velocity.x = 0
				elif evt.key == pygame.K_d and player_char.velocity.x > 0:
					player_char.velocity.x = 0

		keys = [pygame.key.get_pressed(), space_pressed]

		# update player, enemies, level
		level1.update(time_difference, keys)

		# draw to screen and flip
		level1.draw(scale_screen, screen)

		# HUD stuff
		player_HUD.update_display(time_difference)

		# display HUD
		player_HUD.display()
		
		if player_char.won:
			no_win = False

	#player won
	else:
                pygame.event.pump()
		if fade_ct > 0:
			fade_timer -= time_difference
			if fade_timer <= 0:
				fade_ct -= 1
				fade_timer = 100
				screen.blit(transparent, (0,0))
		else:
			if win_screen_timer > 0:
				win_screen_timer -= time_difference
				screen.blit(you_win, (0,0))
			else:
				screen.blit(credits_screen, (0,0))
                                for evt in pygame.event.get():
                                        if evt.type == pygame.KEYDOWN:
                                                pygame.quit()
                                                sys.exit()
                for evt in pygame.event.get():
                        if evt.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

	pygame.display.flip() 
