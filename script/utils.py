import os
import pygame
import random
from datetime import datetime

def load_image(path):
		
	img = pygame.image.load('image/' + path).convert_alpha()
	# img.set_colorkey((0,0,0))
	return img
	
def extract_order_number(file_name):
	try:
		# Trích xuất số thứ tự từ tên tệp
		return int(''.join(filter(str.isdigit, file_name)))
	except ValueError:
		return float('inf')  # Trả về vô cùng nếu không thể trích xuất số thứ tự

def load_images(path):
	images = []
	# Lấy danh sách các tệp trong thư mục
	files = os.listdir('image/' + path)
	# Sắp xếp các tệp dựa trên số thứ tự
	files = sorted(files, key=extract_order_number)
	for image_name in files:
		if not image_name.startswith('.'):
			images.append(load_image(path + '/' + image_name))
	return images


class Animation:
	def __init__(self,images,dur = 5,loop = True):
		self.images = images
		self.duration = dur
		self.loop = loop
		self.done = False
		self.frame = 0
	def copy(self):
		return Animation(self.images,self.duration,self.loop)
	def update(self):
		if self.loop:
			self.frame = (self.frame + 1) % (self.duration * len(self.images))
		else:
			self.frame = min(self.frame + 1,self.duration * len(self.images) - 1)
			if self.frame >= self.duration * len(self.images) -1:
				self.done = True
	def img(self):
		return self.images[int(self.frame/self.duration)]

class DayNight:
	def __init__(self,game):
		self.game = game
		self.display_surf = pygame.Surface((self.game.display.get_size()[0],self.game.display.get_size()[1]))
		self.start_color = [255,255,255]
		self.end_color = (38,101,189)
		# self.end_color = (38,38,38)
		self.reset_color = [255,255,255]
		self.current_time = int(datetime.now().strftime('%M'))
		self.stat = 'day'
	def lightning(self,pos,offset,dt):
		
		for i,value in enumerate(self.start_color):
				if self.start_color[i] > self.end_color[i] and self.stat == 'day':
					self.start_color[i] -= 2 * dt
					if self.start_color[0] <= 38:
						self.stat = 'night'
				elif self.start_color[i] < self.reset_color[i] and self.stat == 'night':
					self.start_color[i] += 2 * dt
					if self.start_color[0] >= 255:
						self.stat = 'day'
			
		self.display_surf.fill(self.start_color)
		# if self.stat == 'night':
		# self.display_surf.blit(self.game.assets['light'],(pos[0] - offset[0],pos[1] - offset[1]),special_flags = pygame.BLEND_RGB_ADD)
	def render(self):
		self.game.display.blit(self.display_surf,(0,0),special_flags = pygame.BLEND_MULT)
class Button():
	def __init__(self,img,pos,size):
		self.img = img
		self.pos = pos
		self.size = size
		self.reset_pos = self.pos[0]
		self.start_pos = self.pos[0] - 200
		self.clicked = False
		self.max_scale = self.size[0] + 10
		self.default_scale = self.size[0]
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
	def animate(self):
		if self.pos[0] < self.reset_pos:
			self.pos[0] += 10
	def scale_button(self):
		if self.size[0] < self.max_scale:
			self.size[0] *= 1.1
		return self.size[0]
	def draw(self,surf):
		action = False
		rect = self.rect()
		m_pos = pygame.mouse.get_pos()
		if rect.collidepoint((m_pos[0]//2,m_pos[1]//2)):
			self.size[0] = int(self.scale_button())
			self.img.set_alpha(235)
			if pygame.mouse.get_pressed()[0]and self.clicked == False:
				self.clicked = True
				action = True
		else:
			self.size[0] = self.default_scale
			self.img.set_alpha(255)
		if pygame.mouse.get_pressed()[0]:
			self.clicked = False
		self.animate()
		surf.blit(pygame.transform.scale(self.img,(self.size[0],self.size[1])),(self.pos[0],self.pos[1]))
		# pygame.draw.rect(surf,'red',rect)

		return action
class Hot_bar():
	def __init__(self,game,pos,size,tile_size,variant):
		self.game = game
		self.pos = pos
		self.size = size
		self.tile_size = tile_size
		self.grid = {}
		self.x_move = pos[0]
		self.y_move = pos[1]
		self.default_status(variant)
	def default_status(self,variant):
		for x in range(self.size[0]//self.tile_size):
			for y in range(self.size[1]//self.tile_size):
				key = (x + self.x_move,y + self.y_move)
				if key not in self.grid:
					self.grid[key] = {'type':'menu','variant':variant,'pos':(x + self.x_move,y + self.y_move)}
	
	def render(self,surf):
		for til in self.grid:
			tile = self.grid[til]
			surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0]*self.tile_size,tile['pos'][1]*self.tile_size))
class Inventory_icon(Hot_bar):
	def __init__(self,game,pos,size,tile_size):
		super().__init__(game,pos,size,tile_size,6)

	def check_mouse(self,pos,event):
		action = False
		loc = (pos[0] // self.tile_size//2,pos[1]//self.tile_size//2)
		if loc in self.grid:
			if self.grid[loc]['type'] == 'menu' and self.grid[loc]['variant'] == 6:
				if event.button == 1:
					action = True
					self.grid[loc]['variant'] = 7
			elif self.grid[loc]['type'] == 'menu' and self.grid[loc]['variant'] == 7:
				if event.button == 1:
					action = True
					self.grid[loc]['variant'] = 6
		return action
	def render(self,surf):
		super().render(surf)
class Setting_icon(Hot_bar):
	def __init__(self,game,pos,size,tile_size):
		super().__init__(game,pos,size,tile_size,5)
	def check_mouse(self,pos,event):
		action = False
		loc = (pos[0] // self.tile_size//2,pos[1]//self.tile_size//2)
		if loc in self.grid:
			if self.grid[loc]['type'] == 'menu' and self.grid[loc]['variant'] == 5:
				if event.button == 1:
					action = True
			
		return action
	def render(self,surf):
		super().render(surf)
