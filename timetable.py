import pygame
import sys
import datetime
import json
import os

# Initialize Pygame
pygame.init()
pygame.key.start_text_input()  # Enable Unicode input

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_TOP, GRID_LEFT = 50, 100
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH - GRID_LEFT - 50, SCREEN_HEIGHT - GRID_TOP - 50
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
TIMES = ['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00']
DATA_FILE = 'timetable_data.json'

# Colors
WHITE, BLACK, GRAY = (255,255,255),(0,0,0),(200,200,200)
BLUE, LIGHT_BLUE, DARK_GRAY, RED = (100,149,237),(173,216,230),(50,50,50),(255,0,0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Timetable with Persistence")

# Font (Korean support)
font = pygame.font.SysFont('malgungothic',24)
small_font = pygame.font.SysFont('malgungothic',20)

# Calculate cell size
cell_width = GRID_WIDTH // len(DAYS)
cell_height = GRID_HEIGHT // len(TIMES)

# Sample timetable
timetable = {(i,i): subj for i,subj in enumerate(['Math','English','Science','History','Art'])}

# Credentials
VALID_USERS={'user1':'pass123','admin':'admin'}

# Load saved items
# Load saved items (수정됨)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)
        data_items = {}
        for k, vlist in raw.items():
            key = tuple(map(int, k.split(',')))
            fixed_list = []
            for item in vlist:
                if item[0] == 'alarm':
                    # 문자열 → datetime 객체로 변환
                    dt = datetime.datetime.strptime(item[1], '%Y-%m-%d %H:%M')
                    fixed_list.append(('alarm', dt, item[2]))
                else:
                    fixed_list.append(tuple(item))
            data_items[key] = fixed_list
else:
    data_items = {}


# InputBox for Unicode
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

# Save function
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


# Login boxes
user_box=InputBox(300,200,200,40,'아이디 입력')
pass_box=InputBox(300,250,200,40,'비밀번호',True)
login_btn=pygame.Rect(350,300,100,40)

# State
logged_in=False
selected_cell=None
input_box=None
add_btn=None
close_btn=None

running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            save_data()
            running=False
        # Login events
        if not logged_in:
            user_box.handle_event(e)
            pass_box.handle_event(e)
            if e.type==pygame.MOUSEBUTTONDOWN and login_btn.collidepoint(e.pos):
                if VALID_USERS.get(user_box.text)==pass_box.text:
                    logged_in=True
        # Select cell
        elif logged_in and selected_cell is None and e.type==pygame.MOUSEBUTTONDOWN:
            x,y=e.pos
            if GRID_LEFT<x<GRID_LEFT+GRID_WIDTH and GRID_TOP<y<GRID_TOP+GRID_HEIGHT:
                col=(x-GRID_LEFT)//cell_width
                row=(y-GRID_TOP)//cell_height
                if (col,row) in timetable:
                    selected_cell=(col,row)
                    ox=(SCREEN_WIDTH-600)//2; oy=(SCREEN_HEIGHT-560)//2
                    input_box=InputBox(ox+20,oy+400,560,40,'이름:내용 또는 이름: YYYY-MM-DD HH:MM')
                    add_btn=pygame.Rect(ox+20,oy+440,120,40)
                    close_btn=pygame.Rect(ox+240,oy+520,100,40)
        # Input overlay events
        elif selected_cell:
            input_box.handle_event(e)
            if e.type==pygame.MOUSEBUTTONDOWN:
                if add_btn.collidepoint(e.pos) and input_box.text:
                    text=input_box.text
                    try:
                        key,val=text.split(':',1)
                        name,content=key.strip(),val.strip()
                        try:
                            dt=datetime.datetime.strptime(content,'%Y-%m-%d %H:%M')
                            item=('alarm',dt,name)
                        except:
                            item=('memo',name,content)
                        data_items.setdefault(selected_cell,[]).append(item)
                    except ValueError:
                        pass
                    input_box.text=''
                    input_box.txt_surf=font.render('',True,input_box.color)
                if close_btn.collidepoint(e.pos):
                    selected_cell=None
    # Draw
    screen.fill(WHITE)
    if not logged_in:
        screen.blit(font.render('Login',True,BLACK),(360,150))
        user_box.draw(screen)
        pass_box.draw(screen)
        pygame.draw.rect(screen,LIGHT_BLUE,login_btn)
        screen.blit(font.render('Login',True,BLACK),(login_btn.x+20,login_btn.y+5))
    else:
        # Draw grid
        pygame.draw.rect(screen,GRAY,(GRID_LEFT,GRID_TOP,GRID_WIDTH,GRID_HEIGHT),2)
        for i,day in enumerate(DAYS):
            x=GRID_LEFT+i*cell_width
            pygame.draw.line(screen,GRAY,(x,GRID_TOP),(x,GRID_TOP+GRID_HEIGHT))
            screen.blit(font.render(day,True,BLACK),(x+cell_width//2-20,GRID_TOP-30))
        for j,time in enumerate(TIMES):
            y=GRID_TOP+j*cell_height
            pygame.draw.line(screen,GRAY,(GRID_LEFT,y),(GRID_LEFT+GRID_WIDTH,y))
            screen.blit(font.render(time,True,BLACK),(GRID_LEFT-80,y+cell_height//2-10))
        # Draw subjects
        for (c,r),subj in timetable.items():
            rct=pygame.Rect(GRID_LEFT+c*cell_width+1,GRID_TOP+r*cell_height+1,cell_width-2,cell_height-2)
            pygame.draw.rect(screen,BLUE,rct)
            screen.blit(font.render(subj,True,WHITE),(rct.x+5,rct.y+5))
        # Overlay
        if selected_cell:
            ox=(SCREEN_WIDTH-600)//2; oy=(SCREEN_HEIGHT-560)//2
            pygame.draw.rect(screen,DARK_GRAY,(ox,oy,600,560))
            screen.blit(font.render(f"Subject: {timetable[selected_cell]}",True,WHITE),(ox+20,oy+20))
            # Display items
            screen.blit(small_font.render('Items:',True,WHITE),(ox+20,oy+60))
            for idx,it in enumerate(data_items.get(selected_cell,[])):
                y=oy+80+idx*24
                if it[0]=='memo':
                    txt=f"- {it[1]}: {it[2]}"
                else:
                    txt=f"- {it[2]} @ {it[1].strftime('%Y-%m-%d %H:%M')}"
                screen.blit(small_font.render(txt,True,WHITE),(ox+40,y))
            # Input & buttons
            input_box.draw(screen)
            pygame.draw.rect(screen,LIGHT_BLUE,add_btn)
            screen.blit(font.render('Add',True,BLACK),(add_btn.x+30,add_btn.y+5))
            pygame.draw.rect(screen,LIGHT_BLUE,close_btn)
            screen.blit(font.render('Close',True,BLACK),(close_btn.x+10,close_btn.y+5))
    pygame.display.flip()

# Cleanup
pygame.key.stop_text_input()
pygame.quit()
sys.exit()