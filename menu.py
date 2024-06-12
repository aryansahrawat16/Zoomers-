import pygame
import sys
import os
import single_player
import four_player

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((500, 499))
pygame.display.set_caption('Zoomers!')

# Load images (replace 'background.png', 'single_player_button.png', 'four_player_button.png', 'exit_button.png' with your image paths)
background_img = pygame.image.load('Project/background1.png')
single_player_button_img = pygame.image.load('Project/single_player_button.png')
four_player_button_img = pygame.image.load('Project/four_player_button.png')
exit_button_img = pygame.image.load('Project/exit_button.png')

# Set up the font
font = pygame.font.SysFont(None, 75)

# Create Button Class
class Button:
    def __init__(self, image, x, y, width, height):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Create Menu Loop
def menu_loop():
    # Create buttons
    single_player_button = Button(single_player_button_img, 150, 150, 200, 50)
    four_player_button = Button(four_player_button_img, 150, 250, 200, 50)
    exit_button = Button(exit_button_img, 150, 350, 200, 50)
    buttons = [single_player_button, four_player_button, exit_button]

    while True:
        screen.blit(background_img, (0, 0))  # Draw the background image

        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_player_button.is_hovered(mouse_pos):
                    print('Single Player Mode button clicked')
                    # Run the single_player.py file
                    single_player.run()
                elif four_player_button.is_hovered(mouse_pos):
                    print('4 Player Mode button clicked')
                    # Run the 4_player.py file
                    four_player.run()
                elif exit_button.is_hovered(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu_loop()
