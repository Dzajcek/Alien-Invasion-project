import os
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # Klasa przedstawiajaca pojedynczego obcego we flocie.

    def __init__(self, ai_game):
        # Inicjalizacja obcego i zdefiniowanie jego polozenia poczatkowego.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Wczytanie obrazu obcego i zdefiniowanie jego atrybutu rect.
        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'images', 'alien.bmp')
        self.image = pygame.image.load(image_path)
        
        self.rect = self.image.get_rect()

        # Umieszczenie nowego obcego w poblizu lewego gornego rogu ekranu.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Przechowywanie dokladnego poziomego polozenia obcego.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Zwraca wartosc True, jesli obcy znajduje sie przy krawedzi ekranu.
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        # Przesuniecie obcego w prawo lub w lewo.
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x