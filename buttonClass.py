# ButtonClass.py

import pygame
pygame.init()

clickSound = pygame.mixer.Sound("music/clickSound.wav")

class Button():

	def __init__(self, x, y, image, scale):
		#initializes placement and image of the button
		self.width = image.get_width()
		self.height = image.get_height()
		self.scale = scale
		self.imageOrig = image
		self.image = pygame.transform.scale(image, (int(self.width*scale), int(self.height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.clicked = False

	def checkClicked(self,event,mouse_pos):
		#checks whether or not the usér's mouse is hovering over the button aswell as clicking,
		#if so, self.clicked is set to true and a sound is played
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.rect.collidepoint(event.pos) and self.clicked == False:
				self.clicked = True
				pygame.mixer.Sound.play(clickSound)
			else:
				self.clicked = False

	def expandOnHover(self,event,mouse_pos):
		#this is used to expand the size of the button whenever the user is hovering over it with their mouse.
		#this provides a much more clear interface
		if self.rect.collidepoint(mouse_pos):
			self.image = pygame.transform.scale(self.imageOrig,((self.width+10) * self.scale ,(self.height+10) * self.scale ))
		else:
			self.image = pygame.transform.scale(self.imageOrig,(self.width * self.scale ,self.height * self.scale))
		
		


	def draw(self,surface,event,mouse_pos):
		#draws the button on screen and returns the state of self.clicked
		self.clicked = False
		
		self.checkClicked(event,mouse_pos)
		self.expandOnHover(event,mouse_pos)

		surface.blit(self.image, (self.rect.x, self.rect.y))

		pygame.event.clear()
		
		return self.clicked 

class customizeButtons(Button):
	def __init__(self, x, y, image,lockedImage,scale,catId,unlocked):
		Button.__init__(self,x,y,image,scale)
		#inherits from button but also have a locked version of the image for when the user's highscore is not large enough
		self.lockedImage = pygame.transform.scale(lockedImage, (int(self.width*scale), int(self.height * scale)))
		self.activeImage = self.lockedImage
		self.action = False
		self.unlocked = unlocked
		self.catId = catId 
				

	def draw(self,surface,event,mouse_pos):
		#changes the active image depending on whether or not the button is unlocked
		if self.unlocked:
			self.checkClicked(event,mouse_pos)
			self.activeImage = self.image
		else:
			self.activeImage = self.lockedImage
		
		#checks for whether mouse is colliding to move image slightly in order for the user to know
		#that they are hovering
		if self.rect.collidepoint(mouse_pos) and self.unlocked:
			surface.blit(self.activeImage, (self.rect.x-10, self.rect.y-10))
		else:
			surface.blit(self.activeImage, (self.rect.x, self.rect.y))

		pygame.event.clear()
	 
	 	#returns state of self.clicked to main program
		return self.clicked


class textButton(Button):
	#is displayed on screen until user clicks on it 
	def __init__(self, x, y, image, scale):
		#inherits from button class
		Button.__init__(self,x,y,image,scale)
		self.errorOn = False

	def handleEvents(self,surface,event,mouse_pos):
		#checks for whether user is clicking
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pygame.mixer.Sound.play(clickSound)
			self.errorOn = False

	def draw(self,surface,event,mouse_pos):
		
		self.handleEvents(surface,event,mouse_pos)

		if self.errorOn:
			surface.blit(self.image,(self.rect.x,self.rect.y))
	