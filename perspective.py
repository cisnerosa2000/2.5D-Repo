from Tkinter import *
import math
import random

root = Tk()
root.title('2.5D')
root.geometry("1000x600+0+0")
canvas = Canvas()
canvas.config(width=1000,height=600,bg='light yellow')

crosshair = PhotoImage(file='crosshair.gif')
hip = PhotoImage(file='HIP.gif')
ads0 = PhotoImage(file='ADS0.gif')
bdo = PhotoImage(file='Back_Door_Open.gif')
bdc = PhotoImage(file='Back_Door_Closed.gif')
enemy_img = PhotoImage(file='Enemy.gif')

class Enemy(object):
    def __init__(self):
        self.z = 1
        self.x = 500
        self.y = 300
        
        self.dx = random.randint(-50,50)
        self.img = canvas.create_image(self.x,self.y,image=enemy_img)
    def loop(self):
        for enemy in player.enemy_list:
            enemy.x = canvas.coords(enemy.img)[0]
            enemy.y = canvas.coords(enemy.img)[1]
        
            
            if enemy.dx + 500 > 500 and enemy.dx+500 != enemy.x and player.alive:
                enemy.x += .5
            elif enemy.dx+500 < 500 and enemy.dx+500 != enemy.x and player.alive:
                enemy.x -= .5
                
            if enemy.y < 400:
                enemy.y += .3
                
                
            
            
            if enemy.z < 10 and player.alive:
                enemy.z += .001
            
            
            canvas.delete(enemy.img)
            
      
            
            enemy.img = canvas.create_image(enemy.x,enemy.y,image=enemy_img)
            
            
            enemy.bbox = canvas.bbox(enemy.img)
            enemy.overlapping = canvas.find_overlapping(*enemy.bbox)
    
            for i in enemy.overlapping:
                if "bullet" in canvas.gettags(i):
                    try:
                        canvas.delete(enemy.img)
                        player.enemy_list.remove(enemy)
                        
                        if player.ammo <= 34:
                            player.ammo += 2
                        player.score += 1
                    except (IndexError,ValueError):
                        pass
            
                        
        if player.alive:
            pass
        else:
            canvas.tag_raise(player.rip_text)
            
            
        
                        
        root.after(1,self.loop)
    def fire_loop(self):
        self.d_list = []
        for i in player.enemy_list:
            if i.y > 400:
                self.d_list.append(i)
        for i in range(len(self.d_list)):
            if player.alive:
                player.health -= 3
                
                
                
        root.after(500,self.fire_loop)
        
            
            
            
            
        
        
        
        
        
class Room(object):
    def __init__(self):
        self.x,self.y = (500,300)    
        self.rectangle = canvas.create_rectangle(self.x-60,self.y-50,self.x+60,self.y+30,outline="black")
        self.rect = canvas.coords(self.rectangle)
    
        self.one = canvas.create_line(0,0,self.rect[0],self.rect[1],fill="black")
        self.two = canvas.create_line(1000,0,self.rect[2],self.rect[1],fill="black")
        self.three = canvas.create_line(200,600,self.rect[0],self.rect[3],fill="black")
        self.four = canvas.create_line(800,600,self.rect[2],self.rect[3],fill="black")
        self.opened = False
        
        
        
        
        self.door = canvas.create_image(500,295,image=bdc)
    def open(self):
        canvas.delete(self.door)
        self.door = canvas.create_image(500,295,image=bdo)
        canvas.tag_lower(room.door)
        self.opened = True
    def close(self):
        canvas.delete(self.door)
        self.door = canvas.create_image(500,295,image=bdc)
        self.opened = False
        canvas.tag_lower(self.door)
        y_line = canvas.create_line(380,400,620,400,fill="red")
        
        
class Player(object):
    def __init__(self):
        self.ammo = 36
        self.mag = 12
        self.health = 100
        self.score = 0
        
        
        self.pistol_img = hip
        self.crosshair_img = crosshair
        self.bullet_bar_list = []
        self.enemy_list = []
        self.bullet_list = []
        self.x = True
        self.alive = True
        self.rate = 1000
        
        self.loop()
    def loop(self):
        self.mx, self.my = canvas.winfo_pointerxy()
        self.mx -= 6
        self.my -= 50
        
        if self.health  <= 0 and self.alive:
            self.alive = False
            self.rip()
        
        try:
            canvas.delete(self.pistol)
            canvas.delete(self.ammo_display)
            canvas.delete(self.healthbar_outline)
            canvas.delete(self.healthbar)
            canvas.delete(self.scoreboard)
            
            
        except AttributeError:
            pass
        
        
        
        self.pistol = canvas.create_image(self.mx, self.my,image = self.pistol_img)
        
        self.ammo_display = canvas.create_text(self.mx,self.my+45,text="%s" % self.ammo)
        
        self.cx = 950
        self.cy = 100
        
        
        for i in self.bullet_bar_list:
            canvas.delete(i)
            self.bullet_bar_list.remove(i)
        
        for i in range(self.mag):
            self.bullet_bar = canvas.create_rectangle(self.cx,self.cy,self.cx+30,self.cy+10,fill="black")
            self.cy += 30
            self.bullet_bar_list.append(self.bullet_bar)
            
        
        
        
        for bullet in self.bullet_list:
            canvas.tag_raise(bullet)
            
        self.healthbar_outline = canvas.create_rectangle(900,100,920,400)
        self.healthbar = canvas.create_rectangle(900,100,920,100+self.health*3,fill="green")
        
        self.zeros = 5 - len(str(self.score))
        self.scoreboard = canvas.create_text(940,500,text="%s%s" % ("0"*self.zeros,self.score),font=("Arial",20))
        
        


        
        
        
        root.after(1,self.loop)
    
        
        
        
        


   
    def fire(self,event):
        if self.mag > 0 and self.alive:
            self.mag -= 1
            root.after(500,self.cleanup)
            
            
            
            
                
            
            self.bx = canvas.coords(self.pistol)[0] + random.randint(-15,15)
            self.by = canvas.coords(self.pistol)[1] - 85
                
                
           
           
                
            
            
            
            
            self.bullet = canvas.create_oval(self.bx-2,self.by-2,self.bx+2,self.by+2,fill="black",tags="bullet")
            self.bullet_list.append(self.bullet)
            
            if self.bullet in canvas.find_overlapping(*canvas.bbox(room.door)) and room.opened == True:
                canvas.delete(self.bullet)
                self.bullet_list.remove(self.bullet)
            
                
                
            




    def reload(self,event):  
        if self.mag == 0 and self.ammo >= 12 and self.alive:
            self.mag += 12
            self.ammo -= 12
        elif self.ammo > 0 and self.alive:
            
            
            self.needed = 12 - self.mag
            if self.needed < self.ammo:
                
                self.mag += self.needed
                self.ammo -= self.needed
            else:
                self.mag += self.ammo
                self.ammo = 0



    def spawn(self):
        
        if self.alive:
            room.open()
        
            enemy = Enemy()
            self.enemy_list.append(enemy)
            root.after(500,room.close)
            
            if self.rate > 80:
                self.rate -= 40
        
        if self.x == True:
            enemy.loop()
            enemy.fire_loop()
            self.x = False
        root.after(self.rate,self.spawn)
        
        
        

    def cleanup(self):
        if self.bullet_list:
            tbd = self.bullet_list[0]
            canvas.delete(tbd)
            self.bullet_list.remove(tbd)

    def rip(self):
        self.rip_text = canvas.create_text(500,300,text="YOU DIED!",fill="red",font="100")
        
        canvas.tag_raise(self.rip_text)



    def aim(self,event):
        self.pistol_img = ads0
    def unaim(self,event):
        self.pistol_img = hip


room = Room()
player = Player()
player.spawn()

    
    



root.bind("<Button-1>",player.fire)
root.bind("<space>",player.reload)
root.bind("<w>",player.aim)
root.bind("<KeyRelease-w>",player.unaim)


    
 
    
canvas.pack()
root.mainloop()