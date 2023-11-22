import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE = 'Flappy Bird'
BIRD_SPEED = 7
GRAVITATION = 0.4
LIMIT_ANGLE = 45
PIPE_SPEED = 5
DISTANCE = 150



class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture('bg.png')
        self.bird = Bird()
        self.pipe_list = arcade.SpriteList()
        self.grass = arcade.load_texture('grass.png')
        self.game = True
        self.game_over = arcade.load_texture('gameover.png')
        self.score = 0

    def setup(self):
        for i in range(6):
            pipe_bottom = Pipe(False)
            pipe_bottom.center_y = random.randint(0, SCREEN_HEIGHT / 8)
            pipe_bottom.center_x = DISTANCE * i + SCREEN_WIDTH
            pipe_bottom.change_x = PIPE_SPEED
            self.pipe_list.append(pipe_bottom)
            pipe_top = Pipe(True)
            pipe_top.center_x = pipe_bottom.center_x
            pipe_top.center_y = random.randint(SCREEN_HEIGHT - SCREEN_HEIGHT / 8, SCREEN_HEIGHT)
            pipe_top.change_x = PIPE_SPEED
            self.pipe_list.append(pipe_top)

    def on_draw(self):
        self.clear((255, 255, 255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.bird.draw()
        self.pipe_list.draw()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.grass)
        if not self.game:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.game_over.width, self.game_over.height, self.game_over)
        arcade.draw_text(f'score: {self.score}', SCREEN_WIDTH - 155, SCREEN_HEIGHT - 60, arcade.color.BANANA_YELLOW , 25)

    def update(self, delta_time: float):
        if self.game:
            self.bird.update_animation(delta_time)
            self.bird.update()
            self.pipe_list.update()
            hit_list = arcade.check_for_collision_with_list(self.bird, self.pipe_list)
            if len(hit_list) > 0:
                self.game = False
                self.bird.stop()
                arcade.play_sound(self.bird.hit_sound, 0.2)
                for pipe in self.pipe_list:
                    pipe.stop()

    def on_key_press(self, key, modifiers):
        if self.game:
            if key == arcade.key.SPACE:
                self.bird.change_y = BIRD_SPEED
                self.bird.change_angle = BIRD_SPEED
                arcade.play_sound(self.bird.wing_sound, 0.2)


class Animate(arcade.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)




class Bird(Animate):
    def __init__(self):
        super().__init__('bird/yellowbird-downflap.png', 1)
        self.append_texture(arcade.load_texture('bird/yellowbird-midflap.png'))
        self.append_texture(arcade.load_texture('bird/yellowbird-upflap.png'))
        self.center_x = 50
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0
        self.hit_sound = arcade.load_sound('audio/hit.wav')
        self.wing_sound = arcade.load_sound('audio/wing.wav')

    def update(self):
        self.change_y -= GRAVITATION
        self.change_angle -= GRAVITATION
        self.center_y += self.change_y
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0
        self.angle += self.change_angle
        if self.angle <= -LIMIT_ANGLE:
            self.angle = -LIMIT_ANGLE
        if self.angle >= LIMIT_ANGLE:
            self.angle = LIMIT_ANGLE


class Pipe(arcade.Sprite):
    def __init__(self, is_up):
        super().__init__('pipe.png', 0.2, flipped_vertically=is_up)
        self.is_up = is_up
        self.point_sound = arcade.load_sound('audio/point.wav')

    def update(self):
        self.center_x -= self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH
            window.score += 1
            arcade.play_sound(self.point_sound, 0.2)
            if self.is_up:
                self.center_y = random.randint(SCREEN_HEIGHT - SCREEN_HEIGHT / 8, SCREEN_HEIGHT)
            else:
                self.center_y = random.randint(0, SCREEN_HEIGHT / 8)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()