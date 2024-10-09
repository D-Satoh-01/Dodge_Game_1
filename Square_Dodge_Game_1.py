import pygame
import time
import random
pygame.font.init()

# ウィンドウサイズ
WIDTH, HEIGHT = 1000, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Dodge Game")

# プレイヤー
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_VEL = 10

# 降ってくる球
STAR_WIDTH = 20
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("Avenir", 50)

# 描画関連
def draw(player, elapsed_time, stars):
    WINDOW.fill((30, 30, 30))
    
    time_text = FONT.render(f"Time : {round(elapsed_time)}s", 1, "white")
    WINDOW.blit(time_text, (10 ,10))

    pygame.draw.rect(WINDOW, (120, 180, 255), player)
    
    # starはプレイヤーより上レイヤーに表示したいので、playerより下のコードラインに記述する
    for star in stars:
        pygame.draw.rect(WINDOW, "white", star)

    pygame.display.update()

# メイン処理
def main():
    run = True
    
    player = pygame.Rect(480, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0
    
    stars = []
    hit = False
    
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        # starの生成
        if star_count > star_add_increment:
            for _ in range(3):
                # starの座標をランダムに設定する
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                # 画面端より上の方にstarを配置する
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                # starをstarリストに追加する
                stars.append(star)
                
            # starの増加速度を加速させる (200は最低値)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # イベントの実行 (?)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        # プレイヤーの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
            
        # starの移動
        # スターリストの複製 (画面下に到達したstarを削除するため)
        # (動作中にリストを変更するとエラーが発生するのでコピーを生成している)
        for star in stars[:]:
            # starを下に動かす
            star.y += STAR_VEL
            # 画面外に行ったstarを削除する
            if star.y > HEIGHT:
                stars.remove(star)
            # starとプレイヤーの衝突を検知する
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        
        # ゲームオーバーの処理
        if hit:
            lost_text = FONT.render("Game Over", 1, "white")
            # テキストを画面中央に配置する
            WINDOW.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            # テキストを表示させる
            pygame.display.update()
            # 4000ミリ秒後にゲームを停止させる
            pygame.time.delay(4000)
            break
        
        # 各オブジェクトの描写
        draw(player, elapsed_time, stars)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()