
import random
import pygame
pygame.init()

skinList = ["White","Calico","Gray","Tortoise","Black"]

CAT_WIDTH = 27
CAT_HEIGHT = 20
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

GRAV = 5

ANI_SPEEDS = {"walk":0.05, "run":0.095, "idle":0.01, "static":0}
imageCache = {}

def loadSprite(colour,name,scale):
		key = (colour,name,scale)
		if key not in imageCache:
			image = pygame.image.load("sprites/"+colour+"/"+name+".png").convert_alpha()
			image = pygame.transform.scale_by(image,scale)
			image = pygame.transform.flip(image,True,False)
			imageCache[key] = image

		return imageCache[key]

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
		self.aniSpeed = ANI_SPEEDS.get(ani,0.2)
		self.reset = False
		self.speed = speed

		self.frames = []
		self.loadedColour = None
		self.current_sprite = 0

		self.change()
		self.image = self.frames[0]
		

	def change(self):
	#updates the frames to the current colour, using the cache
		if self.ani == 'static':
			names = ["stand"]
		elif self.ani == 'idle':
			names = ["stand","sitting","sleeping","sitting"]
		else:
			names = [self.ani+" "+str(i) for i in range(1,7)]

		self.frames = [loadSprite(self.colour,name,self.scale) for name in names]
		self.loadedColour = self.colour


	def animate(self):
		#runs the animation by iterating through the frame list
		self.current_sprite += self.aniSpeed

		if self.current_sprite >= len(self.frames):
			self.current_sprite = 0

		self.image = self.frames[int(self.current_sprite)]

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


	def draw(self,surface):
		#draws object on screen and runs other subroutines
		if self.ani != 'static' and self.ani != 'idle':
			self.movement()
	
		if self.colour != self.loadedColour:
			self.change()

		if self.ani == 'static':
			self.image = self.frames[0]
		else:
			self.animate()
			
		surface.blit(self.image,(self.x,self.y))



