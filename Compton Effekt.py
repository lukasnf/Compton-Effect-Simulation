import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEMOTION
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
f = 3e19 # gamma-ray frequency


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

    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

    # Electron scattering after collision
    def scatter(self,theta,photon):
        lambda_i = c/f
        lambda_f = (h/(m_elektron*c)*(1-np.cos(theta))) + c/f
        p_i = h/lambda_i
        p_f = h/lambda_f
        beta = np.arctan((p_f * np.sin(theta)/p_i-p_f*np.cos(theta)))

        self.v_x = self.velocity * np.cos(-beta)
        self.v_y = self.velocity * np.sin(-beta)
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
    # wasnt tested with dfferent y-pos
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

    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

    # Photon scattering in a given angle: theta
    def scatter(self,theta):
        self.v_x = self.velocity * np.cos(theta)
        self.v_y = self.velocity * np.sin(theta)
        self.pos_x += self.v_x
        self.pos_y += self.v_y

# SLider to adjust theta, made it with a tutorial :)
class Slider:
    def __init__(self,pos_x,pos_y,width,initial_val,min,max,color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.initial_val = initial_val
        self.val = initial_val
        self.min = min
        self.max = max
        self.color = color
        self.circle_x = self.pos_x + (self.val - self.min) / (self.max - self.min) * self.width
        self.line = None
        self.circle = None

    def draw(self):
        self.line = pygame.draw.line(screen,self.color,(self.pos_x,self.pos_y),(self.pos_x + self.width,self.pos_y),5)
        self.circle = pygame.draw.circle(screen,self.color,(self.circle_x,self.pos_y),10)

    def move_knob(self,event):
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] == 1:
                mouse_pos,_ = pygame.mouse.get_pos()
                if self.pos_x <= mouse_pos <= self.pos_x+self.width:
                    self.circle_x = mouse_pos
                    self.val = self.min+(self.max-self.min)/self.width * (mouse_pos-self.pos_x)

    def angle(self):
        return np.radians(self.val)

# Checking for the collision
def check_collision(photon,electron):
    distance = np.sqrt((photon.pos_x-electron.pos_x)**2 + (photon.pos_y-electron.pos_y)**2)
    if distance <= electron.radius + photon.radius:
        return True

def text(text,font,color,x,y):
    text = font.render(text,True,color)
    screen.blit(text,(x,y))

# Calculating photon wavelength and frequency based on Compton
def compton_scattering(photon):
    lambda_0 = photon.wavelength
    delta_lambda = (h/(m_elektron*c)*(1-np.cos(theta)))
    new_wavelength = lambda_0 + delta_lambda
    photon.wavelength = new_wavelength
    photon.frequency = c/new_wavelength

# Reset function, Initializing particles and flag
def reset():
    global photon, electron, collision
    photon = Photon(100, 450, 7, 7, np.sqrt(7**2 + 7**2), "white", 15, c / f, f)# adjust velocity if necessary
    electron = Electron(760, 450, 5, 5, m_elektron, "yellow", 20, np.sqrt(5**2 + 5**2))# adjust velocity if necessary
    collision = False


reset()
slider = Slider(100, 700, 400, 90, 0, 180, "white")
#Graph
x = np.linspace(0, 2*np.pi, 100)
y = (h/(m_elektron*c)*(1-np.cos(x))) + c/f
plt.xlabel("collision angles")
plt.ylabel("wavelength")
plt.plot(x,y)
plt.show()

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset()
        slider.move_knob(event)

    theta = slider.angle()
    screen.fill("black")
    photon.move(electron)
    photon.draw()
    electron.draw()
    slider.draw()

    if check_collision(photon,electron) and not collision:
        compton_scattering(photon)
        photon.scatter(theta)
        photon.has_collided = True
        collision = True

    if photon.has_collided:
        electron.scatter(theta,photon)

    text(f"λ: {photon.wavelength} m",font,"white",1100,90)
    text(f"E: {(h*photon.frequency)*6.242e+18/1000} keV", font, "white", 1100, 110)
    text("Space to restart",font,"white",100,110)
    text(f"θ: {slider.val}°",font,"white",1100,130)



    pygame.display.flip()
    clock.tick(60)
