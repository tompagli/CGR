import pygame 
import math
import random


pygame.init()
height = 560
width = 840
screen = pygame.display.set_mode((width,height)) 

pygame.display.set_caption("Tempestade de Areia")

# Background
background = pygame.image.load('Background.png')

# Airplane
planeSpeed = 1
planeIMG = pygame.image.load('Plane.png') 
planeWidthIMG = 100  
planeX = width * 0.55 
planeY = height * 0.75 
plane_changeX = 0 

# Drone
droneSpeed = 0.5

# Drone attributes
DroneIMG = []
DroneWidthIMG = []
DroneX = []
DroneY = []
Drone_ChangeX = []
Drone_ChangeY = []
# Drone quantity
Dronequant = 4
# Drone data
for i in range(Dronequant):
    DroneIMG.append(pygame.image.load('Drone.png')) 
    DroneIMG.append(pygame.image.load('Drone2.png')) 
    DroneWidthIMG.append(50) 
    DroneX.append(random.randint(0, width - DroneWidthIMG[i]))  
    DroneY.append(height * 0.01) 
    Drone_ChangeX.append(random.randint(-1, 1) * droneSpeed * 1) 
    Drone_ChangeY.append(random.randint(0, 5) * 0.06)  

# Bullet
bulletSpeed = 3
BulletIMG = pygame.image.load('Bullet.png')
BulletX = 0
BulletY = height * 0.90
Bullet_ChangeX = 0 
Bullet_ChangeY = bulletSpeed 
BulletState = "Loaded"

# Collision func
def Collision(X1,Y1,X2,Y2):
    Distance = math.sqrt(math.pow(X1 - X2, 2) + (math.pow(Y1 - Y2, 2)))
    if Distance <= 50  :
        ExplosionIMG = pygame.image.load('Explosion.png') 
        screen.blit(ExplosionIMG, (BulletX, BulletY))
        return True
    else:
        return False


def Player(x,y):
    screen.blit(planeIMG, (x,y)) 
def Enemy(x,y,i):
    screen.blit(DroneIMG[i], (x,y)) 
def ShootBullet(x,y): 
    global BulletState
    BulletState = "Unloaded"
    screen.blit(BulletIMG, (x,y))

# game itself
running = True
while running:
    screen.fill((255,255,255)) 
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if(event.type == pygame.QUIT): 
            running = False 

    
        if(event.type == pygame.KEYDOWN): 
            if(event.key == pygame.K_a): 
                plane_changeX -= planeSpeed
            if(event.key == pygame.K_d): 
                plane_changeX += planeSpeed
            if(event.key == pygame.K_SPACE): 
                if(BulletState == "Loaded"): 
                    BulletX = planeX + planeWidthIMG/4  
                    ShootBullet(BulletX,BulletY) 
        if(event.type == pygame.KEYUP): 
            if(event.key == pygame.K_a):
                plane_changeX = 0
            if(event.key == pygame.K_d):
                plane_changeX = 0

    
    planeX = planeX + plane_changeX  

    
    if (BulletY < 0): 
        BulletY = height * 0.90
        BulletState = "Loaded"   
    if (BulletState == "Unloaded"): 
        ShootBullet(BulletX,BulletY)
        BulletY -= Bullet_ChangeY

    for i in range(Dronequant):
        
        DroneX[i] = DroneX[i] + Drone_ChangeX[i]  
        DroneY[i] = DroneY[i] + Drone_ChangeY[i] 
        
        if(DroneX[i] < 0):
            Drone_ChangeX[i] = droneSpeed
    
        if(width - DroneWidthIMG[i] < DroneX[i]): 
            Drone_ChangeX[i] = -droneSpeed
    
        if(planeY <= DroneY[i]):
            running = False  
        
        Result = Collision(DroneX[i],DroneY[i],BulletX,BulletY)
        if (Result):
            BulletY = height * 0.90
            BulletState = "Loaded" 
            DroneX[i] = random.randint(0, width - DroneWidthIMG[i]) 
            DroneY[i] = height * 0.01 
        Enemy(DroneX[i],DroneY[i], i) 

    
    if(planeX < 0):
        planeX = 0.1
    if(width - planeWidthIMG < planeX):
        planeX = width - planeWidthIMG 
    
     
    Player(planeX,planeY)
    pygame.display.update()
