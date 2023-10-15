import cv2 as cv
from os import system
from time import sleep
from threading import Thread, Lock

from soundPlayer import generateIntruderAlertSound, playCustomSound, durationOfAudioFileFromPath

faces_rect = []

generateIntruderAlertSound()

playSoundMutex = Lock()
playCustomSoundMutex = Lock()
sendIntruderAlertMutex = Lock()

textToPlay = ""


def playSound():
    while True:
        playSoundMutex.acquire()
        playCustomSoundMutex.acquire()
        duration = durationOfAudioFileFromPath("intruder.mp3")
        system("intruder.mp3")
        sleep(duration)
        playCustomSoundMutex.release()
        sleep(10)


# enable webcam
capture = cv.VideoCapture(0)

pre_trained_model = cv.CascadeClassifier('haar_face.xml')


def intruderDetection():
    sendIntruderAlertMutex.acquire()
    playSoundMutex.acquire()
    i = 0
    intruderDetected = False
    while True:
        isSuccessful, frame = capture.read()

        if isSuccessful:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces_rect = pre_trained_model.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=6)

            # send alert if face is first detected
            if len(faces_rect) > 0 and sendIntruderAlertMutex.locked():
                intruderDetected = True
                cv.imwrite("images/image.jpg", frame)
                sendIntruderAlertMutex.release()

            if not intruderDetected:
                pass

            # draw rectangle around the face
            for (x, y, w, h) in faces_rect:
                cv.rectangle(frame, (x, y), (x+w, y+h),
                             (0, 255, 0), thickness=2)

            # cv.imshow('Detected Faces', frame)

            # save image every 100 frames if face is detected
            if (i % 100 == 0) and (len(faces_rect) > 0):
                cv.imwrite(f"images/image{str(i//100)}.jpg", frame)
                cv.imwrite("images/image.jpg", frame)
            i = i + 1

            if len(faces_rect) > 0:
                if playSoundMutex.locked():
                    playSoundMutex.release()

            if cv.waitKey(20) == ord('x'):
                break


def customSound(text):
    playCustomSound(text)


soundThread = Thread(target=playSound, daemon=True)

intruderDetectionThread = Thread(target=intruderDetection, daemon=True)


def initThreads():
    intruderDetectionThread.start()
    soundThread.start()


def main():
    initThreads()
    while True:
        pass


if __name__ == '__main__':
    main()
