import numpy as np
from math import sin,cos,radians
import random
import pygame as game
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT OBJECT LOADER
from objloader import *

playing = True

class balok():
    xKiri = -1
    yBawah = -1
    zBelakang = -1
    r=0
    g=0
    b=0

    def __init__(self, x, y, z,r,g,b, ukX=8, ukZ=8):
        self.xKiri = x
        self.yBawah = y
        self.zBelakang = z
        self.r=r
        self.g=g
        self.b=b
        self.ukZ = ukZ
        self.ukX = ukX

    def draw(self):
        xKiri = self.xKiri
        yBawah = self.yBawah
        zBelakang = self.zBelakang
        glBegin(GL_QUADS)
        glColor3f(self.r, self.g, self.b)
        glVertex3f(xKiri,yBawah,zBelakang)
        glVertex3f(xKiri,yBawah,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah,zBelakang)

        glColor3f(min(self.r+0.2, 1.0),min(self.g+0.2, 1.0),min(self.b+0.2,1.0))
        glVertex3f(xKiri,yBawah+2,zBelakang)
        glVertex3f(xKiri,yBawah+2,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah+2,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah+2,zBelakang)
        
        glColor3f(min(self.r+0.25, 1.0),min(self.g+0.25, 1.0),min(self.b+0.25, 1.0))
        glVertex3f(xKiri,yBawah+2,zBelakang)
        glVertex3f(xKiri,yBawah+2,zBelakang+self.ukZ)
        glVertex3f(xKiri,yBawah,zBelakang+self.ukZ)
        glVertex3f(xKiri,yBawah,zBelakang)

        glColor3f(self.r,self.g,self.b)
        glVertex3f(xKiri+self.ukX,yBawah,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah,zBelakang)
        glVertex3f(xKiri+self.ukX,yBawah+2,zBelakang)
        glVertex3f(xKiri+self.ukX,yBawah+2,zBelakang+self.ukZ)

        glColor3f(self.r, self.g, self.b)
        glVertex3f(xKiri,yBawah+2,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah+2,zBelakang+self.ukZ)
        glVertex3f(xKiri+self.ukX,yBawah,zBelakang+self.ukZ)
        glVertex3f(xKiri,yBawah,zBelakang+self.ukZ)

        glColor3f(self.r, self.g, self.b)
        glVertex3f(xKiri,yBawah+2,zBelakang)
        glVertex3f(xKiri+self.ukX,yBawah+2,zBelakang)
        glVertex3f(xKiri+self.ukX,yBawah,zBelakang)
        glVertex3f(xKiri,yBawah,zBelakang)
        glEnd()
#Text object
def text_objects(text, font):
    black = (0,0,0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#penulisan score
def drawText(text):
    font = pygame.font.SysFont("consolas", 72)
    textSurface = font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(0+(textSurface.get_width()/40), 20, 0)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, textData)
		
# ini pengecekan kapan kalah
def nubruk(A, B):
    return not(
        ((A.xKiri + A.ukX) < B.xKiri) or (A.xKiri > (B.xKiri+B.ukX))
        or
        ((A.zBelakang + A.ukZ) < B.zBelakang) or (A.zBelakang > (B.zBelakang+B.ukZ)) 
        )

def buatBalok(gerak, diem):
    left = diem.xKiri
    right = diem.xKiri+diem.ukX
    back = diem.zBelakang
    front = diem.zBelakang+diem.ukZ
    if (gerak.xKiri>=left and gerak.xKiri<=right):
        left = gerak.xKiri
    if (gerak.xKiri+gerak.ukX>=left and gerak.xKiri+gerak.ukX<=right):
        right = gerak.xKiri+gerak.ukX

    if (gerak.zBelakang>=back and gerak.zBelakang<=front):
        back = gerak.zBelakang
    if (gerak.zBelakang+gerak.ukZ>back and gerak.zBelakang+gerak.ukZ<front):
        front = gerak.zBelakang+gerak.ukZ
    ukX = right-left
    ukZ = front-back
    return balok(left, gerak.yBawah, back, gerak.r, gerak.g, gerak.b, ukX, ukZ)

def main():
    poin = 0
    color_r = random.randint(0,100)/100
    color_g = random.randint(0,100)/100
    color_b = random.randint(0,100)/100
    #untuk pertambahan warna
    add_r= random.randint(1,10)/100
    add_g= random.randint(1,10)/100
    add_b= random.randint(1,10)/100
    

    game.init()
    display = (600, 800)
    game.display.set_mode(display, game.DOUBLEBUF|game.OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0]/display[1]), 0.1, 500)
    #         xyz camera, xyz lookat, 010
    gluLookAt(0, 10, -50, 0,10,0,   0,1,0)
	
    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
	
    arr = []
    arr.append(balok(-3,0,-2,color_r,color_g,color_b))
    running = True
    kalah = False
    turun = False
    ctr_geser=0.3
    tanda=0

    temp = balok(-3,2,-2, color_r,color_g,color_b)
    batasBelakang = temp.zBelakang-temp.ukZ-2
    batasDepan = temp.zBelakang+temp.ukZ+2
    batasKiri = temp.xKiri-temp.ukX-2
    batasKanan = temp.xKiri+temp.ukX+2
    CHEAT=False
    y = 0
	
	#call object
    world=World("background.obj", swapyz=True)
    rx, ry = (273,0)
    tx, ty = (10,0)
    zpos = 17
    game.display.set_caption("STACK")
	
    while running:
        #update score
        drawText(str(poin))

        rx += 0.1
        ry += 0.1
        glPushMatrix()
        glRotatef(30,-1,0,0)
        glRotatef(45,0,-1,0)
        glTranslatef(0, y, 0)
        temp.draw()
        glPopMatrix()
        if (not CHEAT):
            if(tanda%2==0):
                if( temp.zBelakang>=batasDepan or temp.zBelakang<=batasBelakang ):
                    ctr_geser = ctr_geser*-1
                temp.zBelakang=temp.zBelakang+ctr_geser
            else:
                if( temp.xKiri>=batasKanan or  temp.xKiri<=batasKiri):
                    ctr_geser = ctr_geser*-1
                temp.xKiri=temp.xKiri+ctr_geser
        for obj in arr:
            glPushMatrix()
            glRotatef(30,-1,0,0)
            glRotatef(45,0,-1,0)
            glTranslatef(0, y, 0)
            obj.draw()
            glPopMatrix()
        game.time.wait(20)
        game.display.flip()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#RENDER OBJECT
        glPushMatrix()
        glTranslate(tx/20., ty/20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glCallList(world.gl_list)
        glPopMatrix()
        for event in game.event.get():
            if (event.type == game.QUIT):
                running = False
                game.quit()
            elif event.type == game.KEYDOWN:
                if event.key == game.K_w:
                    temp.zBelakang = temp.zBelakang +1
                elif event.key == game.K_s:
                    temp.zBelakang = temp.zBelakang -1
                elif event.key == game.K_a:
                    temp.xKiri = temp.xKiri +1
                elif event.key == game.K_d:
                    temp.xKiri = temp.xKiri -1
                elif event.key == game.K_RETURN:
                    # cycle arah pergerak pertama
                    tanda += 1
                    ctr_geser = ctr_geser*-1 if (tanda%4==0) else ctr_geser
                    tanda %= 4

                    masuk = False
                    # kalah apa ndak dicek disini
                    if (nubruk(temp, arr[-1])):
                        masuk = True

                    # menentukan xyz balok yang ditaruh

                    balokBaru = buatBalok(temp, arr[-1])
                    #untuk warna
                    if(color_r + add_r>1):
                        color_r = 1.00
                        add_r =-1*random.randint(1,5)/100
                    elif (color_r + add_r<0 ):
                        color_r = 0.00
                        add_r =random.randint(1,5)/100
                    else:
                        color_r += add_r

                    if(color_g + add_g>1):
                        color_g = 1.00
                        add_g =-1*random.randint(1,5)/100
                    elif (color_g + add_r<0 ):
                        color_g = 0.00
                        add_g =random.randint(1,5)/100
                    else:
                        color_g += add_g

                    if(color_b + add_b>1):
                        color_b = 1.00
                        add_b =-1 *random.randint(1,5)/100
                    elif (color_b + add_b<=0):
                        color_b = 0.00
                        add_b = random.randint(1,5)/100
                    else:
                        color_b += add_b
                    
                    #------
                    if (masuk):
                        arr.append(balokBaru)
                        temp = balok(balokBaru.xKiri, balokBaru.yBawah+2, balokBaru.zBelakang,color_r,color_g,color_b, balokBaru.ukX, balokBaru.ukZ)
                        batasBelakang = temp.zBelakang-temp.ukZ-2
                        batasDepan = temp.zBelakang+temp.ukZ+2
                        batasKiri = temp.xKiri-temp.ukX-2
                        batasKanan = temp.xKiri+temp.ukX+2
                        poin += 10
                    else:
                        kalah = True
                    if temp.yBawah >= 10:
                        temp.yBawah-=2
                        for i in arr:
                            i.yBawah-=2
                elif event.key == game.K_SPACE:
                    CHEAT = not CHEAT
                    if CHEAT:
                        game.key.set_repeat(10, 100)
                    else:
                        game.key.set_repeat()
                elif event.key == game.K_t:
                    y+=1
                elif event.key == game.K_g:
                    y-=1
                    
        if (kalah):
            CHEAT = True
            print(y, arr[0].yBawah)
            if y+arr[0].yBawah !=0:
                y+=1
            else:
                running = False
                            
    print('POIN', poin)
    gameOver = True
    while gameOver:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                gameOver = False
        white = (255,255,255)
        screen = pygame.display.set_mode([600,800])
        screen.fill(white)
        #TITLE GAMEOVER
        largeText = pygame.font.Font('freesansbold.ttf',80)
        TextSurf, TextRect = text_objects("GAME OVER", largeText)
        TextRect.center = (300,400)
        screen.blit(TextSurf, TextRect)
        #SCORE TEXT
        txtScore = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects("Score : "+str(poin), txtScore)
        TextRect.center = (300,460)
        screen.blit(TextSurf, TextRect)
        

        #MOUSE EVENT
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        hoverRetry = (0,255,0)
        defColorRetry = (0,230,0)
        hoverExit = (255,77,77)
        defColorExit = (255,0,0)
        #BUTTON RETRY
        if 250+100 > mouse[0] > 250 and 500+50 > mouse[1] > 500:
            pygame.draw.rect(screen, hoverRetry,(250,500,100,50))
            if click[0] == 1:
                gameOver = False
        else:
            pygame.draw.rect(screen, defColorRetry,(250,500,100,50))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Retry", smallText)
        textRect.center = ( 300, (500+(50/2)) )
        screen.blit(textSurf, textRect)

        #BUTTON EXIT
        if 250+100 > mouse[0] > 250 and 560+50 > mouse[1] > 560:
            pygame.draw.rect(screen, hoverExit,(250,560,100,50))
            if click[0] == 1:
                game.quit()
        else:
            pygame.draw.rect(screen, defColorExit,(250,560,100,50))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Exit", smallText)
        textRect.center = ( 300, (560+(50/2)) )
        screen.blit(textSurf, textRect)

        game.display.update()
        game.time.wait(15)
        game.display.flip()

while playing:
    main()
