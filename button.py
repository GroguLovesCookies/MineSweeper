import pygame as pg


class Button:
    def __init__(self, screen, img, x, y, text="", font=None):
        self.screen = screen
        self.img = img
        self.coord = (x, y)
        self.text = text
        self.font = font
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.dim = (self.img.get_width(), self.img.get_height())
        self.center = (self.dim[0]//2 + x, self.dim[1]//2 + y)
        self.clicked = False

    def update(self):
        self.screen.blit(self.img, self.coord)
        if self.font is not None:
            label = self.font.render(self.text, 1, (255, 255, 255))
            text_rect = label.get_rect(center=self.center)
            self.screen.blit(label, text_rect)
        if pg.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if not self.clicked:
                    self.clicked = True
                    return self.text
            else:
                self.clicked = False
        else:
            self.clicked = False

