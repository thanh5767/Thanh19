import pygame,sys
from pygame._sdl2.video import Window,Renderer,Texture,Image
pygame.init()

clock = pygame.time.Clock()
window = Window(size = (600,600))
render = Renderer(window)
render.draw_color = (0,0,0,255)

while True:
    render.clear()
    window.title = f'{clock.get_fps()}' 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
    clock.tick(60)
    render.present()