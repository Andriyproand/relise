
from pygame import *
from random import randint  


class GameSprite(sprite.Sprite):

    def __init__(self, player_image , player_x , player_y, size_x, syze_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, syze_y)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset (self):
        window.blit(self.image,(self.rect.x , self.rect.y)) 

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed [K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed  

            keys_pressed = key.get_pressed()
        if keys_pressed [K_RIGHT] and self.rect.x < win_width - 80 :
            self.rect.x += self.speed


    def fire(self):
        bullett = Bullet('laser.png', self.rect.centerx, self.rect.top, 65, 70, -15)
        bullets.add(bullett)
#лічильник збитих і пропущених кораблів
    
score = 0
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



#ігрова сцена
win_width = 1200
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galexy.jpg"), (win_width, win_height))
#шрифти ы написи
font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)


txt_lose_game = font1.render("YOU LOSE", True, [255, 0, 0])
txt_win_game = font1.render("YOU WIN", True, [0, 255, 0])
txt_boss = font1.render("BOSS", True, [0, 0, 0])
#зображення
asteroid = 'enemy.png'
fon = 'galexy.jpg'
rocket = 'lok.png'
BOSS = 'boss_anemy.png'

#спайти
bullets = sprite.Group()


rocket = Player(rocket, 5, win_height - 100, 80, 100, 20)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(asteroid, randint(80, win_width - 80), -40, 140, 150, randint(1, 5))
    monsters.add(monster) 

#змінна гра закінчилась
font.init() 
score_boss= 55         
finish = False
level_1 = True
boss = False
#Основний цикл гри
run = True
while run:

    #подія натискання на кнопку закрити
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
        
    if not finish:
        if level_1:
            window.blit(background, (0, 0))
            
            #пишемо текст на екрані

            text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))

            text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))

            #рухи спрайтів

            rocket.update()
            monsters.update()

            rocket.reset()
            
            monsters.draw(window)
            
            bullets.draw(window)
            bullets.update()

            if sprite.spritecollide(rocket, monsters, False):
                finish = True
                window.blit(txt_lose_game, (200, 200))

            if sprite.spritecollide(boss, bullets, False):
                score_boss -= 1 
            # if score_boss == 0:
            #     ...
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                monster = Enemy(asteroid, randint(80, win_width - 80), -40, 190, 180, randint(1, 5))
                monsters.add(monster) 
                score += 1
            if score == 2 :
                window.blit(txt_boss, (200, 200)) 
                boss = True
                level_1 = False
            if lost >= 6:
                window.blit(txt_lose_game, (200, 200))
                finish = True
        if boss:
            window.blit(background, (0, 0))
            BOSS = Player('boss_anemy.png' , 200, win_height - 700, 400, 500, 0)
            BOSS.reset()
            rocket.update()       
            rocket.reset() 
            bullets.draw(window) 
            bullets.update()
            text_heal= font2.render( "Heal: "+str(score_boss), 1, (100, 255, 255))
            window.blit(text_heal, (10, 50))
            time.set_timer(USEREVENT, 1000)


    else:
            # score = 0
            # score_boss=0
            # lost = 0
            finish = False

            for m in monsters:
                m.kill()
            
            for m in bullets:
                m.kill()

            time.delay(3000)
            for i in range(1, 6):
                monster = Enemy(asteroid, randint(80, win_width - 80), -40, 140, 150, randint(1, 5))
                monsters.add(monster)
        
    



    display.update()

    time.delay(50)  