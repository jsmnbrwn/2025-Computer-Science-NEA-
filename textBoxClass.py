import pygame
import random
pygame.init()
pygame.font.init()


# Initilizes font and loads sounds. Packages all the different type sounds into a list.
base_font = pygame.font.SysFont('november',65)
secondary_font = pygame.font.SysFont('november',30)

clickSound = pygame.mixer.Sound("music/clickSound2.wav")

typeSound1 = pygame.mixer.Sound("music/typeSound1.wav")
typeSound2 = pygame.mixer.Sound("music/typeSound2.wav")
typeSound3 = pygame.mixer.Sound("music/typeSound3.wav")
typeSound4 = pygame.mixer.Sound("music/typeSound4.wav")
typeSound5 = pygame.mixer.Sound("music/typeSound5.wav")

typeSoundList = [typeSound1,typeSound2,typeSound3,typeSound4,typeSound5]


class textBox():
	def __init__(self,x,y,image,scale,smallerFont): 
		#Initializes class, uses the image to get the width and height, which is then able to be scaled accordingly
		self.width = image.get_width()
		self.height = image.get_height()
		self.scale = scale
		self.image = pygame.transform.scale(image, (int(self.width*scale), int(self.height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.text = ''

		self.smallerFont = smallerFont
		#Sets font to smaller font if Boolean value is true.
		if smallerFont:
			self.text_surface = secondary_font.render(self.text, True, (88,71,66))
		else:
			self.text_surface = base_font.render(self.text, True, (88,71,66))
		self.active = False
	
	def reset(self):
		#Resets the textbox to have no contents 
		self.text = '' 	

	def type(self,surface,event,key):
		#Checks if the textbox is active (has been clicked on) and checks if user is deleting characters or has pressed return. 
		#Otherwise, the key the user typed is appended to the string and a random type sound is played. 
		if self.active:
			if key == chr(pygame.K_BACKSPACE):
				pygame.mixer.Sound.play(typeSoundList[(random.randint(0,4))])
				self.text  = self.text[:-1]
			elif key == chr(pygame.K_RETURN):
				self.active = False
			elif len(self.text) < 27:	
				self.text += key
				if key != '':
					pygame.mixer.Sound.play(typeSoundList[(random.randint(0,4))])

	
		self.draw(surface,event)

		




	def handleEvents(self,surface,event,key):
		#Checks whether or not the user has clicked onto the textbox and changes actie to true if this is the case.
		self.type(surface,event,key)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				pygame.mixer.Sound.play(clickSound)
				self.active = True 

			else:
				self.active = False
		
		
		
		return self.text

	def draw(self,surface,event):
		#Draws the textbox image and text.
		if self.active:
			image = pygame.transform.scale(self.image, (int(self.width*self.scale*1.05), int(self.height * self.scale*1.05)))
		else:
			image = pygame.transform.scale(self.image, (int(self.width*self.scale), int(self.height * self.scale)))
		
		#Makes appropriate adjustments if the smallerFont is true or if the textbox is active. 
		if self.smallerFont:
			self.text_surface = secondary_font.render(self.text, True, (88,71,66))
		else:
			self.text_surface = base_font.render(self.text, True, (88,71,66))
		

		surface.blit(image,(self.rect.x, self.rect.y))
		surface.blit(self.text_surface,(self.rect.x+25,self.rect.y+25))

		

			
class textBoxSolid():
	def __init__(self,x,y,text,scale): 
		# Initializes class, uses the image to get the width and height, which is then able to be scaled accordingly.
		self.x = x 
		self.y = y
		self.scale = scale
		self.text = text
		self.font = pygame.font.SysFont('november',int(65 * scale))
		self.text_surface = self.font.render(self.text, True, (53,42,31))
		self.active = False
		


	def handleEvents(self,surface,updatedText):
		#updates text and then calls the draw subroutine
		self.font = pygame.font.SysFont('november',int(65 * self.scale))
		self.text = updatedText

		self.draw(surface)
		

	
	def draw(self,surface):
		#Draws the textbox image + text
		self.text_surface = self.font.render(self.text, True, (53,42,31))
		
		surface.blit(self.text_surface,(self.x,self.y))

				
  					
	
		


			

		
		
