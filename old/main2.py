import kivy

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, NumericProperty

from kivy.logger import Logger

import cv2

class KivyCamera(Image):
	source = ObjectProperty()
	fps = NumericProperty(30)

	def __init__(self, **kwargs):
		super(KivyCamera, self).__init__(**kwargs)
		self._capture = None
		if self.source is not None:
			self._capture = cv2.VideoCapture(self.source)

		Clock.schedule_interval(self.update, 1.0 / self.fps)

	def on_source(self, *args):
		if self._capture is not None:
			self._capture.release()
		self._capture = cv2.VideoCapture(self.source)

	@property
	def capture(self):
		return self._capture

	def update(self, dt):
		ret, frame = self.capture.read()
		if ret:
			buf1 = cv2.flip(frame, 0)
			print(f'Showing frame: {frame.shape}')
			buf = buf1.tostring()
			offset = 0
			if kivy.platform == 'android':
				offset = 4
			image_texture = Texture.create(
				size=(frame.shape[1]+offset, frame.shape[0]+offset), colorfmt="bgr"
			)
			image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
			self.texture = image_texture
		else:
			print(f'OpenCV failed to get frame: {int(ret)}')


class CamApp(App):
	pass


if __name__ == "__main__":
	print('KivyCamera class: ', KivyCamera)
	CamApp().run()
