import argparse
import pygame
import copy
import random
from random import randrange
import math
import time
import threading
from Pacman import *
from BoardGame import *
from Agent import *
import utils

teams = {
        "Random Team": [
                RandomAgent(board_manager, 0),
                RandomAgent(board_manager, 1),
                RandomAgent(board_manager, 2),
                RandomAgent(board_manager, 3),
        ],

        "Greedy Team": [
                GreedyAgent(board_manager, 0),
                GreedyAgent(board_manager, 1),
                GreedyAgent(board_manager, 2),
                GreedyAgent(board_manager, 3),
        ],

        "Greedy Team w/ Social Convention": [
                ConventionAgent(board_manager, 0, CONVENTIONS),
                ConventionAgent(board_manager, 1, CONVENTIONS),
                ConventionAgent(board_manager, 2, CONVENTIONS),
                ConventionAgent(board_manager, 3, CONVENTIONS),
        ],

        "Greedy Team w/ Roles": [
                RoleAgent(board_manager, 0, ROLES),
                RoleAgent(board_manager, 1, ROLES),
                RoleAgent(board_manager, 2, ROLES),
                RoleAgent(board_manager, 3, ROLES),
        ],

    }

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

def displayLaunchScreen():
    # Draw Pacman Title
    pacmanTitle = ["tile016.png", "tile000.png", "tile448.png", "tile012.png", "tile000.png", "tile013.png"]
    for i in range(len(pacmanTitle)):
        letter = pygame.image.load(TextPath + pacmanTitle[i])
        letter = pygame.transform.scale(letter, (int(square * 4), int(square * 4)))
        screen.blit(letter, ((2 + 4 * i) * square, 2 * square, square, square))

    # Draw Character / Nickname
    characterTitle = [
        #Character
        "tile002.png", "tile007.png", "tile000.png", "tile018.png", "tile000.png", "tile002.png", "tile020.png", "tile004.png", "tile018.png",
        # /
        "tile015.png", "tile042.png", "tile015.png",
        # Nickname
        "tile013.png", "tile008.png", "tile002.png", "tile010.png", "tile013.png", "tile000.png", "tile012.png", "tile004.png"
    ]
    for i in range(len(characterTitle)):
        letter = pygame.image.load(TextPath + characterTitle[i])
        letter = pygame.transform.scale(letter, (int(square), int(square)))
        screen.blit(letter, ((4 + i) * square, 10 * square, square, square))

    #Draw Characters and their Nickname
    characters = [
        # Red Ghost
        [
            "tile449.png", "tile015.png", "tile107.png", "tile015.png", "tile083.png", "tile071.png", "tile064.png", "tile067.png", "tile078.png", "tile087.png",
            "tile015.png", "tile015.png", "tile015.png", "tile015.png",
            "tile108.png", "tile065.png", "tile075.png", "tile072.png", "tile077.png", "tile074.png", "tile089.png", "tile108.png"
        ],
        # Pink Ghost
        [
            "tile450.png", "tile015.png", "tile363.png", "tile015.png", "tile339.png", "tile336.png", "tile324.png", "tile324.png", "tile323.png", "tile345.png",
            "tile015.png", "tile015.png", "tile015.png", "tile015.png",
            "tile364.png", "tile336.png", "tile328.png", "tile333.png", "tile330.png", "tile345.png", "tile364.png"
        ],
        # Blue Ghost
        [
            "tile452.png", "tile015.png", "tile363.png", "tile015.png", "tile193.png", "tile192.png", "tile211.png", "tile199.png", "tile197.png", "tile213.png", "tile203.png",
            "tile015.png", "tile015.png", "tile015.png",
            "tile236.png", "tile200.png", "tile205.png", "tile202.png", "tile217.png", "tile236.png"
        ],
        # Orange Ghost
        [
            "tile451.png", "tile015.png", "tile363.png", "tile015.png", "tile272.png", "tile270.png", "tile266.png", "tile260.png", "tile281.png",
            "tile015.png", "tile015.png", "tile015.png", "tile015.png", "tile015.png",
            "tile300.png", "tile258.png", "tile267.png", "tile281.png", "tile259.png", "tile260.png", "tile300.png"
        ]
    ]
    for i in range(len(characters)):
        for j in range(len(characters[i])):
            if j == 0:
                    letter = pygame.image.load(TextPath + characters[i][j])
                    letter = pygame.transform.scale(letter, (int(square * spriteRatio), int(square * spriteRatio)))
                    screen.blit(letter, ((2 + j) * square - square//2, (12 + 2 * i) * square - square//3, square, square))
            else:
                letter = pygame.image.load(TextPath + characters[i][j])
                letter = pygame.transform.scale(letter, (int(square), int(square)))
                screen.blit(letter, ((2 + j) * square, (12 + 2 * i) * square, square, square))
    # Draw Pacman and Ghosts
    event = ["tile449.png", "tile015.png", "tile452.png", "tile015.png",  "tile015.png", "tile448.png", "tile453.png", "tile015.png", "tile015.png", "tile015.png",  "tile453.png"]
    for i in range(len(event)):
        character = pygame.image.load(TextPath + event[i])
        character = pygame.transform.scale(character, (int(square * 2), int(square * 2)))
        screen.blit(character, ((4 + i * 2) * square, 24 * square, square, square))
    # Draw PlatForm from Pacman and Ghosts
    wall = ["tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png", "tile454.png"]
    for i in range(len(wall)):
        platform = pygame.image.load(TextPath + wall[i])
        platform = pygame.transform.scale(platform, (int(square * 2), int(square * 2)))
        screen.blit(platform, ((i * 2) * square, 26 * square, square, square))
    # Credit myself
    credit = ["tile003.png", "tile004.png", "tile022.png", "tile008.png", "tile013.png", "tile015.png", "tile011.png", "tile004.png", "tile000.png", "tile012.png", "tile025.png", "tile015.png", "tile418.png", "tile416.png", "tile418.png", "tile416.png"]
    for i in range(len(credit)):
        letter = pygame.image.load(TextPath + credit[i])
        letter = pygame.transform.scale(letter, (int(square), int(square)))
        screen.blit(letter, ((6 + i) * square, 30 * square, square, square))
    # Press Space to Play
    instructions = ["tile016.png", "tile018.png", "tile004.png", "tile019.png", "tile019.png", "tile015.png", "tile019.png", "tile016.png", "tile000.png", "tile002.png", "tile004.png", "tile015.png", "tile020.png", "tile014.png", "tile015.png", "tile016.png", "tile011.png", "tile000.png", "tile025.png"]
    for i in range(len(instructions)):
        letter = pygame.image.load(TextPath + instructions[i])
        letter = pygame.transform.scale(letter, (int(square), int(square)))
        screen.blit(letter, ((4.5 + i) * square, 35 * square - 10, square, square))

    pygame.display.update()

def pause(time):
    cur = 0
    while not cur == time:
        cur += 1

# Reset after death
def reset(board_manager):
    global game
    game.ghosts = CreateGhosts(game.team)
    #game.getObservations()
    for ghost in game.ghosts:
        ghost.setTarget()
    game.pacman = Pacman(board_manager, 26.0, 13.5)
    game.lives -= 1
    game.paused = True
    game.render()

class Game:
    def __init__(self, board_manager, level, score, team: str = 'Random Team'):
        self.team = team
        self.board_manager = board_manager
        self.paused = True
        self.ghostUpdateDelay = 1
        self.ghostUpdateCount = 0
        self.pacmanUpdateDelay = 1
        self.pacmanUpdateCount = 0
        self.tictakChangeDelay = 10
        self.tictakChangeCount = 0
        self.ghostsAttacked = False
        self.highScore = self.getHighScore()
        self.score = score
        self.level = level
        self.lives = 1
        self.ghostDeaths = 0
        self.pacmanVictories = 0
        self.pacmanDefeats = 0
        self.ghosts = CreateGhosts(self.team)
        self.pacman = Pacman(self.board_manager, 26.0, 13.5) # Center of Second Last Row
        self.total = self.getCount()
        self.ghostScore = 200
        self.levels = [[350, 250], [150, 450], [150, 450], [0, 600]]
        random.shuffle(self.levels)
        # Level index and Level Progress
        self.ghostStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1
        self.collected = 0
        self.started = False
        self.gameOver = False
        self.gameOverCounter = 0
        self.points = []
        self.pointsTimer = 10
        # Berry Spawn Time, Berry Death Time, Berry Eaten
        self.berryState = [200, 400, False]
        self.berryLocation = [20.0, 13.5]
        self.berries = ["tile080.png", "tile081.png", "tile082.png", "tile083.png", "tile084.png", "tile085.png", "tile086.png", "tile087.png"]
        self.berriesCollected = []
        self.levelTimer = 0
        self.berryScore = 100
        self.lockedInTimer = 100
        self.lockedIn = True
        self.extraLifeGiven = False
        self.musicPlaying = 0

    # Driver method: The games primary update method
    def update(self):
        # pygame.image.unload()
        #print(self.ghostStates)
        if self.gameOver:
            self.gameOverFunc()
            return
        if self.paused or not self.started:
            self.drawTilesAround(21, 10)
            self.drawTilesAround(21, 11)
            self.drawTilesAround(21, 12)
            self.drawTilesAround(21, 13)
            self.drawTilesAround(21, 14)
            self.drawReady()
            pygame.display.update()
            return

        self.levelTimer += 1
        self.ghostUpdateCount += 1
        self.pacmanUpdateCount += 1
        self.tictakChangeCount += 1
        self.ghostsAttacked = False
        game.pacman.ghostsAttacked = False

        """
        if self.score >= 10000 and not self.extraLifeGiven:
            self.lives += 1
            self.extraLifeGiven = True
            self.forcePlayMusic("pacman_extrapac.wav")"""

        # Draw tiles around ghosts and pacman
        self.clearBoard()
        for ghost in self.ghosts:
            if ghost.attacked:
                self.ghostsAttacked = True

        # Check if the ghost should chase pacman (only in case the ghost has no agent)
        index = 0
        for state in self.ghostStates:
            state[1] += 1
            if state[1] >= self.levels[index][state[0]]:
                state[1] = 0
                state[0] += 1
                state[0] %= 2
            index += 1

        index = 0
        for ghost in self.ghosts:
            if ghost.agent == None and not ghost.attacked and not ghost.dead and self.ghostStates[index][0] == 0:
                ghost.target = [self.pacman.row, self.pacman.col]
            index += 1

        # Set ghost observations
        self.getObservations()

        if self.levelTimer >= self.lockedInTimer:
            self.lockedIn = False

        self.checkSurroundings
        if self.ghostUpdateCount >= self.ghostUpdateDelay:
            self.update_game_board()
            for ghost in self.ghosts:
                ghost.update()
            self.ghostUpdateCount = 0

        if self.tictakChangeCount >= self.tictakChangeDelay:
            #Changes the color of special Tic-Taks
            self.flipColor()
            self.tictakChangeCount = 0

        if self.pacmanUpdateCount >= self.pacmanUpdateDelay:
            self.pacmanUpdateCount = 0
            self.update_game_board()
            self.pacman.update(CONTROL_PACMAN)
            self.pacman.col %= len(self.board_manager.board[0])
            if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                if self.board_manager.board[int(self.pacman.row)][int(self.pacman.col)] == 2:
                    self.playMusic("munch_1.wav")
                    self.board_manager.board[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.update_game_board()
                    self.score += 10
                    self.collected += 1
                    #print("Nhom Pellet")
                    # Fill tile with black
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                # found special tik-tak
                elif self.board_manager.board[int(self.pacman.row)][int(self.pacman.col)] == 5 or self.board_manager.board[int(self.pacman.row)][int(self.pacman.col)] == 6:
                    self.forcePlayMusic("power_pellet.wav")
                    self.board_manager.board[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.update_game_board()
                    self.collected += 1
                    # Fill tile with black
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                    self.score += 50
                    self.ghostScore = 200
                    for ghost in self.ghosts:
                        ghost.attackedCount = 0
                        ghost.setAttacked(True)
                        ghost.setTarget()
                        self.ghostsAttacked = True
        self.checkSurroundings()
        self.highScore = max(self.score, self.highScore)

        global running
        if self.collected == self.total:
            print("New Level")
            self.forcePlayMusic("intermission.wav")
            self.level += 1
            self.pacmanVictories += 1
            self.newLevel()

        if self.level - 1 == 1: #(self.levels[0][0] + self.levels[0][1]) // 50:
            print("You win", self.level, len(self.levels))
            running = False
        self.softRender()


    # Update the game map through the map manager
    def update_game_board(self, board = None):
        if board == None:
            self.board_manager.update_board(self.board_manager.board)
        else:
            self.board_manager.update_board(board)

    # Render method
    def render(self):
        screen.fill((0, 0, 0)) # Flushes the screen
        # Draws game elements
        currentTile = 0
        self.displayLives()
        self.displayScore()
        for i in range(3, len(self.board_manager.board) - 2):
            for j in range(len(self.board_manager.board[0])):
                if self.board_manager.board[i][j] == 3: # Draw wall
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (square, square))

                    #Display image of tile
                    screen.blit(tileImage, (j * square, i * square, square, square))

                    # pygame.draw.rect(screen, (0, 0, 255),(j * square, i * square, square, square)) # (x, y, width, height)
                elif self.board_manager.board[i][j] == 2: # Draw Tic-Tak
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//4)
                elif self.board_manager.board[i][j] == 5: #Black Special Tic-Tak
                    pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)
                elif self.board_manager.board[i][j] == 6: #White Special Tic-Tak
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)

                currentTile += 1
        # Draw Sprites
        for ghost in self.ghosts:
            ghost.draw()
        self.pacman.draw(self.started)
        # Updates the screen
        pygame.display.update()


    def softRender(self):
        pointsToDraw = []
        for point in self.points:
            if point[3] < self.pointsTimer:
                pointsToDraw.append([point[2], point[0], point[1]])
                point[3] += 1
            else:
                self.points.remove(point)
                self.drawTilesAround(point[0], point[1])

        for point in pointsToDraw:
            self.drawPoints(point[0], point[1], point[2])

        # Draw Sprites
        for ghost in self.ghosts:
            ghost.draw()
        self.pacman.draw(self.started)
        self.displayScore()
        self.displayBerries()
        self.displayLives()
        # for point in pointsToDraw:
        #     self.drawPoints(point[0], point[1], point[2])
        self.drawBerry()
        # Updates the screen
        pygame.display.update()

    def playMusic(self, music):
        # return False # Uncomment to disable music
        global musicPlaying
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unload()
            pygame.mixer.music.load(MusicPath + music)
            pygame.mixer.music.queue(MusicPath + music)
            pygame.mixer.music.play()
            if music == "munch_1.wav":
                musicPlaying = 0
            elif music == "siren_1.wav":
                musicPlaying = 2
            else:
                musicPlaying = 1

    def forcePlayMusic(self, music):
        # return False # Uncomment to disable music
        pygame.mixer.music.unload()
        pygame.mixer.music.load(MusicPath + music)
        pygame.mixer.music.play()
        global musicPlaying
        musicPlaying = 1

    def clearBoard(self):
            # Draw tiles around ghosts and pacman
            for ghost in self.ghosts:
                self.drawTilesAround(ghost.row, ghost.col)
            self.drawTilesAround(self.pacman.row, self.pacman.col)
            self.drawTilesAround(self.berryLocation[0], self.berryLocation[1])
            # Clears Ready! Label
            self.drawTilesAround(20, 10)
            self.drawTilesAround(20, 11)
            self.drawTilesAround(20, 12)
            self.drawTilesAround(20, 13)
            self.drawTilesAround(20, 14)

    def checkSurroundings(self):
        # Check if pacman got killed
        for ghost in self.ghosts:
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.isAttacked() and not ghost.isDead():
                if self.lives == 1:
                    print("You lose")
                    self.forcePlayMusic("death_1.wav")
                    self.pacmanDefeats += 1
                    self.gameOver = True
                    #Removes the ghosts from the screen
                    for ghost in self.ghosts:
                        self.drawTilesAround(ghost.row, ghost.col)
                    self.drawTilesAround(self.pacman.row, self.pacman.col)
                    self.pacman.draw(self.started)
                    pygame.display.update()
                    pause(10000000)
                    return
                self.started = False
                self.forcePlayMusic("pacman_death.wav")
                reset(self.board_manager)
            elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                #print("Nhom Ghost")
                ghost.setDead(True)
                ghost.setTarget()
                ghost.ghostSpeed = 1
                ghost.row = math.floor(ghost.row)
                ghost.col = math.floor(ghost.col)
                self.score += self.ghostScore
                self.ghostDeaths += 1
                self.points.append([ghost.row, ghost.col, self.ghostScore, 0])
                self.ghostScore *= 2
                self.forcePlayMusic("eat_ghost.wav")
                pause(10000000)
        if self.touchingPacman(self.berryLocation[0], self.berryLocation[1]) and \
            not self.berryState[2] and self.levelTimer in range(self.berryState[0], self.berryState[1]):
            #print("Nhom Berry")
            self.berryState[2] = True
            self.score += self.berryScore
            self.points.append([self.berryLocation[0], self.berryLocation[1], self.berryScore, 0])
            self.berriesCollected.append(self.berries[(self.level - 1) % 8])
            self.forcePlayMusic("eat_fruit.wav")

    # [a_i_row, a_i_col, target.row, target.col, pacman.row, pacman.col, self.board_manager.board.num, self.dead, self.attacked, self.ghostSpeed]
    def getObservations(self):
        bestDist = math.inf
        ghostChaser = None
        for ghost in self.ghosts:
            ghost.observe()

            # Pacman automatization
            newDist = calcDistance([self.pacman.row, self.pacman.col], [ghost.row, ghost.col])
            if newDist <= self.pacman.vision_radius and newDist <= bestDist and \
                not ghost.isDead() and self.board_manager.board[int(ghost.row)][int(ghost.col)] != 4:
                bestDist = newDist
                ghostChaser = ghost


        if ghostChaser == None:
            # if pacman was chasing/running away from ghost but isnt anymore, force target reset
            if game.pacman.ghost_location != [-1, -1]:
                game.pacman.target = [-1, -1]
            game.pacman.ghost_location = [-1, -1]
            game.pacman.ghost_id = -1
            game.pacman.running = False
        else:
            game.pacman.ghostsAttacked = ghost.isAttacked()
            # if pacman first sees a new not attacked ghost, it starts running
            if game.pacman.ghost_id != ghost.agent.agent_id and not ghost.isAttacked():
                game.pacman.running = True
            else:
                game.pacman.running = False
            game.pacman.ghost_location = [ghost.row, ghost.col]
            game.pacman.ghost_id = ghost.agent.agent_id

    # Displays the current score
    def displayScore(self):
        textOneUp = ["tile033.png", "tile021.png", "tile016.png"]
        textHighScore = ["tile007.png", "tile008.png", "tile006.png", "tile007.png", "tile015.png", "tile019.png", "tile002.png", "tile014.png", "tile018.png", "tile004.png"]
        index = 0
        scoreStart = 5
        highScoreStart = 11
        for i in range(scoreStart, scoreStart+len(textOneUp)):
            tileImage = pygame.image.load(TextPath + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, (i * square, 4, square, square))
            index += 1
        score = str(self.score)
        if score == "0":
            score = "00"
        index = 0
        for i in range(0, len(score)):
            digit = int(score[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, ((scoreStart + 2 + index) * square, square + 4, square, square))
            index += 1

        index = 0
        for i in range(highScoreStart, highScoreStart+len(textHighScore)):
            tileImage = pygame.image.load(TextPath + textHighScore[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, (i * square, 4, square, square))
            index += 1

        highScore = str(self.highScore)
        if highScore == "0":
            highScore = "00"
        index = 0
        for i in range(0, len(highScore)):
            digit = int(highScore[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, ((highScoreStart + 6 + index) * square, square + 4, square, square))
            index += 1

    def drawBerry(self):
        if self.levelTimer in range(self.berryState[0], self.berryState[1]) and not self.berryState[2]:
            # print("here")
            berryImage = pygame.image.load(ElementPath + self.berries[(self.level - 1) % 8])
            berryImage = pygame.transform.scale(berryImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(berryImage, (self.berryLocation[1] * square, self.berryLocation[0] * square, square, square))

    def drawPoints(self, points, row, col):
        pointStr = str(points)
        index = 0
        for i in range(len(pointStr)):
            digit = int(pointStr[i])
            tileImage = pygame.image.load(TextPath + "tile" + str(224 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square//2, square//2))
            screen.blit(tileImage, ((col) * square + (square//2 * index), row * square - 20, square//2, square//2))
            index += 1

    def drawReady(self):
        ready = ["tile274.png", "tile260.png", "tile256.png", "tile259.png", "tile281.png", "tile283.png"]
        for i in range(len(ready)):
            letter = pygame.image.load(TextPath + ready[i])
            letter = pygame.transform.scale(letter, (int(square), int(square)))
            screen.blit(letter, ((11 + i) * square, 20 * square, square, square))

    def gameOverFunc(self):
        global running
        #if self.gameOverCounter == 12:
        if self.gameOverCounter == 1:
            running = False
            self.recordHighScore()
            return

        # Resets the screen around pacman
        self.drawTilesAround(self.pacman.row, self.pacman.col)

        # Draws new image
        pacmanImage = pygame.image.load(ElementPath + "tile" + str(116 + self.gameOverCounter) + ".png")
        pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(pacmanImage, (self.pacman.col * square + spriteOffset, self.pacman.row * square + spriteOffset, square, square))
        pygame.display.update()
        #pause(5000000)
        self.gameOverCounter += 1

    def displayLives(self):
        # 33 rows || 28 cols
        # Lives[[31, 5], [31, 3], [31, 1]]
        livesLoc = [[34, 3], [34, 1]]
        for i in range(self.lives - 1):
            lifeImage = pygame.image.load(ElementPath + "tile054.png")
            lifeImage = pygame.transform.scale(lifeImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(lifeImage, (livesLoc[i][1] * square, livesLoc[i][0] * square - spriteOffset, square, square))

    def displayBerries(self):
        firstBerrie = [34, 26]
        for i in range(len(self.berriesCollected)):
            berrieImage = pygame.image.load(ElementPath + self.berriesCollected[i])
            berrieImage = pygame.transform.scale(berrieImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(berrieImage, ((firstBerrie[1] - (2*i)) * square, firstBerrie[0] * square + 5, square, square))

    def touchingPacman(self, row, col):
        if row - 0.5 <= self.pacman.row and row >= self.pacman.row and col == self.pacman.col:
            return True
        elif row + 0.5 >= self.pacman.row and row <= self.pacman.row and col == self.pacman.col:
            return True
        elif row == self.pacman.row and col - 0.5 <= self.pacman.col and col >= self.pacman.col:
            return True
        elif row == self.pacman.row and col + 0.5 >= self.pacman.col and col <= self.pacman.col:
            return True
        elif row == self.pacman.row and col == self.pacman.col:
            return True
        return False

    def newLevel(self):
        reset(self.board_manager)
        self.lives += 1
        self.collected = 0
        self.started = False
        self.berryState = [200, 400, False]
        self.levelTimer = 0
        self.lockedIn = True
        for level in self.levels:
            level[0] = min((level[0] + level[1]) - 100, level[0] + 50)
            level[1] = max(100, level[1] - 50)
        random.shuffle(self.levels)
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1

        self.update_game_board(originalGameBoard)
        self.render()

    def drawTilesAround(self, row, col):
        row = math.floor(row)
        col = math.floor(col)
        for i in range(row-2, row+3):
            for j in range(col-2, col+3):
                if i >= 3 and i < len(self.board_manager.board) - 2 and j >= 0 and j < len(self.board_manager.board[0]):
                    imageName = str(((i - 3) * len(self.board_manager.board[0])) + j)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (square, square))
                    #Display image of tile
                    screen.blit(tileImage, (j * square, i * square, square, square))

                    if self.board_manager.board[i][j] == 2: # Draw Tic-Tak
                        pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//4)
                    elif self.board_manager.board[i][j] == 5: #Black Special Tic-Tak
                        pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)
                    elif self.board_manager.board[i][j] == 6: #White Special Tic-Tak
                        pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)

    # Flips Color of Special Tic-Taks
    def flipColor(self):
        for i in range(3, len(self.board_manager.board) - 2):
            for j in range(len(self.board_manager.board[0])):
                if self.board_manager.board[i][j] == 5:
                    self.board_manager.board[i][j] = 6
                    self.update_game_board()
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)
                elif self.board_manager.board[i][j] == 6:
                    self.board_manager.board[i][j] = 5
                    self.update_game_board()
                    pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)

    def getCount(self):
        total = 0
        for i in range(3, len(self.board_manager.board) - 2):
            for j in range(len(self.board_manager.board[0])):
                if self.board_manager.board[i][j] == 2 or self.board_manager.board[i][j] == 5 or self.board_manager.board[i][j] == 6:
                    total += 1
        return total

    def getHighScore(self):
        file = open(DataPath + "HighScore.txt", "r")
        highScore = int(file.read())
        file.close()
        return highScore

    def recordHighScore(self):
        file = open(DataPath + "HighScore.txt", "w").close()
        file = open(DataPath + "HighScore.txt", "w+")
        file.write(str(self.highScore))
        file.close()


class Ghost:
    def __init__(self, board_manager, agent, row, col, color, changeFeetCount):
        self.board_manager = board_manager
        self.agent = agent
        self.row = row
        self.col = col
        self.attacked = False
        self.color = color
        self.dir = randrange(4)
        self.dead = False
        self.changeFeetCount = changeFeetCount
        self.changeFeetDelay = 5
        self.target = [-1, -1]
        self.ghostSpeed = 1/2
        self.lastLoc = [-1, -1]
        #self.attackedTimer = 240
        self.attackedTimer = 170
        self.attackedCount = 0
        self.deathTimer = 120
        self.deathCount = 0
        if self.agent != None:
            self.agent.current_action = self.dir

    def update(self):
        # print(self.row, self.col)
        self.setTarget(True) # if Agent is not None, action is chosen here
        self.setDir()
        self.move()

        if self.attacked:
            self.attackedCount += 1

        if self.attacked and not self.dead:
            self.ghostSpeed = 1/4

        if self.attackedCount == self.attackedTimer and self.attacked:
            if not self.dead:
                self.ghostSpeed = 1/2
                self.row = math.floor(self.row)
                self.col = math.floor(self.col)

            self.attackedCount = 0
            self.attacked = False
            self.setTarget()

        if self.dead and self.board_manager.board[self.row][self.col] == 4:
            self.deathCount += 1
            self.attacked = False
            if self.deathCount == self.deathTimer:
                self.deathCount = 0
                self.dead = False
                self.ghostSpeed = 1/4


    def draw(self): # Ghosts states: Alive, Attacked, Dead Attributes: Color, Direction, Location
        ghostImage = pygame.image.load(ElementPath + "tile152.png")
        currentDir = ((self.dir + 3) % 4) * 2
        if self.changeFeetCount == self.changeFeetDelay:
            self.changeFeetCount = 0
            currentDir += 1
        self.changeFeetCount += 1
        if self.dead:
            tileNum = 152 + currentDir
            ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
        elif self.attacked:
            if self.attackedTimer - self.attackedCount < self.attackedTimer//3:
                if (self.attackedTimer - self.attackedCount) % 31 < 26:
                    ghostImage = pygame.image.load(ElementPath + "tile0" + str(70 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
                else:
                    ghostImage = pygame.image.load(ElementPath + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
            else:
                ghostImage = pygame.image.load(ElementPath + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
        else:
            if self.color == "blue":
                tileNum = 136 + currentDir
                ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
            elif self.color == "pink":
                tileNum = 128 + currentDir
                ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
            elif self.color == "orange":
                tileNum = 144 + currentDir
                ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
            elif self.color == "red":
                tileNum = 96 + currentDir
                if tileNum < 100:
                    ghostImage = pygame.image.load(ElementPath + "tile0" + str(tileNum) + ".png")
                else:
                    ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")

        ghostImage = pygame.transform.scale(ghostImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(ghostImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    def isValidTwo(self, cRow, cCol, dist, visited):
        if cRow < 3 or cRow >= len(self.board_manager.board) - 5 or cCol < 0 or \
            cCol >= len(self.board_manager.board[0]) or self.board_manager.board[cRow][cCol] == 3:
            return False
        elif visited[cRow][cCol] <= dist:
            return False
        return True

    def isValid(self, cRow, cCol):
        if cCol < 0 or cCol > len(self.board_manager.board[0]) - 1:
            return True
        for ghost in game.ghosts:
            if ghost.color == self.color:
                continue
            if ghost.row == cRow and ghost.col == cCol and not self.dead:
                return False
        if not ghostGate.count([cRow, cCol]) == 0:
            if self.dead and self.row < cRow:
                return True
            elif self.row > cRow and not self.dead and not self.attacked and not game.lockedIn:
                return True
            else:
                return False
        if self.board_manager.board[cRow][cCol] == 3:
            return False
        return True

    def observe(self):
        if self.agent != None:
            # an observation is [a_i_row, a_i_col, target.row, target.col, pacman.row, 
            # pacman.col, self.board_manager.board.num, self.dead, self.attacked, self.ghostSpeed]
            observations = []
            pacman_seen = False
            for ghost in game.ghosts:
                observations += [ghost.row, ghost.col]
            observations += [self.target[0], self.target[1]]
            if ((game.pacman.row == self.row) or (game.pacman.col == self.col)) and self.seesPacman():
                pacman_seen = True
                observations += [game.pacman.row, game.pacman.col]
            else:
                observations += [-1, -1]
            observations += [self.board_manager.board[int(self.row)][int(self.col)], 1 if self.dead else 0, 1 if self.attacked else 0, self.ghostSpeed]

            # if agent is CoordinatedAgent and has seen pacman, inform other agents about it
            if pacman_seen and isinstance(self.agent, CoordinatedAgent):
                for ghost in game.ghosts:
                    if ghost.isDead() or ghost.isAttacked():
                        continue
                    if ghost.agent.agent_id == self.agent.agent_id:
                        self.agent.see(observations)
                    else:
                        agent_observations = observations[:2*N_AGENTS] + [ghost.target[0], ghost.target[1], game.pacman.row, game.pacman.col, self.board_manager.board[int(ghost.row)][int(ghost.col)], 1 if ghost.dead else 0, 1 if ghost.attacked else 0, ghost.ghostSpeed]
                        ghost.agent.see(agent_observations)
                        ghost.setTarget()
            else:
                self.agent.see(observations)

    def seesPacman(self):
        sees = False
        if abs(game.pacman.row - self.row) <= 0.5:
            if self.col <= game.pacman.col:
                sees = all((element != 3) and (element != 4) for element in self.board_manager.board[int(self.row)][int(self.col):int(game.pacman.col)])
            else:
                sees = all((element != 3) and (element != 4) for element in self.board_manager.board[int(self.row)][int(game.pacman.col):int(self.col)])
        if abs(game.pacman.col - self.col) <= 0.5:
            column = [row[int(self.col)] for row in self.board_manager.board]
            if self.row <= game.pacman.row:
                sees = all((element != 3) and (element != 4) for element in column[int(self.row):int(game.pacman.row)])
            else:
                sees = all((element != 3) and (element != 4) for element in column[int(game.pacman.row):int(self.row)])
        return sees

    def setDir(self):
        # Very inefficient || can easily refactor
        # BFS search -> Not best route but a route none the less
        # From original code. Original computation of ghost AI
        dirs = [[0, -self.ghostSpeed, 0],
                [1, 0, self.ghostSpeed],
                [2, self.ghostSpeed, 0],
                [3, 0, -self.ghostSpeed]]
        random.shuffle(dirs)
        best = 10000
        bestDir = -1
        for newDir in dirs:
            if calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]]) < best:
                if not (self.lastLoc[0] == self.row + newDir[1] and self.lastLoc[1] == self.col + newDir[2]):
                    if newDir[0] == 0 and self.col % 1.0 == 0:
                        if self.isValid(math.floor(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 1 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.ceil(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 2 and self.col % 1.0 == 0:
                        if self.isValid(math.ceil(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 3 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.floor(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
        self.dir = bestDir

    def setTarget(self, check = False):
        # region STANDARD RULES - apply to every case regardless of agent type #
        if self.board_manager.board[int(self.row)][int(self.col)] == 4 and not self.dead:
            self.target = [ghostGate[0][0] - 1, ghostGate[0][1]+1]
            return
        elif self.board_manager.board[int(self.row)][int(self.col)] == 4 and self.dead:
            self.target = [self.row, self.col]
        elif self.dead:
            self.target = [14, 13]
            return
        # endregion #

        # Follow agent heuristics
        if self.agent != None:
            target = self.agent.action(check)
            if DEBUG_MODE and self.target != target and self.agent.seesPacman() and not self.isDead() and not self.isAttacked() and not isinstance(self, RandomAgent):
                pygame.draw.circle(screen, self.color, (self.target[1] * square + square//2, self.target[0] * square + square//2), square//2)

            self.target = target
        # Finds a target that will keep the ghosts dispersed
        elif not check or self.target == [-1, -1] or (self.row == self.target[0] and self.col == self.target[1]) or \
            self.board_manager.board[int(self.row)][int(self.col)] == 4 or self.dead:
            # Records the quadrants of each ghost's target
            quads = [0, 0, 0, 0]
            for ghost in game.ghosts:
                # if ghost.target[0] == self.row and ghost.col == self.col:
                #     continue
                if ghost.target[0] <= 15 and ghost.target[1] >= 13:
                    quads[0] += 1
                elif ghost.target[0] <= 15 and ghost.target[1] < 13:
                    quads[1] += 1
                elif ghost.target[0] > 15 and ghost.target[1] < 13:
                    quads[2] += 1
                elif ghost.target[0]> 15 and ghost.target[1] >= 13:
                    quads[3] += 1

            while True:
                self.target = [randrange(31), randrange(28)]
                quad = 0
                if self.target[0] <= 15 and self.target[1] >= 13:
                    quad = 0
                elif self.target[0] <= 15 and self.target[1] < 13:
                    quad = 1
                elif self.target[0] > 15 and self.target[1] < 13:
                    quad = 2
                elif self.target[0] > 15 and self.target[1] >= 13:
                    quad = 3

                if not self.board_manager.board[self.target[0]][self.target[1]] == 3 and not self.board_manager.board[self.target[0]][self.target[1]] == 4:
                    break
                elif quads[quad] == 0:
                    break

    def move(self):
        self.lastLoc = [self.row, self.col]
        if self.dir == 0:
            self.row -= self.ghostSpeed
        elif self.dir == 1:
            self.col += self.ghostSpeed
        elif self.dir == 2:
            self.row += self.ghostSpeed
        elif self.dir == 3:
            self.col -= self.ghostSpeed

        # Incase they go through the middle tunnel
        self.col = self.col % len(self.board_manager.board[0])
        if self.col < 0:
            self.col = len(self.board_manager.board[0]) - 0.5

    def setAttacked(self, isAttacked):
        self.attacked = isAttacked

    def isAttacked(self):
        return self.attacked

    def setDead(self, isDead):
        self.dead = isDead

    def isDead(self):
        return self.dead


def CreateGhosts(t = 'Greedy Team w/ Roles') -> List[Ghost]:
    team = teams[t]

    # create ghosts and assign to respective team.
    ghosts = [Ghost(board_manager, team[0], 14.0, 13.5, "red", 0), Ghost(board_manager, team[1], 17.0, 11.5, "blue", 1),
               Ghost(board_manager, team[2], 17.0, 13.5, "pink", 2), Ghost(board_manager, team[3], 17.0, 15.5, "orange", 3)]

    # (original version) ghosts follow the original game's heuristics
    #ghosts = [Ghost(board_manager, None, 14.0, 13.5, "red", 0), Ghost(board_manager, None, 17.0, 11.5, "blue", 1), 
    # Ghost(board_manager, None, 17.0, 13.5, "pink", 2), Ghost(board_manager, None, 17.0, 15.5, "orange", 3)]

    return ghosts


parser = argparse.ArgumentParser()
parser.add_argument("--c", type=str_to_bool, default=False, help="Control Pacman with keyboard vs AI")
parser.add_argument("--debug", type=str_to_bool, default=False, help="Enables debugging features")
opt = parser.parse_args()
CONTROL_PACMAN = opt.c
DEBUG_MODE = opt.debug
# N_EPISODES = 100
N_EPISODES = 1 # perform only a single episode for simplicity

pygame.mixer.init()
pygame.init()
pygame.display.flip()
musicPlaying = 0 # 0: Chomp, 1: Important, 2: Siren

# Evaluate teams
start_time = time.time()
results = {}
scores = {}
pacDefeats = {}
pacVictories = {}
ghostDeaths = {}
fileResults = open("results.txt", "w")

# if not CONTROL_PACMAN perform N_EPISODES episodes for each team. Start with random agents, 
# then greedy, then social conventions and, finally, roles.
# if CONTROL_PACMAN, play normal pacman just for one episode with random agents
for team, agents in teams.items(): 
    print("team: " + team)
    result = np.zeros(N_EPISODES)
    score = np.zeros(N_EPISODES)
    pacDefeat = np.zeros(N_EPISODES)
    pacVictory = np.zeros(N_EPISODES)
    ghostDeath = np.zeros(N_EPISODES)
    for episode in range(N_EPISODES):
        game = Game(board_manager, 1, 0, team)
        running = True
        onLaunchScreen = True
        displayLaunchScreen()
        clock = pygame.time.Clock()
        print("\n")
        print("episode: " + str(episode))
        steps = 0
        if not CONTROL_PACMAN:
            onLaunchScreen = False
            game.render()
            game.softRender()
            pygame.mixer.music.load(MusicPath + "pacman_beginning.wav")
            pygame.mixer.music.play()
            musicPlaying = 1

        while running:
            steps += 1
            clock.tick(40)
            if not CONTROL_PACMAN:
                game.paused = False
                game.started = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game.recordHighScore()
                elif event.type == pygame.KEYDOWN:
                    game.paused = False
                    game.started = True
                    if CONTROL_PACMAN:
                        if event.key in PLAYING_KEYS["up"]:
                            if not onLaunchScreen:
                                game.pacman.newDir = 0
                        elif event.key in PLAYING_KEYS["right"]:
                            if not onLaunchScreen:
                                game.pacman.newDir = 1
                        elif event.key in PLAYING_KEYS["down"]:
                            if not onLaunchScreen:
                                game.pacman.newDir = 2
                        elif event.key in PLAYING_KEYS["left"]:
                            if not onLaunchScreen:
                                game.pacman.newDir = 3
                    if event.key == pygame.K_SPACE:
                        if onLaunchScreen:
                            onLaunchScreen = False
                            game.paused = True
                            game.started = False
                            game.render()
                            pygame.mixer.music.load(MusicPath + "pacman_beginning.wav")
                            pygame.mixer.music.play()
                            musicPlaying = 1
                    elif event.key == pygame.K_q:
                        running = False
                        game.recordHighScore()

            if not onLaunchScreen:
                game.update()

        result[episode] = steps
        score[episode] = game.score
        pacDefeat[episode] = game.pacmanDefeats
        pacVictory[episode] = game.pacmanVictories
        ghostDeath[episode] = game.ghostDeaths
        board_manager.update_board(originalGameBoard)

        if CONTROL_PACMAN:
            break

    if CONTROL_PACMAN:
        break

    results[team] = result
    scores[team] = score
    pacDefeats[team] = pacDefeat
    pacVictories[team] = pacVictory
    ghostDeaths[team] = ghostDeath

    fileResults.write("Team: " + team + "\n")
    fileResults.write("Average Steps: " + str(np.mean(results[team])) + "\n")
    fileResults.write("Average Score: " + str(np.mean(scores[team])) + "\n")
    fileResults.write("Average Pacman Defeats: " + str(np.mean(pacDefeats[team])) + "\n")
    fileResults.write("Average Pacman Victories: " + str(np.mean(pacVictories[team])) + "\n")
    fileResults.write("Average Ghost Deaths: " + str(np.mean(ghostDeaths[team])) + "\n\n")

fileResults.close()
elapsed_time = time.time() - start_time
print("Elapsed time:", elapsed_time, "seconds")

# Compare results
if not CONTROL_PACMAN:
    utils.compare_results(
        results,
        title="Teams Comparison on 'Pacman' Environment",
        colors=["orange", "green", "blue", "gray"]
    )
