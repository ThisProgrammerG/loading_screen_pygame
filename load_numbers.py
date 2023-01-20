# Python 3.11

import itertools
import threading
from collections import deque
import time

import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 500, 250
FONT_SIZE = 24
WIDTH_OFFSET = 50

def load_images(data, container):
    start_time = time.time()
    try:
        while True:
            container.append(next(data))
    except StopIteration:
        print(f'Thread finished: {time.time() - start_time:.2f} seconds.')

def main():
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont('Consolas', FONT_SIZE)

    loading_messages = itertools.cycle([font.render(f'Loading{"." * (i + 1)}', True, 'pink') for i in range(5)])
    image_index = 0
    done_message = font.render('Done.', True, 'Green')
    counter_text = font.render('0', True, 'orange')
    loading_message = next(loading_messages)

    your_data = iter(range(50_000_000)) 

    counter_deque = deque()

    # Daemon threads will shut down with the main thread.
    loading_thread = threading.Thread(
            target=load_images,
            args=(your_data, counter_deque),
            daemon=True
    )

    loading_thread.start()

    while running:
        clock.tick(60)  # Frame-rate will not bottleneck loading. Try with different fps.
        screen.fill('black')

        if loading_thread.is_alive():  # Thread is running
            if image_index % 10 == 0:
                loading_message = next(loading_messages)

            if counter_deque:
                counter_text = font.render(f'{counter_deque[-1]:,}', True, 'orange')

            screen.blit(loading_message, (WIDTH // 2 - WIDTH_OFFSET, HEIGHT // 2))
            screen.blit(counter_text, (WIDTH // 2 - WIDTH_OFFSET, HEIGHT // 2 - FONT_SIZE))
            image_index += 1
        else:
            screen.blit(done_message, (WIDTH // 2 - WIDTH_OFFSET, HEIGHT // 2))


        pygame.display.flip()

        running = not any(filter(lambda event: event.type == pygame.QUIT, pygame.event.get()))

    pygame.quit()

if __name__ == '__main__':
    main()
