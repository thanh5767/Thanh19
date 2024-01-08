import pygame
import math,random

class Bullet():
	def __init__(self,game,entity_pos,target_pos,num):
		self.game = game
		self.pos = [entity_pos[0],entity_pos[1]]
		self.target_pos = target_pos
		self.image = self.game.assets['bullet'][num]
		self.alive = True
		self.shoot = False
		self.angle = math.atan2(self.pos[1] - self.target_pos[1],self.pos[0] - self.target_pos[0])
		self.speed = 15
		self.vel_x = math.cos(self.angle)
		self.vel_y = math.sin(self.angle)
		rel_center = (self.target_pos[0] - self.pos[0], self.target_pos[1] - self.pos[1])
		angle = (1 if self.game.player.flip else -1)*math.degrees(math.atan2(rel_center[1], rel_center[0]))
		self.image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(90 if self.game.player.flip else -90)),angle),self.game.player.flip,False)
		self.rotate_rect = self.image.get_rect(center=self.pos)
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1],self.image.get_width(),self.image.get_height())
	def update(self,tile_map):
		for rect in tile_map.get_rect_tile(self.rotate_rect.center):
			if rect.collidepoint(self.rotate_rect.center):
				self.speed = 0
	def render(self,surf,offset,object_to_draw,tile_map):
		self.pos[0] -= (self.vel_x*self.speed)
		self.pos[1] -= (self.vel_y*self.speed)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		self.update(tile_map)
		# pygame.draw.rect(surf,'red',(self.rotate_rect.x - offset[0],self.rotate_rect.y - offset[1],self.rotate_rect.width,self.rotate_rect.height))
		object_to_draw.append([self.image, self.rotate_rect])
class Arrow(Bullet):
	def __init__(self,game,entity_pos,target_pos):
		super().__init__(game,entity_pos,target_pos,0)
	
	def render(self,surf,offset,object_to_draw,tile_map):
		self.speed = max(0,self.speed - 0.25)
		super().render(surf,offset,object_to_draw,tile_map)
class Pistol_bullet(Bullet):
	def __init__(self,game,entity_pos,target_pos):
		super().__init__(game,entity_pos,target_pos,1)
	
	def render(self,surf,offset,object_to_draw,tile_map):
		super().render(surf,offset,object_to_draw,tile_map)

class Slash():
	def __init__(self,game,size,color,alive_time,entity_pos,target):
		self.game = game
		self.pos = [entity_pos[0],entity_pos[1]]
		self.target = target
		self.size = size
		self.color = color
		if target.__class__.__name__ == 'Player':
			self.angle = math.atan2(self.pos[1] - self.target.pos[1],self.pos[0] - self.target.pos[0])
		else:
			self.angle = math.atan2(self.pos[1] - self.target[1],self.pos[0] - self.target[0])
		self.speed = 10
		self.vel_x = math.cos(self.angle)
		self.vel_y = math.sin(self.angle)
		self.image = pygame.Surface((self.size,self.size))
		self.img_size = self.image.get_size()
		pygame.draw.circle(self.image,self.color,(self.img_size[0]//2,self.img_size[1]//2),self.img_size[0]//2)
		pygame.draw.circle(self.image,'black',(self.img_size[0]//2,self.img_size[1]//2 + self.img_size[1]//4),self.img_size[0]//2)
		self.image.set_colorkey((0,0,0))
		if target.__class__.__name__ == 'Player':
			rel_center = (self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1])
		else:
			rel_center = (self.target[0] - self.pos[0], self.target[1] - self.pos[1])
		angle = (1 if self.game.player.flip else -1)*math.degrees(math.atan2(rel_center[1], rel_center[0]))
		self.image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(90 if self.game.player.flip else -90)),angle),self.game.player.flip,False)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		self.alive = True
		self.alive_time = alive_time
		self.damage = 10
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1],self.image.get_width(),self.image.get_height())
	def update(self,tile_map):
		for rect in tile_map.get_rect_tile(self.rotate_rect.center):
			if rect.collidepoint(self.rotate_rect.center):
				self.speed = 0
	def perfect_collision(self,target):
		if target.__class__.__name__ == 'Player':
			mask1 = pygame.mask.from_surface(self.image)
			mask2 = pygame.mask.from_surface(target.animation.img())
			if mask2.overlap(mask1,(self.rotate_rect.x - target.rect().x,self.rotate_rect.y - target.rect().y + 24)):
				target.hp -= 1
				self.game.screen_shake = 10
				# self.game.slashs.remove(self)
		else:
			pass
	def render(self,surf,offset,object_to_draw,tile_map):
		self.pos[0] -= (self.vel_x*self.speed)
		self.pos[1] -= (self.vel_y*self.speed)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		# self.update(tile_map)
		object_to_draw.append([self.image, self.rotate_rect])
		if self.alive:
			self.alive_time = max(0,self.alive_time-0.25)
			self.image.set_alpha(200 * self.alive_time + 50)
		if self.alive_time == 0:
			self.alive = False

class Weapon():
	def __init__(self,game,number,entity,size,animate):
		self.game = game
		self.entity = entity
		self.size = size
		self.pos = [self.entity.rect().centerx,self.entity.rect().centery]
		self.number = number
		self.angle = 0
		self.image = pygame.Surface((self.game.assets['weapon'][self.number].get_width(),self.game.assets['weapon'][self.number].get_height()*2))
		self.image.blit(self.game.assets['weapon'][self.number],(0,0))
		if self.number != 6:
			pygame.draw.circle(self.image,'#2E7A5B',(self.image.get_width()//2 - 1,self.image.get_height()//2 - 2),2)
			pygame.draw.circle(self.image,'#222034',(self.image.get_width()//2 - 1,self.image.get_height()//2 - 2),3,1)
		self.image.set_colorkey((0,0,0))
		self.stop = False
		self.animate = animate
	def rect(self,target):
		# print(target)
		if target.__class__.__name__ == 'Player':
			rel_center = (target.pos[0] - self.pos[0],target.pos[1] - self.pos[1])
		else:
			rel_center = (target[0] - self.pos[0],target[1] - self.pos[1])
		if self.stop:
			pass
		else:
			self.angle = (1 if self.entity.flip else -1)*math.degrees(math.atan2(rel_center[1], rel_center[0]))
		if self.animate:
			self.rotated_image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(180 if self.entity.flip else 0)),self.angle),self.entity.flip,False)
		else:
			self.rotated_image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(90 if self.entity.flip else -90)),self.angle),self.entity.flip,False)
		self.rotated_rect = self.rotated_image.get_rect(center=self.pos)
		return [self.rotated_image, self.rotated_rect]
	def render(self,surf,offset,object_to_draw,target):
		object_to_draw.append(self.rect(target))
class Bare_hands(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,6,entity,size,True)
		self.time_slash = 0
	def slash(self,event,target):
		if event.button == 1 and self.time_slash == 0:
			
			test_slash = Slash(self.game,30,'white',2,self.game.player.weapon.rect(target)[1].center,self.game.mouse_pos)
			self.time_slash = test_slash.alive_time
			test_slash.speed = 1.3
			self.game.slashs.append(test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)
class Wood_sword(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,0,entity,size,True)
		self.time_slash = 0
	def slash(self,event,target):
		if event and self.time_slash == 0:
			test_slash = Slash(self.game,50,'white',2,self.entity.weapon.rect(target)[1].center,target)
			self.time_slash = test_slash.alive_time
			test_slash.speed = 3
			self.game.slashs.append(test_slash)
	def render(self,surf,offset,object_to_draw,target):

		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)
class Wood_axe(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,1,entity,size,True)
		self.time_slash = 0
	def slash(self,event,target):
		if event.button == 1 and self.time_slash == 0:
			test_slash = Slash(self.game,40,'white',2,self.entity.weapon.rect(target)[1].center,self.game.mouse_pos)
			self.time_slash = 2
			test_slash.speed = 0
			self.game.slashs.append(test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)
class Wood_pickaxe(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,2,entity,size,True)
		self.time_slash = 0
	def slash(self,event,target):
		if event.button == 1 and self.time_slash == 0:
			
			test_slash = Slash(self.game,40,'white',2,self.entity.weapon.rect(target)[1].center,self.game.mouse_pos)
			self.time_slash = 2
			test_slash.speed = 0
			self.game.slashs.append(test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)
class Bow(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,3,entity,size,False)
		self.charge = 0
		self.ratio = 0
	def charge_shoot(self):
		if pygame.mouse.get_pressed()[0]:
			self.charge = min(20,self.charge + 0.25)
			# pygame.draw.line(self.game.display,'green',(self.rect()[1].centerx - self.game.true_scroll[0],self.rect()[1].centery - self.game.true_scroll[1]),(self.game.mouse_pos[0] - self.game.true_scroll[0],self.game.mouse_pos[1] - self.game.true_scroll[1]),1)

		else: self.charge = 0
		self.ratio = self.charge/20
	def shoot_arrow(self,event,target):
		if self.charge >= 5:
			if event.button == 1:
				arrow = Arrow(self.game,self.rect(target)[1].center,self.game.mouse_pos)
				arrow.speed = self.charge
				self.game.bullets.append(arrow)
				self.charge = 0

	def render(self,surf,offset,object_to_draw,target):
		super().render(surf,offset,object_to_draw,target)
		pygame.draw.rect(surf,'#C7CBD1',(self.game.player.pos[0] - offset[0],self.game.player.pos[1] - offset[1] - 20,self.game.player.rect().width,2))
		pygame.draw.rect(surf,'#303841',(self.game.player.pos[0] - offset[0],self.game.player.pos[1] - offset[1] - 20,self.game.player.rect().width*self.ratio,2))

class Spear(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,4,entity,size,False)
		self.charge = 0
		self.ratio = 0
		self.time_slash = 0
		self.test_slash = None

	def slash(self,event,target):
		if event and self.time_slash == 0:
			self.test_slash = Slash(self.game,50,'red',2,self.entity.weapon.rect(target)[1].center,target)
			self.time_slash = self.test_slash.alive_time
			# test_slash.size = (self.charge * 4)
			# self.game.slashs.append(self.test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.pos = list(self.pos)
			self.pos[0] -= self.test_slash.vel_x*7
			self.pos[1] -= self.test_slash.vel_y*7
		super().render(surf,offset,object_to_draw,target)
class Katana(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,5,entity,size,True)
		self.time_slash = 0
		self.test_slash = None
		self.distance = 100
	def slash(self,event,target):
		if event and self.time_slash == 0:
			self.test_slash = Slash(self.game, 50, 'red', 5, self.entity.weapon.rect(target)[1].center, target)
			self.time_slash = 2
			self.test_slash.speed = 5
			self.game.slashs.append(self.test_slash)


	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			# self.entity.pos[0] -= self.test_slash.vel_x * 2
			# self.entity.pos[1] -= self.test_slash.vel_y * 2
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)
class Pistol(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,7,entity,size,False)
		self.charge = 0
		self.ratio = 0
	def charge_shoot(self):
		if pygame.mouse.get_pressed()[0]:
			self.charge = min(20,self.charge + 0.25)
			# pygame.draw.line(self.game.display,'green',(self.rect()[1].centerx - self.game.true_scroll[0],self.rect()[1].centery - self.game.true_scroll[1]),(self.game.mouse_pos[0] - self.game.true_scroll[0],self.game.mouse_pos[1] - self.game.true_scroll[1]),1)

		else: self.charge = 0
		self.ratio = self.charge/20
	def shoot_bullet(self,event,target):
		
		arrow = Pistol_bullet(self.game,self.rect(target)[1].center,self.game.mouse_pos)
		arrow.speed = 20
		self.game.bullets.append(arrow)

	def render(self,surf,offset,object_to_draw,target):
		super().render(surf,offset,object_to_draw,target)

