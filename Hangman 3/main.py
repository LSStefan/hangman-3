import pygame
import os
import sys
import time
import ctypes
import subprocess




module = "pygame"
try:
    subprocess.check_call(['python', '-m', 'pip', 'install', module])
except subprocess.CalledProcessError:
    print(f"Failed to install {module}")
    sys.exit(1)

# Load the shared library from C
lib = ctypes.CDLL("./lib.so")
class Node(ctypes.Structure):
    pass

# for using lists from C
Node._fields_ = [("letter", ctypes.c_char), ("next", ctypes.POINTER(Node))]

lib.create_node.argtypes = [ctypes.c_char]
lib.create_node.restype = ctypes.POINTER(Node)

lib.append.argtypes = [ctypes.POINTER(ctypes.POINTER(Node)), ctypes.c_char]
lib.append.restype = None

lib.list_to_string.argtypes = [ctypes.POINTER(Node)]
lib.list_to_string.restype = ctypes.c_char_p



pygame.init()
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")


# Load the images 
button_image = pygame.image.load("Assets\Start_button.png")  
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
random_image_button = pygame.image.load("Assets\surprise.png")
random_image_rect = random_image_button.get_rect(topright=(WIDTH - 10, 10))
background_credit = pygame.image.load("Assets\credentials.png")

buton_credite = pygame.image.load("Assets\credits.png")
buton_credite = pygame.transform.scale(buton_credite, (200, 40))
buton_credite_rect = buton_credite.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))

random_image_button.set_alpha(0)


font = pygame.font.Font(None, 48)
font2 = pygame.font.Font(None, 30)
fontquestion = pygame.font.Font("Assets\Fonts\DSketch.otf",80)
fonttext = pygame.font.Font("Assets\Fonts\scoobydoo.ttf",22)
fonttext2 = pygame.font.Font("Assets\Fonts\scoobydoo.ttf",20)
fonttext3 = pygame.font.Font("Assets\Fonts\scoobydoo.ttf",25)
fonttext4 = pygame.font.Font("Assets\Fonts\scoobydoo.ttf",48)
fonttext5 = pygame.font.Font("Assets\Fonts\cronometru.TTF",40)
running = True

litere_folosite =  ctypes.POINTER(Node)()  #list of used letters for display
used_letters = [] # list of used letters for checking

lives = 6
score = 0
chances = 1


# Load the sounds
win_music = pygame.mixer.Sound("Assets\sunete\Harp1.Mp3")
wrong_letter = pygame.mixer.Sound("Assets\sunete\CoughClearThroat3.wav")
lose_music = pygame.mixer.Sound("Assets\sunete\Fail Sound Effect.mp3")

# Function to display the used letters
def display_used_letters(used_letters):
    letters_str = lib.list_to_string(used_letters).decode('utf-8')
    return letters_str

# Function to remove spaces from a string
def remove_spaces(string):
    return string.replace(" ", "")

def quiz():
    global screen
    exemplu = "A&B"
    runintrebare = True

    with open("intrebare.txt", "r") as file:
        content = file.read()
        content = content.split("\n")
        intrebare = content[0]
        vara = content[1]
        varb = content[3]
        varc = content[5]
        vard = content[7]

            
    with open("raspuns.txt", "r") as file:
        raspuns = file.read()


    raspunsjucator = ""
    while runintrebare:
        
        RASPUNS = fonttext3.render(raspunsjucator, True, (0,0,0))
        raspunsjucator_rect = RASPUNS.get_rect(center=(screen.get_width() // 2, screen.get_height()-(screen.get_height()-500)))
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            raspunsjucator = raspunsjucator[:-1]
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            raspunsjucator = raspunsjucator.upper()
            raspunsjucator = raspunsjucator.strip()
            if raspunsjucator == raspuns:
                print("Correct")
                runintrebare = False
                win()
            else:
                lose()
        
        
        #display 

        background = pygame.image.load("Assets\Question display mode.png")
        text = "QUESTION"
        text_surface = fontquestion.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height()-(screen.get_height()-50)))
        text_intrebare = fonttext.render(intrebare, True, (0,0,0))
        text_vara = fonttext2.render(vara, True, (0,0,0))
        text_varb = fonttext2.render(varb, True, (0,0,0))
        text_varc = fonttext2.render(varc, True, (0,0,0))
        text_vard = fonttext2.render(vard, True, (0,0,0))
        exemplu_text = fonttext2.render(exemplu, True, (0,0,0))

        screen.blit(background, (0, 0))
        screen.blit(text_surface, text_rect)
        screen.blit(text_intrebare, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-100)))
        screen.blit(text_vara, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-200)))
        screen.blit(text_varb, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-250)))
        screen.blit(text_varc, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-300)))
        screen.blit(text_vard, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-350)))
        screen.blit(exemplu_text, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-400)))
        screen.blit(RASPUNS, raspunsjucator_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                raspunsjucator += event.unicode
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        pygame.display.update()
            
        
# Function to generate a bonus question 
scorex = 0
def question():
    global scorex
    print("pl")
    global screen,running,chances
    chances = 0
    screen.fill((255, 255, 255))
    ###  generate bonus question ### using function from C
    class Intrebare(ctypes.Structure):
                _fields_ = [("text", ctypes.c_char * 100)]  # Adjust size accordingly

    lib.extrag_intrebare.argtypes = [ctypes.c_char_p, ctypes.POINTER(Intrebare)]
    intrebatoare = Intrebare()
    intrebari_hangman = "intrebari_hangman.txt"
    lib.extrag_intrebare(intrebari_hangman.encode(), ctypes.byref(intrebatoare))

    with open("intrebare.txt", "r") as file:
        content = file.read()
        content = content.split("\n")
        intrebare = content[0]
        vara = content[1]
        varaa = content[2]
        varb = content[3]
        varbb = content[4]
        varc = content[5]
        varcc = content[6]
        vard = content[7]
        vardd = content[8]

            
    raspuns = ""
    with open("raspuns.txt", "r") as file:
        raspuns = file.read()


    

    runintrebare = True
    raspunsjucator = ""

    
    t = 899

    while runintrebare:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                raspunsjucator += event.unicode
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    typed_letter = chr(event.key).lower()
                    varaa = list(varaa)  # Convert varaa to a list
                    copyvara = list(vara)    # Convert vara to a list
                    varbb = list(varbb)  # Convert varbb to a list
                    copyvarb = list(varb)
                    varcc = list(varcc)
                    copyvarc = list(varc)
                    vardd = list(vardd)
                    copyvard = list(vard)
                #print(f"varaa length: {len(varaa)}, vara length: {len(vara)}")  # Debugging statement
                for i in range(min(len(varaa), len(vara))):  # Use min() to ensure iterating within bounds
                    if varaa[i] == '?':
                        if copyvara[i] == typed_letter:
                            varaa[i] = typed_letter
                varaa = "".join(varaa)  # Join varaa back into a string after modification
                for i in range(min(len(varb), len(varbb))):  # Use min() to ensure iterating within bounds
                    if varbb[i] == '?':
                        if copyvarb[i] == typed_letter:
                            varbb[i] = typed_letter
                varbb = "".join(varbb)
                for i in range(min(len(varc), len(varcc))):  # Use min() to ensure iterating within bounds
                    if varcc[i] == '?':
                        if copyvarc[i] == typed_letter:
                            varcc[i] = typed_letter
                varcc = "".join(varcc)
                for i in range(min(len(vard), len(vardd))):  # Use min() to ensure iterating within bounds
                    if vardd[i] == '?':
                        if copyvard[i] == typed_letter:
                            vardd[i] = typed_letter
                vardd = "".join(vardd)

                
                
    
        if varaa == vara and varbb == varb and varcc == varc and vardd == vard:
            print("Babasha")
            scorex += 100
            quiz()
            
        #timer
        mins, secs = divmod(t, 60) 
        timer = '{:02.0f}:{:02.0f}'.format(mins, secs) 
        time.sleep(0.1) 
        t -= 0.1

        if t <= 0:
            lose()


        background = pygame.image.load("Assets\Question display mode.png")
        text = "QUESTION"
        text_surface = fontquestion.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height()-(screen.get_height()-50)))
        text_intrebare = fonttext.render(intrebare, True, (0,0,0))
        text_varaa = fonttext2.render(varaa, True, (0,0,0))
        text_varbb = fonttext2.render(varbb, True, (0,0,0))
        text_varcc = fonttext2.render(varcc, True, (0,0,0))
        text_vardd = fonttext2.render(vardd, True, (0,0,0))
        timer = fonttext5.render(timer, True, (0,0,0))
        timer_rect = timer.get_rect(topright=(screen.get_width() - 10, 10))
        score_text = fonttext4.render(f"Score: {scorex}", True, (0,0,0))
        score_rect = score_text.get_rect(topleft=(10, 10))


        screen.blit(background, (0, 0))
        screen.blit(text_surface, text_rect)
        screen.blit(text_intrebare, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-100)))
        screen.blit(text_varaa, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-200)))
        screen.blit(text_varbb, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-250)))
        screen.blit(text_varcc, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-300)))
        screen.blit(text_vardd, (screen.get_width()-(screen.get_width()-100), screen.get_height()-(screen.get_height()-350)))
        screen.blit(timer, timer_rect)
        screen.blit(score_text, score_rect)
        #screen.blit(RASPUNS, raspunsjucator_rect)

        
            
        
        pygame.display.update()  


# Function to display the win screen
def win():

    litere_folosite = ctypes.POINTER(Node)()
    print("You won!")
    win_music.play()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        background = pygame.image.load("Assets\imaginefinal.png")
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))
        pygame.display.update()
        time.sleep(3)
        question()      


# Function to display the lose screen
def lose():
    global scorex,litere_folosite
    litere_folosite = ctypes.POINTER(Node)()
    used_letters = []
    lose_music.play()
    score_text = fonttext4.render(f"Your score was: {scorex}", True, (0,0,0))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        background = pygame.image.load("Assets\lose.png")
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))
        screen.blit(score_text,(screen.get_width() // 2 - 200, screen.get_height()-(screen.get_height()-100)))
        print("Game Over")
        pygame.display.update()
        time.sleep(3)
        score = 0
        litere_folosite = ctypes.POINTER(Node)()  #list of used letters for display
        break
    subprocess.Popen([sys.executable] + sys.argv)
    quit()



def game():
    
    global screen,running,lives,used_letters,chances
    lives = 6
    used_letters = []

    print("Game started")
    # Add your game code here
    with open("./cuvant.txt", "r") as file:
        word = file.read()
        if not word.strip():
            print("File is empty.")
    
    length = len(word)

    # Call the function from the shared C library to encode the word
    lib.codificare_cuvant.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.codificare_cuvant.restype = ctypes.c_char_p

    codificat = lib.codificare_cuvant(word.encode("utf-8"), length)

    codificat = str(codificat) # convert from bytes to string

    word_underline = "" # _ _ _ _ _ _ _ _ _
    for i in codificat:
        if i == "_":
            word_underline += "_ "
        if i == " ":
            word_underline += "  "



    # Call the function from the shared C library to extract a word
    lib.extrag_cuvant()


    
    
    print(word_underline)
    
            
    background = pygame.image.load("Assets\image-06.jpg")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    screen.blit(background, (0, 0))
    pygame.display.update()

    t = 899
    # mediu verde
    # _ _ _ _ _ _ _ _ _
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and lives > 0:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    typed_letter = chr(event.key).lower()
                    if typed_letter in word:
                        print("Correct")
                        word_underline = list(word_underline)
                        for i in range(len(word)):
                            if word[i] == typed_letter:
                                word_underline[i * 2] = typed_letter
                        word_underline = "".join(word_underline)
                        if typed_letter not in used_letters:
                            used_letters.append(typed_letter)
                            lib.append(ctypes.byref(litere_folosite), typed_letter.encode()) #adaugare litera in lista

                                    
                    else:
                        wrong_letter.play()
                        print("Incorrect")
                        print("Lives left:", lives)
                        if typed_letter not in used_letters:
                            lives -= 1
                            used_letters.append(typed_letter)
                            lib.append(ctypes.byref(litere_folosite), typed_letter.encode()) #adaugare litera in lista



        # Background image
        match lives:
            case 6:
                background = pygame.image.load("Assets\image-06.jpg")  
            case 5:
                background = pygame.image.load("Assets\Fundaluri\In-game1.png")
            case 4:
                background = pygame.image.load("Assets\Fundaluri\In-game2.png")
            case 3:
                background = pygame.image.load("Assets\Fundaluri\In-game3.png")
            case 2:
                background = pygame.image.load("Assets\Fundaluri\In-game4.png")
            case 1:
                background = pygame.image.load("Assets\Fundaluri\In-game5.png")
            case _:
                background = pygame.image.load("Assets\image-06.jpg")


        demintrebare = False
        runintrebare = True
        if lives == 0 and chances == 1:
            while runintrebare:
                timetochoose = "Do you want to answer a bonus question? y/n"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            damintrebare = True
                            runintrebare = False
                        if event.key == pygame.K_n:
                            damintrebare = False
                            runintrebare = False

                lives_surface = font.render(f"Lives: {lives}", True, (0,0,0))
                text_surface = fonttext3.render(timetochoose, True, (0,0,0))
                screen.blit(text_surface,(screen.get_width()-(screen.get_width()-10), screen.get_height()-(screen.get_height()-120)))
                screen.blit(lives_surface, (10, 10))
                pygame.display.update()
                
                

        # Check if the player has lost and he doesn't have to answer a bonus question
        if (lives == 0 and damintrebare == False):
            lose()

        
        # Check if the player has lost and has to answer a bonus question
        if lives == 0 and damintrebare == True:
            quiz()
        
        if chances == 0:
            damintrebare = False


        litere_folosite_str = display_used_letters(litere_folosite)

        

        litere = font2.render(f"Used letters:{litere_folosite_str}", True, (0,0,0))

        mins, secs = divmod(t, 60) 
        timer = '{:02.0f}:{:02.0f}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(0.1) 
        t -= 0.1

        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))                    
        text_surface = font.render(word_underline, True, (0,0,0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        lives_surface = font.render(f"Lives: {lives}", True, (0,0,0))
        score_surface = font.render(f"Score: {score}", True, (0,0,0))
        timer = fonttext5.render(timer, True, (0,0,0))
        timer_rect = timer.get_rect(topright=(screen.get_width() - 10, 10))

        



        if t <= 0:
            lose()
        

        screen.blit(background, (0, 0))
        screen.blit(text_surface, text_rect)
        screen.blit(lives_surface, (10, 10))
        screen.blit(score_surface, (10, 50))
        screen.blit(text_surface, text_rect)
        screen.blit(timer, timer_rect)
        screen.blit(litere, (screen.get_width()-(screen.get_width()-10), screen.get_height()-(screen.get_height()-94)))
        


        # Check if the player has won
        copy = remove_spaces(word_underline)
        copyword = word.replace(" ", "")
        if copy == copyword and copy != "":
            win()

        pygame.display.update()



def random():
    global screen
    background = pygame.image.load("Assets\DnPdIe4A.jpeg")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    screen.blit(background, (0, 0))
    pygame.display.update()


def credits():
    global background_credit,screen
    buton = pygame.image.load("Assets\jhon.png")
    buton_rect = buton.get_rect(topright=(screen.get_width() - 10, 10))

    while 1:
        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            quit()
        background_credit = pygame.transform.scale(background_credit, (screen.get_width(), screen.get_height()))
        screen.blit(background_credit, (0, 0))
        buton_rect = buton.get_rect(topright=(screen.get_width() - 10, 10))
        screen.blit(buton, buton_rect)
    
        if buton_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                main()

        pygame.display.update()

    

def main():
    global screen
    t = 10
    running = True
    background = pygame.image.load("Assets\Start_game.png")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))
        button_rect = button_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        random_image_rect = random_image_button.get_rect(topright=(screen.get_width() - 10, 10))
        buton_credite_rect = buton_credite.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 250))
        
        screen.blit(button_image, button_rect)
        screen.blit(random_image_button, random_image_rect)
        screen.blit(buton_credite, buton_credite_rect)


        


        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                question()
        if random_image_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                random()
        if buton_credite_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                credits()
        pygame.display.update()

        
      



if __name__ == "__main__":
    main()



