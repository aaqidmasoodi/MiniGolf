import pygame
import sys
import time
import button
from MENU_CONFIG import *
from levels import LEVELS
pygame.init()


# GAME SETTINGS
FPS = 240
clock = pygame.time.Clock()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
game_paused = False
menu_state = "main"
resume_iteration = False
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("AliciaGolf")
HOLER = 25
HOLER_GRAB = 11
BALL_THICKNESS = 10
xspeed = 0
yspeed = 0
BALL_IN_HOLE = False
strokes = 0
modulator = 20
WALL_COLOR = (204, 102, 0)
LEVEL_NUM = 1
x = LEVELS[LEVEL_NUM]["BALL_INITIAL_LOCATION_X"]
y = LEVELS[LEVEL_NUM]["BALL_INITIAL_LOCATION_Y"]
font_game = pygame.font.Font('BRLNSB.TTF', 100)
font_strokes = pygame.font.Font('BRLNSB.TTF', 100)
overlay = pygame.Surface((800,600), pygame.SRCALPHA)
overlay.fill((0,0,0,200))


# load sounds
# LOAD BACKGRUND MUSIC
pygame.mixer.music.load("./sounds/golf_background.wav")
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1)

# LOAD GOLF HIT
GOLF_HIT = pygame.mixer.Sound("./sounds/golf_hit.wav")
GOLF_SCORED = pygame.mixer.Sound("./sounds/golf_scored.wav")
GOLF_RESPAWN = pygame.mixer.Sound("./sounds/golf_respawn.wav")

#create button instances
RESUME_BTN = button.Button(304, 200, resume_img.convert_alpha(), 1)
QUIT_BTN = button.Button(336, 300, quit_img.convert_alpha(), 1)


font_menu = pygame.font.SysFont("arialblack", 40)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))



#game loop
run = True
while run:
    
  screen.fill((121, 255, 77))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if RESUME_BTN.draw(screen):
        game_paused = False
        resume_iteration = True
      if QUIT_BTN.draw(screen):
        run = False
  else:

    pygame.time.delay(10)

    pos = pygame.mouse.get_pos()

    curr_stokes = font_strokes.render(f'{strokes}', True, (50,50,50))
    screen.blit(curr_stokes, (675,25))


    pygame.draw.circle(screen, (255, 255, 255), (LEVELS[LEVEL_NUM]["HOLE_X_COR"],LEVELS[LEVEL_NUM]["HOLE_Y_COR"]), HOLER+3)
    pygame.draw.circle(screen, (50,50,50), (LEVELS[LEVEL_NUM]["HOLE_X_COR"],LEVELS[LEVEL_NUM]["HOLE_Y_COR"]), HOLER-3)

    # Drawing sand
    for patch in LEVELS[LEVEL_NUM]["SAND_PATCHES"]:
        sandbox = pygame.draw.rect(screen, (212,176,106), patch)
        # Behavior:
        if sandbox.collidepoint(x,y):
            xspeed *= 0.92
            yspeed *= 0.92

    for patch in LEVELS[LEVEL_NUM]["WATER_PATCHES"]:
        water = pygame.draw.rect(screen, (54,84,217), patch)
        # Behavior:
        if water.collidepoint(x,y):
            x = LEVELS[LEVEL_NUM]["BALL_INITIAL_LOCATION_X"]
            y = LEVELS[LEVEL_NUM]["BALL_INITIAL_LOCATION_Y"]
            xspeed = 0
            yspeed = 0
            GOLF_RESPAWN.play()

    for wall in LEVELS[LEVEL_NUM]["L_WALLS"]:
        wall = pygame.draw.rect(screen, WALL_COLOR, wall)
        # Behavior:
        if wall.collidepoint(x+BALL_THICKNESS,y):
            xspeed = -1 *abs(xspeed)

    for wall in LEVELS[LEVEL_NUM]["R_WALLS"]:
        wall = pygame.draw.rect(screen, WALL_COLOR, wall)
        # Behavior:
        if wall.collidepoint(x-BALL_THICKNESS,y):
            xspeed = abs(xspeed)

    for wall in LEVELS[LEVEL_NUM]["T_WALLS"]:
        wall = pygame.draw.rect(screen, WALL_COLOR, wall)
        # Behavior:
        if wall.collidepoint(x,y+BALL_THICKNESS):
            yspeed = -1 *abs(yspeed)

    for wall in LEVELS[LEVEL_NUM]["B_WALLS"]:
        wall = pygame.draw.rect(screen, WALL_COLOR, wall)
        # Behavior:
        if wall.collidepoint(x,y-BALL_THICKNESS):
            yspeed = abs(yspeed)



    

    # Only draw line when stopped
    # POWER
    POWER = max([abs(int((pos[0]-x)/modulator)), abs(int((pos[1]-y)/modulator))])
    BLUE = 255
    LINE_COLOR = POWER * 15
    if LINE_COLOR > 255:
      LINE_COLOR = 255
      BLUE = (255 - LINE_COLOR) + 50
    if abs(xspeed) < 0.1 and abs(yspeed) < 0.1 and not BALL_IN_HOLE:
        pygame.draw.line(screen, (LINE_COLOR, 50, BLUE), (x,y), pos,width=3)

    # ball  
    pygame.draw.circle(screen, (255,255,255), (round(x),round(y)), BALL_THICKNESS)
        # Move the ball
    x += xspeed
    y += yspeed

    # Deceleration
    xspeed = xspeed*0.98
    yspeed = yspeed*0.98

    # Bouncing off screen
    if x > 784 or x < 16:
        xspeed *= -1
    if y >584 or y < 16:
        yspeed *= -1


    # Checks to see if in hole
    if ((x-LEVELS[LEVEL_NUM]["HOLE_X_COR"])**2+(y-LEVELS[LEVEL_NUM]["HOLE_Y_COR"])**2)**0.5 < HOLER_GRAB:
        xspeed *= 0.8
        yspeed *= 0.8
        if abs(yspeed) < 0.1 and abs(xspeed) < 0.1:
            screen.blit(overlay, (0,0))
            winmsg = font_game.render(f'   Level Cleared!   ', True, (255,255,255), (50,50,50))
            screen.blit(winmsg, (0,230))
            xspeed = 0
            yspeed = 0
            BALL_IN_HOLE = True
            GOLF_SCORED.play()
            pygame.display.update()
            time.sleep(2)
            # START Change LEVEL
            if LEVEL_NUM < 3:
              LEVEL_NUM += 1
            else:
              LEVEL_NUM = 1
            x = LEVELS[LEVEL_NUM]["BALL_INITIAL_LOCATION_X"]
            y = LEVELS[LEVEL_NUM]["BALL_INITIAL_LOCATION_Y"]
            strokes = 0
            BALL_IN_HOLE = False
            # END CHANGE LEVEL

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        game_paused = False if game_paused else True

    if event.type == pygame.MOUSEBUTTONUP and not BALL_IN_HOLE and not resume_iteration:
      if abs(yspeed) < 0.1 and abs(xspeed) < 0.1:
        xspeed = int((pos[0]-x)/modulator)
        yspeed = int((pos[1]-y)/modulator)
        strokes += 1
        GOLF_HIT.play()
    if event.type == pygame.MOUSEBUTTONUP and resume_iteration:
      resume_iteration = False

    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()
sys.exit()