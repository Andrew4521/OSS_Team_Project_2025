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
pygame.display.set_caption("Timetable with Memo & Alarm")

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
selected_cell=None
input_box=None
add_btn=None
close_btn=None

tabs = ['기본 정보', '메모', '알람']
current_tab = 0
scroll_offset = 0
delete_buttons = []

def draw_overlay(cell, mouse_event=None):
    global current_tab, delete_buttons, selected_cell
    delete_buttons = []
    ox=(SCREEN_WIDTH-600)//2; oy=(SCREEN_HEIGHT-560)//2
    pygame.draw.rect(screen,DARK_GRAY,(ox,oy,600,560))

    for i, name in enumerate(tabs):
        tab_rect = pygame.Rect(ox + 20 + i * 130, oy + 20, 120, 40)
        pygame.draw.rect(screen, LIGHT_BLUE if current_tab == i else GRAY, tab_rect)
        screen.blit(font.render(name, True, BLACK), (tab_rect.x + 10, tab_rect.y + 5))
        if mouse_event and tab_rect.collidepoint(mouse_event.pos):
            current_tab = i

    items = data_items.get(cell, [])
    visible_area_y = oy + 80
    visible_height = 320
    item_height = 24
    total_height = len(items) * item_height

    if current_tab in [1, 2]:
        start_y = visible_area_y + scroll_offset
        for idx, it in enumerate(items):
            y = start_y + idx * item_height
            if visible_area_y <= y <= visible_area_y + visible_height:
                if (it[0] == 'memo' and current_tab == 1) or (it[0] == 'alarm' and current_tab == 2):
                    text = f"- {it[1]}: {it[2]}" if it[0] == 'memo' else f"- {it[2]} @ {it[1].strftime('%Y-%m-%d %H:%M')}"
                    screen.blit(small_font.render(text, True, WHITE), (ox + 40, y))
                    del_btn = pygame.Rect(ox + 540, y, 20, 20)
                    pygame.draw.rect(screen, RED, del_btn)
                    screen.blit(small_font.render("X", True, WHITE), (del_btn.x + 5, del_btn.y))
                    delete_buttons.append((del_btn, idx))

        if total_height > visible_height:
            scrollbar_height = max(30, visible_height * visible_height // total_height)
            scroll_pos = int((-scroll_offset) * (visible_height - scrollbar_height) / max(total_height, 1))
            scrollbar = pygame.Rect(ox + 560, visible_area_y + scroll_pos, 10, scrollbar_height)
            pygame.draw.rect(screen, GRAY, (ox + 560, visible_area_y, 10, visible_height))
            pygame.draw.rect(screen, RED, scrollbar)

    close_btn_rect = pygame.Rect(ox + 240, oy + 520, 100, 40)
    pygame.draw.rect(screen, LIGHT_BLUE, close_btn_rect)
    screen.blit(font.render('Close', True, BLACK), (close_btn_rect.x + 10, close_btn_rect.y + 5))
    if mouse_event and close_btn_rect.collidepoint(mouse_event.pos):
        selected_cell = None

running = True
while running:
    mouse_click_event = None
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save_data()
            running = False
        elif selected_cell and e.type == pygame.MOUSEWHEEL:
            items = data_items.get(selected_cell, [])
            max_scroll = max(0, len(items)*24 - 320)
            scroll_offset += e.y * 20
            scroll_offset = max(min(scroll_offset, 0), -max_scroll)

        if not logged_in:
            user_box.handle_event(e)
            pass_box.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN and login_btn.collidepoint(e.pos):
                if VALID_USERS.get(user_box.text) == pass_box.text:
                    logged_in = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                if VALID_USERS.get(user_box.text) == pass_box.text:
                    logged_in = True

        elif logged_in and selected_cell is None and e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos
            if GRID_LEFT < x < GRID_LEFT + GRID_WIDTH and GRID_TOP < y < GRID_TOP + GRID_HEIGHT:
                col = (x - GRID_LEFT) // cell_width
                row = (y - GRID_TOP) // cell_height
                if (col, row) in timetable:
                    selected_cell = (col, row)
                    scroll_offset = 0
                    ox = (SCREEN_WIDTH - 600) // 2
                    oy = (SCREEN_HEIGHT - 560) // 2
                    input_box = InputBox(ox + 20, oy + 400, 560, 40, '이름:내용 또는 이름: YYYY-MM-DD HH:MM')
                    add_btn = pygame.Rect(ox + 20, oy + 440, 120, 40)

        elif selected_cell:
            input_box.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_event = e
                if current_tab != 0:
                    for btn, idx in delete_buttons:
                        if btn.collidepoint(e.pos):
                            if selected_cell in data_items and idx < len(data_items[selected_cell]):
                                del data_items[selected_cell][idx]
                                break
                    if add_btn.collidepoint(e.pos) and input_box.text:
                        text = input_box.text
                        try:
                            key, val = text.split(':', 1)
                            name, content = key.strip(), val.strip()
                            try:
                                dt = datetime.datetime.strptime(content, '%Y-%m-%d %H:%M')
                                item = ('alarm', dt, name)
                            except:
                                item = ('memo', name, content)
                            data_items.setdefault(selected_cell, []).append(item)
                        except ValueError:
                            pass
                        input_box.text = ''
                        input_box.txt_surf = font.render('', True, input_box.color)

    screen.fill(WHITE)
    if not logged_in:
        screen.blit(font.render('Login', True, BLACK), (360, 150))
        user_box.draw(screen)
        pass_box.draw(screen)
        pygame.draw.rect(screen, LIGHT_BLUE, login_btn)
        screen.blit(font.render('Login', True, BLACK), (login_btn.x + 20, login_btn.y + 5))
    else:
        colors = [(100,149,237), (173,216,230), (135,206,250), (30,144,255), (70,130,180), (0,191,255), (176,224,230)]
        for i, ((c, r), subj) in enumerate(timetable.items()):
            rct = pygame.Rect(GRID_LEFT + c * cell_width + 1, GRID_TOP + r * cell_height, cell_width - 2, cell_height)
            color = colors[i % len(colors)]
            pygame.draw.rect(screen, color, rct)
            adj_font = get_adjusted_font(subj, cell_width - 10)
            screen.blit(adj_font.render(subj, True, WHITE), (rct.x + 5, rct.y + 5))

        for j in range(len(TIMES)):
            y = GRID_TOP + j * cell_height
            pygame.draw.line(screen, BLACK, (GRID_LEFT, y), (GRID_LEFT + GRID_WIDTH, y), 2)
            screen.blit(font.render(TIMES[j], True, BLACK), (GRID_LEFT - 80, y - 10))

        for i in range(len(DAYS)):
            x = GRID_LEFT + i * cell_width
            pygame.draw.line(screen, BLACK, (x, GRID_TOP), (x, GRID_TOP + GRID_HEIGHT), 2)
            screen.blit(font.render(DAYS[i], True, BLACK), (x + cell_width // 2 - 20, GRID_TOP - 30))

        if selected_cell:
            draw_overlay(selected_cell, mouse_click_event)
            if current_tab != 0:
                input_box.draw(screen)
                pygame.draw.rect(screen, LIGHT_BLUE, add_btn)
                screen.blit(font.render('Add', True, BLACK), (add_btn.x + 30, add_btn.y + 5))

    pygame.display.flip()

pygame.key.stop_text_input()
pygame.quit()
sys.exit()
