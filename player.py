import cv2
import pyaudio
import pygame
import wave
import subprocess
import os


video_name = 'pina.mp4'
all_song = []


def save_audio():
    command = f"ffmpeg -i {video_name} -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    subprocess.call(command, shell=True)


def get_audio():
    global stream

    wf = wave.open("audio.wav", "rb")

    print(wf.getsampwidth(), wf.getframerate(), wf.getnchannels(), wf.getnframes())

    CHUNK = wf.getframerate() // fps
    print(CHUNK)

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data:
        all_song.append(data)
        data = wf.readframes(CHUNK)

    os.remove('audio.wav')


if __name__ == '__main__':

    global stream, fps

    cap = cv2.VideoCapture(video_name)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print('fps =', fps)

    save_audio()
    get_audio()

    clock = pygame.time.Clock()

    ind = 0

    while cap.isOpened():
        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        stream.write(all_song[ind])
        ind += 1

        clock.tick(fps)

        print(clock.get_fps())


    cap.release()
    cv2.destroyAllWindows()