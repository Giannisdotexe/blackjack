import pygame

class Button:
    def __init__(self, surface, width, height, text,  bg, pos, textColor=(0, 0, 0), textSize=20, radius=0):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Consolas', textSize)
        self.text = self.font.render(text, True, textColor)
        self.btnsurf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect =  pygame.draw.rect(self.btnsurf, bg, (0, 0, width, height), border_radius=radius)
        self.btnsurf.blit(self.text, self.text.get_rect(center = self.rect.center))
        # self.btnsurf.blit(self.text, self.text.get_rect(center = self.btnsurf.get_rect().center))
        surface.blit(self.btnsurf, pos)
        self.rect.x, self.rect.y = pos
        self.clicked = False
        # could split up the init function to a draw function for more control (self.drawn in order to avoid false clicks)

    def click(self):
        action = False
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                action = True

        return action
    
    def clear(self, color):
        self.btnsurf.fill(color)
