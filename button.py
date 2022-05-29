import pygame as pg


class Button:
    def __init__(self, screen, img, x, y, text="", font=None):
        self.screen = screen
        self.img = img
        self.large_img = pg.transform.scale(self.img, (int(self.img.get_width()*1.2), int(self.img.get_height()*1.2)))
        self.cur_img = self.img
        self.coord = (x, y)
        self.large_coord = (x - int(self.img.get_width()*0.1), y - int(self.img.get_height()*0.1))
        self.cur_coord = self.coord
        self.text = text
        self.font = font
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.dim = (self.img.get_width(), self.img.get_height())
        self.center = (self.dim[0]//2 + x, self.dim[1]//2 + y)
        self.clicked = False

    def update(self):
        self.screen.blit(self.cur_img, self.cur_coord)
        if self.font is not None:
            label = self.font.render(self.text, 1, (255, 255, 255))
            text_rect = label.get_rect(center=self.center)
            self.screen.blit(label, text_rect)
        pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pos):
                if not self.clicked:
                    self.clicked = True
                    return self.text
            else:
                self.clicked = False
        else:
            if self.rect.collidepoint(pos):
                self.cur_img = self.large_img
                self.cur_coord = self.large_coord
            else:
                self.cur_img = self.img
                self.cur_coord = self.coord
            self.clicked = False


