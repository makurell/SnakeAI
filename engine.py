import pygame
from snake import Field, Pos
import neuroga

COL_BACK0 = (44,45,44)
COL_BACK1 = (66,67,65)
COL_BACK2 = (59,59,58)
COL_FOOD = (242,95,92)
COL_SNAKE = (255,224,102)

with open('models/d/2350.json','r') as f:
    net = neuroga.Network([24,4,4],saved=f.read())

class Engine:

    def __init__(self):
        self.field = Field()
        self.frame_time = 90  # amount of ms each frame is to be shown

        self.cell_width = 30

        # pygame setup
        self.game_surface = pygame.Surface((self.cell_width * self.field.width,
                                            self.cell_width * self.field.height))
        self.stats_surface = pygame.Surface((self.game_surface.get_width(), 34))

        self.screen:pygame.Surface = pygame.display.set_mode(
            (self.game_surface.get_width(),
             self.game_surface.get_height()+self.stats_surface.get_height()))
        pygame.display.set_caption('SnakeAI')

        pygame.font.init()
        self.font1 = pygame.font.SysFont('Arial',20)

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

        self.field.snake_dir=net.forward(self.field.get_senses()).argmax()

        self.field.step()
        # print(self.field.get_senses())

    def __draw_stats(self):
        self.stats_surface.fill(COL_BACK0)

        avg_eat_timing = round(sum(self.field.eat_timings)/len(self.field.eat_timings))
        text = 'Eaten: '+str(self.field.eaten) + '  '+\
               'Avg Steps: ' + str(avg_eat_timing)
        self.stats_surface.blit(self.font1.render(text,False,
                                                  (255,255,255)),(10,4))

    def __draw_backg(self):
        for row in range(self.field.height):
            for col in range(self.field.width):
                pygame.draw.rect(self.game_surface,
                                 (COL_BACK1 if ((col+row)%2==0) else COL_BACK2),
                                 pygame.Rect(col*self.cell_width,
                                             row*self.cell_width,
                                             self.cell_width,
                                             self.cell_width))

    def draw(self):
        self.__draw_stats()
        self.__draw_backg()
        for row in range(self.field.height):
            for col in range(self.field.width):
                cur = Pos(col,row)
                rect = pygame.Rect(cur.x*self.cell_width,
                                   cur.y*self.cell_width,
                                   self.cell_width,
                                   self.cell_width)

                if cur in self.field.snake_arr:
                    pygame.draw.rect(self.game_surface, COL_SNAKE, rect)
                elif cur == self.field.food_pos:
                    pygame.draw.rect(self.game_surface, COL_FOOD, rect)
                else:
                    pass

        self.screen.blit(self.stats_surface,(0,0))
        self.screen.blit(self.game_surface,(0,self.stats_surface.get_height()))

if __name__ == '__main__':
    Engine().run()

