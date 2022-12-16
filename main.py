import pygame
import sys
pygame.init()
wn = pygame.display.set_mode((800,600))
FPS = 240

clock = pygame.time.Clock()

HOLER = 25
BALL_THICKNESS = 10
xspeed = 0
yspeed = 0

BALL_INITIAL_LOCATION_X = 500
BALL_INITIAL_LOCATION_Y = 150

x = BALL_INITIAL_LOCATION_X
y = BALL_INITIAL_LOCATION_Y

strokes = 0
modulator = 20


HOLE_X_COR = 550
HOLE_Y_COR = 450
WALL_COLOR = (204, 102, 0)
sand = [(200,300,100,100),(300,400,50,50)]
waters = [(250,100,75,100)]
lwalls = [(600,50,30,200), (330,250,30,100), (600,350,30,200)]
rwalls = [(100,50,30,500)]
twalls = [(100,520,500,30), (330,250,300,30)]
bwalls = [(100,50,500,30), (330,350,300,30)]

font = pygame.font.Font('BRLNSB.TTF', 30)

while True:
  wn.fill((121, 255, 77))
  pygame.time.delay(10)

  pos = pygame.mouse.get_pos()

  pygame.draw.circle(wn, (22,22,22), (HOLE_X_COR,HOLE_Y_COR), HOLER)
  pygame.draw.circle(wn, (0,0,0), (HOLE_X_COR,HOLE_Y_COR), HOLER-3)

  # Drawing sand
  for patch in sand:
    sandbox = pygame.draw.rect(wn, (212,176,106), patch)
    # Behavior:
    if sandbox.collidepoint(x,y):
      xspeed *= 0.92
      yspeed *= 0.92

  for patch in waters:
    water = pygame.draw.rect(wn, (54,84,217), patch)
    # Behavior:
    if water.collidepoint(x,y):
      x = BALL_INITIAL_LOCATION_X
      xspeed = 0
      y = BALL_INITIAL_LOCATION_Y
      yspeed = 0

  for wall in lwalls:
    wall = pygame.draw.rect(wn, WALL_COLOR, wall)
    # Behavior:
    if wall.collidepoint(x+BALL_THICKNESS,y):
      xspeed = -1 *abs(xspeed)

  for wall in rwalls:
    wall = pygame.draw.rect(wn, WALL_COLOR, wall)
    # Behavior:
    if wall.collidepoint(x-BALL_THICKNESS,y):
      xspeed = abs(xspeed)

  for wall in twalls:
    wall = pygame.draw.rect(wn, WALL_COLOR, wall)
    # Behavior:
    if wall.collidepoint(x,y+BALL_THICKNESS):
      yspeed = -1 *abs(yspeed)

  for wall in bwalls:
    wall = pygame.draw.rect(wn, WALL_COLOR, wall)
    # Behavior:
    if wall.collidepoint(x,y-BALL_THICKNESS):
      yspeed = abs(yspeed)


  

  # Only draw line when stopped
  if abs(xspeed) < 0.5 and abs(yspeed) < 0.5:
    pygame.draw.line(wn, (0,0,0), (x,y), pos,width=3)

  # ball  
  pygame.draw.circle(wn, (255,255,255), (round(x),round(y)), BALL_THICKNESS)

  # Hit the ball on click
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONUP:
      xspeed = int((pos[0]-x)/modulator)
      yspeed = int((pos[1]-y)/modulator)
      print(xspeed, yspeed)
      strokes += 1

    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

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
  if ((x-HOLE_X_COR)**2+(y-HOLE_Y_COR)**2)**0.5 < HOLER:
    xspeed *= 0.97
    yspeed *= 0.97
    if abs(yspeed) < 0.1 and abs(xspeed) < 0.1:
      winmsg = font.render(f'Nice! {strokes} strokes!', True, (255,255,255), (24,110,47))
      wn.blit(winmsg, (150,400))

  pygame.display.update()
  clock.tick(FPS)
