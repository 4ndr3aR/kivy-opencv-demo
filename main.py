import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import ObjectProperty, NumericProperty

import numpy as np
import cv2

#Builder.load_file("myapplayout.kv")




class KivyCamera(Image):
	if kivy.platform == 'android':
		image_resolution = (544, 544)
	else:
		image_resolution = (540, 540)
	source = ObjectProperty()
	fps = NumericProperty(60)
	counter = 0
	#texture = ObjectProperty()
	#.texture_size = ObjectProperty()

	def __init__(self, **kwargs):
		super(KivyCamera, self).__init__(**kwargs)
		self._capture = None
		if self.source is not None:
			self._capture = cv2.VideoCapture(self.source)
		print('asdf')

		Clock.schedule_interval(self.update, 1.0 / self.fps)

	def create_texture(self):
		#self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgb')
		self.texture = Texture.create(size=self.image_resolution, colorfmt='rgb')
		self.texture_size = list(self.texture.size)
		print(f'Created GL texture with size: {self.texture_size}')

	def on_source(self, *args):
		if self._capture is not None:
			self._capture.release()
		self._capture = cv2.VideoCapture(self.source)

	@property
	def capture(self):
		return self._capture

	def update(self, dt):
		ret, frame = self.capture.read()
		print(f'GL texture is {self.texture} - size: {self.texture_size}')
		if ret:
			self.create_texture()
			#frame = self.frame_from_buf()
			print(f'Showing frame: {frame.shape}')
			self.frame_to_screen(frame)
			'''
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
			'''
		else:
			print(f'OpenCV failed to get frame: {int(ret)}')

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
		if kivy.platform == 'android':
			frame_rgb = frame
		else:
			frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		cv2.putText(frame_rgb, str(self.counter), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
		if self.counter == 0:
			print(f'frame_rgb: {frame_rgb[:3]}')
		self.counter += 1
		'''
		if kivy.platform == 'android':
			buf = frame_rgb.tostring()
		else:
			flipped = np.flip(frame_rgb, 0)
			buf = flipped.tostring()
		'''
		flipped = np.flip(frame_rgb, 0)
		buf = flipped.tostring()
		self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

class CamApp(App):
	pass


Builder.load_file("cam.kv")





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
	#MyApp().run()
	CamApp().run()


