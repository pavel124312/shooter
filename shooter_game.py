from pygame import *
from random import randint
import time as t_time

#фоновая музыка
recharge = 0
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
fps = 60
clock = time.Clock()
#шрифты и надписи
font.init()
font1 = font.SysFont("Arial", 90)
win = font1.render("YOU WIN!",True,(255,255,255))
lose = font1.render("YOU LOSE!",True,(180,0,0)) 
recharge_label = font1.render("Recharge!",True,(120,0,0))
font2 = font.SysFont("Arial", 36)

#нужные картинки
img_back = 'galaxy.jpg'   #фон
img_hero = 'rocket.png'   #герой
img_enemy = "ufo.png"     #враг
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"
life = 3
score = 0
lost = 0
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
#конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#класс главного игрока
class Timer():
    def __init__(self, sec):
        self.sec = sec
        self.start_time = t_time.time()
        self.end = self.start_time + sec
    
    def is_running(self):
        return t_time.time() < self.end
    
    def is_end(self):
        return t_time.time() >= self.end
    
    def reset(self):
        self.end = t_time.time() + self.sec



class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15 ,20,-15)
        bullets.add(bullet)

#класс спрайта-врага  
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update (self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill




#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


meteors = sprite.Group()
for i in range(1, 4):
    meteor = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
    meteors.add(meteor)



bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
timer = Timer(2)
while run:
    window.blit(background,(0,0)) 
    #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if recharge >= 5:
                    if timer.is_end():
                        recharge = 0

                else:
                    timer.reset()
                    recharge += 1
                    fire_sound.play()
                    ship.fire()
    if timer.is_running() and recharge >= 5:
        window.blit(recharge_label,(200,100))
    if not finish:
       #обновляем фон
        if sprite.spritecollide(ship,monsters, True) or sprite.spritecollide(ship,meteors,True):
            life -= 1
        if sprite.groupcollide(bullets,monsters,True, True) or sprite.groupcollide(bullets,meteors,True,True):
            score += 1 
        


       #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        #производим движения спрайтов
        ship.update()
        meteors.update()
        monsters.update()
        bullets.update()

       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        meteors.draw(window)
        display.update()
        
        
        if life <= 0:
            window.blit(font1.render("YOU WIN!",True,(255,255,255)),(0,0))
   #цикл срабатывает каждую 0.05 секунд
        if score <= 7:
            window.blit
    clock.tick(fps)