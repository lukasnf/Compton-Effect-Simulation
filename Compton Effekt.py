import pygame
import numpy as np
import matplotlib.pyplot as plt
import sys

# Main Setup
pygame.init()
screen = pygame.display.set_mode((1500,800))
pygame.display.set_caption("Compton Effekt")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Main Constants
c = 3e8 #speed of light
m_elektron = 9.11e-31 #electron mass
h = 6.626e-34 # planck-constant
f = 3e19 # x-ray frequency
theta = np.radians(-180) # adjust theta if necessary

# Particle: Electron
class Electron:
    def __init__(self,pos_x,pos_y,v_x,v_y,mass,color,radius,velocity):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.v_x = v_x
        self.v_y = v_y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.velocity = velocity
        self.circle = None

    # Drawing the electon
    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

    # Electron scattering after collision
    def scatter(self,theta):
        a = 10
        if theta == -np.pi:
            a = 1
        self.v_x = self.velocity * np.cos(theta+np.pi/a)
        self.v_y = self.velocity * -np.sin(theta+np.pi/a)
        self.pos_x += self.v_x
        self.pos_y += self.v_y

# Particle: Photon
class Photon:
    def __init__(self,pos_x,pos_y,v_x,v_y,velocity,color,radius,wavelength,frequency):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.v_x = v_x
        self.v_y = v_y
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.wavelength = wavelength
        self.frequency = frequency
        self.circle = None
        self.has_collided = False

    # Moving the Photon to the electron (photon_pos doensnt matter) -> same y-pos highly recommended
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

    # Drawing the photon
    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

    # Photon scattering in a given angle: theta
    def scatter(self,theta):
        self.v_x = self.velocity * np.cos(theta)
        self.v_y = self.velocity * np.sin(theta)
        self.pos_x += self.v_x
        self.pos_y += self.v_y

# Checking for the collision
def check_collision(photon,electron):
    distance = np.sqrt((photon.pos_x-electron.pos_x)**2 + (photon.pos_y-electron.pos_y)**2)
    if distance <= electron.radius + photon.radius:
        return True

# Initializing text
def text(text,font,color,x,y):
    text = font.render(text,True,color)
    screen.blit(text,(x,y))

# Adjusting photon wavelength and frequency based on Compton
def compton_scattering(photon):
    lambda_0 = photon.wavelength
    delta_lambda = (h/(m_elektron*c)*(1-np.cos(theta)))
    new_wavelength = lambda_0 + delta_lambda
    photon.wavelength = new_wavelength
    photon.frequency = c/new_wavelength

# Inistializing particles and flag
photon = Photon(400,400,7,7,np.sqrt(7**2 + 7**2),"white",15,c/f,f) # adjust velocity if necessary
electron = Electron(860,400,5,5,m_elektron,"yellow",20,np.sqrt(5**2 + 5**2)) # adjust velocity if necessary
collision = False

# Creating the graph
x = np.arange(0,np.pi*2,np.pi/2)
y = (h/(m_elektron*c)*(1-np.cos(x))) + c/f
plt.xlabel("collision angles")
plt.ylabel("wavelength")
plt.plot(x,y)
plt.show()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    screen.fill((0,0,0))
    photon.move(electron)
    photon.draw()
    electron.draw()

    if check_collision(photon,electron) and not collision:
        compton_scattering(photon)
        photon.scatter(theta)
        photon.has_collided = True
        collision = True

    if photon.has_collided:
        electron.scatter(theta)

    # Displays photon´s wavelength and energy
    text(f"λ: {photon.wavelength} m",font,"white",1100,90)
    text(f"E: {(h*photon.frequency)*6.242e+18/1000} keV", font, "white", 1100, 110)

    pygame.display.flip()
    clock.tick(60)
