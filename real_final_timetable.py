import os
import sys
import pygame
import datetime
import json
import subprocess
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.key.start_text_input()

subject_colors = {}

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_TOP, GRID_LEFT = 50, 100
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
TIMES = ['9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00']
cell_height = (SCREEN_HEIGHT - GRID_TOP - 50) // (len(TIMES))
GRID_HEIGHT = cell_height * len(TIMES)
GRID_WIDTH = SCREEN_WIDTH - GRID_LEFT - 50
DATA_FILE = 'timetable_data.json'

WHITE, BLACK, GRAY = (255,255,255),(0,0,0),(200,200,200)
BLUE, LIGHT_BLUE, DARK_GRAY, RED = (100,149,237),(173,216,230),(50,50,50),(255,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Timetable with Scrollable Notes and Delete")

font = pygame.font.SysFont('malgungothic',24)
small_font = pygame.font.SysFont('malgungothic',16)

cell_width = GRID_WIDTH // len(DAYS)

timetable = {}
data_items = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)
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

class InputBox:
    def __init__(self,x,y,w,h,placeholder='',is_password=False):
        self.rect=pygame.Rect(x,y,w,h)
        self.color=BLACK; self.text=''; self.txt_surf=font.render('',True,self.color)
        self.placeholder_surf=font.render(placeholder,True,GRAY)
        self.active=False; self.is_password=is_password
    def handle_event(self,e):
        if e.type==pygame.MOUSEBUTTONDOWN:
            self.active=self.rect.collidepoint(e.pos)
            self.color=BLUE if self.active else BLACK
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

def run_scraper_with_input(student_id, password):
    process = subprocess.Popen(
        [sys.executable, "scraper.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=f"{student_id}\n{password}\n")
    return stdout, stderr

def run_make_timetable():
    result = subprocess.run([sys.executable, "make_timetable.py"], capture_output=True, text=True)
    return result.stdout

def parse_timetable_output(output):
    timetable = {}
    lines = output.splitlines()
    for line in lines:
        match = re.match(r'^([A-Z0-9]+)\s+(.+?)\s+\(.+?\)\s+→\s+(.+)$', line)
        if match:
            code, name, time_str = match.groups()
            time_str = re.sub(r'\[.*?\]', '', time_str)

            # 요일별 블록 분리: '월 08 ,09  수 07 ,08' → ['월 08 ,09', '수 07 ,08']
            blocks = re.findall(r'(?:월|화|수|목|금)[^월화수목금]*', time_str)

            for block in blocks:
                block = block.strip()
                if not block:
                    continue
                current_day = block[0]
                col = {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4}.get(current_day)
                if col is None:
                    continue
                periods = re.findall(r'\d+', block)
                for p in periods:
                    row = int(p) - 1
                    timetable[(col, row)] = name
    return timetable




def draw_text_multiline(surface, texts, rect):
    for i, text in enumerate(texts):
        font_to_use = font if font.size(text)[0] <= rect.width - 10 else small_font
        text_surf = font_to_use.render(text, True, WHITE)
        y = rect.y + 5 + i * font_to_use.get_linesize()
        if y + font_to_use.get_linesize() < rect.y + rect.height:
            surface.blit(text_surf, (rect.x + 5, y))

def draw_text_wrapped(surface, text, rect, font_name, base_size, color):
    size = base_size
    font = pygame.font.SysFont(font_name, size)

    # 폰트 너비가 셀보다 크면 계속 줄이기
    while font.size(text)[0] > rect.width - 10 and size > 10:
        size -= 1
        font = pygame.font.SysFont(font_name, size)

    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] > rect.width - 10:
            lines.append(current_line.strip())
            current_line = word + ' '
        else:
            current_line = test_line
    lines.append(current_line.strip())

    y = rect.top + 5
    for line in lines:
        line_surf = font.render(line, True, color)
        surface.blit(line_surf, (rect.left + 5, y))
        y += font.get_linesize()



logged_in = False
user_box = InputBox(300, 200, 200, 40, '아이디 입력')
pass_box = InputBox(300, 250, 200, 40, '비밀번호', True)
login_btn = pygame.Rect(350, 300, 100, 40)



running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if not logged_in:
            user_box.handle_event(e)
            pass_box.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN and login_btn.collidepoint(e.pos):
                logged_in = True
                stdout, stderr = run_scraper_with_input(user_box.text, pass_box.text)
                if stderr:
                    print("❌ scraper 실행 오류:", stderr)
                timetable_output = run_make_timetable()
                print("=== timetable_output ===")
                print(timetable_output)
                print("========================")
                timetable.clear()
                timetable.update(parse_timetable_output(timetable_output))
                print("== FINAL TIMETABLE ==")
                for k, v in timetable.items():
                    print(k, ":", v)


    screen.fill(WHITE)
    if not logged_in:
        screen.blit(font.render('Login', True, BLACK), (360, 150))
        user_box.draw(screen)
        pass_box.draw(screen)
        pygame.draw.rect(screen, LIGHT_BLUE, login_btn)
        screen.blit(font.render('Login', True, BLACK), (login_btn.x + 20, login_btn.y + 5))
    else:
        pygame.draw.rect(screen, GRAY, (GRID_LEFT, GRID_TOP, GRID_WIDTH, GRID_HEIGHT), 2)
        for i, day in enumerate(DAYS):
            x = GRID_LEFT + i * cell_width
            pygame.draw.line(screen, GRAY, (x, GRID_TOP), (x, GRID_TOP + GRID_HEIGHT))
            screen.blit(font.render(day, True, BLACK), (x + cell_width // 2 - 20, GRID_TOP - 30))
        for j, time in enumerate(TIMES):
            y = GRID_TOP + j * cell_height
            pygame.draw.line(screen, GRAY, (GRID_LEFT, y), (GRID_LEFT + GRID_WIDTH, y))
            screen.blit(font.render(time, True, BLACK), (GRID_LEFT - 80, y - 10))

        for (c, r), subj in timetable.items():
            rct = pygame.Rect(
                GRID_LEFT + c * cell_width + 1,
                GRID_TOP + r * cell_height,
                cell_width - 2,
                cell_height
            )
                # 색상이 등록 안 돼 있으면 새로 생성해서 저장
            if subj not in subject_colors:
                subject_colors[subj] = (
                    random.randint(100, 255),  # 밝은 색상만
                    random.randint(100, 255),
                    random.randint(100, 255)
                )

            color = subject_colors[subj]
            pygame.draw.rect(screen, color, rct)

            draw_text_wrapped(screen, subj, rct, "malgungothic", 18, WHITE)

    pygame.display.flip()

pygame.key.stop_text_input()
pygame.quit()
sys.exit()
