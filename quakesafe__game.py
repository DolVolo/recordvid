
import pygame
import sys
import os

# เริ่มต้น pygame
pygame.init()

# ตั้งค่าหน้าจอ
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (128, 128, 128)

class SimpleGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("QuakeSafe")
        self.clock = pygame.time.Clock()
        self.current_scene = "login"
        self.answered = False
        self.exit_confirm = False
        
        # ระบบดาว
        self.stars = 0
        self.stage_stars = [0]  # ดาวของ stage 1 (0-1 ดาว)
        self.last_answer_correct = False
        
        # โหลดฟอนต์สำหรับภาษาไทย
        self.load_fonts()
        
        # โหลดรูปภาพพื้นหลัง
        self.load_images()
        
    def load_fonts(self):
        """โหลดฟอนต์สำหรับแสดงข้อความภาษาไทย"""
        try:
            # ลองโหลดฟอนต์ไทยจากระบบ
            self.font_large = pygame.font.SysFont("tahoma", 36)
            self.font_medium = pygame.font.SysFont("tahoma", 28)
            self.font_small = pygame.font.SysFont("tahoma", 24)
            print("โหลดฟอนต์ Tahoma สำเร็จ")
        except:
            # ถ้าไม่ได้ ใช้ฟอนต์พื้นฐาน
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 28)
            self.font_small = pygame.font.Font(None, 24)
            print("ใช้ฟอนต์พื้นฐาน")
    
    def load_images(self):
        """โหลดรูปภาพพื้นหลังและปุ่มต่างๆ"""
        try:
            # โหลดพื้นหลังจากโฟลเดอร์ BGlogin
            self.bg_login = pygame.image.load("BGlogin/titlegame.jpg")
            self.bg_login = pygame.transform.scale(self.bg_login, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # โหลดรูปปุ่มต่างๆ
            self.btn_play = pygame.image.load("BGlogin/playbutton.jpg")
            self.btn_exit = pygame.image.load("BGlogin/exitbuttontopleft.jpg")
            self.btn_setting = pygame.image.load("BGlogin/settingbuttontopright.jpg")
            self.btn_profile = pygame.image.load("BGlogin/profiletopright.jpg")
            
            # ปรับขนาดปุ่มให้เหมาะสม
            self.btn_play = pygame.transform.scale(self.btn_play, (200, 60))
            self.btn_exit = pygame.transform.scale(self.btn_exit, (80, 80))
            self.btn_setting = pygame.transform.scale(self.btn_setting, (80, 80))
            self.btn_profile = pygame.transform.scale(self.btn_profile, (80, 80))
            
            print("โหลดรูปภาพสำเร็จ")
        except:
            # ถ้าไม่มีรูป ใช้สีพื้นหลังแทน
            self.bg_login = None
            self.btn_play = None
            self.btn_exit = None
            self.btn_setting = None
            self.btn_profile = None
            print("ไม่พบไฟล์รูปภาพ ใช้ปุ่มสีแทน")
        
    def draw_text(self, text, rect, color=BLACK, center=True):
        """วาดข้อความในพื้นที่ที่กำหนด"""
        text_surface = self.font_medium.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = rect.center
        else:
            text_rect.topleft = rect.topleft
            
        self.screen.blit(text_surface, text_rect)
    
    def draw_star_counter(self):
        """วาดตัวนับดาวพร้อมรูปดาวเรขาคณิตและข้อความภาษาไทย"""
        import math
        
        # สร้างพื้นหลังสำหรับตัวนับดาว
        star_bg_rect = pygame.Rect(30, 30, 200, 70)
        pygame.draw.rect(self.screen, WHITE, star_bg_rect, border_radius=25)
        pygame.draw.rect(self.screen, (255, 215, 0), star_bg_rect, 3, border_radius=25)
        
        # กำหนดตำแหน่งและขนาดของรูปดาว
        star_center_x = 70
        star_center_y = 65
        star_size = 15
        
        # สร้างจุดของดาว 5 แฉก
        star_points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                x = star_center_x + star_size * math.cos(angle - math.pi/2)
                y = star_center_y + star_size * math.sin(angle - math.pi/2)
            else:
                x = star_center_x + (star_size * 0.4) * math.cos(angle - math.pi/2)
                y = star_center_y + (star_size * 0.4) * math.sin(angle - math.pi/2)
            star_points.append((int(x), int(y)))
        
        # วาดรูปดาว
        pygame.draw.polygon(self.screen, (255, 215, 0), star_points)
        pygame.draw.polygon(self.screen, (255, 140, 0), star_points, 2)
        
        # วาดข้อความจำนวนดาว
        if self.current_scene == "stage1":
            stage_stars = self.stage_stars[0]
            star_text = f"ฉาก 1: {stage_stars}/1"
        else:
            total_stars = sum(self.stage_stars)
            star_text = f"รวม: {total_stars} ดาว"
        
        star_text_rect = pygame.Rect(110, 45, 100, 40)
        star_text_surface = self.font_medium.render(star_text, True, (255, 140, 0))
        self.screen.blit(star_text_surface, (star_text_rect.x, star_text_rect.y))
        
    def login_screen(self):
        """หน้าจอ login หลักของเกม"""
        # วาดพื้นหลัง
        if self.bg_login:
            self.screen.blit(self.bg_login, (0, 0))
        else:
            self.screen.fill((135, 206, 235))  # สีฟ้าอ่อน
        
        # สร้างและวาดปุ่มเล่นเกม (อยู่กึ่งกลางล่าง)
        play_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 80)
        if self.btn_play:
            self.screen.blit(self.btn_play, play_rect)
        else:
            pygame.draw.rect(self.screen, BLUE, play_rect, border_radius=15)
            self.draw_text("เล่นเกม", play_rect, WHITE)
        
        # สร้างและวาดปุ่มออกจากเกม (มุมซ้ายบน)
        exit_rect = pygame.Rect(20, 20, 80, 60)
        if self.btn_exit:
            self.screen.blit(self.btn_exit, exit_rect)
        else:
            pygame.draw.rect(self.screen, RED, exit_rect, border_radius=10)
            self.draw_text("ออก", exit_rect, WHITE)
        
        # สร้างและวาดปุ่มตั้งค่า (มุมขวาบน)
        settings_rect = pygame.Rect(SCREEN_WIDTH - 80, 20, 60, 60)
        if self.btn_setting:
            self.screen.blit(self.btn_setting, settings_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, settings_rect, border_radius=10)
            self.draw_text("ตั้งค่า", settings_rect, WHITE)
        
        # สร้างและวาดปุ่มโปรไฟล์ (ข้างปุ่มตั้งค่า)
        profile_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 60, 60)
        if self.btn_profile:
            self.screen.blit(self.btn_profile, profile_rect)
        else:
            pygame.draw.rect(self.screen, GREEN, profile_rect, border_radius=10)
            self.draw_text("โปรไฟล์", profile_rect, WHITE)
        
        return play_rect, exit_rect, settings_rect, profile_rect
    
    def exit_confirmation_screen(self):
        """แสดงหน้าจอยืนยันการออกจากเกม"""
        # วาดพื้นหลังเดิม
        if self.bg_login:
            self.screen.blit(self.bg_login, (0, 0))
        else:
            self.screen.fill((135, 206, 235))
        
        # สร้างโต้ตอบกึ่งกลางหน้าจอ
        dialog_w, dialog_h = 400, 220
        dialog_rect = pygame.Rect((SCREEN_WIDTH-dialog_w)//2, (SCREEN_HEIGHT-dialog_h)//2, dialog_w, dialog_h)
        pygame.draw.rect(self.screen, WHITE, dialog_rect, border_radius=16)
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 3, border_radius=16)
        
        # วาดข้อความถาม
        msg_rect = pygame.Rect(dialog_rect.x, dialog_rect.y+30, dialog_w, 40)
        msg_surface = self.font_medium.render("ต้องการออกจากเกมหรือไม่?", True, BLACK)
        msg_text_rect = msg_surface.get_rect(center=msg_rect.center)
        self.screen.blit(msg_surface, msg_text_rect)
        
        # สร้างปุ่ม ใช่/ไม่
        yes_rect = pygame.Rect(dialog_rect.x+40, dialog_rect.y+120, 120, 60)
        no_rect = pygame.Rect(dialog_rect.x+dialog_w-160, dialog_rect.y+120, 120, 60)
        pygame.draw.rect(self.screen, GREEN, yes_rect, border_radius=8)
        pygame.draw.rect(self.screen, RED, no_rect, border_radius=8)
        self.draw_text("ใช่", yes_rect, WHITE)
        self.draw_text("ไม่", no_rect, WHITE)
        
        return yes_rect, no_rect
    
    def stage_select_screen(self):
        """หน้าเลือก stage (มีเพียง 1 stage สำหรับการบันทึกสั้นๆ)"""
        # พื้นหลังไล่สีสวยงาม
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(30 + 100 * color_ratio)
            g = int(100 + 150 * color_ratio)
            b = int(200 + 55 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # หัวข้อสวยงาม
        title_bg = pygame.Rect(SCREEN_WIDTH//2 - 250, 20, 500, 80)
        pygame.draw.rect(self.screen, WHITE, title_bg, border_radius=20)
        pygame.draw.rect(self.screen, (255, 215, 0), title_bg, 6, border_radius=20)
        title_rect = pygame.Rect(0, 30, SCREEN_WIDTH, 60)
        title_surface = self.font_large.render("เลือกฉากที่ต้องการเล่น", True, (50, 100, 150))
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, title_text_rect)
        
        # สร้างปุ่ม stage 1 ปุ่มเดียว (สำหรับการบันทึกสั้นๆ)
        button_size = 200
        stage_rect = pygame.Rect(SCREEN_WIDTH//2 - button_size//2, 200, button_size, button_size)
        
        # วาดปุ่ม stage 1
        pygame.draw.rect(self.screen, (100, 200, 100), stage_rect, border_radius=25)
        pygame.draw.rect(self.screen, WHITE, stage_rect, 6, border_radius=25)
        
        # แสดงหมายเลข stage
        stage_num_rect = pygame.Rect(stage_rect.x, stage_rect.y + 15, button_size, 50)
        stage_surface = self.font_large.render("ฉากที่ 1", True, WHITE)
        stage_text_rect = stage_surface.get_rect(center=stage_num_rect.center)
        self.screen.blit(stage_surface, stage_text_rect)
        
        # แสดงดาวแบบสวยงาม
        import math
        stars_earned = self.stage_stars[0]
        star_y = stage_rect.y + 80
        star_size = 20
        star_x = stage_rect.x + button_size // 2
        
        # วาดดาวเดียวตรงกลาง
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
        status_rect = pygame.Rect(stage_rect.x, stage_rect.y + 120, button_size, 30)
        if stars_earned > 0:
            status_surface = self.font_small.render("ผ่านแล้ว", True, (255, 215, 0))
        else:
            status_surface = self.font_small.render("พร้อมเล่น", True, BLUE)
        status_text_rect = status_surface.get_rect(center=status_rect.center)
        self.screen.blit(status_surface, status_text_rect)
        
        # ปุ่มกลับสวยงาม
        back_rect = pygame.Rect(50, SCREEN_HEIGHT - 80, 180, 60)
        pygame.draw.rect(self.screen, (200, 50, 50), back_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, back_rect, 4, border_radius=15)
        self.draw_text("กลับหน้าหลัก", back_rect, WHITE)
        
        return stage_rect, back_rect
    
    def settings_screen(self):
        """แสดงหน้าจอตั้งค่า"""
        self.screen.fill(WHITE)
        title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 50)
        title_surface = self.font_large.render("หน้าตั้งค่า", True, BLACK)
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, title_text_rect)
        
        # ข้อความ placeholder
        info_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 100)
        info_surface = self.font_medium.render("ตัวเลือกการตั้งค่าจะถูกเพิ่มที่นี่ในอนาคต", True, BLACK)
        info_text_rect = info_surface.get_rect(center=info_rect.center)
        self.screen.blit(info_surface, info_text_rect)

        # ปุ่มกลับ
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60)
        pygame.draw.rect(self.screen, RED, back_rect, border_radius=15)
        self.draw_text("กลับ", back_rect, WHITE)
        return back_rect

    def profile_screen(self):
        """แสดงหน้าจอโปรไฟล์"""
        self.screen.fill(WHITE)
        title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 50)
        title_surface = self.font_large.render("หน้าโปรไฟล์", True, BLACK)
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, title_text_rect)

        # ข้อความ placeholder
        info_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 100)
        info_surface = self.font_medium.render("สถิติผู้เล่นจะถูกเพิ่มที่นี่ในอนาคต", True, BLACK)
        info_text_rect = info_surface.get_rect(center=info_rect.center)
        self.screen.blit(info_surface, info_text_rect)

        # ปุ่มกลับ
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 60)
        pygame.draw.rect(self.screen, RED, back_rect, border_radius=15)
        self.draw_text("กลับ", back_rect, WHITE)
        return back_rect
        
    def stage1(self):
        """ฉากที่ 1: คำถามเกี่ยวกับแผ่นดินไหว"""
        # พื้นหลังสีฟ้าอ่อน
        self.screen.fill((135, 206, 235))
        
        # หัวข้อฉาก
        title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 60)
        title_surface = self.font_large.render("ฉากที่ 1: ตื่นนอนตอนเช้า", True, BLACK)
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, title_text_rect)
        
        # เรื่องราว
        story_text = "คุณเพิ่งตื่นนอนในตอนเช้า มีข่าวเตือนภัยแผ่นดินไหวออกอากาศ"
        story_rect = pygame.Rect(100, 150, SCREEN_WIDTH-200, 40)
        story_surface = self.font_medium.render(story_text, True, BLACK)
        story_text_rect = story_surface.get_rect(center=story_rect.center)
        self.screen.blit(story_surface, story_text_rect)
        
        question_text = "คุณจะทำอย่างไร?"
        question_rect = pygame.Rect(100, 200, SCREEN_WIDTH-200, 40)
        question_surface = self.font_medium.render(question_text, True, BLACK)
        question_text_rect = question_surface.get_rect(center=question_rect.center)
        self.screen.blit(question_surface, question_text_rect)
        
        # ตัวเลือกคำตอบ
        choice_a_rect = pygame.Rect(150, 300, 320, 80)
        choice_b_rect = pygame.Rect(550, 300, 320, 80)
        
        # วาดปุ่มตัวเลือก A (คำตอบที่ถูก)
        pygame.draw.rect(self.screen, BLUE, choice_a_rect, border_radius=15)
        choice_a_text = "A. เปิดข่าวฟังให้ละเอียด"
        choice_a_surface = self.font_small.render(choice_a_text, True, WHITE)
        choice_a_text_rect = choice_a_surface.get_rect(center=choice_a_rect.center)
        self.screen.blit(choice_a_surface, choice_a_text_rect)
        
        # วาดปุ่มตัวเลือก B (คำตอบที่ผิด)
        pygame.draw.rect(self.screen, GRAY, choice_b_rect, border_radius=15)
        choice_b_text = "B. ไม่สนใจ ทำกิจวัตรปกติ"
        choice_b_surface = self.font_small.render(choice_b_text, True, WHITE)
        choice_b_text_rect = choice_b_surface.get_rect(center=choice_b_rect.center)
        self.screen.blit(choice_b_surface, choice_b_text_rect)
        
        # ปุ่มกลับ
        back_rect = pygame.Rect(50, SCREEN_HEIGHT - 80, 150, 50)
        pygame.draw.rect(self.screen, GREEN, back_rect, border_radius=10)
        back_text_rect = pygame.Rect(back_rect.x, back_rect.y, back_rect.width, back_rect.height)
        self.draw_text("กลับเมนู", back_text_rect, WHITE)
        
        # แสดงตัวนับดาว
        self.draw_star_counter()
        
        return choice_a_rect, choice_b_rect, back_rect
    
    def show_result(self, correct):
        """แสดงผลการตอบ"""
        self.screen.fill(WHITE)
        
        # แสดงผลการตอบ
        if correct:
            result_text = "ถูกต้อง! คุณตอบถูกแล้ว"
            result_color = GREEN
            message = "การรับฟังข่าวสารเตือนภัยเป็นสิ่งสำคัญ"
        else:
            result_text = "ผิด! ลองใหม่อีกครั้ง"
            result_color = RED
            message = "ควรรับฟังข่าวสารเตือนภัยอย่างใกล้ชิด"
        
        # วาดข้อความผลการตอบ
        result_rect = pygame.Rect(0, 200, SCREEN_WIDTH, 60)
        result_surface = self.font_large.render(result_text, True, result_color)
        result_text_rect = result_surface.get_rect(center=result_rect.center)
        self.screen.blit(result_surface, result_text_rect)
        
        # วาดข้อความอธิบาย
        message_rect = pygame.Rect(0, 300, SCREEN_WIDTH, 40)
        message_surface = self.font_medium.render(message, True, BLACK)
        message_text_rect = message_surface.get_rect(center=message_rect.center)
        self.screen.blit(message_surface, message_text_rect)
        
        # ปุ่มกลับไปเล่นใหม่
        retry_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 450, 200, 50)
        pygame.draw.rect(self.screen, BLUE, retry_rect, border_radius=10)
        retry_text_rect = pygame.Rect(retry_rect.x, retry_rect.y, retry_rect.width, retry_rect.height)
        self.draw_text("เล่นใหม่", retry_text_rect, WHITE)
        
        # ปุ่มกลับเมนู
        menu_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 520, 200, 50)
        pygame.draw.rect(self.screen, GREEN, menu_rect, border_radius=10)
        menu_text_rect = pygame.Rect(menu_rect.x, menu_rect.y, menu_rect.width, menu_rect.height)
        self.draw_text("กลับเมนู", menu_text_rect, WHITE)
        
        return retry_rect, menu_rect
    
    def stage_complete_screen(self):
        """หน้าจอเมื่อจบ stage - ดีไซน์สวยงามแบบเกมระดับโลก"""
        # พื้นหลังไล่สีสวยงาม
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(255 * (1 - color_ratio * 0.3))
            g = int(215 * (1 - color_ratio * 0.2))
            b = int(50 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        stars_earned = self.stage_stars[0]
        
        # กล่องหลักสวยงาม
        main_box = pygame.Rect(SCREEN_WIDTH//2 - 300, 100, 600, 500)
        pygame.draw.rect(self.screen, WHITE, main_box, border_radius=25)
        pygame.draw.rect(self.screen, (255, 215, 0), main_box, 8, border_radius=25)
        
        # หัวข้อใหญ่
        title_rect = pygame.Rect(main_box.x, main_box.y + 30, main_box.width, 60)
        if self.last_answer_correct:
            title_surface = self.font_large.render("ฉากที่ 1 เสร็จสิ้น!", True, (50, 150, 50))
        else:
            title_surface = self.font_large.render("ฉากที่ 1 - ตอบผิด!", True, (200, 50, 50))
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, title_text_rect)
        
        # แสดงดาวแบบสวยงาม
        star_display_y = main_box.y + 120
        star_title_rect = pygame.Rect(main_box.x, star_display_y, main_box.width, 40)
        star_title_surface = self.font_medium.render("ผลการเล่น", True, BLACK)
        star_title_text_rect = star_title_surface.get_rect(center=star_title_rect.center)
        self.screen.blit(star_title_surface, star_title_text_rect)
        
        # วาดดาวใหญ่ๆ สวยงาม
        import math
        star_y = star_display_y + 80
        star_size = 18
        star_x = SCREEN_WIDTH//2
        
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
        
        # ข้อความคะแนน
        score_rect = pygame.Rect(main_box.x, star_y + 50, main_box.width, 40)
        score_surface = self.font_medium.render(f"ได้ {stars_earned} ดาว จาก 1 ดาว", True, BLACK)
        score_text_rect = score_surface.get_rect(center=score_rect.center)
        self.screen.blit(score_surface, score_text_rect)
        
        # ปุ่มสวยงาม
        button_y = main_box.y + main_box.height - 80
        button_width = 120
        button_height = 45
        
        # มี 2 ปุ่ม
        total_width = 2 * button_width + 20
        start_x = SCREEN_WIDTH//2 - total_width//2
        menu_rect = pygame.Rect(start_x, button_y, button_width, button_height)
        retry_rect = pygame.Rect(start_x + button_width + 20, button_y, button_width, button_height)
        
        # วาดปุ่มเลือกฉาก
        pygame.draw.rect(self.screen, (70, 130, 180), menu_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, menu_rect, 4, border_radius=15)
        self.draw_text("เลือกฉาก", menu_rect, WHITE)
        
        # วาดปุ่มเล่นใหม่
        pygame.draw.rect(self.screen, (255, 140, 0), retry_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, retry_rect, 4, border_radius=15)
        self.draw_text("เล่นใหม่", retry_rect, WHITE)
        
        return menu_rect, retry_rect
        
    def run(self):
        """ฟังก์ชันหลักของเกม - ลูปหลักที่ควบคุมการทำงานทั้งหมด"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.exit_confirm:
                        yes_rect, no_rect = self.exit_confirmation_screen()
                        if yes_rect.collidepoint(mouse_pos):
                            running = False
                        elif no_rect.collidepoint(mouse_pos):
                            self.exit_confirm = False
                            
                    elif self.current_scene == "login":
                        play_rect, exit_rect, settings_rect, profile_rect = self.login_screen()
                        if play_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage_select"
                        elif exit_rect.collidepoint(mouse_pos):
                            self.exit_confirm = True
                        elif settings_rect.collidepoint(mouse_pos):
                            self.current_scene = "settings"
                        elif profile_rect.collidepoint(mouse_pos):
                            self.current_scene = "profile"
                            
                    elif self.current_scene == "stage_select":
                        stage_rect, back_rect = self.stage_select_screen()
                        if stage_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage1"
                            self.answered = False
                        elif back_rect.collidepoint(mouse_pos):
                            self.current_scene = "login"
                            
                    elif self.current_scene == "settings":
                        back_rect = self.settings_screen()
                        if back_rect.collidepoint(mouse_pos):
                            self.current_scene = "login"
                            
                    elif self.current_scene == "profile":
                        back_rect = self.profile_screen()
                        if back_rect.collidepoint(mouse_pos):
                            self.current_scene = "login"
                            
                    elif self.current_scene == "stage1":
                        choice_a_rect, choice_b_rect, back_rect = self.stage1()
                        if choice_a_rect.collidepoint(mouse_pos) and not self.answered:
                            # ตัวเลือก A - คำตอบที่ถูก
                            self.last_answer_correct = True
                            if self.stage_stars[0] == 0:  # ยังไม่ได้ดาว
                                self.stage_stars[0] = 1  # ได้ดาว 1 ดาว
                            self.current_scene = "stage_complete"
                            self.answered = True
                        elif choice_b_rect.collidepoint(mouse_pos) and not self.answered:
                            # ตัวเลือก B - คำตอบที่ผิด
                            self.last_answer_correct = False
                            self.current_scene = "stage_complete"
                            self.answered = True
                        elif back_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage_select"
                            
                    elif self.current_scene == "stage_complete":
                        menu_rect, retry_rect = self.stage_complete_screen()
                        if menu_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage_select"
                        elif retry_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage1"
                            self.answered = False
            
            # วาดฉากปัจจุบัน
            if self.exit_confirm:
                self.exit_confirmation_screen()
            elif self.current_scene == "login":
                self.login_screen()
            elif self.current_scene == "stage_select":
                self.stage_select_screen()
            elif self.current_scene == "settings":
                self.settings_screen()
            elif self.current_scene == "profile":
                self.profile_screen()
            elif self.current_scene == "stage1":
                self.stage1()
            elif self.current_scene == "stage_complete":
                self.stage_complete_screen()
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SimpleGame()
    game.run()