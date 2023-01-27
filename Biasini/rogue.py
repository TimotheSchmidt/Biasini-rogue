import numpy as np 
import pygame as pg
import matplotlib.pyplot as plt
import random

class Player :
    def __init__(self, x = 0, y = 0, health = 10) :
        self.x = x
        self.y = y
        self.hp = health

    def move(self, dir, board) :
        if dir == 'up' and self.y - 7>=0 and board[self.x, self.y - 7] == 1:
            self.y += -1
        if dir == 'down' and self.y + 7 < len(board) and board[self.x, self.y + 7] == 1:
            self.y += 1
        if dir == 'left' and self.x - 7 >=0 and board[self.x - 7, self.y] == 1 :
            self.x += -1
        if dir == 'right' and self.x + 7 < len( board) and board[self.x + 7, self.y] == 1 :
            self.x += 1

class Field :
    def __init__(self, width = 700, length = 700, colorWalls = [255, 255, 255], colorFloor = [145, 145, 145], numberRooms = 9) :
        self.width = width
        self.length = length
        self.colorWalls = colorWalls
        self.colorFloor = colorFloor
        self.field = np.zeros((width, length))
        self.numberRooms = numberRooms

    def generate_rooms(self, numberRooms = 9) :
        listRooms  = []
        for i in range(numberRooms) :
            sizeRoom = np.random.randint(4,30, size = 2)*7
            
            posRoomX = np.random.randint((i%3)*33*7, (i%3+1)*33*7-sizeRoom[0])
            posRoomY = np.random.randint((i//3)*33*7, (i//3 + 1)*33*7 - sizeRoom[1])
            listRooms.append((posRoomX, posRoomY, sizeRoom))
            
        return listRooms

    def generate_corridor(self, listRooms) :
        n = int(np.sqrt(self.numberRooms))
        corridors = []
        for i in range(n) :
            line = listRooms[n*i:n*(i+1)]
            for k in range(len(line) - 1) :
                corridor_start = (line[k][0] + line[k][2][0], line[k][1] + line[k][2][1]//2)
                corridor_end = (line[k+1][0], line[k+1][1] + line[k+1][2][1]//2)
                corridors.append([corridor_start[0], corridor_start[1], (corridor_end[0] - corridor_start[0])//2, 2*7])
                corridors.append([corridor_start[0] + (corridor_end[0] - corridor_start[0])//2, corridor_end[1], (corridor_end[0] - corridor_start[0])//2 + 2*7, 2*7])
                if corridor_end[1] < corridor_start[1] : 
                    corridors.append([corridor_start[0] + (corridor_end[0] - corridor_start[0])//2, corridor_end[1], 2*7, abs(corridor_end[1] - corridor_start[1])+2*7])
                else : 
                    corridors.append([corridor_start[0] + (corridor_end[0] - corridor_start[0])//2, corridor_start[1], 2*7, abs(corridor_end[1] - corridor_start[1])])
        for i in range (n - 1) :
            random_number = np.random.randint(0, n)
            room_top = listRooms[3*i:3*(i+1)][random_number]
            room_bottom = listRooms[3*(i+1):3*(i+2)][random_number]
            print(room_top, room_bottom)
            corridor_start = (room_top[0] + room_top[2][0]//2, room_top[1] + room_top[2][1])
            corridor_end = (room_bottom[0] + room_bottom[2][0]//2, room_bottom[1])
            corridors.append([corridor_start[0], corridor_start[1], 2*7,(corridor_end[1] - corridor_start[1])//2])
            corridors.append([corridor_end[0], corridor_start[1] + (corridor_end[1] - corridor_start[1])//2, 2*7, (corridor_end[1] - corridor_start[1])//2 +2*7])
            if corridor_start[0] < corridor_end[0] :
                corridors.append([corridor_start[0], corridor_start[1] + (corridor_end[1] - corridor_start[1])//2, abs(corridor_end[0] - corridor_start[0]) + 14,2*7])       
            else : 
                corridors.append([corridor_end[0], corridor_start[1] + (corridor_end[1] - corridor_start[1])//2, abs(corridor_end[0] - corridor_start[0]) + 14,2*7])
        return corridors

    def field_construction(self, listRooms, corridors) :
        board = self.field
        for i in corridors :
            board[i[0] : i[0] + i[2], i[1] : i[1] + i[3]] = np.ones(board[i[0] : i[0] + i[2], i[1] : i[1] + i[3]].shape)
        for i in listRooms :
            board[i[0] : i[0] + i[2][0], i[1] : i[1] + i[2][1]] = np.ones(board[i[0] : i[0] + i[2][0], i[1] : i[1] + i[2][1]].shape)
        '''board[Player.x,Player.y] = 3'''
        return board


class Ennemies :
    def __init__(self, board, listRooms, listCorridors, numberEnnemies = 5) :
        self.field = board
        self.listEnnemies = []
        self.listRooms = listRooms
        self.listCorridors = listCorridors
        for i in range(numberEnnemies) :  
            spawningRoom = np.random.randint(len(self.listRooms))
            while spawningRoom == len(self.listRooms)//2 + 1 :
                spawningRoom = np.random.randint(len(self.listRooms))
            x_spawn = np.random.randint(listRooms[spawningRoom][0], listRooms[spawningRoom][0] + listRooms[spawningRoom][2][0])
            y_spawn = np.random.randint(listRooms[spawningRoom][1], listRooms[spawningRoom][1] + listRooms[spawningRoom][2][1])
            self.listEnnemies.append([x_spawn, y_spawn])

    def move(self,last_dir) :
        list_dir = ['right', 'left', 'up', 'down']
        listRooms = self.listRooms
        listCorridors = self.listCorridors
        
        
        board = self.field
        new_dir = []
        for i in range(len(self.listEnnemies)) :
            
            draw = np.random.rand()
            if draw > 0.8 :
                dir = random.choice(list_dir)
            else : 
                dir = last_dir[i]
            if dir == 'up' and self.listEnnemies[i][1] - 7 >=0 and board[self.listEnnemies[i][0], self.listEnnemies[i][1] - 7] == 1:
                self.listEnnemies[i][1] += -1
            if dir == 'down' and self.listEnnemies[i][1] + 7 < len(board) and board[self.listEnnemies[i][0], self.listEnnemies[i][1] + 7] == 1:
                self.listEnnemies[i][1] += 1
            if dir == 'left' and self.listEnnemies[i][0] - 7 >=0 and board[self.listEnnemies[i][0] - 7, self.listEnnemies[i][1]] == 1 :
                self.listEnnemies[i][0] += -1
            if dir == 'right' and self.listEnnemies[i][0] + 7 < len( board) and board[self.listEnnemies[i][0] + 7, self.listEnnemies[i][1]] == 1 :
                self.listEnnemies[i][0] += 1
            new_dir.append(dir)
        return new_dir   
        


class Game :
    def __init__(self, fps = 60, difficulty =0.7) :
        '''self.playerLook = playerLook
        self.floorLook = floorLook'''
        self.fps = fps
        self.screen = pg.display.set_mode((7*100,7*100))
        self.clock = pg.time.Clock()
        field = Field()
        self.rooms = field.generate_rooms()
        self.corridors = field.generate_corridor(self.rooms)
        self.board = field.field_construction(self.rooms, self.corridors)
        self.player = Player(x = self.rooms[4][0], y = self.rooms[4][1])
        self.ennemies = Ennemies(self.board, self.rooms, self.corridors)
        self.difficulty = difficulty
        

    def update(self, dir,last_dir) :
        
        pg.draw.rect(color = [0, 0, 0], rect = [0, 0, 700, 700], surface = self.screen)
        for i in self.corridors :
            pg.draw.rect(color = [255, 255, 255], rect = i, surface = self.screen)
        for i in self.rooms :
            pg.draw.rect(color = [144, 144, 144], rect = [i[0], i[1], i[2][0], i[2][1]], surface = self.screen)
        self.player.move(dir, self.board)
        image = pg.image.load('Player.png').convert()
        self.screen.blit(image, (self.player.x, self.player.y))
        new_dir = self.ennemies.move(last_dir)
        ennemiesToKill = []
        for i in range(len(self.ennemies.listEnnemies)) :
            self.screen.blit(pg.image.load('Orc.png').convert(), (self.ennemies.listEnnemies[i][0], self.ennemies.listEnnemies[i][1],))
            if abs(self.player.x - self.ennemies.listEnnemies[i][0])<40 and abs(self.player.y - self.ennemies.listEnnemies[i][1])<40 :
                if abs(self.player.x - self.ennemies.listEnnemies[i][0])>abs(self.player.y - self.ennemies.listEnnemies[i][1]) :
                    if self.player.x - self.ennemies.listEnnemies[i][0]>0 :
                        last_dir[i] ='right'
                    else : 
                        last_dir[i]='left'
                else :
                    if self.player.y - self.ennemies.listEnnemies[i][1] :
                        last_dir[i]='down'
                    else : 
                        last_dir[i]='up'

            else : 
                last_dir[i] = new_dir[i]
            if self.player.x in [self.ennemies.listEnnemies[i][0], self.ennemies.listEnnemies[i][0]-1, self.ennemies.listEnnemies[i][0]+1] and self.player.y in [self.ennemies.listEnnemies[i][1], self.ennemies.listEnnemies[i][1]-1, self.ennemies.listEnnemies[i][1]+1] :
                chance = np.random.rand()
                if chance>self.difficulty :
                    ennemiesToKill.append(i)
                    print(chance)
                else : 
                    self.player.hp += -1
        if ennemiesToKill != [] :
            self.ennemies.listEnnemies.pop(ennemiesToKill[0])
        pg.display.set_caption(f"HP:{self.player.hp}")
        return(last_dir)


def Main() :
    running = True
    pg.init()
    game = Game()
    last_dir = ['right' for i in range(5)]
    while running :
        dir = None
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                running = False
        pressed = pg.key.get_pressed()
        if pressed[pg.K_DOWN] :
            dir = 'down'
        elif pressed[pg.K_UP] :
            dir = 'up'            
        elif pressed[pg.K_LEFT] :
            dir = 'left'
        elif pressed[pg.K_RIGHT] :
            dir = 'right'
        last_dir = game.update(dir, last_dir)
        if game.player.hp == 0 :
            running = False
        pg.display.update()
        game.clock.tick(game.fps)
    print('GAME OVER')
    pg.quit()

if __name__ == '__main__' :
    Main()  



