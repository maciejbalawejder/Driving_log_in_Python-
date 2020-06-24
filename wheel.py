import keyboard
import pygame
import pandas as pd
import numpy as np
import cv2
import pyautogui

pygame.init()

def main() :
    data_path = r"C:\Users\macie\Documents\GTA\log.csv"
    video_path = r"C:\Users\macie\Documents\GTA\check.avi"
    fps = 20.0

    # SETTING UP THE SCREEN RECORD
    screen = (1920, 1080)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, fps, (screen))

    # CREATING THE EMPTY LIST FOR DATA FROM STEERING WHEEL
    angle = ['Angle']
    gas = ['Gas']
    brake = ['Brake']

    joysticks = []
    clock = pygame.time.Clock()

    # FUNCTION TO RESHAPE LIST
    def convert(array) :
        array = np.asarray((array))
        array = array.reshape((-1,1))
        return array

    for i in range(0, pygame.joystick.get_count()) :

        joysticks.append(pygame.joystick.Joystick(i))

        joysticks[-1].init()

    while True :
        # SCREEN CAPTURE
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        if cv2.waitKey(1) == ord('q') :
            break

        # STEERING WHEEL CAPTURE
        clock.tick(float(1000 / fps))

        if keyboard.is_pressed('q'):

            angle = convert(angle)
            brake = convert(brake)
            gas = convert(gas)
            final = np.hstack((angle, gas, brake))
            final = pd.DataFrame(final)
            pd.DataFrame(final).to_csv(data_path)
            exit()
        else :
            pass
        for event in pygame.event.get() :
            if event.type == pygame.JOYAXISMOTION :
                angles = pygame.joystick.Joystick(0).get_axis(0)
                print('Angle : {}'.format(pygame.joystick.Joystick(0).get_axis(0)))
                angle.append(angles)

                brakes = (pygame.joystick.Joystick(0).get_axis(1) - 1) / 2
                print('Brake : {}'.format(brakes))
                brake.append(brakes)

                gass = 1 - ((pygame.joystick.Joystick(0).get_axis(3) + 1) / 2)
                print('Gas : {}'. format(gass))
                gas.append(gass)

print('Press s to start : ')
keyboard.wait('s')
print('Here we go')
print('Press q to finish')
main()
