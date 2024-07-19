import pygame as py
from sys import exit
import os
import random
import math
import time
py.init()
screen = py.display.set_mode((800, 400))
ss1 = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("main", "ss1.png")), (80, 60)), 270).convert_alpha()
ss2 = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("main", "ss2.png")), (80, 60)), 90).convert_alpha()
bg=py.transform.scale(py.image.load(os.path.join("main","spacebg.png")),(800,400))
bgwidth=bg.get_width()

metl = []
Clock = py.time.Clock()
one = py.Rect(360, 200, 55, 40)
two = py.Rect(600, 100, 55, 40)
bullets = []
bulletss = []
ss2life = 200
ss1life=200

def meteor(n):
    metx = random.randint(50, 350)
    mety = 0 + n
    x = {"rec":py.Rect(metx, mety, 50, 50),"angle":0}
    metl.append(x)

timer_event = py.USEREVENT + 1
py.time.set_timer(timer_event, 1500)

def metfall():
    global ss1life
    for met in metl:
        # Create a surface for the square and fill it with grey color
        met_surface = py.Surface((50, 50))
        met_surface.fill((192,192,192))
        # Rotate the square
        rotated_met = py.transform.rotate(met_surface, met['angle'])
        rotated_met_rect = rotated_met.get_rect(center=met['rec'].center)
        screen.blit(rotated_met, rotated_met_rect.topleft)
        met["angle"]+=1
        if met['angle'] >= 360:
            met['angle'] = 0
        met["rec"].y += 2
        if one.colliderect(met['rec']):
                # Collision detected
                ss1life-=0.5
                one.y+=1.4
        

def fire(rec):
    if len(bullets) < 3:
        bullet = py.Rect(rec.x, rec.y+30, 15, 7)
        bullets.append(bullet)
    for i in bullets:
        if i.x > 800:
            bullets.clear()

def managebullets():
    global ss2life
    for bullet in bullets:
        py.draw.rect(screen, (0, 250, 154), bullet)
        bullet.x += 10
        if bullet.y < two.y + 40 and bullet.y > two.y:
            if bullet.x < two.x and bullet.x > two.x - 55:
                ss2life -= 1
ebullets=[]
def efire(rec):
    print("fire")
    bullet = py.Rect(rec.x, rec.y+30, 100, 7)
    ebullets.append(bullet)
def emanage():
    global ss1life
    for i in ebullets:
        for j in range(0,4):
            py.draw.rect(screen,(200,0,0),i)
            i.x-=5
        if i.y < one.y + 40 and i.y > one.y:
            if i.x < one.x and i.x > one.x - 55:
                ss1life -= 10
                print(ss1life)
def enemyhb():
    hb = py.Rect(400, 0, ss2life * 2, 10)
    py.draw.rect(screen, (100, 10, 0), hb)
def myhb():
    global ss1life
    hb = py.Rect(0, 0, ss1life * 2, 10)
    py.draw.rect(screen, (0, 250, 154), hb)
def win(bg_x):
    screen.fill((0, 0, 0))
    screen.blit(bg,(bg_x,0))
    screen.blit(bg,(bg_x+bgwidth,0))
    screen.blit(ss2, (two.x, two.y))
    screen.blit(ss1, (one.x, one.y))
    #print(type(screen.blit(ss1, (one.x, one.y))))
    py.draw.rect(screen, (255, 255, 255), py.Rect(400, 0, 10, 400))
    enemyhb()
    myhb()
    managebullets()
    metfall()
    emanage()


def main():
    paused = False
    run = True
    n = math.pi
    mety = 200
    bg_x=0
    while run:
        bg_x-=1
        if bg_x<=-bgwidth:
            bg_x=0
        if not paused:
            mety -= 1
            n += 0.01
            two.y = 200 + math.cos(n) * (-120)
            two.x = 550 + math.sin(n) * (120)
            Clock.tick(60)
            keypressed = py.key.get_pressed()
            if keypressed[py.K_d] and one.x < 360:
                one.x += 2
            if keypressed[py.K_a] and one.x > 0:
                one.x -= 2
            if keypressed[py.K_s] and one.y < 400:
                one.y += 2
            if keypressed[py.K_w] and one.y > 0:
                one.y -= 2
            if keypressed[py.K_SPACE]:
                fire(one)
            win(bg_x)
            for event in py.event.get():
                if event.type == py.QUIT:
                    exit()
                elif event.type == timer_event:
                    meteor(n)
                    efire(two)
                    

                elif event.type == py.KEYDOWN:
                    if event.key == py.K_p:  # Press 'p' to toggle pause
                        paused = True
                        font = py.font.Font('main/pixelsans.ttf', 32)
                        text="press [p] to continue"
                        text_surface = font.render(text, True, (200,200,200))
                        text_rect = text_surface.get_rect()
                        text_rect.center = (400,200)
                        screen.fill((0,0,0))
                        screen.blit(text_surface, text_rect)
                if ss1life<=10:
                    paused=True
                    font = py.font.Font('main/pixelsans.ttf', 32)
                    text="GAMEOVER, YOU LOSE"
                    text_surface = font.render(text, True, (200,200,200))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (400,200)
                    screen.fill((0,0,0))
                    screen.blit(text_surface, text_rect)
                if ss2life<=0:
                    paused=True
                    font = py.font.Font('main/pixelsans.ttf', 32)
                    text="YOU WIN! :D"
                    text_surface = font.render(text, True, (200,200,200))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (400,200)
                    screen.fill((0,0,0))
                    screen.blit(text_surface, text_rect)
                
        else:
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_p:
                        paused = False
                if event.type == py.QUIT:
                    exit()

        py.display.flip()

main()
