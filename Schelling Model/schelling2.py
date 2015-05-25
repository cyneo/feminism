import random
import sys
from tkinter import Frame, Canvas, Button, Label, Scale
import tkinter.messagebox
import time

"""
Copied from:
https://pythonisanthropology.wordpress.com/the-schelling-segregation-model/

Modified by CYNeo:
- Cleaned up formatting to fit Python standards
- Added grid slider for adjusting world size
- Added fill slider to adjust % of the world fill
- Added delay slider for delay between calculations

Want to add in a grid size slider

In Visual, _go:
- added sleep time of 0.15 s. Will find way to make a slider for it

In Visual, _entry:
- Added Fill Scale.
- Need to implement it in actual code
- Implemented by changing the way agents are generated
- Added a scale to modify the number of agents by increasing the size of the
  grid
"""


class Neighbour(dict):
    '''Takes a World object as parameter and returns the
    neigbours of each x & y coordinates in the world.

    Is a dictionary with self(x,y) as 'keys' and neigbors
    x, y as 'values' (which is
    a list consisting of individual neighbour coordinates
    stored as  x,y tuples).
    '''

    def __init__(self, world):
        '''At initialisation a dictionary consisting of neigbours all x,y
        values are created.
        Neighbour grid:
        -------------------------
        |(-1,1 )| (0,1 )| (1,1 )|
        -------------------------
        |(-1,0 )| (x,y )| (1,0 )|
        -------------------------
        |(-1,-1)| (0,-1)| (1,-1)|
        ------------------------- '''

        dict.__init__({})
        self.world = world
        self.xy = self.world.x_y_list()
        self.inhabited = world.inhabited()

        offset = [(-1, 1),
                  (0, 1),
                  (1, 1),
                  (-1, 0),
                  (1, 0),
                  (-1, -1),
                  (0, -1),
                  (1, -1)]

        for x, y in self.xy:
            tmp = []
            for i in range(len(offset)):
                x1 = x + offset[i][0]
                y1 = y + offset[i][1]
                if 0 <= x1 < self.world.grid_size and\
                   0 <= y1 < self.world.grid_size:
                    tmp.append((x1, y1))
            self[(x, y)] = tmp

    def neighbours_xy(self, x, y):
        '''Returns a list of neigbouring x,y values (tuple).

        Takes x,y as parameters.
        '''
        try:
            return self[x, y]
        except KeyError as err:
            print(str(err) + " is outside world's coordinate system.")

    def __str__(self):
        '''Prints the neigbour dictionary.'''
        s = ""
        for key in sorted(self):
            s += str(key) + ":" + str(self[key]) + "\n"
        return s


class Transform(dict):
    '''Class that takes a World object as input and sets up a dictionary
    with both cartesian and tkinter coordinates.
    '''
    def __init__(self, world):
        '''Stores world and set up dictcionary containing both
        cartesian and tkinter coordinates.'''
        dict.__init__({})
        self.world = world
        self._x_y_dict()

    def _x_y_dict(self):
        '''A dictionary consisting of tuples with x, y values.
        The lower left corner is 0,0 (cartesian) and their
        respective x, y coordinates in tkinter.'''
        self._graphics_list()
        self._xy_coords_orig()
        self._xy_coords_tkinter()

        for i in range(len(self.x_y_orig)):
            self[self.x_y_orig[i]] = self.x_y_tkinter[i]

    def _graphics_list(self):
        '''A method for creating a list/dictionary of which to
        create a graphics interface from.'''
        self.visual_list = [[0 for row in range(self.world.grid_size)]
                            for row in range(self.world.grid_size)]
        for x in range(self.world.grid_size):
            count = self.world.height - self.world.counter_y
            for y in range(self.world.grid_size):
                self.visual_list[x][y] = count
                count -= self.world.counter_y

        x = 0
        self.visual_dict = {}
        for element in self.visual_list:
            self.visual_dict[x] = element
            x += self.world.counter_x

    def _xy_coords_orig(self):
        self.x_y_orig = []
        for x in range(self.world.grid_size):
            for y in range(self.world.grid_size):
                self.x_y_orig.append((x, y))

    def _xy_coords_tkinter(self):
        self.x_y_tkinter = []
        for key in sorted(self.visual_dict):
            for i in range(self.world.grid_size):
                self.x_y_tkinter.append((key, self.visual_dict[key][i]))

    def tkinter_coords(self, x, y):
        '''Returns tkinter x, y values (tuple)
        Takes cartesian x,y as parameters.'''
        try:
            return self[x, y]
        except KeyError as err:
            print(str(err) + " is outside world's coordinate system.")

    def __str__(self):
        '''Prints the coordinates dictionary.
        'keys' are cartesian while 'values' are tkinter.'''
        s = ""
        for key in sorted(self):
            s += str(key) + ":" + str(self[key]) + "\n"
        return s


class World(object):
    '''A n X n grid as a spatial representation of a
    world where things happen.'''

    def __init__(self, width, height, n=2):
        self.width = width
        self.height = height
        self.grid_size = n

        self.counter_x = self.width/self.grid_size
        self.counter_y = self.height/self.grid_size
        self.coordinates = Transform(self)
        self.patch_list = [[0 for row in range(n)] for row in range(n)]
        self.neighbour = Neighbour(self)

    def patches(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if not self.patch_list[x][y]:
                    new_patch = Patch(world=self, x=x, y=y, s='P')                 
                    self.register(new_patch)

    def x_y_tkinter(self, x, y):
        '''Returns the tkinter coordinates from cartesian x,y,
        i.e. it calls on a method in Transform.'''
        return self.coordinates.tkinter_coords(x, y)

    def x_y_list(self):
        '''Returns the list of the world's x,y coordinates (cartesian).'''
        return self.coordinates.x_y_orig

    def inhabited(self):
        '''Returns the list of cells with patches.'''
        return self.patch_list

    def register(self, patch):
        '''Register a patch in the World, i.e. put the patch at it's
        coordinates in the World's patch_list.'''
        x = patch.x
        y = patch.y
        self.patch_list[x][y] = patch

    def remove(self, patch):
        '''Remove a patch from the World, i.e. put remove the patch from
        it's current coordinates in the World's patch_list by replacing
        it with zero.'''
        x = patch.x
        y = patch.y
        self.patch_list[x][y] = 0


class Patch(object):
    '''A class that defines separate entity called Patch.
    They inhabit a world and conceptualises a patch in an artificial
    n x n spatial environment.
    '''
    def __init__(self, world, x=0, y=0, s="P", color='dark green'):
        '''Initialise the patches and their position.'''
        self.world = world
        self.name = s
        self.x = x
        self.y = y
        self.color = color
        self.x_draw, self.y_draw = self.world.x_y_tkinter(self.x, self.y)
        self.get_neighbours()

    def position(self):
        '''Return coordinates of current position.'''
        return self.x, self.y, self.x_draw, self.y_draw

    def draw(self, canvas, text1=False):
        '''Method for drawing a patch.
        text1 is a helper parameter to check coordinates,
        both cartesian and tkinter.'''
        x = self.x_draw
        y = self.y_draw
        canvas.create_rectangle(x, y,
                                x+self.world.counter_x,
                                y+self.world.counter_y,
                                fill=self.color, tag=self.name)
        # Debugging
        if text1:
            font = 'Arial ' + str(int(self.world.counter_y//6))
            font1 = 'Arial ' + str(int(self.world.counter_y//7))
            canvas.create_text(x+5, y+(self.world.counter_y/10),
                               text="(" + str(self.x) + "," +
                               str(self.y) + ")",
                               anchor='nw',
                               justify='center',
                               font=font)
            canvas.create_text(x+5, y+self.world.counter_y -
                               (self.world.counter_y/1.5),
                               text="(" + str(int(x)) + "," +
                               str(int(y)) + ")",
                               anchor='nw',
                               justify='center',
                               font=font1)

            c, c1 = canvas.coords(self.name)[0], canvas.coords(self.name)[1]
            c = int(c)
            c1 = int(c1)
            canvas.create_text(x+5, y+self.world.counter_y -
                               (self.world.counter_y/2.5),
                               text="(" + str(c) + "," + str(c1) + ")",
                               anchor='nw', justify='center', font=font1)

    def draw_move(self, canvas, x_old, y_old, text1=False):
        '''Move using canvas.move method'''

        canvas.move(self.name, self.x_draw-x_old, self.y_draw-y_old)

        # Debugging
        if text1:
            x = self.x_draw
            y = self.y_draw

            font = 'Arial ' + str(int(self.world.counter_y//6))
            font1 = 'Arial ' + str(int(self.world.counter_y//7))

            canvas.create_text(x+5, y+(self.world.counter_y/10),
                               text="(" + str(self.x) +
                               "," + str(self.y) + ")",
                               anchor='nw', justify='center',
                               font=font)
            canvas.create_text(x+5, y+self.world.counter_y -
                               (self.world.counter_y/1.5),
                                     text = "(" + str(int(x)) + "," + str(int(y))+ ")",
                                     anchor = 'nw',justify = 'center', font = font1)
 
            c, c1 = canvas.coords(self.name)[0], canvas.coords(self.name)[1]
            c = int(c)
            c1 = int(c1)
            canvas.create_text(x+5, y+self.world.counter_y -
                               (self.world.counter_y/2.5),
                               text="(" + str(c) + "," + str(c1) + ")",
                               anchor='nw', justify='center', font=font1)

    def get_neighbours(self):
        '''Method for getting the Patch's neighbours x, y coordinates.
        Stores them in a list.'''
        self.neighbours = self.world.neighbour.neighbours_xy(self.x, self.y)

    def get_neighbouring_patches(self):
        '''Method for creating a list containing neighbouring pathces.
        Stores them in a list.'''

        self.neighbours_patches = []
        for x, y in self.neighbours:
            if self.world.patch_list[x][y]:
                patch = self.world.patch_list[x][y]
                self.neighbours_patches.append(patch)

    def set_color(self, color):
        '''Method to set the color.'''
        self.color = color

    def __str__(self):
        '''String representation when printing object.'''
        x, y, z, w = self.position()
        s = self.name + ":" + "(" + str(x) + "," + str(y) + ")"
        return s


class Schelling(Patch):
    '''An object that inherits from the Patch class.
       Added functionality consist of movement.'''

    def __init__(self, world, x=0, y=0, s="S",
                 color='dark green', similar_wanted=0.3):
        Patch.__init__(self, world, x, y, s, color)
        self.happy = False
        self.percent_similar = similar_wanted

    def move(self, visual, debug=False):
        '''Move method - can move to random location in the world.

        When debug = True helpful info for checking
        if everything works as intended is printed.'''

        if not any(0 in element for element in self.world.patch_list):
            tkinter.messagebox.showwarning("Warning", "No place to move!")
            visual.movement_possible = False
            visual.master.destroy()
            quit()

        else:
            # new x,y
            x = random.randint(0, self.world.grid_size-1)
            y = random.randint(0, self.world.grid_size-1)
             
            while self.world.patch_list[x][y] != 0:
                x = random.randint(0, self.world.grid_size-1)
                y = random.randint(0, self.world.grid_size-1)

            if debug:
                print('Move, {}, from ({},{}) to ({},{}) '.format(
                    self.name, self.x, self.y, x, y))

            # Remove from previous location
            self.world.remove(self)

            # Update patch
            self.x, self.y = x, y
            x_old, y_old = self.x_draw, self.y_draw

            self.x_draw, self.y_draw = self.world.x_y_tkinter(self.x, self.y)

            # Register and draw patch at new coordinates
            self.world.register(self)
            self.draw_move(visual.canvas, x_old, y_old)

    def update_neighbours(self):
        '''A method that update the Schelling's neigbours attributes,
        i.e. both x,y for neighbours and list of neigbouring pathces.'''
        self.get_neighbours()
        self.get_neighbouring_patches()

    def is_happy(self):
        '''Method to check if whether Schelling is happy or not, i.e.
        if a given percentage or above of neighbouring objects are similar
        to itself, the object is happy.
        '''
        no_neighbours = len(self.neighbours_patches)
         
        if no_neighbours > 0:
            similar = 0
            for other in self.neighbours_patches:
                if other.color == self.color:
                    similar += 1
            prop_similar = similar/no_neighbours

            if prop_similar >= self.percent_similar:
                self.happy = True
            else:
                self.happy = False
        else:
            self.happy = False


class Plotcoords:
    """Internal class for 2-D coordinate transformations.

       Adopted from graphics.py by Jonh Zelle for use with the book
       'Python Programming: An Introduction to Computer Science' Link:
       http://mcsp.wartburg.edu/zelle/python. """
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)

    def screen(self, x, y):
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs + 0.5), int(ys + 0.5)


# GUI
class Visual(Frame):
    '''Class that takes a world as argument and present it graphically
    on a tkinter canvas.'''

    def __init__(self):
        '''
        Sets up a simulation GUI in tkinter.
        '''
        Frame.__init__(self)
        self.master.title("The Schelling Segregation Model in Python")
        self.master.wm_resizable(0, 0)
        self.grid()
        self.movement_possible = True

        # --------------------------------------- #
        # --------- FRAMES FOR GUI -------------- #
        # --------------------------------------- #

        # The pane for user values
        self._entryPane = Frame(self,
                                borderwidth=5,
                                relief='sunken')
        self._entryPane.grid(row=0, column=0, sticky='n')

        # The buttons pane
        self._buttonPane = Frame(self, borderwidth=5)
        self._buttonPane.grid(row=1, column=0, sticky='n')

        # A temp pane where graph is located, just for cosmetic reasons
        width, height = 425, 350
        self._graph = Canvas(self,
                             width=width,
                             height=height,
                             background="black")
        self._graph.configure(relief='sunken', border=2)
        self._graph.grid(row=3, column=0)

        # The pane where the canvas is located
        self._animationPane = Frame(self,
                                    borderwidth=5,
                                    relief='sunken')
        self._animationPane.grid(row=0, column=1,
                                 rowspan=4, pady=10,
                                 sticky="n")

        # --------------------------------------- #
        # --------- FILLING THE FRAMES ---------- #
        # --------------------------------------- #

        self._canvas()      # Create graphics canvas
        self._entry()       # Create entry widgets
        self._buttons()     # Create button widgets

    def _plot_setup(self, time):
        '''Method for crudely annotating the graph window.'''
        time = time

        # Main plot
        width, height = 425, 350
        y0 = -time/10
        self._graph = Canvas(self, width=width,
                             height=height,
                             background="black",
                             borderwidth=5)
        self._graph.grid(row=3, column=0)
        self.trans = Plotcoords(width, height, y0, -0.2, time, 1.3)

        x, y = self.trans.screen(time // 2, 1.2)
        x1, y1 = self.trans.screen(time // 2, 1.13)
        self._graph.create_text(x, y,
                                text="% Happy",
                                fill="green",
                                font="bold 12")
        
        self._graph.create_text(x1, y1,
                                text="% Unhappy",
                                fill="red",
                                font="bold 12")
 
        # Line x-axis
        x, y = self.trans.screen((-5 * (time / 100)), -0.05)
        x1, y = self.trans.screen(time, -0.05)
        self._graph.create_line(x, y, x1, y, fill="white", width=1.5)
         
        # Text x-axis
        x_text, y_text = self.trans.screen(time / 2, -0.15)
        self._graph.create_text(x_text, y_text,
                                text="Time",
                                fill="white",
                                font="bold 12")

        # Line y-axis
        x, y = self.trans.screen((-0.5 * (time / 100)), -0.05)
        x, y1 = self.trans.screen((-5 * (time / 100)), 1)
        self._graph.create_line(x, y, x, y1, fill="white", width=1.5)
 
    def _entry(self):
        '''Method for creating widgets for collecting user input.'''
         
        # N (no of turtles)
        dim = 30*30

        self.fill_label = Label(self._entryPane,
                                anchor='w',
                                justify='left',
                                text='Fill',
                                relief='raised',
                                width=12,
                                height=1,
                                font='italic 20')
        
        self.fill_label.grid(row=0, column=1, ipady=14)

        self.fill = Scale(self._entryPane,
                          from_=0,
                          to=1,
                          resolution=0.01,
                          bd=3,
                          relief='sunken',
                          orient='horizontal',
                          length=235,
                          tickinterval=20)
        self.fill.grid(row=0, column=2)
        self.fill.set(0.8)
                           
        self._N_label = Label(self._entryPane,
                              anchor='w',
                              justify='left',
                              text="N:",
                              relief='raised',
                              width=12,
                              height=1,
                              font="italic 20")
        self._N_label.grid(row=1, column=1, ipady=14)

        self._N = Scale(self._entryPane,
                        from_=0,
                        to=100,
                        resolution=1,
                        bd=3,
                        relief='sunken',
                        orient='horizontal',
                        length=235,
                        tickinterval=20)
        self._N.set(30)
        self._N.grid(row=1, column=2)

        # Ticks (length of simulation)
        self._Ticks_label = Label(self._entryPane,
                                  anchor='w',
                                  justify='left',
                                  text="Time:",
                                  relief='raised',
                                  width=12,
                                  height=1,
                                  font="bold 20")
        self._Ticks_label.grid(row=2, column=1, ipady=14)
 
        self._Ticks = Scale(self._entryPane,
                            from_=10,
                            to=1000,
                            resolution=1,
                            bd=3,
                            relief='sunken',
                            orient='horizontal',
                            length=235,
                            tickinterval=990)
        self._Ticks.set(500)
        self._Ticks.grid(row=2, column=2)
 
        # % similar wanted
        self._Similar_label = Label(self._entryPane,
                                    anchor='w',
                                    justify='left',
                                    text="Similar wanted:",
                                    relief='raised',
                                    width=12,
                                    height=1,
                                    font="bold 20")
         
        self._Similar_label.grid(row=3, column=1, ipady=14)
 
        self._Similar = Scale(self._entryPane,
                              from_=0.0,
                              to=1.0,
                              resolution=0.01,
                              bd=3,
                              relief='sunken',
                              orient='horizontal',
                              length=235,
                              tickinterval=0.5)
        self._Similar.set(0.76)
        self._Similar.grid(row=3, column=2)

        # Delay between steps
        self._delay_label = Label(self._entryPane,
                                  anchor='w',
                                  justify='left',
                                  text="Delay (s):",
                                  relief='raised',
                                  width=12,
                                  height=1,
                                  font="bold 20")
         
        self._delay_label.grid(row=4, column=1, ipady=14)
 
        self._delay = Scale(self._entryPane,
                            from_=0.0,
                            to=1.0,
                            resolution=0.01,
                            bd=3,
                            relief='sunken',
                            orient='horizontal',
                            length=235,
                            tickinterval=0.5)
        self._delay.set(0.15)
        self._delay.grid(row=4, column=2)

    def _buttons(self):
        '''Method for creating button widgets for setting up,
        running and plotting results from simulation.'''
        width = 7
        height = 1

        # The 'Setup' button
        self._setupButton = Button(self._buttonPane,
                                   text="Setup",
                                   command=self._setup,
                                   width=width,
                                   height=height,
                                   font="bold 30",
                                   relief='raised',
                                   borderwidth=5)
        self._setupButton.grid(row=0, column=0)

        # The 'Go' button
        self._goButton = Button(self._buttonPane,
                                text="Go",
                                command=self._go,
                                width=width,
                                height=height,
                                font="bold 30",
                                relief='raised',
                                borderwidth=5)
        self._goButton.grid(row=0, column=1)

        # The 'Quit' button
        self._quitButton = Button(self._buttonPane,
                                  text="Quit",
                                  command=self._quit,
                                  width=width,
                                  height=height,
                                  font="bold 30",
                                  relief='raised',
                                  borderwidth=5)
        self._quitButton.grid(row=1, column=0, columnspan=2)

    def _canvas(self):
        '''Creates the canvas on which everything happens.'''
        # The tick counter information
        self._Tick_counter = Label(self._animationPane,
                                   anchor='w',
                                   justify='left',
                                   text="Time:",
                                   width=5,
                                   font="bold 20")
        self._Tick_counter.grid(row=0, column=0, sticky="e")
        self._Tick_counter1 = Label(self._animationPane,
                                    justify='center',
                                    text="",
                                    relief='raised',
                                    width=5,
                                    font="bold 20")
        self._Tick_counter1.grid(row=0, column=1, sticky='w')
        self.canvas_w, self.canvas_h = 750, 750
        self.canvas = Canvas(self._animationPane,
                             width=self.canvas_w,
                             height=self.canvas_h,
                             background="black")

        self.canvas.grid(row=1, column=0, columnspan=2)

    def _setup(self):
        '''Method for 'Setup' button.'''
        # Clearing the canvas and reset the go button
        self.canvas.delete('all')
        self._goButton['relief'] = 'raised'
        self.N = int(self._N.get())
        self.Ticks = int(self._Ticks.get())
        self.similar = float(self._Similar.get())
        self.data = []
        self.tick_counter = 0
        self._Tick_counter1['text'] = str(self.tick_counter)
        self._plot_setup(self.Ticks)
        self.grid_size = self.N
        self.world = World(750, 750, self.grid_size)
        self.create_turtles()
        self.neighbouring_turtles()
        self.draw_turtles()

    def _go(self):
        '''Method for the 'Go' button, i.e. running the simulation.'''
        self._goButton['relief'] = 'sunken'
        if self.tick_counter <= self.Ticks:
            self._Tick_counter1['text'] = str(self.tick_counter)
            self.canvas.update()

            self._graph.update()
            self._graph.after(0)

            # Data collection
            turtles_unhappy = self.check_satisfaction()
            prop_happy, prop_unhappy = self.calc_prop_happy(self.tick_counter)

            self.data_collection(self.tick_counter, prop_happy, prop_unhappy)

            if self.tick_counter >= 1:

                # HAPPY values (%)
                x0 = self.tick_counter-1
                x1 = self.tick_counter

                # Collecting values from stored data
                y0 = self.data[self.tick_counter-1][1]
                y1 = self.data[self.tick_counter][1]

                # Transforming to tkinter
                x1, y1 = self.trans.screen(x1, y1)
                x0, y0 = self.trans.screen(x0, y0)
                self._graph.create_line(x0, y0, x1, y1,
                                        fill="green", width=1.3,
                                        tag="happy")  # Draw "happy lines

                # UNHAPPY values (%)
                x0 = self.tick_counter-1
                x1 = self.tick_counter

                # Collecting values from stored data
                y0 = self.data[self.tick_counter-1][2]
                y1 = self.data[self.tick_counter][2]

                # Transforming to tkinter
                x1, y1 = self.trans.screen(x1, y1)
                x0, y0 = self.trans.screen(x0, y0)
                self._graph.create_line(x0, y0, x1, y1,
                                        fill="red", width=1.1,
                                        tag="unhappy")  # Draw unhappy lines
             
            if prop_happy < 1:
                self.turtle_move(turtles_unhappy)
                time.sleep(self._delay.get())
                self.update_neighbours()
                self.tick_counter += 1
                self.canvas.after(0, self._go())

        self._goButton['relief'] = 'raised'

    def _quit(self):
        '''Method for the 'Quit' button.'''
        self.master.destroy()

    # ------------------------------------------------------ #
    # ---------- FUNCTIONS CALLED AT EACH TICK ------------- #
    # ------------------------------------------------------ #

    def turtle_move(self, unhappy_turtles):
        '''Moves all the unhappy turtles (randomly).'''
         
        while unhappy_turtles:
            i = random.randint(0, len(unhappy_turtles)-1)
            turtle = unhappy_turtles.pop(i)
            turtle.move(self)

    def update_neighbours(self):
        '''Updates the turtles neigbour attributes. Called
        after all turtles have moved.'''
        for turtle in self.turtles:
            turtle.update_neighbours()

    def check_satisfaction(self):
        '''Checks to see if turtles are happy or not.
        Returns a list of unhappy turtles, i.e. turtles
        that should move.

        Called before the move method.'''

        for turtle in self.turtles:
            turtle.is_happy()

        unhappy_turtles = []
        for element in self.turtles:
            if not element.happy:
                unhappy_turtles.append(element)

        return unhappy_turtles

    def calc_prop_happy(self, i):
        '''Calculates the proportion of happy turtles.'''
        happy = 0
        unhappy = 0

        for turtle in self.turtles:
            if turtle.happy:
                happy += 1
            else:
                unhappy += 1
        prop_happy = happy/len(self.turtles)
        prop_unhappy = unhappy/len(self.turtles)

        return prop_happy, prop_unhappy

    def data_collection(self, i, prop_happy, prop_unhappy):
        '''Method for collecting data at each tick.'''
        self.data.append((i, prop_happy, prop_unhappy))


# ------------------------------------------------------ #
# ---------- INITIALISATION FUNCTIONS ------------------ #
# ------------------------------------------------------ #

    def create_turtles(self):
        '''Method for creating a new list of turtles.

        Upon creation they are registered in the World object.'''
        if self.N*self.N <= self.grid_size*self.grid_size:
            counter = 0
            self.turtles = []
            while counter < self.N * self.N * self.fill.get():
                             
                s = "S"+str(counter)
                if counter <= int(self.N * self.N * self.fill.get() / 2):
                    color = "green"
                else:
                    color = "red"

                x = random.randint(0, self.grid_size-1)
                y = random.randint(0, self.grid_size-1)

                if not self.world.patch_list[x][y]:
                    new_turtle = Schelling(world=self.world,
                                           x=x,
                                           y=y,
                                           s=s,
                                           color=color,
                                           similar_wanted=self.similar)

                    self.world.register(new_turtle)
                    counter += 1
                    self.turtles.append(new_turtle)
        else:
            print("Number of turtles exceeds world!")

    def draw_turtles(self):
        '''Method for drawing turtles on canvas.

           Calls each turtle's own method for drawing.'''
        for turtle in self.turtles:
            turtle.draw(self.canvas)
 
    def neighbouring_turtles(self):
        '''Method for updating turtles' neighbours.

           Calls on each turtle's own method for updating neighbours.'''
        for turtle in self.turtles:
            turtle.get_neighbouring_patches()


def main():
    sys.setrecursionlimit(10000)
    Schelling = Visual()
    Schelling.mainloop()
 
if __name__ == '__main__':
    main()
