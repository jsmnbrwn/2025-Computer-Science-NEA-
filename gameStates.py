import pygame, objectClass, charClass

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))  

#loading of different backgrounds
kitchenBackground = pygame.image.load("images/kitchenBackground.png").convert_alpha()
bedroomBackground = pygame.image.load("images/bedroomBackground.png").convert_alpha()
loungeBackground = pygame.image.load("images/loungeBackground3.png").convert_alpha()
bathroomBackground = pygame.image.load("images/bathroomBackground.png").convert_alpha()

#loading of different sounds
crashSound = pygame.mixer.Sound("music/crashSound.wav")
foodSound = pygame.mixer.Sound("music/foodSound.wav")
metalSound = pygame.mixer.Sound("music/metalSound.wav")
paperSound = pygame.mixer.Sound("music/paperSound.wav")
bookFallSound = pygame.mixer.Sound("music/bookFallSound.wav")

soundList = [crashSound,foodSound,metalSound,paperSound,bookFallSound]

backgroundList = [kitchenBackground,loungeBackground,bedroomBackground,bathroomBackground]

def objectLoadKitchen():
	#creation of platforms and objects and compiling them into a list
	vase = objectClass.objectPoints(12,60,"vase1",3.3,soundList[0],10)
	plant = objectClass.objectPoints(1150,30,"Plant5",3.3,soundList[0],50)
	turkey = objectClass.objectPoints(1035,320,"turkey",4,soundList[1],1000)
	trash = objectClass.objectPoints(-80,710,"trashcan1",4.5,soundList[2],75)
	fish = objectClass.objectPoints(394,675,"fish1",3,soundList[1],100)
	painting = objectClass.objectPoints(605,442,"painting6",9,soundList[3],25)
	painting2 = objectClass.objectPoints(370,50,"painting3",9,soundList[3],25)

	cupboard1 = objectClass.objectSolid(-10,205,"Cupboard1",4.1)
	cupboard2 = objectClass.objectSolid(290,205,"Cupboard1",4.1)
	cupboard3 = objectClass.objectSolid(590,205,"Cupboard1",4.1)
	plat1 = objectClass.objectSolid(1150,205,"platformV",1.8)
	plat2 = objectClass.objectSolid(900,205,"platformV",1.8)
	fridge = objectClass.objectSolid(1002,420,"Fridge",5)
	oven = objectClass.objectSolid(640,690,"Stove",5)
	table = objectClass.objectSolid(330,730,"DiningTable",4.5)

	kitchenObj = [plant,vase,turkey,trash,fish,painting,painting2]
	kitchenPlat = [plat1,plat2,cupboard1,cupboard2,cupboard3,fridge,oven,table]

	return kitchenObj, kitchenPlat



def kitchen(SCREEN,event,Cat,kitchenObj,kitchenPlat):
	
	pygame.mouse.set_visible(False)
	
	#iterates through every object on screen and checks for collisions and thus checks for 
	#any potential points to be added
	for obj in kitchenObj:
		obj.handleEvents(SCREEN,Cat.attack,Cat.rect) 
		Cat.POINTS += obj.points
		
	#draws platforms
	for plat in kitchenPlat:
		plat.draw(SCREEN)

	#draws cat
	Cat.draw(SCREEN,event,kitchenPlat)

	return backgroundList[0]


def objectLoadBedroom():
	#creation of platforms and objects and compiling them into a list
	plant1 = objectClass.objectPoints(220,582,"Plant2",4,soundList[2],25)
	plant2 = objectClass.objectPoints(1045,90,"Plant4",3.4,soundList[2],25)
	globe = objectClass.objectPoints(17,180,"Globe",3,soundList[2],50)
	dresserMirror = objectClass.objectPoints(1111,402,"Dresser2Mirror",4.5,soundList[0],75)
	bag = objectClass.objectPoints(670,630,"bag1",4,soundList[3],50)
	bookcase = objectClass.objectPoints(-100,320,"Bookcase1",5.6,soundList[4],100)
	painting = objectClass.objectPoints(631,158,"painting4",8.5,soundList[3],50)

	# bed = objectClass.objectSolid(-10,205,"Cupboard1",4.1)
	dresser = objectClass.objectSolid(1073,640,"Dresser2",5)
	plat1 = objectClass.objectSolid(900,250,"platformV",2.8)
	plat2 = objectClass.objectSolid(1200,250,"platformV",2.8)

	plat3 = objectClass.objectSolid(10,340,"platformI",2.8)
	plat4 = objectClass.objectSolid(10,520,"platformI",2.8)
	plat5 = objectClass.objectSolid(10,670,"platformI",2.8)
	plat6 = objectClass.objectSolid(480,750,"platformI",2.8)
	plat7 = objectClass.objectSolid(700,750,"platformI",2.8)
	plat8 = objectClass.objectSolid(1240,420,"platformI",1)

	bedroomObj = [plant2,globe,dresserMirror,bag,bookcase,painting,plant1]
	bedroomPlat = [dresser,plat1,plat2,plat3,plat4,plat5,plat6,plat7,plat8]

	return bedroomObj, bedroomPlat

def bedroom(SCREEN,event,Cat,bedroomObj,bedroomPlat):

	pygame.mouse.set_visible(False)

	#iterates through every object on screen and checks for collisions and thus checks for 
	#any potential points to be added
	for obj in bedroomObj:
		obj.handleEvents(SCREEN,Cat.attack,Cat.rect)
		Cat.POINTS += obj.points
	#draws platforms
	for plat in bedroomPlat:
		plat.draw(SCREEN)
	#draws cat
	Cat.draw(SCREEN,event,bedroomPlat)

	return backgroundList[2]


def objectLoadLounge():
	#creation of platforms and objects and compiling them into a list
	plant1 = objectClass.objectPoints(40,622,"Plant1",4,soundList[2],25)
	sofa = objectClass.objectPoints(202,575,"Sofa1",5.5,soundList[4],100)
	plant2 = objectClass.objectPoints(760,608,"Plant2",4,soundList[2],25)
	tv = objectClass.objectPoints(1130,470,"TV1",4,soundList[0],100)
	vase1 = objectClass.objectPoints(30,135,"vase1",4,soundList[0],25)
	vase2 = objectClass.objectPoints(1120,110,"vase2",4,soundList[0],25)
	painting = objectClass.objectPoints(550,150,"painting2",9.5,soundList[3],50)
	
	dresser = objectClass.objectSolid(1053,730,"dresser1",5)
	plat1 = objectClass.objectSolid(1028,311,"platformVDark",2.8)
	plat2 = objectClass.objectSolid(-20,311,"platformVDark",2.8)
	plat3 = objectClass.objectSolid(550,450,"platformVDark",2)
	plat4 = objectClass.objectSolid(560,450,"platformI",3.4)
	plat5 = objectClass.objectSolid(255,750,"platformI",3)
	plat6 = objectClass.objectSolid(375,750,"platformI",3)
	plat7 = objectClass.objectSolid(495,750,"platformI",3)
	plat8 = objectClass.objectSolid(580,750,"platformI",3)

	loungeObj = [sofa,plant1,plant2,tv,vase1,vase2,painting]
	loungePlat = [dresser,plat1,plat2,plat3,plat4,plat5,plat6,plat7,plat8]

	return loungeObj, loungePlat

def lounge(SCREEN,event,cat,loungeObj,loungePlat):

	pygame.mouse.set_visible(False)

	#iterates through every object on screen and checks for collisions and thus checks for 
	#any potential points to be added
	for obj in loungeObj:
		obj.handleEvents(SCREEN,cat.attack,cat.rect)
		cat.POINTS += obj.points
	#draws platforms
	for plat in loungePlat:
		plat.draw(SCREEN)
	#draws cat
	cat.draw(SCREEN,event,loungePlat)

	return backgroundList[1]


def objectLoadBathroom():
	#creation of platforms and objects and compiling them into a list
	mirror = objectClass.objectPoints(238,114,"mirror",4.5,soundList[0],50)
	painting = objectClass.objectPoints(938,114,"painting5",12,soundList[3],25)
	box = objectClass.objectPoints(582,240,"box",3.7,soundList[4],75)
	toilet = objectClass.objectPoints(14,655,"Toilet",4.6,soundList[2],25)
	clotheshanger = objectClass.objectPoints(600,450,"clothhang",5.8,soundList[4],100)
	piggyBank = objectClass.objectPoints(1200,70,"piggybank",3,soundList[0],500)
	
	plat1 = objectClass.objectSolid(65,775,"platformI",2.1)
	plat2 = objectClass.objectSolid(14,655,"platformI",2)
	plat3 = objectClass.objectSolid(900,715,"platformI",3)
	plat4 = objectClass.objectSolid(1130,715,"platformI",3)
	plat5 = objectClass.objectSolid(-190,460,"platformVDark",2.5)
	plat6 = objectClass.objectSolid(525,366,"platformVDark",2.2)
	plat7 = objectClass.objectSolid(1200,185,"platformVDark",2.5)

	bathroomObj = [mirror, painting, box, toilet, clotheshanger,piggyBank]
	bathroomPlat = [plat1,plat2,plat3,plat4,plat5,plat6,plat7]

	return bathroomObj, bathroomPlat

def bathroom(SCREEN, event, cat, bathroomObj, bathroomPlat):

	pygame.mouse.set_visible(False)

	#iterates through every object on screen and checks for collisions and thus checks for 
	#any potential points to be added
	for obj in bathroomObj:
		obj.handleEvents(SCREEN,cat.attack,cat.rect)
	cat.POINTS += obj.points
	#draws platforms
	for plat in bathroomPlat:
		plat.draw(SCREEN)

	#draws cat
	cat.draw(SCREEN,event,bathroomPlat)

	return backgroundList[3]