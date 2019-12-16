import pygame

#constants for color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#screen size constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class Bullet(pygame.sprite.Sprite):
    """This class represents the bullets"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ammunition.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5


class Missile(pygame.sprite.Sprite):
    def __init__(self, speed_x, speed_y, level):
        super().__init__()
        self.levels = {1: 'missile1.png', 2: 'missile2.png', 3: 'missile3.png'}
        self.image = pygame.image.load(self.levels[level]).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Enemy(pygame.sprite.Sprite):
    """This class represents the enemy."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy_sprite.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 75
        self.speed_x = 4
        self.health = 10
        self.enemy_alive = True

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x >= 660:
            self.speed_x *= -1
        if self.rect.x <= 0:
            self.speed_x *= -1

    def health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, 40, 10))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 20, (4 * self.health), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 1
        if not(self.health > 0):
            self.enemy_alive = False
        print('hit')


class Enemy2(pygame.sprite.Sprite):
    """This class represents the enemy."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy2_sprite.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 75
        self.speed_x = 3
        self.health = 15
        self.enemy_alive = True

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x >= 660:
            self.speed_x *= -1
        if self.rect.x <= 0:
            self.speed_x *= -1

    def health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, 40, 10))
        pygame.draw.rect(screen, BLUE, (self.rect.x, self.rect.y - 20, ((2+(2/3)) * self.health), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 1
        if not(self.health > 0):
            self.enemy_alive = False
        print('hit')


class Enemy3(pygame.sprite.Sprite):
    """This class represents the enemy."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy3_sprite.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 75
        self.speed_x = 5
        self.health = 15
        self.enemy_alive = True

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x >= 660:
            self.speed_x *= -1
        if self.rect.x <= 0:
            self.speed_x *= -1

    def health_bar(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, 46, 10))
        pygame.draw.rect(screen, BLUE, (self.rect.x, self.rect.y - 20, ((3+(1/15)) * self.health), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 1
        if not(self.health > 0):
            self.enemy_alive = False
        print('hit')


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface([30, 30])
        #self.image.fill(BLUE)
        self.image = pygame.image.load("player_sprite.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.rect.x = 335
        self.rect.y = 400
        self.health = 10
        self.player_alive = True

    def speed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Update the player location. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - 50:
            self.rect.x = SCREEN_WIDTH - 50
        if self.rect.y <= SCREEN_HEIGHT * 0.4:
            self.rect.y = SCREEN_HEIGHT * 0.4
        if self.rect.y > SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50

    def p_health(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, 50, 10))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 20, (5 * self.health), 10))

    def player_hit(self):
        if self.health > 0:
            self.health -= 1
            print(self.health)
        if not (self.health > 0):
            self.player_alive = False


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self, level):
        """ Constructor. Create all our attributes and initialize
        the game. """
        self.game_over = False
        self.clock = pygame.time.Clock()
        # Create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.missile_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.level = level
        # background image
        if level == 1:
            self.background_image = pygame.image.load("sky_background.png").convert()
        elif level == 2:
            self.background_image = pygame.image.load("galaxy_background.png").convert()
        elif level == 3:
            self.background_image = pygame.image.load("space_background.png").convert()
        else:
            self.background_image = pygame.image.load("ammunition.png").convert()
        # sound
        self.click_sound = pygame.mixer.Sound('laser4.wav')

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)
        self.player_list.add(self.player)

        # Create the enemy
        if level == 1:
            self.enemy = Enemy()
            self.all_sprites_list.add(self.enemy)
            self.enemy_list.add(self.enemy)
        elif level == 2:
            self.enemy = Enemy2()
            self.all_sprites_list.add(self.enemy)
            self.enemy_list.add(self.enemy)
        elif level == 3:
            self.enemy = Enemy3()
            self.all_sprites_list.add(self.enemy)
            self.enemy_list.add(self.enemy)

        self.dt = 0
        self.missile_timer = .5

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over and self.level == 1:
                    self.__init__(2)
                if self.game_over and self.level == 2:
                    self.__init__(3)
                if self.game_over and self.level == 3:
                    self.__init__(1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        #self.click_sound.play()
                        bullet = Bullet()
                        bullet.rect.x = self.player.rect.x + 22.5
                        bullet.rect.y = self.player.rect.y
                        self.all_sprites_list.add(bullet)
                        self.bullet_list.add(bullet)
                if event.key == pygame.K_LEFT:
                    self.player.speed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    self.player.speed(5, 0)
                if event.key == pygame.K_UP:
                    self.player.speed(0, -5)
                if event.key == pygame.K_DOWN:
                    self.player.speed(0, 5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.speed(5, 0)
                if event.key == pygame.K_RIGHT:
                    self.player.speed(-5, 0)
                if event.key == pygame.K_UP:
                    self.player.speed(0, 5)
                if event.key == pygame.K_DOWN:
                    self.player.speed(0, -5)

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()

        for bullet in self.bullet_list:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, self.enemy_list, False)
            for enemy_hit in enemy_hit_list:
                self.enemy.hit()
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
            if self.enemy.health == 0:
                self.game_over = True
                self.all_sprites_list.remove(self.enemy)
                self.enemy_list.remove(self.enemy)
            if bullet.rect.y < -10:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

        self.dt = self.clock.tick(60)/1000
        self.missile_timer -= self.dt
        if self.enemy.enemy_alive:
            if self.missile_timer <= 0:
                if self.level == 1:
                    self.missile_timer = 1
                    missile = Missile(0, 4, self.level)
                    missile.rect.x = self.enemy.rect.x + 17
                    missile.rect.y = self.enemy.rect.y + 40
                    self.all_sprites_list.add(missile)
                    self.missile_list.add(missile)
                if self.level == 2:
                    self.missile_timer = 0.5
                    missile = Missile(1, 5, self.level)
                    missile.rect.x = self.enemy.rect.x + 16
                    missile.rect.y = self.enemy.rect.y + 40
                    missile2 = Missile(-1, 5, self.level)
                    missile2.rect.x = self.enemy.rect.x + 22
                    missile2.rect.y = self.enemy.rect.y + 40
                    self.all_sprites_list.add(missile, missile2)
                    self.missile_list.add(missile, missile2)
                if self.level == 3:
                    self.missile_timer = 0.5
                    missile = Missile(1, 5, self.level)
                    missile.rect.x = self.enemy.rect.x + 14
                    missile.rect.y = self.enemy.rect.y + 75
                    missile2 = Missile(-1, 5, self.level)
                    missile2.rect.x = self.enemy.rect.x + 23
                    missile2.rect.y = self.enemy.rect.y + 75
                    missile3 = Missile(0, 5, self.level)
                    missile3.rect.x = self.enemy.rect.x + 14
                    missile3.rect.y = self.enemy.rect.y + 75
                    self.all_sprites_list.add(missile, missile2, missile3)
                    self.missile_list.add(missile, missile2, missile3)

            for missile in self.missile_list:
                player_hit_list = pygame.sprite.spritecollide(missile, self.player_list, False)
                for player_hit in player_hit_list:
                    self.player.player_hit()
                    self.missile_list.remove(missile)
                    self.all_sprites_list.remove(missile)
                if self.player.health == 0:
                    self.player_list.remove(self.player)
                    self.all_sprites_list.remove(self.player)
                if missile.rect.x < 0 or missile.rect.x > SCREEN_WIDTH:
                    self.missile_list.remove(missile)
                    self.all_sprites_list.remove(missile)
                if missile.rect.y > SCREEN_HEIGHT + 10:
                    self.missile_list.remove(missile)
                    self.all_sprites_list.remove(missile)

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        if self.game_over and self.level in [1, 2, 3]:
            font = pygame.font.SysFont("serif", 30)
            if self.level == 1:
                text = font.render("You're pretty good. Click to enter space.", True, BLACK)
            elif self.level == 2:
                text = font.render("I guess you're ready for It. Click now.", True, RED)
            else:
                text = font.render("Mission complete. Click the X to exit...or click to restart.", True, BLACK)

            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            screen.blit(self.background_image, [0, 0])
            #screen.blit(self.player_image, [self.player.rect.x, self.player.rect.y])
            self.all_sprites_list.draw(screen)
            if self.enemy.enemy_alive:
                self.enemy.health_bar(screen)
            if self.player.player_alive:
                self.player.p_health(screen)

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My First Game")
    pygame.mouse.set_visible(False)

    done = False
    level = 1
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game(level)

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
