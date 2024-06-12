import pygame
import math
from utils import scale_image, blit_rotate_center
import time

def run():
    # Initialize Pygame
    pygame.init()

    # Load images and scale them
    TRACK = scale_image(pygame.image.load("Project/track_1.png"), 1)
    RED_CAR = scale_image(pygame.image.load("Project/red_car2.png"), 0.15)
    GREEN_CAR = scale_image(pygame.image.load("Project/green_car1.png"), 0.15)
    PINK_CAR = scale_image(pygame.image.load("Project/pink_car2.png"), 0.15)  # New car image
    YELLOW_CAR = scale_image(pygame.image.load("Project/yellow_car2.webp"), 0.15)  # New car image

    # Set up display
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zoomers!")

    # Frame rate
    FPS = 60

    # Finish line position
    FINISH_LINE_X = WIDTH - 100  # Adjust this as needed

    class AbstractCar:
        def __init__(self, img, max_vel, start_pos):
            self.img = img
            self.max_vel = max_vel
            self.vel = 0
            self.x, self.y = start_pos
            self.acceleration = 0.1

        def draw(self, win):
            blit_rotate_center(win, self.img, (self.x, self.y), 0)  # No rotation, angle is 0

        def move(self):
            self.x += self.vel

        def move_right(self):
            self.vel = self.max_vel
            self.move()

        def stop(self):
            self.vel = 0

        def check_finish(self):
            return self.x >= FINISH_LINE_X

    def draw(win, images, cars, winner, countdown, go_displayed):
        for img, pos in images:
            win.blit(img, pos)

        for car in cars:
            car.draw(win)

        if countdown > 0:
            font = pygame.font.SysFont("comicsans", 100)
            text = font.render(str(countdown), True, (255, 255, 255))
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        elif not go_displayed:
            font = pygame.font.SysFont("comicsans", 100)
            text = font.render("GO!", True, (255, 255, 255))
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        elif winner:
            font = pygame.font.SysFont("comicsans", 100)
            text = font.render(f"{winner} Wins!", True, (255, 255, 255))
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

        pygame.display.update()

    # Car start positions
    START_POSITIONS = [(8, 190), (-12, 270), (8, 110), (8, 30)]

    # AI car speeds for each level
    LEVEL_AI_SPEEDS = [
        (3, 2, 2.5),  # Speeds for level 1
        (3.5, 2.5, 3),  # Speeds for level 2
        (4, 3, 3.5)   # Speeds for level 3
    ]

    PLAYER_SPEED = 4  # Consistent player speed across levels

    def create_cars(level):
        speeds = LEVEL_AI_SPEEDS[level]
        return [
            AbstractCar(RED_CAR, PLAYER_SPEED, START_POSITIONS[0]),  # Player's car
            AbstractCar(GREEN_CAR, speeds[0], START_POSITIONS[1]),
            AbstractCar(PINK_CAR, speeds[1], START_POSITIONS[2]),
            AbstractCar(YELLOW_CAR, speeds[2], START_POSITIONS[3])
        ]

    # Game loop to handle multiple levels
    def main():
        run = True
        clock = pygame.time.Clock()
        images = [(TRACK, (0, 0))]
        level = 0
        winner = None
        countdown = 3  # Countdown from 3 seconds
        go_displayed = False
        player_won = False

        while run and level < 3:
            cars = create_cars(level)
            start_ticks = pygame.time.get_ticks()  # Starting time for countdown
            countdown = 3
            go_displayed = False
            winner = None

            while run and not winner:
                clock.tick(FPS)

                # Calculate the countdown
                seconds = (pygame.time.get_ticks() - start_ticks) // 1000
                if seconds > 3:
                    countdown = 0
                    if seconds == 4:
                        go_displayed = True
                else:
                    countdown = 3 - seconds

                draw(WIN, images, cars, winner, countdown, go_displayed)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                keys = pygame.key.get_pressed()

                if go_displayed and seconds >= 4:
                    # Update player's car based on the keys
                    player_car = cars[0]
                    if keys[pygame.K_a]:
                        player_car.move_right()
                    elif keys[pygame.K_d]:
                        player_car.move_right()
                    else:
                        player_car.stop()

                    # Update AI cars
                    for car in cars[1:]:
                        car.move_right()

                    # Check if any car has crossed the finish line
                    for i, car in enumerate(cars):
                        if car.check_finish() and not winner:
                            winner = f"Car {i + 1}"
                            player_won = (i == 0)  # Check if the player won

            if player_won:
                level += 1
            else:
                run = False

        if player_won and level == 3:
            print("Congratulations! You've won all levels!")
        else:
            print("Game Over. Try again!")

        pygame.quit()

    main()
