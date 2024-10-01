import pygame
import sys
import math
import config

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_RADIUS = 25
FPS = 60
HIGH_SCORE_FILE = "highscore.txt"


# Colors
WHITE = (255, 255, 255)
DARK_GRAY = (60, 60, 60)  # Background color
LIGHT_GRAY = (200, 200, 200)  # Light gray for settings window
BUTTON_COLOR = (50, 50, 50)  # Button color (dark)
BUTTON_HOVER_COLOR = (80, 80, 80)  # Darker button color on hover
OPAQUE_COLOR = (0, 0, 0, 100)  # Semi-transparent overlay for exit confirmation
TRANSPARENT_COLOR = (0, 0, 0, 50)  # Slightly transparent overlay
SHADOW_COLOR = (0, 0, 0, 80)  # Shadow color

# Constants for volume and screen resolutions
VOLUME_LEVELS = [0, 25, 50, 75, 100]
RESOLUTIONS = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
fullscreen = False
volume = 50  # Default volume level
resolution = RESOLUTIONS[0]  # Default resolution

# Setup the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Font setup
fonts = pygame.font.get_fonts()
font = pygame.font.SysFont("Retro Gaming", 25)

# Button class
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.hovered = False  # Track if the button is hovered over

    def draw(self, surface):
        # Draw shadow
        shadow_rect = pygame.Rect(self.x + 5, self.y + 5, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(surface, SHADOW_COLOR, shadow_rect, border_radius=BUTTON_RADIUS)

        # Draw rounded rectangle
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, (self.x, self.y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=BUTTON_RADIUS)

        # Draw text
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x + BUTTON_WIDTH // 2, self.y + BUTTON_HEIGHT // 2))
        surface.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        # Check matching position with mouse
        if (self.x <= mouse_pos[0] <= self.x + BUTTON_WIDTH and
                self.y <= mouse_pos[1] <= self.y + BUTTON_HEIGHT):
            return True
        return False

    def check_hover(self, mouse_pos):
        self.hovered = self.check_click(mouse_pos)

# Load high score from file
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  # Return 0 if no high score file exists or is invalid

# Save high score to file
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Main menu function
def main_menu(game):
    pygame.display.set_mode((800, 600))
    settings_button = Button("Settings", 20, HEIGHT - 70)  # Bottom left corner
    exit_button = Button("Exit", WIDTH - 220, HEIGHT - 70)  # Bottom right corner
    high_score = load_high_score()  # Load the high score

    while True:
        win.fill(DARK_GRAY)

        # Logo title in the center
        logo_text = font.render("A Star Wars Game", True, WHITE)
        logo_rect = logo_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        win.blit(logo_text, logo_rect)

        # Click anywhere to play prompt with hover animation
        time_passed = pygame.time.get_ticks() / 1000  # Time in seconds
        hover_y_offset = math.sin(time_passed * 2) * 5  # Up and down animation
        click_prompt = font.render("Click Anywhere to Play", True, WHITE)
        prompt_rect = click_prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + hover_y_offset))
        win.blit(click_prompt, prompt_rect)

        settings_button.draw(win)
        exit_button.draw(win)

        # Display the high score in the top right corner
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        win.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if settings_button.check_click(mouse_pos):
                        settings_menu()
                    elif exit_button.check_click(mouse_pos):
                        exit_confirmation()
                    else:
                        story_intro(game)  # Start the story intro

        # Check for hover states
        mouse_pos = pygame.mouse.get_pos()
        settings_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

# Exit confirmation function
def exit_confirmation():
    while True:
        win.fill(DARK_GRAY)

        # Draw slightly transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Allow transparency
        overlay.fill(TRANSPARENT_COLOR)
        win.blit(overlay, (0, 0))

        # Confirmation text
        confirm_text = font.render("Are you sure you want to exit?", True, WHITE)
        confirm_rect = confirm_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        win.blit(confirm_text, confirm_rect)

        # Create buttons with distance from center
        yes_button = Button("Yes", WIDTH // 2 - 210, HEIGHT // 2 + 20)
        no_button = Button("No", WIDTH // 2 + 10, HEIGHT // 2 + 20)

        # Draw buttons
        yes_button.draw(win)
        no_button.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                elif no_button.check_click(pygame.mouse.get_pos()):
                    return  # Go back to main menu

        # Check for hover states
        mouse_pos = pygame.mouse.get_pos()
        yes_button.check_hover(mouse_pos)
        no_button.check_hover(mouse_pos)

        pygame.display.update()


# Settings window function
def settings_menu():
    global fullscreen, volume, resolution

    settings_win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Settings")

    # Define buttons
    how_to_button = Button("How to Play", 300, 100)  # How-to/Tutorial button
    volume_button = Button(f"Volume: {volume}%", 300, 200)  # Volume control
    resolution_button = Button(f"Resolution: {resolution[0]}x{resolution[1]}", 300, 300)  # Resolution control
    fullscreen_button = Button(f"Fullscreen: {'On' if fullscreen else 'Off'}", 300, 400)  # Fullscreen toggle
    back_button = Button("Back", 300, 500)  # Back button

    while True:
        settings_win.fill((40, 40, 40))

        # Draw the "Settings" title at the top
        settings_title = font.render("Settings", True, WHITE)
        settings_title_rect = settings_title.get_rect(center=(400, 50))
        settings_win.blit(settings_title, settings_title_rect)

        # Draw all buttons
        how_to_button.draw(settings_win)
        volume_button.draw(settings_win)
        resolution_button.draw(settings_win)
        fullscreen_button.draw(settings_win)
        back_button.draw(settings_win)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Go to how-to page when clicked
                if how_to_button.check_click(mouse_pos):
                    how_to_play()  # Function that shows how to play

                # Change volume when clicked
                if volume_button.check_click(mouse_pos):
                    volume_index = (VOLUME_LEVELS.index(volume) + 1) % len(VOLUME_LEVELS)
                    volume = VOLUME_LEVELS[volume_index]
                    volume_button.text = f"Volume: {volume}%"

                # Change resolution when clicked
                if resolution_button.check_click(mouse_pos):
                    resolution_index = (RESOLUTIONS.index(resolution) + 1) % len(RESOLUTIONS)
                    resolution = RESOLUTIONS[resolution_index]
                    resolution_button.text = f"Resolution: {resolution[0]}x{resolution[1]}"
                    pygame.display.set_mode(resolution)

                # Toggle fullscreen
                if fullscreen_button.check_click(mouse_pos):
                    fullscreen = not fullscreen
                    fullscreen_button.text = f"Fullscreen: {'On' if fullscreen else 'Off'}"
                    if fullscreen:
                        pygame.display.set_mode(resolution, pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode(resolution)

                # Go back to main menu
                if back_button.check_click(mouse_pos):
                    return  # Go back to main menu

        # Check for hover states
        mouse_pos = pygame.mouse.get_pos()
        how_to_button.check_hover(mouse_pos)
        volume_button.check_hover(mouse_pos)
        resolution_button.check_hover(mouse_pos)
        fullscreen_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        pygame.display.update()



# How-to/Tutorial page function
def how_to_play():
    tutorial_win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("How to Play")

    back_button = Button("Back", 300, 500)  # Back button

    while True:
        tutorial_win.fill((40, 40, 40))

        # Display how-to text (example tutorial content)
        tutorial_text = [
            "How to Play:",
            "1. Move using the arrow keys.",
            "2. Shoot with the spacebar.",
            "3. Avoid obstacles and defeat enemies.",
            "4. Press ESC to return to the main menu."
        ]

        # Render the tutorial text on the window
        for i, line in enumerate(tutorial_text):
            text_surface = font.render(line, True, WHITE)
            tutorial_win.blit(text_surface, (50, 50 + i * 40))  # Adjust y-position

        # Draw back button
        back_button.draw(tutorial_win)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.check_click(mouse_pos):
                    return  # Go back to settings menu

        # Check hover states for back button
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)

        pygame.display.update()

# Story intro function
def story_intro(game):
    # Sample story text 
    # global fullscreen, resolution

    # if fullscreen:
    #     pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    # else:
    #     pygame.display.set_mode(resolution)
    pygame.display.set_mode((800,600))
    story_text = [
        "In a galaxy far, far away...",
        "",
        "You find yourself the"
        "last clone standing on an outpost",
        "",
        "Republican reinforcements are on the way, but the seperatists",
        "have located your position and are closing in"
        "intent on wiping you out.",
        ""
        "With your blaster at the ready",
        "you prepare yourself to fend off the incoming droids.",
        "",
        "Each moment counts as you waits for reinforcements.",
        "",
        "",
        "May the Force be with you..."
    ]

    win.fill(DARK_GRAY)

    # Display each line of text with spacing
    for i, line in enumerate(story_text):
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(800 // 2, 600 // 2 - (len(story_text) // 2 - i) * 30))
        win.blit(text_surface, text_rect)

    # Hovering text prompt to continue
    hover_time_passed = pygame.time.get_ticks() / 1000  # Time in seconds
    hover_y_offset = math.sin(hover_time_passed * 2) * 5  # Up and down animation
    continue_play_prompt = font.render("Press Anywhere to Continue", True, WHITE)
    continue_play_rect = continue_play_prompt.get_rect(center=(800// 2, 600// 2 + 250  + hover_y_offset))
    win.blit(continue_play_prompt, continue_play_rect)

    pygame.display.update()

    while True:  # Wait for user to continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game()  # Return to the main menu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(game)  # Go back to the main menu when Escape is pressed

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

# Start the main menu
if __name__ == "__main__":
    main_menu()



