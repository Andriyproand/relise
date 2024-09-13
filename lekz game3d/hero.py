from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties

key_switch_camera = 'c' 
key_switch_mode = 'z' 

key_forward = 'w'  
key_back = 's'      
key_left = 'a'      
key_right = 'd'     
key_up = 'e'      
key_down = 'q'    

key_turn_left = 'n' 
key_turn_right = 'm'
class Hero():
    def __init__(self,pos,land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel("steve.glb")
        self.hero.setScale(0.1)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.mouseLookEnabled = False
        props.setMouseMode(WindowProperties.M_confined)
        base.win.requestProperties(props)
        self.hero.setHpr(0,90,0)
        self.cameraBind()
        self.cameraOn = True
        self.accept_events()
    def cameraBind(self):
        base.disableMouse()
        base.camera.setHpr(90,90,90)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(5,8,15)
        self.cameraOn = 1
        crosshairs = OnscreenImage(
            image = 'crosshairs.png',
            pos = (0,0,0),
            scale = 0.05,
            )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)
        props = WindowProperties()
        props.setCursorHidden(1)
        props.setMouseMode()


    def cameraUp(self):
        base.enableMouse()
        base.camera.setPos(0,0,0)
        base.camera.reparentTo(render)
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)
        props = WindowProperties()
        props.setCursorHidden(1)
        props.setMouseMode()

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def turn_left(self):
            self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):

        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
    
    def check_dir(self,angle):

        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)


    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)
    
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)
    def changeMode(self):
       if self.mode:
           self.mode = False
       else:
           self.mode = True
           

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)


    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)


        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)