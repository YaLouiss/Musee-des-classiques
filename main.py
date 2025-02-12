import pygame
import random
import os
from datetime import timedelta

# Initialize Pygame
pygame.init()

def get_asset_path(filename):
    # Retourne le chemin correct vers un fichier dans le dossier assets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, 'assets')
    return os.path.join(assets_dir, filename)

global last_game_state
last_game_state = "game"

start_time = pygame.time.get_ticks()

global settings_open, game_paused
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
DARK_BROWN = (70, 35, 10)
GRAY = (169, 169, 169)
BLUE = (50, 153, 213)
LIGHT_BLUE = (135, 206, 250)
GOLD = (255, 215, 0)

# Taille de l'écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Musée des Classiques")

# Taille du fond + zoom
WIDTH, HEIGHT = 960, 1280
zoom = 1.0
min_zoom = 0.5
max_zoom = 2.0

# Calculer le facteur d'échelle pour l'image du musée
scale_factor_museum = min(SCREEN_WIDTH / WIDTH, SCREEN_HEIGHT / HEIGHT)
WIDTH = int(WIDTH * scale_factor_museum)
HEIGHT = int(HEIGHT * scale_factor_museum)

# Volume and music variables
volume = 50
music_on = True

pygame.mixer.music.load(get_asset_path('musicpk.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume / 100)

# images
background = pygame.image.load(get_asset_path('musee.png'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
home_screen = pygame.image.load(get_asset_path('accueil.png'))
Dialogue_original = pygame.image.load(get_asset_path('dialogue.png'))  # Charge l'image originale

dialogue_scale_factor = 1.8  # Facteur d'agrandissement supplémentaire (exemple)

DIALOGUE_WIDTH = int(Dialogue_original.get_width() * scale_factor_museum * dialogue_scale_factor)
DIALOGUE_HEIGHT = int(Dialogue_original.get_height() * scale_factor_museum * dialogue_scale_factor)
Dialogue = pygame.transform.scale(Dialogue_original, (DIALOGUE_WIDTH, DIALOGUE_HEIGHT))

# Réduire la taille de l'écran d'accueil

scale_factor_home = min(SCREEN_WIDTH / home_screen.get_width(), SCREEN_HEIGHT / home_screen.get_height())

# Calculate the new dimensions for the home screen
HOME_WIDTH = int(home_screen.get_width() * scale_factor_home)
HOME_HEIGHT = int(home_screen.get_height() * scale_factor_home)

# Scale the home screen image
home_screen = pygame.transform.scale(home_screen, (HOME_WIDTH, HOME_HEIGHT))

# Bouton commencer
BUTTON_WIDTH = int(HOME_WIDTH * 0.4)
BUTTON_HEIGHT = int(HOME_HEIGHT * 0.15)
button_image = pygame.image.load(get_asset_path('button.png'))
button_image = pygame.transform.scale(button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

# Position du bouton relative à l'écran d'accueil
button_rect = pygame.Rect(
    int(HOME_WIDTH * 0.3),
    int(HOME_HEIGHT * 0.6),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
# Add settings button and interface variables at the top of your code
settings_button_img = pygame.image.load(get_asset_path('reglage.png'))
settings_button_img = pygame.transform.scale(settings_button_img, (150, 150))
settings_button_rect = settings_button_img.get_rect(topright=(SCREEN_WIDTH - 1, 50))


# Settings interface variables
SETTINGS_BG_COLOR = (50, 50, 50)
SETTINGS_TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)
SLIDER_COLOR = (150, 150, 150)
HANDLE_COLOR = (200, 200, 200)

# Settings interface dimensions
SETTINGS_WIDTH = 400
SETTINGS_HEIGHT = 300
SETTINGS_RECT = pygame.Rect((SCREEN_WIDTH - SETTINGS_WIDTH) // 2, (SCREEN_HEIGHT - SETTINGS_HEIGHT) // 2, SETTINGS_WIDTH, SETTINGS_HEIGHT)

# Button and slider dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 10
HANDLE_WIDTH = 10
HANDLE_HEIGHT = 20

# Volume and music variables
volume = 50
dragging_volume = False  # Track if the volume slider is being dragged
music_on = True



key_positions = [
    [
        (int(80 * scale_factor_museum), int(300 * scale_factor_museum)),
        (int(30 * scale_factor_museum), int(390 * scale_factor_museum))
    ],
    [
        (int(80 * scale_factor_museum), int(1190 * scale_factor_museum)),
        (int(80 * scale_factor_museum), int(1190 * scale_factor_museum))
    ],
    [
        (int(500 * scale_factor_museum), int(440* scale_factor_museum)),
        (int(590 * scale_factor_museum), int(620 * scale_factor_museum))
    ],
    [
        (int(500 * scale_factor_museum), int(30 * scale_factor_museum)),
        (int(770 * scale_factor_museum), int(190 * scale_factor_museum))
    ],
    [
        (int(800 * scale_factor_museum), int(1150 * scale_factor_museum)),
        (int(470 * scale_factor_museum), int(1235 * scale_factor_museum))
    ]
]

# Initialiser les clés avec une position aléatoire
# Initialiser les clés avec une position aléatoire
collectible_keys = []
for positions in key_positions:
    x, y = random.choice(positions)  # Choisir une position aléatoire
    collectible_keys.append({
        "rect": pygame.Rect(x, y, int(30 * scale_factor_museum), int(30 * scale_factor_museum)),
        "collected": False
    })


available_games = ["snake", "hangman", "platform", "tir_cible"]

# Artworks : Maintenant, chaque artwork peut potentiellement pointer vers n'importe quel jeu
artworks = [
    {"rect": pygame.Rect(int(450 * scale_factor_museum), int(750 * scale_factor_museum),
                         int(40 * scale_factor_museum), int(40 * scale_factor_museum)), "game": None},
    {"rect": pygame.Rect(int(810 * scale_factor_museum), int(750 * scale_factor_museum),
                         int(40 * scale_factor_museum), int(40 * scale_factor_museum)), "game": None},
    {"rect": pygame.Rect(int(100 * scale_factor_museum), int(610 * scale_factor_museum),
                         int(40 * scale_factor_museum), int(40 * scale_factor_museum)), "game": None},
    {"rect": pygame.Rect(int(850 * scale_factor_museum), int(450 * scale_factor_museum),
                         int(40 * scale_factor_museum), int(40 * scale_factor_museum)), "game": None},
]

# Ajouter un coffre qui augmente la vitesse
chest_positions = [
    [
        (int(310 * scale_factor_museum), int(675 * scale_factor_museum)),  # Position 1 coffre normal
        (int(830 * scale_factor_museum), int(1160 * scale_factor_museum)), # Position 1 coffre lent
        (int(440 * scale_factor_museum), int(480 * scale_factor_museum)),  # Position 1 coffre gain de temps
        (int(10 * scale_factor_museum), int(1190 * scale_factor_museum))   # Position 1 coffre perte de temps
    ],
    [
        (int(830 * scale_factor_museum), int(1160 * scale_factor_museum)), # Position 2 coffre normal
        (int(310 * scale_factor_museum), int(675 * scale_factor_museum)),  # Position 2 coffre lent
        (int(10 * scale_factor_museum), int(1190 * scale_factor_museum)),   # Position 2 coffre gain de temps
        (int(440 * scale_factor_museum), int(480 * scale_factor_museum))   # Position 2 coffre perte de temps
    ]
]

# Choisir aléatoirement un ensemble de positions pour les coffres
chosen_positions = random.choice(chest_positions)

CHEST_SIZE = int(50 * scale_factor_museum)  # Define the chest size based on the scale factor

# Ajouter un coffre qui augmente la vitesse
chest_image = pygame.image.load(get_asset_path('chest.png'))
chest_image = pygame.transform.scale(chest_image, (CHEST_SIZE, CHEST_SIZE))
chest_rect = pygame.Rect(chosen_positions[0][0], chosen_positions[0][1], CHEST_SIZE, CHEST_SIZE)
chest_collected = False

# Ajouter un coffre qui diminue la vitesse
slow_chest_image = pygame.image.load(get_asset_path('chest.png'))
slow_chest_image = pygame.transform.scale(slow_chest_image, (CHEST_SIZE, CHEST_SIZE))
slow_chest_rect = pygame.Rect(chosen_positions[1][0], chosen_positions[1][1], CHEST_SIZE, CHEST_SIZE)
slow_chest_collected = False

# Ajouter un coffre qui fait gagner du temps
time_gain_chest_image = pygame.image.load(get_asset_path('chest.png'))
time_gain_chest_image = pygame.transform.scale(time_gain_chest_image, (CHEST_SIZE, CHEST_SIZE))
time_gain_chest_rect = pygame.Rect(chosen_positions[2][0], chosen_positions[2][1], CHEST_SIZE, CHEST_SIZE)
time_gain_chest_collected = False

# Ajouter un coffre qui fait perdre du temps
time_loss_chest_image = pygame.image.load(get_asset_path('chest.png'))
time_loss_chest_image = pygame.transform.scale(time_loss_chest_image, (CHEST_SIZE, CHEST_SIZE))
time_loss_chest_rect = pygame.Rect(chosen_positions[3][0], chosen_positions[3][1], CHEST_SIZE, CHEST_SIZE)
time_loss_chest_collected = False




def assign_games_to_artworks():
    """Assigner aléatoirement les jeux aux artworks, en excluant les jeux complétés."""
    global artworks, available_games, completed_games

    # Filtrer les jeux disponibles pour exclure ceux qui sont déjà complétés
    available_games_filtered = [
        game for game in available_games if not completed_games.get(game, False)
    ]


    if not available_games_filtered:
        print("Tous les jeux ont été complétés!")

        available_games_filtered = available_games  # Utiliser tous les jeux à nouveau

    # Mélanger la liste des jeux filtrée
    random.shuffle(available_games_filtered)

    # Assigner chaque jeu à un artwork
    for i, artwork in enumerate(artworks):
        if i < len(available_games_filtered):
            artwork["game"] = available_games_filtered[i]
        else:
            # Si plus d'artworks que de jeux disponibles, on peut répéter les jeux restants
            artwork["game"] = random.choice(available_games_filtered) if available_games_filtered else None #Répéter ou laisser vide

# Joeur
SPRITE_SIZE = int(65* scale_factor_museum)
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 100, int(40 * scale_factor_museum), int(50 * scale_factor_museum))
PLAYER_SPEED = int(10 * scale_factor_museum)

# Animation du caractère
spritesheet = pygame.image.load(get_asset_path('character_spritesheet.png'))
sprite_positions = {
    'down': [(i * 65, 0) for i in range(4)],
    'left': [(i * 65, 65) for i in range(4)],
    'right': [(i * 65, 65 * 2) for i in range(4)],
    'up': [(i * 65, 65 * 3) for i in range(4)]
}

player_sprites = {
    direction: [pygame.transform.scale(
        spritesheet.subsurface(pygame.Rect(x, y, 65, 65)),
        (SPRITE_SIZE, SPRITE_SIZE)
    ) for x, y in positions]
    for direction, positions in sprite_positions.items()
}

# Animation : les variables
current_direction = 'down'
animation_frame = 0
animation_speed = 0.2
last_update = pygame.time.get_ticks()

game_paused = False
last_game_state = None

pause_time = 0
total_pause_time = 0

class TimeManager:
    
    def __init__(self):
        self.start_time = None  # Temps de départ en millisecondes
        self.total_pause_time = 0  # Temps total en pause en millisecondes
        self.pause_start_time = None  # Temps de début de la pause en millisecondes
        self.is_paused = False  # Indique si le jeu est en pause
        self.running = False 
    def pause(self):
        """Met le temps en pause."""
        if not self.is_paused:
            self.pause_start_time = pygame.time.get_ticks()
            self.is_paused = True

    def unpause(self):
        """Reprend le temps après une pause."""
        if self.is_paused:
            pause_duration = pygame.time.get_ticks() - self.pause_start_time
            self.total_pause_time += pause_duration
            self.is_paused = False

    def get_elapsed_time(self):
        """Retourne le temps écoulé en secondes."""
        if not self.running or self.start_time is None:
            return 0  # Retourne 0 si le chronomètre n'a pas démarré

        current_time = pygame.time.get_ticks()
        if self.is_paused:
            # Temps écoulé avant la pause
            elapsed_time = (self.pause_start_time - self.start_time -   self.total_pause_time) / 1000
        else:
            # Temps écoulé en tenant compte des pauses
            elapsed_time = (current_time - self.start_time - self.total_pause_time) / 1000
        return elapsed_time  # Retourne un nombre de secondes

    def start(self):
        """Démarre le chronomètre."""
        if not self.running:
            self.start_time = pygame.time.get_ticks()
            self.running = True

    def add_time(self, seconds):
        """Ajoute ou soustrait du temps (en secondes)."""
        self.start_time -= int(seconds * 1000)  # Convertir en millisecondes

    def format_time(self):
        """Formate le temps écoulé en MM:SS."""
        seconds = self.get_elapsed_time()
        if seconds < 0:
            # Gérer les temps négatifs
            seconds = abs(seconds)
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"-{minutes:02}:{seconds:02}"
        else:
            # Formater normalement
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes:02}:{seconds:02}"

time_manager = TimeManager()

def draw_timer(screen):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Temps: {time_manager.format_time()}", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, 20))

def handle_settings_button(mouse_pos, settings_open, game_state):
    global game_paused, last_game_state

    if settings_button_rect.collidepoint(mouse_pos):
        if not settings_open:
            settings_open = True
            game_paused = True
            last_game_state = game_state
            time_manager.pause()  # Mettre en pause le temps
            return settings_open, "settings"
        else:
            settings_open = False
            game_paused = False
            time_manager.unpause()  # Reprendre le temps
            return settings_open, last_game_state
    return settings_open, game_state

def draw_key_progress(screen, collectible_keys):
    """Affiche la progression de la collecte des clés."""
    total_keys = len(collectible_keys)
    collected_keys = sum(1 for key in collectible_keys if key["collected"])
    font = pygame.font.Font(None, 36)
    text = font.render(f"Fragments de Clés: {collected_keys}/{total_keys}", True, WHITE)
    screen.blit(text, (10, 50))  # Position du texte

def draw_progress(screen, completed_games):
    completed_count = sum(1 for game in completed_games.values() if game)
    total_games = len(completed_games)

    font = pygame.font.Font(None, 36)
    progress_text = font.render(f"Progression: {completed_count}/{total_games}", True, (255, 255, 255))
    screen.blit(progress_text, (10, 10))

def draw_player(surface):
    global animation_frame, last_update
    current_time = pygame.time.get_ticks()

    if current_time - last_update > animation_speed * 1000:
        animation_frame = (animation_frame + 1) % 4
        last_update = current_time

    sprite_x = player.x - (SPRITE_SIZE // 2) + (player.width // 2)
    sprite_y = player.y - (SPRITE_SIZE // 2) + (player.height // 2)

    # Ajout d'un offset vertical pour baisser le sprite
    y_offset = -10  # Ajuste cette valeur pour modifier la position verticale du sprite
    sprite_y += y_offset

    surface.blit(player_sprites[current_direction][animation_frame], (sprite_x, sprite_y))

def update_player_hitbox(y_offset=10):  # Utilise la même valeur que dans draw_player
    """Met à jour la hitbox du joueur en fonction de l'offset."""
    global player
    player.y -= y_offset 
     # Ajuste la position de la hitbox vers le haut pour compenser l'offset du sprite

# Exemple d'appel de la fonction pour mettre à jour la hitbox une fois au démarrage ou à chaque modification de l'offset
update_player_hitbox()

def detect_walkable_tiles(surface, tile_size=32):
    walkable_tiles = []
    width, height = surface.get_size()
    scaled_tile_size = int(tile_size * scale_factor_museum)

    for y in range(0, height, scaled_tile_size):
        for x in range(0, width, scaled_tile_size):
            if x + scaled_tile_size <= width and y + scaled_tile_size <= height:
                tile_rect = pygame.Rect(x, y, scaled_tile_size, scaled_tile_size)
                tile_surface = surface.subsurface(tile_rect)
                avg_color = pygame.transform.average_color(tile_surface)

                # Utiliser des plages de couleurs plus larges
                is_red = (avg_color[0] > 100 and avg_color[1] < 100 and avg_color[2] < 100)
                is_dark_brown = (30 < avg_color[0] < 150 and
                                10 < avg_color[1] < 100 and
                                0 < avg_color[2] < 70)

                if is_red or is_dark_brown:
                    walkable_tiles.append(tile_rect)

    return walkable_tiles

def show_instructions(screen, instructions, background_image):
    """Affiche les instructions du jeu avec un fond personnalisé et attend que le joueur appuie sur une touche pour commencer."""
    font = pygame.font.Font(None, 56)
    text_lines = instructions.split('\n')

    # Calculer la hauteur totale du texte
    text_height = len(text_lines) * font.get_linesize()
    text_width = max(font.size(line)[0] for line in text_lines)

    # Calculer la position centrale
    x = (SCREEN_WIDTH - text_width) // 2
    y = (SCREEN_HEIGHT - text_height) // 2

    # Afficher le fond du jeu
    screen.blit(background_image, (0, 0))

    # Afficher les instructions
    for line in text_lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (x, y))
        y += font.get_linesize()

    pygame.display.flip()

    # Attendre que le joueur appuie sur une touche
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                waiting = False

    return True


def is_on_walkable_tile(player_rect):
    return any(tile.collidepoint(player_rect.center) for tile in walkable_tiles)

key_image = pygame.image.load(get_asset_path('key.png'))  # Charger une image de clé
key_image = pygame.transform.scale(key_image, (30, 30))


def draw_game():
    global PLAYER_SPEED, chest_collected, slow_chest_collected

    game_surface = pygame.Surface((WIDTH, HEIGHT))
    game_surface.blit(background, (0, 0))

    # Dessiner les clés
    for key in collectible_keys:
        if not key["collected"]:
            game_surface.blit(key_image, key["rect"].topleft)

    # Dessiner les coffres
    if not chest_collected:
        game_surface.blit(chest_image, chest_rect.topleft)
    if not slow_chest_collected:
        game_surface.blit(slow_chest_image, slow_chest_rect.topleft)
    if not time_gain_chest_collected:
        game_surface.blit(time_gain_chest_image, time_gain_chest_rect.topleft)
    if not time_loss_chest_collected:
        game_surface.blit(time_loss_chest_image, time_loss_chest_rect.topleft)

    draw_player(game_surface)

    # Ajouter l'image en bas à gauche
    game_surface.blit(Dialogue, (int(-10 * scale_factor_museum), int(HEIGHT - 320 * scale_factor_museum)))

    zoomed_width = int(WIDTH * zoom)
    zoomed_height = int(HEIGHT * zoom)
    zoomed_surface = pygame.transform.scale(game_surface, (zoomed_width, zoomed_height))

    screen.fill(BLACK)
    x_offset = (SCREEN_WIDTH - zoomed_width) // 2
    y_offset = (SCREEN_HEIGHT - zoomed_height) // 2
    screen.blit(zoomed_surface, (x_offset, y_offset))

    # Draw the key progress
    draw_key_progress(screen, collectible_keys)


def draw_settings_interface(screen):
    global volume, music_on
    # Draw the background
    pygame.draw.rect(screen, SETTINGS_BG_COLOR, SETTINGS_RECT)

    # Draw the title
    font = pygame.font.Font(None, 36)
    title_text = font.render("Paramètre", True, SETTINGS_TEXT_COLOR)
    screen.blit(title_text, (SETTINGS_RECT.x + 20, SETTINGS_RECT.y + 20))

    # Draw the close button
    close_button_rect = pygame.Rect(SETTINGS_RECT.right - BUTTON_WIDTH - 20, SETTINGS_RECT.y + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, close_button_rect)
    close_text = font.render("Fermer", True, SETTINGS_TEXT_COLOR)
    screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y + 10))

    # Draw the volume slider
    slider_rect = pygame.Rect(SETTINGS_RECT.x + 100, SETTINGS_RECT.y + 100, SLIDER_WIDTH, SLIDER_HEIGHT)
    pygame.draw.rect(screen, SLIDER_COLOR, slider_rect)

    # Draw the volume handle
    handle_x = slider_rect.x + int((volume / 100) * SLIDER_WIDTH) - HANDLE_WIDTH // 2
    handle_rect = pygame.Rect(handle_x, slider_rect.y - 5, HANDLE_WIDTH, HANDLE_HEIGHT)
    pygame.draw.rect(screen, HANDLE_COLOR, handle_rect)

    # Draw the volume text
    volume_text = font.render(f"Volume: {volume}%", True, SETTINGS_TEXT_COLOR)
    screen.blit(volume_text, (slider_rect.x, slider_rect.y - 30))

    # Draw the music toggle button
    music_button_rect = pygame.Rect(SETTINGS_RECT.x + 100, SETTINGS_RECT.y + 150, BUTTON_WIDTH+20, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, music_button_rect)
    music_text = font.render("Musique: On" if music_on else "Musique: Off", True, SETTINGS_TEXT_COLOR)
    screen.blit(music_text, (music_button_rect.x + 10, music_button_rect.y + 10))

    pygame.mixer.music.set_volume(volume / 100)

    return close_button_rect, handle_rect, music_button_rect,

def jeu_tir_cible():
    # Paramètres de la fenêtre
    tir_cible_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = tir_cible_window.get_size()
    pygame.display.set_caption("Tir à la Cible")

    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Chargement des images
    target_image = pygame.image.load(get_asset_path("pacman.png"))
    target_image = pygame.transform.scale(target_image, (200, 100))  # Redimensionner l'image de la cible
    background_image = pygame.image.load(get_asset_path("fond_pacman.png"))
    background_width, background_height = 800, 600  # Taille souhaitée pour l'image de fond
    background_image = pygame.transform.scale(background_image, (background_width, background_height))

    # Positionner l'image de fond au centre de l'écran
    background_x = (SCREEN_WIDTH - background_width) // 2
    background_y = (SCREEN_HEIGHT - background_height) // 2

    # Paramètres du jeu
    score = 0
    clock = pygame.time.Clock()
    time_limit = 20  # Durée du jeu en secondes
    target_limit = 25  # Limite de cibles à toucher
    start_time = pygame.time.get_ticks()

    # Générer une cible aléatoire
    def new_target():
        # Ajuster les coordonnées pour qu'elles soient à l'intérieur de l'image de fond
        x = random.randint(background_x + 100, background_x + background_width - 100)
        y = random.randint(background_y + 50, background_y + background_height - 50)
        return x, y

    target_x, target_y = new_target()

    # Boucle du jeu
    running = True
    while running:
        # Afficher l'image de fond
        tir_cible_window.blit(background_image, (background_x, background_y))

        # Afficher la cible
        tir_cible_window.blit(target_image, (target_x - 100, target_y - 50))

        # Calculer le temps restant
        current_time = (pygame.time.get_ticks() - start_time) // 1000
        time_left = max(0, time_limit - current_time)

        # Affichage du score et du temps restant avec un fond noir
        font = pygame.font.SysFont("Arial", 36)  # Utiliser une police système valide
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Temps restant: {time_left}s", True, WHITE)

        # Dessiner un fond noir derrière le texte
        pygame.draw.rect(tir_cible_window, BLACK, (10, 10, 300, 50))  # Rectangle pour le score
        pygame.draw.rect(tir_cible_window, BLACK, (10, 50, 300, 50))  # Rectangle pour le temps

        # Afficher le texte
        tir_cible_window.blit(score_text, (10, 10))
        tir_cible_window.blit(time_text, (10, 50))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "lose"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Vérifier si le clic est dans la zone rectangulaire de la cible
                if target_x - 100 <= mouse_x <= target_x + 100 and target_y - 50 <= mouse_y <= target_y + 50:
                    score += 1
                    target_x, target_y = new_target()

        # Fin du jeu après 20 cibles touchées ou 20 secondes
        if score >= target_limit or time_left == 0:
            running = False

        pygame.display.flip()
        clock.tick(30)

    # Affichage du score final et message de fin
    tir_cible_window.fill(WHITE)

# Vérifier si le joueur a gagné ou perdu
    if score >= target_limit:
        final_text = font.render(f"Félicitations, vous avez gagné ! Score final: {score}", True, BLACK)
        result = "victory"
    else:
        final_text = font.render(f"Dommage, vous avez perdu ! Score final: {score}", True, BLACK)
        result = "lose"

# Centrer le texte
    text_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    tir_cible_window.blit(final_text, text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)

    # Retour à l'écran principal
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Museum of Classics")
    return result

def jeu_snake():

    snake_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Snake Game")

    #  images
    original_head = pygame.transform.scale(pygame.image.load(get_asset_path("serpent.png")), (60, 60))
    #Permet de tourner la tete du snake
    head_images = {
        "RIGHT": original_head,
        "LEFT": pygame.transform.rotate(original_head, 180),
        "UP": pygame.transform.rotate(original_head, 90),
        "DOWN": pygame.transform.rotate(original_head, 270)
    }
    apple_img = pygame.transform.scale(pygame.image.load(get_asset_path("pomme.png")), (30, 30))
    bg_img = pygame.transform.scale(pygame.image.load(get_asset_path("background_snake.png")), (600, 450))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 25)

    def game_loop():

        cell_size = 30
        snake_pos = [[300, 210]]
        direction = "LEFT"
        apple_pos = [random.randrange(1, 19) * cell_size,
                    random.randrange(1, 13) * cell_size]
        score = 0
        speed = 9.5

        x_offset = (SCREEN_WIDTH - 600) // 2
        y_offset = (SCREEN_HEIGHT - 450) // 2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "lose"
                    elif event.key == pygame.K_LEFT and direction != "RIGHT":
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        direction = "RIGHT"
                    elif event.key == pygame.K_UP and direction != "DOWN":
                        direction = "UP"
                    elif event.key == pygame.K_DOWN and direction != "UP":
                        direction = "DOWN"

            # Directions , commandes
            if direction == "LEFT":
                new_head = [snake_pos[0][0] - cell_size, snake_pos[0][1]]
            elif direction == "RIGHT":
                new_head = [snake_pos[0][0] + cell_size, snake_pos[0][1]]
            elif direction == "UP":
                new_head = [snake_pos[0][0], snake_pos[0][1] - cell_size]
            elif direction == "DOWN":
                new_head = [snake_pos[0][0], snake_pos[0][1] + cell_size]

            # Collision avec les murs
            if (new_head[0] < 0 or new_head[0] >= 600 or
                new_head[1] < 0 or new_head[1] >= 450 or
                new_head in snake_pos[1:]):
                text = font.render(f"Dommage! Score: {score}", True, WHITE)
                snake_window.blit(text, (x_offset + 200, y_offset + 200))
                pygame.display.flip()
                pygame.time.wait(2000)
                return "lose"

            snake_pos.insert(0, new_head)

            # Collision avec les pommes
            if (abs(snake_pos[0][0] - apple_pos[0]) < cell_size and
                abs(snake_pos[0][1] - apple_pos[1]) < cell_size):
                score += 1
                if score >= 20:
                    snake_window.fill(BLACK)
                    snake_window.blit(bg_img, (x_offset, y_offset))
                    win_text = font.render("GG tu as Gagné!", True, WHITE)
                    snake_window.blit(win_text, (x_offset + 200, y_offset + 200))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    return "victory"

                apple_pos = [random.randrange(1, 19) * cell_size,
                            random.randrange(1, 13) * cell_size]
                while apple_pos in snake_pos:
                    apple_pos = [random.randrange(1, 19) * cell_size,
                                random.randrange(1, 13) * cell_size]
            else:
                snake_pos.pop()

            snake_window.fill(BLACK)
            snake_window.blit(bg_img, (x_offset, y_offset))
            snake_window.blit(apple_img, (x_offset + apple_pos[0], y_offset + apple_pos[1]))

            head_offset = 15
            head_img = head_images[direction]
            snake_window.blit(head_img,
                            (x_offset + snake_pos[0][0] - head_offset,
                             y_offset + snake_pos[0][1] - head_offset))

            for pos in snake_pos[1:]:
                pygame.draw.rect(snake_window, BLACK,
                               [x_offset + pos[0], y_offset + pos[1],
                                cell_size, cell_size])

            score_text = font.render(f"Score: {score}", True, LIGHT_BLUE)
            snake_window.blit(score_text, (x_offset + 10, y_offset + 10))

            pygame.display.flip()
            clock.tick(speed)

    result = game_loop()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Museum of Classics")
    return result

def jeu_pendu():

    PENDU_WIDTH, PENDU_HEIGHT = 800, 650
    pendu_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Le Jeu du Pendu")

    SCREEN_WIDTH, SCREEN_HEIGHT = pendu_window.get_size()
    CENTER_X = (SCREEN_WIDTH - PENDU_WIDTH) // 2
    CENTER_Y = (SCREEN_HEIGHT - PENDU_HEIGHT) // 2

    # Dictionnaire de mots
    mots = [
        "CHAT", "CHIEN", "MAISON", "ARBRE", "FLEUR", "SOLEIL", "LUNE", "ETOILE",
        "OISEAU", "LIVRE", "CRAYON", "POMME", "ORANGE", "BANANE", "FRAISE",
        "VELO", "AVION", "BATEAU", "TRAIN", "PLAGE", "FORET", "ECOLE"
        , "SPORT", "CINEMA", "MUSEE", "PARC", "ZOO", "CIRQUE", "FETE",
        "JOUET", "BALLON", "POUPEE", "ROBOT", "PUZZLE", "CARTE", "LEGO",
        "PATE", "DESSIN", "CRAIE", "STYLO", "CAHIER", "BUREAU", "CHAISE", "TABLE",
        "LIT", "LAMPE", "TAPIS","NSI", "SCEAU","NABI","BARRE","KANOE"
    ]

    mot_a_deviner = random.choice(mots)
    lettres_trouvees = set()
    lettres_utilisees = set()
    erreurs = 0
    max_erreurs = 7

    # Fonction pour la transparence
    def rendre_transparent(surface):
        surface = surface.convert_alpha()
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = surface.get_at((x, y))
                if (r, g, b) == (255, 255, 255):
                    surface.set_at((x, y), (255, 255, 255, 0))
        return surface

    # Le fond
    pendu_complet = pygame.image.load(get_asset_path("pendo.png"))
    largeur_sprite = pendu_complet.get_width() // 4
    hauteur_sprite = pendu_complet.get_height() // 2

    # Faire en sorte que l'image soit transparent
    images_pendu = []
    for y in range(2):
        for x in range(4):
            rect = pygame.Rect(x * largeur_sprite, y * hauteur_sprite,
                               largeur_sprite, hauteur_sprite)
            image = pendu_complet.subsurface(rect)
            image = pygame.transform.scale(image,
                                            (int(largeur_sprite * 0.8), int(hauteur_sprite * 0.8)))
            image = rendre_transparent(image)
            images_pendu.append(image)

    # Importer le fond
    fond = pygame.image.load(get_asset_path("fond.png"))
    fond = pygame.transform.scale(fond, (PENDU_WIDTH, PENDU_HEIGHT))

    running = True
    clock = pygame.time.Clock()
    game_result = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "lose"
                elif event.unicode.isalpha():
                    lettre = event.unicode.upper()
                    if lettre not in lettres_utilisees:
                        lettres_utilisees.add(lettre)
                        if lettre in mot_a_deviner:
                            lettres_trouvees.add(lettre)
                        else:
                            erreurs += 1

        pendu_window.fill(BLACK)

        # Draw game background
        pendu_window.blit(fond, (CENTER_X, CENTER_Y))

        # Changement de dessin pour chaque erreur
        if erreurs < len(images_pendu):
            image_pendu = images_pendu[erreurs]
            pendu_window.blit(image_pendu,
                              (CENTER_X + PENDU_WIDTH // 2 - image_pendu.get_width() // 2,
                               CENTER_Y + PENDU_HEIGHT // 2 - image_pendu.get_height() // 2 - 50))

        font = pygame.font.Font(None, 72)
        affichage = " ".join(l if l in lettres_trouvees else "_"
                             for l in mot_a_deviner)
        texte = font.render(affichage, True, BLACK)
        pendu_window.blit(texte,
                          (CENTER_X + PENDU_WIDTH // 2 - texte.get_width() // 2,
                           CENTER_Y + PENDU_HEIGHT // 2 + 150))

        # Display used letters
        font_lettres = pygame.font.Font(None, 36)
        texte_lettres = font_lettres.render(
            "Lettres utilisées : " + " ".join(sorted(lettres_utilisees)),
            True, BLACK)
        pendu_window.blit(texte_lettres,
                          (CENTER_X + PENDU_WIDTH // 2 - texte_lettres.get_width() // 2,
                           CENTER_Y + PENDU_HEIGHT // 2 + 200))

        # Boucle if pour savoir quand le jeu se ferme
        if erreurs >= max_erreurs:
            texte_fin = font.render(
                "Perdu ! Le mot était : " + mot_a_deviner, True, BLACK)
            pendu_window.blit(texte_fin,
                              (CENTER_X + PENDU_WIDTH // 2 - texte_fin.get_width() // 2,
                               CENTER_Y + PENDU_HEIGHT // 2 + 100))
            pygame.display.flip()
            pygame.time.wait(2000)
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.set_caption("Museum of Classics")
            return "lose"
        elif set(mot_a_deviner) <= lettres_trouvees:
            texte_fin = font.render("Gagné !", True, BLACK)
            pendu_window.blit(texte_fin,
                              (CENTER_X + PENDU_WIDTH // 2 - texte_fin.get_width() // 2,
                               CENTER_Y + PENDU_HEIGHT // 2 + 100))
            pygame.display.flip()
            pygame.time.wait(2000)
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.set_caption("Museum of Classics")
            return "victory"

        pygame.display.flip()
        clock.tick(30)

    return True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(get_asset_path('voleur.png')), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 600 - 100
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_available = 1
        self.in_air = False

    def update(self, platforms):
        self.velocity_y += 0.5
        if self.velocity_y > 10:
            self.velocity_y = 10

        self.rect.x += self.velocity_x
        self.handle_horizontal_collision(platforms)

        self.rect.y += self.velocity_y
        self.handle_vertical_collision(platforms)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.land()

    def handle_horizontal_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                self.jump_available = 2

    def handle_vertical_collision(self, platforms):
        self.in_air = True
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.land()
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def land(self):
        self.velocity_y = 0
        self.in_air = False
        self.jump_available = 1

    def jump(self):
        if self.jump_available > 0:
            self.velocity_y = -12
            self.jump_available -= 1
            self.in_air = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, 20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(get_asset_path('pomme.png')), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_coin(platforms):
    while True:
        x = random.randint(150, 750)
        y = random.randint(100, 450)
        coin = Coin(x, y)
        if not pygame.sprite.spritecollideany(coin, platforms):
            return coin

def jeu_platform():

    platform_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Platform Game")

    # Fond du jeu
    background_img = pygame.image.load(get_asset_path('macronisme.png'))
    background_img = pygame.transform.scale(background_img, (800, 600))

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Creation des rectangles
    platform_positions = [
        (0, 550, 800),
        (100, 500, 200),
        (400, 400, 200),
        (200, 300, 150),
        (500, 200, 150)
    ]

    for x, y, width in platform_positions:
        platform = Platform(x, y, width)
        all_sprites.add(platform)
        platforms.add(platform)

    # Creation des pieces à manger
    for _ in range(5):
        coin = create_coin(platforms)
        all_sprites.add(coin)
        coins.add(coin)

    score = 0
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = True

    x_offset = (SCREEN_WIDTH - 800) // 2
    y_offset = (SCREEN_HEIGHT - 600) // 2

    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "lose"
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_z:
                    player.jump()

        keys = pygame.key.get_pressed()
        player.velocity_x = 0
        if keys[pygame.K_LEFT]or keys[pygame.K_q]:
            player.velocity_x = -5
        if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
            player.velocity_x = 5

        player.update(platforms)

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        score += len(collected_coins)

        # RESpawn  des ouevres
        while len(coins) < 5:
            coin = create_coin(platforms)
            all_sprites.add(coin)
            coins.add(coin)

        # Les win conditions
        if score >= 20 or elapsed_time >= 35:
            platform_window.fill(BLACK)
            font = pygame.font.Font(None, 60)
            if elapsed_time >= 35:
                text = font.render("Tu as Perdu", True, RED)
                result = "lose"
            else:
                text = font.render(f"Tu as Gagné ! En {(current_time - start_time)/1000} secondes", True, GOLD)
                result = "victory"
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            platform_window.blit(text, text_rect)

            pygame.display.flip()
            pygame.time.wait(4000)
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.set_caption("Museum of Classics")
            return result

        platform_window.fill(BLACK)
        platform_window.blit(background_img, (x_offset, y_offset))

        # Draw all sprites
        for sprite in all_sprites:
            platform_window.blit(sprite.image, (sprite.rect.x + x_offset, sprite.rect.y + y_offset))

        # Ecran de fin
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}/20", True, WHITE)
        time_text = font.render(f"Time: {35 - elapsed_time:.1f}", True, WHITE)
        platform_window.blit(score_text, (x_offset + 20, y_offset + 20))
        platform_window.blit(time_text, (x_offset + 600, y_offset + 20))

        pygame.display.flip()
        clock.tick(60)

    return True

def launch_game(game_type):
    if game_type == "snake":
        instructions = (
            "Bienvenue dans le jeu Snake!\n\n"
            "Utilisez les flèches directionnelles pour contrôler le serpent.\n"
            "Mangez les pommes pour grandir et gagner des points.\n"
            "Évitez de heurter les murs ou vous-même.\n\n"
            "Appuyez sur n'importe quelle touche pour commencer..."
        )
        background_image = pygame.transform.scale(pygame.image.load(get_asset_path("background_snake.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
        if not show_instructions(screen, instructions, background_image):
            return "quit"
        return jeu_snake()

    elif game_type == "hangman":
        instructions = (
            "Bienvenue dans le jeu du Pendu!\n\n"
            "Devinez le mot en proposant des lettres.\n"
            "Vous avez un nombre limité d'essais avant de perdre.\n\n"
            "Appuyez sur n'importe quelle touche pour commencer..."
        )
        background_image = pygame.transform.scale(pygame.image.load(get_asset_path("fond.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
        if not show_instructions(screen, instructions, background_image):
            return "quit"
        return jeu_pendu()

    elif game_type == "platform":
        instructions = (
            "Bienvenue dans le jeu de Plateforme!\n\n"
            "Utilisez les flèches directionnelles pour vous déplacer.\n"
            "Sautez sur les plateformes et collectez 20 pièces.\n"
            "Évitez de tomber !.\n\n"
            "Appuyez sur n'importe quelle touche pour commencer..."
        )
        background_image = pygame.transform.scale(pygame.image.load(get_asset_path("macronisme.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
        if not show_instructions(screen, instructions, background_image):
            return "quit"
        return jeu_platform()

    elif game_type == "tir_cible":
        instructions = (
            "Bienvenue dans le jeu Tir à la Cible!\n\n"
            "Cliquez sur les cibles pour marquer des points.\n"
            "Vous avez un temps limité pour atteindre un certain 25 cibles.\n\n"
            "Appuyez sur n'importe quelle touche pour commencer..."
        )
        background_image = pygame.transform.scale(pygame.image.load(get_asset_path("fond_pacman.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
        if not show_instructions(screen, instructions, background_image):
            return "quit"
        return jeu_tir_cible()

    return False


completed_games = {
    "snake": False,
    "hangman": False,
    "platform": False,
    "tir_cible": False
}

start_time = None
total_time = timedelta()



def draw_progress_and_time(screen, completed_games, start_time):
    """Affiche la progression et le timer"""
    # Calcul du nombre de jeux complétés
    completed_count = sum(1 for game in completed_games.values() if game)
    total_games = len(completed_games)

    # Création de la barre de progression
    font = pygame.font.Font(None, 36)
    progress_text = font.render(f"Jeux complétés: {completed_count}/{total_games}", True, WHITE)

    # Position en haut de l'écran
    margin = 20
    screen.blit(progress_text, (margin, margin))
active_messages = []

def show_message(screen, message, duration=2000):
    """Affiche un message temporairement en bas à gauche sous la progression des clés."""
    global active_messages

    font = pygame.font.Font(None, 36)
    active_messages.append((message, pygame.time.get_ticks(), duration))

def draw_messages(screen):
    """Dessine les messages actifs en les empilant sous la progression des clés."""
    global active_messages

    font = pygame.font.Font(None, 36)
    current_time = pygame.time.get_ticks()
    
    # Supprime les messages expirés
    active_messages = [msg for msg in active_messages if current_time - msg[1] < msg[2]]

    # Position de base sous la progression des clés
    x, y = 10, 90  # Ajuste "90" si nécessaire pour éviter le chevauchement

    for message, start_time, duration in active_messages:
        text = font.render(message, True, (255, 255, 255))
        screen.blit(text, (x, y))
        y += 40

# Messages spécifiques pour chaque type de coffre
chest_message = "Augmentation de Vitesse !"
slow_chest_message = "Perte  de Vitesse !"
time_gain_message = "Ajout de temps !"
time_loss_message = "Baisse de temps !"

def check_artwork_collisions(player, artworks, completed_games, collectible_keys):
    global chest_collected, slow_chest_collected, time_gain_chest_collected, time_loss_chest_collected, PLAYER_SPEED, start_time, total_time

    # Vérifie les collisions avec les œuvres d'art et les clés
    for artwork in artworks:
        if player.colliderect(artwork["rect"]):
            artwork_x = artwork["rect"].centerx
            artwork_y = artwork["rect"].centery

            # Lancer le mini-jeu
            result = launch_game(artwork["game"])
            if result == "quit":
                return False
            elif result == "victory":
                completed_games[artwork["game"]] = True
            # Repositionner le joueur après le mini-jeu
            move_distance = 60
            if player.centerx < artwork_x:
                player.x = artwork["rect"].left - player.width - move_distance
            else:
                player.x = artwork["rect"].right + move_distance

            if player.centery < artwork_y:
                player.y = artwork["rect"].top - player.height - move_distance
            else:
                player.y = artwork["rect"].bottom + move_distance

            # Vérifier que le joueur réapparaît sur une zone accessible
            if not is_on_walkable_tile(player):
                player.x = WIDTH // 2
                player.y = HEIGHT - 100

            break

    # Vérifier les collisions avec les clés
    for key in collectible_keys:
        if not key["collected"] and player.colliderect(key["rect"]):
            key["collected"] = True

    # Vérifier les collisions avec les coffres
    if not chest_collected and player.colliderect(chest_rect):
        chest_collected = True
        PLAYER_SPEED = int(PLAYER_SPEED * 1.5)  # Augmenter la vitesse du joueur
        show_message(screen, chest_message, 10000)

    if not slow_chest_collected and player.colliderect(slow_chest_rect):
        slow_chest_collected = True
        PLAYER_SPEED = int(PLAYER_SPEED * 0.75)  # Diminuer la vitesse du joueur
        show_message(screen, slow_chest_message, 10000)

    if not time_gain_chest_collected and player.colliderect(time_gain_chest_rect):
        time_gain_chest_collected = True
        time_manager.add_time(+10)
        show_message(screen, time_gain_message, 10000)

    if not time_loss_chest_collected and player.colliderect(time_loss_chest_rect):
        time_loss_chest_collected = True
        time_manager.add_time(-10)
        show_message(screen, time_loss_message, 10000)

    return True
def draw_instructions(screen):
    """Affiche les instructions à droite de l'écran, sous le temps."""
    try:
        # Essayer d'abord avec Segoe UI Emoji (Windows)
        font = pygame.font.SysFont("Segoe UI Emoji", int(31 * scale_factor_museum))
    except:
        try:
            # Sinon essayer Apple Color Emoji (Mac)
            font = pygame.font.SysFont("Apple Color Emoji", int(31 * scale_factor_museum))
        except:
            # Si aucune police emoji n'est disponible, utiliser la police par défaut
            font = pygame.font.Font(None, int(31 * scale_factor_museum))
    
    LIGHT_BLUE = (135, 206, 250)

    instructions = [
        "📋 Instructions :",
        "🎨 Cherche les 4 œuvres à travers",
        "les différents monuments.",
        "",
        "🔍 Résous-les pour voler l'œuvre d'art.",
        "",
        "🔑 Trouve les fragments de clés",
        "pour pouvoir sortir.",
        "",
        "⬆️⬅️➡️⬇️ : pour se déplacer",
        "et jouer aux jeux.",
        "",
        "❌ Échap : Parametre/Quitter ."
    ]
    
    x = SCREEN_WIDTH - int(600 * scale_factor_museum)  # Position à droite ajustée
    y = int(250 * scale_factor_museum)  # Position verticale initiale ajustée
    
    for line in instructions:
        text = font.render(line, True, WHITE)
        screen.blit(text, (x, y))
        y += int(30 * scale_factor_museum)  # Espacement entre les lignes ajusté


def check_victory_condition(completed_games, keys, screen):
    global total_time

    if all(completed_games.values()) and all(key["collected"] for key in collectible_keys):
        # Créer un fond semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Afficher le texte de victoire et le temps final
        font = pygame.font.Font(None, 50)
        victory_text = font.render("FÉLICITATIONS! Vous avez terminé tous les jeux et trouvé les clés!", True, WHITE)
        time_text = font.render(f"Temps total: {time_manager.format_time()}", True, WHITE)

        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

        screen.blit(victory_text, text_rect)
        screen.blit(time_text, time_rect)

        pygame.display.flip()
        pygame.time.wait(10000)
        return False

    return True
# Main game setup
clock = pygame.time.Clock()
FPS = 60
game_state = "menu"
walkable_tiles = detect_walkable_tiles(background)

# Main game loop
running = True
settings_open = False  # Track if the settings interface is open
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if settings_open:
                    if close_button_rect.collidepoint(mouse_pos):
                        settings_open = False
                        game_paused = False
                        game_state = last_game_state
                        time_manager.unpause()  # Reprendre le temps lorsque le jeu reprend
                    elif handle_rect.collidepoint(mouse_pos):
                        dragging_volume = True
                    elif music_button_rect.collidepoint(mouse_pos):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                else:
                    settings_open, game_state = handle_settings_button(mouse_pos, settings_open, game_state)

                    if not game_paused and game_state == "menu":
                        adjusted_x = mouse_pos[0] - (SCREEN_WIDTH - HOME_WIDTH) // 2
                        adjusted_y = mouse_pos[1] - (SCREEN_HEIGHT - HOME_HEIGHT) // 2
                        if button_rect.collidepoint(adjusted_x, adjusted_y):
                            game_state = "game"
                            start_time = pygame.time.get_ticks()  # Réinitialiser le timer

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_volume = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_volume and settings_open:
                mouse_pos = pygame.mouse.get_pos()
                relative_x = mouse_pos[0] - (SETTINGS_RECT.x + 100)
                new_volume = int((relative_x / SLIDER_WIDTH) * 100)
                volume = max(0, min(100, new_volume))
                pygame.mixer.music.set_volume(volume / 100)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "game":  # Si le jeu est en cours
                    game_paused = not game_paused  # Basculer entre pause et reprise
                    if game_paused:
                        last_game_state = game_state
                        game_state = "settings"  # Ouvrir les paramètres
                        settings_open = True  # Activer l'interface des paramètres
                        time_manager.pause()  # Mettre le jeu en pause
                    else:
                        game_state = last_game_state  # Revenir au jeu
                        settings_open = False  # Désactiver l'interface des paramètres
                        time_manager.unpause()  # Reprendre le jeu
                elif game_state == "settings":  # Si les paramètres sont ouverts
                    game_paused = False
                    game_state = last_game_state  # Revenir au jeu
                    settings_open = False  # Désactiver l'interface des paramètres
                    time_manager.unpause()  # Reprendre le jeu
        elif event.type == pygame.MOUSEWHEEL:
            zoom = max(min_zoom, min(max_zoom, zoom + event.y * 0.1))

    # Ne mettre à jour le jeu que s'il n'est pas en pause
    if not game_paused:
        if game_state == "menu":
            assign_games_to_artworks()
            screen.fill(BLACK)
            x_offset = (SCREEN_WIDTH - HOME_WIDTH) // 2
            y_offset = (SCREEN_HEIGHT - HOME_HEIGHT) // 2
            screen.blit(home_screen, (x_offset, y_offset))
            screen.blit(button_image, (x_offset + button_rect.x, y_offset + button_rect.y))

        elif game_state == "game":
            screen.fill(BLACK)
            time_manager.start()
            # Gestion des mouvements du joueur
            keys = pygame.key.get_pressed()
            new_x = player.x
            new_y = player.y

            if keys[pygame.K_LEFT] or keys[pygame.K_q]:  # Flèche gauche ou Q
                new_x -= PLAYER_SPEED
                current_direction = 'left'
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Flèche droite ou D
                new_x += PLAYER_SPEED
                current_direction = 'right'
            if keys[pygame.K_UP] or keys[pygame.K_z]:  # Flèche haut ou Z
                new_y -= PLAYER_SPEED
                current_direction = 'up'
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Flèche bas ou S
                new_y += PLAYER_SPEED
                current_direction = 'down'

            new_pos = pygame.Rect(new_x, new_y, player.width, player.height)

            if is_on_walkable_tile(new_pos):
                player.x = max(0, min(new_x, WIDTH - player.width))
                player.y = max(0, min(new_y, HEIGHT - player.height))

            if not check_artwork_collisions(player, artworks, completed_games, collectible_keys):
                running = False
                break

            draw_game()
            draw_progress(screen, completed_games)
            draw_timer(screen)
            draw_messages(screen)
            draw_instructions(screen)

            if not check_victory_condition(completed_games, keys, screen):
                running = False
                break

    # Toujours afficher ces éléments, même en pause
    screen.blit(settings_button_img, settings_button_rect)

    if settings_open:
        close_button_rect, handle_rect, music_button_rect = draw_settings_interface(screen)

    pygame.display.flip()
    
pygame.quit()