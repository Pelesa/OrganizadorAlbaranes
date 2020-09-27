import pygame
import sys
from PIL import Image

#Scrollbar https://github.com/edward344/scrollbar/blob/master/scrollbar.py o https://pygame-menu.readthedocs.io/en/latest/_source/widgets_scrollbar.html

pygame.init()

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)
def setup(path):
    screen_width=595
    screen_height=842

    px = pygame.image.load(path)
    print(px.get_rect().size[0],px.get_rect().size[1])

    #Escalar imagen (tener en cuenta que esto distorsiona el rectangulo)
    px = pygame.transform.scale(px, (screen_width, screen_height))
    
    
    screen=pygame.display.set_mode([screen_width,screen_height])

    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

# def escalar(screen, img):
    


def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n=0
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n=1
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return ( topleft + bottomright )

if __name__ == "__main__":
    input_loc = 'page1.jpg'
    output_loc = 'out.png'
    screen, px = setup(input_loc)
    print(screen, px)
    left, upper, right, lower = mainLoop(screen, px)

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower
    im = Image.open(input_loc)
    im = im.crop(( left, upper, right, lower))
    pygame.display.quit()
    im.save(output_loc)


    