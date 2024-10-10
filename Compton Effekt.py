import pygame
import numpy as np
import sys

pygame.init()
screen = pygame.display.set_mode((1500,800))
pygame.display.set_caption("Compton Effekt")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

c = 3e8
m_elektron = 9.11e-31
h = 6.626e-34
f = 3e19
theta = 180 * ((2*np.pi)/360) #change angle if needed


class Electron:
    def __init__(self,pos_x,pos_y,v_x,v_y,mass,color,radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.v_x = v_x
        self.v_y = v_y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.circle = None
    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

class Photon:
    def __init__(self,pos_x,pos_y,v_x,v_y,velocity,color,radius,wavelength):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.v_x = v_x
        self.v_y = v_y
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.wavelength = wavelength
        self.circle = None
    def move(self,electron):
        delta_x = electron.pos_x - self.pos_x
        delta_y = electron.pos_y - self.pos_y
        direction = np.sqrt(delta_x**2 + delta_y**2)

        if direction != 0:
            vect_x = delta_x/direction
            vect_y = delta_y/direction
            self.pos_x += vect_x * self.v_x
            self.pos_y += vect_y * self.v_y

    def erase_trail(self):
        pygame.draw.circle(screen,"black",(self.pos_x,self.pos_y),self.radius)
    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)
    def scattering(self,electron):
        if check_collision(self, electron):
            self.v_y = self.velocity * np.sin(theta)
            self.v_x = self.velocity * np.cos(theta)
            self.pos_x += self.v_x
            self.pos_y += self.v_y


def check_collision(photon,electron):
    distance = np.sqrt((photon.pos_x-electron.pos_x)**2 + (photon.pos_y-electron.pos_y)**2)
    if distance <= electron.radius + photon.radius:
        return True
    if distance == electron.radius + photon.radius:
        return False

def text(text,font,color,x,y):
    text = font.render(text,True,color)
    screen.blit(text,(x,y))


def compton_scattering(photon):
    lambda_0 = photon.wavelength
    delta_lambda = (h/(m_elektron*c)*(1-np.cos(theta)))
    new_wavelength = lambda_0 + delta_lambda
    photon.wavelength = new_wavelength

def collision_angle(photon,electron):
    delta_x = electron.pos_x - photon.pos_x
    delta_y = electron.pos_y - photon.pos_y
    if delta_x == 0:
        if delta_y > 0:
            return 90 * (180/np.pi)
        else: return -90 * (180/np.pi)
    angle = np.arctan2(delta_y,delta_x)
    print(f"delta_x: {delta_x}, delta_y: {delta_y}")
    return angle * (180/np.pi)



photon = Photon(860,600,10,10,np.sqrt(10**2 + 10**2),"white",15,c/f) #change velocity if needed
electron = Electron(860,400,0,0,m_elektron,"yellow",20)
collision = False

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    screen.fill((0,0,0))
    photon.erase_trail()
    photon.move(electron)
    photon.draw()
    electron.draw()
    if check_collision(photon,electron) and not collision:
        electron.color = "green"
        compton_scattering(photon)
        collision = True
        photon.scattering(electron)
        print(collision_angle(photon, electron))



    text(f"λ: {photon.wavelength} m",font,"white",1100,90)
    text(f"p: {(h*f)/photon.velocity} Ns", font, "white", 1100, 110)
    pygame.display.flip()
    clock.tick(60)
