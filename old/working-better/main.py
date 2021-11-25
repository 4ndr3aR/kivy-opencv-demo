from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
import numpy as np
import cv2

Builder.load_file("myapplayout.kv")

class AndroidCamera(Camera):
    camera_resolution = (640, 480)
    counter = 0

    def _camera_loaded(self, *largs):
        #self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgb')
        self.texture = Texture.create(size=self.camera_resolution, colorfmt='rgb')
        self.texture_size = list(self.texture.size)
        print(f'Created GL texture with size: {self.texture_size}')

    def on_tex(self, *l):
        if self._camera._buffer is None:
            return None
        frame = self.frame_from_buf()
        self.frame_to_screen(frame)
        super(AndroidCamera, self).on_tex(*l)

    def frame_from_buf(self):
        w, h = self.resolution
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))	# original one
        #frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((w, h + h // 2))
        print(f'{frame.shape = }')
        #frame_bgr = cv2.cvtColor(frame, 93)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV21)
        #return np.rot90(frame_bgr, 3)
        return frame_bgr

    def frame_to_screen(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame_rgb, str(self.counter), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        self.counter += 1
        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tostring()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()
