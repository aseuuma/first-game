import pygame
import random
import math
# Initialize Pygame
#first try 
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MY SHOOTING GAME")

# Load and resize an image
def load_and_resize_image(image_path, width, height):
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_resize_image("fall_1.png", 50, 50)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.prev_pos = self.rect.topleft  # Store previous position of the player

    def update(self):
        keys = pygame.key.get_pressed()
        self.prev_pos = self.rect.topleft  # Update previous position before moving
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Check for collision with obstacles
        collision_obstacle = pygame.sprite.spritecollideany(self, obstacles)
        if collision_obstacle:
            # Revert to previous position to prevent moving through obstacles
            self.rect.topleft = self.prev_pos

        # Check for collision with enemy bullets
        if pygame.sprite.spritecollideany(self, enemy_bullets):
            # Game over logic or deduct health points
            pass

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        dx = target_x - x
        dy = target_y - y
        distance = max(1, abs(dx) + abs(dy))
        self.dx = dx / distance * self.speed
        self.dy = dy / distance * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_and_resize_image("w2.png", 50, 50)  # Load and resize obstacle image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Player instance
player = Player()
all_sprites.add(player)

# Create obstacles
for _ in range(10):
    obstacle = Obstacle(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 255))  # Blue color for enemy bullets
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        dx = target_x - x
        dy = target_y - y
        distance = max(1, abs(dx) + abs(dy))
        self.dx = dx / distance * self.speed
        self.dy = dy / distance * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

# Update Enemy class to handle shooting behavior
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = load_and_resize_image("fall_22.png", 30, 30)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.player = player
        self.shoot_delay = 100  # Delay between enemy shots
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # Move towards the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist != 0:
            self.rect.x += self.speed * dx / dist
            self.rect.y += self.speed * dy / dist

        # Shoot at the player
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, self.player.rect.centerx, self.player.rect.centery)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

# Create sprite group for enemy bullets
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
for _ in range(3):
    enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), player)  # Pass the player object
    enemies.add(enemy)
    all_sprites.add(enemy)
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update enemies
    for enemy in enemies:
        enemy.update()

    # Check for collisions between player and enemy bullets
    if pygame.sprite.spritecollideany(player, enemy_bullets):
        # Game over logic here
        # For example, you can end the game
        running = False

    # Update enemy bullets
    enemy_bullets.update()

    # Check for collisions between bullets and enemies
    for bullet in bullets:
        enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
        if enemy_hit:
            enemy_hit.kill()  # Remove the enemy from the group
            bullet.kill()     # Remove the bullet from the group

    all_sprites.update()

    screen.fill((255, 255, 255))  # Clear the screen
    all_sprites.draw(screen)  # Draw all sprites
    pygame.display.flip()  # Update the display

    player.update()  # Update player position

    pygame.time.Clock().tick(60)  # Limit frame rate

pygame.quit()  # Quit Pygame
