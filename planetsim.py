import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1080, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")

PLANET_MASS = 250
SHIP_MASS = 10
G = 5
FPS = 60
PLANET_SIZE = 75
OBJ_SIZE = 10
VEL_SCALE = 100

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

pygame.font.init() 
big_font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 20)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        #win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))
        pygame.draw.circle(win, BLUE, (self.x, self.y), PLANET_SIZE)

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.force = 0
        self.mass = mass
        self.color = BLUE
        self.passed_points = []
        self.point_id = 0

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        self.force = (G * self.mass * planet.mass) / distance ** 2
        
        acceleration = self.force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y
        
        self.point_id += 1
        self.passed_points.append([self.x, self.y, self.point_id])
    
    def draw(self):
        
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), OBJ_SIZE, width = 5)
        pygame.draw.circle(win, BLACK, (int(self.x), int(self.y)), OBJ_SIZE - 5)
        txt1 = small_font.render(('V: '+str(round( math.sqrt( self.vel_x**2 + self.vel_y**2 ), 3 ))), True, WHITE)
        txt2 = small_font.render(('F: '+str(round(self.force,3))), True, WHITE)
        win.blit(txt1, (self.x + 25, self.y))  
        win.blit(txt2, (self.x + 25, self.y - 20))  
        
    def draw_lines(self):
        for i in self.passed_points:
            if i[2] % 2 == 0:
                pygame.draw.circle(win, GRAY, (i[0], i[1]), 1)
               
    def update_color(self):
        vel = math.sqrt(self.vel_x**2 + self.vel_y**2)
        self.color = get_color(vel)


def clamp(n, min, max):
  if min < n < max:
    return n
  elif n >= max:
    return max
  else:
    return min

def mixrgb(fac, rgb1, rgb2):
  return tuple([c2 * fac + c1 * (1 - fac) for c1, c2 in zip(rgb1, rgb2)])


def get_color(speed):
  return mixrgb(clamp(speed / 3.5, 0, 1), (0, 0, 255), (255, 0, 0))


def create_ship(location, mouse):

    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (t_x - m_x) / VEL_SCALE
    vel_y = (t_y - m_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)
        num_ships = 0
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.fill(BLACK)         

        if temp_obj_pos:
            pygame.draw.line(win, RED, temp_obj_pos, mouse_pos, 3)
            pygame.draw.circle(win, BLUE, temp_obj_pos, OBJ_SIZE, width = 5)
            pygame.draw.circle(win, BLACK, temp_obj_pos, OBJ_SIZE - 5)
        
        for obj in objects[:]:
            obj.draw_lines()
            
        for obj in objects[:]:
            num_ships += 1
            obj.draw()
            obj.update_color()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE + 5
            if off_screen or collided:
                objects.remove(obj)

        planet.draw()
        txt = big_font.render(('Objects: '+str(num_ships)), True, WHITE)
        win.blit(txt, (75, 75))  
        
        pygame.display.update()
         
    
    pygame.quit()

if __name__ == "__main__":
    main()