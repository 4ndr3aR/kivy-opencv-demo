import kivy

from kivy.app import App
from kivy.core.window import Window
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

media_source = 'video'
#media_source = 'camera'			# remember to manually grant permissions for this!

class KivyCamera(Image):
	screen_resolution = (544, 544)
	if kivy.platform == 'android':
		image_resolution = (544, 544)
	else:
		image_resolution = (540, 540)

	source = ObjectProperty()
	fps = NumericProperty(60)
	counter = 0
	debug = 0

	def __init__(self, **kwargs):
		super(KivyCamera, self).__init__(**kwargs)
		self._capture = None
		if self.source is not None:
			self._capture = cv2.VideoCapture(self.source)

		self.screen_resolution = Window.size
		print(f'Screen size: {Window.size}, setting new screen resolution to: {self.screen_resolution}')

		Clock.schedule_interval(self.update, 1.0 / self.fps)

	def create_texture(self):
		self.texture = Texture.create(size=self.screen_resolution, colorfmt='rgb')
		self.texture_size = list(self.texture.size)
		if self.debug:
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
		if self.debug:
			print(f'GL texture is {self.texture} - size: {self.texture_size}')
		if ret:
			self.create_texture()
			if self.counter < 5:
				print(f'Showing frame: {frame.shape}')
			self.frame_to_screen(frame)
		else:
			print(f'OpenCV failed to get frame: {int(ret)}')

	def frame_to_screen(self, frame):
		if kivy.platform == 'android':
			frame_rgb = frame
		else:
			frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		cv2.putText(frame_rgb, str(self.counter), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
		if self.counter == 0:
			print(f'frame_rgb: {frame_rgb[:3]}')
		self.counter += 1
		flipped = np.flip(frame_rgb, 0)
		if self.screen_resolution != self.image_resolution:
			aspect_ratio = self.image_resolution[0] / self.image_resolution[1]
			if self.counter < 5:
				print(f'{aspect_ratio = }')
			flipped = cv2.resize(flipped, (int(self.screen_resolution[1]*aspect_ratio), self.screen_resolution[1]))	# I know, this one takes into account one case out of four or more (TODO)
			self.screen_resolution = (int(self.screen_resolution[1]*aspect_ratio), self.screen_resolution[1])
			if self.counter < 5:
				print(f'Screen resolution != image resolution with aspect ratio: {aspect_ratio}, setting new screen resolution to: {self.screen_resolution}')
		buf = flipped.tostring()
		self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

class CamApp(App):
	pass







class AndroidCamera(Camera):
	camera_resolution = (640, 480)
	counter = 0

	def _camera_loaded(self, *largs):
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
		frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))	# TODO: try to understand why the frame size has nothing to do with the original resolution
		print(f'{frame.shape = }')
		frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV21)
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
	if media_source == 'video':
		Builder.load_file("cam.kv")
		CamApp().run()
	else:
		Builder.load_file("myapplayout.kv")
		MyApp().run()


