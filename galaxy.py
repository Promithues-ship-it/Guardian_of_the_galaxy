# FILENAME: promit_module.py

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

# ==============================================================================
# PART 1: COMMON SCAFFOLDING (Included for all members to run independently)
# ==============================================================================

# Window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 720
GRID_LENGTH = 600
fovY = 120

# Camera settings
camera_pos = (0, 500, 500)
first_person_view = False

# Player variables
gun_angle = 0
player_pos = [0, 200, 0]
player_speed = 6
player_max_health = 100
player_health = 100
weapon_level = 1
speed_boost_active = False
speed_boost_end_frame = 0
shield_active = False
shield_end_frame = 0
cheat_mode = False

# Game stats
score = 0
total_points = 0
missed_bullets = 0
lives = 10
game_over = False
level = 1
last_level_up_score = 0
score_multiplier = 1
frame_counter = 0
last_enemy_spawn_frame = 0
last_boss_spawn_frame = 0
last_auto_fire_frame = 0
last_manual_fire_frame = 0

# Game objects
enemies = []
enemy_spaceships = []
bullets = []
enemy_bullets = []
power_ups = []
resources = []
explosions = []
boss_enemies = []

# Animation variables
earth_angle = 0
moon_angle = 0

# Power-up types
HEALTH_POWERUP, WEAPON_POWERUP, SPEED_POWERUP, SHIELD_POWERUP = 0, 1, 2, 3

# Constants
MAX_POWERUPS = 5
POWERUP_LIFETIME_FRAMES = 900
MAX_RESOURCES = 5
MIN_RESOURCES = 2
RESOURCE_LIFETIME_FRAMES = 300
GAME_Z_LEVEL = 0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# ==============================================================================
# PART 2: PLACEHOLDER FUNCTIONS (For other members' modules)
# ==============================================================================

def draw_healing_center(): # Nashid's module
    pass

def draw_enemy_spaceship(x, y, z, health): # Nashid's module
    pass

def draw_boss_enemy(x, y, z, health): # Nashid's module
    pass

def update_cheat_mode(): # Nashid's module
    pass
    
def shoot_bullets(): # Nashid's module
    pass

def update_enemy_spaceships(): # Nashid's module
    pass

def update_boss_enemies(): # Nashid's module
    pass
    
def update_bullets(): # Nashid's module
    pass
    
def update_enemy_bullets(): # Nashid's module
    pass

def draw_resource(x, y, z, rotation): # Sakib's module
    pass

def update_resources(): # Sakib's module
    pass

def manage_resources(): # Sakib's module
    pass

# ==============================================================================
# PART 3: PROMIT'S IMPLEMENTED CODE
# ==============================================================================

def draw_health_bar():
    bar_width, bar_height, bar_x, bar_y = 250, 25, 15, WINDOW_HEIGHT - 200
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    health_ratio = player_health / player_max_health
    if health_ratio > 0.6: glColor3f(0, 1, 0)
    elif health_ratio > 0.3: glColor3f(1, 1, 0)
    else: glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y)
    glVertex2f(bar_x + bar_width * health_ratio, bar_y)
    glVertex2f(bar_x + bar_width * health_ratio, bar_y + bar_height)
    glVertex2f(bar_x, bar_y + bar_height)
    glEnd()
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    glVertex2f(bar_x, bar_y); glVertex2f(bar_x + bar_width, bar_y)
    glVertex2f(bar_x + bar_width, bar_y + bar_height); glVertex2f(bar_x, bar_y + bar_height)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_mini_map():
    map_size, map_x, map_y = 150, WINDOW_WIDTH - 150 - 10, 10
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor4f(0, 0, 0, 0.7)
    glEnable(GL_BLEND)
    glBegin(GL_QUADS)
    glVertex2f(map_x, map_y); glVertex2f(map_x + map_size, map_y)
    glVertex2f(map_x + map_size, map_y + map_size); glVertex2f(map_x, map_y + map_size)
    glEnd()
    glColor3f(0, 1, 1)
    glBegin(GL_LINES)
    glVertex2f(map_x, map_y); glVertex2f(map_x + map_size, map_y)
    glVertex2f(map_x + map_size, map_y + map_size); glVertex2f(map_x, map_y + map_size)
    glEnd()
    scale, center_x, center_y = map_size / (GRID_LENGTH * 2), map_x + map_size / 2, map_y + map_size / 2
    glColor3f(0, 1, 0); glPointSize(8); glBegin(GL_POINTS); glVertex2f(center_x, center_y); glEnd() # Center
    px, py = center_x + player_pos[0] * scale, center_y + player_pos[1] * scale
    if map_x <= px <= map_x + map_size and map_y <= py <= map_y + map_size:
        glColor3f(0, 1, 1); glPointSize(6); glBegin(GL_POINTS); glVertex2f(px, py); glEnd() # Player
    glDisable(GL_BLEND)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_power_up(x, y, z, power_type, rotation):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation, 1, 1, 0)
    if power_type == HEALTH_POWERUP:
        glColor3f(1, 0, 0); glutSolidCube(25)
        glColor3f(1, 1, 1); glPushMatrix(); glScalef(0.2, 1.8, 0.2); glutSolidCube(18); glPopMatrix()
        glPushMatrix(); glScalef(1.8, 0.2, 0.2); glutSolidCube(18); glPopMatrix()
    elif power_type == WEAPON_POWERUP:
        glColor3f(1, 1, 0); glutSolidCube(25)
    elif power_type == SPEED_POWERUP:
        glColor3f(0, 0.5, 1); glutSolidCube(25)
    elif power_type == SHIELD_POWERUP:
        glColor3f(1, 0, 1); glutSolidCube(25)
    glPopMatrix()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 2500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if first_person_view:
        look_x = player_pos[0] + 100 * math.cos(math.radians(gun_angle))
        look_y = player_pos[1] + 100 * math.sin(math.radians(gun_angle))
        pos_x = player_pos[0] - 25 * math.cos(math.radians(gun_angle))
        pos_y = player_pos[1] - 25 * math.sin(math.radians(gun_angle))
        gluLookAt(pos_x, pos_y, player_pos[2] + 40, look_x, look_y, player_pos[2], 0, 0, 1)
    else:
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 0, 1)

def update_power_ups():
    global power_ups, player_health, weapon_level, speed_boost_active, speed_boost_end_frame, shield_active, shield_end_frame, frame_counter
    power_ups[:] = [p for p in power_ups if frame_counter - p[5] <= POWERUP_LIFETIME_FRAMES]
    for p in power_ups[:]:
        p[4] += 4
        if math.sqrt((p[0] - player_pos[0])**2 + (p[1] - player_pos[1])**2) < 40:
            power_ups.remove(p)
            if p[3] == HEALTH_POWERUP: player_health = min(player_max_health, player_health + 35)
            elif p[3] == WEAPON_POWERUP: weapon_level = min(5, weapon_level + 1)
            elif p[3] == SPEED_POWERUP:
                speed_boost_active = True
                speed_boost_end_frame = frame_counter + 600
            elif p[3] == SHIELD_POWERUP:
                shield_active = True
                shield_end_frame = frame_counter + 720
                
# ==============================================================================
# PART 4: MAIN GAME LOGIC (Modified to call Promit's functions)
# ==============================================================================

def draw_shapes():
    # Draw player spaceship for camera context
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(gun_angle, 0, 0, 1)
    glColor3f(0.8, 0.8, 0.95)
    glutSolidSphere(22, 20, 20)
    glPopMatrix()
    
    # Draw power-ups
    for p in power_ups:
        draw_power_up(p[0], p[1], GAME_Z_LEVEL, p[3], p[4])

def keyboardListener(key, x, y):
    global first_person_view, speed_boost_active, speed_boost_end_frame, frame_counter
    if game_over: return
    if key == b'v': first_person_view = not first_person_view
    elif key == b'c':
        if not speed_boost_active:
            speed_boost_active = True
            speed_boost_end_frame = frame_counter + 360

def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_LEFT: cx -= 15
    elif key == GLUT_KEY_RIGHT: cx += 15
    elif key == GLUT_KEY_UP: cz += 15
    elif key == GLUT_KEY_DOWN: cz -= 15
    camera_pos = (cx, cy, cz)

def idle():
    global frame_counter, speed_boost_active, speed_boost_end_frame, shield_active, shield_end_frame
    if game_over:
        glutPostRedisplay()
        return
    frame_counter += 1
    
    if speed_boost_active and frame_counter > speed_boost_end_frame: speed_boost_active = False
    if shield_active and frame_counter > shield_end_frame: shield_active = False

    # Spawn some powerups for testing purposes
    if len(power_ups) < MAX_POWERUPS and random.random() < 0.01:
        px = random.uniform(-GRID_LENGTH//2, GRID_LENGTH//2)
        py = random.uniform(-GRID_LENGTH//2, GRID_LENGTH//2)
        ptype = random.randint(0, 3)
        power_ups.append([px, py, GAME_Z_LEVEL, ptype, 0, frame_counter])
        
    update_power_ups()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupCamera()
    draw_shapes()
    
    # Promit's UI elements
    draw_health_bar()
    draw_mini_map()
    draw_text(15, WINDOW_HEIGHT - 35, f"SCORE: {score}", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(15, WINDOW_HEIGHT - 90, f"HEALTH: {int(player_health)}/{player_max_health}")
    effects_text = ""
    if speed_boost_active: effects_text += " | SPEED BOOST ACTIVE"
    if shield_active: effects_text += " | SHIELD ACTIVE"
    draw_text(15, WINDOW_HEIGHT - 115, effects_text)
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Promit's Module")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()