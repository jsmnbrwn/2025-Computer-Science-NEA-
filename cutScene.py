import pygame
pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

BLACK = (0,0,0,1)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))       




class cutscene():
	def __init__(self, x, y, numOfFrames, type, speed, scale):
		#Makes use of strategically names files and iterates through for however many frames there are in order to load all images of a cutscene into a list
		self.numOfFrames =  numOfFrames 
		self.type = type 
		self.frameList = []
		self.scale = scale 
		self.finished = False
		self.onScreen = False
		self.blackScreen = False 

		self.frameX = x 
		self.frameY = y

		self.image = ''

		self.currentFrame = 0
		self.animationSpeed = speed 


		for i in range(numOfFrames):
			self.frameList.append(pygame.transform.scale_by((pygame.image.load("cutSceneImages/"+type+str(i+1)+".png")),scale))


	def getFrame(self):
		#Iterates through the frameList and updates self.image at the speed which was initialized at creation.
		self.currentFrame += float(self.animationSpeed)

		if self.currentFrame >= len(self.frameList):
			self.currentFrame = 0
			self.finished = True
			self.onScreen = False  

		self.image = self.frameList[int(self.currentFrame)]

	def play(self, SCREEN):
		#calls the getFrame subroutine and then draws this image on screen 
		self.getFrame()
		if self.onScreen:
			SCREEN.blit(self.image, (self.frameX,self.frameY))

		



		