# เกมฝึกพิมพ์ - โครงสร้างเกมง่ายๆ พร้อมคำถามและตัวเลือก
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
        pygame.display.set_caption("เกมฝึกพิมพ์ - QuakeSafe")
        self.clock = pygame.time.Clock()
        self.current_scene = "menu"
        self.answered = False
        
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
        """โหลดรูปภาพพื้นหลัง"""
        try:
            # โหลดพื้นหลังจากโฟลเดอร์ BGlogin
            self.bg_login = pygame.image.load("BGlogin/titlegame.jpg")
            self.bg_login = pygame.transform.scale(self.bg_login, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print("โหลดพื้นหลังสำเร็จ")
        except:
            # ถ้าไม่มีรูป ใช้สีพื้นหลังแทน
            self.bg_login = None
            print("ไม่พบไฟล์พื้นหลัง ใช้สีพื้นหลังแทน")
        
    def draw_text(self, text, rect, color=BLACK, center=True):
        """วาดข้อความในพื้นที่ที่กำหนด"""
        text_surface = self.font_medium.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = rect.center
        else:
            text_rect.topleft = rect.topleft
            
        self.screen.blit(text_surface, text_rect)
        
    def main_menu(self):
        """หน้าเมนูหลัก"""
        # วาดพื้นหลัง
        if self.bg_login:
            self.screen.blit(self.bg_login, (0, 0))
        else:
            self.screen.fill((135, 206, 235))  # สีฟ้าอ่อน
        
        # หัวข้อเกม
        title_rect = pygame.Rect(0, 100, SCREEN_WIDTH, 80)
        title_surface = self.font_large.render("เกมแผ่นดินไหว - ฝึกพิมพ์", True, BLACK)
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, title_text_rect)
        
        # ปุ่มเล่นเกม
        play_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 60)
        pygame.draw.rect(self.screen, BLUE, play_rect, border_radius=15)
        play_text_rect = pygame.Rect(play_rect.x, play_rect.y, play_rect.width, play_rect.height)
        self.draw_text("เล่นเกม", play_text_rect, WHITE)
        
        # ปุ่มออกจากเกม
        quit_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 60)
        pygame.draw.rect(self.screen, RED, quit_rect, border_radius=15)
        quit_text_rect = pygame.Rect(quit_rect.x, quit_rect.y, quit_rect.width, quit_rect.height)
        self.draw_text("ออกจากเกม", quit_text_rect, WHITE)
        
        return play_rect, quit_rect
        
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
        
    def run(self):
        """ฟังก์ชันหลักของเกม - ลูปหลักที่ควบคุมการทำงานทั้งหมด"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.current_scene == "menu":
                        play_rect, quit_rect = self.main_menu()
                        if play_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage1"
                            self.answered = False
                        elif quit_rect.collidepoint(mouse_pos):
                            running = False
                            
                    elif self.current_scene == "stage1":
                        choice_a_rect, choice_b_rect, back_rect = self.stage1()
                        if choice_a_rect.collidepoint(mouse_pos) and not self.answered:
                            # ตัวเลือก A - คำตอบที่ถูก
                            self.current_scene = "result_correct"
                            self.answered = True
                        elif choice_b_rect.collidepoint(mouse_pos) and not self.answered:
                            # ตัวเลือก B - คำตอบที่ผิด
                            self.current_scene = "result_wrong"
                            self.answered = True
                        elif back_rect.collidepoint(mouse_pos):
                            self.current_scene = "menu"
                            
                    elif self.current_scene == "result_correct":
                        retry_rect, menu_rect = self.show_result(True)
                        if retry_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage1"
                            self.answered = False
                        elif menu_rect.collidepoint(mouse_pos):
                            self.current_scene = "menu"
                            
                    elif self.current_scene == "result_wrong":
                        retry_rect, menu_rect = self.show_result(False)
                        if retry_rect.collidepoint(mouse_pos):
                            self.current_scene = "stage1"
                            self.answered = False
                        elif menu_rect.collidepoint(mouse_pos):
                            self.current_scene = "menu"
            
            # วาดฉากปัจจุบัน
            if self.current_scene == "menu":
                self.main_menu()
            elif self.current_scene == "stage1":
                self.stage1()
            elif self.current_scene == "result_correct":
                self.show_result(True)
            elif self.current_scene == "result_wrong":
                self.show_result(False)
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SimpleGame()
    game.run()