import pygame
from circleshape import CircleShape
from constants import *
from asteroid import Shot

PLAYER_SHOOT_COOLDOWN = 0.3


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.position = pygame.Vector2(x, y)
        self.angle = 0
        self.shoot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            2
        )

    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def update(self, dt):
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)  # Rotate left
        if keys[pygame.K_d]:
            self.rotate(dt)  # Rotate right

        if keys[pygame.K_w]:
            self.move(dt)   # Move forward
        if keys[pygame.K_s]:
            self.move(-dt)  # Move backward

    def shoot(self):
    # Check if player can shoot
        if self.shoot_timer <= 0:
        # Reset the timer
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        # Create a shot where the player is, passing the player's rotation
            new_shot = Shot(self.position.x, self.position.y, self.rotation)
            return new_shot
        return None  # Return None if player can't shoot