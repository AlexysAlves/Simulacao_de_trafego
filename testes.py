import random
import time
import threading
import pygame
import sys

# Default values of signal timers
defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
defaultRed = 150
defaultYellow = 5

signals1 = []
signals2 = []
signals3 = []
signals4 = []
noOfSignals = 4
currentGreen = 0  # Indicates which signal is green currently
nextGreen = (currentGreen + 1) % noOfSignals  # Indicates which signal will turn green next
currentYellow = 0  # Indicates whether yellow signal is on or off

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}  # average speeds of vehicles

# Coordinates of vehicles' start
x = {'rightup': [0, 0, 0], 'rightdown': [755, 727, 697], 'downright': [755, 727, 697], 'downleft': [755, 727, 697], 'leftup': [1400, 1400, 1400], 'leftdown': [1400, 1400, 1400], 'upright': [602, 627, 657], 'upleft': [602, 627, 657]}
y = {'rightup': [348, 370, 398], 'rightdown': [348, 370, 398], 'downright': [0, 0, 0], 'downleft': [0, 0, 0], 'leftup': [498, 466, 436], 'leftdown': [498, 466, 436], 'upright': [800, 800, 800], 'upleft': [800, 800, 800]}

vehicles = {'rightup': {0: [], 1: [], 2: [], 'crossed': 0}, 'rightdown': {0: [], 1: [], 2: [], 'crossed': 0}, 'downright': {0: [], 1: [], 2: [], 'crossed': 0}, 'downleft': {0: [], 1: [], 2: [], 'crossed': 0},
            'leftup': {0: [], 1: [], 2: [], 'crossed': 0}, 'leftdown': {0: [], 1: [], 2: [], 'crossed': 0}, 'upright': {0: [], 1: [], 2: [], 'crossed': 0}, 'upleft': {0: [], 1: [], 2: [], 'crossed': 0}}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}
directionNumbers = {0: 'rightup', 1: 'rightdown', 2: 'downright', 3: 'downleft', 4: 'leftup', 5: 'leftdown', 6: 'upright', 7: 'upleft'}

# Coordinates of signal image, timer, and vehicle count
signalCoods1 = [(300, 150), (400, 150), (400, 250), (300, 250)] #(350, 200)
signalTimerCoods1 = [(300, 140), (400, 140), (400, 240), (300, 240)]
signalCoods2 = [(1000, 150), (1100, 150), (1100, 250), (1000, 250)] #(1050, 200)
signalTimerCoods2 = [(1000, 140), (1100, 140), (1100, 240), (1000, 240)]
signalCoods3 = [(1000, 550), (1100, 550), (1100, 650), (1000, 650)] #(1050, 600)
signalTimerCoods3 = [(1000, 540), (1100, 540), (1100, 640), (1000, 640)]
signalCoods4 = [(300, 550), (400, 550), (400, 650), (300, 650)] #(350, 600)
signalTimerCoods4 = [(300, 540), (400, 540), (400, 640), (300, 640)]

# Coordinates of stop lines
stopLines1 = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop1 = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stopLines2 = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop2 = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stopLines3 = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop3 = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stopLines4 = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop4 = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}

# Gap between vehicles
stoppingGap = 15  # stopping gap
movingGap = 15  # moving gap

pygame.init()
simulation = pygame.sprite.Group()


class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + "x4.png"
        self.image = pygame.image.load(path)

        if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][
            self.index - 1].crossed == 0):  # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
            if (direction == 'rightup'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().width - stoppingGap  # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            elif (direction == 'rightdown'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().width - stoppingGap  # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            elif (direction == 'leftup'):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
                    self.index - 1].image.get_rect().width + stoppingGap
            elif (direction == 'leftdown'):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
                    self.index - 1].image.get_rect().width + stoppingGap
            elif (direction == 'downright'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().height - stoppingGap
            elif (direction == 'downleft'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().height - stoppingGap
            elif (direction == 'upright'):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
                    self.index - 1].image.get_rect().height + stoppingGap
            elif (direction == 'upleft'):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
                    self.index - 1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Set new starting and stopping coordinate
        if (direction == 'right'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] -= temp
        elif (direction == 'left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif (direction == 'down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif (direction == 'up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x + self.image.get_rect().width > stopLines[
                self.direction]):  # if the image has crossed stop line now
                self.crossed = 1
            if ((self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                    currentGreen == 0 and currentYellow == 0)) and (
                    self.index == 0 or self.x + self.image.get_rect().width < (
                    vehicles[self.direction][self.lane][self.index - 1].x - movingGap))):
                # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                self.x += self.speed  # move the vehicle
        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]):
                self.crossed = 1
            if ((self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (
                    currentGreen == 1 and currentYellow == 0)) and (
                    self.index == 0 or self.y + self.image.get_rect().height < (
                    vehicles[self.direction][self.lane][self.index - 1].y - movingGap))):
                self.y += self.speed
        elif (self.direction == 'left'):
            if (self.crossed == 0 and self.x < stopLines[self.direction]):
                self.crossed = 1
            if ((self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
                    self.index == 0 or self.x > (
                    vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().width + movingGap))):
                self.x -= self.speed
        elif (self.direction == 'up'):
            if (self.crossed == 0 and self.y < stopLines[self.direction]):
                self.crossed = 1
            if ((self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (
                    self.index == 0 or self.y > (
                    vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().height + movingGap))):
                self.y -= self.speed


# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()


def repeat():
    global currentGreen, currentYellow, nextGreen
    while (signals[currentGreen].green > 0):  # while the timer of current green signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 1  # set yellow signal on
    # reset stop coordinates of lanes and vehicles
    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while (signals[currentGreen].yellow > 0):  # while the timer of current yellow signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 0  # set yellow signal off

    # reset all signal times of current signal to default times
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # set next signal as green signal
    nextGreen = (currentGreen + 1) % noOfSignals  # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow + signals[
        currentGreen].green  # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()


# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Generating vehicles in the simulation
def generateVehicles():
    daytime = 360
    sleeptime = 0
    while (True):
        lane_number = random.randint(1,2)
        cartype = [60, 70, 80, 100]
        dist = [25, 50, 75, 100]
        temp1 = random.randint(0, 99)
        temp2 = random.randint(0, 99)
        direction_number = 0
        if (temp1 < cartype[0]):
            vehicle_type = 0
        elif (temp1 < cartype[1]):
            vehicle_type = 1
        elif (temp1 < cartype[2]):
            vehicle_type = 2
        elif (temp1 < cartype[3]):
            vehicle_type = 3
        if (temp2 < dist[0]):
            direction_number = 0
        elif (temp2 < dist[1]):
            direction_number = 1
        elif (temp2 < dist[2]):
            direction_number = 2
        elif (temp2 < dist[3]):
            direction_number = 3
        if (daytime < 360):
            sleeptime = 5
        elif (daytime >= 360 and daytime < 480):
            sleeptime = 2
        elif (daytime >= 480 and daytime < 720):
            sleeptime = 3
        elif (daytime >= 720 and daytime < 840):
            sleeptime = 2
        elif (daytime >= 840 and daytime < 1080):
            sleeptime = 3
        elif (daytime >= 1080 and daytime < 1260):
            sleeptime = 1
        elif (daytime >= 1260):
            sleeptime = 4
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(sleeptime)
        daytime += sleeptime


def turnp(probability):
    rnumber = random.uniform(0, 1)
    if rnumber > probability:
        return False
    else:
        return True


class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, args=())  # initialization
    thread1.daemon = True
    thread1.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersectionx4.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/redx4.png')
    yellowSignal = pygame.image.load('images/signals/yellowx4.png')
    greenSignal = pygame.image.load('images/signals/greenx4.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())  # Generating vehicles
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))  # display background in simulation
        for i in range(0,
                       noOfSignals):  # display signal and set timer according to current status: green, yello, or red
            if (i == currentGreen):
                if (currentYellow == 1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if (signals[i].red <= 10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["", "", "", ""]

        # display signal timer
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # display the vehicles
        for vehicle in simulation:
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()
        pygame.display.update()


Main()