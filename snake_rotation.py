import pygame


def snake_direction(event, snake, tile_size):
    if len(snake.body) > 1:
        if event.key == pygame.K_UP and snake.direction not in ["up", 'down']:
            if snake.head.y - tile_size != snake.body[1].y:
                snake.direction = 'up'
        elif event.key == pygame.K_DOWN and snake.direction not in ["up", 'down']:
            if snake.head.y + tile_size != snake.body[1].y:
                snake.direction = 'down'
        elif event.key == pygame.K_LEFT and snake.direction not in ["left", 'right']:
            if snake.head.x - tile_size != snake.body[1].x:
                snake.direction = 'left'
        elif event.key == pygame.K_RIGHT and snake.direction not in ["left", 'right']:
            if snake.head.x + tile_size != snake.body[1].x:
                snake.direction = 'right'
    else:
        if event.key == pygame.K_UP and snake.direction not in ["up", 'down']:
            snake.direction = "up"
        elif event.key == pygame.K_DOWN and snake.direction not in ["up", 'down']:
            snake.direction = "down"
        elif event.key == pygame.K_LEFT and snake.direction not in ["left", 'right']:
            snake.direction = "left"
        elif event.key == pygame.K_RIGHT and snake.direction not in ["left", 'right']:
            snake.direction = "right"


def head_orientation(snake):
    if snake.direction == "left":
        return 90
    elif snake.direction == "down":
        return 180
    elif snake.direction == "right":
        return 270
    else:
        return 0


def body_orientation(curr, prev):
    if prev.y < curr.y:
        return 0
    if prev.x < curr.x:
        return 90
    if prev.y > curr.y:
        return 180
    if prev.x > curr.x:
        return 270


def turn_orientation(curr, prev, previouser, coming, tile_size):
    # regular turn piece
    if ((prev.x - tile_size == curr.x or prev.x - tile_size == previouser.x) and
            (prev.y + tile_size == curr.y or prev.y + tile_size == previouser.y)):
        return 0
    if ((prev.x + tile_size == curr.x or prev.x + tile_size == previouser.x) and
            (prev.y + tile_size == curr.y or prev.y + tile_size == previouser.y)):
        return 90
    if ((prev.x + tile_size == curr.x or prev.x + tile_size == previouser.x) and
            (prev.y - tile_size == curr.y or prev.y - tile_size == previouser.y)):
        return 180
    if ((prev.x - tile_size == curr.x or prev.x - tile_size == previouser.x) and
            (prev.y - tile_size == curr.y or prev.y - tile_size == previouser.y)):
        return 270

    # fruit overlap turn piece
    if coming is not None:
        if ((prev.x - tile_size == coming.x or prev.x - tile_size == previouser.x) and
                (prev.y + tile_size == coming.y or prev.y + tile_size == previouser.y)):
            return 0
        if ((prev.x + tile_size == coming.x or prev.x + tile_size == previouser.x) and
                (prev.y + tile_size == coming.y or prev.y + tile_size == previouser.y)):
            return 90
        if ((prev.x + tile_size == coming.x or prev.x + tile_size == previouser.x) and
                (prev.y - tile_size == coming.y or prev.y - tile_size == previouser.y)):
            return 180
        if ((prev.x - tile_size == coming.x or prev.x - tile_size == previouser.x) and
                (prev.y - tile_size == coming.y or prev.y - tile_size == previouser.y)):
            return 270


def turn_on_fruit_overlap(curr, prev, previouser, coming, snake):
    if curr.x == prev.x and curr.y == prev.y and curr != snake.body[-1]:
        if previouser.x != coming.x and previouser.y != coming.y and prev != snake.body[0]:
            return True
