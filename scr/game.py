import pygame
import sys
import winsound
import threading
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quick Box / BETA RELEASE")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

PLAYER_SIZE = 40
PLAYER_VEL = 5
GRAVITY = 0.6
JUMP_VEL = -12

BUTTON_RECT = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
EDITOR_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 - 110, 260, 40)

GREEN_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 - 50, 60, 40)
BLUE_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 30, HEIGHT // 2 - 50, 60, 40)
YELLOW_BUTTON_RECT = pygame.Rect(WIDTH // 2 + 70, HEIGHT // 2 - 50, 60, 40)

LEVEL1_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 130, 100, 40)
LEVEL2_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 130, 100, 40)
LEVEL3_BUTTON_RECT = pygame.Rect(WIDTH // 2 + 60, HEIGHT // 2 + 130, 100, 40)
CUSTOM_LEVEL_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 190, 160, 40)

BACK_BUTTON_RECT = pygame.Rect(WIDTH - 60, 10, 50, 50)
SAVE_BUTTON_RECT = pygame.Rect(WIDTH - 100, 10, 40, 50)
CLEAR_BUTTON_RECT = pygame.Rect(WIDTH - 150, 10, 40, 50)

FONT = pygame.font.SysFont("arial", 36)
SMALL_FONT = pygame.font.SysFont("arial", 24)

selected_color = GREEN
selected_level = 0
custom_level_data = None
attempts = 0

EDITOR_PANEL_RECT = pygame.Rect(0, HEIGHT - 80, WIDTH, 80)
PANEL_VISIBLE = True
PANEL_TOGGLE_BUTTON = pygame.Rect(WIDTH - 40, HEIGHT - 80, 40, 20)

EDITOR_CUBE_BUTTON = pygame.Rect(20, HEIGHT - 70, 50, 50)
EDITOR_SPIKE_BUTTON = pygame.Rect(90, HEIGHT - 70, 50, 50)
EDITOR_PLAYER_START_BUTTON = pygame.Rect(160, HEIGHT - 70, 50, 50)
EDITOR_DELETE_BUTTON = pygame.Rect(230, HEIGHT - 70, 50, 50)
EDITOR_ORB_BUTTON = pygame.Rect(300, HEIGHT - 70, 50, 50)
EDITOR_FAKE_BUTTON = pygame.Rect(370, HEIGHT - 70, 50, 50)
EDITOR_ROTATE_BUTTON = pygame.Rect(440, HEIGHT - 70, 50, 50)

editor_mode = "cube"
editor_objects = []
player_start_pos = None
last_placed_pos = None

class Orb:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 5, y + 5, 30, 30)
        self.x = x
        self.y = y
    
    def draw(self):
        pygame.draw.circle(WIN, ORANGE, (self.x + 20, self.y + 20), 15)
        pygame.draw.circle(WIN, YELLOW, (self.x + 20, self.y + 20), 10)
    
    def activate(self, player_rect, y_vel):
        if player_rect.colliderect(self.rect) and y_vel >= 0:
            return JUMP_VEL * 0.7
        return y_vel

def draw_menu_buttons():
    pygame.draw.rect(WIN, GRAY, BUTTON_RECT)
    text_surf = FONT.render("Играть", True, BLACK)
    text_rect = text_surf.get_rect(center=BUTTON_RECT.center)
    WIN.blit(text_surf, text_rect)
    
    pygame.draw.rect(WIN, GRAY, EDITOR_BUTTON_RECT)
    text_surf = SMALL_FONT.render("Редактор уровней", True, BLACK)
    text_rect = text_surf.get_rect(center=EDITOR_BUTTON_RECT.center)
    WIN.blit(text_surf, text_rect)
    
    pygame.draw.rect(WIN, GREEN, GREEN_BUTTON_RECT)
    pygame.draw.rect(WIN, BLUE, BLUE_BUTTON_RECT)
    pygame.draw.rect(WIN, YELLOW, YELLOW_BUTTON_RECT)
    
    pygame.draw.rect(WIN, GRAY, LEVEL1_BUTTON_RECT)
    pygame.draw.rect(WIN, GRAY, LEVEL2_BUTTON_RECT)
    pygame.draw.rect(WIN, GRAY, LEVEL3_BUTTON_RECT)
    pygame.draw.rect(WIN, GRAY, CUSTOM_LEVEL_BUTTON_RECT)
    
    text1 = SMALL_FONT.render("1", True, BLACK)
    text2 = SMALL_FONT.render("2", True, BLACK)
    text3 = SMALL_FONT.render("3", True, BLACK)
    text_custom = SMALL_FONT.render("Ваша карта", True, BLACK)
    
    WIN.blit(text1, text1.get_rect(center=LEVEL1_BUTTON_RECT.center))
    WIN.blit(text2, text2.get_rect(center=LEVEL2_BUTTON_RECT.center))
    WIN.blit(text3, text3.get_rect(center=LEVEL3_BUTTON_RECT.center))
    WIN.blit(text_custom, text_custom.get_rect(center=CUSTOM_LEVEL_BUTTON_RECT.center))

def draw_back_button():
    pygame.draw.polygon(WIN, BLACK, [
        (BACK_BUTTON_RECT.x + 35, BACK_BUTTON_RECT.y + 15),
        (BACK_BUTTON_RECT.x + 15, BACK_BUTTON_RECT.y + 25),
        (BACK_BUTTON_RECT.x + 35, BACK_BUTTON_RECT.y + 35)
    ])
    pygame.draw.rect(WIN, BLACK, BACK_BUTTON_RECT, 2)

def draw_save_button():
    text_surf = SMALL_FONT.render("C", True, BLACK)
    text_rect = text_surf.get_rect(center=SAVE_BUTTON_RECT.center)
    pygame.draw.rect(WIN, GRAY, SAVE_BUTTON_RECT)
    pygame.draw.rect(WIN, BLACK, SAVE_BUTTON_RECT, 2)
    WIN.blit(text_surf, text_rect)

def draw_clear_button():
    text_surf = SMALL_FONT.render("X", True, BLACK)
    text_rect = text_surf.get_rect(center=CLEAR_BUTTON_RECT.center)
    pygame.draw.rect(WIN, GRAY, CLEAR_BUTTON_RECT)
    pygame.draw.rect(WIN, BLACK, CLEAR_BUTTON_RECT, 2)
    WIN.blit(text_surf, text_rect)

def draw_spike(x, y):
    points = [
        (x + 20, y),
        (x, y + 40),
        (x + 40, y + 40)
    ]
    pygame.draw.polygon(WIN, BLACK, points)

def draw_rotated_spike(x, y, angle):
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    points = [(20, 0), (0, 40), (40, 40)]
    pygame.draw.polygon(surf, BLACK, points)
    rotated = pygame.transform.rotate(surf, angle)
    rect = rotated.get_rect(center=(x + 20, y + 20))
    WIN.blit(rotated, rect)

def draw_rotated_block(x, y, angle, color):
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    surf.fill(color)
    rotated = pygame.transform.rotate(surf, angle)
    rect = rotated.get_rect(center=(x + 20, y + 20))
    WIN.blit(rotated, rect)

def draw_editor_panel():
    global PANEL_VISIBLE, EDITOR_PANEL_RECT, EDITOR_CUBE_BUTTON, EDITOR_SPIKE_BUTTON, EDITOR_PLAYER_START_BUTTON, EDITOR_DELETE_BUTTON, EDITOR_ORB_BUTTON, EDITOR_FAKE_BUTTON, EDITOR_ROTATE_BUTTON, PANEL_TOGGLE_BUTTON
    
    if PANEL_VISIBLE:
        EDITOR_PANEL_RECT = pygame.Rect(0, HEIGHT - 80, WIDTH, 80)
        EDITOR_CUBE_BUTTON = pygame.Rect(20, HEIGHT - 70, 50, 50)
        EDITOR_SPIKE_BUTTON = pygame.Rect(90, HEIGHT - 70, 50, 50)
        EDITOR_PLAYER_START_BUTTON = pygame.Rect(160, HEIGHT - 70, 50, 50)
        EDITOR_DELETE_BUTTON = pygame.Rect(230, HEIGHT - 70, 50, 50)
        EDITOR_ORB_BUTTON = pygame.Rect(300, HEIGHT - 70, 50, 50)
        EDITOR_FAKE_BUTTON = pygame.Rect(370, HEIGHT - 70, 50, 50)
        EDITOR_ROTATE_BUTTON = pygame.Rect(440, HEIGHT - 70, 50, 50)
        PANEL_TOGGLE_BUTTON = pygame.Rect(WIDTH - 40, HEIGHT - 80, 40, 20)
        
        pygame.draw.rect(WIN, LIGHT_GRAY, EDITOR_PANEL_RECT)
        pygame.draw.rect(WIN, BLACK, EDITOR_PANEL_RECT, 2)
        
        pygame.draw.rect(WIN, GREEN if editor_mode == "cube" else GRAY, EDITOR_CUBE_BUTTON)
        pygame.draw.rect(WIN, BLACK, EDITOR_CUBE_BUTTON, 2)
        pygame.draw.rect(WIN, BLACK, EDITOR_CUBE_BUTTON.inflate(-10, -10))
        
        pygame.draw.rect(WIN, RED if editor_mode == "spike" else GRAY, EDITOR_SPIKE_BUTTON)
        pygame.draw.rect(WIN, BLACK, EDITOR_SPIKE_BUTTON, 2)
        spike_points = [(EDITOR_SPIKE_BUTTON.x + 25, EDITOR_SPIKE_BUTTON.y + 5), (EDITOR_SPIKE_BUTTON.x + 5, EDITOR_SPIKE_BUTTON.y + 45), (EDITOR_SPIKE_BUTTON.x + 45, EDITOR_SPIKE_BUTTON.y + 45)]
        pygame.draw.polygon(WIN, BLACK, spike_points)
        
        pygame.draw.rect(WIN, BLUE if editor_mode == "player_start" else GRAY, EDITOR_PLAYER_START_BUTTON)
        pygame.draw.rect(WIN, BLACK, EDITOR_PLAYER_START_BUTTON, 2)
        pygame.draw.circle(WIN, BLUE, EDITOR_PLAYER_START_BUTTON.center, 15)
        
        pygame.draw.rect(WIN, (255, 100, 100) if editor_mode == "delete" else GRAY, EDITOR_DELETE_BUTTON)
        pygame.draw.rect(WIN, BLACK, EDITOR_DELETE_BUTTON, 2)
        text_surf = SMALL_FONT.render("DEL", True, BLACK)
        text_rect = text_surf.get_rect(center=EDITOR_DELETE_BUTTON.center)
        WIN.blit(text_surf, text_rect)
        
        pygame.draw.rect(WIN, ORANGE if editor_mode == "orb" else GRAY, EDITOR_ORB_BUTTON)
        pygame.draw.rect(WIN, BLACK, EDITOR_ORB_BUTTON, 2)
        pygame.draw.circle(WIN, ORANGE, EDITOR_ORB_BUTTON.center, 15)
        pygame.draw.circle(WIN, YELLOW, EDITOR_ORB_BUTTON.center, 10)
        
        pygame.draw.rect(WIN, (150, 150, 150) if editor_mode == "fake" else GRAY, EDITOR_FAKE_BUTTON)
        pygame.draw.rect(WIN, RED, EDITOR_FAKE_BUTTON, 3)
        
        pygame.draw.rect(WIN, (100, 100, 200) if editor_mode == "rotate" else GRAY, EDITOR_ROTATE_BUTTON)
        pygame.draw.rect(WIN, BLACK, EDITOR_ROTATE_BUTTON, 2)
        text_surf = SMALL_FONT.render("R", True, BLACK)
        text_rect = text_surf.get_rect(center=EDITOR_ROTATE_BUTTON.center)
        WIN.blit(text_surf, text_rect)
    else:
        EDITOR_PANEL_RECT = pygame.Rect(0, HEIGHT, WIDTH, 80)
        PANEL_TOGGLE_BUTTON = pygame.Rect(WIDTH - 40, HEIGHT - 20, 40, 20)
        pygame.draw.rect(WIN, DARK_GRAY, PANEL_TOGGLE_BUTTON)
    
    pygame.draw.rect(WIN, DARK_GRAY, PANEL_TOGGLE_BUTTON)
    if PANEL_VISIBLE:
        pygame.draw.polygon(WIN, WHITE, [(PANEL_TOGGLE_BUTTON.x + 10, PANEL_TOGGLE_BUTTON.y + 5), (PANEL_TOGGLE_BUTTON.x + 30, PANEL_TOGGLE_BUTTON.y + 5), (PANEL_TOGGLE_BUTTON.x + 20, PANEL_TOGGLE_BUTTON.y + 15)])
    else:
        pygame.draw.polygon(WIN, WHITE, [(PANEL_TOGGLE_BUTTON.x + 10, PANEL_TOGGLE_BUTTON.y + 10), (PANEL_TOGGLE_BUTTON.x + 30, PANEL_TOGGLE_BUTTON.y + 10), (PANEL_TOGGLE_BUTTON.x + 20, PANEL_TOGGLE_BUTTON.y)])

def draw_attempts():
    text_surf = FONT.render(str(attempts), True, RED)
    WIN.blit(text_surf, (10, 10))

def start_game_from_objects(platforms, spikes, cubes, orbs, fake_blocks, start_pos):
    player_rect = pygame.Rect(start_pos[0], start_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    y_vel = 0
    grounded = False
    is_dead = False
    death_timer = 0
    return player_rect, y_vel, grounded, is_dead, death_timer

def get_level_objects_custom():
    if custom_level_data:
        platforms = []
        spikes = []
        cubes = []
        orbs = []
        fake_blocks = []
        for obj in custom_level_data.get("objects", []):
            if obj["type"] == "cube":
                cubes.append({"rect": pygame.Rect(obj["x"], obj["y"], 40, 40), "angle": obj.get("angle", 0)})
            elif obj["type"] == "spike":
                spikes.append({"rect": pygame.Rect(obj["x"], obj["y"], 40, 40), "angle": obj.get("angle", 0)})
            elif obj["type"] == "orb":
                orbs.append(Orb(obj["x"], obj["y"]))
            elif obj["type"] == "fake":
                fake_blocks.append(pygame.Rect(obj["x"], obj["y"], 40, 40))
        start_pos = custom_level_data.get("player_start", (50, HEIGHT - PLAYER_SIZE - 10))
        return platforms, spikes, cubes, orbs, fake_blocks, start_pos
    return [], [], [], [], [], (50, HEIGHT - PLAYER_SIZE - 10)

def play_death_sound():
    winsound.Beep(1200, 2000)

def main():
    global selected_color, selected_level, custom_level_data, editor_mode, editor_objects, player_start_pos, last_placed_pos, attempts, PANEL_VISIBLE
    
    clock = pygame.time.Clock()
    game_state = "menu"
    player_rect = None
    y_vel = 0
    grounded = False
    is_dead = False
    death_timer = 0
    respawn_timer = 0
    platforms = []
    spikes = []
    cubes = []
    orbs = []
    fake_blocks = []
    
    mouse_held = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BUTTON_RECT.collidepoint(event.pos) and selected_level > 0:
                        attempts = 0
                        if selected_level == 4 and custom_level_data:
                            platforms, spikes, cubes, orbs, fake_blocks, start_pos = get_level_objects_custom()
                            player_rect, y_vel, grounded, is_dead, death_timer = start_game_from_objects(platforms, spikes, cubes, orbs, fake_blocks, start_pos)
                            game_state = "playing"
                        elif selected_level in [1,2,3]:
                            if selected_level == 1:
                                platforms = []
                                spikes = [{"rect": pygame.Rect(WIDTH // 2 - 45, HEIGHT - 40, 40, 40), "angle": 0}, {"rect": pygame.Rect(WIDTH // 2 - 15, HEIGHT - 40, 40, 40), "angle": 0}]
                                cubes = []
                                orbs = []
                                fake_blocks = []
                                start_pos = (50, HEIGHT - PLAYER_SIZE - 10)
                            elif selected_level == 2:
                                platforms = []
                                cubes = [{"rect": pygame.Rect(WIDTH // 2 - 20, HEIGHT - 40, 40, 40), "angle": 0}]
                                spikes = [{"rect": pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 40), "angle": 0}]
                                orbs = []
                                fake_blocks = []
                                start_pos = (50, HEIGHT - PLAYER_SIZE - 10)
                            elif selected_level == 3:
                                platforms = []
                                spikes = [{"rect": pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 40, 40), "angle": 0}, {"rect": pygame.Rect(WIDTH // 2 - 30, HEIGHT - 40, 40, 40), "angle": 0}, {"rect": pygame.Rect(WIDTH // 2, HEIGHT - 40, 40, 40), "angle": 0}]
                                cubes = []
                                orbs = []
                                fake_blocks = []
                                start_pos = (50, HEIGHT - PLAYER_SIZE - 10)
                            player_rect, y_vel, grounded, is_dead, death_timer = start_game_from_objects(platforms, spikes, cubes, orbs, fake_blocks, start_pos)
                            game_state = "playing"
                    elif EDITOR_BUTTON_RECT.collidepoint(event.pos):
                        if custom_level_data:
                            editor_objects = custom_level_data.get("objects", []).copy()
                            player_start_pos_data = custom_level_data.get("player_start", [50, HEIGHT - PLAYER_SIZE - 10])
                            player_start_pos = pygame.Rect(player_start_pos_data[0], player_start_pos_data[1], PLAYER_SIZE, PLAYER_SIZE)
                        else:
                            editor_objects = []
                            player_start_pos = None
                        editor_mode = "cube"
                        PANEL_VISIBLE = True
                        game_state = "editor"
                    elif GREEN_BUTTON_RECT.collidepoint(event.pos):
                        selected_color = GREEN
                    elif BLUE_BUTTON_RECT.collidepoint(event.pos):
                        selected_color = BLUE
                    elif YELLOW_BUTTON_RECT.collidepoint(event.pos):
                        selected_color = YELLOW
                    elif LEVEL1_BUTTON_RECT.collidepoint(event.pos):
                        selected_level = 1
                    elif LEVEL2_BUTTON_RECT.collidepoint(event.pos):
                        selected_level = 2
                    elif LEVEL3_BUTTON_RECT.collidepoint(event.pos):
                        selected_level = 3
                    elif CUSTOM_LEVEL_BUTTON_RECT.collidepoint(event.pos):
                        if custom_level_data:
                            selected_level = 4
            
            if game_state == "editor":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON_RECT.collidepoint(event.pos):
                        game_state = "menu"
                    elif SAVE_BUTTON_RECT.collidepoint(event.pos):
                        if player_start_pos:
                            custom_level_data = {
                                "objects": editor_objects.copy(),
                                "player_start": [player_start_pos.x, player_start_pos.y]
                            }
                            selected_level = 4
                            game_state = "menu"
                    elif CLEAR_BUTTON_RECT.collidepoint(event.pos):
                        editor_objects = []
                        player_start_pos = None
                    elif PANEL_TOGGLE_BUTTON.collidepoint(event.pos):
                        PANEL_VISIBLE = not PANEL_VISIBLE
                    elif PANEL_VISIBLE and event.pos[1] > HEIGHT - 80:
                        if EDITOR_CUBE_BUTTON.collidepoint(event.pos):
                            editor_mode = "cube"
                        elif EDITOR_SPIKE_BUTTON.collidepoint(event.pos):
                            editor_mode = "spike"
                        elif EDITOR_PLAYER_START_BUTTON.collidepoint(event.pos):
                            editor_mode = "player_start"
                        elif EDITOR_DELETE_BUTTON.collidepoint(event.pos):
                            editor_mode = "delete"
                        elif EDITOR_ORB_BUTTON.collidepoint(event.pos):
                            editor_mode = "orb"
                        elif EDITOR_FAKE_BUTTON.collidepoint(event.pos):
                            editor_mode = "fake"
                        elif EDITOR_ROTATE_BUTTON.collidepoint(event.pos):
                            editor_mode = "rotate"
                    elif (PANEL_VISIBLE and event.pos[1] < HEIGHT - 80) or (not PANEL_VISIBLE and event.pos[1] < HEIGHT):
                        mouse_held = True
                        x = (event.pos[0] // 40) * 40
                        y = (event.pos[1] // 40) * 40
                        if (PANEL_VISIBLE and y < HEIGHT - 80) or (not PANEL_VISIBLE and y < HEIGHT):
                            last_placed_pos = (x, y)
                            if editor_mode == "cube":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "cube":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "cube", "x": x, "y": y, "angle": 0})
                            elif editor_mode == "spike":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "spike":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "spike", "x": x, "y": y, "angle": 0})
                            elif editor_mode == "player_start":
                                player_start_pos = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
                            elif editor_mode == "orb":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "orb":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "orb", "x": x, "y": y})
                            elif editor_mode == "fake":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "fake":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "fake", "x": x, "y": y})
                            elif editor_mode == "delete":
                                for i in range(len(editor_objects)-1, -1, -1):
                                    if editor_objects[i].get("x") == x and editor_objects[i].get("y") == y:
                                        editor_objects.pop(i)
                                if player_start_pos and player_start_pos.x == x and player_start_pos.y == y:
                                    player_start_pos = None
                            elif editor_mode == "rotate":
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and (obj["type"] == "cube" or obj["type"] == "spike"):
                                        obj["angle"] = (obj.get("angle", 0) + 30) % 360
                
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_held = False
                    last_placed_pos = None
                
                if event.type == pygame.MOUSEMOTION and mouse_held:
                    if (PANEL_VISIBLE and event.pos[1] < HEIGHT - 80) or (not PANEL_VISIBLE and event.pos[1] < HEIGHT):
                        x = (event.pos[0] // 40) * 40
                        y = (event.pos[1] // 40) * 40
                        if (x, y) != last_placed_pos:
                            last_placed_pos = (x, y)
                            if editor_mode == "cube":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "cube":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "cube", "x": x, "y": y, "angle": 0})
                            elif editor_mode == "spike":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "spike":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "spike", "x": x, "y": y, "angle": 0})
                            elif editor_mode == "player_start":
                                player_start_pos = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
                            elif editor_mode == "orb":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "orb":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "orb", "x": x, "y": y})
                            elif editor_mode == "fake":
                                exists = False
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and obj["type"] == "fake":
                                        exists = True
                                        break
                                if not exists:
                                    editor_objects.append({"type": "fake", "x": x, "y": y})
                            elif editor_mode == "delete":
                                for i in range(len(editor_objects)-1, -1, -1):
                                    if editor_objects[i].get("x") == x and editor_objects[i].get("y") == y:
                                        editor_objects.pop(i)
                                if player_start_pos and player_start_pos.x == x and player_start_pos.y == y:
                                    player_start_pos = None
                            elif editor_mode == "rotate":
                                for obj in editor_objects:
                                    if obj.get("x") == x and obj.get("y") == y and (obj["type"] == "cube" or obj["type"] == "spike"):
                                        obj["angle"] = (obj.get("angle", 0) + 30) % 360
            
            if game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON_RECT.collidepoint(event.pos):
                        game_state = "menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and grounded and not is_dead and respawn_timer == 0:
                        y_vel = JUMP_VEL
                        grounded = False

        if game_state == "menu":
            WIN.fill(WHITE)
            draw_menu_buttons()
            pygame.display.update()
            clock.tick(60)
            continue
        
        if game_state == "editor":
            WIN.fill(WHITE)
            
            grid_height = HEIGHT - 80 if PANEL_VISIBLE else HEIGHT
            for x in range(0, WIDTH, 40):
                pygame.draw.line(WIN, LIGHT_GRAY, (x, 0), (x, grid_height))
            for y in range(0, grid_height, 40):
                pygame.draw.line(WIN, LIGHT_GRAY, (0, y), (WIDTH, y))
            
            for obj in editor_objects:
                if obj["type"] == "cube":
                    draw_rotated_block(obj["x"], obj["y"], obj.get("angle", 0), BLACK)
                elif obj["type"] == "spike":
                    draw_rotated_spike(obj["x"], obj["y"], obj.get("angle", 0))
                elif obj["type"] == "orb":
                    pygame.draw.circle(WIN, ORANGE, (obj["x"] + 20, obj["y"] + 20), 15)
                    pygame.draw.circle(WIN, YELLOW, (obj["x"] + 20, obj["y"] + 20), 10)
                elif obj["type"] == "fake":
                    pygame.draw.rect(WIN, BLACK, (obj["x"], obj["y"], 40, 40))
            
            if player_start_pos and (player_start_pos.y < grid_height or not PANEL_VISIBLE):
                pygame.draw.circle(WIN, BLUE, player_start_pos.center, 20)
                pygame.draw.circle(WIN, BLACK, player_start_pos.center, 20, 2)
            
            draw_editor_panel()
            draw_back_button()
            draw_save_button()
            draw_clear_button()
            pygame.display.update()
            clock.tick(60)
            continue

        if is_dead:
            death_timer += 1
            if death_timer >= 120:
                death_timer = 0
                is_dead = False
                respawn_timer = 180
                if selected_level == 4 and custom_level_data:
                    _, _, _, _, _, start_pos = get_level_objects_custom()
                    player_rect.x = start_pos[0]
                    player_rect.y = start_pos[1]
                else:
                    player_rect.x = 50
                    player_rect.y = HEIGHT - PLAYER_SIZE - 10
                y_vel = 0
                grounded = False
                attempts += 1
        elif respawn_timer > 0:
            respawn_timer -= 1
            if selected_level == 4 and custom_level_data:
                _, _, _, _, _, start_pos = get_level_objects_custom()
                player_rect.x = start_pos[0]
                player_rect.y = start_pos[1]
            else:
                player_rect.x = 50
                player_rect.y = HEIGHT - PLAYER_SIZE - 10
            y_vel = 0
            grounded = False
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player_rect.x -= PLAYER_VEL
            if keys[pygame.K_d]:
                player_rect.x += PLAYER_VEL

            if player_rect.left < 0:
                player_rect.left = 0
            if player_rect.right > WIDTH:
                game_state = "menu"
                continue

            old_y = player_rect.y
            y_vel += GRAVITY
            player_rect.y += y_vel

            grounded = False
            
            all_blocks = cubes + platforms
            for block in all_blocks:
                rect = block["rect"] if isinstance(block, dict) else block
                if player_rect.colliderect(rect):
                    if y_vel > 0 and player_rect.bottom > rect.top and old_y + PLAYER_SIZE <= rect.top + 10:
                        player_rect.bottom = rect.top
                        y_vel = 0
                        grounded = True
                    elif y_vel < 0 and player_rect.top < rect.bottom and old_y >= rect.bottom - 10:
                        player_rect.top = rect.bottom
                        y_vel = 0

            for block in all_blocks:
                rect = block["rect"] if isinstance(block, dict) else block
                if player_rect.colliderect(rect):
                    if player_rect.right > rect.left and player_rect.left < rect.left:
                        player_rect.right = rect.left
                    elif player_rect.left < rect.right and player_rect.right > rect.right:
                        player_rect.left = rect.right

            for fake in fake_blocks:
                if player_rect.colliderect(fake):
                    if not is_dead and respawn_timer == 0:
                        sound_thread = threading.Thread(target=play_death_sound)
                        sound_thread.start()
                        is_dead = True
                        death_timer = 0

            if player_rect.top < 0:
                player_rect.top = 0
                y_vel = 0
            if player_rect.bottom >= HEIGHT:
                player_rect.bottom = HEIGHT
                y_vel = 0
                grounded = True

            for spike in spikes:
                spike_hitbox = pygame.Rect(spike["rect"].x + 12, spike["rect"].y + 15, 16, 20)
                if player_rect.colliderect(spike_hitbox):
                    if not is_dead and respawn_timer == 0:
                        sound_thread = threading.Thread(target=play_death_sound)
                        sound_thread.start()
                        is_dead = True
                        death_timer = 0

            for orb in orbs:
                new_y_vel = orb.activate(player_rect, y_vel)
                if new_y_vel != y_vel:
                    y_vel = new_y_vel
                    grounded = False

        WIN.fill(WHITE)
        
        for platform in platforms:
            pygame.draw.rect(WIN, BLACK, platform)
        for spike in spikes:
            draw_rotated_spike(spike["rect"].x, spike["rect"].y, spike["angle"])
        for cube in cubes:
            draw_rotated_block(cube["rect"].x, cube["rect"].y, cube["angle"], BLACK)
        for orb in orbs:
            orb.draw()
        for fake in fake_blocks:
            pygame.draw.rect(WIN, BLACK, fake)
        
        draw_back_button()
        draw_attempts()
        
        if respawn_timer > 0:
            pass
        elif is_dead:
            pygame.draw.rect(WIN, RED, player_rect)
        else:
            pygame.draw.rect(WIN, selected_color, player_rect)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
