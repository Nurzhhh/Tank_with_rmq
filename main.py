import pika
import sys
from threading import Thread
import pygame
import colorsys
import json
import random
import time
from datetime import datetime
import uuid

size_x = 800
size_y = 600

pygame.init()
screen = pygame.display.set_mode((size_x, size_y))

tank_right = pygame.image.load('pictures\\tank_right.png')
tank_left = pygame.image.load('pictures\\tank_left.png')
tank_up = pygame.image.load('pictures\\tank_up.png')
tank_down = pygame.image.load('pictures\\tank_down.png')

bullet_right = pygame.image.load('pictures\\bullet_r.png')
bullet_left = pygame.image.load('pictures\\bullet_l.png')
bullet_up = pygame.image.load('pictures\\bullet_u.png')
bullet_down = pygame.image.load('pictures\\bullet_d.png')

opp_right = pygame.image.load('pictures\\opp_r.png')
opp_left = pygame.image.load('pictures\\opp_l.png')
opp_up = pygame.image.load('pictures\\opp_u.png')
opp_down = pygame.image.load('pictures\\opp_d.png')

br = pygame.image.load('pictures\\br.png')
bl = pygame.image.load('pictures\\bl.png')
bu = pygame.image.load('pictures\\bu.png')
bd = pygame.image.load('pictures\\bd.png')

black = pygame.Color(0, 0, 0)
white = pygame.Color(250, 250, 200)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

Directions = {
    pygame.K_RIGHT: 'RIGHT', 
    pygame.K_LEFT: 'LEFT',
    pygame.K_UP: 'UP', 
    pygame.K_DOWN: 'DOWN',
    pygame.K_d: 'RIGHT', 
    pygame.K_a: 'LEFT',
    pygame.K_w: 'UP', 
    pygame.K_s: 'DOWN'
}


def singleplayer():
    class Tank:
        def __init__(self, x, y, speed, color, shoot):
            self.x = x
            self.y = y
            self.score = 3
            self.speed = speed
            self.color = color
            self.len = 31
            self.direction = 'RIGHT'
            self.KEYPULL = shoot

        def draw(self):
            if self.direction == 'UP':
                screen.blit(tank_up, (self.x, self.y))

            if self.direction == 'DOWN':
                screen.blit(tank_down, (self.x, self.y))

            if self.direction == 'RIGHT':
                screen.blit(tank_right, (self.x, self.y))

            if self.direction == 'LEFT':
                screen.blit(tank_left, (self.x, self.y))

            


        def change_direction(self, direction):
            self.direction = direction

        def move(self):
            if self.direction == 'LEFT':
                self.x -= self.speed
            if self.direction == 'RIGHT':
                self.x += self.speed
            if self.direction == 'UP':
                self.y -= self.speed
            if self.direction == 'DOWN':
                self.y += self.speed
            self.draw()
        
    class Bull:
        def __init__(self,x=0,y=0,color=(0,0,0),direction='LEFT',speed=7):
            self.x=x
            self.y=y
            self.color=color
            self.speed=speed
            self.direction=direction
            self.status=True
            self.distance=0
            self.a = 15
            self.b = 5

        def move(self):
            if self.direction == 'LEFT':
                self.x -= self.speed
            if self.direction == 'RIGHT':
                self.x += self.speed
            if self.direction == 'UP':
                self.y -= self.speed
            if self.direction == 'DOWN':
                self.y += self.speed
            self.distance += 1
            self.draw()

        def draw(self):
            if self.direction == 'LEFT':
                screen.blit(bullet_left, (self.x + 10, self.y - 1))

            elif self.direction == 'RIGHT':
                screen.blit(bullet_right, (self.x - 25, self.y - 2))

            elif self.direction == 'UP':
                screen.blit(bullet_up, (self.x - 1, self.y + 10))

            else:
                screen.blit(bullet_down, (self.x - 2, self.y - 25))


    class Super_Bull:
        def __init__(self,x=0,y=0,color=(0,0,0),direction='LEFT',speed=14):
            self.x=x
            self.y=y
            self.color=color
            self.speed=speed
            self.direction=direction
            self.status=True
            self.distance=0
            self.a = 15
            self.b = 5

        def move(self):
            if self.direction == 'LEFT':
                self.x -= self.speed
            if self.direction == 'RIGHT':
                self.x += self.speed
            if self.direction == 'UP':
                self.y -= self.speed
            if self.direction == 'DOWN':
                self.y += self.speed
            self.distance += 1
            self.draw()

        def draw(self):
            if self.direction == 'LEFT':
                screen.blit(bullet_left, (self.x + 10, self.y - 1))

            elif self.direction == 'RIGHT':
                screen.blit(bullet_right, (self.x - 25, self.y - 2))

            elif self.direction == 'UP':
                screen.blit(bullet_up, (self.x - 1, self.y + 10))

            else:
                screen.blit(bullet_down, (self.x - 2, self.y - 25))


    class Wall:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def draw(self):
            screen.blit(picture_wall, (self.x, self.y))
            
    class Health:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def draw(self):
            screen.blit(picture_heart, (self.x, self.y))

    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y))

    pygame.mixer.music.load('music\\nurzh.mp3')
    pygame.mixer.music.play()

    bulletSound=pygame.mixer.Sound('music\\bullet.wav')
    game_overSound=pygame.mixer.Sound('music\\game_over.wav')

    def buhhh(tank):
        if tank.direction == 'RIGHT':
            x = tank.x + tank.len + tank.len // 2
            y = tank.y + tank.len // 2

        if tank.direction == 'LEFT':
            x = tank.x - tank.len // 2
            y = tank.y + tank.len // 2

        if tank.direction == 'UP':
            x = tank.x + tank.len // 2
            y = tank.y - tank.len // 2

        if tank.direction == 'DOWN':
            x = tank.x + tank.len // 2
            y = tank.y + tank.len + tank.len // 2

        if ok:
            p = Super_Bull(x, y, black, tank.direction)
        else:
            p = Bull(x, y, black, tank.direction)
        bullets.append(p)

    def boom():
        for p in bullets:
            if p.x < 0 or p.x > size_x: #granica
                bullets.remove(p)
            if p.y < 0 or p.y > size_y: #granica
                bullets.remove(p)
            for i in walls:
                if p.x + 15 >= i.x and p.x <= i.x + 30:
                    if p.y + 8 > i.y and p.y < i.y + 31:
                        bullets.remove(p)
                        walls.remove(i)

        for wall in walls:
            if tanks[0].x + 31 > wall.x and tanks[0].x < wall.x + 31:
                if tanks[0].y + 31 > wall.y and tanks[0].y < wall.y + 31:
                    walls.remove(wall)
                    tanks[0].score -= 1
        


        if tanks[0].score <= 0:
            died()

    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Health : ' + str(tanks[0].score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (50, 10)
        else:
            score_rect.midtop = (250 , int(500.0 // 1.25))
        screen.blit(score_surface, score_rect)

    def died():
        pygame.mixer.music.stop()
        game_overSound.play()
        screen.fill((0,200,255))
        my_font = pygame.font.SysFont('times new roman', 75)
        game_over_surface = my_font.render('YOU DIED!', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (size_x//2, size_y//4)
        screen.fill(black)
        screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        main_menu()

    def game_over():
        pygame.mixer.music.stop()
        game_overSound.play()
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('Good Bye!', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (size_x//2, size_y//4)
        screen.fill(black)
        screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


    tank1 = Tank(160, 120, 3, (43, 68, 51), shoot=pygame.K_SPACE)

    bullet1 = Bull()


    tanks = [tank1]
    bullets = [bullet1]
    walls = []
    hearts = []
    picture_wall = pygame.image.load('pictures\\wall.png')
    picture_heart = pygame.image.load('pictures\\heart.png')
    clock = pygame.time.Clock()

    used = False
    # global ok
    ok = False
    start_time = random.randint(1, 54)
    runtime = start_time + 5
    tank_time = 0
    run = True
    while run:
        clock.tick(30)
        screen.fill(white)
        
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        run = False
                    pressed = pygame.key.get_pressed()
                    for tank in tanks:
                        if event.key in Directions.keys():
                            tank.change_direction(Directions[event.key])
                        
                        if pressed[tank.KEYPULL]:
                            bulletSound.play()
                            buhhh(tank)

            for tank in tanks:                   
                tank.move()

            for p in bullets:
                p.move()
            
            for tank in tanks:
                tank.draw() 
            
            if len(walls) < 5:
                walls.append(Wall(random.randint(31, size_x - 31), random.randint(31, size_y - 31)))

            for i in walls:
                i.draw()

            if not(used) and datetime.now().second == start_time:
                hearts.append(Health(random.randint(60, size_x - 60), random.randint(60, size_y - 60)))
                used = True
            
            if used and datetime.now().second == runtime:
                hearts = []
                used = False
                start_time = random.randint(1, 54)
                runtime = start_time + 5

            for i in hearts:
                i.draw()

            for heart in hearts:
                if tanks[0].x + 31 > heart.x and tanks[0].x < heart.x + 31:
                    if tanks[0].y + 31 > heart.y and tanks[0].y < heart.y + 31:
                        if used:
                            tank_time = datetime.now().second
                            hearts.remove(heart)
                            tanks[0].speed = 6
                            used = False
                            ok = True
                            start_time = random.randint(1, 54)
                            runtime = start_time + 5

            if ok and (tank_time + 5) % 60 == datetime.now().second:
                tanks[0].speed = 3
                ok = False

            cheat(tanks[0])
            boom()
            show_score(1, green, 'times', 20)
        
        except:
            pass

        pygame.display.flip()

#######################################################################################


def multiplayer():
    IP = '34.254.177.17'
    PORT = 5672
    VIRTUAL_HOST = 'dar-tanks'
    USERNAME = 'dar-tanks'
    PASSWORD ='5orPLExUYnyVYZg48caMpX'
    white = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode((size_x + 200, size_y))

    pygame.mixer.music.load('music\\nurzh.mp3')

    bulletSound=pygame.mixer.Sound('music\\bullet.wav')

    class Producer:
        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',
            auto_delete=True,
            exclusive=True 
            )
            self.callback_queue = queue.method.queue
            self.channel.queue_bind(
                exchange = 'X:routing.topic',
                queue= self.callback_queue
            )

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True
            )

            self.response = None
            self.corr_id = None
            self.token = None
            self.tank_id = None
            self.room_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)
                print(self.response)

        def call(self, key, message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message)
            )
            while self.response is None:
                self.connection.process_data_events()

        def check_sever_status(self):
            self.call('tank.request.healthcheck')
            return self.response['status'] == '200'

        def obtain_token(self, room_id):
            message = {
                'roomId': room_id
            }
            self.call('tank.request.register', message)
            if 'token' in self.response:
                self.token = self.response['token']
                self.tank_id = self.response['tankId']
                self.room_id = self.response['roomId']
                return True
            return False

        def turn_tank(self, token, direction):
            message = {
                'token': token,
                'direction': direction
            }
            self.call('tank.request.turn', message)

        def fire_bullet(self, token):
            message = {
                'token': token
            }
            self.call('tank.request.fire', message)

    class Consumer(Thread):
        def __init__(self, room_id):
            super().__init__()
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',
            auto_delete=True,
            exclusive=True 
            )
            event_listener = queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic', 
            queue = event_listener,
            routing_key='event.state.'+room_id)

            self.channel.basic_consume(
                queue=event_listener,
                on_message_callback=self.on_response,
                auto_ack=True
            )
            self.response=None

        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
            print(self.response)

        def run(self):
            self.channel.start_consuming()

        def close(self):
            self.channel.stop_consuming()

    Directions = {
        pygame.K_RIGHT: 'RIGHT', 
        pygame.K_LEFT: 'LEFT',
        pygame.K_UP: 'UP', 
        pygame.K_DOWN: 'DOWN',
        pygame.K_d: 'RIGHT', 
        pygame.K_a: 'LEFT',
        pygame.K_w: 'UP', 
        pygame.K_s: 'DOWN'
    }

    inform_hits = []

    def draw_tank(id, x, y, width, height, direction, **kwargs): 
        if id == mytank:
            if direction == 'UP':
                screen.blit(tank_up, (x, y))

            if direction == 'DOWN':
                screen.blit(tank_down, (x, y))

            if direction == 'RIGHT':
                screen.blit(tank_right, (x, y))

            if direction == 'LEFT':
                screen.blit(tank_left, (x, y))
        else:
            if direction == 'UP':
                screen.blit(opp_up, (x, y))

            if direction == 'DOWN':
                screen.blit(opp_down, (x, y))

            if direction == 'RIGHT':
                screen.blit(opp_right, (x, y))

            if direction == 'LEFT':
                screen.blit(opp_left, (x, y))


    def draw_bullet(owner, x, y, direction, **kwargs):
        if owner == mytank:
            if direction == 'LEFT':
                screen.blit(bullet_left, (x, y))

            elif direction == 'RIGHT':
                screen.blit(bullet_right, (x, y))

            elif direction == 'UP':
                screen.blit(bullet_up, (x, y))

            else:
                screen.blit(bullet_down, (x, y))
        else:
            if direction == 'LEFT':
                screen.blit(bl, (x, y))

            elif direction == 'RIGHT':
                screen.blit(br, (x, y))

            elif direction == 'UP':
                screen.blit(bu, (x, y))

            else:
                screen.blit(bd, (x, y))

    def back():
        main_menu()

    def Kick(n):
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 50)
        text = font.render('You KICKED OUT', True, red)
        score = str(n)
        text_score = font.render('Score: ' + score, True, red)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 70)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        back()

    def Win(n):
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 50)
        text = font.render('You WON', True, red)
        score = str(n)
        text_score = font.render('Score: ' + score, True, red)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 70)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        back()

    def Lose(n):
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 50)
        text = font.render('You LOSE', True, red)
        score = str(n)
        text_score = font.render('Score: ' + score, True, red)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 70)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        back()

    def restart():
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 80)
        text = font.render('Wait!!!', True, red)
        text_score = font.render('Restarting...' , True, white)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2 - 50)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 50)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        multiplayer()

    def game_start():
        mainloop = True

        font = pygame.font.Font('docktrin.ttf', 17)

        ok_kick = False
        ok_lose = False
        ok_win = False

        cnt = 0

        while mainloop:
            pygame.display.flip()
            screen.fill(white)
            pygame.draw.rect(screen, (blue), (800, 0, 200, 600))
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    client.daemon = True
                    event_client.close()
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        client.daemon = True
                        event_client.close()
                        mainloop = False
                    if event.key in Directions:
                        client.turn_tank(client.token, Directions[event.key])
                    if event.key == pygame.K_SPACE:
                        client.fire_bullet(client.token)
                        bulletSound.play()
                    if event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        client.daemon = True
                        event_client.close()
                        mainloop = False
                        restart()

            if event_client.response.get('remainingTime'):
                remaining_time = event_client.response['remainingTime']
            else:
                for i in kicked:
                    print(mytank)
                    if i['tankId'] == mytank:
                        pygame.mixer.music.stop()
                        ok_kick = True
                        cnt = i['score']

                for i in winners:
                    if i['tankId'] == mytank:
                        pygame.mixer.music.stop()
                        ok_win = True
                        cnt = i['score']

                for i in losers:
                    if i['tankId'] == mytank:
                        pygame.mixer.music.stop()
                        ok_lose = True
                        cnt = i['score']

                if ok_kick:
                    client.daemon = True
                    event_client.close()
                    Kick(cnt)

                if ok_win:
                    client.daemon = True
                    event_client.close()
                    Win(cnt)

                if ok_lose:
                    client.daemon = True
                    event_client.close()
                    Lose(cnt)

            text = font.render('Remaining Time: {}'.format(remaining_time), True, black) 
            textRect = text.get_rect()
            textRect.center = (size_x // 2, 100)
            screen.blit(text, textRect)
            

            tanks = event_client.response['gameField']['tanks']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            hits = event_client.response['hits']
            kicked = event_client.response['kicked']
            losers = event_client.response['losers']

            text = font.render('Id || score || health', True, (255, 255, 0)) 
            textRect = text.get_rect()
            textRect.center = (900, 40)
            screen.blit(text, textRect)
            sort = []

            for tank in tanks:
                draw_tank(**tank)
                score = tank['score']
                health = tank['health']
                id_tank = tank['id'][5:]
                sort.append([score, health, id_tank])
            k = 100
            for tank in sorted(sort, reverse=True):
                if tank[2] == mytank[5:]:
                    text = font.render('{} || {} || {}'.format(tank[2], tank[0], tank[1]), True, black) 
                else:
                    text = font.render('{} || {} || {}'.format(tank[2], tank[0], tank[1]), True, red) 
                textRect = text.get_rect()
                textRect.center = (900, k)
                screen.blit(text, textRect)
                k += 20

            for bullet in bullets:
                draw_bullet(**bullet)

            for hit in hits:
                now = datetime.now().second
                inform_hits.append([hit['source'], hit['destination'], now])

            text = font.render('Hits:', True, black) 
            textRect = text.get_rect()
            textRect.center = (900, 500)
            screen.blit(text, textRect)

            k = 520
            for hit in inform_hits:
                now = datetime.now().second
                if (hit[2] + 3) % 60 == now:
                    inform_hits.remove(hit)
                else:
                    if hit[1] == mytank:
                        text = font.render('{} => {}'.format(hit[0], hit[1]), True, black)
                    else:
                        if hit[2] == mytank:
                            text = font.render('{} => {}'.format(hit[0], hit[1]), True, red)
                        else:
                            text = font.render('{} => {}'.format(hit[0], hit[1]), True, green)
                    textRect = text.get_rect()
                    textRect.center = (900, k)
                    screen.blit(text, textRect)
                    k += 20

            for i in kicked:
                print(mytank)
                if i['tankId'] == mytank:
                    pygame.mixer.music.stop()
                    ok_kick = True
                    cnt = i['score']

            for i in winners:
                if i['tankId'] == mytank:
                    pygame.mixer.music.stop()
                    ok_win = True
                    cnt = i['score']

            for i in losers:
                if i['tankId'] == mytank:
                    pygame.mixer.music.stop()
                    ok_lose = True
                    cnt = i['score']

            if ok_kick:
                client.daemon = True
                event_client.close()
                Kick(cnt)

            if ok_win:
                client.daemon = True
                event_client.close()
                Win(cnt)

            if ok_lose:
                client.daemon = True
                event_client.close()
                Lose(cnt)
            pygame.display.flip()
            

    client = Producer()
    client.check_sever_status()
    client.obtain_token('room-17')
    mytank = client.tank_id
    event_client = Consumer('room-17')
    event_client.start()
    pygame.mixer.music.play()
    game_start()

##########################################################################################################


def multiplayer_with_ai():
    IP = '34.254.177.17'
    PORT = 5672
    VIRTUAL_HOST = 'dar-tanks'
    USERNAME = 'dar-tanks'
    PASSWORD ='5orPLExUYnyVYZg48caMpX'
    white = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode((size_x + 200, size_y))

    pygame.mixer.music.load('music\\nurzh.mp3')

    bulletSound=pygame.mixer.Sound('music\\bullet.wav')

    class Producer:
        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',
            auto_delete=True,
            exclusive=True 
            )
            self.callback_queue = queue.method.queue
            self.channel.queue_bind(
                exchange = 'X:routing.topic',
                queue= self.callback_queue
            )

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True
            )

            self.response = None
            self.corr_id = None
            self.token = None
            self.tank_id = None
            self.room_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)
                print(self.response)

        def call(self, key, message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message)
            )
            while self.response is None:
                self.connection.process_data_events()

        def check_sever_status(self):
            self.call('tank.request.healthcheck')
            return self.response['status'] == '200'

        def obtain_token(self, room_id):
            message = {
                'roomId': room_id
            }
            self.call('tank.request.register', message)
            if 'token' in self.response:
                self.token = self.response['token']
                self.tank_id = self.response['tankId']
                self.room_id = self.response['roomId']
                return True
            return False

        def turn_tank(self, token, direction):
            message = {
                'token': token,
                'direction': direction
            }
            self.call('tank.request.turn', message)

        def fire_bullet(self, token):
            message = {
                'token': token
            }
            self.call('tank.request.fire', message)

    class Consumer(Thread):
        def __init__(self, room_id):
            super().__init__()
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',
            auto_delete=True,
            exclusive=True 
            )
            event_listener = queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic', 
            queue = event_listener,
            routing_key='event.state.'+room_id)

            self.channel.basic_consume(
                queue=event_listener,
                on_message_callback=self.on_response,
                auto_ack=True
            )
            self.response=None

        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
            print(self.response)

        def run(self):
            self.channel.start_consuming()

        def close(self):
            self.channel.stop_consuming()

    Directions = {
        pygame.K_RIGHT: 'RIGHT', 
        pygame.K_LEFT: 'LEFT',
        pygame.K_UP: 'UP', 
        pygame.K_DOWN: 'DOWN',
        pygame.K_d: 'RIGHT', 
        pygame.K_a: 'LEFT',
        pygame.K_w: 'UP', 
        pygame.K_s: 'DOWN'
    }

    def draw_tank(id, x, y, width, height, direction, **kwargs): 
        if id == mytank:
            if direction == 'UP':
                screen.blit(tank_up, (x, y))

            if direction == 'DOWN':
                screen.blit(tank_down, (x, y))

            if direction == 'RIGHT':
                screen.blit(tank_right, (x, y))

            if direction == 'LEFT':
                screen.blit(tank_left, (x, y))
        else:
            if direction == 'UP':
                screen.blit(opp_up, (x, y))

            if direction == 'DOWN':
                screen.blit(opp_down, (x, y))

            if direction == 'RIGHT':
                screen.blit(opp_right, (x, y))

            if direction == 'LEFT':
                screen.blit(opp_left, (x, y))


    def draw_bullet(owner, x, y, direction, **kwargs):
        if owner == mytank:
            if direction == 'LEFT':
                screen.blit(bullet_left, (x, y))

            elif direction == 'RIGHT':
                screen.blit(bullet_right, (x, y))

            elif direction == 'UP':
                screen.blit(bullet_up, (x, y))

            else:
                screen.blit(bullet_down, (x, y))
        else:
            if direction == 'LEFT':
                screen.blit(bl, (x, y))

            elif direction == 'RIGHT':
                screen.blit(br, (x, y))

            elif direction == 'UP':
                screen.blit(bu, (x, y))

            else:
                screen.blit(bd, (x, y))

    def back():
        main_menu()

    def Kick(n):
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 50)
        text = font.render('You KICKED OUT', True, red)
        score = str(n)
        text_score = font.render('Score: ' + score, True, red)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2 - 40)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 30)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        back()

    def Win(n):
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 50)
        text = font.render('You WON', True, red)
        score = str(n)
        text_score = font.render('Score: ' + score, True, red)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2 - 40)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 30)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        back()

    def Lose(n):
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 50)
        text = font.render('You LOSE', True, red)
        score = str(n)
        text_score = font.render('Score: ' + score, True, red)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2 - 40)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 30)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        back()

    def restart():
        pygame.init()
        screen = pygame.display.set_mode((size_x, size_y))
        screen.fill(black)
        font = pygame.font.Font('docktrin.ttf', 80)
        text = font.render('Wait!!!', True, red)
        text_score = font.render('Restarting...' , True, white)
        textRect = text.get_rect()
        text_scoreRect = text_score.get_rect()
        textRect.center = (size_x // 2, size_y // 2 - 50)
        text_scoreRect.center = (size_x // 2, size_y // 2 + 50)
        screen.blit(text, textRect)
        screen.blit(text_score, text_scoreRect)
        pygame.display.flip()
        time.sleep(5)
        multiplayer_with_ai()

    def game_start():
        mainloop = True
        font = pygame.font.Font('docktrin.ttf', 17)

        ok_kick = False
        ok_lose = False
        ok_win = False

        mytank_x = None
        mytank_y = None
        mytank_direction = None

        cnt = 0
        while mainloop:
            pygame.display.flip()
            screen.fill(white)
            turn = False
            pygame.draw.rect(screen, (blue), (800, 0, 200, 600))
            pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    client.daemon = True
                    event_client.close()
                    mainloop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        client.daemon = True
                        event_client.close()
                        mainloop = False

                    if event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        client.daemon = True
                        event_client.close()
                        mainloop = False
                        restart()

            tanks = event_client.response['gameField']['tanks']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            hits = event_client.response['hits']
            kicked = event_client.response['kicked']
            losers = event_client.response['losers']

            # Mina zherde ozimnin ornimdi tauip alam
            for tank in tanks: 
                if tank['id'] == mytank:
                    mytank_x = tank['x']
                    mytank_y = tank['y']
                    mytank_direction = tank['direction']

            #tank burilu atu
            for tank in tanks:
                if tank['id'] != mytank:
                    if mytank_x - 71 > tank['x'] > mytank_x + 71 and mytank_y - 71 > tank['y'] > mytank_y + 71:
                        if tank['direction'] == 'LEFT' or tank['direction'] == 'RIGHT':
                            client.turn_tank(client.token, Directions[pygame.K_DOWN])
                        else:
                            client.turn_tank(client.token, Directions[pygame.K_LEFT])
                        # turn = True

                    elif tank['x'] + 31 > mytank_x > tank['x'] - 31:
                        if mytank_y > tank['y']:
                            client.turn_tank(client.token, Directions[pygame.K_UP])
                            client.fire_bullet(client.token)
                            bulletSound.play()
                        else:
                            client.turn_tank(client.token, Directions[pygame.K_DOWN])
                            client.fire_bullet(client.token)
                            bulletSound.play()
                        # turn = True

                    elif tank['y'] + 31 > mytank_y > tank['y'] - 31:
                        if mytank_x > tank['x']:
                            client.turn_tank(client.token, Directions[pygame.K_LEFT])
                            client.fire_bullet(client.token)
                            bulletSound.play()
                        else:
                            client.turn_tank(client.token, Directions[pygame.K_RIGHT])
                            client.fire_bullet(client.token)
                            bulletSound.play()
                        # turn = True
            #tank burilu atu
            for bullet in bullets:
                bullet_direction = bullet['direction']
                bullet_x = bullet['x']
                bullet_y = bullet['y']
                if bullet['owner'] != mytank: #and not(turn):
                    if bullet_direction == 'RIGHT' or bullet_direction == 'LEFT':
                        if mytank_direction == 'LEFT' or bullet_direction == 'RIGHT':
                            if -31 > mytank_y - bullet_y > 5:
                                client.turn_tank(client.token, Directions[pygame.K_DOWN])
                    else:
                        if mytank_direction == 'UP' or bullet_direction == 'DOWN':
                            if -31 > mytank_x - bullet_x > 5:
                                client.turn_tank(client.token, Directions[pygame.K_RIGHT])

                    if bullet_direction == 'RIGHT':
                        if mytank_direction == 'UP':
                            if 15 > mytank_x - bullet_x > 65:
                                if 5 > mytank_y - bullet_y > 55:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_DOWN])
                        elif mytank_direction == 'DOWN':
                            if 15 > mytank_x - bullet_x > 65:
                                if 30 > bullet_y - mytank_y > 80:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_UP])
                        elif mytank_direction == 'LEFT':
                            if -31 > mytank_y - bullet_y > 5:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_UP])
                        else:
                            if -31 > mytank_y - bullet_y > 5:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_DOWN])
                    elif bullet_direction == 'LEFT':
                        if mytank_direction == 'UP':
                            if 30 > bullet_x - mytank_x > 80:
                                if 5 > mytank_y - bullet_y > 55:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_DOWN])
                        elif mytank_direction == 'DOWN':
                            if 30 > bullet_x - mytank_x > 80:
                                if 30 > bullet_y - mytank_y > 80:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_UP])
                        elif mytank_direction == 'LEFT':
                            if -31 > mytank_y - bullet_y > 5:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_UP])
                        else:
                            if -31 > mytank_y - bullet_y > 5:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_DOWN])
                    elif bullet_direction == 'DOWN':
                        if mytank_direction == 'UP':
                            if -31 > mytank_x - bullet_x > 5:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_LEFT])
                        elif mytank_direction == 'DOWN':
                            if -31 > mytank_x - bullet_x > 5:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_RIGHT])
                        elif mytank_direction == 'LEFT':
                            if 15 > mytank_y - bullet_y > 65:
                                if 5 > mytank_x - bullet_x > 55:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_RIGHT])
                        else:
                            if 15 > mytank_y - bullet_y > 65:
                                if 31 > bullet_x - mytank_x > 81:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_LEFT])
                    else:
                        if mytank_direction == 'UP':
                            if -5 > mytank_x - bullet_x > 31:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_LEFT])
                        elif mytank_direction == 'DOWN':
                            if -5 > mytank_x - bullet_x > 31:
                                client.fire_bullet(client.token)
                                bulletSound.play()
                                client.turn_tank(client.token, Directions[pygame.K_RIGHT])
                        elif mytank_direction == 'LEFT':
                            if 31 > bullet_y - mytank_y > 81:
                                if 5 > mytank_x - bullet_x > 55:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_RIGHT])
                        else:
                            if 31 > bullet_y - mytank_y > 81:
                                if 31 > bullet_x - mytank_x > 81:
                                    client.fire_bullet(client.token)
                                    bulletSound.play()
                                    client.turn_tank(client.token, Directions[pygame.K_LEFT])
    
            if event_client.response.get('remainingTime'):
                remaining_time = event_client.response['remainingTime']
                if remaining_time % 10 == 0 and remaining_time % 20 != 0:
                    client.turn_tank(client.token, Directions[pygame.K_LEFT])
                elif remaining_time % 10 == 0 and remaining_time % 20 == 0:
                    client.turn_tank(client.token, Directions[pygame.K_RIGHT])
                if remaining_time % 4 == 0:
                    client.fire_bullet(client.token)
                    bulletSound.play()
            else:
                for i in kicked:
                    print(mytank)
                    if i['tankId'] == mytank:
                        pygame.mixer.music.stop()
                        ok_kick = True
                        cnt = i['score']

                for i in winners:
                    if i['tankId'] == mytank:
                        pygame.mixer.music.stop()
                        ok_win = True
                        cnt = i['score']

                for i in losers:
                    if i['tankId'] == mytank:
                        pygame.mixer.music.stop()
                        ok_lose = True
                        cnt = i['score']

                if ok_kick:
                    client.daemon = True
                    event_client.close()
                    Kick(cnt)

                if ok_win:
                    client.daemon = True
                    event_client.close()
                    Win(cnt)

                if ok_lose:
                    client.daemon = True
                    event_client.close()
                    Lose(cnt)

            text = font.render('Remaining Time: {}'.format(remaining_time), True, black) 
            textRect = text.get_rect()
            textRect.center = (size_x // 2, 100)
            screen.blit(text, textRect)
            


            text = font.render('Id || score || health', True, black) 
            textRect = text.get_rect()
            textRect.center = (900, 40)
            screen.blit(text, textRect)
            sort = []
    
            for tank in tanks:
                draw_tank(**tank)
                score = tank['score']
                health = tank['health']
                id_tank = tank['id'][5:]
                sort.append([score, health, id_tank])
            k = 100
            for tank in sorted(sort, reverse=True):
                if tank[2] == mytank[5:]:
                    text = font.render('{} || {} || {}'.format(tank[2], tank[0], tank[1]), True, black) 
                else:
                    text = font.render('{} || {} || {}'.format(tank[2], tank[0], tank[1]), True, red) 
                textRect = text.get_rect()
                textRect.center = (900, k)
                screen.blit(text, textRect)
                k += 20
                
            for bullet in bullets:
                draw_bullet(**bullet)

            for i in kicked:
                print(mytank)
                if i['tankId'] == mytank:
                    pygame.mixer.music.stop()
                    ok_kick = True
                    cnt = i['score']

            for i in winners:
                if i['tankId'] == mytank:
                    pygame.mixer.music.stop()
                    ok_win = True
                    cnt = i['score']

            for i in losers:
                if i['tankId'] == mytank:
                    pygame.mixer.music.stop()
                    ok_lose = True
                    cnt = i['score']

            if ok_kick:
                client.daemon = True
                event_client.close()
                Kick(cnt)

            if ok_win:
                client.daemon = True
                event_client.close()
                Win(cnt)

            if ok_lose:
                client.daemon = True
                event_client.close()
                Lose(cnt)
            pygame.display.flip()
            

    client = Producer()
    client.check_sever_status()
    client.obtain_token('room-17')
    mytank = client.tank_id
    event_client = Consumer('room-17')
    event_client.start()
    pygame.mixer.music.play()
    game_start()

###################################################################################


def cheat(tank):
    if tank.x < -41:
        tank.x = size_x
    elif tank.x > size_x:
        tank.x = -40
    if tank.y < -41:
        tank.y = size_y
    elif tank.y > size_y:
        tank.y = -40

def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Good Bye!', True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (size_x//2, size_y//4)
    screen.fill(black)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

white = (255, 255, 255)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y))
    font = "docktrin.ttf"
    click = False
    klok = pygame.time.Clock()
    FPS = 60
    while True:
        ms = klok.tick(FPS)
        screen.fill((0,200,255))

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(170, 245, 460, 70)
        button2 = pygame.Rect(180, 325, 440, 70)
        button3 = pygame.Rect(50, 405, 700, 70)
        button4 = pygame.Rect(280, 485, 280, 70)

        ok1 = False
        ok2 = False
        ok3 = False
        ok4 = False

        if button1.collidepoint((mx, my)):
            ok1 = True
            if click:
                singleplayer()

        if button2.collidepoint((mx, my)):
            ok2 = True
            if click:
                multiplayer()
            
        if button3.collidepoint((mx, my)):
            ok3 = True
            if click:
                multiplayer_with_ai()

        if button4.collidepoint((mx, my)):
            ok4 = True
            if click:
                game_over()

        if ok1:
            pygame.draw.rect(screen, (255, 0, 0), button1)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button1)
        if ok2:
            pygame.draw.rect(screen, (255, 0, 0), button2)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button2)
        if ok3:
            pygame.draw.rect(screen, (255, 0, 0), button3)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button3)
        if ok4:
            pygame.draw.rect(screen, (255, 0, 0), button4)
        else:
            pygame.draw.rect(screen, (200, 0, 0), button4)

        my_font = pygame.font.SysFont('times new roman', 90)

        single_player_text = text_format("Single Player", font, 75, white) 
        multi_player_text = text_format("Multiplayer", font, 75, white)
        multi_player_with_ai_text = text_format("Multiplayer with AI" ,font, 75, white)
        quit_text = text_format("QUIT", font, 75, white)

        single_player_rect = single_player_text.get_rect()
        multi_player_rect = multi_player_text.get_rect()
        multi_player_with_ai_rect = multi_player_with_ai_text.get_rect()
        quit_rect = quit_text.get_rect()

        screen.blit(single_player_text, (size_x//2 - (single_player_rect[2]//2), 250))
        screen.blit(multi_player_text, (size_x//2 - (multi_player_rect[2]//2), 330))
        screen.blit(multi_player_with_ai_text, (size_x//2 - (multi_player_with_ai_rect[2]//2), 410))
        screen.blit(quit_text, (size_x//2 - (quit_rect[2]//2), 490))
        pygame.display.update()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        

main_menu()