import pygame

def manhattanDistance( xy1, xy2 ):
    # Returns the Manhattan distance between points xy1 and xy2
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def getinput(where="keyboard"):
    if where == "keyboard":
        input = pygame.key.get_pressed()
        if input[pygame.K_LEFT]:
            out_direction = "West"
        elif input[pygame.K_RIGHT]:
            out_direction = "East"
        elif input[pygame.K_UP]:
            out_direction = "North"
        elif input[pygame.K_DOWN]:
            out_direction = "South"
        else: return None

    #else: out_direction = "South" #TODO agent

    return out_direction