import pygame
import os

class Arrow:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # Wczytanie obrazu
        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'images', 'arrow.bmp')
        self.image = pygame.image.load(image_path)
        
        self.rect = self.image.get_rect()
        # Na początku schowana (np. pod ekranem)
        self.rect.y = 2000 

    def move_to_button(self, button_rect):
        # Ustawia strzałkę pod środkiem klikniętego przycisku.
        self.rect.midtop = button_rect.midbottom
        self.rect.y += 10  # Mały odstęp od dołu przycisku

    def blitme(self):
        self.screen.blit(self.image, self.rect)