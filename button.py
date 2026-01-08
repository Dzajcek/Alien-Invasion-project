import pygame.font
import os

class Button:
    # Klasa przeznaczona do tworzenia przyciskow dla gry.

    def __init__(self, ai_game, msg, position_x="center", position_y="center", text_color=(255, 255, 255), font=48):
        # Inicjalizacja atrybutow przycisku.
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Zdefiniowanie wymiarow i wlasciwosci przycisku.
        self.width, self.height = 200, 50
        current_path = os.path.dirname(__file__)
        font_path = os.path.join(current_path, 'fonts', 'retro.ttf')
        self.font = pygame.font.Font(font_path, 20)

        
        # Utworzenie prostokata przycisku i ustawienie jego wspolrzednych.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        if position_x == "center" and position_y == "center":
            self.rect.center = self.screen_rect.center
        else:
            self.rect.x = int(position_x)
            self.rect.y = int(position_y)
        

        # Komunikat wyswietlany przez przycisk trzeba przygotowac jednokrotnie.
        self._prep_msg(msg, text_color, self.font)

    def _prep_msg(self, msg, text_color, font):
        # Umieszczenie komunikatu w wygenerowanym obrazie i wysrodkowanie tekstu na przycisku.
        self.msg_image = self.font.render(msg, True, text_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, background=True, button_color=(0, 135, 0)):
        # Wyswietlenie pustego przycisku, a nastepnie komunikatu na nim.
        if background:
            self.screen.fill(button_color, self.rect)

        self.screen.blit(self.msg_image, self.msg_image_rect)