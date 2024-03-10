import pygame
import random
import sys

SCREEN_SIZE = [1920, 1080]
FPS_LIMIT = 60

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

dictionary_file_name = 'dictionary.txt'
words = []

on_screen_words = {}

player_text_pos = (SCREEN_SIZE[0] // 2, 800)
score_text_pos = (100, 800)

words_movement_speed = 10

speed_up_speed = 1

def init():
    # Load words dictionary from file
    load_dictionary()
    
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_SIZE))
    pygame.display.set_caption("Words Invaders!")
    screen.fill(COLOR_WHITE)

    return screen

# Main game loop
def update(screen):
    # Initialize font
    font = pygame.font.SysFont(None, 36)

    # Set up the clock
    clock = pygame.time.Clock()

    curr_word = ''
    words_timer = 0
    speed_up_timer = 0
    score = 0

    generator_speed = 3

    while True:
        for event in pygame.event.get():
            # Handle quit
            if event.type == pygame.QUIT:
                return None
            
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key in range(32, 127): # If the player entered a letter
                    curr_word += chr(event.key)
                elif event.key == pygame.K_BACKSPACE: # If the player pressed backspace
                    curr_word = curr_word[:-1]

        words_timer += clock.get_time() / 1000
        speed_up_timer += clock.get_time() / 1000

        update_words_location()

        if words_timer >= generator_speed:
            words_timer = 0
            add_word()

        if speed_up_timer >= speed_up_speed:
            speed_up_timer = 0
            generator_speed *= 0.9

        scored = False
        to_delete = []
        for word in on_screen_words.keys():
            if word == curr_word:
                scored = True
                score += len(word)
                to_delete.append(word)
            elif on_screen_words[word][0] > SCREEN_SIZE[0]:
                score -= len(word)
                to_delete.append(word)

        for word in to_delete:
            on_screen_words.pop(word, None)
        
        if scored:
            curr_word = ''

        # Draw on screen
        screen.fill(COLOR_WHITE) # Clear screen
        draw_text(screen, curr_word, player_text_pos, font, COLOR_BLACK) # Draw player text
        draw_text(screen, "Score: " + str(score), score_text_pos, font, COLOR_BLACK) # Draw the score
        
        # Draw words
        for word in on_screen_words.keys():
            draw_text(screen, word, on_screen_words[word], font, COLOR_BLACK)    

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS_LIMIT)  # Limit to 60 frames per second

def draw_text(surface, text, pos, font, color):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

# Load words dictionary from file
def load_dictionary():
    with open(dictionary_file_name) as file:
        for line in file:
            words.append(line.rstrip().lower)

def update_words_location():
    for word in on_screen_words.keys():
        on_screen_words[word] = (on_screen_words[word][0], on_screen_words[word][1] + words_movement_speed)

# Add a word to the words on screen dictionary with horizontal location
def add_word():
    on_screen_words[choose_word()] = (random.randint(200, SCREEN_SIZE[0] - 200), 0)

def choose_word():
    new_word = words[random.randint(0, len(words) - 1)]
    while new_word in on_screen_words.keys():
        new_word = words[random.randint(0, len(words) - 1)]
    return new_word

if __name__ == '__main__':
    screen = init()
    update(screen)