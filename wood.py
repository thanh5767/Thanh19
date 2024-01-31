import pygame
import sys,random,time
from math import sin
from datetime import datetime
from script.utils import load_image,load_images,Animation,DayNight,Hot_bar,Inventory_icon,Setting_icon,Health_bar,Energy_bar
from script.entity import Physical_Entity,Player,Bunhin,Item,Pink,Homeless,Tree,Block,Tile_func
from script.weapon import Weapon,Wood_sword,Wood_axe,Wood_pickaxe,Bow,Spear,Katana,Bare_hands,Pistol,Energy_sword,Energy_bow
from script.tile_map import Tile_map
from script.inventory import Inventory,Chest_inventory
from script.setting import weapon_type,block_list_l2,block_list_l3,nblock_list,item_id,no_block_item,layer,font_1
class Game():
	def __init__(self):
		pygame.init()
		self.monitorsize = [pygame.display.Info().current_w,pygame.display.Info().current_h]
		self.screen = pygame.display.set_mode((self.monitorsize),pygame.DOUBLEBUF)
		self.display = pygame.Surface((self.screen.get_size()[0]//2,self.screen.get_size()[1]//2))
		self.clock = pygame.time.Clock()
		self.movement = [False,False,False,False]
		self.tile_map = Tile_map(self,tile_size = 24)
		self.scroll = [0,0]
		self.assets = {
		'grass': load_images('grass'),
		'solid_dirt': load_images('solid_dirt'),
		'sand': load_images('sand'),
		'tree': load_images('tree'),
		'player/idle': Animation(load_images('entity/player/idle'),dur = 5,loop = True),
		'player/run': Animation(load_images('entity/player/run'),dur = 3,loop = True),
		'player2/idle': Animation(load_images('entity/player2/idle'),dur = 5,loop = True),
		'player2/run': Animation(load_images('entity/player2/run'),dur = 3,loop = True),
		'dafluffy/idle': Animation(load_images('entity/dafluffy/idle'),dur = 5,loop = True),
		'dafluffy/run': Animation(load_images('entity/dafluffy/run'),dur = 3,loop = True),
		'pink/idle': Animation(load_images('entity/pink/idle'),dur = 5,loop = True),
		'pink/run': Animation(load_images('entity/pink/run'),dur = 3,loop = True),
		'homeless/idle': Animation(load_images('entity/homeless/idle'),dur = 5,loop = True),
		'homeless/run': Animation(load_images('entity/homeless/run'),dur = 3,loop = True),
		'bunhin/idle': Animation(load_images('entity/bunhin/idle'),dur = 5,loop = True),
		'bunhin/run': Animation(load_images('entity/bunhin/run'),dur = 3,loop = True),
		'stone': load_images('stone'),
		'solid_stone': load_images('solid_stone'),
		'wood_block': load_images('wood_block'),
		'water': load_images('water'),
		'solid_water': load_images('solid_water'),
		'fence': load_images('fence'),
		'flower': load_images('flower'),
		'wood_slab': load_images('wood_slab'),
		'wood_wall': load_images('wood_wall'),
		'torch': load_images('torch'),
		'rock': load_images('rock'),
		'fence_stake': load_images('fence_stake'),
		'sand_stone': load_images('sand_stone'),
		'test' : load_images('stone')[0],
		'box': load_images('box'),
		'chest': load_images('chest'),
		'menu':load_images('menu'),
		'weapon':load_images('weapon'),
		'bullet':load_images('bullet'),
		'item':load_images('item'),
		'cusor':load_images('cusor'),
		'light':load_images('light'),
		}
		self.font = pygame.font.SysFont('minecraft',int(self.monitorsize[0]/192))
		self.player = Player(self,[0,0],[16,6])
		self.player.health_bar = Health_bar((self.player.tool_bar.x_move*30,self.player.tool_bar.y_move*30 - 20),[75,10],self.player.hp,self.player.max_hp)
		self.player.energy_bar = Energy_bar((self.player.tool_bar.x_move*30 + 90,self.player.tool_bar.y_move*30 - 20),[75,10],self.player.energy,self.player.max_energy)
		self.weapon_class = {
		'wood_sword':Wood_sword(self,self.player,[24,24]),
		'wood_axe': Wood_axe(self,self.player,[24,24]),
		'wood_pickaxe': Wood_pickaxe(self,self.player,[24,24]),
		'bow': Bow(self,self.player,[24,24]),
		'spear': Spear(self,self.player,[24,24]),
		'katana': Katana(self,self.player,[24,24]),
		'bare_hand': Bare_hands(self,self.player,[24,24]),
		'pistol': Pistol(self,self.player,[24,24]),
		'energy_sword':Energy_sword(self,self.player,[24,24]),
		'energy_bow':Energy_bow(self,self.player,[24,24]),
		}
		self.player.weapon = self.weapon_class['bare_hand']
		self.elite_group = []
		self.animals = []
		self.enemies = []
		self.item_group = []
		# for i in range(10):
		# 	# daff = Dafluffy(self,[0,0],[12,4])
		# 	# daff.weapon = Katana(self,daff,[24,24])
		# 	# self.elite_group.append(daff)
		# 	# self.animals.append(Pink(self,[0,0],[24,24]))
		# 	homeless = Homeless(self,[random.randint(-300,300),random.randint(-300,300)],[16,6])
		# 	homeless.target = self.player
		# 	homeless.weapon = Wood_axe(self,homeless,[48,48])
		# 	self.enemies.append(homeless)
		bunhin = Bunhin(self,[random.randint(-300,300),random.randint(-300,300)],[16,6])
		bunhin.weapon = Wood_sword(self,bunhin,[48,48])
		self.enemies.append(bunhin)
		self.spawn_enemy = pygame.USEREVENT + 1
		pygame.time.set_timer(self.spawn_enemy,7000)
		self.tile_map.seed = random.randint(-5000,5000)
		# self.tile_map.seed = -170
		# self.tile_map.seed = 2000
		self.player_speed = 2
		self.daynight = DayNight(self)
		self.hold = None
		self.invent_icon = Inventory_icon(self,[0,1],[48,48],48)
		self.setting_icon = Setting_icon(self,[0,2],[48,48],48)
		self.use = {'type':0,'quantity':0}
		self.time = -10
		self.bullets = []
		self.slashs = []
		self.interact_tile = []
		self.screen_shake = 0
		self.block_click = False
		self.dig_click = False
		self.click_objcet = False
	def create_shadow(self,display, objects_to_draw, scroll,dt):
		shadow_surf = pygame.Surface(display.get_size())
		shadow_surf.fill((30,30,30))
		for obj in objects_to_draw:
			image, rect = obj[0], obj[1]
			if image not in self.assets['stone'] and image not in self.assets['sand_stone']:
				self.shadow_def(shadow_surf, image, rect,scroll,dt)
				shadow_surf.set_colorkey((30,30,30))
				shadow_surf.set_alpha(50)
		display.blit(shadow_surf, (0, 0))
	def create_shadow_optimize(self,display, objects_to_draw, scroll):
		shadow_surf = pygame.Surface(display.get_size(), pygame.SRCALPHA)
		for obj in objects_to_draw:
			image, rect = obj[0], obj[1]
			if image in self.assets['tree']:
				pygame.draw.ellipse(shadow_surf, (0, 0, 0, 50), (rect.x - scroll[0], rect.y - scroll[1] + rect.height // 1.25, rect.width, rect.height // 3))
			elif image in self.assets['stone'] or image in self.assets['wood_wall'] or image in self.assets['solid_stone'] or image in self.assets['chest'] or image in self.assets['wood_block']:
				pygame.draw.rect(shadow_surf, (0, 0, 0, 50), (rect.x - scroll[0], rect.y - scroll[1] + rect.height, rect.width, rect.height // 3))
		display.blit(shadow_surf, (0, 0))
	def draw_object(self,display,objects_to_draw,scroll,player):
		for obj in sorted(objects_to_draw,key = lambda obj:obj[1].bottom):
			image = obj[0]
			rect = obj[1]
			display.blit(image,(rect.x- scroll[0],rect.y -scroll[1]))
	def draw_text(self,text,font,color,surface,loc):
		surface.blit(font.render(text,1,color),(loc[0],loc[1]))
	def outline_tile(self,tile,num):
		mask = pygame.mask.from_surface(self.assets[tile['type']][tile['variant']])
		mask_surface = pygame.Surface((self.assets[tile['type']][tile['variant']].get_width(),self.assets[tile['type']][tile['variant']].get_height() + 1))
		if num == 0:
			mask_surface.blit(mask.to_surface(unsetcolor=(0,0,0,0),setcolor=(100,255,100,255)),(0,0))
			mask_surface.set_colorkey((0,0,0))
			mask_surface.set_alpha(60)
		elif num == 1:
			outline = [(p[0],p[1]) for p in mask.outline()]
			# value = max(0,sin(pygame.time.get_ticks()*0.01) * 255)
			pygame.draw.lines(mask_surface,(255,255,255),False,outline)
			mask_surface.set_colorkey((0,0,0))
		return mask_surface
	def main_menu(self):
		buttons = []
		for i in range(3):
			button = pygame.Rect(self.display.get_width()//2 - self.assets['menu'][0].get_width(),self.display.get_height()//2 + i*75,192,48)
			buttons.append(button)
		self.scroll = [0,0]
		while True:
			# self.screen_shader.render(self.display)
			# self.display.blit(pygame.transform.scale(self.assets['menu'][8],self.display.get_size()),(0,0))
			self.display.fill('black')
			mx,my = pygame.mouse.get_pos()
			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True
			img = pygame.mask.from_surface(pygame.transform.scale2x(self.assets['menu'][0]))
			self.display.blit(pygame.transform.scale2x(self.assets['menu'][0]),buttons[0])
			self.display.blit(pygame.transform.scale2x(self.assets['menu'][1]),buttons[1])
			self.display.blit(pygame.transform.scale2x(self.assets['menu'][2]),buttons[2])
			if buttons[0].collidepoint(mx//2,my//2):
				outline = [(p[0] + buttons[0].x,p[1] + buttons[0].y) for p in img.outline(every = 1)]
				pygame.draw.lines(self.display,'white',True,outline,2)
				if click:
					self.start_game()
			elif buttons[1].collidepoint(mx//2,my//2):
				outline = [(p[0] + buttons[1].x,p[1] + buttons[1].y) for p in img.outline(every = 1)]
				pygame.draw.lines(self.display,'white',True,outline,2)
				if click:
					self.option()
			elif buttons[2].collidepoint(mx//2,my//2):
				outline = [(p[0] + buttons[2].x,p[1] + buttons[2].y) for p in img.outline(every = 1)]
				pygame.draw.lines(self.display,'white',True,outline,2)
				if click:
					pygame.quit()
					sys.exit()
			self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
			pygame.display.flip()
	def option(self):
		while True:
			# self.screen_shader.render(self.display)
			self.display.fill('black')
			if pygame.key.get_pressed()[pygame.K_o]:
				self.run()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
			
			pygame.display.flip()
	def pause_game(self):
		buttons = []
		for i in range(3):
			button = pygame.Rect(self.display.get_width()//2 - self.assets['menu'][0].get_width(),self.display.get_height()//2 + i*75,192,48)
			buttons.append(button)
		while True:
			# self.screen_shader.render(self.display)
			self.display.fill('black')
			mx,my = pygame.mouse.get_pos()
			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True
			img = pygame.mask.from_surface(pygame.transform.scale2x(self.assets['menu'][0]))
			self.display.blit(pygame.transform.scale2x(self.assets['menu'][5]),buttons[0])
			self.display.blit(pygame.transform.scale2x(self.assets['menu'][4]),buttons[1])
			if buttons[0].collidepoint(mx//2,my//2):
				outline = [(p[0] + buttons[0].x,p[1] + buttons[0].y) for p in img.outline(every = 1)]
				pygame.draw.lines(self.display,'white',True,outline,2)
				if click:
					self.run()
			elif buttons[1].collidepoint(mx//2,my//2):
				outline = [(p[0] + buttons[1].x,p[1] + buttons[1].y) for p in img.outline(every = 1)]
				pygame.draw.lines(self.display,'white',True,outline,2)
				if click:
					self.main_menu()
			self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
			pygame.display.flip()
	def start_game(self):
		font = pygame.font.SysFont('minecraft',30)
		self.user_text = ''
		click = False
		while True:
			# self.screen_shader.render(self.display)
			self.screen.fill('black')
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						self.user_text = self.user_text[:-1]
					elif len(self.user_text) <30:
						self.user_text += event.unicode
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True 
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = False
					
						
			if len(self.user_text)>=30:
				font_warning = font.render('Is full',True,'red')
				self.screen.blit(font_warning,((self.monitorsize[0]/2 - font_surface.get_width()/2)+font_surface.get_width() + 10,(self.monitorsize[1]/2 - font_surface.get_height()/2)))	
			font_write = font.render('Nhap Ten Cua Ban:',True,'white')
			self.screen.blit(font_write,((self.monitorsize[0]/2 - font_write.get_width()/2),(self.monitorsize[1]/2 - font_write.get_height()/2) - 60))
			font_surface = font.render(self.user_text,True,'white')
			pygame.draw.rect(self.screen,'white',((self.monitorsize[0]/2 - font_surface.get_width()/2) - 10,(self.monitorsize[1]/2 - font_surface.get_height()/2)-10,font_surface.get_width() + 20,font_surface.get_height() + 20),1)
			self.screen.blit(font_surface,((self.monitorsize[0]/2 - font_surface.get_width()/2),(self.monitorsize[1]/2 - font_surface.get_height()/2)))
			font_button = font.render('Start Game',True,'white')
			button_rect = pygame.Rect(((self.monitorsize[0]/2 - font_button.get_width()/2),(self.monitorsize[1]/2 - font_button.get_height()/2) + 60,171,33))
			mpos = pygame.mouse.get_pos()
			if button_rect.collidepoint(mpos[0],mpos[1]):
				if click:
					self.run()
			self.screen.blit(font_button,((self.monitorsize[0]/2 - font_button.get_width()/2),(self.monitorsize[1]/2 - font_button.get_height()/2) + 60))
			pygame.display.flip()

	def run(self):
		while True:
			# pygame.mouse.set_visible(False)
			# self.display.blit(self.assets['cusor'][0],(pygame.mouse.get_pos()[0]//2 - 8,pygame.mouse.get_pos()[1]//2 - 8))
			# self.screen_shader.render(self.display)
			self.dt = self.clock.tick(30)/1000
			self.display.fill('#8A6556')
			self.scroll[0] += (self.player.pos[0] - self.scroll[0] - self.display.get_size()[0]/2)/5
			self.scroll[1] += (self.player.pos[1] - self.scroll[1] - self.display.get_size()[1]/2)/5
			self.true_scroll =[int(self.scroll[0]),int(self.scroll[1])]
			if self.screen_shake > 0:
				self.scroll[0] += random.randint(0,8) - 4
				self.scroll[1] += random.randint(0,8) - 4
				self.screen_shake -= 1
			self.scaling_factor_x = self.screen.get_width() / (self.display.get_width())
			self.scaling_factor_y = self.screen.get_height() / (self.display.get_height())
			self.key = pygame.key.get_pressed()
			self.mouse_pos = pygame.mouse.get_pos()
			self.mouse_pos = (self.mouse_pos[0]//self.scaling_factor_x + self.scroll[0], self.mouse_pos[1]//self.scaling_factor_y + self.scroll[1])
			self.object_to_draw = []
			if self.click_objcet and self.tile_map.check_chest(self.player.pos,self.display)!=None:
				self.check_chest = self.tile_map.check_chest(self.player.pos,self.display)
			else:
				self.check_chest = None
				self.click_objcet = False
			if len(self.tile_map.check_object(self.player.pos,'tree',self.player.direct,3)) > 0:
				if self.use['type'] == 'wood_axe':
					tile = self.tile_map.check_object(self.player.pos,'tree',self.player.direct,3)[0]
					check_loc = (tile['pos'][0],tile['pos'][1],3)
					mask_surface = self.outline_tile(tile,1)
					self.object_to_draw.append([mask_surface,pygame.Rect(tile['pos'][0]*self.tile_map.tile_size - self.assets[tile['type']][tile['variant']].get_width() // 7 ,tile['pos'][1]*self.tile_map.tile_size - self.tile_map.tile_size * 2,mask_surface.get_width(),mask_surface.get_height())])
					if self.player.weapon.damage == True:
						tile['hp'] -= 1
						self.screen_shake = 2
						if tile['hp'] == 0:
							self.interact_tile.append(Tree(self,[tile['pos'][0] * self.tile_map.tile_size,tile['pos'][1] * self.tile_map.tile_size],tile['hp'],tile['variant']))
			elif len(self.tile_map.check_object(self.player.pos,block_list_l3,self.player.direct,3)) > 0:
				if self.use['type'] in ('wood_pickaxe','wood_axe'):
					tile = self.tile_map.check_object(self.player.pos,block_list_l3,self.player.direct,3)[0]
					mask_surface = self.outline_tile(tile,1)
					self.object_to_draw.append([mask_surface,pygame.Rect(tile['pos'][0]*self.tile_map.tile_size,tile['pos'][1]*self.tile_map.tile_size - self.tile_map.tile_size,mask_surface.get_width(),mask_surface.get_height())])
					if self.player.weapon.damage == True:
						tile['hp'] -= 1
						self.screen_shake = 2
						if tile['hp'] == 0:
							self.interact_tile.append(Block(self,tile['type'],[tile['pos'][0] * self.tile_map.tile_size,tile['pos'][1] * self.tile_map.tile_size],tile['hp'],tile['variant']))
			
			elif len(self.tile_map.check_object(self.player.pos,block_list_l2,(0,0),2)) > 0:
				if self.use['type'] in weapon_type:
					tile = self.tile_map.check_object(self.player.pos,block_list_l2,(0,0),2)[0]
					mask_surface = self.outline_tile(tile,1)
					self.object_to_draw.append([mask_surface,pygame.Rect(tile['pos'][0]*self.tile_map.tile_size,tile['pos'][1]*self.tile_map.tile_size,mask_surface.get_width(),mask_surface.get_height())])
					if self.player.weapon.damage == True:
						tile['hp'] -= 1
						self.screen_shake = 2
						if tile['hp'] == 0:
							self.interact_tile.append(Block(self,tile['type'],[tile['pos'][0] * self.tile_map.tile_size,tile['pos'][1] * self.tile_map.tile_size],tile['hp'],tile['variant']))
			if len(self.tile_map.check_object(self.player.pos,'chest',self.player.direct,3)) > 0:
				tile = self.tile_map.check_object(self.player.pos,'chest',self.player.direct,3)[0]
				check_loc = (tile['pos'][0],tile['pos'][1],3)
				mask_surface = self.outline_tile(tile,1)
				self.object_to_draw.append([mask_surface,pygame.Rect(tile['pos'][0]*self.tile_map.tile_size,tile['pos'][1]*self.tile_map.tile_size - self.tile_map.tile_size,mask_surface.get_width(),mask_surface.get_height())])
				
			for i in self.interact_tile:
				i.render(self.display,self.object_to_draw)
				if not i.alive:
					i.drop_item_type(i.drop_item,Item)
					self.interact_tile.remove(i)
			self.tile_map.render(self.display,self.true_scroll,self.object_to_draw)
			self.player.update(self.tile_map,((self.movement[3] - self.movement[2])*self.player_speed,(self.movement[1] - self.movement[0])*self.player_speed))
			self.player.render(self.display,self.true_scroll,self.object_to_draw)
			if self.use['type'] in weapon_type:
				self.player.weapon = self.weapon_class[self.use['type']]
			# elif self.player.energy >= 1:
			# 	self.player.weapon = self.weapon_class[8]
			else: 
				self.player.weapon = self.weapon_class['bare_hand']
			if self.player.weapon != None:
				self.player.weapon.pos = (self.player.rect().centerx,self.player.rect().centery -4)
				self.player.weapon.render(self.display,self.true_scroll,self.object_to_draw,self.mouse_pos)
				if self.use['type'] == 'bow':
					self.player.weapon.charge_shoot()
				elif self.player.weapon == self.weapon_class['energy_bow'] and self.use['type'] == 0 and self.player.energy >= 1:
					self.player.weapon.charge_shoot()
			render_rect = pygame.Rect(self.true_scroll[0],self.true_scroll[1] - 25,self.display.get_width(),self.display.get_height() + 50)
			for elite in self.elite_group:
				elite.update(self.tile_map)
				elite.render(self.display,self.true_scroll,self.object_to_draw)
				elite.weapon.pos = [elite.rect().centerx,elite.rect().centery - 5]
				# elite.weapon.slash(1,self.player.rect().center)
				elite.weapon.render(self.display,self.true_scroll,self.object_to_draw,self.player.rect().center)
			for animal in self.animals:
				animal.update(self.tile_map)
				animal.render(self.display,self.true_scroll,self.object_to_draw)
			for enemy in self.enemies:
				if enemy.rect().colliderect(render_rect):
					enemy.active = True
					enemy.update(self.tile_map)
					enemy.render(self.display,self.true_scroll,self.object_to_draw)
					enemy.weapon.pos = [enemy.rect().centerx,enemy.rect().centery - 4]
					enemy.weapon.render(self.display,self.true_scroll,self.object_to_draw,self.player)
					if enemy.hp <=0:
						self.enemies.remove(enemy)
				else:
					enemy.active = False
			for item in reversed(self.item_group):
				if item.rect().colliderect(self.player.rect()):
					self.player.inventory.add_item(item.type_e,item.type_e[1],1)
					self.item_group.remove(item)
				item.update(self.tile_map)
				item.render(self.display,self.true_scroll,self.object_to_draw)
			for bullet in reversed(self.bullets):
				# bullet.update(self.tile_map)
				if bullet.rotate_rect.colliderect(render_rect):
					bullet.perfect_collision(bullet.target)
					bullet.active = True
				else: bullet.active = False
				bullet.render(self.display,self.true_scroll,self.object_to_draw,self.tile_map)
				if not bullet.alive:
					self.bullets.remove(bullet)
			for slash in reversed(self.slashs):
				if slash.alive:
					slash.perfect_collision(slash.target)
					slash.render(self.display,self.true_scroll,self.object_to_draw,self.tile_map)
				else:
					self.slashs.remove(slash)
			self.create_shadow_optimize(self.display,self.object_to_draw,self.true_scroll)
			# self.create_shadow(self.display,self.object_to_draw,self.true_scroll,self.dt)
			self.draw_object(self.display,self.object_to_draw,self.true_scroll,self.player)

			self.m_pos_screen = (pygame.mouse.get_pos()[0]//2,pygame.mouse.get_pos()[1]//2)
			self.daynight.lightning(self.dt,self.player.pos,self.true_scroll)
			self.daynight.render()
			# PLAYER iNVENTORY
			self.player.tool_bar.render(self.display)
			self.player.health_bar.render(self.display,self.player.hp)
			self.draw_text('HP',self.font,'red',self.display,[self.player.health_bar.pos[0] + 77,self.player.health_bar.pos[1] + 2])
			self.player.energy_bar.render(self.display,self.player.energy)
			self.draw_text('EN',self.font,'blue',self.display,[self.player.energy_bar.pos[0] + 77,self.player.energy_bar.pos[1] + 2])
			if self.player.inventory.update == True or self.check_chest!=None:
				self.player.inventory.render(self.display)
				self.player.craft_table.render(self.display)
			else:
				loc = (self.mouse_pos[0]//self.tile_map.tile_size,self.mouse_pos[1]//self.tile_map.tile_size,self.tile_map.check_layer(self.use['type']))
				test_distance = abs(int(self.player.pos[0]) - int(self.mouse_pos[0])) <= 300 and abs(int(self.player.pos[1]) - int(self.mouse_pos[1])) <=150
				if self.use != None and self.use['quantity'] > 0 and self.use['type'] not in weapon_type and test_distance:
					if self.use['type'] != 0 and self.use['type'] not in no_block_item:
						if self.tile_map.map_data[loc]['type'] == 0:
							# item_image = self.assets[self.use['type']][0].copy()
							# item_image.set_alpha(150)
							# self.display.blit(item_image,(self.tile_map.map_data[loc]['pos'][0]*self.tile_map.tile_size - self.true_scroll[0],self.tile_map.map_data[loc]['pos'][1]*self.tile_map.tile_size - self.true_scroll[1]))
							pygame.draw.rect(self.display,'white',(self.tile_map.map_data[loc]['pos'][0]*self.tile_map.tile_size - self.true_scroll[0],self.tile_map.map_data[loc]['pos'][1]*self.tile_map.tile_size - self.true_scroll[1],self.tile_map.tile_size,self.tile_map.tile_size),1)
						else:
							pygame.draw.rect(self.display,'red',(self.tile_map.map_data[loc]['pos'][0]*self.tile_map.tile_size - self.true_scroll[0],self.tile_map.map_data[loc]['pos'][1]*self.tile_map.tile_size - self.true_scroll[1],self.tile_map.tile_size,self.tile_map.tile_size),1)
						if self.block_click:
							if loc in self.tile_map.map_data:
								if self.tile_map.map_data[loc]['type'] == 0:
									self.tile_map.place_block(self.mouse_pos,self.use['type'])
									self.use['quantity'] -= 1
									if self.use['quantity'] == 0:
										self.use['type'] = 0
										self.use['quantity'] = 0
			self.tile_map.chest_inventory[self.check_chest]['inventory'].render(self.display) if self.check_chest != None else True
			#menu

			self.invent_icon.render(self.display)
			self.setting_icon.render(self.display)
			if pygame.key.get_pressed()[pygame.K_r]:
				self.tile_map.place_block(self.mouse_pos,0)
			# self.daynight.render()
			# self.daynight.lightning([self.player.pos[0],self.player.pos[1]],self.true_scroll,self.dt)
			# if self.use['type'] == 'weapon' and self.use['variant'] in [0,1,2,4,5,6,8]:
			if self.dig_click:
				if(self.player.weapon.type != 'range'):
					self.player.weapon.slash(1,self.mouse_pos)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				# if event.type == self.spawn_enemy:
				# 	homeless = Homeless(self,[random.randint(int(self.player.pos[0] -300),int(self.player.pos[0] + 300)),random.randint(int(self.player.pos[1]-300),int(self.player.pos[1] + 300))],[16,6])
				# 	homeless.target = self.player
				# 	homeless.weapon = Wood_axe(self,homeless,[24,24])
				# 	self.enemies.append(homeless)
				# if event.type == self.spawn_enemy:
				# 	self.animals.append(Pink(self,[random.randint(int(self.player.pos[0] -300),int(self.player.pos[0] + 300)),random.randint(int(self.player.pos[1]-300),int(self.player.pos[1] + 300))],[24,24]))
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.movement[0] = True
					if event.key == pygame.K_DOWN:
						self.movement[1] = True
					if event.key == pygame.K_LEFT:
						self.movement[2] = True
					if event.key == pygame.K_RIGHT:
						self.movement[3] = True
					if event.key == pygame.K_y:
						self.tile_map.place_struct([self.mouse_pos[0]//self.tile_map.tile_size,self.mouse_pos[1]//self.tile_map.tile_size])
					if event.key == pygame.K_s:
						self.player.inventory.sorted_storage()
						self.player.tool_bar.sorted_storage()
						self.tile_map.chest_inventory[self.check_chest]['inventory'].sorted_storage() if self.check_chest != None else True
					if event.key == pygame.K_p:
						self.pause_game()
					if event.key == pygame.K_SPACE and self.click_objcet == False:
						self.click_objcet = True 
					elif event.key == pygame.K_SPACE and self.click_objcet == True:
						self.click_objcet = False 
					
					if self.player.inventory.update == True or self.check_chest!=None:
						self.player.inventory.split_item(self.m_pos_screen,event,self.display) 
						self.player.craft_table.split_item(self.m_pos_screen,event,self.display) 
						self.player.tool_bar.split_item(self.m_pos_screen,event,self.display)

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						self.movement[0] = False
					if event.key == pygame.K_DOWN:
						self.movement[1] = False
					if event.key == pygame.K_LEFT:
						self.movement[2] = False
					if event.key == pygame.K_RIGHT:
						self.movement[3] = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					self.tile_map.chest_inventory[self.check_chest]['inventory'].replace_item(self.m_pos_screen,event,self.display) if (self.check_chest!=None) else True
					if self.player.inventory.update == True or self.check_chest!=None:
						self.player.inventory.replace_item(self.m_pos_screen,event,self.display) 
						self.player.craft_table.replace_item(self.m_pos_screen,event,self.display) 
						self.player.tool_bar.replace_item(self.m_pos_screen,event,self.display)
					else:
						if self.player.weapon == self.weapon_class['pistol']:
							self.player.weapon.shoot_bullet(event,self.mouse_pos)
						elif self.player.weapon == self.weapon_class['energy_bow'] and self.use['type'] == 0 and self.player.energy >= 1:
							self.player.weapon.shoot_arrow(event,self.mouse_pos)
						if event.button == 1:
							self.use = self.player.tool_bar.get_box(self.m_pos_screen,event)
							self.block_click = True
							self.dig_click = True
					if self.invent_icon.check_mouse(pygame.mouse.get_pos(),event):
						self.player.inventory.check_on()
					if self.setting_icon.check_mouse(pygame.mouse.get_pos(),event):
						self.pause_game()
					self.player.craft_table.craft_item(event,self.m_pos_screen)
					
				if event.type == pygame.MOUSEBUTTONUP:
					if self.use['type'] == 'bow':
						self.player.weapon.shoot_arrow(event,self.mouse_pos)
					if event.button == 1:
						self.block_click = False
						self.dig_click = False
			
			# self.draw_text(f'{self.weapon_class[].charge}',self.font,'black',self.display,[0,40])
			self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))	

			self.draw_text(f'FPS: {(self.clock.get_fps())}\nSEED: {int(self.tile_map.seed)}\nPOS: {[self.player.pos[0]//self.tile_map.tile_size,self.player.pos[1]//self.tile_map.tile_size]}\nCOLOR: {(self.daynight.start_color)}',font_1,'white',self.screen,[10,10])

			# if self.hold != None:
			# 	surf_infor = pygame.Surface((220,180))
			# 	surf_infor.fill('black')
			# 	self.draw_text(f'Item: {self.hold[0]}\n\nQuantity: {self.hold[1]}\n{infor_of_item[self.hold[0]]}',font_infor_item,'white',surf_infor,(20,20))
			# 	self.screen.blit(surf_infor,(420,180))

			pygame.display.flip()
if __name__ == '__main__':
	game = Game()
	game.main_menu()
	
