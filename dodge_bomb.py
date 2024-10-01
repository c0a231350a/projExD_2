import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),pg.K_DOWN: (0, +5),pg.K_LEFT: (-5, 0),pg.K_RIGHT: (+5, 0),}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとん,または,爆弾のRect
    戻り値：真理値タプル（横判定結果，縦判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen):
    r = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(r,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    r.set_alpha(200)
    screen.blit(r,[0,0])
    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game Over",True,(255,255,255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2,HEIGHT/2
    screen.blit(txt,txt_rct)
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct2 = kk_img2.get_rect()
    kk_rct2.center = WIDTH/2-200,HEIGHT/2
    screen.blit(kk_img2,kk_rct2)
    kk_rct2.center = WIDTH/2+200,HEIGHT/2
    screen.blit(kk_img2,kk_rct2)
    pg.display.update()
    time.sleep(5)

def bomb_ex():
    accs = [a for a in range(1,11)]
    imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        imgs.append(bb_img)
    return accs,imgs

def kk_de(kk_img):
    return_img = kk_img
    key_lst = pg.key.get_pressed()
    if key_lst[pg.K_UP]:
        return_img= pg.transform.rotozoom(kk_img, 0, 0.9)
    elif key_lst[pg.K_DOWN]:
        return_img=pg.transform.rotozoom(kk_img, 180, 0.9)
    elif key_lst[pg.K_LEFT]:
        pg.transform.rotozoom(kk_img, 270, 0.9)
    elif key_lst[pg.K_RIGHT]:
        pg.transform.rotozoom(kk_img, 90, 0.9)
    elif key_lst[pg.K_UP] and key_lst[pg.K_RIGHT] :
        pg.transform.rotozoom(kk_img, 45, 0.9)
    elif key_lst[pg.K_DOWN] and key_lst[pg.K_RIGHT]:
        pg.transform.rotozoom(kk_img, 135, 0.9) 
    elif key_lst[pg.K_DOWN] and key_lst[pg.K_LEFT]:
        pg.transform.rotozoom(kk_img, 225, 0.9)
    elif key_lst[pg.K_UP] and key_lst[pg.K_LEFT]:
        pg.transform.rotozoom(kk_img, 315 ,0.9)                  
    return return_img

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) # 空のSurface
    bb_accs,bb_imgs = bomb_ex() #追加機能2
    bb_img.set_colorkey((0,0,0)) # 空のSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect() # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx,vy = +5 ,+5 # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            # こうかとんと爆弾が重なっていたら
            gameover(screen) #追加機能1
            print("GameOver")
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] # 横座標, 縦座標
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] # 横方向
                sum_mv[1] += tpl[1] # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        new_kk_img =kk_de(kk_img)
        kk_img = new_kk_img #追加機能3

        #bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        avx,avy = vx*bb_accs[min(tmr//500,9)] , vy*bb_accs[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500,9)]
        bb_rct.move_ip(avx,avy)
        bb_rct.width, bb_rct.height = bb_img.get_rect().width, bb_img.get_rect().height
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
