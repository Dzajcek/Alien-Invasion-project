import sys
import os
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from arrow import Arrow
from toogle import Toggle


class AlienInvasion:
# Ogólna klasa przeznaczona do zarzadzania zasobami i sposobem dzialania gry.

    def __init__(self):
        # Inicjalizacja gry i utworzenie jej zasasobow.
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Załadowanie dźwięku wystrzału
        current_path = os.path.dirname(__file__)
        sound_path = os.path.join(current_path, 'sounds', 'shoot.wav')
        self.shoot_sound = pygame.mixer.Sound(sound_path)
        # Możesz ustawić głośność (od 0.0 do 1.0)
        self.shoot_sound.set_volume(0.2)
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Utworzenie egzemplarza przechowujacego dane statystyczne dotyczace gry.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.arrow = Arrow(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Uruchomienie gry "Alien Invasion" w stanie aktywnym
        self.game_active = False

        # Utworzenie przyciskow
        self._create_buttons()
        self.is_difficult_button_click = False

        # Umieszczenie w prawym dolnym rogu
        self.hitbox_toggle = Toggle(self, "Hitbox", 1000, 700)
        self.fps_toggle = Toggle(self, "FPS", 1000, 740)
        

    def run_game(self):
        # Rozpoczecie petli glownej gry.
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(180)
            
    def _check_events(self):
        # Reakcja na zdarzenia generowane przez klawiature i mysz.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_difficult_button(mouse_pos)
                self._check_toggles(mouse_pos)

    def _check_difficult_button(self, mouse_pos):
        if not self.game_active:
            # Sprawdzamy każdy przycisk po kolei
            if self.level_easy_button.rect.collidepoint(mouse_pos):
                self.settings.difficult_level("easy")
                self.is_difficult_button_click = True
                self.arrow.move_to_button(self.level_easy_button.rect)
                
            elif self.level_normal_button.rect.collidepoint(mouse_pos):
                self.settings.difficult_level("normal")
                self.is_difficult_button_click = True
                self.arrow.move_to_button(self.level_normal_button.rect)
                
            elif self.level_hard_button.rect.collidepoint(mouse_pos):
                self.settings.difficult_level("hard")
                self.is_difficult_button_click = True
                self.arrow.move_to_button(self.level_hard_button.rect)

            elif self.level_extreme_button.rect.collidepoint(mouse_pos): 
                self.settings.difficult_level("extreme")
                self.is_difficult_button_click = True
                self.arrow.move_to_button(self.level_extreme_button.rect)

            elif self.level_impossible_button.rect.collidepoint(mouse_pos): 
                self.settings.difficult_level("impossible")
                self.is_difficult_button_click = True
                self.arrow.move_to_button(self.level_impossible_button.rect)

            if self.is_difficult_button_click and self.start_button.rect.collidepoint(mouse_pos):
                self._start_game()
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
                
    def _check_toggles(self, mouse_pos):
        if not self.game_active:
            if self.hitbox_toggle.rect.collidepoint(mouse_pos):
                self.settings.show_hitboxes = not self.settings.show_hitboxes
            if self.fps_toggle.rect.collidepoint(mouse_pos):
                self.settings.show_fps = not self.settings.show_fps    
        
    def _start_game(self):
            self.is_difficult_button_click = False
            # Przywrocenie domyslnej predkosci gry
            self.settings.initialize_dynamic_settings()

            # Wyzerowanie danych statystycznych gry.
            self.stats.reset_stats()
            self.game_active = True

            # Usuniecie zawartosci list bullets i aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Utworzenie nowej floty i wysrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            # Ukrycie kursora myszy.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        # Reakcja na nacisniecie klawisza.
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        # Reakcja na zwolnienie klawisza.
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # Utworzenie nowego pocisku i dodanie go do grupy pociskow.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            self.shoot_sound.play()

    def _update_bullets(self):
        # Uaktualnienie polozenia pociskow i usuniecie tych niewidocznych na ekranie.

        # Uaktualnienie polozenia pociskow
        self.bullets.update()

        # Usuniecie pociskow, ktore znajduja sie poza ekranem.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Reakcja na kolizje miedzy pociskiem i obcym.

        # Usuniecie wszystkich pociskow i obcych, miedzy ktorymi doszlo do kolizji.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #Pozbycie sie istniejacych pociskow i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Inkrementacja numeru poziomu.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        # Reakcja na uderzenie obcego w statek.

        if self.stats.ships_left > 1:

            # Zmniejszenie wartosci przechowywanej w ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Usuniecie zawartosci list bullets i aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Utworzenie nowej floty i wysrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            # Pauza.
            sleep(0.5)
        else:
            self.stats.ships_left = 0
            self.sb.prep_ships()

            self.aliens.empty()
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        # Sprawdzenie, czy ktorykolwiek obcy dotarl do dolnej krawedzi ekranu.
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Tak samo jak w przypadku zderzenia statku z obcym.
                self._ship_hit()
                break

    def _update_aliens(self):
        # Sprawdzenie, czy floata obcych znajduje sie przy krawedzi, a nastepnie uaktualnienie polozenia wszystkich obcych we flocie.

        self._check_fleet_edges()
        self.aliens.update()

        # Wykrywanie kolizji miedzy obcym i statkiem.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Wyszukiwanie obcych docierajacych do dolnej krawedzi ekranu.
        self._check_aliens_bottom()

    def _create_fleet(self):
        # Utworzenie pełnej floty obcych.

        # Utworzenie obcego i dodawanie kolejnych obcych, ktorzy zmieszcza sie w rzedzie.
        # Odleglosc miedzy poszczegolnymi obcymi jest rowna szerokosci obcego.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height + 25
        while current_y < (self.settings.screen_height - 7 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Ukonczenie rzedu, wyzerowanie wartosci x oraz inkrementacja wartosci y.
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _create_alien(self, x_position, y_position):
        # Utworzenie obcego i umieszczenie go w rzedzie.
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        # Odpowiednia reakcja, gdy obcy dotrze do krawedzi ekranu.
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Przesuniecie calej floty w dol i zmiana kierunku, w ktorym sie ona porusza.
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_buttons(self):
        self.start_button = Button(self, "Start", 500, 650, (0, 180, 50), 55)
        self.game_over_button = Button(self, "Game over!", 500, 200, (255, 0, 0), 65)
        self.choose_level_button = Button(self, "Select level:", 500, 450, (0, 0, 0))
        self.level_easy_button = Button(self, "Easy", 20, 500)
        self.level_normal_button = Button(self, "Normal", 260, 500)
        self.level_hard_button = Button(self, "Hard", 500, 500)
        self.level_extreme_button = Button(self, "Extreme", 740, 500)
        self.level_impossible_button = Button(self, "Impossible", 980, 500)

    def _draw_buttons(self):
        self.level_easy_button.draw_button(button_color=(0, 120, 220))
        self.level_normal_button.draw_button()
        self.level_hard_button.draw_button(button_color=(220, 180, 0))
        self.level_extreme_button.draw_button(button_color=(155, 0, 0))
        self.level_impossible_button.draw_button(button_color=(0, 0, 0))
        self.choose_level_button.draw_button(background=False)

        if self.is_difficult_button_click:
            self.start_button.draw_button(background=False)
            self.arrow.blitme()

        if self.stats.ships_left == 0: 
            self.game_over_button.draw_button(background=False)
    
    def _update_screen(self):
        # Uaktualnianie obrazów na ekranie i wyswietlenie tego ekranu.
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        # Wyswietlenie przycsiku tylko wtedy, gdy gra jest nieaktywna
        if not self.game_active:
            self._draw_buttons()
            self.hitbox_toggle.draw(self.settings.show_hitboxes)
            self.fps_toggle.draw(self.settings.show_fps)

        # Wyświetlanie FPS w rogu podczas gry
        if self.settings.show_fps:
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            fps_image = self.sb.font.render(fps_text, True, (0, 255, 0))
            self.screen.blit(fps_image, (10, 770))

        # Wyświetlanie hitboxów (według wcześniejszego pomysłu)
        if self.settings.show_hitboxes:
            pygame.draw.rect(self.screen, (255, 0, 0), self.ship.rect, 1)
            for alien in self.aliens.sprites():
                pygame.draw.rect(self.screen, (0, 0, 255), alien.rect, 1)

        pygame.display.flip()
    
if __name__ == "__main__":
    # Utworzenie egzemplarza gry i jej uruchomienie. 
    ai = AlienInvasion()
    ai.run_game()