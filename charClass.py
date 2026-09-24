
import random
import pygame
pygame.init()

skinList = ["White","Calico","Gray","Tortoise","Black"]

CAT_WIDTH = 14
CAT_HEIGHT = 13
IMG_WIDTH = 25
IMG_HEIGHT = 15
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

GRAV = 5



class catChar():
	def __init__(self, x, y, colourID, scale):
		#Intiializes variables like the cat’s coordinates or the rect representing the cat
		self.width = CAT_WIDTH * scale
		self.height = CAT_HEIGHT * scale 
		self.x = x 
		self.y = y
		self.rectX = x + 11
		self.rectY = y + 3
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.scale = scale 
		colourID = int(colourID)
		self.colour = skinList[colourID]
		self.jumpCount = 45
		self.vel_y = 0
		self.FLOOR = y + self.height

		#boolean values which reference the current activity of the cat.
		self.moving = False
		self.left = False
		self.sprint = False
		self.isJump = False
		self.isCrouch = False


		#five different animation lists where the images are loaded of the correct cat
		#each list is ended with a float value which represents the animation speed.

		self.jump = []
		self.jump.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 1.png")).convert_alpha(),scale))
		self.jump.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 2.png")).convert_alpha(),scale))
		self.jump.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 3.png")).convert_alpha(),scale))
		self.jump.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 3.png")).convert_alpha(),scale))
		self.jump.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 3.png")).convert_alpha(),scale))
		self.jump.append("0.03")

		self.crouch = []
		self.crouch.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/crouch 1.png")).convert_alpha(),scale))
		self.crouch.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/crouch 2.png")).convert_alpha(),scale))
		self.crouch.append("0.005")

		self.idle = []
		self.idle.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 1.png")).convert_alpha(),scale))
		self.idle.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 2.png")).convert_alpha(),scale))
		self.idle.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 3.png")).convert_alpha(),scale))
		self.idle.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 4.png")).convert_alpha(),scale))
		self.idle.append("0.01")

		self.walk = []
		self.walk.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 1.png")).convert_alpha(),scale))
		self.walk.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 2.png")).convert_alpha(),scale))
		self.walk.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 3.png")).convert_alpha(),scale))
		self.walk.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 4.png")).convert_alpha(),scale))
		self.walk.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 5.png")).convert_alpha(),scale))
		self.walk.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 6.png")).convert_alpha(),scale))
		self.walk.append("0.03")

		self.run = []
		self.run.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 1.png")).convert_alpha(),scale))
		self.run.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 2.png")).convert_alpha(),scale))
		self.run.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 3.png")).convert_alpha(),scale))
		self.run.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 4.png")).convert_alpha(),scale))
		self.run.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 5.png")).convert_alpha(),scale))
		self.run.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 6.png")).convert_alpha(),scale))
		self.run.append("0.045")

		self.POINTS = 0 

		self.current_sprite = 0

		self.attack = False

		self.onPlatform = False

		self.image = self.idle[self.current_sprite]
		

	def changeColour(self,colourID):
		#Updates the animation lists with the new images after a user changes their active skin.
		self.colour = skinList[colourID]

		self.jump[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 1.png")).convert_alpha(),self.scale)
		self.jump[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 2.png")).convert_alpha(),self.scale)
		self.jump[2] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 3.png")).convert_alpha(),self.scale)
		self.jump[3] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 3.png")).convert_alpha(),self.scale)
		self.jump[4] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/jump 3.png")).convert_alpha(),self.scale)
		

		
		self.crouch[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/crouch 1.png")).convert_alpha(),self.scale)
		self.crouch[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/crouch 2.png")).convert_alpha(),self.scale)
		

		self.idle[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 1.png")).convert_alpha(),self.scale)
		self.idle[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 2.png")).convert_alpha(),self.scale)
		self.idle[2] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 3.png")).convert_alpha(),self.scale)
		self.idle[3] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/idle 4.png")).convert_alpha(),self.scale)
		

		
		self.walk[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 1.png")).convert_alpha(),self.scale)
		self.walk[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 2.png")).convert_alpha(),self.scale)
		self.walk[2] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 3.png")).convert_alpha(),self.scale)
		self.walk[3] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 4.png")).convert_alpha(),self.scale)
		self.walk[4] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 5.png")).convert_alpha(),self.scale)
		self.walk[5] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/walk 6.png")).convert_alpha(),self.scale)
		

		self.run[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 1.png")).convert_alpha(),self.scale)
		self.run[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 2.png")).convert_alpha(),self.scale)
		self.run[2] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 3.png")).convert_alpha(),self.scale)
		self.run[3] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 4.png")).convert_alpha(),self.scale)
		self.run[4] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 5.png")).convert_alpha(),self.scale)
		self.run[5] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/run 6.png")).convert_alpha(),self.scale)







	
	def collisions(self,objectRect,dx,dy):
		#This code checks whether or not the next movement of the rectangle will collide with the on-screen objects. 
		#This subroutine is run after all other movement calculations are performed. This is because, this subroutine 
		#will change the next movement of the cat (dy) to 0 in order to stop the cat moving due to the collision. 
		for obj in objectRect:
			if self.rect.bottom <= obj.rect.top:
				

				if self.left:
					if obj.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
						
						self.onPlatform = True
						dy = obj.rect.top - self.rect.bottom
						self.vel_y = 0
						self.isJump = False

				else:
					if obj.rect.colliderect(self.rect.x+90,self.rect.y+dy,self.width,self.height):
						
						self.onPlatform = True
						dy = obj.rect.top - self.rect.bottom
						self.vel_y = 0
						self.isJump = False


			
			# if self.rect.bottom < obj.rect.top:

			# 	if not self.left:
			# 		if obj.rect.colliderect(self.rect.x+100,self.rect.y+dy,self.width,self.height):
			# 			print("colliding R",dy)
			# 			self.onPlatform = True
			# 			isJump = False
			# 			dy = 0
							
			# 			self.vel_y = 0
			# 	elif obj.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
			# 			print("colliding L",dy)
			# 			self.onPlatform = True
			# 			isJump = False
			# 			dy = 0
						
		# print('vel_y',self.vel_y)
		# print('rect.y',self.rect.y)
		# print('dy',dy)
		return dx,dy


	def movement(self,event,objectRect):
		#Gets the input of the user’s keyboard to see if they want the cat to move left or right and checks to 
		#see whether the user is pressing shift/crouching which increases/reduces the speed.
		dx = 0
		dy = 0 
		
		key_pressed = pygame.key.get_pressed()

		if key_pressed[pygame.K_d]:
			dx += 1.5
			self.left = False
			self.moving = True
		elif key_pressed[pygame.K_a]:
			dx -= 1.5
			self.left = True
			self.moving = True
		else:
			self.moving = False

		
		if key_pressed[pygame.K_LSHIFT]:
			dx *= 1.7
			self.sprint = True
		else:
			self.sprint = False
		if self.isCrouch:
			dx *= 0.1

		if not self.isJump:
			if key_pressed[pygame.K_SPACE]:
				self.isJump = True
			
		#Uses a quadratic for the jump movement in order for there to be a slight pause at the top.
		if self.isJump:
			if self.jumpCount > -45:
				isJump = True

				self.vel_y = ((self.jumpCount * GRAV) * -0.5) / 15
				self.jumpCount -= 0.65
			else:
				self.jumpCount = 45
				self.isJump = False

			dy = self.vel_y
			
		
		#Handles gravity- if user is not jumping then will constantly be moving down, 
		#however then the following if statement checks whether or not the cat is about to pass through the ground. 
		#If it is, then dy is set to 0 and the cat’s y coordinate is not effected.
		if not self.isJump:
			self.jumpCount = 45
			self.vel_y += 2
			if self.vel_y >= 13:
				self.vel_y = 13
			if self.rect.bottom < self.FLOOR:
				dy += self.vel_y * GRAV * 0.1

		
		dx,dy = self.collisions(objectRect,dx,dy)

		if self.rect.bottom > self.FLOOR:
			self.rect.bottom = self.FLOOR

			
		
	
	
		self.y += dy
		self.x += dx

	def ability(self,event):
		#Checks whether or not the the user is attacking/crouching. Sets relevant Boolean values to true which means other subroutines can 
		key_pressed = pygame.key.get_pressed()

		if key_pressed[pygame.K_c]:
			self.isCrouch = True
		else:
			self.isCrouch = False

		

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			self.attack = True
			# print("Attack")
			return True
		else:
			self.attack = False

		#used to allow the user to drop down from a platform
		if key_pressed[pygame.K_s] and self.onPlatform:
			self.y += 1
			self.rectY += 1
			self.onPlatform = False

		

	def update(self,event):
		#sets the current animation list to different lists depending on the boolean values
		current = self.idle


		if self.isJump:
			current = self.jump
		elif self.moving:
			if self.sprint:
				current = self.run
			else:
				current = self.walk
		else:
			current = self.idle

		if self.isCrouch:
			current = self.crouch

		self.current_sprite += float(current[-1])

		if int(self.current_sprite) >= len(current)-1:
			self.current_sprite = 0

		self.image = current[int(self.current_sprite)]
		
		self.rect = pygame.Rect((self.x,self.y),(self.width,self.height))
		# self.imageRect = pygame.Rect((self.x,self.y),(IMG_WIDTH*self.scale,IMG_HEIGHT*self.scale))



		# if self.isJump: 																			Original aniumation code which I optimized 
		# 	self.current_sprite += 0.1

		# 	if int(self.current_sprite) >= len(self.jump):
		# 		self.current_sprite = 0

		# 	self.image = self.jump[int(self.current_sprite)]


		# if not self.moving:
		# 	self.current_sprite += 0.1

		# 	if int(self.current_sprite) >= len(self.idle):
		# 		self.current_sprite = 0

		# 	self.image = self.idle[int(self.current_sprite)]

		# if self.moving: 
		# 	if self.sprint:
		# 		self.current_sprite += 0.3

		# 		if int(self.current_sprite) >= len(self.run):
		# 			self.current_sprite = 0

		# 		self.image = self.run[int(self.current_sprite)]

		# 	elif not self.sprint:
		# 		self.current_sprite += 0.2

		# 		if int(self.current_sprite) >= len(self.walk):
		# 			self.current_sprite = 0

		# 		self.image = self.walk[int(self.current_sprite)]

	def draw(self,surface,event,objectRect): 
		#runs appropriate subroutines and draws the image of the cat on screen.
		self.movement(event,objectRect)
		self.ability(event)
		self.update(event)
		


		if self.left:
			surface.blit(pygame.transform.flip(self.image, True,False),(self.x,self.y))
		if not self.left:
			surface.blit(self.image,(self.x,self.y))

		
