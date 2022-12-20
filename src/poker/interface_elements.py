import pygame as pg
from pygame.locals import *

class InputBox:
    """class Input Box to modelize an entry text box"""
    def __init__(self, x, y, w = 200, h = 32, 
                 text='', textSize=None, textType = None,
                 color_active = 'black',
                 color_inactive = 'red',
                 centered=False):
        """
        initialization of an entry text box

        Parameters
        ----------
        x : int
            first coordinate pixel.
        y : int
            second coordinate pixel.
        w : int, optional
            wildth. The default is 200.
        h : int, optional
            height. The default is 32.
        text : string, optional
            initial text to show. The default is ''.
        textSize : int, optional
            size of the text, The default if the Box height
        textType : string, otional
            type of text, The default is system default
        color_active : string, optional
            color of the box if active. The default is 'black'.
        color_inactive : string, optional
            color of the box if inactive. The default is 'red'.
        centered : boolean, optional
            If True, the text is displayed in the center of the box. 
            The default is False.

        Returns
        -------
        None.

        """
        self.ow = w # save original width for update
        self.text = text
        self.COLOR_ACTIVE = pg.Color(color_active)
        self.COLOR_INACTIVE = pg.Color(color_inactive)
        self.color = self.COLOR_INACTIVE
        self.centered = centered
        self.FONT = pg.font.SysFont(textType, 
                                    size=h if textSize is None else textSize)
        self.rect = pg.Rect(x, y, w, h)
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    #self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self, screen, tickness = 2):
        text_w = self.txt_surface.get_width()
        # Resize the box if the text is too long.
        self.rect.w = max(self.ow, text_w +10)
        # Blit the text.
        if self.centered:
            screen.blit(self.txt_surface, 
                        (self.rect.x+(self.rect.w-text_w)//2, 
                         self.rect.y+5))
        else:
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, tickness)

class Button():
    # INITIALIZATION OF BUTTON COMPONENTS LIKE POSITION OF BUTTON,
    # COLOR OF BUTTON, FONT COLOR OF BUTTON, FONT SIZE, TEXT INSIDE THE BUTTON
    def __init__(self, x, y, sx, sy,
                 shape = 'rect',
                 colour_mouse_on = 'black', colour_mouse_off = 'red', 
                 textType = "TimeNewRoman", textColour = 'white', 
                 textSize = 25, text = "..."):
        """
        Generate button

        Parameters
        ----------
        x : int
            x origin.
        y : int
            y origin.
        sx : int
            width.
        sy : int
            height.
        shape : string, optional
            type shape of the button. Can rectangular (rect),
            or circular (circle). The default is 'rect'.
        colour_mouse_on : string, optional
            button colour when the mouse is on it. The default is 'black'.
        colour_mouse_off : string, optional
            button colour when the house is off it. The default is 'red'.
        textType : string, optional
            DESCRIPTION. The default is "TimeNewRoman".
        textColour : string, optional
            colour of the text. The default is 'white'.
        text : string, optional
            text displayed in the button. The default is "...".

        Returns
        -------
        None.

        """
        # origin coordinates :
        self.x = x
        self.y = y
        # last coordinates :
        self.sx = sx
        self.sy = sy
        # Colours possible deponding on mouse position :
        self.COLOR_INACTIVE = pg.Color(colour_mouse_off)
        self.COLOR_ACTIVE = pg.Color(colour_mouse_on)
        self.fbcolour = self.COLOR_INACTIVE #couleur actuelle
        # text :
        self.tcolour = pg.Color(textColour)
        self.text = text
        self.fontsize = textSize
        self.buttonf = pg.font.SysFont(textType, self.fontsize)
        # CURRENT IS OFF
        self.CurrentState = False
        # COLLIDER FOR THE CLICK CHECKING
        self.shape = shape 
        self.rect = pg.Rect(x, y, sx, sy)

 
    def handle_event(self, event):
        #change color if mouse on button : 
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.fbcolour=self.COLOR_ACTIVE
        else:
            self.fbcolour = self.COLOR_INACTIVE
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.CurrentState = True
            else:
                self.CurrentState = False
                
    # DRAW THE BUTTON
    def draw(self, display, tickness = 0):
        # RENDER THE FONT OBJECT FROM THE STSTEM FONTS
        textsurface = self.buttonf.render(self.text,
                                          False, self.tcolour)
 
        # THIS LINE WILL DRAW THE SURF ONTO THE SCREEN
        if self.shape == 'rect':
            pg.draw.rect(display, self.fbcolour, self.rect, tickness)
        elif self.shape == 'circle':
            pg.draw.ellipse(display, self.fbcolour,self.rect, tickness)
            
        display.blit(textsurface,
                 (self.x + (self.sx - textsurface.get_width())//2,
                  self.y + (self.sy - self.fontsize)//2))
 

class Player:
    def __init__(self, x, y, w, h, 
                 pseudo, isMe = False, isAI=False,
                 textType = "TimeNewRoman",
                 textSize = 25):
        
        #coordonnées :
        self.x, self.y, self.w, self.h = x,y,w,h
        
        #infos :
        self.pseudo = pseudo
        self.money = 0
        self.mise = 0
        
        #statut joueur
        self.isMe= isMe
        self.isAI = isAI
        self.isPlaying = False
        
        #creation des fonts d'affichage du pseudo et de l'argent :
        self.font_pseudo = pg.font.SysFont(textType, textSize)
        self.font_money = pg.font.SysFont(textType, textSize)
        
        self.color = pg.Color('black')
        
        #affichage des cartes :
        im = pg.image.load('cards/back.jpg')
        self.card_1 = pg.transform.scale(im, (100, 60))
        self.card_2 = pg.transform.scale(im, (100, 60))
            
        #creation des boutons si le joueur est moi:
        if isMe:
            call = Button(x,y,...,...)
            check = Button(x,y,...)
            fold = Button(x,y,...)
            raise_ = Button(x,y,...)
            bet = Button(x,y,...)
            #creation de l'entrée de mise :
            bet_entry = InputBox(x,y,...)
            self.myActions = [call,check,fold,raise_,[bet,bet_entry]]
        
            
            
    def draw(self, screen):
        self.show_pseudo.render(self.pseudo,False, self.color)
        screen.blit(self.card_1,(self.x,self.y))
        screen.blit(self.card_2,(self.x+20,self.y+20))
        
        if self.isMe and self.isPlaying:
            ### TODO : affichage des bons boutons ###
            pass
        
    def update_player_info(self, infos):
        #mise à jour des infos du joueur en fonction des infos du server
        for player in infos['players']:
            if player['pseudo'] == self.pseudo:
                self.money = player['money']
                self.mise = player['mise']
                self.isPlaying = player['isPlaying']
    
    def handle_event(self,event):
        ### TODO : gestion des actions sur les boutons et envoi des bonnes
        ### infos au server
        pass
        
