import pygame


class Snake:
    def __init__(self, width, height, tile_size):
        self.head = pygame.Rect(width // 2, height // 2, tile_size, tile_size)
        self.body = [self.head]
        self.color = "black"
        self.direction = "up"
        self.grow = False

    def update_position(self, tile_size, fruit):
        # changes snake direction
        self.snake_grow(fruit)

        if self.direction == "up":
            new_head = pygame.Rect(self.head.x, self.head.y - tile_size, tile_size, tile_size)
        elif self.direction == "down":
            new_head = pygame.Rect(self.head.x, self.head.y + tile_size, tile_size, tile_size)
        elif self.direction == "right":
            new_head = pygame.Rect(self.head.x + tile_size, self.head.y, tile_size, tile_size)
        elif self.direction == "left":
            new_head = pygame.Rect(self.head.x - tile_size, self.head.y, tile_size, tile_size)

        """dont think this does anything"""
        if self.grow:
            self.body.insert(0, self.head.copy())
            self.grow = False
        self.head = new_head

        # update the position of each body segment
        for i in range(len(self.body) - 1, 0, -1):
            segment = self.body[i]
            previous_segment = self.body[i - 1]
            segment.x = previous_segment.x
            segment.y = previous_segment.y

        if self.grow:
            self.body.insert(0, self.head.copy())
            self.grow = False
        else:
            self.body[0] = self.head

    def snake_grow(self, fruit):
        if self.head.colliderect(fruit):
            self.grow = True

    def collide_detect(self, width, height, tile_size):
        # Check if the snake collided with a wall
        if self.head.x < 0 or self.head.x > width - tile_size or self.head.y < 0 or self.head.y > height - tile_size:
            return True

        # # Check if the snake collided with itself
        for segment in self.body[1:]:
            if self.head.colliderect(segment):
                return True

        return False
