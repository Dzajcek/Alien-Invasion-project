import pygame
import os

class Toggle:
    def __init__(self, ai_game, msg, x, y):
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        current_path = os.path.dirname(__file__)
        font_path = os.path.join(current_path, 'fonts', 'retro.ttf')
        self.font = pygame.font.Font(font_path, 20)
        
        self.msg = msg
        self.rect = pygame.Rect(x, y, 20, 20) # Kwadracik checkboxa
        
    def draw(self, is_on):
        # Rysowanie tekstu
        msg_image = self.font.render(self.msg, True, (30, 30, 30))
        msg_rect = msg_image.get_rect()
        msg_rect.left = self.rect.right + 10
        msg_rect.centery = self.rect.centery
        self.screen.blit(msg_image, msg_rect)
        
        # Rysowanie ramki checkboxa
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        if is_on:
            # Wypełnienie środka jeśli włączone
            internal_rect = self.rect.inflate(-8, -8)
            pygame.draw.rect(self.screen, (0, 200, 0), internal_rect)