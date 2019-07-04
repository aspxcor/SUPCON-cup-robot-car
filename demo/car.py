import pyfirmata
from time import sleep

class Car:
     # The normal speed
    SPEED = 0.5

    def __init_constants(self):
        ## CONSTANTS
        # actual speed(right):speed(left)
        self.LEFT_RATIO = 0.8
        self.A2D_THRESHOLD = 0.5
        # inverse ifrared in self-contructed environment
        self.INFRARED_INVERSED = True
        self.WHITE = 0
        self.BLACK = 1
        # turn sleep interval(s) to make sure the direction is right
        self.TURN_WAIT_INTERVAL = 0.5
        # adjust speed(a small turn) when following line
        self.ADJUST_COEFF = 0.065
       
        # weight for adjust go_straight (order: infrared 0 .. 3)
        self.WEIGHT = (3, 1, -1, -3)

        # the speed of the 2 motors
        self.speed = {'left': 0.85, 'right': 0.85}

        # states space
        self.trans_states = ['TURN', 'FOLLOW_LINE']
        self.count_states = ['COUNT_LINE', 'OFF_LINE']

        # direction space (counter-clockwise)
        self.direction_space = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init_globals(self):
        ## Globals in the class
        # variables for proper turning state transition
        # if not is following the line, turn left
        self.state = 'FOLLOW_LINE'
        self.count_state = 'OFF_LINE'


        # position
        # uniquely determine which segment is the car on
        # by specifying the most recently passed by coordinate
        # and the direction the car is going
        self.position = (-1, 1) # initial position
        self.direction = (1, 0)

    def __init__(self):
        self.__init_constants()
        self.__init_globals()
        self.__init_map()

        ## init
        self.board = pyfirmata.ArduinoMega('/dev/ttyUSB0')
        
        self.__init_motor()
        self.__init_infrared()
        
        # refresh GPIO input
        it = pyfirmata.util.Iterator(self.board)
        it.start()
        sleep(0.1)
        
    def __init_map(self):
        self.map = []
        for i in range(0, 10):
            self.map.append([0]*10)
        
        # the platform area
        for i in range(3, 7):
            for j in range(3,7):
                self.map[i][j] = 1
        
        # assume all obstacles are there for convenience
        for pos in [(8, 1), (8, 4), (8, 8), (5, 8), (1, 5), (1, 8)]:
            self.map[pos[0]][pos[1]] = 1
        
    def __init_motor(self):
        self.motor = {}
        # left motor
        self.motor['left_1'] = self.board.get_pin('d:4:o')
        self.motor['left_2'] = self.board.get_pin('d:3:o')
        self.motor['left_pwm'] = self.board.get_pin('d:2:p')
        
        # right motor
        self.motor['right_1'] = self.board.get_pin('d:6:o')
        self.motor['right_2'] = self.board.get_pin('d:5:o')
        self.motor['right_pwm'] = self.board.get_pin('d:7:p')
        
        
        # the motors should stay still at the initial state
        
    def __init_infrared(self):
        order = (2, 3, 5, 4, 1, 0, 6, 7)
        self.infrared = [self.board.get_pin('a:{}:i'.format(i)) for i in order]
    
    # only used for test purposes
    def __test_infrared(self):
        res = [i.read() for i in self.infrared]
        print(res)
        sleep(0.1)
        
    # analog signal converted to digital
    def __get_infrared(self, which_one):
        res = 0
        if self.infrared[which_one].read() > self.A2D_THRESHOLD:
            res = 1
        if self.INFRARED_INVERSED:
            res = 1 - res
        return res
    
    def __is_online(self, which_one):
        return self.__get_infrared(which_one) == self.WHITE

    def __set_state(self, state):
        assert state in self.trans_states, '{} is not a valid state!'.format(state)
        self.state = state
        
    def __is_state_equal(self, state):
        assert state in self.trans_states, '{} is not a valid state!'.format(state)
        return self.state == state

    def __set_count_state(self, state):
        assert state in self.count_states, '{} is not a valid count state!'.format(state)
        self.count_state = state
        
    def __is_count_state_equal(self, state):
        assert state in self.count_states, '{} is not a valid count state!'.format(state)
        return self.count_state == state
    
    def __go_straight(self, speed=SPEED):
        self.__motor('left', speed)
        self.__motor('right', speed)
        
    def __go_straight(self, left_speed, right_speed):
        if left_speed > 1:
            left_speed = 1
        if left_speed < 0:
            left_speed = 0
        if right_speed > 1:
            right_speed = 1
        if right_speed < 0:
            right_speed = 0 
        self.__motor('left', left_speed)
        self.__motor('right', right_speed)
    
    # turn_direction: 'left' or 'right'
    def __update_direction(turn_direction):
        if turn_direction == 'left':
            offset = 1
        else:
            offset = -1

        self.direction = self.direction_space[(self.direction_space.index(turn_direction) + offset + 4) % 4]

    
    # direction:
    # speed > 0: left
    # speed < 0: right
    def __turn(self, speed):
        self.__motor('left', -speed)
        self.__motor('right', speed)
    
        
    # detects when to stop
    # isFinished is returned
    # returns False when the turn is finished
    # otherwise, True is returned
    def __turn90(self, speed):
        if not self.__is_state_equal('TURN'):
            return
        
        self.__turn(speed)
        
        if speed < 0:    # turn right
            detector = 3
        else:
            detector = 0     # turn left
            
        #print('infrared:', self.__get_infrared(detector))
        if self.__get_infrared(detector) == self.WHITE:
            self.__go_straight(0, 0)  # suitable to stay still?
            # wait an interval(about 0.1s) for faster adjustment
            sleep(self.TURN_WAIT_INTERVAL) 
            self.__set_state('FOLLOW_LINE')
            
        
    def __motor(self, which_motor, speed):   
        one = 1
        if speed < 0:
            speed = -speed
            one = 0
            
        if which_motor == 'left':
            speed = speed * self.LEFT_RATIO
            
        self.motor['{}_1'.format(which_motor)].write(one)
        self.motor['{}_2'.format(which_motor)].write(1 - one)
        self.motor['{}_pwm'.format(which_motor)].write(speed)
        
        # follow the white line
    def __follow_line(self):
        if not self.__is_state_equal('FOLLOW_LINE'):
            return
        
        delta = sum([int(self.__get_infrared(i) == self.BLACK) * self.WEIGHT[i] for i in range(0, 4)])
        diff = delta * self.ADJUST_COEFF
        
        self.__go_straight(self.speed['left'] + diff, self.speed['right'] - diff)
        # print('left:', self.speed['left'], 'right:', self.speed['right'])
        
    def __get_next_position(self):
        return tuple(self.position[i] + self.direction[i] for i in (0, 1))

    def __update_position(self):
        self.position = self.__get_next_position()

    # check if the next position is available
    def __is_next_position_avail(self):
        next_pos = self.__get_next_position()
        return self.map[next_pos[0]][next_pos[1]] == 0

    def __count_line(self):
        if self.__is_state_equal('FOLLOW_LINE'):
            if self.__is_count_state_equal('OFF_LINE'):
                if self.__is_online(4):
                    self.__set_count_state('COUNT_LINE')

            if self.__is_count_state_equal('COUNT_LINE'):
                if not self.__is_online(4):
                    self.__set_count_state('OFF_LINE')
                    self.__update_position()

        if self.__is_state_equal('TURN'):
            # figure the special case out
            pass

    # returns the position difference in tuple, pos2 - pos1
    def __pos_diff(self, pos1, pos2)
        return (pos2[0] - pos1[0], pos2[1] - pos1[0])
            
    # pos: a tuple (x, y), returns True if succeeds, otherwise, False is returned
    # the direction of the car when it reaches the destination
    def move(self, destination, dest_direction):
        # perform every loop to make sure the position is right
        self.__count_line()
        # test print
        print('position', self.position)

        # figure out the relative position
        # turn if necessary (when <0 relative position value occurs
        # & when obstacle occurs)
        # make sure the direction maximun consistency
        # move to the next position
        if self.__is_count_state_equal('COUNT_LINE'):   # when on a point
            diff = self.__pos_diff(self.position, destination)

            possible_directions = []

            # extract the 2 possible directions from the diff data
            x = diff[0] / abs(diff[0])
            y = diff[1] / abs(diff[1])
            
            if x != 0:
                possible_directions.append((x, 0))

            if y != 0:
                possible_directions.append((y, 0))

            # if there's obstacle, change direction
            if self.direction in possible_directions:
                 self.__follow_line()
            elif len(possible_directions):   # or (len(possible_directions) == 2 and self.direction not in possible_directions):
                self.direction = possible_directions[0]
                # update the car direction
                
            else:
                # move ends
                pass


            # if there's obstacle, possible direction in None



        # move next_position->destination
        # go ahead go back
        if self.__is_count_state_equal('OFF_LINE'):
            self.__follow_line()
        
    
    def loop(self):
        while True:
            self.__test()
            
    def __test(self):
        # TEST1 __go_straight success
        #self.__go_straight(0.5, 0.5)
            
        # TEST2 __turn90_aux
        # self.__turn90_aux(0.5)
            
        # TEST3 test the infrared sensors
        # self.__test_infrared()
            
        # TEST4 test turn90
        # self.__set_state('TURN')
        # self.__turn90(0.5)
            
        # TEST5 follow line
        # self.__follow_line()
        
        # TEST6 move & count lines
        self.move((2, 0), (1, 0))
            
car = Car()
car.loop()


    
        
        
    
