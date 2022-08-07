import sys, pygame

# Initializing pygame
pygame.font.init()
 
# Check if font is initialized
pygame.font.get_init()

# Create the display surface
display_surface = pygame.display.set_mode((500, 500))

score = 0

font1 = pygame.font.SysFont('freesanbold.ttf', 50)
text1 = font1.render(f'{score}', True, (0, 255, 0))
textRect1 = text1.get_rect()

# Center for text
textRect1.center = (350, 50)

# Cookie img
cookie = pygame.image.load("cookie.png")
cookie = pygame.transform.scale(cookie,(100,100))
cookierect = cookie.get_rect()
cookierect.center = (250,250)

def between_two_numbers(num,a,b):
    if a < num and num < b: 
        return True
    else: 
        return False

def check_click_on_cookie(pos):
    if between_two_numbers(pos[0],200,300) and between_two_numbers(pos[1],200,300):
        return True

while 1:

    display_surface.fill((0,0,0))

    display_surface.blit(font1.render(f'{score}', True, (0, 255, 0)), textRect1)

    display_surface.blit(cookie, cookierect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if check_click_on_cookie(pos):
                score +=1


    pygame.display.update()