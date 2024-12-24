import math
import random
from BoardGame import *

class Pacman:
    def __init__(self, board_manager, row, col):
        self.board_manager = board_manager
        self.row = row
        self.col = col
        self.mouthOpen = False
        self.pacSpeed = 1/2
        self.mouthChangeDelay = 5
        self.mouthChangeCount = 0
        self.dir = 0 # 0: North, 1: East, 2: South, 3: West
        self.newDir = 0
        self.target = [-1, -1]
        self.lastLoc = [-1, -1]
        self.ghost_location = [-1, -1]
        self.ghost_id = -1
        self.running = False
        self.ghostsAttacked = False
        self.vision_radius = 5

    def update(self, control_pacman):
        #if true, pacman is controlled by user, else simple AI
        if control_pacman:
            self.updateManual()
        else:
            # run away from ghosts
            if self.seesGhost() and not self.ghostsAttacked:
                self.target = self.calculateEscapeDir()
            # chase ghosts
            elif self.seesGhost() and self.ghostsAttacked:
                self.target = self.ghost_location
            # eat special tic taks
            elif self.target == [-1, -1] or (self.row == self.target[0] and self.col == self.target[1]):
                target = self.chooseTarget()
                if target != [-1, -1]:
                    self.target = target
                else:
                    self.target = GetRandomTarget()

            self.setDir()
            self.move()

    # if pacman is controlled by user input and not AI
    def updateManual(self):
        if self.newDir == 0:
            if self.canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 1:
            if self.canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 2:
            if self.canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 3:
            if self.canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed
                self.dir = self.newDir
                return

        if self.dir == 0:
            if self.canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
        elif self.dir == 1:
            if self.canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
        elif self.dir == 2:
            if self.canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
        elif self.dir == 3:
            if self.canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed

    def calculateEscapeDir(self):
        # Calculate the row and column differences
        row_diff = self.row - self.ghost_location[0]
        col_diff = self.col - self.ghost_location[1]

        # Determine the direction based on the differences
        if abs(row_diff) > abs(col_diff):
            # Pacman is further apart vertically, so move in the vertical direction
            if row_diff > 0:
                # down
                return [self.row + self.pacSpeed, self.col]
            else:
                # up
                return [self.row -self.pacSpeed, self.col]
        else:
            # Pacman is further apart horizontally, so move in the horizontal direction
            if col_diff > 0:
                # right
                return [self.row, self.col + self.pacSpeed]
            else:
                # left
                return [self.row, self.col - self.pacSpeed]

    def chooseTarget(self):
        min_dist = math.inf
        best_tic = [-1, -1]
        # special tic taks
        tictaks = [(i, j) for i, row in enumerate(self.board_manager.board) for j, tile in enumerate(row) if tile == 5 or tile == 6 or tile == 2]
        for t in tictaks:
            if t != [-1, -1]:
                dist = calcDistance((self.row, self.col), t)
                # fast search, the more tictaks, the bigger the radius
                # makes up for a more fair algorithm so that pacman doesnt prioritize the special tictaks and makes the game last too long by perma attacking ghosts
                if dist <= (self.vision_radius * len(tictaks) * 0.5):
                    best_tic = t
                    break
                if dist < min_dist:
                    best_tic = t
                    min_dist = dist

        """# if no more special tics are available, go for normal ones to complete level
        if best_tic == [-1, -1]:
            # coordinates of currently existing normal tictaks
            tictaks = [(i, j) for i, row in enumerate(self.board_manager.board) for j, tile in enumerate(row) if tile == 2]
            min_dist = math.inf
            for t in tictaks:
                dist = calcDistance((self.row, self.col), t)
                if dist < min_dist:
                    min_dist = dist
                    best_tic = t"""
        return best_tic

    # Draws pacman based on his current state
    def draw(self, started):
        if not started:
            pacmanImage = pygame.image.load(ElementPath + "tile112.png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))
            return

        if self.mouthChangeCount >= self.mouthChangeDelay:
            self.mouthChangeCount = 0
            self.mouthOpen = not self.mouthOpen
        self.mouthChangeCount += 1
        # pacmanImage = pygame.image.load("Sprites/tile049.png")
        if self.dir == 0:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile049.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile051.png")
        elif self.dir == 1:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile052.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile054.png")
        elif self.dir == 2:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile053.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile055.png")
        elif self.dir == 3:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile048.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile050.png")

        pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    def setDir(self):
        # Very inefficient || can easily refactor
        # BFS search -> Not best route but a route none the less
        # Original computation of ghost AI
        dirs = [[0, -self.pacSpeed, 0],
                [1, 0, self.pacSpeed],
                [2, self.pacSpeed, 0],
                [3, 0, -self.pacSpeed]]
        random.shuffle(dirs)
        best = 10000
        bestDir = -1
        for newDir in dirs:
            if calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]]) < best:
                if self.running or not (self.lastLoc[0] == self.row + newDir[1] and self.lastLoc[1] == self.col + newDir[2]):
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

    def move(self):
        self.lastLoc = [self.row, self.col]
        if self.dir == 0:
            self.row -= self.pacSpeed
        elif self.dir == 1:
            self.col += self.pacSpeed
        elif self.dir == 2:
            self.row += self.pacSpeed
        elif self.dir == 3:
            self.col -= self.pacSpeed

        # Incase they go through the middle tunnel
        self.col = self.col % len(self.board_manager.board[0])
        if self.col < 0:
            self.col = len(self.board_manager.board[0]) - 0.5

    def isValid(self, cRow, cCol):
        if cCol < 0 or cCol > len(self.board_manager.board[0]) - 1:
            return True
        if self.row == cRow and self.col == cCol:
            return False
        if self.board_manager.board[cRow][cCol] == 3:
            return False
        return True

    def seesGhost(self):
        return self.ghost_location != [-1, -1]

    def canMove(self, row, col):
        if col == -1 or col == len(self.board_manager.board[0]):
            return True
        if self.board_manager.board[int(row)][int(col)] != 3:
            return True
        return False
