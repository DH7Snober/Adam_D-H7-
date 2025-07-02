import cv2
import numpy as np
from sklearn.linear_model import LinearRegression
import speech_recognition as sr
import pyttsx3

# Fonksyon pale
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Fonksyon chatbot
def chatbot():
    print("Ekri 'sòti' pou sòti nan chat.")
    while True:
        msg = input("Ou: ")
        if msg.lower() == "sòti":
            break
        elif "non" in msg:
            print("AI: Mwen rele TF-AI.")
        elif "kijan ou ye" in msg:
            print("AI: Mwen anfòm, mesi!")
        else:
            print("AI: M pa konprann sa, men m ap aprann.")

# Fonksyon vwa
def voice_ai():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Koute...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ht-HT")
            print("Ou di:", text)
            if "non" in text:
                speak("Mwen se TF-AI")
            elif "kijan ou ye" in text:
                speak("Mwen anfòm, mesi")
            else:
                speak("M pa konprann, repete tanpri")
        except:
            speak("M pa t ka tande byen.")

# Fonksyon jwèt: tictactoe AI
def game_ai():
    print("AI ap jwe tictactoe kont tèt li.")
    board = [" "] * 9

    def show():
        print("\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)]))

    def move(player):
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                break

    for _ in range(5):
        move("O")
        show()
        move("X")
        show()

# Fonksyon kamera (rekonesans figi)
def vision_ai():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("Peze 'q' pou sòti.")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow('Vizion AI', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Fonksyon prediksyon senp
def predictor_ai():
    print("Prediksyon pri vs laj.")
    X = np.array([[5], [10], [15], [20], [25]])
    y = np.array([50, 100, 150, 200, 250])

    model = LinearRegression()
    model.fit(X, y)

    try:
        laj = int(input("Antre laj pou predi pri: "))
        pred = model.predict([[laj]])
        print(f"Pri predi a se: ${int(pred[0])}")
    except:
        print("Sòti nonb valab tanpri.")

# Meni prensipal
while True:
    print("\nKisa ou vle AI a fè?\n1. Chat\n2. Tande vwa\n3. Jwe jwèt\n4. Kamera\n5. Prediksyon\n6. Sòti")
    chwa = input("Antre chwa w: ")

    if chwa == "1":
        chatbot()
    elif chwa == "2":
        voice_ai()
    elif chwa == "3":
        game_ai()
    elif chwa == "4":
        vision_ai()
    elif chwa == "5":
        predictor_ai()
    elif chwa == "6":
        break
    else:
        print("Chwa pa rekonèt.")
