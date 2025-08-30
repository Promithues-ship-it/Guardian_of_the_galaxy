# FILENAME: nashid_module.py

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

def draw_health_bar(): # Promit's module
    pass

def draw_mini_map(): # Promit's module
    pass

def draw_power_up(x, y, z, power_type, rotation): # Promit's module
    pass

def draw_resource(x, y, z, rotation): # Sakib's module
    pass

def update_power_ups(): # Promit's module
    pass

def update_resources(): # Sakib's module
    pass

def manage_resources(): # Sakib's module
    pass

# ==============================================================================
# PART 3: NASHID'S IMPLEMENTED CODE
# ==============================================================================

def draw_healing_center():
    glPushMatrix()
    glTranslatef(0, 0, GAME_Z_LEVEL)
    glColor3f(0, 1, 0)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glRotatef(earth_angle * 2, 0, 0, 1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 80, 80, 8, 24, 1)
    glPopMatrix()
    glColor3f(0, 0.9, 0)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glRotatef(-earth_angle * 3, 0, 0, 1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 60, 60, 8, 20, 1)
    glPopMatrix()
    glColor3f(0, 0.8, 0)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glRotatef(earth_angle * 4, 0, 0, 1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 40, 40, 8, 16, 1)
    glPopMatrix()
    glColor3f(0, 1, 0.5)
    glutSolidSphere(25, 20, 20)
    dist_to_center = math.sqrt(player_pos[0]**2 + player_pos[1]**2)
    if dist_to_center < 150:
        glColor3f(0, 1, 0.7)
        for i in range(12):
            angle = i * 30 + earth_angle * 5
            x = 70 * math.cos(math.radians(angle))
            y = 70 * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, y, 15)
            glutSolidSphere(4, 10, 10)
            glPopMatrix()
    glPopMatrix()

def draw_enemy_spaceship(x, y, z, health):
    glPushMatrix()
    glTranslatef(x, y, z)
    health_ratio = health / 30.0
    glColor3f(1, 0.2 + 0.8 * health_ratio, 0.2 + 0.8 * health_ratio)
    glutSolidCube(22)
    glColor3f(0.8, 0, 0)
    glPushMatrix()
    glTranslatef(18, 0, 0)
    glScalef(0.6, 2.5, 0.4)
    glutSolidCube(12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-18, 0, 0)
    glScalef(0.6, 2.5, 0.4)
    glutSolidCube(12)
    glPopMatrix()
    glColor3f(0.2, 0.2, 1)
    glutSolidSphere(8, 12, 12)
    glPopMatrix()

def draw_boss_enemy(x, y, z, health):
    glPushMatrix()
    glTranslatef(x, y, z)
    health_ratio = health / 150.0
    glColor3f(0.5 + 0.5 * health_ratio, 0, 0.5 + 0.5 * health_ratio)
    glutSolidSphere(45, 24, 24)
    glColor3f(1, 0, 1)
    for i in range(12):
        angle = i * 30 + earth_angle * 3
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)
        glTranslatef(55, 0, 0)
        glScalef(2.5, 0.6, 0.6)
        glutSolidCube(12)
        glPopMatrix()
    glColor3f(1, 0.5, 1)
    glPushMatrix()
    glRotatef(-earth_angle * 5, 0, 0, 1)
    glutSolidSphere(20, 16, 16)
    glPopMatrix()
    glPopMatrix()

def find_closest_enemy():
    min_dist = float('inf')
    closest = None
    for e in enemies:
        dist = (e[0] - player_pos[0])**2 + (e[1] - player_pos[1])**2
        if dist < min_dist:
            min_dist = dist
            closest = {'x': e[0], 'y': e[1]}
    for e in enemy_spaceships:
        dist = (e[0] - player_pos[0])**2 + (e[1] - player_pos[1])**2
        if dist < min_dist:
            min_dist = dist
            closest = {'x': e[0], 'y': e[1]}
    for b in boss_enemies:
        dist = (b[0] - player_pos[0])**2 + (b[1] - player_pos[1])**2
        if dist < min_dist:
            min_dist = dist
            closest = {'x': b[0], 'y': b[1]}
    return closest

def update_cheat_mode():
    global gun_angle, last_auto_fire_frame, frame_counter
    if not cheat_mode: return
    closest = find_closest_enemy()
    if closest:
        dx = closest['x'] - player_pos[0]
        dy = closest['y'] - player_pos[1]
        target_angle = math.degrees(math.atan2(dy, dx))
        angle_diff = (target_angle - gun_angle + 180) % 360 - 180
        gun_angle += angle_diff * 0.2
        if abs(angle_diff) < 15 and frame_counter - last_auto_fire_frame > 25:
            shoot_bullets()
            last_auto_fire_frame = frame_counter
    else:
        gun_angle += 1

def shoot_bullets():
    global bullets
    bx = player_pos[0] + 35 * math.cos(math.radians(gun_angle))
    by = player_pos[1] + 35 * math.sin(math.radians(gun_angle))
    bz = GAME_Z_LEVEL
    if weapon_level == 1:
        bullets.append([bx, by, bz, gun_angle, 15])
    elif weapon_level == 2:
        bullets.append([bx, by, bz, gun_angle, 15])
        bullets.append([bx, by, bz, gun_angle + 12, 15])
        bullets.append([bx, by, bz, gun_angle - 12, 15])
    elif weapon_level == 3:
        for i in range(5): bullets.append([bx, by, bz, gun_angle + (i - 2) * 18, 15])
    elif weapon_level == 4:
        for i in range(7): bullets.append([bx, by, bz, gun_angle + (i - 3) * 22, 15])
    else:
        for i in range(16): bullets.append([bx, by, bz, gun_angle + i * 22.5, 15])

def spawn_boss():
    global frame_counter, last_boss_spawn_frame, level
    if level >= 3 and level % 3 == 0 and frame_counter - last_boss_spawn_frame > 1200 and len(boss_enemies) == 0:
        bx = random.uniform(-200, 200)
        by = random.uniform(-200, 200)
        boss_enemies.append([bx, by, GAME_Z_LEVEL, 150, 0, 0])
        last_boss_spawn_frame = frame_counter

def update_enemy_spaceships():
    global enemy_spaceships, enemy_bullets, explosions, player_health, shield_active, game_over, frame_counter
    for e in enemy_spaceships[:]:
        dx, dy = player_pos[0] - e[0], player_pos[1] - e[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            speed = 1.0 + level * 0.05
            e[0] += (dx / dist) * speed
            e[1] += (dy / dist) * speed
        if dist < 300 and frame_counter - e[4] > 180:
            angle = math.degrees(math.atan2(dy, dx))
            enemy_bullets.append([e[0], e[1], GAME_Z_LEVEL, angle, 4])
            e[4] = frame_counter
        if dist < 30:
            enemy_spaceships.remove(e)
            explosions.append([e[0], e[1], GAME_Z_LEVEL, 35, 30])
            if not shield_active:
                player_health -= 8
                if player_health <= 0: game_over = True

def update_boss_enemies():
    global boss_enemies, enemy_bullets, frame_counter
    for b in boss_enemies[:]:
        b[5] += 1
        if b[5] % 360 < 180:
            angle = b[5] * 1
            b[0] = 250 * math.cos(math.radians(angle))
            b[1] = 250 * math.sin(math.radians(angle))
        else:
            dx, dy = player_pos[0] - b[0], player_pos[1] - b[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                speed = 0.3
                b[0] += (dx / dist) * speed
                b[1] += (dy / dist) * speed
        if frame_counter - b[4] > 150:
            base_angle = math.degrees(math.atan2(player_pos[1] - b[1], player_pos[0] - b[0]))
            for i in range(5):
                angle = base_angle + (i - 2) * 25
                enemy_bullets.append([b[0], b[1], GAME_Z_LEVEL, angle, 4])
            b[4] = frame_counter

def update_bullets():
    global bullets, enemies, enemy_spaceships, boss_enemies, score, explosions, missed_bullets, score_multiplier
    for b in bullets[:]:
        b[0] += b[4] * math.cos(math.radians(b[3]))
        b[1] += b[4] * math.sin(math.radians(b[3]))
        hit = False
        for e in enemies[:]:
            if math.sqrt((e[0] - b[0])**2 + (e[1] - b[1])**2) < e[3] + 8:
                enemies.remove(e)
                bullets.remove(b)
                explosions.append([e[0], e[1], GAME_Z_LEVEL, e[3] * 1.5, 25])
                score += 1 * score_multiplier
                hit = True
                break
        if hit: continue
        for e in enemy_spaceships[:]:
            if math.sqrt((e[0] - b[0])**2 + (e[1] - b[1])**2) < 25:
                e[3] -= 8
                bullets.remove(b)
                if e[3] <= 0:
                    enemy_spaceships.remove(e)
                    explosions.append([e[0], e[1], GAME_Z_LEVEL, 35, 30])
                    score += 3 * score_multiplier
                hit = True
                break
        if hit: continue
        for boss in boss_enemies[:]:
            if math.sqrt((boss[0] - b[0])**2 + (boss[1] - b[1])**2) < 50:
                boss[3] -= 3
                bullets.remove(b)
                if boss[3] <= 0:
                    boss_enemies.remove(boss)
                    explosions.append([boss[0], boss[1], GAME_Z_LEVEL, 80, 40])
                    score += 25 * score_multiplier
                hit = True
                break
        if hit: continue
        if abs(b[0]) > GRID_LENGTH + 100 or abs(b[1]) > GRID_LENGTH + 100:
            bullets.remove(b)
            missed_bullets += 1

def update_enemy_bullets():
    global enemy_bullets, player_health, shield_active, game_over
    for b in enemy_bullets[:]:
        b[0] += b[4] * math.cos(math.radians(b[3]))
        b[1] += b[4] * math.sin(math.radians(b[3]))
        if math.sqrt((b[0] - player_pos[0])**2 + (b[1] - player_pos[1])**2) < 25:
            enemy_bullets.remove(b)
            if not shield_active:
                player_health -= 3
                if player_health <= 0: game_over = True
            continue
        if abs(b[0]) > GRID_LENGTH + 100 or abs(b[1]) > GRID_LENGTH + 100:
            enemy_bullets.remove(b)

# ==============================================================================
# PART 4: MAIN GAME LOGIC (Modified to call Nashid's functions)
# ==============================================================================

def draw_shapes():
    # ... (Drawing stars, Earth, Moon can be kept for context)
    # Draw healing center - ENHANCED VISIBILITY
    draw_healing_center()
    
    # Draw spaceship
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(gun_angle, 0, 0, 1)
    if shield_active:
        glColor3f(0, 0.6, 1)
        glutSolidSphere(50, 16, 16)
    if cheat_mode:
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0, 35)
        glutSolidSphere(10, 12, 12)
        glPopMatrix()
    glColor3f(0.8, 0.8, 0.95)
    glPushMatrix()
    glScalef(1.8, 0.9, 0.6)
    glutSolidSphere(22, 20, 20)
    glPopMatrix()
    # ... other spaceship details
    if weapon_level > 1:
        glColor3f(1, 1, 0)
        for i in range(weapon_level - 1):
            glPushMatrix()
            glTranslatef(20, (i - (weapon_level-2)/2) * 12, 5)
            glutSolidSphere(4, 10, 10)
            glPopMatrix()
    glPopMatrix()
    
    # Draw enemy spaceships, bosses etc.
    for e in enemy_spaceships: draw_enemy_spaceship(e[0], e[1], GAME_Z_LEVEL, e[3])
    for b in boss_enemies: draw_boss_enemy(b[0], b[1], GAME_Z_LEVEL, b[3])
    # ... drawing bullets, explosions etc.
    glColor3f(1, 1, 0)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], GAME_Z_LEVEL)
        glutSolidSphere(6, 10, 10)
        glPopMatrix()
    glColor3f(1, 0.2, 0.2)
    for b in enemy_bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], GAME_Z_LEVEL)
        glutSolidSphere(5, 8, 8)
        glPopMatrix()


def keyboardListener(key, x, y):
    global gun_angle, player_pos, cheat_mode, last_manual_fire_frame, frame_counter
    if game_over: return
    speed = player_speed * 2.5 if speed_boost_active else player_speed
    if key == b'w':
        player_pos[0] += speed * math.cos(math.radians(gun_angle))
        player_pos[1] += speed * math.sin(math.radians(gun_angle))
    elif key == b's': cheat_mode = not cheat_mode
    elif key == b'a': gun_angle += 8
    elif key == b'd': gun_angle -= 8
    elif key == b' ' and frame_counter - last_manual_fire_frame > 20:
        shoot_bullets()
        last_manual_fire_frame = frame_counter

# ... (Include other necessary functions like specialKeyListener, mouseListener, setupCamera)
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

def idle():
    global frame_counter, earth_angle, moon_angle, player_health
    if game_over:
        glutPostRedisplay()
        return
    frame_counter += 1
    earth_angle += 0.2
    moon_angle += 0.4
    update_cheat_mode()
    
    # Healing logic
    if math.sqrt(player_pos[0]**2 + player_pos[1]**2) < 120:
        player_health = min(player_max_health, player_health + 1.2)
        
    spawn_boss()
    # update_enemies() # This can be stubbed or included if needed for testing
    update_enemy_spaceships()
    update_boss_enemies()
    update_bullets()
    update_enemy_bullets()
    # update_explosions() # This can be stubbed or included
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupCamera()
    draw_shapes()
    # ... Draw UI text related to Nashid's features
    draw_text(15, WINDOW_HEIGHT - 90, f"HEALTH: {int(player_health)}/{player_max_health}  |  WEAPON LEVEL: {weapon_level}")
    effects_text = f"CHEAT: {'ON' if cheat_mode else 'OFF'} (S key)"
    draw_text(15, WINDOW_HEIGHT - 115, effects_text)
    if len(boss_enemies) > 0:
        glColor3f(1, 0, 0)
        draw_text(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 80, f"!!! BOSS BATTLE - HEALTH: {boss_enemies[0][3]} !!!")
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Nashid's Module")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    # glutSpecialFunc(specialKeyListener)
    # glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()