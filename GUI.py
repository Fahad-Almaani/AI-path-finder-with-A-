import pygame
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
class Button:
    def __init__(self,x,y,width,height,color,text) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        
        self.color = color


    def draw(self,win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, black)
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(text, text_rect)

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # self.click_function()
                return True
        return False


