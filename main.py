import pygame as pm
from pygame.locals import *
import os
import random
import asyncio
import time

highscore = 0


class Assets:
    def __init__(self,screen,image = None,pos = None,size = None,velocity = (0,0), acceleration = (0,0),flipx = False,flipy = False):
        self.velocity, self.acceleration = (velocity, acceleration)
        self.objects = {}
        self.obstacle = False
        self.screen = screen
        self.fixed_size = size
        self._size = size
        self.file_list = None
        if self._size:
            self.width,self.height = self._size
        self._folder = None
        self.rate = 30
        self.count = 0
        self.frame_count = 0
        self.previous_size = None
        self._image = None
        self.image = image
        self.pos = pos
        self.folder_once = True
        if self._image:
            self.image_blit = pm.transform.flip(pm.image.load(f'assets/{self._image}').convert_alpha(),flipx,flipy)
            if self._size:
                self.image_blit = pm.transform.scale(self.image_blit,size)
            self.width, self.height = (self.image_blit.get_width(),self.image_blit.get_height())
        

        pass
    def collision(self,object):
        self.objects[f'{object}'] = object
        self.objects[f'{object}'].right_collide = False
        self.objects[f'{object}'].left_collide = False
        self.objects[f'{object}'].up_collide = False
        self.objects[f'{object}'].down_collide = False
        if self.pos[1] + self.height > object.pos[1] and self.pos[1] < object.pos[1] + object.height:
            if self.pos[0] + self.width > object.pos[0] and self.pos[0] < object.pos[0]:
                self.objects[f'{object}'].right_collide = True
                
                pass
            else:
                self.objects[f'{object}'].right_collide = False
            if self.pos[0] < object.pos[0] + object.width and self.pos[0] + self.width > object.pos[0] + object.width:
                self.objects[f'{object}'].left_collide = True
            else:
                self.objects[f'{object}'].left_collide = False

                pass
        if self.pos[0] + self.width > object.pos[0] and self.pos[0] < object.pos[0] + object.width:
            if self.pos[1] + self.height > object.pos[1] and self.pos[1] < object.pos[1] + object.height:
                self.objects[f'{object}'].up_collide = True
            else:
                self.objects[f'{object}'].up_collide = False
                pass
            if self.pos[1] < object.pos[1] + object.height and self.pos[1] + self.height > object.pos[1]:
                self.objects[f'{object}'].down_collide = True
            else:
                self.objects[f'{object}'].down_collide = False
        collided = True if self.objects[f'{object}'].right_collide or self.objects[f'{object}'].left_collide or self.objects[f'{object}'].up_collide or self.objects[f'{object}'].down_collide else False
        return collided
    def mask_collision(self,object):
        rect_collide = self.collision(object)
        if rect_collide:
            if self.mask.overlap(object.mask,(object.pos[0] - self.pos[0],object.pos[1] - self.pos[1])):
                return True
            else:
                return False
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self,value):
        if self._size != value:
            self._size = value
            if self._size != None:
                self.image_blit = pm.transform.scale(self.image_blit,self._size)
                self.width, self.height = (self.image_blit.get_width(),self.image_blit.get_height())
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self,value):
        if self._image != value:
            self._image = value
            if self._image:
                self.image_blit = pm.image.load(f'assets/{self._image}').convert_alpha()
                if self.fixed_size == None:
                    self.size = self.image_blit.get_size()
                else:
                    self.image_blit = pm.transform.scale(self.image_blit,self._size)
                if self.previous_size:
                    self.pos = (self.pos[0] + self.previous_size[0] - self.size[0],self.pos[1] + self.previous_size[1] - self.size[1])
                self.mask = pm.mask.from_surface(self.image_blit)
    @property
    def folder(self):
        return self._folder
    @folder.setter
    def folder(self,value):
        if self._folder != value:
            self._folder = value
            self.count = 0
            self.frame_count = 0
            self.folder_once = True
            self.animate(self._folder,self.rate)
    def show(self,dt = 1):
        if self._image:
            self.previous_size = self.size
            self.velocity = (self.velocity[0] + self.acceleration[0] * dt, self.velocity[1] + self.acceleration[1] * dt)
            self.pos = (self.pos[0] + self.velocity[0] * dt,self.pos[1] + self.velocity[1] * dt)
            self.screen.blit(self.image_blit,self.pos)

    def animate(self,folder,rate = 40,adjust_size = True,flip = False):
        self.rate = rate
        if self.folder_once == True:
            self._folder = folder
            self.folder_once = False
        self.file_list = os.listdir(f'assets/{self._folder}')
        if self.count == rate:
            self.frame_count += 1
            self.count = 0
        if self.frame_count == len(self.file_list):
            self.frame_count = 0
        self.image = f'{self._folder}/{self.file_list[self.frame_count]}'
        # print(self.image)
        if flip == True:
            self.image_blit = pm.transform.flip(pm.image.load(self._image).convert_alpha(),flip_x = True,flip_y = False)
        
        self.count += 1


class Manager:
    def __init__(self, screen, image=None, repeat_pos=None, repeated=None, size=None):
        self.screen = screen
        self.size = size
        self.image = image
        self.repeat_pos = repeat_pos if repeat_pos is not None else []
        self.repeated = repeated if repeated is not None else []
        self.once_till = True
        self.ys = []
    def repeatperscreen(self,screenwidth,asset,pos,count,y_list = None,biasx = 5,biasy = 0,randomyrange = (0,0),moveby = 0,score = None,dt = 1):
        # print(asset)
        gap = screenwidth/(count - 1)
        # if len(asset) > count:
        #     asset.pop(0)
        # print(score)
        while len(asset) < count:
            if y_list == None:
                #Assets(self.screen,image = self.image,size = self.size,pos = positions)
                asset.append(Assets(self.screen,image=self.image,pos = [pos[0] + len(asset) * gap,random.randint(randomyrange[0],randomyrange[1])],size = self.size))
            else:
                asset.append(Assets(self.screen,image = self.image,pos = [pos[0] + len(asset) * gap,y_list[len(asset)] + biasy],size = self.size))
            self.ys.append(asset[-1].pos[1])
        self.a = asset
        for object in asset:
            object.velocity = (moveby * dt,0)
            object.pos = [object.pos[0] + object.velocity[0] * 1,object.pos[1]]
            if object.pos[0] + object.size[0] < 0:
                object.obstacle = False
                if score != None:
                    score += 1
                if y_list == None:
                    object.pos = [gap * count - (object.size[0] + biasx),random.randint(randomyrange[0],randomyrange[1])]
                else:
                    object.pos = [gap * count - (object.size[0] + biasx),y_list[-1] + biasy]
                self.ys.pop(0)
                self.ys.append(object.pos[1])
                pos = [pos[0] + gap,pos[1]]
            object.screen.blit(object.image_blit,object.pos)

        if score != None:
            return asset,score
        else:
            return asset,self.ys
    def repeat(self,gap,range_to,till,player = None,erase_before = None,velocity = 0,positions = None,dt = 1):
        if self.once_till == True:
            self.till = till
            self.till[0] = till[0]
            self.once_till = False
        self.collisions = []
        self.till[1] = till[1]
        dis = self.till[1] - self.till[0]
        self.repeat_num = int(dis/gap) + 1
        count = 0
        for i in range(self.repeat_num):
            try:
                object = self.repeated[count]
            except:
                object = Assets(self.screen,image = self.image,size = self.size,pos = positions)
                self.repeated.append(object)
            posx = self.till[0] + count * gap
            if not object.pos:
                try:
                    posy = self.repeat_pos[count]
                except:
                    posy = random.randint(range_to[0],range_to[1])
            else:
                posy = object.pos[1]
            pos = (posx,posy)
            object.size = self.size
            object.velocity = (velocity,0)
            object.pos = pos
            object.show(dt = dt)
            if player:
                if object.mask_collision(player):
                    self.collisions.append(object)
            # if erase_before:
            #     if posx < erase_before:
            #         self.repeated.remove(object)
            count += 1
            if erase_before:
                if object.pos[0] < erase_before:
                    self.till = [self.till[0] + gap,self.till[1]]
                    try:
                        self.repeated.remove(object)
                    except:
                        pass
        self.till = [self.till[0] + velocity,self.till[1]]
        return self.repeated
        pass

class Main:
    def __init__(self):
        pm.init()
        screen_info = pm.display.Info()
        self._screenheight  = screen_info.current_h
        self._screenwidth = screen_info.current_w
        self.groundy_list = [self.screenheight - 100,self.screenheight - 100,self.screenheight - 100]
        pass
    @property
    def screenheight(self):
        return self._screenheight
    @screenheight.setter
    def screenheight(self,value):
        if self._screenheight != value:
            self._screenheight = value
            self.screen = pm.display.set_mode((self._screenwidth,self._screenheight))
    @property
    def screenwidth(self):
        return self._screenwidth
    @screenwidth.setter
    def screenwidth(self,value):
        if self._screenwidth != value:
            self._screenwidth = value
            self.screen = pm.display.set_mode((self._screenwidth,self._screenheight))
    def ground(self,gap,range_to,till):
        self.ground_num = int(till/gap) + 1
        self.ground_count = 0
        ground_list = []
        for i in range(self.ground_num):
            posx = self.ground_count * gap
            try:
                posy = self.groundy_list[self.ground_count]
            except:
                posy = random.randint(range_to[0],range_to[1])
                self.groundy_list.append(posy)
            pos = (posx,posy)
            ground_list.append(pos)
            self.ground_count += 1
        return ground_list
        pass
    async def main(self):
        print('working....')
        clock = pm.time.Clock()
        global highscore
        scores = 0
        death = False
        pm.display.set_caption("DODGE")
        self.screen = pm.display.set_mode((self._screenwidth,self._screenheight))
        # icon = pm.image.load('ICON.png').convert_alpha()
        # pm.display.set_icon(icon)
        player = Assets(self.screen,velocity = (0,0),pos = (50,50))
        player_flip = False
        landed = False
        first_fall = False
        dash = True
        dash_once = False
        velx = 5
        xvel = velx
        dash_vel = 7
        dash_maxdis = 250
        dash_dis = 0
        yacc = accy = 0.5
        xacc = accx = 0.001
        jump_velocity = -10
        drop_rate = 0.5
        launched = False
        move_for = False
        move_back = False
        slide = False
        Font = pm.font.SysFont("Courier New",30)
        Font2 = pm.font.SysFont("Tahoma",30)
        gr = {}
        ground = Manager(self.screen,image = 'land5.png',size = (self._screenwidth/2,200))
        grounds = []
        ground_start = 0
        ground_vel = 0
        background = Manager(self.screen,image = 'background.png',size = (self._screenwidth,self._screenheight))
        backgrounds = []
        space = pm.transform.scale(Font2.render('Press Space Key once to jump and double to double jump " "',True,(112,112,112)),(self._screenwidth/2.5,30))
        right = pm.transform.scale(Font2.render('Press Right Arrow Key to dash "→"',True,(112,112,112)),(self._screenwidth/4,25))
        down = pm.transform.scale(Font2.render('Press Down Arrow Key to slide "↓"',True,(112,112,112)),(self._screenwidth/4,25))
        prev_time = time.time()
        def ground_interaction(player,i):
            nonlocal landed,launched,blocked
            player.collision(i)
            if player.objects[f'{i}'].right_collide == True and player.objects[f'{i}'].left_collide == False and i.pos[1] <= player.pos[1] + (player.height/2):
                blocked = True
                player.pos = (i.pos[0] - player.width,player.pos[1])
                player.objects[f'{i}'].down_collide = False
            if player.objects[f'{i}'].left_collide == True and player.objects[f'{i}'].right_collide == False and i.pos[1] <= player.pos[1] + (player.height/2):
                player.pos = (i.pos[0] + i.width,player.pos[1])
                player.objects[f'{i}'].down_collide = False
            if player.objects[f'{i}'].down_collide == True:
                if launched == False:
                    # print(True)
                    landed = True
                    player.velocity = (player.velocity[0],0)
                player.pos = (player.pos[0],i.pos[1] - player.height)

        def obstacles(screen,ground,player,obs_list = [None],dt = 1):
            nonlocal scores,death
            global highscore
            if ground.obstacle != False:
                obstacle = ground.obstacle
            else:
                object = random.choice(obs_list)
                if object:
                    if object.get('repeat',False) == False:
                        obstacle = ground.obstacle = Assets(screen,image = object.get('image',None),
                                         pos = (ground.pos[0] + ground.size[0] + object.get('posbiasx',0),ground.pos[1] + object.get('posbiasy',0)),
                                         size = object.get('size',None),
                                         velocity=(object.get('velocityx',0) + ground.velocity[0],object.get('velocityy',0) + ground.velocity[1]),
                                         flipx = object.get('flipx',False),flipy = object.get('flipy',False))
                    else:
                        obstacle = ground.obstacle = Manager(screen,image = object.get('image',None),size = object.get('size',None))
                    obstacle.posbias = (object.get('posbiasx',0),object.get('posbiasy',0))
                    obstacle.vel = (object.get('velocityx',0),object.get('velcoityy',0))
                    obstacle.folder = object.get('folder',None)
                    obstacle.rate = object.get('rate',0)
                    obstacle.flip = (object.get('flipx',False),object.get('flipy',False))
                    obstacle.shoot = object.get('shoot',None)
                    obstacle.gap = object.get('gap',0)
                    obstacle.repeats = object.get('repeat',False)
                    obstacle.erasebefore = object.get('erasebefore',None)
                    obstacle.damage = object.get('damage',False)
                    obstacle.score = False
                else:
                    obstacle = ground.obstacle = object
            if obstacle:
                if obstacle.repeats == False:
                    if obstacle.folder:
                        obstacle.animate(obstacle.folder,rate=obstacle.rate,flip = obstacle.flip[0])
                    obstacle.velocity = (obstacle.vel[0] * dt + ground.velocity[0],obstacle.vel[1] * dt + ground.velocity[1])
                    # print('ground_velocity:',ground.velocity)
                    # print('obstacle_velocity:',obstacle.velocity)
                    obstacle.show()
                    if obstacle.pos[0] + obstacle.size[0] < player.pos[0] and not obstacle.score:
                        scores += 1
                        obstacle.score = True
                    if obstacle.damage and obstacle.mask_collision(player):
                        pm.display.update()
                        death = True
                else:
                    obstacle.repeat(obstacle.gap,(ground.pos[1] + obstacle.posbias[1],ground.pos[1] + obstacle.posbias[1]),[ground.pos[0] + ground.size[0] + obstacle.posbias[0],ground.pos[0] + ground.size[0] + obstacle.posbias[0]],player = player,
                                    positions= (ground.pos[0] + ground.size[0] + obstacle.posbias[0],ground.pos[1] + obstacle.posbias[1]),erase_before=obstacle.erasebefore,velocity = obstacle.vel[0] + ground.velocity[0])
                    if obstacle.collisions and obstacle.damage:
                        pm.display.update()
                        death = True
                    # print({f'{obstacle.image}' : len(obstacle.repeated)})
                    pass
                if obstacle.shoot:
                    obstacles(screen,obstacle,player,obstacle.shoot,dt = dt)
        
        cannon_ball = {'image' : 'cannon_ball.png','size' : (10,10),'posbiasy' : 5,'posbiasx' : -50,'velocityx' : -1,'repeat' : True,'gap' : 300,'erasebefore' : 0,'damage' : True}
        cannon = {'image' : 'cannon.png','size' : (50,35),'posbiasx' : -50,'posbiasy' : -35,'flipx' : True,'shoot' : [cannon_ball],'repeat' : False}
        spikes = {'image' : 'spikes.png','size' : (204,19),'posbiasy' : -19,'posbiasx' : -504,'damage' : True}
        fireball = {'image' : 'fireball.png','size' : (10,10),'posbiasy' : 10,'posbiasx' : -25,'velocityx' : -5,'repeat' : True,'gap' : 300,'erasebefore' : 0,'damage' : True}
        statue = {'image' : 'ancientdog_statue.png','size' : (25,50),'posbiasx' : -25,'posbiasy' : -50,'flipx' : True,'shoot' : [fireball],'repeat' : False}
        obstacle_list = [None]
        counts = 0
        while True:
            clock.tick(120)
            # print(clock.get_fps())
            now = time.time()
            dt = (now - prev_time) * 120
            prev_time = now
            if death == False:
                blocked = False
                if xvel < 15:
                    xvel += accx * dt
                    dash_vel += accx * dt
                else:
                    xvel = 15
                self.screen.fill((50,50,50))
                # self.screen.blit(background,(0,0))
                # ground.show()
                backgrounds,ys = background.repeatperscreen(3 * self._screenwidth,backgrounds,[0,0],6,moveby = ground_vel/6,dt = dt)
                player.animate('walking',rate = 5,flip = False)
                player.show()
                # player.mask = pm.mask.from_surface(player.image_blit).to_surface()
                # self.screen.blit(player.mask,player.pos)
                #grounds = ground.repeat(ground.size[0],(self.screenheight - 200,self.screenheight - 50),[ground_start,self.screenwidth],velocity = ground_vel,erase_before=-1000)
                grounds,groundys = ground.repeatperscreen(self._screenwidth,grounds,[0,0],3,randomyrange=[self._screenheight-200,self._screenheight - 50],biasx = 15,moveby = ground_vel,dt = dt)
                dodged_score = Font.render(f"Obstacles dodged : {scores}",True,(122,122,122))
                high_score = Font.render(f"High Score : {highscore}",True,(122,122,122))

                self.screen.blit(dodged_score,(self._screenwidth/2 - dodged_score.get_width()/2,100))
                self.screen.blit(high_score,(self._screenwidth/2 - high_score.get_width()/2,dodged_score.get_height() + 110))
                self.screen.blit(space,(0,50))
                self.screen.blit(right,(0,100))
                self.screen.blit(down,(0,150))
                # grounds = self.ground(150,(600,700),1400)
                landed = False
                # print(player.velocity[1])
                if player.velocity[1] >= 0:
                    launched = False
                for i in grounds:
                    obstacles(self.screen,i,player,obstacle_list,dt = dt)
                    ground_interaction(player,i)
                    player.objects.clear()
                counts += 1
                if counts > 15:
                    obstacle_list = [None,spikes,statue,cannon]
                # for i in range(len(grounds)):
                #     gr[i] = Assets(self.screen,image = 'land.png',pos = grounds[i],size = (150,100))
                #     gr[i].show()
                #     player.collision(gr[i])
                #     if player.objects[f'{gr[i]}'].down_collide == True:
                #         landed = True
                #         player.velocity = (player.velocity[0],0)
                #         player.pos = (player.pos[0],gr[i].pos[1] - player.height)
                if landed == False:
                    # if player.velocity[1] >= 0:
                    #     print('yes')
                    #     player.velocity = (player.velocity[0],1)
                    #     player.acceleration = (0,0)
                    # else:
                    if dash_once == False:
                        player.acceleration = (player.acceleration[0],accy)
                    else:
                        velx = dash_vel
                        dash_dis += dash_vel
                        player.velocity = (velx,0)
                        # player.folder = "dash"
                        if dash_dis >= dash_maxdis:
                            dash_once = False
                            dash = False
                            dash_dis = 0
                            velx = xvel
                else:
                    dash_once = False
                    dash = True
                    accy = yacc
                    dash_dis = 0
                    velx = xvel
                # if move_for == True:
                if player.pos[0] < 150 and blocked == False:
                    player.velocity = (velx,player.velocity[1])
                    ground_vel = 0
                else:
                    player.pos = (150,player.pos[1])
                    ground_vel = -velx
                    if blocked:
                        player.folder = 'standing'
                        player.velocity = (ground_vel,player.velocity[1])
                    else:
                        if dash_once == True:
                            player.folder = 'dash'
                        else:
                            if slide:
                                player.folder = 'sliding'
                            else:
                                player.folder = 'walking'
                        player.velocity = (0,player.velocity[1])
                # else:
                #     player.velocity = (0,player.velocity[1])

                # elif move_back == True:
                #     if player.pos[0] > 100:
                #         player.velocity = (-1,player.velocity[1])
                #         ground_vel = 0
                #     else:
                #         player.velocity = (0,player.velocity[1])
                #         ground_vel = 1
                #     player_flip = True
                # else:
                #     player.velocity = (0,player.velocity[1])
                #     player.folder = 'walking'
                #     ground_vel = 0
                if player.pos[1] > self.screenheight:
                    death = True
                # if dash == True:
                #     dash = False
                #     velx = xvel
                for event in pm.event.get():
                    if event.type == pm.QUIT:
                        quit()
                    if event.type == pm.KEYDOWN:
                        if event.key == pm.K_SPACE and (landed == True or first_fall == True) and not slide:
                            if first_fall:
                                first_fall = False
                            if landed:
                                first_fall = True
                            player.velocity = (player.velocity[0],jump_velocity)
                            launched = True
                        if event.key == pm.K_DOWN:
                            if landed:
                                slide = True
                            else:
                                accy += drop_rate
                                slide = True
                        if event.key == pm.K_RIGHT and not landed and dash == True:
                            dash_once = True
                            # print(dash)
                    elif event.type == pm.KEYUP:
                        if event.key == pm.K_DOWN:
                            slide = False
                if scores > highscore:
                    highscore = scores
            else:
                # if scores >= highscore:
                #     with open('highscore.txt','w') as file:
                #         file.write(str(scores))
                game_over = pm.transform.scale(Font.render('GAME OVER',True,(122,0,0)),(500,250))
                self.screen.blit(game_over,(self._screenwidth/2 - game_over.get_width()/2,self._screenheight/2 - game_over.get_height()/2))
                pm.display.update()
                run = True
                for event in pm.event.get():
                    if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                        death = False
                        game = Main()
                        return await game.main()
                    if event.type == QUIT:
                        pm.quit()
            pm.display.update()
            await asyncio.sleep(0)
            pass
        pass
    
asyncio.run(Main().main())
# game.main()