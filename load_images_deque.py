# Python 3.11

import itertools
import threading
from collections import deque
import time
import random
import os
from glob import iglob

import pygame


pygame.init()

SIZE = WIDTH, HEIGHT = 1500, 950
FONT_SIZE = 24
WIDTH_OFFSET = 50
IMAGE_TIMER = pygame.event.custom_type()

def get_center(width, height, other_width, other_height):
    x = width // 2 - other_width // 2
    y = height // 2 - other_height // 2

    return x, y

def load_images(container, image_paths):
    start_time = time.time()
    for image_path in iglob(rf'{image_paths}\*poster*.jpg'):
        image = pygame.image.load(image_path)
        image = pygame.transform.smoothscale(image, size=(700, 850))
        container.append(image)

    print(f'Thread finished: {time.time() - start_time:.2f} seconds.')

def main(image_paths):
    pygame.time.set_timer(IMAGE_TIMER, 1_000)

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont('Consolas', FONT_SIZE)

    loading_messages = itertools.cycle([font.render(f'Loading{"." * (i + 1)}', True, 'pink') for i in range(5)])
    message_index = 0
    done_message = font.render('Done loading.', True, 'Green')
    image = pygame.Surface((700, 850))
    loading_message = next(loading_messages)

    image_deque = deque()
    image_index = 0

    # Daemon threads will shut down with the main thread.
    loading_thread = threading.Thread(
            target=load_images,
            args=(image_deque, image_paths),
            daemon=True
    )
    loading_thread.start()

    while running:
        clock.tick(60)  # Frame-rate will not bottleneck loading. Try with different fps.
        screen.fill('black')

        if loading_thread.is_alive():  # Thread is running
            if message_index % 10 == 0:
                loading_message = next(loading_messages)
            screen.blit(loading_message, (0, HEIGHT // 2))
            message_index += 1
        else:
            screen.blit(done_message, (0, HEIGHT // 2))

        screen.blit(image, get_center(WIDTH, HEIGHT, image.get_width(), image.get_height()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == IMAGE_TIMER and image_deque:
                image = image_deque[image_index]
                image_index += 1  # TODO Needs error checking implementation

    pygame.quit()

def make_images(image_paths, total_images=10):
    if not os.path.exists(image_paths):
        os.mkdir(image_paths)

    for i in range(total_images):
        image = pygame.Surface((100, 150))
        image.fill(random.sample(range(256), 3))
        pygame.image.save(image, os.path.join(image_paths, f'poster{i}.jpg'), 'JPG')

if __name__ == '__main__':
    IMAGE_PATHS = os.path.join(os.path.dirname(__file__), 'images')
    #make_images(IMAGE_PATHS)
    main(IMAGE_PATHS)




































