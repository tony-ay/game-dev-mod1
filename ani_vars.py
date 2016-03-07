from utils import *

class ani_var:
	def __init__(self,frame_ct,img_W,img_H,time_between_frames):
		self.frame_ct=frame_ct
		self.img_H=img_H
		self.img_W=img_W
		self.time_between_frames=time_between_frames
		self.time_since_last_frame=0
		self.frame=0

	def update(self, time_diff):
		self.time_since_last_frame+=time_diff

	def get_time_since_last_frame(self):
		return self.time_since_last_frame

	def get_img_H(self):
		return self.img_H
		
	def get_img_W(self):
		return self.img_W