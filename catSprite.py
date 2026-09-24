
import random
import pygame
pygame.init()

skinList = ["White","Calico","Gray","Tortoise","Black"]

CAT_WIDTH = 27
CAT_HEIGHT = 20
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

GRAV = 5

class catSprite():
	def __init__(self,x,y,scale,ani,speed,colour):
		#Intiializes variables like the cat’s coordinates or the rect representing the cat
		self.width = CAT_WIDTH * scale
		self.height = CAT_HEIGHT * scale 
		self.x = x
		self.y = y
		self.rect = ((self.x,self.y),(self.width,self.height))
		self.scale = scale 
		#use of random library in order to have the on screen animated cats on the menu be randomized
		if colour == "random":
			self.colour = skinList[(random.randint(0,4))]
		else:
			self.colour = skinList[int(colour)]
		self.ani = ani
		self.image = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/stand.png")),self.scale)
		self.reset = False
		self.speed = speed

		# different animation lists where the images are loaded of the correct cat
		#each list is ended with a float value which represents the animation speed.
		if ani == 'static':
			self.animation = []
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/stand.png")),scale))

		
		elif ani == 'idle':

			self.idleList = []
			self.idleList.append(self.image)
			self.idleList.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/sitting.png")),scale))
			self.idleList.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/sleeping.png")),scale))
			self.idleList.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/sitting.png")),scale))
			self.idleList.append("0.01")

		elif ani != 'idle':
			self.animation = []
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+ani+" 1.png")),scale))
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+ani+" 2.png")),scale))
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+ani+" 3.png")),scale))
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+ani+" 4.png")),scale))
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+ani+" 5.png")),scale))
			self.animation.append(pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+ani+" 6.png")),scale))

			if ani == "walk":
				self.animation.append("0.2")
			if ani == "run":
				self.animation.append("0.3")

		self.current_sprite = 0

	def change(self):
		#used to update the object with a new colour
		
		if self.ani == 'idle':
			self.idleList[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/stand.png")),self.scale)
			self.idleList[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/sitting.png")),self.scale)
			self.idleList[2] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/sleeping.png")),self.scale)
			self.idleList[3] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/sitting.png")),self.scale)

		elif self.ani == 'static':
			self.image = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/stand.png")),self.scale)

		else:
			self.animation[0] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+self.ani+" 1.png")),self.scale)
			self.animation[1] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+self.ani+" 2.png")),self.scale)
			self.animation[2] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+self.ani+" 3.png")),self.scale)
			self.animation[3] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+self.ani+" 4.png")),self.scale)
			self.animation[4] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+self.ani+" 5.png")),self.scale)
			self.animation[5] = pygame.transform.scale_by((pygame.image.load("sprites/"+self.colour+"/"+self.ani+" 6.png")),self.scale)


	def animate(self):
		#runs the animation by iterating through the frame list
		self.current_sprite += float(self.animation[-1])
		

		if self.current_sprite >= len(self.animation) - 1:
			self.current_sprite = 0

		self.image = self.animation[int(self.current_sprite)]

	def movement(self):
		#used for if the cats on the menu run off screen, they are repositioned on the right hand side 
		#in order for them to keep running.
		self.x -= self.speed

		if self.x+320 <= 0:
			self.x = 1400
			self.colour = skinList[(random.randint(0,4))]
			self.reset = True
		else:
			self.reset = False


	def idleMovement(self):
		#handles the idle movement of the active skin display
		self.current_sprite += float(self.idleList[-1])

		if self.current_sprite >= len(self.idleList) - 1:
			self.current_sprite = 0

		self.image = self.idleList[int(self.current_sprite)]

	def draw(self,surface):
		#draws object on screen and runs other subroutines
		if self.ani == 'static':
			self.change()
			surface.blit(pygame.transform.flip(self.image, True, False), (self.x,self.y))
		elif self.ani != "idle":

			self.movement()
			if self.reset:
				self.change()
			self.animate()
			surface.blit(pygame.transform.flip(self.image, True,False),(self.x,self.y))

		else:
			
			
			self.change()
			self.idleMovement()
			surface.blit(pygame.transform.flip(self.image, True, False), (self.x,self.y))


