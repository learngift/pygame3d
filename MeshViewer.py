import random, math, pygame

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __str__(self):
        return f'Point3D({self.x}, {self.y}, {self.z})'

    def __neg__(self):
        return Point3D(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def scale(self, v):
        self.x = self.x * v
        self.y = self.y * v
        self.z = self.z * v

    def rotateX(self, angle):
    	c, s = math.cos(angle), math.sin(angle)
    	self.y, self.z = self.y * c - self.z * s, self.y * s + self.z * c

    def rotateY(self, angle):
    	c, s = math.cos(angle), math.sin(angle)
    	self.z, self.x = self.z * c - self.x * s, self.z * s + self.x * c

    def rotateZ(self, angle):
    	c, s = math.cos(angle), math.sin(angle)
    	self.x, self.y = self.x * c - self.y * s, self.x * s + self.y * c

    def projection(self, env3d):
        return [ env3d.wincenter[0] + self.x * env3d.zoom_factor, \
                 env3d.wincenter[1] + self.y * env3d.zoom_factor ]

    def normalize(self):
        self.scale(1/self.norm())

class Face:
    def render(self, env3d, points):
        polygon = self.getPolygon(points, env3d)
        pygame.draw.polygon(env3d.screen, WHITE, polygon, 1)

class Triangle(Face):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def dist(self, points):
        return (points[self.a].z + points[self.b].z + points[self.c].z) / 3

    def getPolygon(self, points, env3d):
        return (points[self.a].projection(env3d),
                points[self.b].projection(env3d),
                points[self.c].projection(env3d),)

class Objet:
    """Un objet est une collection de points et de faces.
    Les faces sont composées des indices référençant les points"""
    def __init__(self):
        self.name = 'unknown'
        self.points, self.faces = [], []

    def __str__(self):
        return f'Objet {len (self.points)} points, {len (self.faces)} faces'

    def display(self, env3d):
        env3d.screen.fill(BLACK)
        self.faces.sort(key = lambda t : t.dist(self.points))
        for face in self.faces:
            face.render(env3d, self.points)

    def rotateX(self, angle):
        for p in self.points: p.rotateX(angle)

    def rotateY(self, angle):
        for p in self.points: p.rotateY(angle)

    def rotateZ(self, angle):
        for p in self.points: p.rotateZ(angle)

def GetCube():
    o = Objet()
    o.name = 'Cube'
    o.points.append(Point3D( -1, -1, -1))
    o.points.append(Point3D( -1, -1,  1))
    o.points.append(Point3D( -1,  1, -1))
    o.points.append(Point3D( -1,  1,  1))
    o.points.append(Point3D(  1, -1, -1))
    o.points.append(Point3D(  1, -1,  1))
    o.points.append(Point3D(  1,  1, -1))
    o.points.append(Point3D(  1,  1,  1))
    o.faces.append (Triangle(0, 1, 2))
    o.faces.append (Triangle(3, 2, 1))
    o.faces.append (Triangle(7, 2, 3))
    o.faces.append (Triangle(7, 6, 2))
    o.faces.append (Triangle(5, 4, 7))
    o.faces.append (Triangle(7, 4, 6))
    o.faces.append (Triangle(5, 1, 4))
    o.faces.append (Triangle(1, 0, 4))
    o.faces.append (Triangle(1, 5, 3))
    o.faces.append (Triangle(7, 3, 5))
    o.faces.append (Triangle(6, 2, 4))
    o.faces.append (Triangle(0, 2, 4))
    return o

class Env3D:
    def __init__(self, winsize=[800, 600]):
        self.winsize = winsize
        self.zoom_factor = 200
        self.light_vector_1 = Point3D(random.random(), random.random(), random.random())
        self.light_vector_1.normalize()
        self.light_vector_2 = Point3D(random.random(), random.random(), random.random())
        self.light_vector_2.normalize()
        self.screen = pygame.display.set_mode(winsize)
        pygame.display.set_caption('3D viewer')
        self.wincenter = [winsize[0]/2, winsize[1]/2]

def interactive(env3d, main_object):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    main_object.rotateY(math.pi / 20)
                elif event.key == pygame.K_RIGHT:
                    main_object.rotateY(-math.pi / 20)
                elif event.key == pygame.K_UP:
                    main_object.rotateX(math.pi / 20)
                elif event.key == pygame.K_DOWN:
                    main_object.rotateX(-math.pi / 20)
                elif event.key == pygame.K_PAGEUP:
                    main_object.rotateZ(math.pi / 20)
                elif event.key == pygame.K_PAGEDOWN:
                    main_object.rotateZ(-math.pi / 20)
                elif event.key == pygame.K_KP_MINUS: # K_F1 si laptop
                    env3d.zoom_factor /= 1.1
                elif event.key == pygame.K_KP_PLUS: # K_F2
                    env3d.zoom_factor *= 1.1

        main_object.display(env3d)
        pygame.display.flip()
    pygame.quit()

interactive(Env3D(), GetCube())

