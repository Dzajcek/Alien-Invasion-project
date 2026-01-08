class Settings:
    # Klasa przeznaczona do przechowywania wszystkich ustawien gry.

    def __init__(self):
        # Inicjalizacja danych statycznych gry.

        # Ustawienia ekranu.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienia dotyczace statku.
        self.ship_limit = 3

        # Ustawienia dotyczace pocisku.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Ustawienia dotyczace obcego.
        self.fleet_drop_speed = 8
        
        self.initialize_dynamic_settings()


        self.show_hitboxes = False
        self.show_fps = False

    def initialize_dynamic_settings(self):
        # Initializacja ustawien, ktore ulegaja zmianie w trakcie gry.
        self.ship_speed = 0.5
        self.bullet_speed = 0.83

        # Wartosc fleet_direction wynoszaca 1 oznacza prawo, natomiast -1 oznacza lewo.
        self.fleet_direction = 1

        # Punktacja.
        self.alien_points = 50

    def difficult_level(self, difficult):
        if difficult == "easy":
            self.alien_speed = 0.53
            # Łatwa zmiana szybkosci gry.
            self.speedup_scale = 1.1
            # Łatwa zmiana liczby punktow przyznawanych za zestrzelenie obcego.
            self.score_scale = 1.2

        elif difficult == "normal":
            self.alien_speed = 0.7
            # Łatwa zmiana szybkosci gry.
            self.speedup_scale = 1.2
            # Łatwa zmiana liczby punktow przyznawanych za zestrzelenie obcego.
            self.score_scale = 1.5

        elif difficult == "hard":
            self.alien_speed = 1.03
            # Łatwa zmiana szybkosci gry.
            self.speedup_scale = 1.3
            # Łatwa zmiana liczby punktow przyznawanych za zestrzelenie obcego.
            self.score_scale = 2.0

        elif difficult == "extreme":
            self.alien_speed = 1.53
            # Łatwa zmiana szybkosci gry.
            self.speedup_scale = 1.4
            # Łatwa zmiana liczby punktow przyznawanych za zestrzelenie obcego.
            self.score_scale = 3.0

        elif difficult == "impossible":
            self.alien_speed = 2.2
            # Łatwa zmiana szybkosci gry.
            self.speedup_scale = 1.5
            # Łatwa zmiana liczby punktow przyznawanych za zestrzelenie obcego.
            self.score_scale = 5.0

    def increase_speed(self):
        # Zmiana ustawien dotyczacych szybkosci.
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)