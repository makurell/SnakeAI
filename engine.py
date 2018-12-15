import pygame
from snake import Field, Pos

COL_BACK1 = (66,67,65)
COL_BACK2 = (59,59,58)
COL_FOOD = (242,95,92)
COL_SNAKE = (255,224,102)

class Engine:

    def __init__(self):
        self.field = Field()
        self.frame_time = 90  # amount of ms each frame is to be shown

        self.cell_width = 30

        # pygame setup
        self.screen = pygame.display.set_mode((self.cell_width*self.field.width,
                                               self.cell_width*self.field.height))
        pygame.display.set_caption('SnakeAI')

        pygame.font.init()
        self.font1 = pygame.font.SysFont('Arial',15)

    def run(self):
        while True:
            t0 = pygame.time.get_ticks()

            if not self.field.game_over:
                # game loop
                self.draw()
                self.update()
            else:
                print('game over')
                return

            pygame.display.flip()

            # wait for remaining time
            pygame.time.wait(self.frame_time - (pygame.time.get_ticks() - t0))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.field.snake_dir = 0
                if event.key == pygame.K_DOWN:
                    self.field.snake_dir = 1
                if event.key == pygame.K_RIGHT:
                    self.field.snake_dir = 2
                if event.key == pygame.K_LEFT:
                    self.field.snake_dir = 3

        self.field.step()

    def __draw_backg(self):
        for row in range(self.field.height):
            for col in range(self.field.width):
                pygame.draw.rect(self.screen,
                                 (COL_BACK1 if ((col+row)%2==0) else COL_BACK2),
                                 pygame.Rect(col*self.cell_width,
                                             row*self.cell_width,
                                             self.cell_width,
                                             self.cell_width))

    def draw(self):
        self.__draw_backg()
        for row in range(self.field.height):
            for col in range(self.field.width):
                cur = Pos(col,row)
                rect = pygame.Rect(cur.x*self.cell_width,
                                   cur.y*self.cell_width,
                                   self.cell_width,
                                   self.cell_width)

                if cur in self.field.snake_arr:
                    pygame.draw.rect(self.screen,COL_SNAKE,rect)
                elif cur == self.field.food_pos:
                    pygame.draw.rect(self.screen,COL_FOOD,rect)
                else:
                    pass

if __name__ == '__main__':
    Engine().run()

