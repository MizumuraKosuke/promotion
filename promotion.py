from tkinter import *
import time, random, math
pic=6
FIELD_X, FIELD_Y = 80, 80
FIELD_Xp, FIELD_Yp = 100, 80

tk = Tk()
tk.title("Mental distance")
canvas = Canvas(tk, width=FIELD_X*pic, height=FIELD_Y*pic)
canvas.pack()

tkp = Tk()
tkp.title("Physical distance")
canvasp = Canvas(tkp, width=FIELD_Xp*pic, height=FIELD_Yp*pic)
canvasp.pack()

class World:
    def __init__(self,population):
    #population:グループごとの人数
        self.people = []
        self.bases = []
        self.advertise = []
        self.population = population
        self.communication = []
    def add_people(self, group, personal_number):
        self.people.append(Human(group,personal_number))
    def add_base(self, size, group):
        self.bases.append(Base(size,group))
    def add_advertise(self, x, y, wide):
        self.advertise.append(Advertise(x,y,wide))
    def step(self):
        people_sample = []
        people_sample_p = []
        for human in self.people:
            human.move()
            human.movep()
            people_sample.append(human)
            people_sample_p.append(human)
        for A in self.people: #心的接触判定
            for B in people_sample:
                if (A.x == B.x) and (A.y == B.y):
                    if A.group != B.group:
                        self.communication.append((A,B))
            people_sample.pop(0)
        for A in self.people:
            for advertise in self.advertise:
                advertise.effect(A)
            for B in people_sample_p:
                if (A.xp == B.xp) and (A.yp == B.yp):
                    if A.number != B.number:
                        if (A.known != 1000) or (B.known != 1000):
                            A.reviews(B)
            people_sample_p.pop(0)
        for human in self.people:
            human.render()
        for base in self.bases:
            base.render()
        for advertise in self.advertise:
            advertise.render()
        tk.update()
        tkp.update()
        tk.update_idletasks()
        tkp.update_idletasks()
        canvas.delete("all")
        canvasp.delete("all")
        time.sleep(0.05)
    def start(self, n_steps):
        current = 0
        for i in range(self.population):
            for j in range(5):
                current = current+1
                self.add_people(j+1,current)
        for i in range(5):
            self.add_base(16,i+1)
        self.add_advertise(10,10,4)
        self.add_advertise(80,60,6)
        for x in range(n_steps):
            self.step()

class Human:
    def __init__(self, group, personal_number):
    #group:所属グループ名 personal_number:個人番号(１人１つ)
        self.group = group
        self.number =personal_number
        self.known = 0    #情報を知っているかどうか(この値が1000のとき知っている)
        self.base_size = 16
        self.s = self.base_size/2
        self.colors = ["tomato","lime","gold","magenta","deepskyblue"]
        self.cities = [("Shinjuku",5,30,20),("Ikebukuro",6,80,70)] #都市のリスト(都市名, 都市レベル(0~10), x, y)
        city = random.choice(self.cities)
        self.like_city = city
        favo = random.randint(1,10)
        self.favorite_level = favo
        if self.group == 1: #グループ1
            self.center_x,self.center_y = 40,10 #グループの本拠地の中心
            self.return_p = 40 #戻り率:小さいほどコミュニケーション能力が高いグループ
        elif self.group == 2: #グループ2
            self.center_x,self.center_y = 10,40
            self.return_p = 20
        elif self.group == 3: #グループ3
            self.center_x,self.center_y = 70,40
            self.return_p = 10
        elif self.group == 4: #グループ4
            self.center_x,self.center_y = 20,70
            self.return_p = 30
        elif self.group == 5: #グループ5
            self.center_x,self.center_y = 60,70
            self.return_p = 50
        for i in range(5):
            if self.group == i+1:
                rx = random.randint(self.center_x-self.s,self.center_x+self.s)
                ry = random.randint(self.center_y-self.s,self.center_y+self.s)
                self.base_x, self.base_y = rx,ry #個人の定位置
                self.color = self.colors[i] #個体の色
        self.x, self.y = self.base_x, self.base_y #個人の心理的位置
        self.xp, self.yp = self.base_x, self.base_y #個人の物理的位置
        self.vx, self.vy = 1, 1
        self.vxp, self.vyp = 1, 1
    def move(self):
        self.change_dir()
        if self.x == FIELD_X:
            self.vx = -self.vx
        self.x = self.x + self.vx
        if self.y == FIELD_Y:
            self.vy = -self.vy
        self.y = self.y + self.vy
    def change_dir(self):
        dirs = [(1,1),(-1,1),(-1,-1),(1,-1),
                (1,0),(0,1),(-1,0),(0,-1),(0,0)]
        ind = dirs.index((self.vx, self.vy))
        r = random.random()
        if r > 0.95:
            newInd = (ind + 1) % len(dirs)
            self.vx, self.vy = dirs[newInd]
        elif r <= 0.01*self.return_p:
        #本拠地方向に進む
            if self.x < self.base_x:
                self.vx = 1
            elif self.x == self.base_x:
                self.vx = 0
            elif self.x > self.base_x:
                self.vx = -1
            if self.y < self.base_y:
                self.vy = 1
            elif self.y == self.base_y:
                self.vy = 0
            elif self.y > self.base_y:
                self.vy = -1
        else:
            newInd = ind
            self.vx, self.vy = dirs[newInd]
    def movep(self):
        self.change_dirp()
        self.xp = (self.xp + self.vxp)%FIELD_Xp
        self.yp = (self.yp + self.vyp)%FIELD_Yp
    def change_dirp(self):
        dirs = [(1,1),(-1,1),(-1,-1),(1,-1),
                (1,0),(0,1),(-1,0),(0,-1),(0,0)]
        ind = dirs.index((self.vxp, self.vyp))
        r = random.random()
        if r < 0.1:
            newInd = (ind + 1) % len(dirs)
            self.vxp, self.vyp = dirs[newInd]
        elif r >= 0.1 and r< 0.2:
            if r < self.like_city[1]*0.1:
                if self.xp < self.like_city[2]:
                    self.vxp = 1
                elif self.xp == self.like_city[2]:
                    self.vxp = 0
                elif self.xp > self.like_city[2]:
                    self.vxp = -1
                if self.yp < self.like_city[3]:
                    self.vyp = 1
                elif self.yp == self.like_city[3]:
                    self.vyp = 0
                elif self.yp > self.like_city[3]:
                    self.vyp = -1
        else:
            newInd = ind
            self.vxp, self.vyp = dirs[newInd]
    def reviews(self,human):     #口コミ
        dist = math.sqrt(pow(self.x-human.x,2)+pow(self.y-human.y,2))
        Field_size = math.sqrt(pow(FIELD_X,2)+pow(FIELD_Y,2))
        p = dist/Field_size + 0.5
        rr = random.random()
        if rr >= p:
            if (rr < self.favorite_level*0.1) and (rr < human.favorite_level*0.1):
                if self.known == 1000:
                    human.known = 1000
                    print("グループ{} {}番がグループ{} {}番に口コミ 心的距離:{}".format(self.group,self.number,human.group,human.number,dist))
                elif human.known == 1000:
                    self.known = 1000
                    print("グループ{} {}番がグループ{} {}番に口コミ 心的距離:{}".format(human.group,human.number,self.group,self.number,dist))
    def render(self):
        canvas.create_rectangle(self.x*pic, self.y*pic,
                                self.x*pic+pic, self.y*pic+pic,
                                fill=self.color, outline=self.color)
        if self.known == 1000:
            out = "Black"
        else:
            out = self.color
        canvasp.create_rectangle(self.xp*pic, self.yp*pic,
                                 self.xp*pic+pic, self.yp*pic+pic,
                                 fill=self.color, outline=out)

class Base:
    def __init__(self, size, group):
    #size:本拠地のサイズ group:グループ名
        self.size = size
        self.group = group
        self.human = Human(self.group,None) #グループの情報を知りたいだけなので
                                            #個人番号はなんでもよし
    def render(self):
        canvas.create_rectangle((self.human.center_x-(self.size/2))*pic,
                                (self.human.center_y-(self.size/2))*pic,
                                (self.human.center_x+(self.size/2)+1)*pic,
                                (self.human.center_y+(self.size/2)+1)*pic,
                                outline=self.human.color)
        canvas.create_text(self.human.center_x*pic, self.human.center_y*pic,
                           text="グループ{}".format(self.group))

class Advertise: #広告
    def __init__(self, x, y, wide):
        self.x, self.y = x, y
        self.wide = wide
    def effect(self, human):  #広告による効果
        if human.known != 1000:
            if (human.xp >= self.x) and (human.xp <= self.x+self.wide) and (human.yp >= self.y) and (human.yp <= self.y+1):
                human.known = human.known + 1
                if human.known == 13 - human.favorite_level:
                    print("広告効果 広告を見た回数:{}回".format(human.known))
                    human.known = 1000
    def render(self):
        canvasp.create_rectangle(self.x*pic, self.y*pic,
                                (self.x+self.wide)*pic, (self.y+1)*pic,
                                fill="blue", outline="blue")
        canvasp.create_text((self.x+self.wide/2)*pic, (self.y+1/2)*pic,
                           text="広告")

world = World(50)
world.start(3000)
