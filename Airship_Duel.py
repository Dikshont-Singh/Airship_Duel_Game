import pygame
import math
import random
import sys
from pathlib import Path

pygame.init()

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
ASSET_DIR = BASE_DIR / "Game Assets"


def asset_path(filename):
    return str(ASSET_DIR / filename)

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 1300, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airship")
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load(asset_path("logo.png")).convert_alpha())
FPS = 60
# Game states
game_paused = False
game_state = "menu"

# For text rendering
font=pygame.font.SysFont("Algerian", 24)
text_color=(255, 255, 255)

def text(text, font, color,size,x,y):
    font = pygame.font.SysFont("Arial", size)
    imgage = font.render(text, True, color)
    screen.blit(imgage, (x, y))


def draw_main_menu(buttons, ship_options, ship_names, p1_index, p2_index):
    ticks = pygame.time.get_ticks()
    pulse = 170 + int(55 * (0.5 + 0.5 * math.sin(ticks * 0.004)))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((3, 8, 22, 155))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("Algerian", 76)
    player_font = pygame.font.SysFont("Arial", 24, bold=True)
    name_font = pygame.font.SysFont("Algerian", 42)
    ability_font = pygame.font.SysFont("Arial", 26, bold=True)
    phrase_font = pygame.font.SysFont("Arial", 20)
    small_font = pygame.font.SysFont("Arial", 25)
    button_font = pygame.font.SysFont("Arial", 23, bold=True)

    ability_data = {
        "Falcon": ("Force Field", "Raises a hollow shield that absorbs fire."),
        "Blade": ("Boost Dash", "Dashes forward with a tight ram shield."),
        "Nova": ("Twin Shot", "Fires two bullets at once for a short time."),
        "Vortex": ("Phase Shift", "Teleports behind the enemy and phases briefly."),
        "Raven": ("Homing Missile", "Launches a tracking missile at the opponent."),
        "Specter": ("Curve Burst", "Fires a fast curved shotgun burst."),
        "Phantom": ("Cloak", "Stealth prototype. Active ability coming soon."),
        "Titan": ("Heavy Hull", "A sturdy ship with no active ability yet."),
    }

    for i in range(42):
        star_x = (i * 97 + ticks // 18) % WIDTH
        star_y = (i * 53 + 80) % HEIGHT
        star_color = (55, 95, 150) if i % 2 else (90, 140, 210)
        pygame.draw.circle(screen, star_color, (star_x, star_y), 1)

    title = title_font.render("AIRSHIP DUEL", True, (255, pulse, 120))
    subtitle = phrase_font.render("Choose your ship. Learn its ability. Start the duel.", True, (220, 232, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 58)))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 112)))

    def draw_ship_card(rect, player_label, ship_index, accent, rotate_angle):
        ship_name = ship_names[ship_index]
        ability_name, phrase = ability_data.get(ship_name, ("Unknown", "Ability data unavailable."))
        glow = pygame.Surface((rect.width + 22, rect.height + 22), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*accent, 55), glow.get_rect(), border_radius=22)
        screen.blit(glow, (rect.x - 11, rect.y - 11))

        pygame.draw.rect(screen, (14, 22, 45), rect, border_radius=18)
        pygame.draw.rect(screen, accent, rect, width=3, border_radius=18)
        pygame.draw.line(screen, (*accent,), (rect.left + 28, rect.top + 70), (rect.right - 28, rect.top + 70), 2)

        player_text = player_font.render(player_label, True, accent)
        name_text = name_font.render(ship_name.upper(), True, (255, 245, 205))
        screen.blit(player_text, player_text.get_rect(center=(rect.centerx, rect.top + 32)))
        screen.blit(name_text, name_text.get_rect(center=(rect.centerx, rect.top + 95)))

        preview_box = pygame.Rect(rect.left + 64, rect.top + 135, rect.width - 128, 170)
        pygame.draw.rect(screen, (8, 14, 34), preview_box, border_radius=14)
        pygame.draw.rect(screen, (70, 95, 145), preview_box, width=1, border_radius=14)
        for ring in range(3):
            pygame.draw.circle(
                screen,
                (accent[0], accent[1], accent[2],),
                preview_box.center,
                42 + ring * 28,
                1,
            )

        ship_img = pygame.transform.rotozoom(ship_options[ship_index], rotate_angle, 1.35)
        screen.blit(ship_img, ship_img.get_rect(center=preview_box.center))

        tag = small_font.render("SHIFT ABILITY", True, (175, 195, 230))
        ability_text = ability_font.render(ability_name, True, accent)
        phrase_text = phrase_font.render(phrase, True, (230, 238, 255))
        screen.blit(tag, tag.get_rect(center=(rect.centerx, rect.top + 335)))
        screen.blit(ability_text, ability_text.get_rect(center=(rect.centerx, rect.top + 365)))
        screen.blit(phrase_text, phrase_text.get_rect(center=(rect.centerx, rect.top + 398)))

    left_card = pygame.Rect(70, 145, 460, 455)
    right_card = pygame.Rect(WIDTH - 530, 145, 460, 455)
    draw_ship_card(left_card, "PLAYER 1", p1_index, (80, 220, 255), 90)
    draw_ship_card(right_card, "PLAYER 2", p2_index, (255, 130, 105), -90)

    vs_font = pygame.font.SysFont("Algerian", 74)
    vs_text = vs_font.render("VS", True, (255, 235, 160))
    screen.blit(vs_text, vs_text.get_rect(center=(WIDTH // 2, 360)))

    hint = small_font.render("Let's Fight", True, (190, 205, 235))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 585)))

    mouse_pos = pygame.mouse.get_pos()
    for key, rect in buttons.items():
        if key == "START GAME":
            base = (180, 110, 35)
            hover = (235, 160, 55)
            border = (255, 220, 125)
        elif key == "QUIT":
            base = (80, 35, 50)
            hover = (130, 55, 75)
            border = (255, 150, 170)
        else:
            base = (32, 50, 92)
            hover = (60, 85, 145)
            border = (175, 205, 255)
        color = hover if rect.collidepoint(mouse_pos) else base
        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, border, rect, width=2, border_radius=12)
        label = button_font.render(key, True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=rect.center))


def draw_help_menu(back_button):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 145))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("Algerian", 60)
    line_font = pygame.font.SysFont("Arial", 27)
    small_font = pygame.font.SysFont("Arial", 22)

    panel = pygame.Rect(WIDTH // 2 - 420, HEIGHT // 2 - 260, 840, 520)
    pygame.draw.rect(screen, (18, 28, 58), panel, border_radius=16)
    pygame.draw.rect(screen, (130, 180, 255), panel, width=2, border_radius=16)

    title = title_font.render("CONTROLS", True, (255, 220, 120))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200)))

    lines = [
        "# Player 1: A/D rotate, W thrust, Left Ctrl shoot",
        "# Player 2: Left/Right arrow rotate, Up arrow thrust, Right Ctrl shoot",
        '# Press Left and Right Shift to activate ship ability ',
        "# Menu: Click P1 SHIP / P2 SHIP to change ship variant",
        "# Press Enter from menu to start quickly",
        '# If any ship wins, press "SPACE" to return to main menu',
    ]
    y_pos = HEIGHT // 2 - 138
    for line in lines:
        txt = line_font.render(line, True, (230, 235, 255))
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y_pos)))
        y_pos += 40

    
    

    mouse_pos = pygame.mouse.get_pos()
    color = (80, 110, 180) if back_button.collidepoint(mouse_pos) else (50, 70, 120)
    pygame.draw.rect(screen, color, back_button, border_radius=10)
    pygame.draw.rect(screen, (180, 210, 255), back_button, width=2, border_radius=10)
    label = small_font.render("BACK", True, (255, 255, 255))
    screen.blit(label, label.get_rect(center=back_button.center))
   

# ---------------- LOAD BACKGROUND ----------------
bg = pygame.image.load(asset_path("p-1.png")).convert_alpha()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# ---------------- LOAD PLANETS ----------------
planet1 = pygame.image.load(asset_path('p-2.png')).convert_alpha()
planet2 = pygame.image.load(asset_path('p-4.png')).convert_alpha()
planet3 = pygame.image.load(asset_path('p-3.png')).convert_alpha()
star=pygame.image.load(asset_path('p-5.png')).convert_alpha()

def scale_image(image, scale):
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))

def load_ship_variants(paths, names, scale):
    loaded_ships = []
    for path in paths:
        image = pygame.image.load(asset_path(path)).convert_alpha()
        loaded_ships.append(scale_image(image, scale))
    return loaded_ships, names


ship_paths = ["playership.png", "2B.png", "4B.png", "8B.png", "7B.png", "12B.png", "eh3.png", "9B.png"]
ship_names_data = ["Falcon", "Blade", "Nova", "Vortex", "Raven", "Specter", "Phantom" , "Titan"]
ship_options, ship_names = load_ship_variants(ship_paths, ship_names_data, 0.3)

# The supplied missile artwork has a solid background and wide padding.
# Remove the background, crop the missile, then scale it for gameplay.
missile_source = pygame.image.load(asset_path("Missile05.png")).convert()
missile_source.set_colorkey(missile_source.get_at((0, 0)))
missile_crop = missile_source.subsurface(
    pygame.Rect(
        int(missile_source.get_width() * 0.22),
        0,
        int(missile_source.get_width() * 0.56),
        int(missile_source.get_height() * 0.72),
    )
).copy()
missile_image = pygame.transform.smoothscale(missile_crop, (18, 30))

player1_ship_index = 0
player2_ship_index = 1

menu_buttons = {
    "START GAME": pygame.Rect(WIDTH // 2 - 150, 620, 300, 54),
    "P1 SHIP": pygame.Rect(190, 625, 220, 48),
    "P2 SHIP": pygame.Rect(WIDTH - 410, 625, 220, 48),
    "CONTROLS": pygame.Rect(WIDTH // 2 - 220, 695, 190, 42),
    "QUIT": pygame.Rect(WIDTH // 2 + 30, 695, 190, 42),
}
help_back_button = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 165, 180, 42)


# ---------------- Player 1 SHIP STATE ----------------
P1_START_X, P1_START_Y = 300, 400
P2_START_X, P2_START_Y = 1000, 400
x, y = P1_START_X, P1_START_Y

angle = 0.0
vel_x = 0.0
vel_y = 0.0
rotation_speed = 3
acceleration = 0.25
friction = 0.99
max_speed = 8

# ---------------- Player 2 SHIP STATE ----------------
x1, y1 = P2_START_X, P2_START_Y

angle1 = 0.0
vel_x1 = 0.0
vel_y1 = 0.0
rotation_speed = 3
acceleration = 0.25
friction = 0.99
max_speed = 8

# ---------------- PLAYER 1 HEALTH ----------------
player_max_health = 100
player_health = 100
# ---------------- PLAYER 2 HEALTH ----------------
player_max_health1 = 100
player_health1 = 100


# FALCON ABILITY — SHIELD
FALCON_NAME = "Falcon"
shield_max = 100
player1_shield = shield_max
player2_shield = shield_max
player1_shield_active = False
player2_shield_active = False
player1_shield_cooldown = 0
player2_shield_cooldown = 0
player1_shield_duration = 0
player2_shield_duration = 0
shield_radius = 62
shield_recharge_duration = 3 * FPS
shield_recharge = shield_max / shield_recharge_duration
shield_active_duration = 7 * FPS

# NOVA ABILITY — TWIN SHOT 
NOVA_NAME = "Nova"
twin_shot_duration = 8 * FPS
twin_shot_cooldown_duration = 4 * FPS
player1_twin_shot_active = False
player2_twin_shot_active = False
player1_twin_shot_timer = 0
player2_twin_shot_timer = 0
player1_twin_shot_cooldown = 0
player2_twin_shot_cooldown = 0

# BLADE ABILITY: BOOST DASH
BLADE_NAME = "Blade"
blade_dash_duration = int(0.5 * FPS)
blade_dash_recharge_duration = 3 * FPS
blade_dash_speed = 20
blade_dash_damage = 18
blade_dash_knockback = 20
blade_dash_shield_radius = 40
player1_blade_dash_timer = 0
player2_blade_dash_timer = 0
player1_blade_dash_cooldown = 0
player2_blade_dash_cooldown = 0
player1_blade_dash_dir = (1, 0)
player2_blade_dash_dir = (-1, 0)
player1_blade_dash_hit = False
player2_blade_dash_hit = False

# SPECTER ABILITY: CURVED SHOTGUN BURST
SPECTER_NAME = "Specter"
specter_burst_cooldown_duration = 4 * FPS
specter_burst_min_bullets = 10
specter_burst_max_bullets = 15
specter_burst_speed = 12.5
specter_burst_life = 45
specter_burst_damage = 7
player1_specter_burst_cooldown = 0
player2_specter_burst_cooldown = 0

#  VORTEX ABILITY: PHASE SHIFT 
VORTEX_NAME = "Vortex"
phase_shift_distance = 110
phase_shift_recharge_duration = 4 * FPS
phase_protection_duration = int(0.4 * FPS)
player1_phase_shift_cooldown = 0
player2_phase_shift_cooldown = 0
player1_phase_protection = 0
player2_phase_protection = 0

#RAVEN ABILITY: HOMING MISSILE 
RAVEN_NAME = "Raven"
missile_damage = 35
missile_speed = 7
missile_turn_strength = 0.24
missile_life = 300
missile_recharge_duration = 8 * FPS
player1_missile_cooldown = 0
player2_missile_cooldown = 0

# PHANTOM ABILITY: INVISIBILITY CLOAK
phantom_cloak = False
phantom_cloak_start = 0

PHANTOM_CLOAK_DURATION = 3000      
PHANTOM_CLOAK_COOLDOWN = 8000

phantom_last_used = -PHANTOM_CLOAK_COOLDOWN




# ---------------- BULLETS ----------------
bullets = []
missiles = []
bullet_speed = 10
bullet_radius = 3
bullet_life = 60
bullet_damage = 10
shoot_cooldown_frames = 12
ship1_cooldown = 0
ship2_cooldown = 0

# ---------------- PARTICLES ----------------
particles = []

def reset_match():
    global x, y, angle, vel_x, vel_y
    global x1, y1, angle1, vel_x1, vel_y1
    global player_health, player_health1, player1_shield, player2_shield
    global player1_shield_active, player2_shield_active
    global player1_shield_cooldown, player2_shield_cooldown
    global player1_shield_duration, player2_shield_duration
    global player1_twin_shot_active, player2_twin_shot_active
    global player1_twin_shot_timer, player2_twin_shot_timer
    global player1_twin_shot_cooldown, player2_twin_shot_cooldown
    global player1_blade_dash_timer, player2_blade_dash_timer
    global player1_blade_dash_cooldown, player2_blade_dash_cooldown
    global player1_blade_dash_dir, player2_blade_dash_dir
    global player1_blade_dash_hit, player2_blade_dash_hit
    global player1_specter_burst_cooldown, player2_specter_burst_cooldown
    global player1_phase_shift_cooldown, player2_phase_shift_cooldown
    global player1_phase_protection, player2_phase_protection
    global player1_missile_cooldown, player2_missile_cooldown
    global bullets, missiles, particles, ship1_cooldown, ship2_cooldown

    x, y = P1_START_X, P1_START_Y
    x1, y1 = P2_START_X, P2_START_Y
    angle = 0.0
    angle1 = 0.0
    vel_x = 0.0
    vel_y = 0.0
    vel_x1 = 0.0
    vel_y1 = 0.0
    player_health = player_max_health
    player_health1 = player_max_health1
    player1_shield = shield_max
    player2_shield = shield_max
    player1_shield_active = False
    player2_shield_active = False
    player1_shield_cooldown = 0
    player2_shield_cooldown = 0
    player1_shield_duration = 0
    player2_shield_duration = 0
    player1_twin_shot_active = False
    player2_twin_shot_active = False
    player1_twin_shot_timer = 0
    player2_twin_shot_timer = 0
    player1_twin_shot_cooldown = 0
    player2_twin_shot_cooldown = 0
    player1_blade_dash_timer = 0
    player2_blade_dash_timer = 0
    player1_blade_dash_cooldown = 0
    player2_blade_dash_cooldown = 0
    player1_blade_dash_dir = (1, 0)
    player2_blade_dash_dir = (-1, 0)
    player1_blade_dash_hit = False
    player2_blade_dash_hit = False
    player1_specter_burst_cooldown = 0
    player2_specter_burst_cooldown = 0
    player1_phase_shift_cooldown = 0
    player2_phase_shift_cooldown = 0
    player1_phase_protection = 0
    player2_phase_protection = 0
    player1_missile_cooldown = 0
    player2_missile_cooldown = 0
    bullets = []
    missiles = []
    particles = []
    ship1_cooldown = 0
    ship2_cooldown = 0


def create_explosion(x_pos, y_pos, count=45):
    for _ in range(count):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.2, 6.0)
        particles.append(
            {
                "x": x_pos,
                "y": y_pos,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(18, 42),
                "size": random.randint(2, 5),
                "color": random.choice(
                    [(255, 220, 80), (255, 150, 60), (255, 80, 40), (220, 220, 220)]
                ),
            }
        )


def create_phase_blast(x_pos, y_pos, count=32):
    """Create a brief purple burst for Vortex's advanced Phase Shift."""
    phase_colors = [(220, 120, 255), (165, 80, 255), (110, 55, 220), (245, 190, 255)]
    for _ in range(count):
        particle_angle = random.uniform(0, math.tau)
        speed = random.uniform(2.0, 5.0)
        particles.append(
            {
                "x": x_pos,
                "y": y_pos,
                "vx": math.cos(particle_angle) * speed,
                "vy": math.sin(particle_angle) * speed,
                "life": random.randint(8, 16),
                "size": random.randint(2, 4),
                "color": random.choice(phase_colors),
            }
        )


def create_engine_trail(x_pos, y_pos, forward_x, forward_y):
    """Create a short flame trail behind a ship while it is using thrust."""
    for _ in range(2):
        sideways = random.uniform(-5, 5)
        # Place the particle behind the ship, with a small sideways spread.
        start_x = x_pos - forward_x * 24 - forward_y * sideways
        start_y = y_pos - forward_y * 24 + forward_x * sideways
        backward_speed = random.uniform(1.5, 3.0)
        particles.append(
            {
                "x": start_x,
                "y": start_y,
                "vx": -forward_x * backward_speed - forward_y * random.uniform(-0.8, 0.8),
                "vy": -forward_y * backward_speed + forward_x * random.uniform(-0.8, 0.8),
                "life": random.randint(5, 9),
                "size": random.randint(2, 4),
                "color": random.choice([(255, 235, 120), (255, 155, 55), (255, 80, 35)]),
            }
        )


def create_blade_dash_trail(x_pos, y_pos, forward_x, forward_y):
    """Create blue overboost particles behind Blade during dash."""
    boost_colors = [(60, 220, 255), (80, 150, 255), (30, 95, 255), (180, 245, 255)]
    for _ in range(4):
        sideways = random.uniform(-10, 10)
        start_x = x_pos - forward_x * 28 - forward_y * sideways
        start_y = y_pos - forward_y * 28 + forward_x * sideways
        backward_speed = random.uniform(3.0, 6.0)
        particles.append(
            {
                "x": start_x,
                "y": start_y,
                "vx": -forward_x * backward_speed - forward_y * random.uniform(-1.4, 1.4),
                "vy": -forward_y * backward_speed + forward_x * random.uniform(-1.4, 1.4),
                "life": random.randint(7, 13),
                "size": random.randint(2, 5),
                "color": random.choice(boost_colors),
            }
        )


def create_blade_impact(x_pos, y_pos, count=34):
    """Create a blue-green burst when Blade's dash slams into a ship."""
    impact_colors = [(70, 240, 255), (55, 150, 255), (80, 255, 170), (210, 255, 245)]
    for _ in range(count):
        particle_angle = random.uniform(0, math.tau)
        speed = random.uniform(2.2, 6.5)
        particles.append(
            {
                "x": x_pos,
                "y": y_pos,
                "vx": math.cos(particle_angle) * speed,
                "vy": math.sin(particle_angle) * speed,
                "life": random.randint(10, 22),
                "size": random.randint(2, 5),
                "color": random.choice(impact_colors),
            }
        )


def create_specter_muzzle_burst(x_pos, y_pos, forward_x, forward_y, owner):
    """Create sharp smoke and spark particles for Specter's shotgun burst."""
    side_x = -forward_y
    side_y = forward_x
    colors = (
        [(120, 255, 240), (210, 255, 255), (80, 180, 255)]
        if owner == 1
        else [(255, 130, 220), (255, 215, 250), (180, 100, 255)]
    )
    for _ in range(18):
        sideways = random.uniform(-22, 22)
        speed = random.uniform(1.5, 4.5)
        particles.append(
            {
                "x": x_pos + forward_x * 32 + side_x * sideways,
                "y": y_pos + forward_y * 32 + side_y * sideways,
                "vx": forward_x * speed + side_x * random.uniform(-1.2, 1.2),
                "vy": forward_y * speed + side_y * random.uniform(-1.2, 1.2),
                "life": random.randint(8, 18),
                "size": random.randint(2, 4),
                "color": random.choice(colors),
            }
        )


def fire_specter_burst(x_pos, y_pos, forward_x, forward_y, owner):
    """Fire 6-9 faster bullets in a curved shotgun pattern."""
    base_angle = math.atan2(forward_y, forward_x)
    side_x = -forward_y
    side_y = forward_x
    bullet_count = random.randint(specter_burst_min_bullets, specter_burst_max_bullets)
    color = (120, 255, 240) if owner == 1 else (255, 130, 220)
    for index in range(bullet_count):
        t = 0 if bullet_count == 1 else index / (bullet_count - 1)
        curve = t - 0.5
        shot_angle = base_angle + math.radians(curve * 72)
        dir_x = math.cos(shot_angle)
        dir_y = math.sin(shot_angle)
        side_offset = curve * 42
        front_offset = 34 + abs(curve) * 20
        bullets.append(
            {
                "x": x_pos + forward_x * front_offset + side_x * side_offset,
                "y": y_pos + forward_y * front_offset + side_y * side_offset,
                "vx": dir_x * specter_burst_speed,
                "vy": dir_y * specter_burst_speed,
                "life": specter_burst_life,
                "owner": owner,
                "damage": specter_burst_damage,
                "radius": 4,
                "color": color,
            }
        )
    create_specter_muzzle_burst(x_pos, y_pos, forward_x, forward_y, owner)


def create_missile_trail(x_pos, y_pos, forward_x, forward_y):
    """Create one small exhaust particle for a compact homing missile."""
    backward_speed = random.uniform(1.2, 2.0)
    particles.append(
        {
            "x": x_pos - forward_x * 10,
            "y": y_pos - forward_y * 10,
            "vx": -forward_x * backward_speed,
            "vy": -forward_y * backward_speed,
            "life": random.randint(3, 5),
            "size": random.randint(1, 2),
            "color": random.choice([(255, 225, 120), (255, 125, 45)]),
        }
    )


def launch_homing_missile(x_pos, y_pos, forward_x, forward_y, owner):
    """Launch a Raven missile in the ship's forward direction."""
    missiles.append(
        {
            "x": x_pos + forward_x * 36,
            "y": y_pos + forward_y * 36,
            "vx": forward_x * missile_speed,
            "vy": forward_y * missile_speed,
            "owner": owner,
            "life": missile_life,
        }
    )


def draw_player_health(surface, health, max_health):
    bar_width = 200
    bar_height = 20
    x = WIDTH - bar_width - 20
    y = 20
    ratio = max(0, health) / max_health
    pygame.draw.rect(surface, (80, 80, 80), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)
def draw_player_health1(surface, health1, max_health1):
    bar_width = 200
    bar_height = 20
    x = 20
    y = 20
    ratio = max(0, health1) / max_health1
    pygame.draw.rect(surface, (80, 80, 80), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)


# ---------------- FALCON ABILITY: USER INTERFACE ----------------
def draw_shield_bar(surface, shield, max_shield, player, active, cooldown, duration):
    """Draw a Falcon's shield meter directly below that player's health bar."""
    bar_width = 200
    bar_height = 12
    x = 20 if player == 1 else WIDTH - bar_width - 20
    y = 46
    ratio = max(0, shield) / max_shield
    pygame.draw.rect(surface, (35, 55, 95), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (70, 190, 255), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (180, 230, 255), (x, y, bar_width, bar_height), 1)
    if active:
        status = f"SHIELD ACTIVE: {duration / FPS:.1f}s"
    elif cooldown > 0:
        status = f"RECHARGING: {cooldown / FPS:.1f}s"
    else:
        status = "SHIELD READY"
    label = pygame.font.SysFont("Arial", 14).render(status, True, (190, 230, 255))
    surface.blit(label, (x, y + 14))


# ---------------- NOVA ABILITY: USER INTERFACE ----------------
def draw_twin_shot_bar(surface, timer, cooldown, player):
    """Draw Nova's active timer or four-second cooldown below the health bar."""
    bar_width = 200
    bar_height = 12
    x = 20 if player == 1 else WIDTH - bar_width - 20
    y = 46
    if timer > 0:
        ratio = timer / twin_shot_duration
        status = f"TWIN SHOT: {timer / FPS:.1f}s"
    else:
        ratio = 1 - (cooldown / twin_shot_cooldown_duration)
        status = f"TWIN SHOT RECHARGING: {cooldown / FPS:.1f}s"
    pygame.draw.rect(surface, (75, 35, 110), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (210, 100, 255), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (245, 200, 255), (x, y, bar_width, bar_height), 1)
    label = pygame.font.SysFont("Arial", 14).render(status, True, (245, 200, 255))
    surface.blit(label, (x, y + 14))


# ---------------- BLADE ABILITY: USER INTERFACE ----------------
def draw_blade_dash_bar(surface, timer, cooldown, player):
    """Draw Blade's dash timer or recharge below the health bar."""
    bar_width = 200
    bar_height = 12
    x = 20 if player == 1 else WIDTH - bar_width - 20
    y = 46
    if timer > 0:
        ratio = timer / blade_dash_duration
        status = f"BLADE DASH: {timer / FPS:.1f}s"
    else:
        ratio = 1 - (cooldown / blade_dash_recharge_duration)
        status = f"DASH RECHARGING: {cooldown / FPS:.1f}s"
    pygame.draw.rect(surface, (25, 70, 65), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (80, 255, 150), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (190, 255, 220), (x, y, bar_width, bar_height), 1)
    label = pygame.font.SysFont("Arial", 14).render(status, True, (190, 255, 220))
    surface.blit(label, (x, y + 14))


def draw_blade_dash_shield(surface, x_pos, y_pos, forward_x, forward_y):
    """Draw a tight green ship-shaped shield around Blade during dash."""
    side_x = -forward_y
    side_y = forward_x
    points = [
        (x_pos + forward_x * 48, y_pos + forward_y * 48),
        (x_pos + side_x * 30, y_pos + side_y * 30),
        (x_pos - forward_x * 34, y_pos - forward_y * 34),
        (x_pos - side_x * 30, y_pos - side_y * 30),
    ]
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(overlay, (70, 255, 150, 45), points)
    pygame.draw.polygon(overlay, (95, 255, 165, 220), points, 3)
    pygame.draw.polygon(overlay, (220, 255, 235, 120), points, 1)
    surface.blit(overlay, (0, 0))


# ---------------- SPECTER ABILITY: USER INTERFACE ----------------
def draw_specter_burst_bar(surface, cooldown, player):
    """Draw Specter's shotgun reload bar below the health bar."""
    bar_width = 200
    bar_height = 12
    x = 20 if player == 1 else WIDTH - bar_width - 20
    y = 46
    ratio = 1 - (cooldown / specter_burst_cooldown_duration)
    pygame.draw.rect(surface, (35, 45, 70), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (120, 255, 240), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (210, 255, 255), (x, y, bar_width, bar_height), 1)
    label = pygame.font.SysFont("Arial", 14).render(
        f"SHOTGUN RELOADING: {cooldown / FPS:.1f}s", True, (210, 255, 255)
    )
    surface.blit(label, (x, y + 14))


# ---------------- VORTEX ABILITY: USER INTERFACE ----------------
def draw_phase_shift_bar(surface, cooldown, player):
    """Draw Vortex's Phase Shift recharge bar below the health bar."""
    bar_width = 200
    bar_height = 12
    x = 20 if player == 1 else WIDTH - bar_width - 20
    y = 46
    ratio = 1 - (cooldown / phase_shift_recharge_duration)
    pygame.draw.rect(surface, (30, 50, 105), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (100, 170, 255), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (200, 225, 255), (x, y, bar_width, bar_height), 1)
    label = pygame.font.SysFont("Arial", 14).render(
        f"PHASE SHIFT RECHARGING: {cooldown / FPS:.1f}s", True, (200, 225, 255)
    )
    surface.blit(label, (x, y + 14))


# ---------------- RAVEN ABILITY: USER INTERFACE ----------------
def draw_missile_bar(surface, cooldown, player):
    """Draw Raven's missile recharge bar below the health bar."""
    bar_width = 200
    bar_height = 12
    x = 20 if player == 1 else WIDTH - bar_width - 20
    y = 46
    ratio = 1 - (cooldown / missile_recharge_duration)
    pygame.draw.rect(surface, (65, 45, 25), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (255, 175, 65), (x, y, bar_width * ratio, bar_height))
    pygame.draw.rect(surface, (255, 225, 180), (x, y, bar_width, bar_height), 1)
    label = pygame.font.SysFont("Arial", 14).render(
        f"MISSILE RECHARGING: {cooldown / FPS:.1f}s", True, (255, 225, 180)
    )
    surface.blit(label, (x, y + 14))
    


# ---------------- MAIN LOOP ----------------
run = True
while run:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    
    screen.blit(planet1, (200, 150))
    screen.blit(planet2, (850, 350))
    screen.blit(planet3, (600, 600))
    screen.blit(planet3, (400, 100))
    screen.blit(star,(0,0))

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif game_state == "playing" and event.type == pygame.KEYDOWN:
            game_over = player_health <= 0 or player_health1 <= 0
            if game_over and event.key == pygame.K_SPACE:
                reset_match()
                game_state = "menu"
            elif not game_over and event.key == pygame.K_LSHIFT:
                # Player 1: activate Falcon shield only when it is ready.
                if (
                    ship_names[player1_ship_index] == FALCON_NAME
                    and player1_shield > 0
                    and player1_shield_cooldown == 0
                    and not player1_shield_active
                ):
                    player1_shield_active = True
                    player1_shield_duration = shield_active_duration
                elif (
                    ship_names[player1_ship_index] == NOVA_NAME
                    and not player1_twin_shot_active
                    and player1_twin_shot_cooldown == 0
                ):
                    player1_twin_shot_active = True
                    player1_twin_shot_timer = twin_shot_duration
                elif (
                    ship_names[player1_ship_index] == BLADE_NAME
                    and player1_blade_dash_timer == 0
                    and player1_blade_dash_cooldown == 0
                ):
                    dash_rad = math.radians(angle - 90)
                    player1_blade_dash_dir = (math.cos(dash_rad), -math.sin(dash_rad))
                    player1_blade_dash_timer = blade_dash_duration
                    player1_blade_dash_hit = False
                elif (
                    ship_names[player1_ship_index] == SPECTER_NAME
                    and player1_specter_burst_cooldown == 0
                ):
                    burst_rad = math.radians(angle - 270)
                    burst_x = -math.cos(burst_rad)
                    burst_y = math.sin(burst_rad)
                    fire_specter_burst(x, y, burst_x, burst_y, 1)
                    player1_specter_burst_cooldown = specter_burst_cooldown_duration
                elif (
                    ship_names[player1_ship_index] == VORTEX_NAME
                    and player1_phase_shift_cooldown == 0
                ):
    
                    # Move Player 1 behind Player 2 using Player 2's heading.
                    target_rad = math.radians(angle1 - 270)
                    target_forward_x = -math.cos(target_rad)
                    target_forward_y = math.sin(target_rad)
                    phase_x = x1 - target_forward_x * phase_shift_distance
                    phase_y = y1 - target_forward_y * phase_shift_distance
                    x = phase_x % WIDTH
                    y = phase_y % HEIGHT
                    vel_x = 0
                    vel_y = 0
                    create_phase_blast(x, y)
                    player1_phase_protection = phase_protection_duration
                    player1_phase_shift_cooldown = phase_shift_recharge_duration
                elif (
                    ship_names[player1_ship_index] == RAVEN_NAME
                    and player1_missile_cooldown == 0
                ):
                    rad = math.radians(angle - 90)
                    launch_homing_missile(x, y, math.cos(rad), -math.sin(rad), 1)
                    player1_missile_cooldown = missile_recharge_duration
            elif not game_over and event.key == pygame.K_RSHIFT:
                # Player 2: activate Falcon shield only when it is ready.
                if (
                    ship_names[player2_ship_index] == FALCON_NAME
                    and player2_shield > 0
                    and player2_shield_cooldown == 0
                    and not player2_shield_active
                ):
                    player2_shield_active = True
                    player2_shield_duration = shield_active_duration
                elif (
                    ship_names[player2_ship_index] == NOVA_NAME
                    and not player2_twin_shot_active
                    and player2_twin_shot_cooldown == 0
                ):
                    player2_twin_shot_active = True
                    player2_twin_shot_timer = twin_shot_duration
                elif (
                    ship_names[player2_ship_index] == BLADE_NAME
                    and player2_blade_dash_timer == 0
                    and player2_blade_dash_cooldown == 0
                ):
                    dash_rad1 = math.radians(angle1 - 270)
                    player2_blade_dash_dir = (-math.cos(dash_rad1), math.sin(dash_rad1))
                    player2_blade_dash_timer = blade_dash_duration
                    player2_blade_dash_hit = False
                elif (
                    ship_names[player2_ship_index] == SPECTER_NAME
                    and player2_specter_burst_cooldown == 0
                ):
                    burst_rad1 = math.radians(angle1 - 270)
                    burst_x1 = -math.cos(burst_rad1)
                    burst_y1 = math.sin(burst_rad1)
                    fire_specter_burst(x1, y1, burst_x1, burst_y1, 2)
                    player2_specter_burst_cooldown = specter_burst_cooldown_duration
                elif (
                    ship_names[player2_ship_index] == VORTEX_NAME
                    and player2_phase_shift_cooldown == 0
                ):
                    # Move Player 2 behind Player 1 using Player 1's heading.
                    target_rad = math.radians(angle - 90)
                    target_forward_x = math.cos(target_rad)
                    target_forward_y = -math.sin(target_rad)
                    phase_x = x - target_forward_x * phase_shift_distance
                    phase_y = y - target_forward_y * phase_shift_distance
                    x1 = phase_x % WIDTH
                    y1 = phase_y % HEIGHT
                    vel_x1 = 0
                    vel_y1 = 0
                    create_phase_blast(x1, y1)
                    player2_phase_protection = phase_protection_duration
                    player2_phase_shift_cooldown = phase_shift_recharge_duration
                elif (
                    ship_names[player2_ship_index] == RAVEN_NAME
                    and player2_missile_cooldown == 0
                ):
                    rad1 = math.radians(angle1 - 270)
                    launch_homing_missile(x1, y1, -math.cos(rad1), math.sin(rad1), 2)
                    player2_missile_cooldown = missile_recharge_duration
        elif game_state == "menu" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN,pygame.K_SPACE):
                reset_match()
                game_state = "playing"
            elif event.key == pygame.K_h:
                game_state = "help"
            elif event.key == pygame.K_ESCAPE:
                run = False
        elif game_state == "menu" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_buttons["START GAME"].collidepoint(event.pos):
                reset_match()
                game_state = "playing"
            elif menu_buttons["P1 SHIP"].collidepoint(event.pos):
                player1_ship_index = (player1_ship_index + 1) % len(ship_options)
            elif menu_buttons["P2 SHIP"].collidepoint(event.pos):
                player2_ship_index = (player2_ship_index + 1) % len(ship_options)
            elif menu_buttons["CONTROLS"].collidepoint(event.pos):
                game_state = "help"
            elif menu_buttons["QUIT"].collidepoint(event.pos):
                run = False
        elif game_state == "help" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                game_state = "menu"
        elif game_state == "help" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if help_back_button.collidepoint(event.pos):
                game_state = "menu"

    if game_state == "menu":
        draw_main_menu(menu_buttons, ship_options, ship_names, player1_ship_index, player2_ship_index)
        pygame.display.update()
        continue
    if game_state == "help":
        draw_help_menu(help_back_button)
        pygame.display.update()
        continue

    draw_player_health(screen, player_health1, player_max_health1)
    draw_player_health1(screen, player_health, player_max_health)
    if (
        ship_names[player1_ship_index] == FALCON_NAME
        and (player1_shield_active or player1_shield_cooldown > 0)
    ):
        draw_shield_bar(
            screen,
            player1_shield,
            shield_max,
            1,
            player1_shield_active,
            player1_shield_cooldown,
            player1_shield_duration,
        )
    if (
        ship_names[player2_ship_index] == FALCON_NAME
        and (player2_shield_active or player2_shield_cooldown > 0)
    ):
        draw_shield_bar(
            screen,
            player2_shield,
            shield_max,
            2,
            player2_shield_active,
            player2_shield_cooldown,
            player2_shield_duration,
        )
    if (
        ship_names[player1_ship_index] == NOVA_NAME
        and (player1_twin_shot_active or player1_twin_shot_cooldown > 0)
    ):
        draw_twin_shot_bar(
            screen, player1_twin_shot_timer, player1_twin_shot_cooldown, 1
        )
    if (
        ship_names[player2_ship_index] == NOVA_NAME
        and (player2_twin_shot_active or player2_twin_shot_cooldown > 0)
    ):
        draw_twin_shot_bar(
            screen, player2_twin_shot_timer, player2_twin_shot_cooldown, 2
        )
    if (
        ship_names[player1_ship_index] == BLADE_NAME
        and (player1_blade_dash_timer > 0 or player1_blade_dash_cooldown > 0)
    ):
        draw_blade_dash_bar(
            screen, player1_blade_dash_timer, player1_blade_dash_cooldown, 1
        )
    if (
        ship_names[player2_ship_index] == BLADE_NAME
        and (player2_blade_dash_timer > 0 or player2_blade_dash_cooldown > 0)
    ):
        draw_blade_dash_bar(
            screen, player2_blade_dash_timer, player2_blade_dash_cooldown, 2
        )
    if ship_names[player1_ship_index] == SPECTER_NAME and player1_specter_burst_cooldown > 0:
        draw_specter_burst_bar(screen, player1_specter_burst_cooldown, 1)
    if ship_names[player2_ship_index] == SPECTER_NAME and player2_specter_burst_cooldown > 0:
        draw_specter_burst_bar(screen, player2_specter_burst_cooldown, 2)
    if ship_names[player1_ship_index] == VORTEX_NAME and player1_phase_shift_cooldown > 0:
        draw_phase_shift_bar(screen, player1_phase_shift_cooldown, 1)
    if ship_names[player2_ship_index] == VORTEX_NAME and player2_phase_shift_cooldown > 0:
        draw_phase_shift_bar(screen, player2_phase_shift_cooldown, 2)
    if ship_names[player1_ship_index] == RAVEN_NAME and player1_missile_cooldown > 0:
        draw_missile_bar(screen, player1_missile_cooldown, 1)
    if ship_names[player2_ship_index] == RAVEN_NAME and player2_missile_cooldown > 0:
        draw_missile_bar(screen, player2_missile_cooldown, 2)
    
                       
    if game_paused== True:
        pass
    else:
        game_paused == False
    keys = pygame.key.get_pressed()
    ship1_alive = player_health > 0
    ship2_alive = player_health1 > 0

    
    # FALCON ABILITY: SHIELD  
    
    player1_is_falcon = ship_names[player1_ship_index] == FALCON_NAME
    player2_is_falcon = ship_names[player2_ship_index] == FALCON_NAME

    if not player1_is_falcon or not ship1_alive:
        player1_shield_active = False
        player1_shield_duration = 0
    if not player2_is_falcon or not ship2_alive:
        player2_shield_active = False
        player2_shield_duration = 0

    if player1_shield_active:
        player1_shield_duration = max(0, player1_shield_duration - 1)
        if player1_shield_duration == 0:
            player1_shield_active = False
            player1_shield_cooldown = shield_recharge_duration
    if player1_shield_cooldown > 0:
        player1_shield = min(shield_max, player1_shield + shield_recharge)
        player1_shield_cooldown -= 1
    elif player1_is_falcon and not player1_shield_active:
        player1_shield = min(shield_max, player1_shield + shield_recharge)

    if player2_shield_active:
        player2_shield_duration = max(0, player2_shield_duration - 1)
        if player2_shield_duration == 0:
            player2_shield_active = False
            player2_shield_cooldown = shield_recharge_duration
    if player2_shield_cooldown > 0:
        player2_shield = min(shield_max, player2_shield + shield_recharge)
        player2_shield_cooldown -= 1
    elif player2_is_falcon and not player2_shield_active:
        player2_shield = min(shield_max, player2_shield + shield_recharge)

    # ---------------- NOVA ABILITY: TWIN SHOT TIMER ----------------
    player1_is_nova = ship_names[player1_ship_index] == NOVA_NAME
    player2_is_nova = ship_names[player2_ship_index] == NOVA_NAME

    if not player1_is_nova or not ship1_alive:
        player1_twin_shot_active = False
        player1_twin_shot_timer = 0
        player1_twin_shot_cooldown = 0
    elif player1_twin_shot_active:
        player1_twin_shot_timer = max(0, player1_twin_shot_timer - 1)
        if player1_twin_shot_timer == 0:
            player1_twin_shot_active = False
            player1_twin_shot_cooldown = twin_shot_cooldown_duration
    elif player1_twin_shot_cooldown > 0:
        player1_twin_shot_cooldown -= 1

    if not player2_is_nova or not ship2_alive:
        player2_twin_shot_active = False
        player2_twin_shot_timer = 0
        player2_twin_shot_cooldown = 0
    elif player2_twin_shot_active:
        player2_twin_shot_timer = max(0, player2_twin_shot_timer - 1)
        if player2_twin_shot_timer == 0:
            player2_twin_shot_active = False
            player2_twin_shot_cooldown = twin_shot_cooldown_duration
    elif player2_twin_shot_cooldown > 0:
        player2_twin_shot_cooldown -= 1

    # ---------------- BLADE ABILITY: BOOST DASH TIMER ----------------
    player1_is_blade = ship_names[player1_ship_index] == BLADE_NAME
    player2_is_blade = ship_names[player2_ship_index] == BLADE_NAME

    if not player1_is_blade or not ship1_alive:
        player1_blade_dash_timer = 0
        player1_blade_dash_cooldown = 0
        player1_blade_dash_hit = False
    elif player1_blade_dash_timer > 0:
        player1_blade_dash_timer -= 1
        if player1_blade_dash_timer == 0:
            player1_blade_dash_cooldown = blade_dash_recharge_duration
    elif player1_blade_dash_cooldown > 0:
        player1_blade_dash_cooldown -= 1

    if not player2_is_blade or not ship2_alive:
        player2_blade_dash_timer = 0
        player2_blade_dash_cooldown = 0
        player2_blade_dash_hit = False
    elif player2_blade_dash_timer > 0:
        player2_blade_dash_timer -= 1
        if player2_blade_dash_timer == 0:
            player2_blade_dash_cooldown = blade_dash_recharge_duration
    elif player2_blade_dash_cooldown > 0:
        player2_blade_dash_cooldown -= 1

    # ---------------- SPECTER ABILITY: SHOTGUN BURST RELOAD ----------------
    player1_is_specter = ship_names[player1_ship_index] == SPECTER_NAME
    player2_is_specter = ship_names[player2_ship_index] == SPECTER_NAME

    if not player1_is_specter or not ship1_alive:
        player1_specter_burst_cooldown = 0
    elif player1_specter_burst_cooldown > 0:
        player1_specter_burst_cooldown -= 1

    if not player2_is_specter or not ship2_alive:
        player2_specter_burst_cooldown = 0
    elif player2_specter_burst_cooldown > 0:
        player2_specter_burst_cooldown -= 1

    # ---------------- VORTEX ABILITY: PHASE SHIFT RECHARGE ----------------
    if player1_phase_shift_cooldown > 0:
        player1_phase_shift_cooldown -= 1
    if player2_phase_shift_cooldown > 0:
        player2_phase_shift_cooldown -= 1
    if player1_phase_protection > 0:
        player1_phase_protection -= 1
    if player2_phase_protection > 0:
        player2_phase_protection -= 1

    # ---------------- RAVEN ABILITY: MISSILE RECHARGE ----------------
    if player1_missile_cooldown > 0:
        player1_missile_cooldown -= 1
    if player2_missile_cooldown > 0:
        player2_missile_cooldown -= 1

    if keys[pygame.K_ESCAPE]:
        game_paused == True
            

    # ---------- PLAYER 1 ROTATION ----------
    if ship1_alive and keys[pygame.K_a]:
        angle += rotation_speed
    if ship1_alive and keys[pygame.K_d]:
        angle -= rotation_speed
 

    # ---------- PLAYER 1 THRUST ----------
    if ship1_alive and keys[pygame.K_w]:
        rad = math.radians(angle-90)
        forward_x = math.cos(rad)
        forward_y = -math.sin(rad)
        vel_x += forward_x * acceleration
        vel_y += forward_y * acceleration
        create_engine_trail(x, y, forward_x, forward_y)
    if ship1_alive and player1_blade_dash_timer > 0:
        dash_x, dash_y = player1_blade_dash_dir
        vel_x = dash_x * blade_dash_speed
        vel_y = dash_y * blade_dash_speed
        create_blade_dash_trail(x, y, dash_x, dash_y)
    # ---------- PLAYER 1 PHYSICS ----------
    vel_x *= friction
    vel_y *= friction

    speed = math.hypot(vel_x, vel_y)
    current_max_speed = blade_dash_speed if player1_blade_dash_timer > 0 else max_speed
    if speed > current_max_speed:
        scale = current_max_speed / speed
        vel_x *= scale
        vel_y *= scale

    if ship1_alive:
        x += vel_x
        y += vel_y

    x %= WIDTH
    y %= HEIGHT

    # ---------- PLAYER 2 ROTATION ----------
    if ship2_alive and keys[pygame.K_LEFT]:
        angle1 += rotation_speed
    if ship2_alive and keys[pygame.K_RIGHT]:
        angle1 -= rotation_speed

    # ---------- PLAYER 2 THRUST ----------
    if ship2_alive and keys[pygame.K_UP]:
        rad1 = math.radians(angle1-270)
        forward_x1 = -math.cos(rad1)
        forward_y1 = math.sin(rad1)
        vel_x1 += forward_x1 * acceleration
        vel_y1 += forward_y1 * acceleration
        create_engine_trail(x1, y1, forward_x1, forward_y1)
    if ship2_alive and player2_blade_dash_timer > 0:
        dash_x1, dash_y1 = player2_blade_dash_dir
        vel_x1 = dash_x1 * blade_dash_speed
        vel_y1 = dash_y1 * blade_dash_speed
        create_blade_dash_trail(x1, y1, dash_x1, dash_y1)

    # ---------- PLAYER 2 PHYSICS ----------
    vel_x1 *= friction
    vel_y1 *= friction

    speed1 = math.hypot(vel_x1, vel_y1)
    current_max_speed1 = blade_dash_speed if player2_blade_dash_timer > 0 else max_speed
    if speed1 > current_max_speed1:
        scale1 = current_max_speed1 / speed1
        vel_x1 *= scale1
        vel_y1 *= scale1

    if ship2_alive:
        x1 += vel_x1
        y1 += vel_y1

    x1 %= WIDTH
    y1 %= HEIGHT
   
   
    
    # ---------- FIRE BULLETS ----------
    if ship1_cooldown > 0:
        ship1_cooldown -= 1
    if ship2_cooldown > 0:
        ship2_cooldown -= 1

    if ship1_alive and keys[pygame.K_LCTRL] and ship1_cooldown == 0:
        rad = math.radians(angle - 270)
        dir_x = -math.cos(rad)
        dir_y = math.sin(rad)
        offsets = (-11, 11) if player1_twin_shot_active else (0,)
        for offset in offsets:
            bullets.append(
                {
                    "x": x + dir_x * 35 - dir_y * offset,
                    "y": y + dir_y * 35 + dir_x * offset,
                    "vx": dir_x * bullet_speed,
                    "vy": dir_y * bullet_speed,
                    "life": bullet_life,
                    "owner": 1,
                }
            )
        ship1_cooldown = shoot_cooldown_frames

    if ship2_alive and keys[pygame.K_RCTRL] and ship2_cooldown == 0:
        rad1 = math.radians(angle1 - 270)
        dir_x1 = -math.cos(rad1)
        dir_y1 = math.sin(rad1)
        offsets = (-11, 11) if player2_twin_shot_active else (0,)
        for offset in offsets:
            bullets.append(
                {
                    "x": x1 + dir_x1 * 35 - dir_y1 * offset,
                    "y": y1 + dir_y1 * 35 + dir_x1 * offset,
                    "vx": dir_x1 * bullet_speed,
                    "vy": dir_y1 * bullet_speed,
                    "life": bullet_life,
                    "owner": 2,
                }
            )
        ship2_cooldown = shoot_cooldown_frames

    # ---------- ROTATE SHIP (PLAYER 1) ----------
    current_ship1 = ship_options[player1_ship_index]
    current_ship2 = ship_options[player2_ship_index]

    rotated_ship = pygame.transform.rotate(current_ship1, angle)
    ship_rect = rotated_ship.get_rect(center=(x, y))

    # ---------- ROTATE SHIP (PLAYER 2) ----------
    rotated_ship2 = pygame.transform.rotate(current_ship2, angle1)
    ship_rect2 = rotated_ship2.get_rect(center=(x1, y1))

    # ---------- SHIP-TO-SHIP COLLISION (ALL SHIPS, INCLUDING TITAN) ----------
    # Use each selected ship's rotated rectangle, so every ship variant uses
    # the same collision and bounce behavior.
    if ship1_alive and ship2_alive and ship_rect.colliderect(ship_rect2):
        overlap_x = min(ship_rect.right, ship_rect2.right) - max(ship_rect.left, ship_rect2.left)
        overlap_y = min(ship_rect.bottom, ship_rect2.bottom) - max(ship_rect.top, ship_rect2.top)

        if overlap_x < overlap_y:
            normal_x = 1 if x1 >= x else -1
            normal_y = 0
            separation = overlap_x / 2 + 1
        else:
            normal_x = 0
            normal_y = 1 if y1 >= y else -1
            separation = overlap_y / 2 + 1

        # Move them apart before applying a bounce, preventing overlap.
        x -= normal_x * separation
        y -= normal_y * separation
        x1 += normal_x * separation
        y1 += normal_y * separation

        impact_x = (x + x1) / 2
        impact_y = (y + y1) / 2
        blade_knockback_to_p1 = (0, 0)
        blade_knockback_to_p2 = (0, 0)

        if (
            player1_blade_dash_timer > 0
            and not player1_blade_dash_hit
            and player2_phase_protection == 0
        ):
            dash_x, dash_y = player1_blade_dash_dir
            player_health1 = max(0, player_health1 - blade_dash_damage)
            blade_knockback_to_p2 = (dash_x * blade_dash_knockback, dash_y * blade_dash_knockback)
            player1_blade_dash_hit = True
            create_blade_impact(impact_x, impact_y)

        if (
            player2_blade_dash_timer > 0
            and not player2_blade_dash_hit
            and player1_phase_protection == 0
        ):
            dash_x1, dash_y1 = player2_blade_dash_dir
            player_health = max(0, player_health - blade_dash_damage)
            blade_knockback_to_p1 = (dash_x1 * blade_dash_knockback, dash_y1 * blade_dash_knockback)
            player2_blade_dash_hit = True
            create_blade_impact(impact_x, impact_y)

        bounce_strength = 1.5
        vel_x = -vel_x * 0.7 - normal_x * bounce_strength
        vel_y = -vel_y * 0.7 - normal_y * bounce_strength
        vel_x1 = -vel_x1 * 0.7 + normal_x * bounce_strength
        vel_y1 = -vel_y1 * 0.7 + normal_y * bounce_strength
        vel_x += blade_knockback_to_p1[0]
        vel_y += blade_knockback_to_p1[1]
        vel_x1 += blade_knockback_to_p2[0]
        vel_y1 += blade_knockback_to_p2[1]

        # Bullet and missile checks below use the corrected positions.
        ship_rect = rotated_ship.get_rect(center=(x, y))
        ship_rect2 = rotated_ship2.get_rect(center=(x1, y1))

    # ---------- BULLET UPDATE + COLLISION ----------
    for bullet in bullets[:]:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]
        bullet["life"] -= 1

        if (
            bullet["x"] < -10
            or bullet["x"] > WIDTH + 10
            or bullet["y"] < -10
            or bullet["y"] > HEIGHT + 10
            or bullet["life"] <= 0
        ):
            bullets.remove(bullet)
            continue

        if (
            bullet["owner"] == 1
            and player2_blade_dash_timer > 0
            and math.hypot(bullet["x"] - x1, bullet["y"] - y1) <= blade_dash_shield_radius
        ):
            bullets.remove(bullet)
            continue

        if (
            bullet["owner"] == 1
            and player2_shield_active
            and player2_phase_protection == 0
            and math.hypot(bullet["x"] - x1, bullet["y"] - y1) <= shield_radius
        ):
            player2_shield = max(0, player2_shield - bullet.get("damage", bullet_damage))
            if player2_shield == 0:
                player2_shield_active = False
                player2_shield_duration = 0
                player2_shield_cooldown = shield_recharge_duration
            bullets.remove(bullet)
            continue

        if (
            bullet["owner"] == 1
            and ship2_alive
            and player2_phase_protection == 0
            and player2_blade_dash_timer == 0
            and ship_rect2.collidepoint(bullet["x"], bullet["y"])
        ):
            player_health1 = max(0, player_health1 - bullet.get("damage", bullet_damage))
            bullets.remove(bullet)
            if player_health1 <= 0:
                create_explosion(ship_rect2.centerx, ship_rect2.centery)
            continue

        if (
            bullet["owner"] == 2
            and player1_blade_dash_timer > 0
            and math.hypot(bullet["x"] - x, bullet["y"] - y) <= blade_dash_shield_radius
        ):
            bullets.remove(bullet)
            continue

        if (
            bullet["owner"] == 2
            and player1_shield_active
            and player1_phase_protection == 0
            and math.hypot(bullet["x"] - x, bullet["y"] - y) <= shield_radius
        ):
            player1_shield = max(0, player1_shield - bullet.get("damage", bullet_damage))
            if player1_shield == 0:
                player1_shield_active = False
                player1_shield_duration = 0
                player1_shield_cooldown = shield_recharge_duration
            bullets.remove(bullet)
            continue

        if (
            bullet["owner"] == 2
            and ship1_alive
            and player1_phase_protection == 0
            and player1_blade_dash_timer == 0
            and ship_rect.collidepoint(bullet["x"], bullet["y"])
        ):
            player_health = max(0, player_health - bullet.get("damage", bullet_damage))
            bullets.remove(bullet)
            if player_health <= 0:
                create_explosion(ship_rect.centerx, ship_rect.centery)
            continue

    # ---------- DRAW BULLETS ----------
    for bullet in bullets:
        color = bullet.get("color", (80, 220, 255) if bullet["owner"] == 1 else (255, 120, 100))
        radius = bullet.get("radius", bullet_radius)
        pygame.draw.circle(screen, color, (int(bullet["x"]), int(bullet["y"])), radius)

    # ---------------- RAVEN ABILITY: HOMING MISSILES ----------------
    for missile in missiles[:]:
        if missile["owner"] == 1:
            target_x, target_y = x1, y1
            target_alive = ship2_alive
        else:
            target_x, target_y = x, y
            target_alive = ship1_alive

        if not target_alive:
            missiles.remove(missile)
            continue

        # Steer the missile a little toward its target every frame.
        target_dx = target_x - missile["x"]
        target_dy = target_y - missile["y"]
        target_distance = math.hypot(target_dx, target_dy)
        if target_distance > 0:
            missile["vx"] += (target_dx / target_distance) * missile_turn_strength
            missile["vy"] += (target_dy / target_distance) * missile_turn_strength

        current_speed = math.hypot(missile["vx"], missile["vy"])
        if current_speed > 0:
            missile["vx"] = (missile["vx"] / current_speed) * missile_speed
            missile["vy"] = (missile["vy"] / current_speed) * missile_speed

        missile["x"] += missile["vx"]
        missile["y"] += missile["vy"]
        missile["life"] -= 1

        forward_x = missile["vx"] / missile_speed
        forward_y = missile["vy"] / missile_speed
        create_missile_trail(missile["x"], missile["y"], forward_x, forward_y)

        if missile["life"] <= 0:
            missiles.remove(missile)
            continue

        if missile["owner"] == 1:
            if (
                player2_blade_dash_timer > 0
                and math.hypot(missile["x"] - x1, missile["y"] - y1) <= blade_dash_shield_radius
            ):
                missiles.remove(missile)
                create_explosion(missile["x"], missile["y"], 25)
                continue
            if (
                player2_shield_active
                and player2_phase_protection == 0
                and math.hypot(missile["x"] - x1, missile["y"] - y1) <= shield_radius
            ):
                player2_shield = max(0, player2_shield - missile_damage)
                if player2_shield == 0:
                    player2_shield_active = False
                    player2_shield_duration = 0
                    player2_shield_cooldown = shield_recharge_duration
                missiles.remove(missile)
                create_explosion(missile["x"], missile["y"], 25)
                continue
            if (
                player2_phase_protection == 0
                and player2_blade_dash_timer == 0
                and ship_rect2.collidepoint(missile["x"], missile["y"])
            ):
                player_health1 = max(0, player_health1 - missile_damage)
                missiles.remove(missile)
                create_explosion(missile["x"], missile["y"], 55)
                continue
        else:
            if (
                player1_blade_dash_timer > 0
                and math.hypot(missile["x"] - x, missile["y"] - y) <= blade_dash_shield_radius
            ):
                missiles.remove(missile)
                create_explosion(missile["x"], missile["y"], 25)
                continue
            if (
                player1_shield_active
                and player1_phase_protection == 0
                and math.hypot(missile["x"] - x, missile["y"] - y) <= shield_radius
            ):
                player1_shield = max(0, player1_shield - missile_damage)
                if player1_shield == 0:
                    player1_shield_active = False
                    player1_shield_duration = 0
                    player1_shield_cooldown = shield_recharge_duration
                missiles.remove(missile)
                create_explosion(missile["x"], missile["y"], 25)
                continue
            if (
                player1_phase_protection == 0
                and player1_blade_dash_timer == 0
                and ship_rect.collidepoint(missile["x"], missile["y"])
            ):
                player_health = max(0, player_health - missile_damage)
                missiles.remove(missile)
                create_explosion(missile["x"], missile["y"], 55)
                continue

    # Rotate the upward-pointing missile artwork to match its travel direction.
    for missile in missiles:
        image_angle = math.degrees(math.atan2(-missile["vx"], -missile["vy"]))
        rotated_missile = pygame.transform.rotate(missile_image, image_angle)
        missile_rect = rotated_missile.get_rect(center=(missile["x"], missile["y"]))
        screen.blit(rotated_missile, missile_rect)

    # ---------- PARTICLE UPDATE ----------
    for particle in particles[:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["vx"] *= 0.97
        particle["vy"] *= 0.97
        particle["life"] -= 1
        if particle["life"] <= 0:
            particles.remove(particle)
            continue
        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            particle["size"],
        )

    if ship1_alive:
        screen.blit(rotated_ship, ship_rect.topleft)
    if ship2_alive:
        screen.blit(rotated_ship2, ship_rect2.topleft)    

    # ---------------- FALCON ABILITY: FORCE-FIELD EFFECT ----------------
    # Draw a hollow circle around every active Falcon shield.
    if player1_shield_active:
        pygame.draw.circle(screen, (80, 210, 255), (int(x), int(y)), shield_radius, 3)
    if player2_shield_active:
        pygame.draw.circle(screen, (255, 150, 100), (int(x1), int(y1)), shield_radius, 3)

    # ---------------- BLADE ABILITY: BOOST DASH SHIELD ----------------
    if player1_blade_dash_timer > 0:
        draw_blade_dash_shield(screen, x, y, player1_blade_dash_dir[0], player1_blade_dash_dir[1])
    if player2_blade_dash_timer > 0:
        draw_blade_dash_shield(screen, x1, y1, player2_blade_dash_dir[0], player2_blade_dash_dir[1])
        
    if player_health <= 0:
        text("Player 2 Wins!", font, (255, 255, 100), 48, WIDTH // 2 - 120, HEIGHT // 2 - 20)
        text("Press SPACE to return to Main Menu", font, (255, 255, 255), 30, WIDTH // 2 - 225, HEIGHT // 2 + 35)
        
    elif player_health1 <= 0:
        text("Player 1 Wins!", font, (255, 255, 100), 48, WIDTH // 2 - 120, HEIGHT // 2 - 20)
        text("Press SPACE to return to Main Menu", font, (255, 255, 255), 30, WIDTH // 2 - 225, HEIGHT // 2 + 35)
        
    pygame.display.update()

pygame.quit()
