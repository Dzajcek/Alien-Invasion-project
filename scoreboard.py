import pygame.font
import os
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    # Klasa przeznaczona do przedstawiania informacji o punktacji.

    def __init__(self, ai_game):
        # Inicjalizacja atrybutow dotyczacych  punktacji.
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Ustawienia czcionki dla informacji dotyczacych punktacji.
        self.text_color = (30, 30, 30)

        current_path = os.path.dirname(__file__)
        font_path = os.path.join(current_path, 'fonts', 'retro.ttf')
        self.font = pygame.font.Font(font_path, 20)

        # Przygotowanie poczatkowych obrazow z punktacja.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # Przeksztalcenie punktacji na wygenerowany obraz.
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(f"SCORE:{score_str}", True, self.text_color)

        # Wyswietlenie punktacji w prawym gornym rogu ekranu.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        # Konwersja najlepszego wyniku w grze na wygenerowany obraz.
        high_score = round(self.stats.high_score, - 1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(f"HIGH SCORE:{high_score_str}", True, self.text_color)

        # Wyswietlenie najlepszego wyniku w grze na srodku ekranu, przy gornej krawedzi.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        # Konwersja numeru poziomu na wygenerowany obraz.
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"wave {level_str}", True, self.text_color)

        # Numer poziomu jest wyswietlany pod aktualna punktacja
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # Wyswietla liczbe serc, jakie pozostaly graczowi.
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game, is_heart=True)
            ship.rect.x = 10 + ship_number * (10 + ship.rect.width)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        # Wyświetlenie punktacji na ekranie.
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        # Sprawdzenie, czy mamy nowy najlepszy wynik osiagniety dotad w grze.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()