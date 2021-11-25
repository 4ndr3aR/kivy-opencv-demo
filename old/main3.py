import os

import cv2

import kivy

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.utils import platform


#from kivy.uix import vkeyboard

#print(dir(vkeyboard))
#print(vkeyboard.layout)




class KivyCamera(Image):
    def __init__(self, capture=None, fps=0, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        capturefile = 'http://deeplearning.ge.imati.cnr.it/genova-5G/video/VID_20211031_162912.mp4-inference.mp4'
        capturefile = 'VID_20211031_162912.mp4-inference.mp4'
        #capturefile = 'sample_960x400_ocean_with_audio.mjpeg'
        # self.capture = cv2.VideoCapture("/sdcard2/python-apk/2.mp4")
        print("file path exist :" + str(os.path.exists(capturefile)))
        self.capture = cv2.VideoCapture(capturefile)
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        print(f'platform: {platform} - {kivy.platform}')
        '''
        if platform == 'android':
            print(str(os.listdir('/bin')))
            #print(str(os.listdir('/storage/emulated/0')))
        else:
            print(str(os.listdir('/bin')))
        '''
        if ret:
            # convert it to texture
            print(f'Showing frame: {frame.shape}')
            if platform == 'android':
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            buf1 = cv2.flip(gray, 0)
            buf = buf1.tostring()
            '''
            '''
            print(f'Showing gray: {gray.shape}')
            image_texture = Texture.create(size=(gray.shape[1], gray.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
        else:
            print(f'Nothing to show here! {ret}')


class CamApp(App):
    def build(self):
        self.my_camera = KivyCamera(fps=30)
        self.box = BoxLayout(orientation='vertical')
        btn1 = Button(text="Hello")
        self.box.add_widget(btn1)
        # l = Label(text=cv2.__version__, font_size=150)
        # self.box.add_widget(l)
        self.box.add_widget(self.my_camera)
        return self.box

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        # self.capture.release()
        pass

    def on_pause(self):
        return True


if __name__ == '__main__':
    CamApp().run()
