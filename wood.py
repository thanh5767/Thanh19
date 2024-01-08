import pygame
import pygame_shaders
import sys,random,time
from datetime import datetime
from script.utils import load_image,load_images,Animation,DayNight,Hot_bar,Inventory_icon,Setting_icon,Health_bar,Energy_bar
from script.entity import Physical_Entity,Player,Dafluffy,Inventory,Chest_inventory,Item,Deer,Homeless
from script.weapon import Weapon,Wood_sword,Wood_axe,Wood_pickaxe,Bow,Spear,Katana,Bare_hands,Pistol
from script.tile_map import Tile_map


class Game():
	def __init__(self):
		pygame.init()
		self.monitorsize = [pygame.display.Info().current_w,pygame.display.Info().current_h]
		self.screen = pygame.display.set_mode((self.monitorsize),pygame.OPENGL|pygame.DOUBLEBUF)
		self.display = pygame.Surface((self.screen.get_size()[0]//2,self.screen.get_size()[1]//2))
		# self.display.set_colorkey((0,0,0))
		self.screen_shader = pygame_shaders.Shader((self.monitorsize), (self.monitorsize), (0,0), "shaders/main_screen/vertex.glsl", "shaders/main_screen/fragment.glsl",self.display)
		self.clock = pygame.time.Clock()
		self.movement = [False,False,False,False]
		self.tile_map = Tile_map(self,tile_size = 24)
		self.scroll = [0,0]
		self.assets = {
		'grass': load_images('grass'),
		'sand': load_images('sand'),
		'tree': load_images('tree'),
		'player/idle': Animation(load_images('entity/player/idle'),dur = 5,loop = True),
		'player/run': Animation(load_images('entity/player/run'),dur = 3,loop = True),
		'player2/idle': Animation(load_images('entity/player2/idle'),dur = 5,loop = True),
		'player2/run': Animation(load_images('entity/player2/run'),dur = 3,loop = True),
		'dafluffy/idle': Animation(load_images('entity/dafluffy/idle'),dur = 5,loop = True),
		'dafluffy/run': Animation(load_images('entity/dafluffy/run'),dur = 3,loop = True),
		'deer/idle': Animation(load_images('entity/deer/idle'),dur = 5,loop = True),
		'deer/run': Animation(load_images('entity/deer/run'),dur = 3,loop = True),
		'homeless/idle': Animation(load_images('entity/homeless/idle'),dur = 5,loop = True),
		'homeless/run': Animation(load_images('entity/homeless/run'),dur = 3,loop = True),
		'stone': load_images('stone'),
		'wood_block': load_images('wood_block'),
		'water': load_images('water'),
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
		}
		self.font = pygame.font.SysFont('minecraft',8)

		self.player = Player(self,[0,0],[16,6])
		self.player.health_bar = Health_bar((self.player.tool_bar.x_move*30,self.player.tool_bar.y_move*30 - 20),[75,10],self.player.hp,self.player.max_hp)
		self.player.energy_bar = Energy_bar((self.player.tool_bar.x_move*30 + 90,self.player.tool_bar.y_move*30 - 20),[75,10],self.player.energy,self.player.max_energy)
		self.weapon_class = [
		Wood_sword(self,self.player,[24,24]),
		Wood_axe(self,self.player,[24,24]),
		Wood_pickaxe(self,self.player,[24,24]),
		Bow(self,self.player,[24,24]),
		Spear(self,self.player,[24,24]),
		Katana(self,self.player,[24,24]),
		Bare_hands(self,self.player,[24,24]),
		Pistol(self,self.player,[24,24]),
		]
		self.player.weapon = self.weapon_class[6]
		self.elite_group = []
		self.animals = []
		self.enemies = []
		self.item_group = []
		for i in range(6):
			# daff = Dafluffy(self,[0,0],[12,4])
			# daff.weapon = Katana(self,daff,[24,24])
			# self.elite_group.append(daff)
			# self.animals.append(Deer(self,[0,0],[24,24]))
			homeless = Homeless(self,[0,0],[16,6])
			homeless.target = self.player
			homeless.weapon = Katana(self,homeless,[24,24])
			self.enemies.append(homeless)
		self.tile_map.seed = random.randint(-1000,1000)
		# self.tile_map.seed = 10000
		self.player_speed = 2
		self.daynight = DayNight(self)
		self.hold = None
		self.invent_icon = Inventory_icon(self,[0,1],[48,48],48)
		self.setting_icon = Setting_icon(self,[0,2],[48,48],48)
		self.use = {'type':0,'quantity':0}
		self.time = -10
		self.bullets = []
		self.slashs = []
		self.screen_shake = 0

	def shadow_def(self,display, image, rect, scroll,dt):
		# shadow_surf = pygame.Surface((self.monitorsize))
		mask = pygame.mask.from_surface(image)
		mask_outline = [(point[0] + rect.x - scroll[0], point[1] + rect.y - scroll[1]) for point in mask.outline()]
		pygame.draw.polygon(display, (0, 0, 0), [(x + width, y) for (x, y), width in zip(mask_outline, [height * dt for height in [(y - rect.y + scroll[1] - rect.height) * -0.1 for x, y in mask_outline]])])

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
			if image in self.assets['tree'] or image in self.assets['rock'] or image in self.assets['item']:
				pygame.draw.ellipse(shadow_surf, (0, 0, 0, 50), (rect.x - scroll[0], rect.y - scroll[1] + rect.height // 1.25, rect.width, rect.height // 3))
			elif image in self.assets['stone'] or image in self.assets['wood_wall'] or image in self.assets['sand_stone'] or image in self.assets['chest'] or image in self.assets['wood_block']:
				pygame.draw.rect(shadow_surf, (0, 0, 0, 50), (rect.x - scroll[0], rect.y - scroll[1] + rect.height, rect.width, rect.height // 3))
		display.blit(shadow_surf, (0, 0))
	def draw_object(self,display,objects_to_draw,scroll,player):
		for obj in sorted(objects_to_draw,key = lambda obj:obj[1].bottom):
			image = obj[0]
			rect = obj[1]
			display.blit(image,(rect.x- scroll[0],rect.y -scroll[1]))
	def draw_text(self,text,font,color,surface,loc):
		surface.blit(font.render(text,1,color),(loc[0],loc[1]))
	def main_menu(self):
		buttons = []
		for i in range(3):
			button = pygame.Rect(self.display.get_width()//2 - self.assets['menu'][0].get_width(),self.display.get_height()//2 + i*75,192,48)
			buttons.append(button)
		self.scroll = [0,0]
		while True:
			self.screen_shader.render(self.display)
			# self.display.blit(pygame.transform.scale(self.assets['menu'][8],self.display.get_size()),(0,0))
			self.display.fill('salmon')
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
					self.run()
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
			
			pygame.display.flip()
	def option(self):
		while True:
			self.screen_shader.render(self.display)
			self.display.fill('red')
			if pygame.key.get_pressed()[pygame.K_o]:
				self.run()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.flip()
	def pause_game(self):
		buttons = []
		for i in range(3):
			button = pygame.Rect(self.display.get_width()//2 - self.assets['menu'][0].get_width(),self.display.get_height()//2 + i*75,192,48)
			buttons.append(button)
		while True:
			self.screen_shader.render(self.display)
			self.display.fill('salmon')
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
			pygame.display.flip()
	def run(self):
		while True:
			self.screen_shader.render(self.display)
			self.dt = self.clock.tick(30)/1000
			self.display.fill('#8A6556')
			self.scroll[0] += (self.player.pos[0] - self.scroll[0] - self.display.get_size()[0]/2)/20
			self.scroll[1] += (self.player.pos[1] - self.scroll[1] - self.display.get_size()[1]/2)/20
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

			self.tile_map.render(self.display,self.true_scroll,self.object_to_draw,Chest_inventory(self))
			self.check_chest = self.tile_map.check_chest(self.player.pos,self.display)
			if len(self.tile_map.check_object(self.player.pos,'tree')) > 0:
				if self.use['type'] == 'weapon' and self.use['variant'] == 1:
					temp_tree = self.tile_map.check_object(self.player.pos,'tree')
					if temp_tree != []:
						tree = self.tile_map.map_data[temp_tree[0]['pos']]
						if self.player.weapon.time_slash == 2:
							tree['hp'] = max(0,tree['hp'] - 1)
						if tree['hp'] == 0:
							self.item_group.append(Item(self,'item',[tree['pos'][0] * self.tile_map.tile_size,tree['pos'][1]*self.tile_map.tile_size],[20,20]))
							tree['type'] = 0
			if len(self.tile_map.check_object(self.player.pos,'stone')) > 0:
				if self.use['type'] == 'weapon' and self.use['variant'] == 2:
					temp_tree = self.tile_map.check_object(self.player.pos,'stone')
					if temp_tree != []:
						tree = self.tile_map.map_data[temp_tree[0]['pos']]
						if self.player.weapon.time_slash == 2 if self.player.weapon != None else False:
							tree['hp'] = max(0,tree['hp'] - 1)
						if tree['hp'] == 0:
							self.item_group.append(Item(self,tree['type'],[tree['pos'][0] * self.tile_map.tile_size,tree['pos'][1]*self.tile_map.tile_size],[20,20]))
							tree['type'] = 0

			self.player.update(self.tile_map,((self.movement[3] - self.movement[2])*self.player_speed,(self.movement[1] - self.movement[0])*self.player_speed))
			self.player.render(self.display,self.true_scroll,self.object_to_draw)
			if self.use['type'] == 'weapon':
				self.player.weapon = self.weapon_class[self.use['variant']]
			else: 
				self.player.weapon = self.weapon_class[6]
			if self.player.weapon != None:
				self.player.weapon.pos = (self.player.rect().centerx,self.player.rect().centery -4)
				self.player.weapon.render(self.display,self.true_scroll,self.object_to_draw,self.mouse_pos)
				# rect_weapon = self.player.weapon.rect()[1]
				if self.use['type'] == 'weapon' and self.use['variant'] in [3]:
					self.player.weapon.charge_shoot()
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
				enemy.update(self.tile_map)
				enemy.render(self.display,self.true_scroll,self.object_to_draw)
				enemy.weapon.pos = [enemy.rect().centerx,enemy.rect().centery - 4]
				enemy.weapon.render(self.display,self.true_scroll,self.object_to_draw,self.player)
			for i,item in sorted(enumerate(self.item_group),reverse = True):
				if item.rect().colliderect(self.player.rect()):
					self.player.inventory.add_item(item.type_e,0)
					self.item_group.remove(item)
				item.update(self.tile_map)
				item.render(self.display,self.true_scroll,self.object_to_draw)
			for bullet in self.bullets:
				# bullet.update(self.tile_map)
				bullet.render(self.display,self.true_scroll,self.object_to_draw,self.tile_map)
			for i,slash in sorted(enumerate(self.slashs),reverse=True):
				if slash.alive:
					slash.perfect_collision(slash.target)
					slash.render(self.display,self.true_scroll,self.object_to_draw,self.tile_map)
				else:
					self.slashs.remove(slash)

			self.create_shadow_optimize(self.display,self.object_to_draw,self.true_scroll)
			# self.create_shadow(self.display,self.object_to_draw,self.true_scroll,self.dt)
			self.draw_object(self.display,self.object_to_draw,self.true_scroll,self.player)
			
			self.m_pos_screen = (pygame.mouse.get_pos()[0]//2,pygame.mouse.get_pos()[1]//2)

			# PLAYER iNVENTORY
			self.player.tool_bar.render(self.display)
			self.player.health_bar.render(self.display,self.player.hp)
			self.draw_text('HP',self.font,'red',self.display,[self.player.health_bar.pos[0] + 77,self.player.health_bar.pos[1] + 2])
			self.player.energy_bar.render(self.display,self.player.energy)
			self.draw_text('EN',self.font,'blue',self.display,[self.player.energy_bar.pos[0] + 77,self.player.energy_bar.pos[1] + 2])
			if self.player.inventory.update == True or self.check_chest!=None:
				self.player.inventory.render(self.display)
			else:
				loc = (self.mouse_pos[0]//self.tile_map.tile_size,self.mouse_pos[1]//self.tile_map.tile_size,self.tile_map.check_layer(self.use['type']))
				test_distance = abs(int(self.player.pos[0]) - int(self.mouse_pos[0])) <= 300 and abs(int(self.player.pos[1]) - int(self.mouse_pos[1])) <=150
				if self.use != None and self.use['quantity'] > 0 and self.use['type'] not in [0,'weapon'] and test_distance:
					if self.use['type'] != 0:
						if self.tile_map.map_data[loc]['type'] == 0:
							# item_image = self.assets[self.use['type']][0].copy()
							# item_image.set_alpha(150)
							# self.display.blit(item_image,(self.tile_map.map_data[loc]['pos'][0]*self.tile_map.tile_size - self.true_scroll[0],self.tile_map.map_data[loc]['pos'][1]*self.tile_map.tile_size - self.true_scroll[1]))
							pygame.draw.rect(self.display,'white',(self.tile_map.map_data[loc]['pos'][0]*self.tile_map.tile_size - self.true_scroll[0],self.tile_map.map_data[loc]['pos'][1]*self.tile_map.tile_size - self.true_scroll[1],self.tile_map.tile_size,self.tile_map.tile_size),1)
						else:
							pygame.draw.rect(self.display,'red',(self.tile_map.map_data[loc]['pos'][0]*self.tile_map.tile_size - self.true_scroll[0],self.tile_map.map_data[loc]['pos'][1]*self.tile_map.tile_size - self.true_scroll[1],self.tile_map.tile_size,self.tile_map.tile_size),1)
						if pygame.mouse.get_pressed()[0]:
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
			self.daynight.render()
			self.daynight.lightning([self.player.pos[0],self.player.pos[1]],self.true_scroll,self.dt)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
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
					self.player.inventory.replace_item(self.m_pos_screen,event,self.display) if (self.player.inventory.update == True or self.check_chest!=None) else True
					self.tile_map.chest_inventory[self.check_chest]['inventory'].replace_item(self.m_pos_screen,event,self.display) if self.check_chest != None else True
					self.player.tool_bar.replace_item(self.m_pos_screen,event,self.display) if (self.player.inventory.update == True or self.check_chest!=None) else True
					self.use = self.player.tool_bar.get_box(self.m_pos_screen,event)

					if self.invent_icon.check_mouse(pygame.mouse.get_pos(),event):
						self.player.inventory.check_on()
					if self.setting_icon.check_mouse(pygame.mouse.get_pos(),event):
						self.pause_game()
					if self.use['type'] == 'weapon' and self.use['variant'] in [0,1,2,4,5,6]:
						self.weapon_class[self.use['variant']].slash(event,self.mouse_pos)
					if self.player.weapon == self.weapon_class[6] and self.use['type'] == 0:
						self.player.weapon.slash(event,self.mouse_pos)
					if self.player.weapon == self.weapon_class[7]:
						self.player.weapon.shoot_bullet(event,self.mouse_pos)
				if event.type == pygame.MOUSEBUTTONUP:
					if self.use['type'] == 'weapon' and self.use['variant'] in [3]:
						self.weapon_class[self.use['variant']].shoot_arrow(event,self.mouse_pos)
			
			self.draw_text(f'{self.weapon_class[3].charge}',self.font,'black',self.display,[0,40])
			# self.daynight.lightning([self.player.pos[0] - self.assets['light'].get_size()[0]/2,self.player.pos[1]- self.assets['light'].get_size()[1]/2],self.true_scroll,self.dt)
			self.draw_text(f'FPS: {(self.clock.get_fps())}\nSEED: {int(self.tile_map.seed)}\nPOS: {[self.player.pos[0]//self.tile_map.tile_size,self.player.pos[1]//self.tile_map.tile_size]}',self.font,'black',self.display,[0,10])
			pygame.display.flip()

if __name__ == '__main__':
	game = Game()
	game.main_menu()
