import pygame
from circleshape import CircleShape
from constants import PLAYER_SHOOT_SPEED
from constants import SHOT_RADIUS, ASTEROID_MIN_RADIUS
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)  # Default to stationary


    @property
    def rect(self):
        """
        Dynamically calculates a bounding rectangle based on the circle's position and radius.
        """
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


    def draw(self, surface):
        # Draw a circle at the asteroid's position
        pygame.draw.circle(
            surface,  # The surface to draw on
            (255, 255, 255),  # The color
            (int(self.position.x), int(self.position.y)),  # Position as a tuple of integers
            int(self.radius),  # Radius as an integer
            2  # Width of 2 for an outline
        )

    def update(self, dt):
        # Move the asteroid based on its velocity and the time elapsed
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt


    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
    
        # Generate random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
    
        # Create two new velocity vectors by rotating the current one
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)
    
        # Calculate the new radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS
    
        # Create two new asteroids - they'll be added to the containers automatically
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
    
        # Set their velocities, making them faster
        asteroid1.velocity = new_velocity1 * 1.2
        asteroid2.velocity = new_velocity2 * 1.2

        if hasattr(self.__class__, 'containers'):
            for container in self.__class__.containers:
                container.add(asteroid1)
                container.add(asteroid2)
    
        

class Shot(CircleShape):
    def __init__(self, x, y, angle):
        # Call the parent initializer
        super().__init__(x, y, SHOT_RADIUS)

        # Set the position as a Vector2 for easier math
        self.position = pygame.Vector2(x, y)

        # Create and set the velocity based on the direction and speed
        direction = pygame.Vector2(0, 1)  # Defaults to "downward" in common setups
        self.velocity = direction.rotate(angle) * PLAYER_SHOOT_SPEED

    @property
    def rect(self):
        """
        Dynamically calculates a bounding rectangle based on the circle's position and radius.
        """
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (255, 0, 0),  # A distinct color for the shot
            (int(self.position.x), int(self.position.y)),
            int(self.radius),  # Radius as an integer 
        )

    def update(self, delta_time):
        """
        Updates the shot's position based on its velocity and the time step.
        """
        self.position += self.velocity * delta_time