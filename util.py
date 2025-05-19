import pygame

def manhattanDistance( xy1, xy2 ):
    # Returns the Manhattan distance between points xy1 and xy2
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def getinput(where="keyboard"):
    if where == "keyboard":
        while True:  # Block until a key is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        return "West"
                    elif event.key == pygame.K_RIGHT:
                        return "East"
                    elif event.key == pygame.K_UP:
                        return "North"
                    elif event.key == pygame.K_DOWN:
                        return "South"

