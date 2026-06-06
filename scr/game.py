import pygame
import sys
import winsound
import threading

pygame.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quick Box / BETA RELISE")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

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

FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 24)

selected_color = GREEN
selected_level = 0
custom_level_data = None

EDITOR_PANEL_RECT = pygame.Rect(0, HEIGHT - 80, WIDTH, 80)
EDITOR_CUBE_BUTTON = pygame.Rect(20, HEIGHT - 70, 50, 50)
EDITOR_SPIKE_BUTTON = pygame.Rect(90, HEIGHT - 70, 50, 50)
EDITOR_PLAYER_START_BUTTON = pygame.Rect(160, HEIGHT - 70, 50, 50)
EDITOR_DELETE_BUTTON = pygame.Rect(230, HEIGHT - 70, 50, 50)

editor_mode = "cube"
editor_objects = []
player_start_pos = None
last_placed_pos = None

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

def draw_editor_panel():
    pygame.draw.rect(WIN, LIGHT_GRAY, EDITOR_PANEL_RECT)
    pygame.draw.rect(WIN, BLACK, EDITOR_PANEL_RECT, 2)
    
    pygame.draw.rect(WIN, GREEN if editor_mode == "cube" else GRAY, EDITOR_CUBE_BUTTON)
    pygame.draw.rect(WIN, BLACK, EDITOR_CUBE_BUTTON, 2)
    pygame.draw.rect(WIN, BLACK, EDITOR_CUBE_BUTTON.inflate(-10, -10))
    
    pygame.draw.rect(WIN, RED if editor_mode == "spike" else GRAY, EDITOR_SPIKE_BUTTON)
    pygame.draw.rect(WIN, BLACK, EDITOR_SPIKE_BUTTON, 2)
    draw_spike(EDITOR_SPIKE_BUTTON.x + 5, EDITOR_SPIKE_BUTTON.y + 5)
    
    pygame.draw.rect(WIN, BLUE if editor_mode == "player_start" else GRAY, EDITOR_PLAYER_START_BUTTON)
    pygame.draw.rect(WIN, BLACK, EDITOR_PLAYER_START_BUTTON, 2)
    pygame.draw.circle(WIN, BLUE, EDITOR_PLAYER_START_BUTTON.center, 15)
    
    pygame.draw.rect(WIN, (255, 100, 100) if editor_mode == "delete" else GRAY, EDITOR_DELETE_BUTTON)
    pygame.draw.rect(WIN, BLACK, EDITOR_DELETE_BUTTON, 2)
    text_surf = SMALL_FONT.render("DEL", True, BLACK)
    text_rect = text_surf.get_rect(center=EDITOR_DELETE_BUTTON.center)
    WIN.blit(text_surf, text_rect)

def start_game_from_objects(platforms, spikes, cubes, start_pos):
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
        for obj in custom_level_data.get("objects", []):
            if obj["type"] == "cube":
                cubes.append(pygame.Rect(obj["x"], obj["y"], 40, 40))
            elif obj["type"] == "spike":
                spikes.append(pygame.Rect(obj["x"], obj["y"], 40, 40))
        start_pos = custom_level_data.get("player_start", (50, HEIGHT - PLAYER_SIZE - 10))
        return platforms, spikes, cubes, start_pos
    return [], [], [], (50, HEIGHT - PLAYER_SIZE - 10)

def play_death_sound():
    winsound.Beep(1200, 2000)

def main():
    global selected_color, selected_level, custom_level_data, editor_mode, editor_objects, player_start_pos, last_placed_pos
    
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
    
    mouse_held = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BUTTON_RECT.collidepoint(event.pos) and selected_level > 0:
                        if selected_level == 4 and custom_level_data:
                            platforms, spikes, cubes, start_pos = get_level_objects_custom()
                            player_rect, y_vel, grounded, is_dead, death_timer = start_game_from_objects(platforms, spikes, cubes, start_pos)
                            game_state = "playing"
                        elif selected_level in [1,2,3]:
                            if selected_level == 1:
                                platforms = []
                                spikes = [pygame.Rect(WIDTH // 2 - 45, HEIGHT - 40, 40, 40), pygame.Rect(WIDTH // 2 - 15, HEIGHT - 40, 40, 40)]
                                cubes = []
                                start_pos = (50, HEIGHT - PLAYER_SIZE - 10)
                            elif selected_level == 2:
                                platforms = []
                                cube_rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 40, 40, 40)
                                spike_rect = pygame.Rect(WIDTH // 2 - 20, cube_rect.y - 40, 40, 40)
                                spikes = [spike_rect]
                                cubes = [cube_rect]
                                start_pos = (50, HEIGHT - PLAYER_SIZE - 10)
                            elif selected_level == 3:
                                platforms = []
                                spikes = [pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 40, 40), pygame.Rect(WIDTH // 2 - 30, HEIGHT - 40, 40, 40), pygame.Rect(WIDTH // 2, HEIGHT - 40, 40, 40)]
                                cubes = []
                                start_pos = (50, HEIGHT - PLAYER_SIZE - 10)
                            player_rect, y_vel, grounded, is_dead, death_timer = start_game_from_objects(platforms, spikes, cubes, start_pos)
                            game_state = "playing"
                    elif EDITOR_BUTTON_RECT.collidepoint(event.pos):
                        editor_objects = []
                        player_start_pos = None
                        editor_mode = "cube"
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
                                "objects": editor_objects,
                                "player_start": [player_start_pos.x, player_start_pos.y]
                            }
                            selected_level = 4
                            game_state = "menu"
                    elif CLEAR_BUTTON_RECT.collidepoint(event.pos):
                        editor_objects = []
                        player_start_pos = None
                    elif EDITOR_CUBE_BUTTON.collidepoint(event.pos):
                        editor_mode = "cube"
                    elif EDITOR_SPIKE_BUTTON.collidepoint(event.pos):
                        editor_mode = "spike"
                    elif EDITOR_PLAYER_START_BUTTON.collidepoint(event.pos):
                        editor_mode = "player_start"
                    elif EDITOR_DELETE_BUTTON.collidepoint(event.pos):
                        editor_mode = "delete"
                    else:
                        mouse_held = True
                        x = (event.pos[0] // 40) * 40
                        y = (event.pos[1] // 40) * 40
                        last_placed_pos = (x, y)
                        if editor_mode == "cube":
                            if {"type": "cube", "x": x, "y": y} not in editor_objects:
                                editor_objects.append({"type": "cube", "x": x, "y": y})
                        elif editor_mode == "spike":
                            if {"type": "spike", "x": x, "y": y} not in editor_objects:
                                editor_objects.append({"type": "spike", "x": x, "y": y})
                        elif editor_mode == "player_start":
                            player_start_pos = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
                        elif editor_mode == "delete":
                            for obj in editor_objects[:]:
                                if obj["x"] == x and obj["y"] == y:
                                    editor_objects.remove(obj)
                            if player_start_pos and player_start_pos.x == x and player_start_pos.y == y:
                                player_start_pos = None
                
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_held = False
                    last_placed_pos = None
                
                if event.type == pygame.MOUSEMOTION and mouse_held:
                    if event.pos[1] < EDITOR_PANEL_RECT.y:
                        x = (event.pos[0] // 40) * 40
                        y = (event.pos[1] // 40) * 40
                        if (x, y) != last_placed_pos:
                            last_placed_pos = (x, y)
                            if editor_mode == "cube":
                                if {"type": "cube", "x": x, "y": y} not in editor_objects:
                                    editor_objects.append({"type": "cube", "x": x, "y": y})
                            elif editor_mode == "spike":
                                if {"type": "spike", "x": x, "y": y} not in editor_objects:
                                    editor_objects.append({"type": "spike", "x": x, "y": y})
                            elif editor_mode == "player_start":
                                player_start_pos = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
                            elif editor_mode == "delete":
                                for obj in editor_objects[:]:
                                    if obj["x"] == x and obj["y"] == y:
                                        editor_objects.remove(obj)
                                if player_start_pos and player_start_pos.x == x and player_start_pos.y == y:
                                    player_start_pos = None
            
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
            
            for x in range(0, WIDTH, 40):
                pygame.draw.line(WIN, LIGHT_GRAY, (x, 0), (x, HEIGHT - 80))
            for y in range(0, HEIGHT - 80, 40):
                pygame.draw.line(WIN, LIGHT_GRAY, (0, y), (WIDTH, y))
            
            for obj in editor_objects:
                if obj["type"] == "cube":
                    pygame.draw.rect(WIN, BLACK, (obj["x"], obj["y"], 40, 40))
                elif obj["type"] == "spike":
                    draw_spike(obj["x"], obj["y"])
            
            if player_start_pos:
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
                    _, _, _, start_pos = get_level_objects_custom()
                    player_rect.x = start_pos[0]
                    player_rect.y = start_pos[1]
                else:
                    player_rect.x = 50
                    player_rect.y = HEIGHT - PLAYER_SIZE - 10
                y_vel = 0
                grounded = False
        elif respawn_timer > 0:
            respawn_timer -= 1
            if selected_level == 4 and custom_level_data:
                _, _, _, start_pos = get_level_objects_custom()
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

            y_vel += GRAVITY
            player_rect.y += y_vel

            grounded = False
            for platform in platforms:
                if player_rect.colliderect(platform):
                    if y_vel >= 0 and player_rect.bottom >= platform.top:
                        player_rect.bottom = platform.top
                        y_vel = 0
                        grounded = True
                    elif y_vel < 0 and player_rect.top <= platform.bottom:
                        player_rect.top = platform.bottom
                        y_vel = 0

            for cube in cubes:
                if player_rect.colliderect(cube):
                    if y_vel >= 0 and player_rect.bottom >= cube.top:
                        player_rect.bottom = cube.top
                        y_vel = 0
                        grounded = True
                    elif y_vel < 0 and player_rect.top <= cube.bottom:
                        player_rect.top = cube.bottom
                        y_vel = 0

            if player_rect.top < 0:
                player_rect.top = 0
                y_vel = 0
            if player_rect.bottom >= HEIGHT:
                player_rect.bottom = HEIGHT
                y_vel = 0
                grounded = True

            for spike in spikes:
                if player_rect.colliderect(spike):
                    if not is_dead and respawn_timer == 0:
                        sound_thread = threading.Thread(target=play_death_sound)
                        sound_thread.start()
                        is_dead = True
                        death_timer = 0

        WIN.fill(WHITE)
        
        for platform in platforms:
            pygame.draw.rect(WIN, BLACK, platform)
        for spike in spikes:
            draw_spike(spike.x, spike.y)
        for cube in cubes:
            pygame.draw.rect(WIN, BLACK, cube)
        
        draw_back_button()
        
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
