# FILENAME: sakib_module.py

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

def draw_health_bar(): # Promit's module
    pass

def draw_mini_map(): # Promit's module
    pass

def draw_power_up(x, y, z, power_type, rotation): # Promit's module
    pass

def update_power_ups(): # Promit's module
    pass

# ==============================================================================
# PART 3: SAKIB'S IMPLEMENTED CODE
# ==============================================================================

def draw_resource(x, y, z, rotation):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation, 0, 0, 1)
    glRotatef(rotation * 0.7, 1, 0, 0)
    glColor3f(1, 0.9, 0)
    glPushMatrix()
    glScalef(18, 18, 18)
    glBegin(GL_TRIANGLES)
    # Top pyramid
    glVertex3f(1,0,0); glVertex3f(0,1,0); glVertex3f(0,0,1)
    glVertex3f(0,1,0); glVertex3f(-1,0,0); glVertex3f(0,0,1)
    glVertex3f(-1,0,0); glVertex3f(0,-1,0); glVertex3f(0,0,1)
    glVertex3f(0,-1,0); glVertex3f(1,0,0); glVertex3f(0,0,1)
    # Bottom pyramid
    glVertex3f(1,0,0); glVertex3f(0,1,0); glVertex3f(0,0,-1)
    glVertex3f(0,1,0); glVertex3f(-1,0,0); glVertex3f(0,0,-1)
    glVertex3f(-1,0,0); glVertex3f(0,-1,0); glVertex3f(0,0,-1)
    glVertex3f(0,-1,0); glVertex3f(1,0,0); glVertex3f(0,0,-1)
    glEnd()
    glPopMatrix()
    glColor3f(1, 1, 0.5)
    glutSolidSphere(12, 12, 12)
    glPopMatrix()

def update_resources():
    global resources, score, total_points, score_multiplier, frame_counter
    resources[:] = [r for r in resources if frame_counter - r[4] <= RESOURCE_LIFETIME_FRAMES]
    for r in resources[:]:
        r[3] += 5
        dist = math.sqrt((r[0] - player_pos[0])**2 + (r[1] - player_pos[1])**2)
        if dist < 35:
            resources.remove(r)
            points = 8 * score_multiplier
            score += points

def manage_resources():
    global resources, frame_counter
    if len(resources) < MIN_RESOURCES:
        for _ in range(MIN_RESOURCES - len(resources)):
            rx = random.uniform(-GRID_LENGTH//2, GRID_LENGTH//2)
            ry = random.uniform(-GRID_LENGTH//2, GRID_LENGTH//2)
            resources.append([rx, ry, GAME_Z_LEVEL, 0, frame_counter])
    if len(resources) < MAX_RESOURCES and random.random() < 0.1:
        rx = random.uniform(-GRID_LENGTH//2, GRID_LENGTH//2)
        ry = random.uniform(-GRID_LENGTH//2, GRID_LENGTH//2)
        resources.append([rx, ry, GAME_Z_LEVEL, 0, frame_counter])

def spawn_enemy(): # Contains time-based difficulty logic
    global frame_counter, last_enemy_spawn_frame, level
    spawn_interval = max(90 - level * 5, 30) # Difficulty increases with level
    if frame_counter - last_enemy_spawn_frame > spawn_interval:
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left': ex, ey = -GRID_LENGTH + 50, random.uniform(-GRID_LENGTH, GRID_LENGTH)
        elif side == 'right': ex, ey = GRID_LENGTH - 50, random.uniform(-GRID_LENGTH, GRID_LENGTH)
        elif side == 'top': ex, ey = random.uniform(-GRID_LENGTH, GRID_LENGTH), GRID_LENGTH - 50
        else: ex, ey = random.uniform(-GRID_LENGTH, GRID_LENGTH), -GRID_LENGTH + 50
        # For testing, we just add a generic enemy
        enemies.append([ex, ey, GAME_Z_LEVEL, 15, 0])
        last_enemy_spawn_frame = frame_counter

# ==============================================================================
# PART 4: MAIN GAME LOGIC (Modified to call Sakib's functions)
# ==============================================================================

def draw_shapes():
    # Draw player spaceship for context
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(gun_angle, 0, 0, 1)
    glColor3f(0.8, 0.8, 0.95)
    glutSolidSphere(22, 20, 20)
    glPopMatrix()
    
    # Draw resources
    for r in resources:
        draw_resource(r[0], r[1], GAME_Z_LEVEL, r[3])

def keyboardListener(key, x, y):
    global game_over, score, total_points
    if key == b'r' and game_over:
        total_points += score
        # Reset relevant stats for Sakib's module
        score = 0
        game_over = False
        level = 1
        last_level_up_score = 0
        resources.clear()

def idle():
    global frame_counter, level, last_level_up_score, score_multiplier
    if game_over:
        glutPostRedisplay()
        return
    frame_counter += 1
    
    # Level Progression and Score Multiplier Logic
    if score - last_level_up_score >= 15:
        level += 1
        last_level_up_score = score
        score_multiplier = level
        
    # Time-based Difficulty
    spawn_enemy()
    
    # Resource Management
    manage_resources()
    update_resources()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # A simple camera setup for testing
    gluLookAt(0, 400, 400, 0, 0, 0, 0, 0, 1)
    
    draw_shapes()
    
    # Sakib's UI elements
    draw_text(15, WINDOW_HEIGHT - 35, f"SCORE: {score}  |  LEVEL: {level}  |  MULTIPLIER: x{score_multiplier}", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(15, WINDOW_HEIGHT - 65, f"*** TOTAL CAREER POINTS: {total_points + score} ***", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(15, WINDOW_HEIGHT - 140, f"OBJECTS: {len(resources)}/{MAX_RESOURCES} Crystals | {len(enemies)} Enemies")
    
    if game_over:
        draw_text(WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 20, f"TOTAL CAREER POINTS: {total_points + score}", GLUT_BITMAP_TIMES_ROMAN_24)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Sakib's Module")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()