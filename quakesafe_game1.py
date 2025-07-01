# นำเข้าไลบรารี่ที่จำเป็น
import pygame  # ไลบรารี่สำหรับสร้างเกม
import sys     # ไลบรารี่สำหรับจัดการระบบ
import os      # ไลบรารี่สำหรับจัดการไฟล์และโฟลเดอร์
import math    # ไลบรารี่สำหรับคำนวณทางคณิตศาสตร์
import random   # ไลบรารี่สำหรับสุ่ม

# เริ่มต้น pygame
pygame.init()

# กำหนดค่าคงที่สำหรับขนาดหน้าจอและสี
SCREEN_WIDTH = 1024   # ความกว้างหน้าจอ
SCREEN_HEIGHT = 768   # ความสูงหน้าจอ
WHITE = (255, 255, 255)  # สีขาว
BLACK = (0, 0, 0)        # สีดำ
BLUE = (0, 100, 200)     # สีน้ำเงิน
GREEN = (0, 200, 0)      # สีเขียว
RED = (200, 0, 0)        # สีแดง
GRAY = (128, 128, 128)   # สีเทา
YELLOW = (255, 255, 0)   # สีเหลือง (เพิ่มสำหรับ stage ใหม่)
ORANGE = (255, 165, 0)   # สีส้ม (เพิ่มสำหรับ stage ใหม่)

class QuakeSafeGame:
    """คลาสหลักของเกม QuakeSafe - เกมแผ่นดินไหว...ใจต้องนิ่ง"""
    
    def __init__(self):
        """ฟังก์ชันเริ่มต้นเกม - กำหนดค่าเริ่มต้นทั้งหมด"""
        # สร้างหน้าจอเกม
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # กำหนดชื่อหน้าต่างเกม
        pygame.display.set_caption("QuakeSafe - เกมแผ่นดินไหว...ใจต้องนิ่ง")
        
        # กำหนดไอคอนหน้าต่าง
        try:
            icon = pygame.image.load("BGlogin/titlegame.jpg")  # โหลดรูปไอคอน
            icon = pygame.transform.scale(icon, (32, 32))     # ปรับขนาดเป็น 32x32 พิกเซล
            pygame.display.set_icon(icon)                     # ตั้งเป็นไอคอนหน้าต่าง
        except:
            pass  # หากโหลดไอคอนไม่ได้ ให้ข้ามไป
            
        # สร้างนาฬิกาสำหรับควบคุม FPS
        self.clock = pygame.time.Clock()
        
        # โหลดฟอนต์
        self.load_fonts()
        
        # กำหนดตัวแปรสถานะเกม
        self.current_scene = "login"    # ฉากปัจจุบัน (เริ่มที่หน้า login)
        self.stars = 0                  # จำนวนดาวที่เก็บได้
        self.stage = 1                  # ระดับปัจจุบัน
        self.exit_confirm = False       # สถานะการยืนยันออกจากเกม
        self.answered = False           # ป้องกันการเพิ่มดาวซ้ำ
        self.max_stars = 4              # จำนวนดาวสูงสุดที่เก็บได้ (จะเพิ่มเป็น 4 stage)
        self.last_answer_correct = False # เก็บผลการตอบล่าสุด
        
        # ระบบปลดล็อก stage (แบบ Angry Birds)
        self.unlocked_stages = [True, False, False, False]  # stage 1 ปลดล็อกแล้ว, อื่นๆ ยังล็อก
        self.stage_stars = [0, 0, 0, 0]  # ดาวที่ได้จากแต่ละ stage (0-1 ดาวต่อ stage)
        self.selected_stage = 1          # stage ที่เลือกจะเล่น
        
        # โหลดรูปภาพทั้งหมด
        self.load_images()
        
        # ตัวแปรสำหรับหน้าจอсั่น
        self.shake_intensity = 0
        self.shake_duration = 0
        self.stage3_shaken = False

    def load_fonts(self):
        """โหลดฟอนต์สำหรับแสดงข้อความภาษาไทย"""
        font_path = None
        # ลองโหลดฟอนต์ TH Sarabun PSK จากโฟลเดอร์ local ก่อน
        local_font_paths = [
            "font/TH Sarabun PSK V-1/THSarabun.ttf",           # ฟอนต์ปกติ
            "font/TH Sarabun PSK V-1/THSarabun Bold.ttf",      # ฟอนต์หนา (สำหรับหัวข้อ)
        ]
        
        # ตรวจสอบฟอนต์ local ก่อน
        for path in local_font_paths:
            if os.path.exists(path):  # ถ้าไฟล์ฟอนต์มีอยู่
                font_path = path
                break
        
        # ถ้าไม่มีฟอนต์ local ให้ลองฟอนต์ระบบ
        if font_path is None:  # ถ้ายังไม่เจอฟอนต์ที่ใช้ได้
            system_font_paths = [  # รายการฟอนต์ที่อาจมีในระบบ
                "C:/Windows/Fonts/thsarabunpsk.ttf",           # ฟอนต์ Windows - TH Sarabun PSK
                "C:/Windows/Fonts/thsarabunnew.ttf",           # ฟอนต์ Windows - TH Sarabun New
                "C:/Windows/Fonts/cordiaupc.ttf",              # ฟอนต์ Windows - Cordia UPC
                "C:/Windows/Fonts/angsanaupc.ttf",             # ฟอนต์ Windows - Angsana UPC
                "C:/Windows/Fonts/browallianew.ttf",           # ฟอนต์ Windows - Browallia New
                "C:/Windows/Fonts/tahoma.ttf",                 # ฟอนต์ Windows - Tahoma (รองรับไทย)
                "/usr/share/fonts/truetype/tahoma.ttf",        # ฟอนต์ Linux - Tahoma
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # ฟอนต์ Linux - DejaVu Sans
            ]
            for path in system_font_paths:  # วนลูปตรวจสอบทีละฟอนต์
                if os.path.exists(path):     # ถ้าไฟล์ฟอนต์มีอยู่ในระบบ
                    font_path = path         # เก็บ path ของฟอนต์ที่เจอ
                    break                    # หยุดการค้นหา (ใช้ฟอนต์แรกที่เจอ)
        
        # โหลดฟอนต์ด้วย path ที่เจอ
        if font_path:  # ถ้าเจอฟอนต์ที่ใช้ได้ (ไม่ว่าจะ local หรือ system)
            try:  # ลองโหลดฟอนต์ (อาจมีข้อผิดพลาด)
                # สร้างฟอนต์ขนาดต่างๆ จากไฟล์เดียวกัน
                self.font_large = pygame.font.Font(font_path, 44)   # ฟอนต์ใหญ่ 44px สำหรับหัวข้อ
                self.font_medium = pygame.font.Font(font_path, 32)  # ฟอนต์กลาง 32px สำหรับข้อความปกติ
                self.font_small = pygame.font.Font(font_path, 24)   # ฟอนต์เล็ก 24px สำหรับข้อความในปุ่ม
                
                # ลองโหลดฟอนต์หนาสำหรับหัวข้อ (ถ้ามี)
                bold_font_path = "font/TH Sarabun PSK V-1/THSarabun Bold.ttf"  # path ของฟอนต์หนา
                if os.path.exists(bold_font_path):  # ถ้ามีไฟล์ฟอนต์หนา
                    self.font_bold = pygame.font.Font(bold_font_path, 36)  # โหลดฟอนต์หนา 36px
                else:  # ถ้าไม่มีฟอนต์หนา
                    self.font_bold = self.font_large  # ใช้ฟอนต์ปกติขนาดใหญ่แทน
                    
                print(f"โหลดฟอนต์สำเร็จ: {font_path}")  # แจ้งผลสำเร็จ
            except Exception as e:  # ถ้าเกิดข้อผิดพลาดในการโหลด
                print(f"ข้อผิดพลาดในการโหลดฟอนต์ {font_path}: {e}")  # แจ้งข้อผิดพลาด
                self.load_fallback_fonts()  # เรียกใช้ฟอนต์สำรองแทน
        else:  # ถ้าไม่เจอฟอนต์ไฟล์เลย
            print("ไม่พบไฟล์ฟอนต์ที่เหมาะสม ใช้ฟอนต์ระบบ")  # แจ้งว่าจะใช้ฟอนต์ระบบ
            self.load_fallback_fonts()  # เรียกใช้ฟอนต์สำรองจากระบบ
    
    def load_fallback_fonts(self):
        """โหลดฟอนต์สำรองจากระบบถ้าโหลดไฟล์ฟอนต์ไม่ได้"""
        # รายการฟอนต์ที่จะลองใช้จากระบบ (เรียงตามความสวยงาม)
        font_names = ["TH SarabunPSK", "TH Sarabun New", "Cordia New", "Angsana New", "Browallia New", "tahoma"]
        
        for font_name in font_names:  # วนลูปลองทีละฟอนต์
            try:  # ลองโหลดฟอนต์จากระบบ (อาจไม่มีในระบบ)
                # สร้างฟอนต์ขนาดต่างๆ จากชื่อฟอนต์ระบบ
                self.font_large = pygame.font.SysFont(font_name, 44)        # ฟอนต์ใหญ่ 44px
                self.font_medium = pygame.font.SysFont(font_name, 32)       # ฟอนต์กลาง 32px
                self.font_small = pygame.font.SysFont(font_name, 24)        # ฟอนต์เล็ก 24px
                self.font_bold = pygame.font.SysFont(font_name, 36, bold=True)  # ฟอนต์หนา 36px
                print(f"โหลดฟอนต์ระบบสำเร็จ: {font_name}")  # แจ้งผลสำเร็จ
                return  # หยุดการค้นหา (ใช้ฟอนต์แรกที่โหลดได้)
            except:  # ถ้าฟอนต์นี้ไม่มีในระบบ
                continue  # ลองฟอนต์ถัดไป
        
        # ฟอนต์สำรองสุดท้าย (ถ้าไม่มีฟอนต์ไทยเลย)
        self.font_large = pygame.font.SysFont("arial", 44)              # Arial ใหญ่
        self.font_medium = pygame.font.SysFont("arial", 32)             # Arial กลาง
        self.font_small = pygame.font.SysFont("arial", 24)              # Arial เล็ก
        self.font_bold = pygame.font.SysFont("arial", 36, bold=True)    # Arial หนา
        print("ใช้ฟอนต์ Arial เป็นฟอนต์สำรองสุดท้าย")  # แจ้งว่าใช้ Arial

    def load_images(self):
        """โหลดรูปภาพทั้งหมดที่ใช้ในเกม"""
        # โหลดพื้นหลังหน้า login
        self.bg_login = pygame.image.load("BGlogin/titlegame.jpg")  # โหลดรูปพื้นหลังหลัก
        self.bg_login = pygame.transform.scale(self.bg_login, (SCREEN_WIDTH, SCREEN_HEIGHT))  # ปรับขนาดให้พอดีหน้าจอ
        self.bg_login_exit = pygame.image.load("BGlogin/titlewhenclickexit.jpg")  # โหลดพื้นหลังตอนจะออกจากเกม
        self.bg_login_exit = pygame.transform.scale(self.bg_login_exit, (SCREEN_WIDTH, SCREEN_HEIGHT))  # ปรับขนาดให้พอดีหน้าจอ
        
        # โหลดรูปปุ่มต่างๆ
        self.btn_play = pygame.image.load("BGlogin/playbutton.jpg")        # โหลดปุ่มเล่นเกม
        self.btn_exit = pygame.image.load("BGlogin/exitbuttontopleft.jpg") # โหลดปุ่มออกจากเกม
        self.btn_setting = pygame.image.load("BGlogin/settingbuttontopright.jpg")  # โหลดปุ่มตั้งค่า
        self.btn_profile = pygame.image.load("BGlogin/profiletopright.jpg")        # โหลดปุ่มโปรไฟล์
        
        # ปรับขนาดปุ่มให้เหมาะสม
        self.btn_play = pygame.transform.scale(self.btn_play, (200, 60))      # ปรับขนาดปุ่มเล่น เป็น 200x60 พิกเซล
        self.btn_exit = pygame.transform.scale(self.btn_exit, (80, 80))       # ปรับขนาดปุ่มออก เป็น 80x80 พิกเซล
        self.btn_setting = pygame.transform.scale(self.btn_setting, (80, 80)) # ปรับขนาดปุ่มตั้งค่า เป็น 80x80 พิกเซล
        self.btn_profile = pygame.transform.scale(self.btn_profile, (80, 80)) # ปรับขนาดปุ่มโปรไฟล์ เป็น 80x80 พิกเซล

    def draw_text(self, text, font, color, rect, center=True):
        """วาดข้อความในพื้นที่ที่กำหนด พร้อมการตัดบรรทัดอัตโนมัติ"""
        lines = self.wrap_text(text, font, rect.width)  # แบ่งข้อความเป็นหลายบรรทัดให้พอดีกับความกว้าง
        y = rect.y + (rect.height - len(lines)*font.get_linesize())//2  # คำนวณตำแหน่ง y เริ่มต้นให้อยู่กึ่งกลาง
        
        for line in lines:  # วนลูปวาดทีละบรรทัด
            surf = font.render(line, True, color)  # สร้างพื้นผิวข้อความจากบรรทัดนี้
            surf_rect = surf.get_rect()            # ได้ขนาดของข้อความที่สร้าง
            
            if center:  # ถ้าต้องการจัดข้อความกึ่งกลาง
                surf_rect.centerx = rect.centerx   # จัดให้อยู่กึ่งกลางแนวนอน
            else:       # ถ้าต้องการจัดข้อความชิดซ้าย
                surf_rect.x = rect.x               # จัดให้ชิดซ้าย
                
            surf_rect.y = y  # กำหนดตำแหน่ง y ของข้อความ
            self.screen.blit(surf, surf_rect)  # วาดข้อความลงบนหน้าจอ
            y += font.get_linesize()  # เลื่อนตำแหน่ง y ไปบรรทัดถัดไป

    def wrap_text(self, text, font, max_width):
        """แบ่งข้อความยาวๆ ให้พอดีกับความกว้างที่กำหนด"""
        words = text.split(' ')  # แยกข้อความออกเป็นคำๆ ด้วยช่องว่าง
        lines = []               # ลิสต์เก็บบรรทัดที่แบ่งแล้ว
        current = ''             # บรรทัดปัจจุบันที่กำลังสร้าง
        
        for word in words:  # วนลูปตรวจสอบทีละคำ
            test = current + (' ' if current else '') + word  # ลองรวมคำใหม่เข้ากับบรรทัดปัจจุบัน
            if font.size(test)[0] <= max_width:  # ถ้าความกว้างยังไม่เกินที่กำหนด
                current = test  # เก็บคำนี้ไว้ในบรรทัดปัจจุบัน
            else:  # ถ้าความกว้างเกินแล้ว
                if current:  # ถ้ามีข้อความในบรรทัดปัจจุบัน
                    lines.append(current)  # เก็บบรรทัดปัจจุบันลงในลิสต์
                current = word  # เริ่มบรรทัดใหม่ด้วยคำนี้
                
        if current:  # ถ้ายังมีข้อความในบรรทัดสุดท้าย
            lines.append(current)  # เก็บบรรทัดสุดท้าย
        return lines  # คืนค่าลิสต์ของบรรทัดทั้งหมด

    def login_screen(self):
        """แสดงหน้าจอ login หลักของเกม"""
        self.screen.blit(self.bg_login, (0, 0))  # วาดพื้นหลังที่ตำแหน่ง (0,0)
        
        # สร้างและวาดปุ่มเล่นเกม (อยู่กึ่งกลางล่าง)
        play_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 80)  # สร้างสี่เหลี่ยมปุ่มเล่น
        self.screen.blit(self.btn_play, play_rect)  # วาดปุ่มเล่นลงบนหน้าจอ
        
        # สร้างและวาดปุ่มออกจากเกม (มุมซ้ายบน)
        exit_rect = pygame.Rect(20, 20, 80, 60)  # สร้างสี่เหลี่ยมปุ่มออก
        self.screen.blit(self.btn_exit, exit_rect)  # วาดปุ่มออกลงบนหน้าจอ
        
        # สร้างและวาดปุ่มตั้งค่า (มุมขวาบน)
        settings_rect = pygame.Rect(SCREEN_WIDTH - 80, 20, 60, 60)  # สร้างสี่เหลี่ยมปุ่มตั้งค่า
        self.screen.blit(self.btn_setting, settings_rect)  # วาดปุ่มตั้งค่าลงบนหน้าจอ
        
        # สร้างและวาดปุ่มโปรไฟล์ (ข้างปุ่มตั้งค่า)
        profile_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 60, 60)  # สร้างสี่เหลี่ยมปุ่มโปรไฟล์
        self.screen.blit(self.btn_profile, profile_rect)  # วาดปุ่มโปรไฟล์ลงบนหน้าจอ
        
        return play_rect, exit_rect, settings_rect, profile_rect  # คืนค่าตำแหน่งปุ่มทั้งหมดเพื่อตรวจสอบการคลิก

    def settings_screen(self):
        """แสดงหน้าจอตั้งค่า"""
        self.screen.fill(WHITE)
        title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 50)
        self.draw_text("หน้าตั้งค่า", self.font_large, BLACK, title_rect)
        
        # Placeholder text
        info_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 100)
        self.draw_text("ตัวเลือกการตั้งค่าจะถูกเพิ่มที่นี่ในอนาคต", self.font_medium, BLACK, info_rect)

        # Back button
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60)
        pygame.draw.rect(self.screen, RED, back_rect, border_radius=15)
        self.draw_text("กลับ", self.font_medium, WHITE, back_rect)
        return back_rect

    def profile_screen(self):
        """แสดงหน้าจอโปรไฟล์"""
        self.screen.fill(WHITE)
        title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 50)
        self.draw_text("หน้าโปรไฟล์", self.font_large, BLACK, title_rect)

        # Placeholder text
        info_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 100)
        self.draw_text("สถิติผู้เล่นจะถูกเพิ่มที่นี่ในอนาคต", self.font_medium, BLACK, info_rect)

        # Back button
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60)
        pygame.draw.rect(self.screen, RED, back_rect, border_radius=15)
        self.draw_text("กลับ", self.font_medium, WHITE, back_rect)
        return back_rect

    def stage_select_screen(self):
        """หน้าเลือก stage แบบ Angry Birds - ดีไซน์สวยงาม"""
        # พื้นหลังไล่สีสวยงาม
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(30 + 100 * color_ratio)   # ไล่จากน้ำเงินเข้มไปอ่อน
            g = int(100 + 150 * color_ratio)
            b = int(200 + 55 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # หัวข้อสวยงาม
        title_bg = pygame.Rect(SCREEN_WIDTH//2 - 250, 20, 500, 80)
        pygame.draw.rect(self.screen, WHITE, title_bg, border_radius=20)
        pygame.draw.rect(self.screen, (255, 215, 0), title_bg, 6, border_radius=20)
        title_rect = pygame.Rect(0, 30, SCREEN_WIDTH, 60)
        self.draw_text("เลือกฉากที่ต้องการเล่น", self.font_large, (50, 100, 150), title_rect)
        
        # สร้างปุ่ม stage 4 ปุ่ม (2x2) ขนาดใหญ่ขึ้น
        stage_buttons = []
        button_size = 180  # ขนาดใหญ่ขึ้น
        spacing = 60       # ระยะห่างมากขึ้น
        start_x = (SCREEN_WIDTH - (2 * button_size + spacing)) // 2
        start_y = 140
        
        for i in range(4):  # 4 stages
            row = i // 2  # แถว (0 หรือ 1)
            col = i % 2   # คอลัมน์ (0 หรือ 1)
            
            x = start_x + col * (button_size + spacing)
            y = start_y + row * (button_size + 40)
            
            stage_rect = pygame.Rect(x, y, button_size, button_size)
            stage_num = i + 1
            
            # เช็คว่า stage นี้ปลดล็อกหรือยัง
            if self.unlocked_stages[i]:
                # ปลดล็อกแล้ว - ไล่สีสวยงาม
                pygame.draw.rect(self.screen, (100, 200, 100), stage_rect, border_radius=25)
                pygame.draw.rect(self.screen, WHITE, stage_rect, 6, border_radius=25)
                
                # แสดงหมายเลข stage ใหญ่
                stage_num_rect = pygame.Rect(x, y + 15, button_size, 50)
                self.draw_text(f"ฉากที่ {stage_num}", self.font_large, WHITE, stage_num_rect)
                
                # แสดงดาวแบบสวยงาม
                stars_earned = self.stage_stars[i]
                star_y = y + 80
                star_size = 20  # ขนาดใหญ่ขึ้นเพราะมีดาวเดียว
                
                # วาดดาวเดียวตรงกลาง (เปลี่ยนจาก 3 ดาวเป็น 1 ดาว)
                star_x = x + button_size // 2
                
                # วาดดาวรูปทรงเรขาคณิต
                star_points = []
                for j in range(10):
                    angle = j * math.pi / 5
                    if j % 2 == 0:
                        sx = star_x + star_size * math.cos(angle - math.pi/2)
                        sy = star_y + star_size * math.sin(angle - math.pi/2)
                    else:
                        sx = star_x + (star_size * 0.4) * math.cos(angle - math.pi/2)
                        sy = star_y + (star_size * 0.4) * math.sin(angle - math.pi/2)
                    star_points.append((int(sx), int(sy)))
                
                # ตรวจสอบว่ามีจุดเพียงพอสำหรับวาดดาว
                if len(star_points) >= 3:
                    if stars_earned > 0:
                        # ดาวที่ได้แล้ว - สีทองเจิดจ้า
                        pygame.draw.polygon(self.screen, (255, 215, 0), star_points)
                        pygame.draw.polygon(self.screen, (255, 140, 0), star_points, 2)
                        # เอฟเฟกต์เปล่งแสง
                        pygame.draw.circle(self.screen, (255, 255, 200, 100), (star_x, star_y), star_size + 8, 3)
                    else:
                        # ดาวที่ยังไม่ได้ - สีเทาอ่อน
                        pygame.draw.polygon(self.screen, (180, 180, 180), star_points)
                        pygame.draw.polygon(self.screen, (120, 120, 120), star_points, 2)
                
                # ข้อความสถานะ
                status_rect = pygame.Rect(x, y + 120, button_size, 30)
                if stars_earned > 0:
                    self.draw_text("ผ่านแล้ว", self.font_small, (255, 215, 0), status_rect)
                else:
                    self.draw_text("พร้อมเล่น", self.font_small, BLUE, status_rect)
                
            else:
                # ยังล็อกอยู่ - สีเทาและเอฟเฟกต์ล็อก
                pygame.draw.rect(self.screen, (120, 120, 120), stage_rect, border_radius=25)
                pygame.draw.rect(self.screen, (80, 80, 80), stage_rect, 6, border_radius=25)
                
                # ไอคอนล็อกใหญ่และสวยงาม
                lock_size = 40
                lock_x = x + button_size//2
                lock_y = y + button_size//2 - 10
                
                # วาดกุญแจ
                pygame.draw.circle(self.screen, (60, 60, 60), (lock_x, lock_y - 15), 25, 8)
                lock_body = pygame.Rect(lock_x - 20, lock_y - 5, 40, 30)
                pygame.draw.rect(self.screen, (60, 60, 60), lock_body, border_radius=8)
                
                # ข้อความล็อก
                lock_text_rect = pygame.Rect(x, y + 130, button_size, 30)
                self.draw_text("ล็อก", self.font_small, (60, 60, 60), lock_text_rect)
            
            stage_buttons.append((stage_rect, stage_num, self.unlocked_stages[i]))
        
        # ปุ่มกลับสวยงาม
        back_rect = pygame.Rect(50, SCREEN_HEIGHT - 80, 180, 60)
        pygame.draw.rect(self.screen, (200, 50, 50), back_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, back_rect, 4, border_radius=15)
        self.draw_text("กลับหน้าหลัก", self.font_medium, WHITE, back_rect)
        
        # แสดงสถิติรวม
        total_stars = sum(self.stage_stars)
        stats_rect = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 200, 60)
        pygame.draw.rect(self.screen, WHITE, stats_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 215, 0), stats_rect, 4, border_radius=15)
        self.draw_text(f"รวม: {total_stars}/4 ดาว", self.font_medium, (255, 140, 0), stats_rect)
        
        return stage_buttons, back_rect

    def draw_star_counter(self):
        """วาดตัวนับดาวพร้อมรูปดาวเรขาคณิตและข้อความภาษาไทย"""
        import math  # นำเข้าไลบรารี่คณิตศาสตร์สำหรับคำนวณมุม
        
        # สร้างพื้นหลังสำหรับตัวนับดาว
        star_bg_rect = pygame.Rect(30, 30, 200, 70)  # สร้างสี่เหลี่ยมพื้นหลัง ขนาด 200x70 ที่ตำแหน่ง (30,30)
        pygame.draw.rect(self.screen, WHITE, star_bg_rect, border_radius=25)  # วาดพื้นหลังสีขาวมุมโค้ง
        pygame.draw.rect(self.screen, (255, 215, 0), star_bg_rect, 3, border_radius=25)  # วาดขอบสีทองหนา 3 พิกเซล
        
        # กำหนดตำแหน่งและขนาดของรูปดาว
        star_center_x = 70  # จุดกึ่งกลางดาวแนวนอน
        star_center_y = 65  # จุดกึ่งกลางดาวแนวตั้ง
        star_size = 15      # ขนาดรัศมีของดาว
        
        # สร้างจุดของดาว 5 แฉก (ใช้ 10 จุด: 5 จุดนอก + 5 จุดใน)
        star_points = []  # ลิสต์เก็บจุดทั้งหมดของดาว
        for i in range(10):  # วนลูป 10 รอบสำหรับ 10 จุด
            angle = i * math.pi / 5  # คำนวณมุมของแต่ละจุด (36 องศาต่อจุด)
            if i % 2 == 0:  # จุดคู่ = จุดนอก (ปลายดาว)
                x = star_center_x + star_size * math.cos(angle - math.pi/2)  # คำนวณ x ของจุดนอก
                y = star_center_y + star_size * math.sin(angle - math.pi/2)  # คำนวณ y ของจุดนอก
            else:  # จุดคี่ = จุดใน (ร่องดาว)
                x = star_center_x + (star_size * 0.4) * math.cos(angle - math.pi/2)  # คำนวณ x ของจุดใน (เล็กกว่า 40%)
                y = star_center_y + (star_size * 0.4) * math.sin(angle - math.pi/2)  # คำนวณ y ของจุดใน
            star_points.append((int(x), int(y)))  # เก็บจุดลงในลิสต์ (แปลงเป็นจำนวนเต็ม)
        
        # วาดรูปดาว
        pygame.draw.polygon(self.screen, (255, 215, 0), star_points)  # วาดดาวสีทองเต็ม
        pygame.draw.polygon(self.screen, (255, 140, 0), star_points, 2)  # วาดขอบดาวสีส้มหนา 2 พิกเซล
        
        # วาดข้อความจำนวนดาวเป็นภาษาไทย
        if self.current_scene.startswith("stage"):
            stage_index = self.selected_stage - 1
            stage_stars = self.stage_stars[stage_index]
            star_text = f"ฉาก {self.selected_stage}: {stage_stars}/1"  # แสดงดาวของ stage ปัจจุบัน
        else:
            total_stars = sum(self.stage_stars)
            star_text = f"รวม: {total_stars} ดาว"  # แสดงดาวรวมทั้งหมด
        star_text_rect = pygame.Rect(110, 45, 100, 40)  # กำหนดพื้นที่สำหรับข้อความ
        self.draw_text(star_text, self.font_medium, (255, 140, 0), star_text_rect, center=False)  # วาดข้อความสีส้มชิดซ้าย

    def exit_confirmation_screen(self):
        """แสดงหน้าจอยืนยันการออกจากเกม"""
        # วาดพื้นหลังเดิม (ไม่ใช่พื้นหลังออกจากเกม)
        self.screen.blit(self.bg_login, (0, 0))  # ใช้พื้นหลัง login ปกติ
        
        # สร้างกล่องโต้ตอบกึ่งกลางหน้าจอ
        dialog_w, dialog_h = 400, 220  # กำหนดขนาดกล่องโต้ตอบ กว้าง 400 สูง 220
        dialog_rect = pygame.Rect((SCREEN_WIDTH-dialog_w)//2, (SCREEN_HEIGHT-dialog_h)//2, dialog_w, dialog_h)  # คำนวณตำแหน่งกึ่งกลาง
        pygame.draw.rect(self.screen, WHITE, dialog_rect, border_radius=16)  # วาดกล่องสีขาวมุมโค้ง
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 3, border_radius=16)  # วาดขอบสีดำหนา 3 พิกเซล
        
        # วาดข้อความถาม
        msg_rect = pygame.Rect(dialog_rect.x, dialog_rect.y+30, dialog_w, 40)  # กำหนดพื้นที่ข้อความ
        self.draw_text("ต้องการออกจากเกมหรือไม่?", self.font_medium, BLACK, msg_rect)  # วาดข้อความถาม
        
        # สร้างปุ่ม ใช่/ไม่ (สี่เหลี่ยม)
        yes_rect = pygame.Rect(dialog_rect.x+40, dialog_rect.y+120, 120, 60)  # ปุ่ม "ใช่" ทางซ้าย
        no_rect = pygame.Rect(dialog_rect.x+dialog_w-160, dialog_rect.y+120, 120, 60)  # ปุ่ม "ไม่" ทางขวา
        pygame.draw.rect(self.screen, GREEN, yes_rect, border_radius=8)  # วาดปุ่ม "ใช่" สีเขียว
        pygame.draw.rect(self.screen, RED, no_rect, border_radius=8)    # วาดปุ่ม "ไม่" สีแดง
        self.draw_text("ใช่", self.font_medium, WHITE, yes_rect)  # วาดข้อความ "ใช่" สีขาว
        self.draw_text("ไม่", self.font_medium, WHITE, no_rect)   # วาดข้อความ "ไม่" สีขาว
        
        # หมายเหตุสำหรับนักพัฒนา:
        # yes_rect: สี่เหลี่ยมสำหรับปุ่ม "ใช่" - สามารถแทนที่ด้วยรูปภาพได้ในอนาคต
        # no_rect:  สี่เหลี่ยมสำหรับปุ่ม "ไม่" - สามารถแทนที่ด้วยรูปภาพได้ในอนาคต
        return yes_rect, no_rect  # คืนค่าตำแหน่งปุ่มเพื่อตรวจสอบการคลิก

    def stage1_scene(self):
        """ฉากที่ 1: ตื่นนอนตอนเช้า - การรับรู้ข่าวสารเตือนภัย"""
        self.screen.fill((135, 206, 235))  # เติมพื้นหลังสีฟ้าอ่อน (สีท้องฟ้าตอนเช้า)
        
        # สร้างและวาดหัวข้อฉาก
        title_rect = pygame.Rect(0, 30, SCREEN_WIDTH, 50)  # กำหนดพื้นที่สำหรับหัวข้อ
        # ลองใช้ฟอนต์หนาสำหรับหัวข้อ (ถ้ามี)
        try:
            bold_font = pygame.font.Font(self.font_medium.get_name(), 28)  # ลองสร้างฟอนต์ขนาด 28
        except:
            bold_font = self.font_medium  # ถ้าไม่ได้ ใช้ฟอนต์ปกติ
        self.draw_text("ฉากที่ 1: ตื่นนอนตอนเช้า", bold_font, BLACK, title_rect)  # วาดหัวข้อ
        
        # วาดเรื่องราวของฉาก
        story = "คุณเพิ่งตื่นนอนในตอนเช้า มีข่าวเตือนภัยแผ่นดินไหวออกอากาศ คุณจะทำอย่างไร?"
        story_rect = pygame.Rect(100, 100, SCREEN_WIDTH-200, 80)  # กำหนดพื้นที่เรื่องราว (เว้นขอบ 100 พิกเซลซ้าย-ขวา)
        self.draw_text(story, self.font_medium, BLACK, story_rect)  # วาดเรื่องราว
        
        # สร้างปุ่มตัวเลือก
        choice_a_rect = pygame.Rect(150, 300, 320, 90)  # ปุ่มตัวเลือก A (ซ้าย)
        choice_b_rect = pygame.Rect(550, 300, 320, 90)  # ปุ่มตัวเลือก B (ขวา)
        pygame.draw.rect(self.screen, BLUE, choice_a_rect, border_radius=18)   # วาดปุ่ม A สีน้ำเงิน (ตัวเลือกที่ถูก)
        pygame.draw.rect(self.screen, GRAY, choice_b_rect, border_radius=18)   # วาดปุ่ม B สีเทา (ตัวเลือกที่ผิด)
        self.draw_text("A. เปิดข่าวฟังให้ละเอียด", self.font_small, WHITE, choice_a_rect)  # ข้อความตัวเลือก A
        self.draw_text("B. ไม่สนใจ ทำกิจวัตรปกติ", self.font_small, WHITE, choice_b_rect)  # ข้อความตัวเลือก B
        
        # แสดงตัวนับดาว
        self.draw_star_counter()  # เรียกฟังก์ชันวาดตัวนับดาว
        return choice_a_rect, choice_b_rect  # คืนค่าตำแหน่งปุ่มเพื่อตรวจสอบการคลิก

    def stage2_scene(self):
        self.screen.fill((255, 228, 196))
        title_rect = pygame.Rect(0, 30, SCREEN_WIDTH, 50)
        self.draw_text("ฉากที่ 2: ได้รับแจ้งเตือนแผ่นดินไหว", self.font_large, BLACK, title_rect)
        story = "คุณได้รับการแจ้งเตือนว่าจะมีแผ่นดินไหวในพื้นที่ของคุณภายใน 30 นาที คุณควรทำอย่างไร?"
        story_rect = pygame.Rect(100, 100, SCREEN_WIDTH-200, 80)
        self.draw_text(story, self.font_medium, BLACK, story_rect)
        # Choices
        choice_a_rect = pygame.Rect(150, 300, 320, 90)
        choice_b_rect = pygame.Rect(550, 300, 320, 90)
        pygame.draw.rect(self.screen, BLUE, choice_a_rect, border_radius=18)
        pygame.draw.rect(self.screen, GRAY, choice_b_rect, border_radius=18)
        self.draw_text("A. เตรียมกระเป๋าฉุกเฉิน", self.font_small, WHITE, choice_a_rect)
        self.draw_text("B. ออกจากบ้านทันที", self.font_small, WHITE, choice_b_rect)
        # Stars - Simple design that won't interfere with Thai text
        self.draw_star_counter()
        return choice_a_rect, choice_b_rect

    def stage3_scene(self):
        """ฉากที่ 3: แผ่นดินไหวเริ่มขึ้น - ต้องหลบภัยอย่างถูกต้อง"""
        self.screen.fill((255, 200, 200))  # สีแดงอ่อน แสดงความเร่งด่วน
        if not self.stage3_shaken:
            self.shake_duration = 180  # 3 seconds at 60 FPS
            self.shake_intensity = 10
            self.stage3_shaken = True
        
        # หัวข้อฉาก
        title_rect = pygame.Rect(0, 30, SCREEN_WIDTH, 50)
        self.draw_text("ฉากที่ 3: แผ่นดินไหวเริ่มขึ้น!", self.font_large, BLACK, title_rect)
        
        # เรื่องราว
        story = "แผ่นดินไหวเริ่มขึ้นแล้ว! บ้านเริ่มสั่นสะเทือน คุณต้องหลบภัยอย่างรวดเร็ว คุณจะทำอย่างไร?"
        story_rect = pygame.Rect(100, 100, SCREEN_WIDTH-200, 80)
        self.draw_text(story, self.font_medium, BLACK, story_rect)
        
        # ตัวเลือก
        choice_a_rect = pygame.Rect(150, 300, 320, 90)
        choice_b_rect = pygame.Rect(550, 300, 320, 90)
        pygame.draw.rect(self.screen, BLUE, choice_a_rect, border_radius=18)
        pygame.draw.rect(self.screen, GRAY, choice_b_rect, border_radius=18)
        self.draw_text("A. หลบใต้โต๊ะที่แข็งแรง", self.font_small, WHITE, choice_a_rect)
        self.draw_text("B. วิ่งออกจากบ้านทันที", self.font_small, WHITE, choice_b_rect)
        
        # แสดงตัวนับดาว
        self.draw_star_counter()
        return choice_a_rect, choice_b_rect

    def stage4_scene(self):
        """ฉากที่ 4: ช่วยเหลือสมาชิกในครอบครัว"""
        self.screen.fill((255, 220, 150))  # สีเหลืองอ่อน
        
        # หัวข้อฉาก
        title_rect = pygame.Rect(0, 30, SCREEN_WIDTH, 50)
        self.draw_text("ฉากที่ 4: ช่วยเหลือน้อง", self.font_large, BLACK, title_rect)
        
        # เรื่องราว
        story = "คุณเห็นน้องอยู่ในครัว เขากำลังตกใจและไม่รู้จะทำอย่างไร คุณจะช่วยเขาอย่างไร?"
        story_rect = pygame.Rect(100, 100, SCREEN_WIDTH-200, 80)
        self.draw_text(story, self.font_medium, BLACK, story_rect)
        
        # ตัวเลือก
        choice_a_rect = pygame.Rect(150, 300, 320, 90)
        choice_b_rect = pygame.Rect(550, 300, 320, 90)
        pygame.draw.rect(self.screen, BLUE, choice_a_rect, border_radius=18)
        pygame.draw.rect(self.screen, GRAY, choice_b_rect, border_radius=18)
        self.draw_text("A. พาน้องหลบใต้โต๊ะด้วยกัน", self.font_small, WHITE, choice_a_rect)
        self.draw_text("B. บอกให้น้องหนีคนเดียว", self.font_small, WHITE, choice_b_rect)
        
        # แสดงตัวนับดาว
        self.draw_star_counter()
        return choice_a_rect, choice_b_rect

    def show_result(self, correct, message):
        """แสดงผลการตอบและอัปเดตดาวของ stage"""
        self.screen.fill(WHITE)
        result_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 60)
        if correct:
            self.draw_text("ถูกต้อง! +1 ดาว", self.font_large, GREEN, result_rect)
            # เพิ่มดาวให้ stage ปัจจุบัน
            stage_index = self.selected_stage - 1
            if self.stage_stars[stage_index] < 1:  # สูงสุด 1 ดาวต่อ stage
                self.stage_stars[stage_index] = 1
        else:
            self.draw_text("ผิด! ลองใหม่", self.font_large, RED, result_rect)
        
        msg_rect = pygame.Rect(0, 300, SCREEN_WIDTH, 60)
        self.draw_text(message, self.font_medium, BLACK, msg_rect)
        
        # แสดงดาวของ stage นี้ (ย้ายตำแหน่งให้ไม่บังข้อความ)
        stage_index = self.selected_stage - 1
        star_rect = pygame.Rect(0, 450, SCREEN_WIDTH, 40)
        self.draw_text(f"ฉากที่ {self.selected_stage} - ดาว: {self.stage_stars[stage_index]}/1", self.font_medium, BLACK, star_rect)
        
        # ปรับตำแหน่งปุ่มให้ไม่ทับกับข้อความ
        button_y = 520
        
        cont_rect = pygame.Rect(SCREEN_WIDTH//2 - 75, button_y, 150, 50)
        pygame.draw.rect(self.screen, GREEN, cont_rect, border_radius=12)
        self.draw_text("ต่อไป", self.font_small, WHITE, cont_rect)
        
        # เพิ่มปุ่มเลือกฉากและเล่นใหม่
        select_rect = pygame.Rect(SCREEN_WIDTH//2 - 210, button_y, 140, 50)
        pygame.draw.rect(self.screen, BLUE, select_rect, border_radius=12)
        self.draw_text("เลือกฉาก", self.font_small, WHITE, select_rect)
        
        retry_rect = pygame.Rect(SCREEN_WIDTH//2 + 70, button_y, 140, 50)
        pygame.draw.rect(self.screen, GRAY, retry_rect, border_radius=12)
        self.draw_text("เล่นใหม่", self.font_small, WHITE, retry_rect)
        
        return cont_rect, select_rect, retry_rect

    def stage_complete_screen(self):
        """หน้าจอเมื่อจบ stage - ดีไซน์สวยงามแบบเกมระดับโลก"""
        # พื้นหลังไล่สีสวยงาม
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(255 * (1 - color_ratio * 0.3))  # ไล่จากทองเข้มไปอ่อน
            g = int(215 * (1 - color_ratio * 0.2))
            b = int(50 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        stage_index = self.selected_stage - 1
        stars_earned = self.stage_stars[stage_index]
        
        # ปลดล็อก stage ถัดไป (ถ้ามี)
        if self.selected_stage < 4 and stars_earned > 0:
            self.unlocked_stages[self.selected_stage] = True
        
        # กล่องหลักสวยงาม
        main_box = pygame.Rect(SCREEN_WIDTH//2 - 300, 100, 600, 500)
        pygame.draw.rect(self.screen, WHITE, main_box, border_radius=25)
        pygame.draw.rect(self.screen, (255, 215, 0), main_box, 8, border_radius=25)
        
        # หัวข้อใหญ่
        title_rect = pygame.Rect(main_box.x, main_box.y + 30, main_box.width, 60)
        if self.last_answer_correct:
            self.draw_text(f"ฉากที่ {self.selected_stage} เสร็จสิ้น!", self.font_large, (50, 150, 50), title_rect)
        else:
            self.draw_text(f"ฉากที่ {self.selected_stage} - ตอบผิด!", self.font_large, (200, 50, 50), title_rect)
        
        # แสดงดาวแบบสวยงาม
        star_display_y = main_box.y + 120
        star_title_rect = pygame.Rect(main_box.x, star_display_y, main_box.width, 40)
        self.draw_text("ผลการเล่น", self.font_medium, BLACK, star_title_rect)
        
        # วาดดาวใหญ่ๆ สวยงาม (เปลี่ยนเป็น 1 ดาว) - ย้ายลงมาเพิ่ม
        star_y = star_display_y + 80  # เพิ่มระยะห่างจากหัวข้อ
        star_size = 18  # ลดขนาดอีกหน่อย
        star_x = SCREEN_WIDTH//2  # ตรงกลาง
        
        # วาดดาว
        star_points = []
        for j in range(10):
            angle = j * math.pi / 5
            if j % 2 == 0:
                x = star_x + star_size * math.cos(angle - math.pi/2)
                y = star_y + star_size * math.sin(angle - math.pi/2)
            else:
                x = star_x + (star_size * 0.4) * math.cos(angle - math.pi/2)
                y = star_y + (star_size * 0.4) * math.sin(angle - math.pi/2)
            star_points.append((int(x), int(y)))
        
        if stars_earned > 0:
            # ดาวที่ได้ - สีทองเจิดจ้า
            pygame.draw.polygon(self.screen, (255, 215, 0), star_points)
            pygame.draw.polygon(self.screen, (255, 140, 0), star_points, 3)
            # เอฟเฟกต์เปล่งแสง
            pygame.draw.circle(self.screen, (255, 255, 200, 100), (star_x, star_y), star_size + 10, 3)
        else:
            # ดาวที่ยังไม่ได้ - สีเทา
            pygame.draw.polygon(self.screen, (150, 150, 150), star_points)
            pygame.draw.polygon(self.screen, (100, 100, 100), star_points, 3)
        
        # ข้อความคะแนน - ลดระยะห่างจากดาว
        score_rect = pygame.Rect(main_box.x, star_y + 50, main_box.width, 40)
        self.draw_text(f"ได้ {stars_earned} ดาว จาก 1 ดาว", self.font_medium, BLACK, score_rect)
        
        # ข้อความปลดล็อก (ถ้ามี)
        unlock_y = score_rect.y + 40
        if self.selected_stage < 4 and stars_earned > 0:
            unlock_rect = pygame.Rect(main_box.x, unlock_y, main_box.width, 40)
            self.draw_text(f"ปลดล็อกฉากที่ {self.selected_stage + 1} แล้ว!", self.font_medium, GREEN, unlock_rect)
            unlock_y += 40
        
        # ปุ่มสวยงาม - ให้อยู่ในกล่องหลักเสมอ
        # คำนวณตำแหน่งให้อยู่ด้านล่างของกล่อง
        button_y = main_box.y + main_box.height - 80  # 80 พิกเซลจากขอบล่างของกล่อง
        button_width = 120  # ลดขนาดลง
        button_height = 45  # ลดความสูง
        
        # คำนวณตำแหน่งปุ่ม
        if self.selected_stage < 4 and self.last_answer_correct:  # แสดงปุ่มถัดไปเฉพาะเมื่อตอบถูกและยังไม่ใช่ stage สุดท้าย
            # มี 3 ปุ่ม - จัดให้อยู่กึ่งกลางพอดี
            total_width = 3 * button_width + 2 * 20  # 3 ปุ่ม + ช่องว่าง 20 พิกเซล
            start_x = SCREEN_WIDTH//2 - total_width//2
            menu_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            retry_rect = pygame.Rect(start_x + button_width + 20, button_y, button_width, button_height)
            next_rect = pygame.Rect(start_x + 2 * (button_width + 20), button_y, button_width, button_height)
        else:
            # มี 2 ปุ่ม (ตอบผิด หรือ stage สุดท้าย)
            total_width = 2 * button_width + 20  # 2 ปุ่ม + ช่องว่าง
            start_x = SCREEN_WIDTH//2 - total_width//2
            menu_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            retry_rect = pygame.Rect(start_x + button_width + 20, button_y, button_width, button_height)
            next_rect = None
        
        # วาดปุ่มเลือกฉาก
        pygame.draw.rect(self.screen, (70, 130, 180), menu_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, menu_rect, 4, border_radius=15)
        self.draw_text("เลือกฉาก", self.font_small, WHITE, menu_rect)
        
        # วาดปุ่มเล่นใหม่
        pygame.draw.rect(self.screen, (255, 140, 0), retry_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, retry_rect, 4, border_radius=15)
        self.draw_text("เล่นใหม่", self.font_small, WHITE, retry_rect)
        
        # วาดปุ่มฉากถัดไป (ถ้ามี)
        if next_rect:
            pygame.draw.rect(self.screen, (50, 180, 50), next_rect, border_radius=15)
            pygame.draw.rect(self.screen, WHITE, next_rect, 4, border_radius=15)
            self.draw_text("ฉากถัดไป", self.font_small, WHITE, next_rect)
            return menu_rect, retry_rect, next_rect
        else:
            return menu_rect, retry_rect, None

    def game_complete(self):
        self.screen.fill((255, 215, 0))
        title_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 60)
        self.draw_text("ยินดีด้วย! คุณผ่านเกมแล้ว", self.font_large, BLACK, title_rect)
        score_rect = pygame.Rect(0, 300, SCREEN_WIDTH, 40)
        self.draw_text(f"คะแนนรวม: {self.stars} ดาว", self.font_medium, BLACK, score_rect)
        msg_rect = pygame.Rect(0, 350, SCREEN_WIDTH, 40)
        if self.stars >= 4:
            self.draw_text("คุณได้คะแนนเต็ม! เก่งมาก!", self.font_medium, GREEN, msg_rect)
        elif self.stars >= 3:
            self.draw_text("เก่งมาก! เกือบเต็มแล้ว!", self.font_medium, BLUE, msg_rect)
        elif self.stars >= 2:
            self.draw_text("ดีแล้ว! ลองเล่นใหม่เพื่อเก็บดาวให้ครบ!", self.font_medium, BLUE, msg_rect)
        else:
            self.draw_text("ลองเล่นใหม่เพื่อเก็บดาวให้ครบ!", self.font_medium, BLUE, msg_rect)
        restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 450, 200, 60)
        exit_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 530, 200, 60)
        pygame.draw.rect(self.screen, GREEN, restart_rect, border_radius=12)
        pygame.draw.rect(self.screen, RED, exit_rect, border_radius=12)
        self.draw_text("เล่นใหม่", self.font_small, WHITE, restart_rect)
        self.draw_text("ออกจากเกม", self.font_small, WHITE, exit_rect)
        return restart_rect, exit_rect

    def run(self):
        """ฟังก์ชันหลักของเกม - ลูปหลักที่ควบคุมการทำงานทั้งหมด"""
        running = True
        show_result_screen = False
        result_correct = False
        result_message = ""
        
        login_buttons = None
        stage_select_buttons = None
        exit_buttons = None
        stage_buttons = None
        result_button = None
        stage_complete_buttons = None
        complete_buttons = None
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.exit_confirm and exit_buttons:
                        yes_rect, no_rect = exit_buttons
                        if yes_rect.collidepoint(mouse_pos):
                            running = False
                        elif no_rect.collidepoint(mouse_pos):
                            self.exit_confirm = False
                            
                    elif self.current_scene == "login" and login_buttons:
                        play_rect, exit_rect, settings_rect, profile_rect = login_buttons
                        if play_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage_select"
                        elif exit_rect.collidepoint(mouse_pos):
                            self.exit_confirm = True
                            
                    elif self.current_scene == "stage_select" and stage_select_buttons:
                        stage_buttons_list, back_rect = stage_select_buttons
                        if back_rect.collidepoint(mouse_pos):
                            self.current_scene = "login"
                        else:
                            for stage_rect, stage_num, is_unlocked in stage_buttons_list:
                                if stage_rect.collidepoint(mouse_pos) and is_unlocked:
                                    self.selected_stage = stage_num
                                    self.current_scene = f"stage{stage_num}"
                                    self.answered = False
                                    if stage_num == 3:
                                        self.stage3_shaken = False
                                    break
                            
                    elif self.current_scene.startswith("stage") and self.current_scene != "stage_complete" and not show_result_screen and stage_buttons:
                        choice_a, choice_b = stage_buttons
                        if choice_a.collidepoint(mouse_pos) and not self.answered:
                            self.last_answer_correct = True
                            stage_index = self.selected_stage - 1
                            if self.stage_stars[stage_index] == 0:
                                self.stage_stars[stage_index] = 1
                            self.current_scene = "stage_complete"
                            self.answered = True
                        elif choice_b.collidepoint(mouse_pos) and not self.answered:
                            self.last_answer_correct = False
                            self.current_scene = "stage_complete"
                            self.answered = True
                            
                    elif self.current_scene == "stage_complete" and stage_complete_buttons:
                        menu_rect, retry_rect, next_rect = stage_complete_buttons
                        if next_rect and next_rect.collidepoint(mouse_pos):
                            self.selected_stage += 1
                            self.current_scene = f"stage{self.selected_stage}"
                            self.answered = False
                        elif menu_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage_select"
                        elif retry_rect.collidepoint(mouse_pos):
                            self.current_scene = f"stage{self.selected_stage}"
                            self.answered = False
                            if self.selected_stage == 3:
                                self.stage3_shaken = False
                                
                    elif self.current_scene == "complete" and complete_buttons:
                        restart_rect, exit_rect = complete_buttons
                        if restart_rect.collidepoint(mouse_pos):
                            self.stars = 0
                            self.current_scene = "login"
                        elif exit_rect.collidepoint(mouse_pos):
                            running = False
            
            # Screen Shake Logic
            screen_to_draw = self.screen
            if self.shake_duration > 0:
                self.shake_duration -= 1
                if self.shake_intensity > 0:
                    offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
                    offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
                    temp_surface = pygame.Surface(self.screen.get_size())
                    temp_surface.blit(self.screen, (offset_x, offset_y))
                    screen_to_draw = temp_surface

            if self.exit_confirm:
                exit_buttons = self.exit_confirmation_screen()
            elif self.current_scene == "login":
                login_buttons = self.login_screen()
            elif self.current_scene == "stage_select":
                stage_select_buttons = self.stage_select_screen()
            elif self.current_scene == "stage1" and not show_result_screen:
                stage_buttons = self.stage1_scene()
            elif self.current_scene == "stage2" and not show_result_screen:
                stage_buttons = self.stage2_scene()
            elif self.current_scene == "stage3" and not show_result_screen:
                stage_buttons = self.stage3_scene()
            elif self.current_scene == "stage4" and not show_result_screen:
                stage_buttons = self.stage4_scene()
            elif self.current_scene == "stage_complete":
                stage_complete_buttons = self.stage_complete_screen()
            elif self.current_scene == "complete":
                complete_buttons = self.game_complete()
                
            if self.shake_duration > 0:
                self.screen.blit(screen_to_draw, (0,0))

            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = QuakeSafeGame()
    game.run()