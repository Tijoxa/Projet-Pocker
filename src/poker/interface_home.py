import pygame as pg
from pygame.locals import *

from interface_elements import *
        
class GUI_homepage:
    def __init__(self):
        pg.init()
        #create the window :
        self.homepage = pg.display.set_mode([640, 480])
        pg.display.set_caption('Poker')
        
        #background :
        my_bg=pg.image.load('backgrounds/poker_background.jpg')
        self.bg = pg.transform.scale(my_bg, (640, 480))
        
        #create name entry box :
        self.input_name = InputBox(100, 400, 300, 32,'name',
                                   centered=True)
        
    def mainloop(self):
        clock = pg.time.Clock()
        input_box1 = self.input_name
        input_boxes = [input_box1]
        input_button1 = Button(200, 150, 125, 50, (255, 250, 250),
                     (255, 0, 0), "TimesNewRoman",
                     (255, 255, 255), "Jouer !")
        input_buttons = [input_button1]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)
                for button in input_buttons :
                    button.handle_event(event)

            self.homepage.blit(self.bg,(0,0))
            for box in input_boxes:
                box.draw(self.homepage)
            for button in input_buttons : 
                button.showButton(self.homepage)

            if input_button1.CurrentState:
                input_button1.CurrentState = False
                pg.quit()
                return "WAITING"

            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""