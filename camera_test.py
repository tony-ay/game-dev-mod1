import sys, pygame

pygame.init()

DIM = [1024, 768]

screen = pygame.display.set_mode( (DIM[0], DIM[1]) )

bgsize = (2000,2000)
background = pygame.Surface(bgsize)
background.fill((0,255,0))

test = pygame.Surface((100,200))
test.fill((255,0,0))

other = pygame.Surface((100,200))
other.fill((0,0,255))

testx = 700
testy = 700

otherx = 1000
othery = 700

while True:

	pygame.event.pump()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()

	testx += -1
	testy += 0

	background = pygame.Surface((2000,2000))
	background.fill((0,255,0))	
	background.blit(test, (testx,testy))
	background.blit(other, (otherx,othery))

	screenposx = testx-DIM[0]/2
	screenposy = testy-DIM[1]/2

	if(screenposx + DIM[0]>=bgsize[0]+50):
		screenposx = bgsize[0] - DIM[0] + 50
	elif(screenposx<=-50):
		screenposx = -50
	if(screenposy + DIM[1]>=bgsize[1]+50):
		screenposy = bgsize[1] - DIM[1] + 50
	elif(screenposy<=-50):
		screenposy = -50

	screen.fill((0,0,255))
	screen.blit(background, (-screenposx,-screenposy))

	pygame.display.flip()