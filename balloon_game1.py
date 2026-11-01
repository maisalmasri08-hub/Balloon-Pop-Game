import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from volume_controller import VolumeController
import random
import pygame
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

base_options1 = python.BaseOptions( model_asset_path="hand_landmarker.task")
options1 = vision.HandLandmarkerOptions(
    base_options=base_options1,
    num_hands=1,
    running_mode=vision.RunningMode.VIDEO
)

base_options2 = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options2 = vision.GestureRecognizerOptions(
    base_options=base_options2,
    running_mode=vision.RunningMode.IMAGE
)

detector = vision.HandLandmarker.create_from_options(options1)
recognizer = vision.GestureRecognizer.create_from_options(options2)

cap = cv2.VideoCapture(0)

timestamp_ms = 0

pygame.init()

WIDTH = 1600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Pop Game 🎈🏹")

clock = pygame.time.Clock()


SKY_BLUE = (190, 230, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


BALLOON_COLORS = [
    (255, 0, 0),      # أحمر
    (255, 255, 0),    # أصفر
    (0, 120, 255),    # أزرق
    (160, 50, 220),   # بنفسجي
    (255, 140, 0),    # برتقالي
    (0, 200, 80),     # أخضر
    (255, 80, 160),   # وردي
    (0 , 0 , 0 )      #أسود
]

colors_weights = [ 50 , 50 , 50 , 50 , 50 , 50 , 50 , 20 ]

arrow = pygame.image.load("arrow.png")
arrow= pygame.transform.scale(arrow, (25, 160))

bow = pygame.image.load("bow.png")
bow = pygame.transform.scale(bow, (250, 200))

balloon_image = pygame.image.load("balloon2.png")
balloon_image= pygame.transform.scale(balloon_image, (120, 200))

sky = pygame.image.load("sky.jpg")
sky = pygame.transform.scale(sky, (1600, 800))

gameover = pygame.image.load("gameover.png")
gameover = pygame.transform.scale(gameover, (1600, 800))

win = pygame.image.load("win.png")
win = pygame.transform.scale(win, (1600, 800))

start = pygame.image.load("start.png")
start = pygame.transform.scale(start, (WIDTH, HEIGHT))

screen.blit(start, (0,0))
is_shooting = False
arrowHeight = arrow.get_height()

pointer = pygame.image.load("pointer.png")
pointer_x = 0
pointer_y = 0
pointer = pygame.transform.scale(pointer, (30, 30))
screen.blit(pointer, (pointer_x,pointer_y))
score = 0 

pop = pygame.mixer.Sound("Pop.mp3")
black_pop = pygame.mixer.Sound("black_pop.mp3")
arrow_sound = pygame.mixer.Sound("arrow_sound.mp3")
button = pygame.mixer.Sound("button.mp3")
Losing_sound = pygame.mixer.Sound("Losing_sound.mp3")
Victory_Sound = pygame.mixer.Sound("Victory_Sound.mp3")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(loops=-1)

bow_x=WIDTH//2
bow_y=HEIGHT-80
arrow_x=WIDTH//2
arrow_y=HEIGHT-62

font = pygame.font.Font(None, 50)
current_time = pygame.time.get_ticks()

balloons = []            #  إنشاء البوالين
for i in range(6):

    balloon = {
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(400, 450),
        "radius": random.randint(25, 35),
        "speed": random.uniform(3, 6),
        "color": random.choice(BALLOON_COLORS),
    }

    balloons.append(balloon)


last_shot_time = 0
shoot_cooldown = 1500
running = True
starting = False
ending = False
controller = VolumeController()
target_volume = 0
seconds = 0
current_time_text = font.render(f"Time: {int(seconds)}",True,(0, 0, 0))
start_time = 0

while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False
    if starting == False and ending == False :  #start
      screen.blit(start, (0,0))
      screen.blit(pointer, (pointer_x,pointer_y))
      if starting==False  and ending==False and pointer_x < 1050 and pointer_x > 550 and pointer_y < 535 and pointer_y > 400 :
                     if gesture_name == "Victory" :
                      start_time = pygame.time.get_ticks() 
                      button.play()
                      starting = True



    elif starting == False and ending == True :  #game over
      screen.blit(gameover, (0,0))
      screen.blit(pointer, (pointer_x,pointer_y))
      pygame.mixer_music.pause()
    #   pygame.draw.rect(screen, (255, 0, 0), (850,520,435,135), 2)
    #   pygame.mixer.music.set_volume(0.0)  #(380,520,380,135)
      if starting==False and pointer_x < 1285 and pointer_x > 850 and pointer_y < 655 and pointer_y > 520 : #restart
                    if gesture_name == "Victory" :
                      starting = True
                      ending = False
                      button.play()
                      start_time = pygame.time.get_ticks()
                      seconds = (current_time - start_time) / 1000 
                      pygame.mixer_music.unpause()
    

      if starting==False and pointer_x < 760 and pointer_x > 380 and pointer_y < 655 and pointer_y > 520 : #exit
        if gesture_name == "Victory" :  
                  button.play()
                  time.sleep(0.6)
                  running = False
        
    elif starting == True and ending == True : # win 
          screen.blit(win , (0 , 0))
          screen.blit(pointer, (pointer_x,pointer_y))
          pygame.mixer_music.pause()

          if starting==True and pointer_x < 1285 and pointer_x > 850 and pointer_y < 655 and pointer_y > 520 : #restart
                              if gesture_name == "Victory" :
                                starting = True
                                ending = False
                                button.play()
                                pygame.mixer_music.unpause()
                                start_time = pygame.time.get_ticks()


                                
          
          if starting==True and pointer_x < 760 and pointer_x > 380 and pointer_y < 655 and pointer_y > 520 : #exit
                  if gesture_name == "Victory" :
                            button.play()
                            time.sleep(0.6)
                            running = False

             
    else  :
     screen.blit(sky , (0 , 0))
     current_time = pygame.time.get_ticks()
     seconds = (current_time - start_time) / 1000
     current_time_text = font.render(f"Time: {int(seconds)}",True,(0, 0, 0))
     screen.blit(current_time_text, (1400, 70))
    
     
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if ret:

        # تحويل الصورة من BGR إلى RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # تحويلها إلى MediaPipe Image
        mp_image = mp.Image(mp.ImageFormat.SRGB,rgb_frame )

        # تحليل اليد
        result = detector.detect_for_video(mp_image,timestamp_ms)

        timestamp_ms += 33

  
    recognition_result = recognizer.recognize(mp_image) # اكتشاف اليد 
    if recognition_result.gestures:
              top_gesture = recognition_result.gestures[0][0]
              gesture_name = top_gesture.category_name  
              gscore = top_gesture.score                
    
            # طباعة الاسم على الشاشة
              cv2.putText(frame, f"Gesture: {gesture_name} ({gscore:.2f})", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
            # فحص حركة السبابة المرفوعة للأعلى
              current_time = pygame.time.get_ticks() 
              if starting == True and  ending== False and gesture_name == "Pointing_Up" and gscore > 0.6 and (current_time - last_shot_time > shoot_cooldown):
                cv2.putText(frame, "SHOOT! 🏹", (20, 100),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                is_shooting = True
                arrow_sound.play() 
                last_shot_time = current_time   
    if result and result.hand_landmarks:

            for hand in result.hand_landmarks:

                # رسم نقاط اليد
                for lm in hand:

                    x = int(lm.x * frame.shape[1])
                    y = int(lm.y * frame.shape[0])

                    cv2.circle(frame, (x, y), 4, (255, 0, 0), -1 )

               
                thumb_tip = hand[4]
                index_tip = hand[8]
                pointer_x= int(( index_tip.x) * WIDTH)
                pointer_y= int(( index_tip.y) * HEIGHT)

                dist = ((thumb_tip.x-index_tip.x)**2 + (thumb_tip.y-index_tip.y)**2)**0.5 

 
                if starting==False or  (ending == True and starting==True) :
                   if pointer_x < 1500 and pointer_x > 1300 and pointer_y < 290 and pointer_y > 90 :
                          controller.update(dist, frame)
    # # 1. رسم النص الخاص بنسبة الصوت
                          font_volume = pygame.font.Font(None, 36)
                          volume_text = font_volume.render(f"Volume: {int(controller.vol_percent)}%", True, (255, 255, 255))
                          screen.blit(volume_text, (1340, 55))
                          target_volume = controller.vol_percent / 100.0

    # 2. إعدادات ورسم شريط الصوت العمودي
                          bar_x = 1500
                          bar_y = 85
                          bar_width = 25
                          bar_max_height = 150
                          current_bar_height = int((controller.vol_percent / 100) * bar_max_height)
    # رسم إطار الشريط الخارجي
                          pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_max_height), 3, border_radius=5)
    # رسم الشريط الممتلئ من الأسفل للأعلى
                          fill_y = bar_y + bar_max_height - current_bar_height
                          pygame.draw.rect(screen, (0, 255, 0), (bar_x, fill_y, bar_width, current_bar_height), border_radius=5)
                bow_x = int(( thumb_tip.x) * WIDTH)
                if not is_shooting :
                   arrow_x = int((thumb_tip.x) * WIDTH)
    else:

             cv2.putText(frame,"No hand detected", (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255), 2)


    cv2.imshow("Hand Camera", frame )

    font = pygame.font.Font(None, 50)

    score_text = font.render(  f"Score: {score}",True,(0, 0, 0))

    if starting == True and ending == False :       # القوس
     screen.blit(bow,( bow_x - bow.get_width() // 2, bow_y - bow.get_height() // 2) )

            # السهم
            
     screen.blit(arrow, (arrow_x-arrow.get_width() // 2,  arrow_y-arrow.get_height() // 2))

    if is_shooting :
        arrow_y -= 50
    if starting == True and ending == False and arrow_y < - arrowHeight :
                           is_shooting = False 
                           arrow_y= HEIGHT-62
                           score = score - 1

    for balloon in balloons:
           
             balloon["y"] -= balloon["speed"]

             # إذا خرج البالون من الأعلى
             if balloon["y"] < -balloon["radius"] * 2:
              balloon["y"] =  random.randint(450, 500)
              balloon["x"] = random.randint( 50,WIDTH - 50)
              balloon["color"] = random.choices(BALLOON_COLORS ,weights = colors_weights , k=1)[0]
              if seconds > 0 :
                 balloon["speed"] = random.uniform(7,10 )
              if seconds > 20 :
                 balloon["speed"] = random.uniform(11,13 )
              if seconds > 40 :
                 balloon["speed"] = random.uniform(14 , 16)
              if seconds > 60 :
                 balloon["speed"] = random.uniform(16 , 18)
                

             colored_balloon = balloon_image.copy()


             colored_balloon.fill(
              balloon["color"],
              special_flags=pygame.BLEND_MULT
             )

             if starting == True and ending == False  : # شاشة اللعب و شرط التلامس
              screen.blit(colored_balloon,(int(balloon["x"]- balloon_image.get_width() / 2 ),int(balloon["y"]- balloon_image.get_height() / 2)))

             arrow_rect = arrow.get_rect(center=(arrow_x, arrow_y))
             balloon_rect = pygame.Rect(balloon["x"] - 60,balloon["y"] - 70,120,100)
             if  starting == True and  ending == False and arrow_rect.colliderect(balloon_rect) and balloon["color"] > (0,0,0) :
                     score = score + 1
                     arrow_y= HEIGHT-62
                     pop.play()
                     balloon["y"] =  random.randint(400, 450)
                     balloon["x"] = random.randint( 50,WIDTH - 50)
                     balloon["color"] = random.choices(BALLOON_COLORS ,weights = colors_weights , k=1)[0]
                     is_shooting = False
             if  starting == True and  ending == False and arrow_rect.colliderect(balloon_rect) and balloon["color"] == (0,0,0) :
                                  score = score - 1
                                  arrow_y= HEIGHT-62
                                  black_pop.play()
                                  balloon["y"] =  random.randint(400, 450)
                                  balloon["x"] = random.randint( 50,WIDTH - 50)
                                  balloon["color"] = random.choices(BALLOON_COLORS ,weights = colors_weights , k=1)[0]
                                  is_shooting = False
    if starting == True and ending == False :     
     screen.blit(score_text, (1400, 25))
     screen.blit(current_time_text, (1400, 70))

    pygame.display.update()  


    if score == -5 :
            starting=False 
            ending = True
            score = 0 
            seconds = 0
            Losing_sound.play()

    if seconds > 60 and score < 15 :
        start_time = pygame.time.get_ticks()
        starting=False 
        ending = True
        score = 0 
        seconds=0
        Losing_sound.play()


    if score == 5:
        starting = True
        ending = True 
        score = 0 
        Victory_Sound.play()


    if cv2.waitKey(1) & 0xFF == 27:
             running = False

    clock.tick(60)    # سرعة اللعبة


cap.release()

cv2.destroyAllWindows()

detector.close()

pygame.quit()