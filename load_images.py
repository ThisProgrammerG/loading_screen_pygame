# Python 3.11

import itertools
import threading
from queue import Queue
import time
import random

import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 1500, 950
FONT_SIZE = 24
WIDTH_OFFSET = 50
TOTAL_IMAGES = 10
IMAGE_TIMER = pygame.event.custom_type()

def get_center(width, height, other_width, other_height):
    x = width // 2 - other_width // 2
    y = height // 2 - other_height // 2

    return x, y

def load_images(container, amount):
    start_time = time.time()
    for _ in range(amount):
        image = pygame.Surface((700, 850))
        image.fill(random.sample(range(256), 3))
        container.put(image)

    print(f'Thread finished: {time.time() - start_time:.2f} seconds.')

def main():
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

    # Only hold max 3 images(or however many that makes sense) to save on memory usage
    image_queue = Queue(maxsize=3)

    # Daemon threads will shut down with the main thread.
    loading_thread = threading.Thread(
            target=load_images,
            args=(image_queue, TOTAL_IMAGES),
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
            elif event.type == IMAGE_TIMER and not image_queue.empty():  # Use empty() and not not_empty
                image = image_queue.get_nowait()  # get is blocking(hangs) if it somehow reaches here

    pygame.quit()

if __name__ == '__main__':
    main()
