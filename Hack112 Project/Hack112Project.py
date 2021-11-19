from cmu_112_graphics import *
import random, string, math, time
from dataclasses import make_dataclass

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


def appStarted(app):
    app.level = 1
    app.gameover = False
    app.rows = 50
    app.cols = 70
    app.radius = 18
    app.life = 5
    nextLevel(app)
    app.bg = app.loadImage("BG.png")
    app.ghost = app.loadImage('smallGhost.png')
    app.startMenu = True
    app.inGame = False
    app.inInstructions = False
    app.instructionPage = 1
    app.color = 'black'

def nextLevel(app):
    app.gameover = False
    app.win = False
    app.die = False
    app.lose = False
    app.jump = False
    app.rise = False
    app.fall = True
    app.veloX = 5
    app.veloRise = 20
    app.veloFall = 2
    app.left = False
    app.right = False
    app.posAX = app.width/2
    app.posAY = app.height - app.radius
    app.veloBad = []
    for i in range(2*app.level):
        direction = random.randint(0,1)
        if direction == 0:
            direction = -1
        app.veloBad.append(direction*3*app.level)
    if app.level == 1:
        app.board = getMap1(app)
    elif app.level == 2:
        app.board = getMap2(app)
    elif app.level == 3:
        app.board = getMap3(app)
    generateBad(app)

def sizeChanged(app):
    app.width = 700
    app.height = 500

def generateBad(app):
    playerRow, playerCol = getCell(app, app.posAX, app.posAY) 
    app.bads = []
    while True:
        row = random.randint(5, app.rows-10)
        col = random.randint(5, app.cols-10)
        if isLegalMove(app, row, col):
            if len(app.bads) > 0:
                pre = app.bads[len(app.bads)-1]
                preRow, preCol = getCell(app, pre[0], pre[1])
                if abs(preRow - row) >= 3:
                    x, y = getXY(app, row, col)
                    app.bads.append([x, y])
            else:
                x, y = getXY(app, row, col)
                app.bads.append([x, y])
        if len(app.bads) == min(2*app.level,5):
            break

def moveBad(app):
    r = 10
    i = 0
    for bad in app.bads:
        bad[0] += app.veloBad[i]
        if bad[0]-r <= 0:
            bad[0] += abs(app.veloBad[i])
            app.veloBad[i] *= -1
        elif bad[0]+r >= app.width:
            bad[0] -= abs(app.veloBad[i])
            app.veloBad[i] *= -1
        i += 1

def checkLose(app):
    for bad in app.bads:
        if math.sqrt((bad[0]-app.posAX)**2+(bad[1]-app.posAY)**2)<app.radius+10:
            app.die = True
            app.gameover = True
            app.life -= 1
            if app.life == 0:
                app.die = False
                app.lose = True
                app.gameover = True
        

def moveLeft(app):
    app.posAX -= app.veloX
    if app.posAX-app.radius <= 0:
        app.posAX += app.veloX
        app.left = False

def moveRight(app):
    app.posAX += app.veloX
    if app.posAX+app.radius >= app.width:
        app.posAX -= app.veloX
        app.right = False

def rise(app):
    if app.veloRise == 0:
            app.rise = False
            app.fall = True  
    for i in range(app.veloRise):
        app.posAY -= 1
        playerRow, playerCol = getCell(app, app.posAX, app.posAY)     
        if not isLegalMove(app, playerRow-2, playerCol) or playerRow-2 < 0:
            app.rise = False
            app.fall = True
            app.veloFall = 2
            

def fall(app):
    for i in range(app.veloFall):
        app.posAY += 1
        playerRow, playerCol = getCell(app, app.posAX, app.posAY)
        if playerRow >= app.rows-4:
                app.posAY = app.height - app.radius
                app.jump = False
                app.fall = False
                app.veloRise = 20
                app.veloFall = 2
        elif not isLegalMove(app, playerRow+2, playerCol):
            app.posAY -= 1
            app.fall = False
            app.jump = False
            app.veloRise = 20
            app.veloFall = 2
            break
            



def keyPressedInGame(app,event):
    if app.gameover == False:
        if app.left == False and app.right == False:
            if event.key == "a":
                app.left = True
            elif event.key == "d":
                app.right = True
        elif app.left == True and app.right == False:
            if event.key == 'd':
                app.left = False
                app.right = True
        elif app.right == True and app.left == False:
            if event.key == 'a':
                app.right = False
                app.left = True
        if app.left == True or app.right == True:
            if event.key == 's':
                app.left = False
                app.right = False
        if app.jump == False:
            if event.key == 'w':
                app.jump = True
                app.rise = True
                app.fall = False
    elif app.die == True and app.lose == False:
        if event.key == 'r':
            nextLevel(app)
    elif app.lose == True:
        if event.key == 'r':
            appStarted(app)
    elif app.win == True:
        if event.key == 'n':
            if app.level == 1:
                app.level = 2
                nextLevel(app)
            elif app.level == 2:
                app.level = 3
                nextLevel(app)

    
           

def keyPressed(app,event):
    if app.inGame == True:
        keyPressedInGame(app, event)
    
def clickNext(app, x, y):
    if  (610 <= x <= 680 and 440 <= y <= 480):
        app.instructionPage = 2
        

def clickBack(app, x, y):
    if  (530 <= x <= 600 and 440 <= y <= 480):
        app.instructionPage = 1
        

def clickReturn(app, x, y):
    if  (20 <= x <= 90 and 440 <= y <= 480):
        app.inInstructions = False
        app.startMenu = True

def clickStart(app, x, y):
    if  (app.width/2-50 <= x <= app.width/2+50 and 
         app.height*2/3+50 <= y <= app.height*2/3+90):
         app.inGame = True
         app.startMenu = False
         app.time0 = time.time()
         app.timeLeft = int(90-(time.time()-app.time0))

def clickRules(app, x, y):
    if  (app.width/2-50 <= x <= app.width/2+50 and 
         app.height*2/3-50 <= y <= app.height*2/3-10):
         app.inInstructions = True
         app.startMenu = False

def mousePressedStartMenu(app, event):
    clickStart(app, event.x, event.y)
    clickRules(app, event.x, event.y)

    

def mousePressed(app, event):
    if app.startMenu == True:
        mousePressedStartMenu(app, event)
    elif app.inInstructions == True:
        clickNext(app, event.x, event.y)
        clickBack(app, event.x, event.y)
        clickReturn(app, event.x, event.y)


def isLegalMove(app, row, col):
    if col > app.cols-1 or col < 0 or row > app.rows-1 or row < 0:
        return False
    if app.board[row][col] == None:
        return True
    # See if you have reached the door
    elif app.board[row][col] == 2:
        return 2
    else:
        return False

def checkWin(app):
    playerRow, playerCol = getCell(app, app.posAX, app.posAY)
    if isLegalMove(app, playerRow, playerCol) == 2:
        app.win = True
        app.gameover = True

def checkRise(app):
    if app.rise == True:
            rise(app)
            app.veloRise -= 2

def checkFall(app):
    playerRow, playerCol = getCell(app, app.posAX, app.posAY)
    if app.fall == False:
        if playerRow <= app.rows-4 or isLegalMove(app, playerRow+1, playerCol):
            if app.rise == False:
                app.fall = True
    if app.fall == True:
        fall(app)
        app.veloFall += 2           


def timerFired(app):
    if app.lose == False:
        if app.inGame == True:
            app.timeLeft = int(90-(time.time()-app.time0))
            if app.timeLeft <= 0:
                app.timeLeft = 0
                app.die = False
                app.lose = True
                app.gameover = True
            if app.timeLeft <= 30:
                app.color = 'red'
            else:
                app.color = 'black'
    if app.gameover == False:
        moveBad(app)
        checkWin(app)
        checkLose(app)
        checkFall(app)
        app.timerDelay = 10
        if app.jump == True:
            checkRise(app)
        if app.left == True:
            playerRow, playerCol = getCell(app, app.posAX, app.posAY)
            if isLegalMove(app, playerRow, playerCol-2):
                moveLeft(app)
        if app.right == True:
            playerRow, playerCol = getCell(app, app.posAX, app.posAY)
            if isLegalMove(app, playerRow, playerCol+2):
                moveRight(app)
        for bad in app.bads:
            veloBad = 10


def getCell(app, x, y):
    row = int(y/10)
    col = int(x/10)
    return row, col

def getXY(app,row,col): # 25 rows 35 cols xy--sw corner
   x = col * 10
   y = 10+row * 10 # cell width&height 20
   return (x,y)



def drawStartMenu(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
            image= ImageTk.PhotoImage(app.bg))
    canvas.create_text(app.width/2, app.height/3, 
                        text = "Freddy Jump", font = "Arial 40")
    canvas.create_rectangle(app.width/2-50, app.height*2/3-50, app.width/2+50, 
    app.height*2/3-10, fill = 'lightgreen')
    canvas.create_text(app.width/2, app.height*2/3-30, 
                        text = "RULES", font = "Arial 18")
    canvas.create_rectangle(app.width/2-50, app.height*2/3+50, app.width/2+50, 
    app.height*2/3+90, fill = 'lightgreen')
    canvas.create_text(app.width/2, app.height*2/3+70, 
                        text = "START", font = "Arial 18")
        

def drawInstructions(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
            image= ImageTk.PhotoImage(app.bg))
    canvas.create_rectangle(20, 440, 90, 480, fill = 'lightgreen')
    canvas.create_text(55, 460, text = 'Return', font = 'Arial 16')
    if app.instructionPage == 1:
        canvas.create_text(40,30, 
    text = 'Freddy Jump is a game developed by Alisa, Alvin, Ella, and Eric.' 
    + '\nIn this game, you will control Freddy using the keys AWSD.'
    + '\n\nW: makes Freddy jump'
    + '\nD: makes Freddy move right'
    + '\nA: makes Freddy move left'
    + '\nS: makes Freddy stop moving'
    + '\n\nNote that you do not need to hold on keys, once a key is pressed,'
    + '\nFreddy will continue moving in that direction.'
    + '\n\nThe goal of the game is to reach the red door. However, there'
    + '\nare ghosts, so beware since Touching a ghost results in losing 1 life!'
    + '\nThe game has three levels in total.'
    + '\nAlso be aware of time. You lose when time becomes 0!!'
    + '\n\nGood luck, and may you make your Freddy shine!',
    font = 'Arial 16', anchor = 'nw')
        canvas.create_rectangle(610, 440, 680, 480, fill = 'lightgreen')
        canvas.create_text(645, 460, text = 'Next', font = 'Arial 16')
    elif app.instructionPage == 2:
        canvas.create_rectangle(50,370,100,420,width=5) # grid for A
        canvas.create_rectangle(120,370,170,420,width=5) # grid for S
        canvas.create_rectangle(190,370,240,420,width=5) # grid for D
        canvas.create_rectangle(120,300,170,350,width=5) # grid for W
        canvas.create_text(75,395,text="A",font="Helvetica 20 bold") # A
        canvas.create_text(145,395,text="S",font="Helvetica 20 bold") # S
        canvas.create_text(215,395,text="D",font="Helvetica 20 bold") # D
        canvas.create_text(145,325,text="W",font="Helvetica 20 bold") # W
        canvas.create_text(290,340,text="To Control",font="Helvetica 20 bold")
        canvas.create_text(50,340,text="Use",font="Helvetica 20 bold")
        canvas.create_oval(490,140,510,160,fill="white",width=2) # ghost
        canvas.create_oval(497,149,504,156,fill="red",width=0)
        canvas.create_line(520,150,570,150,fill="blue",width=2)
        canvas.create_line(540,140,590,140,fill="blue",width=2)
        canvas.create_line(540,160,590,160,fill="blue",width=2)
        canvas.create_text(500,200,text="Be aware of the ghosts!!!",
                            font="Helvetica 20 bold",fill="red")
        canvas.create_rectangle(100,150,200,160,fill="pink",width=0)
        canvas.create_rectangle(0,80,100,90,fill="pink",width=0)
        canvas.create_rectangle(20,70,80,80,fill="red",width=0)
        canvas.create_rectangle(20,60,80,70,fill="red",width=0)
        canvas.create_rectangle(20,50,80,60,fill="red",width=0)
        canvas.create_rectangle(20,40,80,50,fill="red",width=0)
        canvas.create_rectangle(20,30,80,40,fill="red",width=0)
        canvas.create_rectangle(20,20,80,30,fill="red",width=0)
        canvas.create_text(250,50,text="Arrive safely at the door",
                            font="Helvetica 20 bold",fill="orange")
        canvas.create_text(250,90,text="to WIN!",
                            font="Helvetica 20 bold",fill="orange")
        canvas.create_rectangle(500,420,750,430,fill="pink",width=0)
        
        canvas.create_oval(575-20,400-20,575+20,400+20,
                            fill="brown", width=20//10)
        canvas.create_oval(575-20//2,400+(20//3)-20//2,
                            575+20//2,400+(20//3)+20//2,
                            fill = "burlywood", width = 20//20)
        canvas.create_oval(575-20//8,400+(20//6)-20//8,
                            575+20//8,400+(20//6)+20//8,
                            fill = "black") # draw the nose
        canvas.create_oval(575-20//2-20//6,
                            400-20//2+(20//6)-20//6,
                            575-20//2+20//6,
                            400-20//2+(20//6)+20//6,
                            fill = "black") # draw left eyes
        canvas.create_oval(575+20//2-20//6,
                            400-20//2+(20//6)-20//6,
                            575+20//2+20//6,
                            400-20//2+(20//6)+20//6,
                            fill = "black") # draw right eyes
        canvas.create_oval(575-21-10,400-21-10,575-21+10,400-21+10,
                       fill="brown", width=20//10)# draw left ear
        canvas.create_oval(570-17-6,400-17-6,570-17+6,400-17+6,
                            fill="burlywood", width=20//10)# draw left ear inner
        canvas.create_oval(575+21-10,400-21-10,575+21+10,400-21+10,
                            fill="brown", width=20//10)# draw right ear
        canvas.create_oval(580+17-6,400-17-6,580+17+6,400-17+6,
                            fill="burlywood", width=20//10) # draw right ear inner

        canvas.create_rectangle(530, 440, 600, 480, fill = 'lightgreen')
        canvas.create_text(565, 460, text = 'Back', font = 'Arial 16')
    

def drawGame(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
            image= ImageTk.PhotoImage(app.bg))
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col] == 1:
                (x0,y0,x1,y1)= getCellBounds(app, row, col)
                canvas.create_rectangle(x0,y0,x1,y1, fill = "mistyrose",
                outline = "hotpink")
            if app.board[row][col] == 2:
                (x0,y0,x1,y1)= getCellBounds(app, row, col)
                canvas.create_rectangle(x0,y0,x1,y1, fill = "red", 
                outline = "red")
    canvas.create_oval(app.posAX - app.radius, app.posAY - app.radius,
                        app.posAX + app.radius, app.posAY + app.radius, 
                        fill = "cyan", outline = "cyan")
    drawFace(app, canvas, 1, app.posAX, app.posAY, app.radius, "brown")
    drawBad(app, canvas)
    drawWin(app, canvas)
    if app.inGame == True:
        drawTime(app, canvas)
    drawLose(app, canvas)
    drawLife(app, canvas)


def drawWin(app, canvas):
    if app.win == True and app.level == 3:
        canvas.create_text(app.width//2, app.height//2, 
                            text = 'FINAL WIN', font = 'Arial 60 bold')
    elif app.win == True:
        canvas.create_text(app.width/2,app.height/2 , text = 'YOU WIN!!! Press N to enter the next level',
         font = 'Arial 20 bold')


def drawLose(app, canvas):
    if app.timeLeft == 0:
        canvas.create_text(app.width/2,app.height/2 , text = 
        'TIMES UP!! Press R to restart the game!',
            font = 'Arial 20 bold')
    elif app.die == True:
        canvas.create_text(app.width/2,app.height/2 , text = 
        'YOU DIE!! Press R to try again!',
            font = 'Arial 20 bold')
    elif app.lose == True:
        canvas.create_text(app.width/2,app.height/2 , text = 
        'YOU LOSE!! Press R to restart the game!',
            font = 'Arial 20 bold')
        
def drawLife(app, canvas):
    canvas.create_text(app.width//2, app.height//15, 
                        text = f'current life: {app.life}', fill = 'red',
                        font = 'Arial 20 bold')

def drawBad(app, canvas):
    for bad in app.bads:
        canvas.create_image(bad[0], bad[1], 
        image= ImageTk.PhotoImage(app.ghost))

def drawTime(app, canvas):
    if app.timeLeft %60 >= 10:
        canvas.create_text(app.width//8, app.height//15, 
                        text = f'0{app.timeLeft//60}:{app.timeLeft%60} left',
                        font = 'Arial 20 bold',
                        fill = app.color)
    else:
        canvas.create_text(app.width//8, app.height//15, 
                        text = f'0{app.timeLeft//60}:0{app.timeLeft%60} left',
                        font = 'Arial 20 bold',
                        fill = app.color)

def drawFace(app, canvas, level, x, y, size, color):
    if level == 0:
        canvas.create_oval(x - size, y - size, x+size, y + size, fill = color,
                        width = size/10)
        mouthcx, mouthcy, mousesize = x, y + 7/20 * size, 1/2 * size
        canvas.create_oval(mouthcx - mousesize, mouthcy - mousesize,
                        mouthcx + mousesize, mouthcy + mousesize, 
                        fill = "burlywood", width = size/20)
        if size == 18:
            nosecx, nosecy = x, y + 1/7* size
            noseEyeSize = 1/7 * size
            canvas.create_oval(nosecx - noseEyeSize, nosecy - noseEyeSize,
                            nosecx + noseEyeSize, nosecy + noseEyeSize, 
                            fill = "black", width = size/20)
            eye1cx, eye1cy = x - 4/9* size, y - 1/3*size
            canvas.create_oval(eye1cx - noseEyeSize, eye1cy - noseEyeSize,
                            eye1cx + noseEyeSize, eye1cy + noseEyeSize, 
                            fill = "black", width = size/20)
            eye2cx, eye2cy = x + 4/9* size, y - 1/3*size
            canvas.create_oval(eye2cx - noseEyeSize, eye2cy - noseEyeSize,
                            eye2cx + noseEyeSize, eye2cy + noseEyeSize, 
                            fill = "black", width = size/20)
            mouth1x, mouth1y = x - (1/5 ) * size, y + 2/5 *size
            mouthwidth, mouthheight = 1/5 *size, 1/5 *size
            canvas.create_arc(mouth1x, mouth1y, mouth1x + mouthwidth,
                    mouth1y + mouthheight, start = 180, extent = 180,
                    style = ARC, width = size/18)
            canvas.create_arc(mouth1x  + mouthwidth, mouth1y, 
                    mouth1x  + 2 * mouthwidth, mouth1y + mouthheight, 
                    start = 180, extent = 180,
                    style = ARC, width = size/18)
    else:
        drawFace(app, canvas, level-1, x , y, size, color)
        # Left top Freddy
        coeff = 3/4 * math.sqrt(2)
        drawFace(app, canvas, level-1, 
                x - coeff * size , y - coeff * size, size/2, color)
        # Right top Freddy
        drawFace(app, canvas, level-1,
                x + coeff * size , y - coeff * size, size/2, color)

def drawGameAcknowledgements(app, canvas):
    canvas.create_text(350, 250, 
    text = 'Congradulations!'
    + '\nYou have passed all three levels. Thank you for playing this game.'
    + '\n感谢你能花费自己生命中的几分钟来玩我们创造的这个小游戏'
    + '\n游戏虽然结束了，但是你的人生还在继续，頑張ってください！', font = 'Arial 17')
    canvas.create_text(500, 450, text = '邱诗芸、邹锐骅、赵禹诺、向喆华', font = 'Arial 18')


def redrawAll(app, canvas):
    if app.startMenu == True:
        drawStartMenu(app, canvas)
    elif app.inInstructions == True:
        drawInstructions(app, canvas)
    elif app.win == True and app.level == 3:
        drawGameAcknowledgements(app, canvas)
    elif app.inGame == True:
        drawGame(app, canvas)


def getCellBounds(app, row, col):
    x0 = 10*col
    y0 = 10* row
    x1 = 10 *(col +1)
    y1 = 10* (row +1)
    return(x0,y0,x1,y1)

def getMap2(app):
    board = [[None]*app.cols for i in range(app.rows)]
    for i in range(20,70):
        board[10][i] = 1
    for i in range(62,68):
        board[9][i] = 2
    for i in range(62,68):
        board[8][i] = 2
    for i in range(62,68):
        board[7][i] = 2
    for i in range(62,68):
        board[6][i] = 2
    for i in range(62,68):
        board[5][i] = 2
    for i in range(62,68):
        board[4][i] = 2
    for i in range(62,68):
        board[3][i] = 2
    for i in range(62,68):
        board[2][i] = 2
    for i in range(10,15):
        board[17][i] = 1
    for i in range(10,28):
        board[24][i] = 1
    for i in range(35,40):
        board[28][i] = 1
    for i in range(63,70):
        board[33][i] = 1
    for i in range(35,50):
        board[38][i] = 1
    for i in range(0,8):
        board[45][i] = 1
    for i in range(20,30):
        board[40][i] = 1
    return board

def getMap1(app):
    board = [[None]*app.cols for i in range(app.rows)]
    for i in range(20,40):
        board[41][i] = 1
        board = [[None]*70 for i in range (50)]
    for i in range(11,40):
        board[42][i] = 1
    for i in range(39,52):
        board[34][i] = 1
    for i in range(25,40):
        board[26][i] = 1
    for i in range(0,20):
        board[18][i] = 1
    for i in range(25,34):
        board[10][i] = 1
    for row in range(5, 10):
        for col in range(28, 32):
            board[row][col] = 2
    return board


def getMap3(app):
    board = [[None]*app.cols for i in range(app.rows)]
    for i in range(58,70):
        board[10][i] = 1
    for i in range(62,68):
        board[9][i] = 2
    for i in range(62,68):
        board[8][i] = 2
    for i in range(62,68):
        board[7][i] = 2
    for i in range(62,68):
        board[6][i] = 2
    for i in range(62,68):
        board[5][i] = 2
    for i in range(62,68):
        board[4][i] = 2
    for i in range(62,68):
        board[3][i] = 2
    for i in range(62,68):
        board[2][i] = 2
    for i in range(38,43):
        board[15][i] = 1
    for i in range(46,50):
        board[8][i] = 1
    for i in range(55,70):
        board[20][i] = 1
    for i in range(27,32):
        board[17][i] = 1
    for i in range(13,20):
        board[20][i] = 1
    for i in range(0,6):
        board[23][i] = 1
    for i in range(8,12):
        board[29][i] = 1
    for i in range(25,30):
        board[36][i] = 1
    for i in range(35,40):
        board[41][i] = 1
    for i in range(10,20):
        board[37][i] = 1
    return board









def main():
    runApp(width=700, height=500)


if __name__ == '__main__':
    main()
