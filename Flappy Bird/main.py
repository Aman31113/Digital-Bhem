import random
import sys
import pygame
from pygame.locals import *

# Global Variables for the game
Fps = 32
ScreenWidth = 289
ScreenHeight = 511
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
Ground = ScreenHeight * 0.8
Game_Sprites = {}
Game_Sounds = {}
Player = 'gallery/sprites/bird.png'
BackGround = 'gallery/sprites/BackGround.jpg'
Pipe = 'gallery/sprites/pipe.png'


def welcomeScreen():

    PlayerX = int(ScreenWidth/5)
    PlayerY = int((ScreenHeight - Game_Sprites['Player'].get_height())/2)
    messageX = int((ScreenWidth - Game_Sprites['message'].get_width())/2)
    messageY = int(ScreenHeight*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                Screen.blit(Game_Sprites['BackGround'], (0, 0))
                Screen.blit(Game_Sprites['Player'], (PlayerX, PlayerY))
                Screen.blit(Game_Sprites['message'], (messageX, messageY))
                Screen.blit(Game_Sprites['base'], (basex, Ground))
                pygame.display.update()
                FpsClock.tick(Fps)


def mainGame():
    score = 0
    PlayerX = int(ScreenWidth/5)
    PlayerY = int(ScreenWidth/2)
    basex = 0

    # Create 2 pipes for blitting on the Screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': ScreenWidth+200, 'y': newPipe1[0]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': ScreenWidth+200, 'y': newPipe1[1]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    PlayerVelY = -9
    PlayerMaxVelY = 10
    PlayerMinVelY = -8
    PlayerAccY = 1

    PlayerFlapAccv = -8  # velocity while flapping
    PlayerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if PlayerY > 0:
                    PlayerVelY = PlayerFlapAccv
                    PlayerFlapped = True
                    Game_Sounds['wing'].play()

        crashTest = isCollide(PlayerX, PlayerY, upperPipes, lowerPipes)
        if crashTest:
            return

        # check for score
        PlayerMidPos = PlayerX + Game_Sprites['Player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + Game_Sprites['pipe'][0].get_width()/2
            if pipeMidPos <= PlayerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                Game_Sounds['point'].play()

        if PlayerVelY < PlayerMaxVelY and not PlayerFlapped:
            PlayerVelY += PlayerAccY

        if PlayerFlapped:
            PlayerFlapped = False
        PlayerHeight = Game_Sprites['Player'].get_height()
        PlayerY = PlayerY + min(PlayerVelY, Ground - PlayerY - PlayerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the Screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the Screen, remove it
        if upperPipes[0]['x'] < -Game_Sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        Screen.blit(Game_Sprites['BackGround'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            Screen.blit(Game_Sprites['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            Screen.blit(Game_Sprites['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        Screen.blit(Game_Sprites['base'], (basex, Ground))
        Screen.blit(Game_Sprites['Player'], (PlayerX, PlayerY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += Game_Sprites['numbers'][digit].get_width()
        Xoffset = (ScreenWidth - width)/2

        for digit in myDigits:
            Screen.blit(Game_Sprites['numbers'][digit],
                        (Xoffset, ScreenHeight*0.12))
            Xoffset += Game_Sprites['numbers'][digit].get_width()
        pygame.display.update()
        FpsClock.tick(Fps)


def isCollide(PlayerX, PlayerY, upperPipes, lowerPipes):
    if PlayerY > Ground - 25 or PlayerY < 0:
        Game_Sounds['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = Game_Sprites['pipe'][0].get_height()
        if (PlayerY < pipeHeight + pipe['y'] and abs(PlayerX - pipe['x']) < Game_Sprites['pipe'][0].get_width()):
            Game_Sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (PlayerY + Game_Sprites['Player'].get_height() > pipe['y']) and abs(PlayerX - pipe['x']) < Game_Sprites['pipe'][0].get_width():
            Game_Sounds['hit'].play()
            return True

    return False


def getRandomPipe():

    pipeHeight = Game_Sprites['pipe'][0].get_height()
    offset = ScreenHeight/3
    y2 = offset + random.randrange(0, int(ScreenHeight -
                                   Game_Sprites['base'].get_height() - 1.2 * offset))
    pipeX = ScreenWidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()  # Initialize all pygame's modules
    FpsClock = pygame.time.Clock()
    Game_Sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    Game_Sprites['message'] = pygame.image.load(
        'gallery/sprites/message.png').convert_alpha()
    Game_Sprites['base'] = pygame.image.load(
        'gallery/sprites/base.png').convert_alpha()
    Game_Sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(), 180),
                            pygame.image.load(Pipe).convert_alpha()
                            )

    # Game sounds
    Game_Sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    Game_Sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    Game_Sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    Game_Sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    Game_Sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    Game_Sprites['BackGround'] = pygame.image.load(BackGround).convert()
    Game_Sprites['Player'] = pygame.image.load(Player).convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome Screen to the user until he presses a button
        mainGame()  # This is the main game function



