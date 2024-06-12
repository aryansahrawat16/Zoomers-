import pygame
import math
import time

from utils import scale_image, blit_rotate_center

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
        def __init__(self, img, max_vel, start_pos, name):
            self.img = img
            self.max_vel = max_vel
            self.vel = 0
            self.x, self.y = start_pos
            self.acceleration = 0.1
            self.name = name

        def draw(self, win):
            blit_rotate_center(win, self.img, (self.x, self.y), 0)  # No rotation, angle is 0

        def move(self):
            self.x += self.vel

        def move_right(self):
            self.vel = self.max_vel
            self.move()

        def check_finish(self):
            return self.x >= FINISH_LINE_X

    def draw(win, images, cars, winner):
        for img, pos in images:
            win.blit(img, pos)

        for car in cars:
            car.draw(win)

        if winner:
            font = pygame.font.SysFont("comicsans", 100)
            text = font.render(f"{winner} Wins!", True, (255, 255, 255))
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

        pygame.display.update()

    # Car start positions and names
    START_POSITIONS = [(8, 190), (-12, 270), (8, 110), (8, 30)]
    CAR_NAMES = ["Red Car", "Green Car", "Pink Car", "Yellow Car"]

    run = True
    clock = pygame.time.Clock()
    images = [(TRACK, (0, 0))]
    cars = [
        AbstractCar(RED_CAR, 4, START_POSITIONS[0], CAR_NAMES[0]),
        AbstractCar(GREEN_CAR, 4, START_POSITIONS[1], CAR_NAMES[1]),
        AbstractCar(PINK_CAR, 4, START_POSITIONS[2], CAR_NAMES[2]),
        AbstractCar(YELLOW_CAR, 4, START_POSITIONS[3], CAR_NAMES[3])
    ]

    # Assign keys for each car
    car_keys = [
        (pygame.K_q, pygame.K_w),
        (pygame.K_z, pygame.K_x),
        (pygame.K_o, pygame.K_p),
        (pygame.K_n, pygame.K_m)
    ]

    # Track the last key pressed for each car
    last_keys = [None] * len(cars)

    winner = None
    win_time = None  # Variable to track the time when a player wins

    while run:
        clock.tick(FPS)

        draw(WIN, images, cars, winner)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        # Update each car based on their respective keys
        for i, car in enumerate(cars):
            if keys[car_keys[i][0]] and last_keys[i] != car_keys[i][0]:
                car.move_right()
                last_keys[i] = car_keys[i][0]
            elif keys[car_keys[i][1]] and last_keys[i] != car_keys[i][1]:
                car.move_right()
                last_keys[i] = car_keys[i][1]
            else:
                car.vel = 0  # Stop moving when no key is pressed or the same key is pressed consecutively

            # Check if car has crossed the finish line
            if car.check_finish() and not winner:
                winner = car.name  # Assign the name of the winning car
                win_time = time.time()  # Record the time when a player wins

        # If a winner is declared and 10 seconds have passed, quit the game
        if winner and time.time() - win_time >= 10:
            run = False

    pygame.quit()
