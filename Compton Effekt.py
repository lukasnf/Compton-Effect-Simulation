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
theta = np.radians(-90) #change scatter angle when needed


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
        self.has_collided = False
    def move(self,electron):
        if not self.has_collided:
            delta_x = electron.pos_x - self.pos_x
            delta_y = electron.pos_y - self.pos_y
            direction = np.sqrt(delta_x**2 + delta_y**2)

            if direction != 0:
                vect_x = delta_x/direction
                vect_y = delta_y/direction
                self.pos_x += vect_x * self.v_x
                self.pos_y += vect_y * self.v_y
        else:
            self.pos_x += self.v_x
            self.pos_y += self.v_y

    def erase_trail(self):
        pygame.draw.circle(screen,"black",(self.pos_x,self.pos_y),self.radius)

    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

    def scattering(self,theta): #!!
        self.v_x = self.velocity * np.cos(theta)
        self.v_y = self.velocity * np.sin(theta)


def check_collision(photon,electron):
    distance = np.sqrt((photon.pos_x-electron.pos_x)**2 + (photon.pos_y-electron.pos_y)**2)
    if distance <= electron.radius + photon.radius:
        return True

def text(text,font,color,x,y):
    text = font.render(text,True,color)
    screen.blit(text,(x,y))


def compton_scattering(photon):
    lambda_0 = photon.wavelength
    delta_lambda = (h/(m_elektron*c)*(1-np.cos(theta)))
    new_wavelength = lambda_0 + delta_lambda
    photon.wavelength = new_wavelength


photon = Photon(400,400,7,7,np.sqrt(7**2 + 7**2),"white",15,c/f) #change velocity if needed
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
        photon.scattering(theta)
        photon.has_collided = True
        collision = True

    text(f"λ: {photon.wavelength} m",font,"white",1100,90)
    text(f"p: {(h*f)/photon.velocity} Ns", font, "white", 1100, 110)
    pygame.display.flip()
    clock.tick(60)
