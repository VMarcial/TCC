import pygame
from pygame.locals import *
import sys
import sim, world

def main():

    # Constantes utilizadas e variável de estado do programa
    BLUE =          (0      ,0      ,255    )
    BACKGROUND =    (31     ,153    ,49     )
    GRAY =          (160    ,160    ,160    )
    RED =           (255    ,8      ,0      )
    HEIGHT =    800
    WIDTH =     800
    running =   True

    # Inicialização do Pygame
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PROJETOS 3")

    # Inicializando os indivíduos e o mapa
    pop = sim.generate(center = [HEIGHT/2, WIDTH/2])
    gamemap = world.world()
    gamemap.generate_food()

    while running:
        print(1)
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.event.pump()
        
        gamemap.time += 1

        if gamemap.time % 7200 == 0:
            gamemap.generate_food()

        for item in gamemap.items:
            pygame.draw.circle(screen, RED, (item.posX, item.posY), 5)
        

        for ind in pop:
            if ind.state == "DEAD":
                pygame.draw.circle(screen, GRAY, (ind.posX, ind.posY), 20)
            else:
                pygame.draw.circle(screen, BLUE, (ind.posX, ind.posY), 20)
                ind.action(gamemap)

        pygame.display.update()
        


if __name__ == "__main__":

    main()
