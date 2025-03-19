# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from asteroid import Shot
import sys


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # Initialize pygame
    pygame.init()
    
    # Create a window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    dt = 0

    # Create the groups
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable_group, drawable_group)

    AsteroidField.containers = (updatable_group,)

    Shot.containers = (shots, updatable_group, drawable_group)
    
# Set both groups as containers for the Player
    Player.containers = (updatable_group, drawable_group)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    running = True

    

    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # When player rotates left
                    player.angle += rotation_speed
                elif event.key == pygame.K_RIGHT:
                    # When player rotates right
                    player.angle -= rotation_speed
                elif event.key == pygame.K_SPACE:
            # Player shoots when spacebar is pressed
                    try:
                        new_shot = player.shoot()
                    except Exception as e:
                        print(f"An error occurred in player.shoot(): {e}")
        # Fill screen with black
        screen.fill("black")

                    
        updatable_group.update(dt)

        for asteroid in asteroids:
            # Check if the player collides with the current asteroid
            if player.collision(asteroid):
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.rect.colliderect(bullet.rect):
                    # Collision detected! Proceed to kill both
                    asteroid.split()
                    bullet.kill()
        

         # Draw all drawable objects
        for entity in drawable_group:
            entity.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control FPS and get delta time
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
    pygame.quit()