import pygame, pygame.mixer

pygame.init()

class object():

	def __init__(self, x,y,image,scale):
		#loads image and initializes the placement and scale
		self.scale = scale
		self.x = x
		self.y = y
		self.image = pygame.transform.scale_by((pygame.image.load("Props/"+image+".png")).convert_alpha(),scale)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		

	def draw(self,surface):
		#draws object on screen
		surface.blit(self.image,(self.x,self.y))



class objectSolid(object):
	#child of object class, use to be a solid platform that the cat can jump on.
	def __init__(self,x,y,image,scale):
		object.__init__(self,x,y,image,scale)

class objectPoints(object):
	
	def __init__(self,x,y,image,scale,noise,value):
		#inherits from object
		object.__init__(self,x,y,image,scale)
		#loads the original and broken version of the image.
		self.imageOrig = pygame.transform.scale_by((pygame.image.load("Props/"+image+".png")).convert_alpha(),scale)
		self.imageBroken = pygame.transform.scale_by((pygame.image.load("Props/"+image+"A.png")).convert_alpha(),scale)
		
		self.broken = False
		
		self.noise = noise
		self.value = value
		self.points = 0

	def handleEvents(self,surface,attack,catrect):
		#checks for whether or not the cat is colliding and attacking.
		#if so, then the breaking noise is played and the on-screen image is changed. 
		#and the value of the object is added to points which makes it avaliable for the main program to add to the total
		self.points = 0
		if catrect.colliderect(self.rect):
			
			if attack:
				if not self.broken:
					pygame.mixer.Sound.play(self.noise)
					self.points = self.value
					
				self.broken = True

		if self.broken:
			self.image = self.imageBroken
		else:
			self.image = self.imageOrig

		self.draw(surface)


	def draw(self,surface):
		#draws object on screen and returns points
		surface.blit(self.image,(self.x,self.y))
		return int(self.points)

# class objectMed():
	
# 	def __init__(self,x,y,image,scale,noise):
# 		self.scale = scale
# 		self.x = x 
# 		self.y = y
# 		self.imageOrig = pygame.transform.scale_by((pygame.image.load("Props/"+image+".png")).convert_alpha(),scale)
# 		self.imageBroken = pygame.transform.scale_by((pygame.image.load("Props/"+image+"A.png")).convert_alpha(),scale)
# 		self.width = self.imageOrig.get_width()
# 		self.height = self.imageOrig.get_width()
# 		self.image = pygame.transform.scale_by((self.imageOrig),scale)
# 		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
# 		self.broken = False
# 		self.mask = pygame.mask.from_surface(self.imageOrig)
# 		self.noise = noise
# 		self.points = 0

# 	def handleEvents(self,surface,attack,catrect):
# 		self.points = 0

# 		if catrect.colliderect(self.rect):
			
# 			if attack:
# 				if not self.broken:
# 					pygame.mixer.Sound.play(self.noise)
# 					self.points = 75
# 				self.broken = True

		

				

# 		# if attack and self.rect.collidepoint(catX,catY):
# 		# 	broken  = True

# 		self.draw(surface)


# 	def draw(self,surface):

# 		if self.broken:
# 			self.image = self.imageBroken
# 		else:
# 			self.image = self.imageOrig

# 		surface.blit(self.image,(self.x,self.y))

# class objectHigh():
	
# 	def __init__(self,x,y,image,scale,noise):
# 		self.scale = scale
# 		self.x = x 
# 		self.y = y
# 		self.imageOrig = pygame.transform.scale_by((pygame.image.load("Props/"+image+".png")).convert_alpha(),scale)
# 		self.imageBroken = pygame.transform.scale_by((pygame.image.load("Props/"+image+"A.png")).convert_alpha(),scale)
# 		self.width = self.imageOrig.get_width()
# 		self.height = self.imageOrig.get_width()
# 		self.image = pygame.transform.scale_by((self.imageOrig),scale)
# 		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
# 		self.broken = False
# 		self.mask = pygame.mask.from_surface(self.imageOrig)
# 		self.noise = noise
# 		self.points = 0

# 	def handleEvents(self,surface,attack,catrect):
# 		self.points = 0

# 		if catrect.colliderect(self.rect):
			
# 			if attack:
# 				if not self.broken:
# 					pygame.mixer.Sound.play(self.noise)
# 					self.points = 100
# 				self.broken = True

		

				

# 		# if attack and self.rect.collidepoint(catX,catY):
# 		# 	broken  = True

# 		self.draw(surface)


# 	def draw(self,surface):

# 		if self.broken:
# 			self.image = self.imageBroken
# 		else:
# 			self.image = self.imageOrig

# 		surface.blit(self.image,(self.x,self.y))