import pygame
import sys
import datetime
import json
import os
import random

pygame.init()
pygame.key.start_text_input()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_TOP, GRID_LEFT = 50, 100
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
TIMES = ['9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00']
cell_height = (SCREEN_HEIGHT - GRID_TOP - 50) // (len(TIMES) - 1)
GRID_HEIGHT = cell_height * (len(TIMES) - 1)
GRID_WIDTH = SCREEN_WIDTH - GRID_LEFT - 50
DATA_FILE = 'timetable_data.json'

WHITE, BLACK, GRAY = (255,255,255),(0,0,0),(200,200,200)
LIGHT_BLUE, DARK_GRAY, RED = (173,216,230),(50,50,50),(255,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Timetable")

font = pygame.font.SysFont('malgungothic',24)
small_font = pygame.font.SysFont('malgungothic',20)

def get_adjusted_font(text, max_width, base_size=24):
    size = base_size
    while size > 10:
        f = pygame.font.SysFont('malgungothic', size)
        if f.size(text)[0] <= max_width:
            return f
        size -= 1
    return pygame.font.SysFont('malgungothic', 10)

cell_width = GRID_WIDTH // len(DAYS)

VALID_USERS={'user1':'pass123','admin':'admin'}

timetable = {
    (0, 0): '수학',
    (1, 1): '영어',
    (2, 2): '과학',
    (3, 3): '국어',
    (4, 4): '사회',
    (0, 1): '세계사와문명교류'
}

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)
        data_items = {}
        for k, vlist in raw.items():
            key = tuple(map(int, k.split(',')))
            fixed_list = []
            for item in vlist:
                if item[0] == 'alarm':
                    dt = datetime.datetime.strptime(item[1], '%Y-%m-%d %H:%M')
                    fixed_list.append(('alarm', dt, item[2]))
                else:
                    fixed_list.append(tuple(item))
            data_items[key] = fixed_list
else:
    data_items = {}

class InputBox:
    def __init__(self,x,y,w,h,placeholder='',is_password=False):
        self.rect=pygame.Rect(x,y,w,h)
        self.color=BLACK; self.text=''; self.txt_surf=font.render('',True,self.color)
        self.placeholder_surf=font.render(placeholder,True,GRAY)
        self.active=False; self.is_password=is_password
    def handle_event(self,e):
        if e.type==pygame.MOUSEBUTTONDOWN:
            self.active=self.rect.collidepoint(e.pos)
            self.color=LIGHT_BLUE if self.active else BLACK
        elif e.type==pygame.KEYDOWN and self.active:
            if e.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]
        elif e.type==pygame.TEXTINPUT and self.active:
            self.text+=e.text
        disp='*'*len(self.text) if self.is_password else self.text
        self.txt_surf=font.render(disp,True,self.color)
    def draw(self,s):
        if not self.text:
            s.blit(self.placeholder_surf,(self.rect.x+5,self.rect.y+5))
        else:
            s.blit(self.txt_surf,(self.rect.x+5,self.rect.y+5))
        pygame.draw.rect(s,self.color,self.rect,2)

def save_data():
    serial = {}
    for k, v_list in data_items.items():
        ser_list = []
        for item in v_list:
            if item[0] == 'alarm':
                ser_list.append(['alarm', item[1].strftime('%Y-%m-%d %H:%M'), item[2]])
            else:
                ser_list.append(list(item))
        serial[f"{k[0]},{k[1]}"] = ser_list
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(serial, f, ensure_ascii=False, indent=2)

user_box=InputBox(300,200,200,40,'아이디 입력')
pass_box=InputBox(300,250,200,40,'비밀번호',True)
login_btn=pygame.Rect(350,300,100,40)

logged_in=False

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save_data()
            running = False

        if not logged_in:
            user_box.handle_event(e)
            pass_box.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN and login_btn.collidepoint(e.pos):
                if VALID_USERS.get(user_box.text) == pass_box.text:
                    logged_in = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                if VALID_USERS.get(user_box.text) == pass_box.text:
                    logged_in = True

    screen.fill(WHITE)
    if not logged_in:
        screen.blit(font.render('Login', True, BLACK), (360, 150))
        user_box.draw(screen)
        pass_box.draw(screen)
        pygame.draw.rect(screen, LIGHT_BLUE, login_btn)
        screen.blit(font.render('Login', True, BLACK), (login_btn.x + 20, login_btn.y + 5))
    else:
        colors = [(100,149,237), (173,216,230), (135,206,250), (30,144,255), (70,130,180), (0,191,255), (176,224,230)]

        # timetable 수업 블록 먼저 그리기
        for i, ((c, r), subj) in enumerate(timetable.items()):
            rct = pygame.Rect(GRID_LEFT + c * cell_width + 1, GRID_TOP + r * cell_height, cell_width - 2, cell_height)
            color = colors[i % len(colors)]
            pygame.draw.rect(screen, color, rct)
            adj_font = get_adjusted_font(subj, cell_width - 10)
            screen.blit(adj_font.render(subj, True, WHITE), (rct.x + 5, rct.y + 5))

        # 시간 및 요일 라벨 아래에 그리드 선 그리기 (항상 위에 오도록 마지막에 그림)
        for j in range(len(TIMES)):
            y = GRID_TOP + j * cell_height
            pygame.draw.line(screen, BLACK, (GRID_LEFT, y), (GRID_LEFT + GRID_WIDTH, y), 2)
            screen.blit(font.render(TIMES[j], True, BLACK), (GRID_LEFT - 80, y - 10))

        for i in range(len(DAYS)):
            x = GRID_LEFT + i * cell_width
            pygame.draw.line(screen, BLACK, (x, GRID_TOP), (x, GRID_TOP + GRID_HEIGHT), 2)
            screen.blit(font.render(DAYS[i], True, BLACK), (x + cell_width // 2 - 20, GRID_TOP - 30))

    pygame.display.flip()

pygame.key.stop_text_input()
pygame.quit()
sys.exit()
