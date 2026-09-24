import pygame, random, sys, os, pygame.mixer
import sqlite3, hashlib

import buttonClass, charClass, catSprite, textBoxClass, objectClass, gameStates, cutScene

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
#Creates constants of screen size
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
try:
    pygame.Window.from_display_module().maximize()
except AttributeError:
    pass    
pygame.display.set_caption("CATastrophe")                                                 
#Initializes db connection and pygame display
dataConnection = sqlite3.connect('AccountData')
dataCursor = dataConnection.cursor()

#creates accounts table if it doesnt already exist
dataCursor.execute(""" 
CREATE TABLE IF NOT EXISTS accounts (
	id INTEGER PRIMARY KEY NOT NULL,
	username VARCHAR(16) NOT NULL, 
	password VARCHAR(16) NOT NULL
)
""")

#creates accountData table if it doesnt already exist
dataCursor.execute(""" 
CREATE TABLE IF NOT EXISTS accountData (
	id INTEGER PRIMARY KEY NOT NULL,
	username VARCHAR(16),
	highScore INT NOT NULL, 
	skinData VARCHAR(5) NOT NULL,
	activeSkin VARCHAR(1) NOT NULL
)
""")


#creates friendRequests table if it doesnt already exist
dataCursor.execute(""" 
CREATE TABLE IF NOT EXISTS friendRequests (
	requestID INTEGER PRIMARY KEY NOT NULL,
	requestingUserID INTEGER NOT NULL,
	targetUserID INTEGER NOT NULL,
	FOREIGN KEY (requestingUserID) REFERENCES accountData(id),
	FOREIGN KEY (targetUserID) REFERENCES accountData(id)
)
""")


#creates friendList table if it doesnt already exist
dataCursor.execute(""" 
CREATE TABLE IF NOT EXISTS friendList (
	friendshipID INTEGER PRIMARY KEY NOT NULL,
	user1ID INTEGER NOT NULL,
	user2ID INTEGER NOT NULL,
	FOREIGN KEY (user1ID) REFERENCES friendRequests(requestingUserID),
	FOREIGN KEY (user2ID) REFERENCES friendRequests(targetUserID)

)
""")


#creates a blank event used to clear the active event after each main loop
blankEvent = pygame.event.Event(pygame.event.custom_type())


#Loads all images:
BaseBackground = pygame.image.load("images/BaseBackground.png")
MainBackground = pygame.image.load("images/MainBackground.png")
MainBackground2 = pygame.image.load("images/MainBackground2.png")
SignupBackground = pygame.image.load("images/SignupBackground2.png")
LoginBackground = pygame.image.load("images/LoginBackground2.png")
leaderboardBackground = pygame.image.load("images/leaderboardBackground.png")
customizeBackground = pygame.image.load("images/customizeBackground.png")
FriendBackground = pygame.image.load("images/friendBackground.png")
AccountBackground = pygame.image.load("images/accountBackground.png")

outroBackground = pygame.image.load("images/outroBackground.png").convert_alpha()
introBackground =  pygame.image.load("images/introBackground.png").convert_alpha()
# testBackground = pygame.image.load("images/blackBackground.png").convert_alpha()
# testBackground.set_alpha(200)

friendTextboxImage = pygame.image.load("images/friendTextboxImage.png").convert_alpha()
TextboxImage = pygame.image.load("images/TextboxImage.png").convert_alpha()
PlayImage = pygame.image.load("images/PLAY BUTTON2.png").convert_alpha()
CustomizeImage = pygame.image.load("images/CUSTOMIZE BUTTON2.png").convert_alpha()
LeaderboardImage = pygame.image.load("images/LEADERBOARD BUTTON2.png").convert_alpha()
LoginImage = pygame.image.load("images/LOGIN.png").convert_alpha()
SignupImage = pygame.image.load("images/SIGNUP.png").convert_alpha()
BackwardImage = pygame.image.load("images/BackwardImage.png").convert_alpha()
EnterImage = pygame.image.load("images/EnterImage.png").convert_alpha()
FriendsImage = pygame.image.load("images/FRIENDS.png").convert_alpha()
accountImage = pygame.image.load("images/ACCOUNT.png").convert_alpha()
friendEnterButtonImage = pygame.image.load("images/friendEnterButton.png").convert_alpha()
friendAcceptImage = pygame.image.load("images/friendAcceptImage.png").convert_alpha()
friendDeclineImage = pygame.image.load("images/friendDeclineImage.png").convert_alpha()
accountEnterButtonImage = pygame.image.load("images/accountEnterButton.png").convert_alpha()
accountLogoutButtonImage = pygame.image.load("images/accountLogoutButton.png").convert_alpha()
accountDeleteButtonImage = pygame.image.load("images/accountDeleteButton.png").convert_alpha()
accountTextboxImage = pygame.image.load("images/accountNameTextbox.png").convert_alpha()

noAccountFoundImage = pygame.image.load("images/noAccountFoundIMG.png").convert_alpha()
incorrectPasswordImage = pygame.image.load("images/incorrectPasswordIMG.png").convert_alpha()
unsecurePasswordImage =  pygame.image.load("images/unsecurePasswordIMG.png").convert_alpha()
accountAlreadyExistsImage = pygame.image.load("images/accountAlreadyExistsIMG.png").convert_alpha()
usernameTooShortImage = pygame.image.load("images/usernameTooShortIMG.png").convert_alpha()
loginToPlayImage = pygame.image.load("images/loginToPlayIMG.png").convert_alpha()
loginToCustomizeImage = pygame.image.load("images/loginToCustomizeIMG.png").convert_alpha()
friendsWithYourselfImage = pygame.image.load("images/friendsWithYourself.png").convert_alpha()
requestAlreadySentImage  = pygame.image.load("images/requestAlreadySent.png").convert_alpha()
alreadyFriendsImage = pygame.image.load("images/alreadyFriends.png").convert_alpha()
tooManyFriendsImage = pygame.image.load("images/tooManyFriends.png").convert_alpha()
noFriendshipFoundImage = pygame.image.load("images/noFriendshipFound.png").convert_alpha()
friendDeletedImage = pygame.image.load("images/friendDeleted.png").convert_alpha()
friendReqSentImage = pygame.image.load("images/friendReqSent.png").convert_alpha()
newHighscoreImage = pygame.image.load("images/newHighscore.png").convert_alpha()
nameSuccessfullyChangedImage = pygame.image.load("images/nameSuccessfullyChangedIMG.png").convert_alpha()
accountDeletedImage = pygame.image.load("images/accountDeletedIMG.png").convert_alpha()
# unknownErrorImage = pygame.image.load("images/unknownErrorImage.png").convert_alpha()

whiteCatImage = pygame.image.load("sprites/White/stand.png").convert_alpha()
calicoCatImage = pygame.image.load("sprites/Calico/stand.png").convert_alpha()
grayCatImage = pygame.image.load("sprites/Gray/stand.png").convert_alpha()
tortoiseCatImage = pygame.image.load("sprites/Tortoise/stand.png").convert_alpha()
blackCatImage = pygame.image.load("sprites/Black/stand.png").convert_alpha()

calicoCatLocked = pygame.image.load("sprites/Calico/calicoUnlock.png").convert_alpha()
grayCatLocked = pygame.image.load("sprites/Gray/grayUnlock.png").convert_alpha()
tortoiseCatLocked = pygame.image.load("sprites/Tortoise/tortoiseUnlock.png").convert_alpha()
blackCatLocked = pygame.image.load("sprites/Black/blackUnlock.png").convert_alpha()





# MAIN MENU BUTTONS
PlayButton = buttonClass.Button(203,108,PlayImage,1)
CustomizeButton = buttonClass.Button(120,278,CustomizeImage,1)
LeaderboardButton = buttonClass.Button(155,454,LeaderboardImage,1)
LoginButton = buttonClass.Button(750,15,LoginImage,1)
SignupButton = buttonClass.Button(1050,18,SignupImage,1.04)
AccountButton = buttonClass.Button(1050,18,accountImage,1.04)
FriendsButton = buttonClass.Button(750,15,FriendsImage,1)

# SIGNUP / LOGIN BUTTONS
BackwardButton = buttonClass.Button(40,850,BackwardImage,1.8)
EnterButton = buttonClass.Button(600,800,EnterImage,1)
loginUser = textBoxClass.textBox(310,300,TextboxImage,1.3,False)
loginPass = textBoxClass.textBox(310,590,TextboxImage,1.3,False)
signupUser = textBoxClass.textBox(310,300,TextboxImage,1.3,False)
signupPass = textBoxClass.textBox(310,590,TextboxImage,1.3,False)

# LEADERBOARD BUTTONS
leaderboardBackwardButton = buttonClass.Button(1250,20,BackwardImage,1.8)
userHighscore = textBoxClass.textBoxSolid(1040,720,'',2.5)

# CUSTOMIZE BUTTONS
customizeBackwardButton = buttonClass.Button(40,850,BackwardImage,1.8)
catSelectWhite = buttonClass.customizeButtons(160,192,whiteCatImage,whiteCatImage,8.5,0,True)
catSelectCalico = buttonClass.customizeButtons(565,192,calicoCatImage,calicoCatLocked,8.5,1,False)
catSelectGray = buttonClass.customizeButtons(1005,192,grayCatImage,grayCatLocked,8.5,2,False)
catSelectTortoise = buttonClass.customizeButtons(150,469,tortoiseCatImage,tortoiseCatLocked,8.5,3,False)
catSelectBlack = buttonClass.customizeButtons(565,469,blackCatImage,blackCatLocked,8.5,4,False)


customizeSelectList = [catSelectWhite,catSelectCalico,catSelectGray,catSelectTortoise,catSelectBlack]


# FRIEND BUTTONS

addUserBox = textBoxClass.textBox(695,505,friendTextboxImage,1.3,True)
removeUserBox = textBoxClass.textBox(985,280,friendTextboxImage,1.3,True)
requestsBox = textBoxClass.textBoxSolid(1016,675,"REQUEST",0.4,)
friendBackwardButton = buttonClass.Button(40,850,BackwardImage,1.8)
friendAcceptButton = buttonClass.Button(1004,753,friendAcceptImage,1)
friendDeclineButton = buttonClass.Button(1125,753,friendDeclineImage,1)
numOfFriends = textBoxClass.textBoxSolid(530,752,'0',0.4)
friendEnterButton = buttonClass.Button(985,445,friendEnterButtonImage,1)
# friendBackwardsButton = 

# ACCOUNT BUTTONS

accountBackwardsButton = buttonClass.Button(1225,40,BackwardImage,2)
accountDeleteButton = buttonClass.Button(146,620,accountDeleteButtonImage,1.05)
accountEnterButton = buttonClass.Button(1026,229,accountEnterButtonImage,1.05)
accountLogoutButton = buttonClass.Button(788,607,accountLogoutButtonImage,1.05)
accountNameTextbox = textBoxClass.textBox(96,235,accountTextboxImage,1,False)

# ERROR BUTTONS

noAccountFound = buttonClass.textButton(380,170,noAccountFoundImage,1)
incorrectPassword = buttonClass.textButton(380,170,incorrectPasswordImage,1)
unsecurePassword = buttonClass.textButton(380,170,unsecurePasswordImage,1)
accountAlreadyExists = buttonClass.textButton(380,170,accountAlreadyExistsImage,1)
usernameTooShort = buttonClass.textButton(380,170,usernameTooShortImage,1)
loginToPlay = buttonClass.textButton(650,200,loginToPlayImage,0.9)
loginToCustomize = buttonClass.textButton(650,200,loginToCustomizeImage,0.9)
friendsWithYourself = buttonClass.textButton(380,170,friendsWithYourselfImage,1)
requestAlreadySent = buttonClass.textButton(380,170,requestAlreadySentImage,1)
alreadyFriends = buttonClass.textButton(380,170,alreadyFriendsImage,1)
tooManyFriends = buttonClass.textButton(380,170,tooManyFriendsImage,1)
noFriendshipFound = buttonClass.textButton(380,170,noFriendshipFoundImage,1)
friendDeleted = buttonClass.textButton(380,170,friendDeletedImage,1)
friendReqSent = buttonClass.textButton(380,170,friendReqSentImage,1)
newHighscore = buttonClass.textButton(650,200,newHighscoreImage,1)
accountDeleted = buttonClass.textButton(380,170,accountDeletedImage,1)
nameChanged = buttonClass.textButton(380,170,nameSuccessfullyChangedImage,1)
# unknownError = buttonClass.textButton(380,170,unknownErrorImage,1)


errorList = [nameChanged,accountDeleted,noAccountFound, incorrectPassword, unsecurePassword, accountAlreadyExists, usernameTooShort, loginToPlay, loginToCustomize, friendsWithYourself, requestAlreadySent, alreadyFriends, tooManyFriends, noFriendshipFound,newHighscore,friendReqSent,friendDeleted]
#packages all possible errors into a list 

#subroutine which creates the objects for the on-screen scores and usernames on the leaderboard screen
def leaderboardItems():
	user1 = textBoxClass.textBoxSolid(200,250,'XXXX',0.7)
	user2 = textBoxClass.textBoxSolid(200,315,'XXXX',0.7)
	user3 = textBoxClass.textBoxSolid(200,380,'XXXX',0.7)
	user4 = textBoxClass.textBoxSolid(200,445,'XXXX',0.7)
	user5 = textBoxClass.textBoxSolid(200,510,'XXXX',0.7)
	user6 = textBoxClass.textBoxSolid(200,575,'XXXX',0.7)
	user7 = textBoxClass.textBoxSolid(200,640,'XXXX',0.7)
	user8 = textBoxClass.textBoxSolid(200,700,'XXXX',0.7)
	user9 = textBoxClass.textBoxSolid(200,765,'XXXX',0.7)
	user10 = textBoxClass.textBoxSolid(200,830,'XXXX',0.7)

	score1 = textBoxClass.textBoxSolid(700,250,'XXXX',0.7)
	score2 = textBoxClass.textBoxSolid(700,315,'XXXX',0.7)
	score3 = textBoxClass.textBoxSolid(700,380,'XXXX',0.7)
	score4 = textBoxClass.textBoxSolid(700,445,'XXXX',0.7)
	score5 = textBoxClass.textBoxSolid(700,510,'XXXX',0.7)
	score6 = textBoxClass.textBoxSolid(700,575,'XXXX',0.7)
	score7 = textBoxClass.textBoxSolid(700,640,'XXXX',0.7)
	score8 = textBoxClass.textBoxSolid(700,700,'XXXX',0.7)
	score9 = textBoxClass.textBoxSolid(700,765,'XXXX',0.7)
	score10 = textBoxClass.textBoxSolid(700,830,'XXXX',0.7)

	leaderboardUserText = [user1,user2,user3,user4,user5,user6,user7,user8,user9,user10]
	leaderboardScoreText = [score1,score2,score3,score4,score5,score6,score7,score8,score9,score10]

	return leaderboardUserText, leaderboardScoreText

#subroutine which creates the objects for the highscores, active colour and usernames on the friend list screen
def friendListItems():
	friendUser1 = textBoxClass.textBoxSolid(165,295,'',0.45)
	friendUser2 = textBoxClass.textBoxSolid(165,345,'',0.45)
	friendUser3 = textBoxClass.textBoxSolid(165,390,'',0.45)
	friendUser4 = textBoxClass.textBoxSolid(165,435,'',0.45)
	friendUser5 = textBoxClass.textBoxSolid(165,480,'',0.45)
	friendUser6 = textBoxClass.textBoxSolid(165,525,'',0.45)
	friendUser7 = textBoxClass.textBoxSolid(165,570,'',0.45)
	friendUser8 = textBoxClass.textBoxSolid(165,615,'',0.45)
	friendUser9 = textBoxClass.textBoxSolid(165,660,'',0.45)
	friendUser10 = textBoxClass.textBoxSolid(165,705,'',0.45)

	friendScore1 = textBoxClass.textBoxSolid(520,295,'',0.45)
	friendScore2 = textBoxClass.textBoxSolid(520,345,'',0.45)
	friendScore3 = textBoxClass.textBoxSolid(520,390,'',0.45)
	friendScore4 = textBoxClass.textBoxSolid(520,435,'',0.45)
	friendScore5 = textBoxClass.textBoxSolid(520,480,'',0.45)
	friendScore6 = textBoxClass.textBoxSolid(520,525,'',0.45)
	friendScore7 = textBoxClass.textBoxSolid(520,570,'',0.45)
	friendScore8 = textBoxClass.textBoxSolid(520,615,'',0.45)
	friendScore9 = textBoxClass.textBoxSolid(520,660,'',0.45)
	friendScore10 = textBoxClass.textBoxSolid(520,705,'',0.45)

	friendColour1 = catSprite.catSprite(380,290,2.75,"static",0,0)
	friendColour2 = catSprite.catSprite(380,340,2.75,"static",0,0)
	friendColour3 = catSprite.catSprite(380,385,2.75,"static",0,0)
	friendColour4 = catSprite.catSprite(380,430,2.75,"static",0,0)
	friendColour5 = catSprite.catSprite(380,475,2.75,"static",0,0)
	friendColour6 = catSprite.catSprite(380,520,2.75,"static",0,0)
	friendColour7 = catSprite.catSprite(380,565,2.75,"static",0,0)
	friendColour8 = catSprite.catSprite(380,610,2.75,"static",0,0)
	friendColour9 = catSprite.catSprite(380,655,2.75,"static",0,0)
	friendColour10 = catSprite.catSprite(380,700,2.75,"static",0,0)

	friendUserText = [friendUser1,friendUser2,friendUser3,friendUser4,friendUser5,friendUser6,friendUser7,friendUser8,friendUser9,friendUser10]
	friendScoreText = [friendScore1,friendScore2,friendScore3,friendScore4,friendScore5,friendScore6,friendScore7,friendScore8,friendScore9,friendScore10]
	friendColourText = [friendColour1,friendColour2,friendColour3,friendColour4,friendColour5,friendColour6,friendColour7,friendColour8,friendColour9,friendColour10]
	
	return friendUserText, friendScoreText, friendColourText

menuCat1 = catSprite.catSprite(0,720,13,"run",10,'random')
menuCat2 = catSprite.catSprite(450,720,13,"walk",5,'random')
menuCat3 = catSprite.catSprite(900,720,13,"walk",5,'random')
menuCat4 = catSprite.catSprite(1400,720,13,"walk",5,'random')


EMPTY_STRING = ""

skinList = ["White","Calico","Gray","Tortoise","Black"]


friendUserText, friendScoreText, friendColourText = friendListItems()

leaderboardUserText, leaderboardScoreText = leaderboardItems()

#loads objects and platforms from the gameStates file and packages them into lists
kitchenObj, kitchenPlat = gameStates.objectLoadKitchen()

bedroomObj, bedroomPlat = gameStates.objectLoadBedroom()

loungeObj, loungePlat = gameStates.objectLoadLounge()

bathroomObj, bathroomPlat = gameStates.objectLoadBathroom()

objList = [kitchenObj,loungeObj,bedroomObj,bathroomObj]
platList = [kitchenPlat,loungePlat,bedroomPlat,bathroomPlat]

gameStateList = ["kitchen","lounge","bedroom","bathroom"]

#creates objects of the cat sprite and the on-screen display of the uesr's active colour 
catAvatar = charClass.catChar(600,840,3,8)
currentAvatarDisplay = catSprite.catSprite(840,320,15,"idle",2,0)


#loads music and adjusts volume
menuMusic = "music/menuMusic.mp3"
gameMusic = "music/gameMusic.mp3"
pygame.mixer.music.load(menuMusic)
pygame.mixer.music.set_volume(0.25)

#creates cutscene  objects
gameLoad = cutScene.cutscene(0,0,78 ,'gameLoad',0.4,1)
gameOutro = cutScene.cutscene(0, 0, 36, 'outro', 0.25, 1)
gameIntro = cutScene.cutscene(0, 0, 48, 'intro', 0.4, 1)

cutSceneList = [gameOutro, gameIntro]

# ================================================================================
# ================================================================================
# ================================================================================


def gameReset(gameState):
	#this subroutine is called during the post-game handling. 
	#this resets every object so they are no longer broken in order to allow the user to play the game again.
	#additionally, the cat sprites location is returned to the kitchen.
	kitchenObj, kitchenPlat = gameStates.objectLoadKitchen()

	bedroomObj, bedroomPlat = gameStates.objectLoadBedroom()

	loungeObj, loungePlat = gameStates.objectLoadLounge()

	bathroomObj, bathroomPlat = gameStates.objectLoadBathroom()

	objList = [kitchenObj,loungeObj,bedroomObj,bathroomObj]
	platList = [kitchenPlat,loungePlat,bedroomPlat,bathroomPlat]

	gameState = "kitchen"
	catAvatar.rectX = 600 
	catAvatar.x = 600
	 

	return gameState, objList, platList 

def displayWindow(background,menu_state,loggedIn,accData):
	#changes the game's background'and loads the active colour display if user is logged in. 
		SCREEN.blit(background, (0,0))
		if loggedIn and menu_state == 'main' and gameOutro.onScreen == False:
			currentAvatarDisplay.colour = skinList[int(accData[4])]
			currentAvatarDisplay.draw(SCREEN)

def mainMenuDraw(event,mouse_pos,state_stack,loggedIn):
	#draws the buttons on the main menu and appends to the state stack if one is clicked.
	startTime = None 
	
	#iterates through the error list and displays any relevant on screen error messages.
	for error in errorList:
			if error.errorOn == True: 
				error.draw(SCREEN, event, mouse_pos)
				
	if PlayButton.draw(SCREEN,event,mouse_pos):
		if loggedIn:
			state_stack.append("play")
			startTime = pygame.time.get_ticks()
			gameIntro.onScreen = True 
			pygame.mixer.music.pause()
		else:
			loginToPlay.errorOn = True

	if CustomizeButton.draw(SCREEN,event,mouse_pos):
		if loggedIn:
			state_stack.append("customize")
		else:
			loginToCustomize.errorOn = True 

	if LeaderboardButton.draw(SCREEN,event,mouse_pos):
		state_stack.append("leaderboard")

	if not loggedIn:
		if LoginButton.draw(SCREEN,event,mouse_pos):
			state_stack.append("login")

		if SignupButton.draw(SCREEN,event,mouse_pos):
			state_stack.append("signup")
	else:
		if AccountButton.draw(SCREEN,event,mouse_pos):
			state_stack.append("account")

		if FriendsButton.draw(SCREEN,event,mouse_pos):
			state_stack.append("friends")

	#iterates through cutscene list and draws the images on screen
	for cutScene in cutSceneList:
		if cutScene.onScreen == True: 
			cutScene.play( SCREEN)
			background = introBackground

	return state_stack, startTime

def checkUnlocked(accData):
	#retrieves the highscore from the database and compares it to the constant scoreList in order
	#to see which variations the user is able to choose from 
	dataCursor.execute("SELECT highscore FROM accountData WHERE username = ?",[accData[1]])
	highscore = dataCursor.fetchone()
	highscore = int(highscore[0])

	scoreList = [200,500,750,1000]
	newSkinData = '1' 

	for score in scoreList:
		if highscore >= score:
			newSkinData += '1' 
		else:
			newSkinData += '0'


	dataCursor.execute("UPDATE accountData SET skinData = ? WHERE username = ?",(newSkinData,accData[1]))
	dataConnection.commit()

def unlockSkins(accData):
	#retrieves the skinData from accountData and unlocks relevant avatars.

	dataCursor.execute("SELECT skinData FROM accountData WHERE username = ?",[accData[1]])
	skinData = dataCursor.fetchone()
	skinData = skinData[0]

	for i in range(len(skinData)):
		
		if int(skinData[i]) == 1:	
			customizeSelectList[i].unlocked = True
		else:

			customizeSelectList[i].unlocked = False

def customizeCat(SCREEN,event,mouse_pos,state_stack,accData,loggedIn):
	#displays the buttons which allow the user to return to main menu or choose a different avatar
	if customizeBackwardButton.draw(SCREEN,event,mouse_pos):
		state_stack.pop()

	checkUnlocked(accData)

	unlockSkins(accData)



	for avatar in customizeSelectList:
		if avatar.draw(SCREEN,event,mouse_pos):
			dataCursor.execute("UPDATE accountData SET activeSkin = ? WHERE username = ?",(avatar.catId,accData[1]))
			dataConnection.commit()

			dataCursor.execute("SELECT * from accountData where username = ?",[accData[1]])
			accData = dataCursor.fetchone()
			


	return accData
		

def handleUserScore(SCREEN,highscore):
	#changes the scale/x coordinate of the user's personal highscore depending on the number of digits
	if int(highscore) < 10:
		userHighscore.x = 1120
	elif int(highscore) <100:
		userHighscore.x = 1080
	elif int(highscore) < 1000:
		userHighscore.x = 1035
	else:
		userHighscore.x = 1025
		userHighscore.scale = 2
	
	userHighscore.handleEvents(SCREEN,highscore)

def handleleaderboard(SCREEN,event,mouse_pos,state_stack,loggedIn,accData,keyPressed,):
	#checks if user is logged in, and if so runs necessary subroutines and code to display their highscore on screen
	#regardless if user is logged in, the top 10 highscores in the database will be fetched and displayed in descending order
	if loggedIn:

		dataCursor.execute("SELECT highscore FROM accountData WHERE username = ?",[accData[1]])
		score = dataCursor.fetchone()
		data = str(score[0])

		handleUserScore(SCREEN,data)

	dataCursor.execute("SELECT username, highscore FROM accountData ORDER BY highscore DESC")
	topTen = dataCursor.fetchmany(10)
	
	for i in range(len(topTen)):
		leaderboardUserText[i].handleEvents(SCREEN,str(topTen[i][0]))
		leaderboardScoreText[i].handleEvents(SCREEN,str(topTen[i][1]))
		print(topTen[i][0],topTen[i][1])
			

	if leaderboardBackwardButton.draw(SCREEN,event,mouse_pos):
		state_stack.pop()
	

def validSignup(SCREEN,userUsername,userPassword):
	#validates the username and password the user has entered to attempt to signup and returns a relevant error
	#message if necessary

	dataCursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE lower(username) = lower(?))", (userUsername,))
	result = dataCursor.fetchone()
	valid = result[0]

	if valid == 1:
		accountAlreadyExists.errorOn = True
	elif len(userUsername) <= 5:
		usernameTooShort.errorOn = True
		valid = 1	
	elif len(userPassword) < 7: 
		unsecurePassword.errorOn = True
		valid = 1
	elif userPassword.isalpha():
		unsecurePassword.errorOn = True
		valid = 1
	elif userPassword.isnumeric():
		unsecurePassword.errorOn = True
		valid = 1
		

	return valid

def signUpMenu(SCREEN,event,mouse_pos,state_stack,keyPressed,loggedIn):
	#draws textbox + buttons which allow user to enter username and password to signup

	userUsername = signupUser.handleEvents(SCREEN,event,keyPressed)
	userPassword = signupPass.handleEvents(SCREEN,event,keyPressed)

	#iterates through errorlist and displays any necessary errors
	for error in errorList:
		if error.errorOn == True: 
			error.draw(SCREEN, event, mouse_pos)

	if EnterButton.draw(SCREEN,event,mouse_pos):

		encodedPassword = hashlib.sha256(userPassword.encode()).hexdigest()
		

		valid = validSignup(SCREEN,userUsername,userPassword)

		if valid == 0:
			#if username and password are validated, then new records are made in accountData and accounts
			dataCursor.execute("INSERT INTO accounts (id, username,password) VALUES (NULL, ?,?)",(userUsername,encodedPassword))	
			dataConnection.commit()

			dataCursor.execute("INSERT INTO accountData (id, username,highScore,skinData,activeSkin) VALUES (NULL, ?,?,?,?)",(userUsername,'0','00000','0'))
			dataConnection.commit()

			loggedIn = True 
			signupUser.reset()
			signupPass.reset()
		
		
		
	#resets username and password textbox if user goes back
	if BackwardButton.draw(SCREEN,event,mouse_pos):
		signupUser.reset()
		signupPass.reset()
		state_stack.pop() 

	if loggedIn:
		state_stack.pop()
		return userUsername, loggedIn, state_stack
	else:
		return EMPTY_STRING, loggedIn, state_stack

def validLogin(userUsername,userPassword,SCREEN,event,mouse_pos):
	#validates the username and password the user has entered to attempt to login and returns a relevant error
	#message if necessary
	dataCursor.execute("SELECT EXISTS(SELECT id FROM accounts WHERE username = ?)", (userUsername,))
	result = dataCursor.fetchone()
	
	if result[0] == 0:
			noAccountFound.errorOn = True
	else:
		encodedPassword = hashlib.sha256(userPassword.encode()).hexdigest()

		dataCursor.execute("SELECT password from accounts where username = ?",[userUsername])
		accountPassword = dataCursor.fetchone()

		if encodedPassword == accountPassword[0]:
			return True
		else:			
			incorrectPassword.errorOn = True

def loginMenu(SCREEN,event,mouse_pos,state_stack,keyPressed,loggedIn):
	#draws textbox + buttons which allow user to enter username and password to login
	userUsername = loginUser.handleEvents(SCREEN,event,keyPressed)
	userPassword = loginPass.handleEvents(SCREEN,event,keyPressed)

	#iterates through errorlist and displays any necessary errors
	for error in errorList:
		if error.errorOn == True: 
			error.draw(SCREEN, event, mouse_pos)

	if EnterButton.draw(SCREEN,event,mouse_pos):
		
		if validLogin(userUsername,userPassword,SCREEN,event,mouse_pos):
			#if details are validated, then login is set to true and the username is returned for the 
			#program to load the details.
			loggedIn = True 
			username, password = EMPTY_STRING, EMPTY_STRING
			state_stack.pop()
			loginUser.reset()
			loginPass.reset()
		else:
			loggedIn = False

	if BackwardButton.draw(SCREEN,event,mouse_pos):
		loginUser.reset()
		loginPass.reset()
		state_stack.pop()

	
	if loggedIn:
		return userUsername, loggedIn, state_stack
	else:
		return EMPTY_STRING, loggedIn, state_stack



def checkRequestValidity(requestingUser,targetUser):
	#validates the friend request attempt:
	#makes sure user exists, they are not already friends, no request already exists etc. 

	requestingID = EMPTY_STRING
	targetID = EMPTY_STRING
	error = False

	if requestingUser == targetUser:
		friendsWithYourself.errorOn = True
		error = True 
	else:
		dataCursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ?)", (targetUser,))
		existsResults = dataCursor.fetchone()
		exists = existsResults[0]

		if exists == 0:
			noAccountFound.errorOn = True
			error = True 

		else:

			dataCursor.execute("SELECT id FROM accountData WHERE username = ?",[requestingUser])
			requestingID = dataCursor.fetchone()

			dataCursor.execute("SELECT id FROM accountData WHERE username = ?",[targetUser])
			targetID = dataCursor.fetchone()
			
			
			requestingID = int(requestingID[0])
			targetID = int(targetID[0])
			

			dataCursor.execute("SELECT EXISTS(SELECT 1 FROM friendRequests WHERE requestingUserID = ? and targetUserID = ?)", (requestingID,targetID))
			existsResults = dataCursor.fetchall()
			exists = existsResults[0][0]
			
			if exists == 1:
				requestAlreadySent.errorOn = True
				error = True 
			else:
				dataCursor.execute("SELECT EXISTS(SELECT 1 FROM friendList WHERE user1ID = ? and user2ID = ?)", (requestingID,targetID))
				existsResults = dataCursor.fetchone()
				exists = existsResults[0]

				if exists == 1:
					alreadyFriends.errorOn = True
					error = True 

	return error, targetID, requestingID

def sendRequests(targetUser,accData,friendUserList):
	#after validating the request, the program will create a new record in the friendRequests table
	try:
		requestingUser = accData[1]
			
		error, targetID, requestingID = checkRequestValidity(requestingUser,targetUser)
		
		if error == False: 
			
			if len(friendUserList) == 10:
				tooManyFriends.errorOn = True
			else:
				dataCursor.execute("INSERT INTO friendRequests (requestingUserID, targetUserID) VALUES (?,?)",(requestingID,targetID))
				friendReqSent.errorOn = True
				dataConnection.commit()
	except:
		unknownError.errorOn = True 
		

def receiveRequests(accData,event,mouse_pos,friendUserList):
	#fetches any pending friend requests for the logged in user and displays them one-by-one 
	#on screen to allow the user to accept or decline

	requestsList = []
	userID = accData[0]

	dataCursor.execute("SELECT requestingUserID FROM friendRequests WHERE targetUserID = ?", [userID])
	IDList = dataCursor.fetchall()
	
	if len(IDList) != 0:
		avaliableRequests = True 
		for i in range(len(IDList)):
			dataCursor.execute("SELECT username FROM accountData WHERE id = ?", IDList[i])
			requestUsername = dataCursor.fetchone()		
			requestsList.append(requestUsername[0])
	
		for i in range(len(requestsList)):		
			requestsBox.handleEvents(SCREEN,requestsList[-1])
	else:
		avaliableRequests = False

	if friendAcceptButton.draw(SCREEN,event,mouse_pos) and avaliableRequests:
	#if user accepts the friend request, the request record is deleted and a new record is made in friendList with the relevant IDs	
		if len(friendUserList) >= 10:
			tooManyFriends.errorOn = True 

		else:
			requestedID = int(IDList[-1][0])

			dataCursor.execute("INSERT INTO friendList (friendshipID, user1ID,user2ID) VALUES (NULL,?,?)",(int(userID),requestedID))
			IDList.pop()
			requestsList.pop()
			dataCursor.execute("DELETE FROM friendRequests WHERE requestingUserID = ? and targetUserID = ?", (requestedID, userID))
			dataConnection.commit()

			# dataCursor.execute("SELECT * FROM friendList")
			# aaaa = dataCursor.fetchall()
			# print(aaaa)



	if friendDeclineButton.draw(SCREEN,event,mouse_pos) and avaliableRequests:
	#if user declines the friend request, the request record is deleted and the ID/Request lists are popped with no further action.
		requestedID = int(IDList[-1][0])
		dataCursor.execute("DELETE FROM friendRequests WHERE requestingUserID = ? and targetUserID = ?", (requestedID, userID))
		IDList.pop()
		requestsList.pop()
		dataConnection.commit()

def checkDeletionValidity(targetUser, accData):
	#attempts to fetch the id linked with the input username from the database. If no such username exists then this ‘None’
	#is returned to the deleteUser() subroutine where appropriate error messages occur.

	dataCursor.execute("SELECT id FROM accountData WHERE username = ?", [targetUser])
	deletingID = dataCursor.fetchone()

	if deletingID != None:
		deletingID = deletingID[0]
		
	
	userID = accData[0]

	return deletingID, userID

def getFriendshipID(deletingID,userID): 
	# finds the friendshipID of the friendship between the user and the targetUser 
	#in order to return it to the deleteUser() subroutine so the correct record is deleted. 
	dataCursor.execute("SELECT friendshipID FROM friendList WHERE user1ID = ? and user2ID = ?", (userID,deletingID))
	friendshipID1 = dataCursor.fetchone()

	dataCursor.execute("SELECT friendshipID FROM friendList WHERE user1ID = ? and user2ID = ?", (deletingID,userID))
	friendshipID2 = dataCursor.fetchone()	

	if friendshipID2 == friendshipID1:
		noFriendshipFound.errorOn = True
		
		return None
	else:
		
		if friendshipID1 == None:
			return friendshipID2
		else:
			return friendshipID1

def deleteUser(targetUser, accData):
	#takes the input of the user and validates the target, then calls the subroutine to retrieve the ID of the 
	#record relating to the friendship between the two users in order to delete it. 
	try:
		error = EMPTY_STRING
		friendshipID = EMPTY_STRING
		deletingID = EMPTY_STRING
		
		deletingID, userID = checkDeletionValidity(targetUser,accData)

		if deletingID == None:
			noAccountFound.errorOn = True
		else:
			friendshipID = getFriendshipID(deletingID,userID)
			
			if friendshipID != None:
				
				friendshipID = friendshipID[0]
				dataCursor.execute("DELETE FROM friendList WHERE friendshipID = ?", [friendshipID])
				dataConnection.commit()
				friendDeleted.errorOn = True
				
	except:
		unknownError.errorOn = True 
		pass
				
def displayFriends(accData,friendUserList,friendHighscoreList,friendActiveCat):
	#iterates through the friends the user has and updates the on-screen objects in order for them to 
	#correctly display the friend’s usernames, highscores and active colours.
	friendUserText, friendScoreText, friendColourText = friendListItems()
	
	friendAmount = str(len(friendUserList))
	
	for i in range(len(friendUserList)):

		friendColourText[i].colour = skinList[int(friendActiveCat[i][0])]
		friendUserText[i].handleEvents(SCREEN,str(friendUserList[i][0]))
		friendScoreText[i].handleEvents(SCREEN,str(friendHighscoreList[i]))
		friendColourText[i].draw(SCREEN)

	numOfFriends.handleEvents(SCREEN,friendAmount)

def getHighscoreList(friendUserList):
	#Uses the list of friend’s usernames to fetch the highscore and append them to a list and then return this list.

	friendHighscoreList = []

	for i in range (len(friendUserList)):
		dataCursor.execute("SELECT highscore FROM accountData WHERE username = ?",[friendUserList[i][0]])
		highscore = dataCursor.fetchone()
		friendHighscoreList.append(highscore[0])

	return friendHighscoreList

def getUsernameList(accData):
	#Fetches the userIDs of the individuals that the user is friends with, then uses these IDs to create a list of usernames. 
	userID = accData[0]

	friendIdList = []
	friendUserList = []
	

	dataCursor.execute("SELECT user1ID from friendList where user2ID = ?", [userID])
	friendID1 = dataCursor.fetchall()
	dataCursor.execute("SELECT user2ID from friendList where user1ID = ?", [userID]) 
	friendID2 = dataCursor.fetchall()



	if len(friendID1) != 0:
		for friendID in friendID1:
			dataCursor.execute("SELECT username from accountData where id = ?",[friendID[0]])
			friendUserList.append(dataCursor.fetchone())

	if len(friendID2) != 0:
		for friendID in friendID2:
			dataCursor.execute("SELECT username from accountData where id = ?",[friendID[0]])
			friendUserList.append(dataCursor.fetchone())

	return friendUserList

def getActiveColour(friendUserList):
	#Gets the index of the colour avatar that each friend is currently using and appends it to a list.
	friendActiveCat = []

	for i in range (len(friendUserList)):
		dataCursor.execute("SELECT activeSkin from accountData where username = ?",[friendUserList[i][0]])
		colour = dataCursor.fetchone()
		friendActiveCat.append(colour)

	return friendActiveCat

def getFriendlistData(accData):
	#Calls subroutines to fetch active colour, usernames, and highscores.

	friendUserList = getUsernameList(accData)

	friendHighscoreList = getHighscoreList(friendUserList)

	friendActiveCat = getActiveColour(friendUserList)
	
	return friendUserList, friendHighscoreList, friendActiveCat

def friendScreen(SCREEN,event,mouse_pos,state_stack,accData,keyPressed,):
	#Draws relevant objects which allows user to delete existing friends or add new ones. 
	targetUser = addUserBox.handleEvents(SCREEN,event,keyPressed)
	deletedUser = removeUserBox.handleEvents(SCREEN,event,keyPressed)

	if friendBackwardButton.draw(SCREEN,event,mouse_pos):
		addUserBox.reset()
		removeUserBox.reset()
		state_stack.pop()

	#Calls subroutines which retrieve the user’s friend’s data aswell as displaying this data on screen. 
	friendUserList, friendHighscoreList, friendActiveCat = getFriendlistData(accData)

	receiveRequests(accData,event,mouse_pos,friendUserList)
	displayFriends(accData,friendUserList,friendHighscoreList,friendActiveCat)
	
	#iterates through errorlist and displays any necessary errors
	for error in errorList:
		if error.errorOn == True: 
			error.draw(SCREEN, event, mouse_pos)


	if friendEnterButton.draw(SCREEN,event,mouse_pos):
		
		if targetUser != EMPTY_STRING:
			sendRequests(targetUser, accData,friendUserList)
		if deletedUser != EMPTY_STRING:
			deleteUser(deletedUser,accData)

	if not addUserBox.active:
		addUserBox.reset()
	if not removeUserBox.active:
		removeUserBox.reset()

def handleKitchen(gameState,catAvatar):
	#Checks the x coordinate of the user’s sprite and changes the room depending on if the cat moves between them. 
	#Checks for any object points that need to be added to the user’s total.

	if catAvatar.x + 20 >= 1430:
		gameState = gameStateList[1]
		catAvatar.rectX = -80
		catAvatar.x = -80

	if catAvatar.x <= -81:
		gameState = gameStateList[3]
		catAvatar.rectX = 1400
		catAvatar.x = 1400

	return gameState 

def handleLounge(gameState,catAvatar):
	if catAvatar.x + 20 >= 1430:
		gameState = gameStateList[2]
		catAvatar.rectX = -80
		catAvatar.x = -80

	if catAvatar.x <= -81:
		gameState = gameStateList[0]
		catAvatar.rectX = 1400
		catAvatar.x = 1400

			
	return gameState

def handleBedroom(gameState,catAvatar):
	if catAvatar.x <= -81:
		gameState = gameStateList[1]
		catAvatar.rectX = 1400
		catAvatar.x = 1400

	if catAvatar.x + 20 >= 1430:
		gameState = gameStateList[3]
		catAvatar.rectX = -80
		catAvatar.x = -80 

	return gameState

def handleBathroom(gameState,catAvatar):
		if catAvatar.x <= -81:
			gameState = gameStateList[2]
			catAvatar.rectX = 1400
			catAvatar.x = 1400

		if catAvatar.x + 20 >= 1430:
			gameState = gameStateList[0]
			catAvatar.rectX = -80
			catAvatar.x = -80

		return gameState

def playGame(gameState, SCREEN, event, catAvatar, objList, platList,startTime):
	seconds = (pygame.time.get_ticks() - startTime) / 1000 
	#Calcuates the number of seconds that have passed since game begun.
	#Uses selection to run appropriate subroutines based on which room the cat is in. 
	if gameState == "kitchen":
		background = gameStates.kitchen(SCREEN,event,catAvatar,objList[0],platList[0])
		
		gameState =	handleKitchen(gameState,catAvatar)

	elif gameState == "lounge":

		background = gameStates.lounge(SCREEN,event,catAvatar,objList[1],platList[1])
		gameState = handleLounge(gameState,catAvatar)
		
	elif gameState == "bedroom":
		background = gameStates.bedroom(SCREEN,event,catAvatar,objList[2],platList[2])
		gameState = handleBedroom(gameState,catAvatar)
	
	
	elif gameState == "bathroom":

		background = gameStates.bathroom(SCREEN,event,catAvatar,objList[3],platList[3])
		gameState = handleBathroom(gameState,catAvatar)
	else:
		background = MainBackground
	
	return gameState, background, seconds
	
def postGame(seconds, state_stack, accData,gameState,objList,platList,catAvatar):
	#Only runs postgame if timer is up. 23 seconds is used because the intro of the game is 3 seconds long.
	if seconds > 23:
		#Stops the game music and loads and plays the menu music.
		pygame.mixer.music.stop()
		pygame.mixer.music.load(menuMusic)
		pygame.mixer.music.set_volume(0.25)
		pygame.mixer.music.play()

		#Runs the game outro and pops the state_stack in order to return the program back to the main menu
		gameOutro.onScreen = True
		state_stack.pop()
		
		#Resets the game’s objects so the user is able to play again.
		gameState, objList, platList = gameReset(gameState)

		#Compares the user’s score with their existing highscore and updates highscore if necessary.
		if catAvatar.POINTS > int(accData[2]):
			dataCursor.execute("UPDATE accountData SET highscore = ?  WHERE username = ?",(catAvatar.POINTS, accData[1]))
			dataConnection.commit()
			newHighscore.errorOn = True
		
		catAvatar = charClass.catChar(600,840,int(accData[4]),8)

	return state_stack, gameState, objList, platList, catAvatar

def handleIntro(SCREEN):
	#Runs game intro cutscene and updates the background to the intro background
	gameIntro.play(SCREEN) 
	background = introBackground

	return background

def handleOutro(SCREEN):
	#Runs game outro cutscene and if appropriate, displays a ‘New Highscore’ message on screen
	gameOutro.play(SCREEN)
	if newHighscore.errorOn == True: 
		SCREEN.blit(newHighscoreImage,(650,200)) 

	return outroBackground

def checkNameValid(username):
	#verifies whether or not the username which the user wants to change their username to already exists or is too short
	if len(username) <= 5:
		usernameTooShort.errorOn = True	
		return False 

	else:
		dataCursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ?)", (username,))
		result = dataCursor.fetchone()
		valid = result[0]
		if valid == 1:
			accountAlreadyExists.errorOn = True	
			return False
		else:
			return True



def changeName(username, accData):
	#updates the username of the user in accounts and account data and refreshes the accData variable
	userID = accData[0]

	dataCursor.execute("UPDATE accountData SET username = ? WHERE id = ?",(username, userID))
	dataCursor.execute("UPDATE accounts SET username = ? WHERE id = ?",(username, userID))
	dataConnection.commit()

	dataCursor.execute("SELECT * FROM accountData WHERE username = ?",(str(username),))
	accData = dataCursor.fetchone()
	return accData


def deleteFriends(accData):
	#deletes any pending friend requests or friend connections between the user. 
	userID = accData[0]

	dataCursor.execute("DELETE FROM friendList WHERE user1ID = ? or user2ID = ?",(userID,userID,))
	dataCursor.execute("DELETE FROM friendRequests WHERE targetUserID = ? or requestingUserID = ?",(userID,userID,))
	dataConnection.commit()

def deleteAccount(accData):
	#deletes records from accountData and accounts
	userID = accData[0]

	dataCursor.execute("DELETE FROM accountData WHERE id = ?",(userID,))
	dataCursor.execute("DELETE FROM accounts WHERE id = ?",(userID,))
	dataConnection.commit()

def accountScreen(SCREEN,event,mouse_pos,state_stack,accData,keyPressed,loggedIn):
	#draws any on screen buttons/textboxes for the user to interact with
	#calls relevant validation subroutines
	username = accountNameTextbox.handleEvents(SCREEN,event,keyPressed)
	if accountBackwardsButton.draw(SCREEN,event,mouse_pos):
		state_stack.pop()
		accountNameTextbox.reset()

	if accountLogoutButton.draw(SCREEN,event,mouse_pos):
		state_stack.pop()
		accData = []
		loggedIn = False
		accountNameTextbox.reset()

	if accountDeleteButton.draw(SCREEN,event,mouse_pos):
		deleteFriends(accData)
		deleteAccount(accData)
		state_stack.pop()
		accData = []
		loggedIn = False
		accountNameTextbox.reset()
		accountDeleted.errorOn = True 
		

	if accountEnterButton.draw(SCREEN,event,mouse_pos):
		valid = checkNameValid(username)
		if valid:
			accData = changeName(username,accData)
			nameChanged.errorOn = True

	#iterates through errorlist and displays any necessary errors
	for error in errorList:
			if error.errorOn == True: 
				error.draw(SCREEN, event, mouse_pos)

	return state_stack, accData, loggedIn

def main():

	run = True
	objList = [kitchenObj,loungeObj,bedroomObj,bathroomObj]
	platList = [kitchenPlat,loungePlat,bedroomPlat,bathroomPlat]

	#Plays music indefinitely
	pygame.mixer.music.play(-1)
	
	#Sets background to the main menu aswell as initlalisizng variables like menu_state.
	background = MainBackground
	state_stack = ["main"]
	gameState = gameStateList[0]
	menu_state = state_stack[-1]
	
	loggedIn = False 
	#Logged in is automatically set to false, with account+accData being empty
	account = EMPTY_STRING
	accData = EMPTY_STRING

	startTime = 0

	keyPressed = EMPTY_STRING
	#Runs displayWindow subroutine to update the program background.
	displayWindow(background,menu_state,loggedIn,accData)

	#Turns on the game-load cutscene. 
	gameLoad.onScreen = True 

	while run:

		
		
		menu_state = state_stack[-1]

		displayWindow(background,menu_state,loggedIn,accData)


		events = pygame.event.get()

		for event in events:
			#Checks for events like the user quitting or typing.
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				keyPressed = event.unicode
				
			
				
				

		mouse_pos = pygame.mouse.get_pos()
		#Gets mouse position in order to check for any button-pressing
		
	
		#Uses iteration to run different code depending on whether the user clicks on the login screen, signup, customize etc.
		if menu_state == "main" and gameOutro.onScreen == False:
			
			if loggedIn:
				background = MainBackground2
				
			else:
				background = MainBackground

			pygame.mouse.set_visible(True)

			menuCat1.draw(SCREEN)
			menuCat2.draw(SCREEN)
			menuCat3.draw(SCREEN)
			menuCat4.draw(SCREEN)
				
		
			state_stack,startTime = mainMenuDraw(event,mouse_pos,state_stack,loggedIn)
		
		if menu_state == "login":
			background = LoginBackground

			account, loggedIn, state_stack = loginMenu(SCREEN,event,mouse_pos,state_stack,keyPressed,loggedIn)
			
			if loggedIn:
				dataCursor.execute("SELECT * from accountData where username = ?",[account])
				accData = dataCursor.fetchone()
				
				catAvatar = charClass.catChar(600,840,int(accData[4]),8)
				currentAvatarDisplay = catSprite.catSprite(840,320,15,"idle",0,int(accData[4]))

		if menu_state == "signup":
			background = SignupBackground
			account, loggedIn, state_stack = signUpMenu(SCREEN,event,mouse_pos,state_stack,keyPressed, loggedIn)
			
			if loggedIn:
				dataCursor.execute("SELECT * from accountData where username = ?",[account])
				accData = dataCursor.fetchone()
				


		if menu_state == "leaderboard":
			background = leaderboardBackground
			handleleaderboard(SCREEN,event,mouse_pos,state_stack,loggedIn,accData,keyPressed,)
		
		if menu_state == "customize":
			accData = customizeCat(SCREEN,event,mouse_pos,state_stack,accData,loggedIn)
			background = customizeBackground
			#catAvatar.changeColour(int(accData[4])) 
			
		if menu_state == "play":

	
			#Checks if user is logged in- if not then the game is not run. 
			if loggedIn:

				if not pygame.mixer.music.get_busy():
					pygame.mixer.music.load(gameMusic)
					pygame.mixer.music.set_volume(0.15)
					pygame.mixer.music.play(0)
					#The game musici s loaded and played and when the gameIntro is finished running, 
					#the playGame() and postGame() subroutines are called. 


				if gameIntro.onScreen == False:


					gameState, background, seconds = playGame(gameState, SCREEN, event, catAvatar, objList, platList,startTime)
					print(gameState)
					state_stack, gameState, objList, platList, catAvatar  = postGame(seconds, state_stack, accData, gameState, objList, platList, catAvatar)
						

				else:
				 	background = handleIntro(SCREEN)

				 	
				
			else:

				pygame.mixer.music.unpause()
				state_stack.pop()
		
		if menu_state == "friends":
			background = FriendBackground
			friendScreen(SCREEN,event,mouse_pos,state_stack,accData,keyPressed)

		if menu_state == "account":
			background = AccountBackground
			state_stack, accData, loggedIn = accountScreen(SCREEN,event,mouse_pos,state_stack,accData,keyPressed, loggedIn)
			
			
		if gameOutro.onScreen == True:
			background = handleOutro(SCREEN)
				
		if gameLoad.onScreen == True:
			gameLoad.play(SCREEN)
			

		pygame.display.update()
		event = blankEvent
		keyPressed = EMPTY_STRING




main()


dataConnection.close()
