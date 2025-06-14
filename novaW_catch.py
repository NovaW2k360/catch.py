#Nova Winston
#CS120
#June 13,2025
#Slide and catch

import pygame, simpleGE, random

class Cat(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("cat.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 8
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed

class Fish(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("fish_blue.png")
        self.setSize(25, 25)
        self.minSpeed = 5
        self.maxSpeed = 12
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        self.bgColor = "lightsteelblue"
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 20"
        self.center = (500, 30)
        self.bgColor = "lightsteelblue"
    
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("cloud_bkg.png")
        self.sound = pygame.mixer.Sound("Cat Song 1.0.wav")
        pygame.mixer.music.load("Cat Song 1.0.wav")
        pygame.mixer.music.play()
        
        
        self.sndFish = simpleGE.Sound("meowing_cat.mp3")
        pygame.mixer.music.play()
        self.numFish = 10
        self.score = 0
        self.lblScore = LblScore()

        self.timer = simpleGE.Timer()
        self.timer.totalTime = 20
        self.lblTime = LblTime()
        
        self.cat = Cat(self)
        
        self.fish = []
        for i in range(self.numFish):
            self.fish.append(Fish(self))
            
        self.sprites = [self.cat, 
                        self.fish,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for fish in self.fish:        
            if fish.collidesWith(self.cat):
                fish.reset()
                self.sndFish.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()

        self.prevScore = prevScore

        self.setImage("cloud_bkg.png")
        self.response = "Quit"
        
        
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
        "You're a very hungry kitty!", 
        "Move left and right on the keyboard to move",
        "Catch the fishes!",
        ]
        self.instructions.bgColor = "aliceblue"
        
        self.instructions.center = (320, 200)
        self.instructions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        self.btnPlay.bgColor = "aliceblue"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        self.btnQuit.bgColor = "aliceblue"
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        self.lblScore.bgColor = "lightsteelblue"
        
        
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.bgColor = "lightsteelblue"

        
        self.sprites = [self.instructions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()


def main():
    
    keepGoing = True
    lastScore = 0

    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        
        if instructions.response == "Play":    
            game = Game()
            game.start()
            lastScore = game.score
            
        else:
            keepGoing = False
            
if __name__ == "__main__":
    main()