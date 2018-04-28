import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import Tkinter as tk
LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

class Visualization(tk.Tk):
    def __init__(self, mah, *args, **kwargs):
        self.mah = mah
        self.f = Figure(figsize=(5,5), dpi=100)
        self.graph = 0

        self.a = self.f.add_subplot(1,1,1)

        #self.update()


        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = TunePage(container, self, mah)
        self.frames[TunePage] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(TunePage, 0)


    def show_frame(self, cont, graph):
        self.graph = graph

        frame = self.frames[cont]
        frame.tkraise()

    def update(self):
        if (self.graph != -1):
            x = ( self.graph / 6 ) + 1
            y = self.graph - (6 * x) + 6
            data = self.mah.get_data(x,y)
            self.a.clear()
            if data is None or len(data[0]) == 0:
                self.a.plot([0,1],[0,1],[0,1],[0,0])
            else:
                self.a.plot(data[0], data[1], data[0], data[2])

    def animate(self, i):
        self.update()

class StartPage(tk.Frame):

    def __init__(self, parent, controller, mah):
        self.mah = mah
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Tune Pid", command=lambda: controller.show_frame(TunePage, 1))
        button1.pack()

        canvas = FigureCanvasTkAgg(controller.f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()

class TunePage(tk.Frame):
    def __init__(self, parent, controller, mah):
        self.controller = controller
        self.mah = mah
        tk.Frame.__init__(self, parent)
        x = 0
        y = 0
        self.label = tk.Label(self, text=self.get_title(controller.graph), font=LARGE_FONT)
        self.label.grid(column=x, row=y, columnspan=2, rowspan=2)
        y = y + 2

        button0 = tk.Button(self, text=self.get_title(0), command=lambda: self.change(0))
        button0.grid(column=x, row=y)
        y = y + 1

        button1 = tk.Button(self, text=self.get_title(1), command=lambda: self.change(1))
        button1.grid(column=x, row=y)
        y = y + 1

        button2 = tk.Button(self, text=self.get_title(2), command=lambda: self.change(2))
        button2.grid(column=x, row=y)
        y = y + 1

        button3 = tk.Button(self, text=self.get_title(3), command=lambda: self.change(3))
        button3.grid(column=x, row=y)
        y = y + 1

        button4 = tk.Button(self, text=self.get_title(4), command=lambda: self.change(4))
        button4.grid(column=x, row=y)
        y = y + 1

        button5 = tk.Button(self, text=self.get_title(5), command=lambda: self.change(5))
        button5.grid(column=x, row=y)
        x = x + 1
        y = y - 5

        button6 = tk.Button(self, text=self.get_title(6), command=lambda: self.change(6))
        button6.grid(column=x, row=y)
        y = y + 1

        button7 = tk.Button(self, text=self.get_title(7), command=lambda: self.change(7))
        button7.grid(column=x, row=y)
        y = y + 1

        button8 = tk.Button(self, text=self.get_title(8), command=lambda: self.change(8))
        button8.grid(column=x, row=y)
        y = y + 1

        button9 = tk.Button(self, text=self.get_title(9), command=lambda: self.change(9))
        button9.grid(column=x, row=y)
        y = y + 1

        button10 = tk.Button(self, text=self.get_title(10), command=lambda: self.change(10))
        button10.grid(column=x, row=y)
        y = y + 1

        button11 = tk.Button(self, text=self.get_title(11), command=lambda: self.change(11))
        button11.grid(column=x, row=y)
        y = y + 1

        button12 = tk.Button(self, text=self.get_title(12), command=lambda: self.change(12))
        button12.grid(column=x-1, row=y, columnspan=2)

        y = y - 6
        x = x + 1
        canvas = FigureCanvasTkAgg(controller.f, self)
        canvas.show()
        canvas.get_tk_widget().grid(column=x, row=y, rowspan=7, columnspan=7)

        x = 3
        y = 0
        self.p_value = tk.Label(self, text='', font=LARGE_FONT)
        self.p_value.grid(column=x, row=y)
        x = x + 1
        self.i_value = tk.Label(self, text='', font=LARGE_FONT)
        self.i_value.grid(column=x, row=y)
        x = x + 1
        self.d_value = tk.Label(self, text='', font=LARGE_FONT)
        self.d_value.grid(column=x, row=y)
        x = 3
        y = 1
        self.p_input = tk.Entry(self)
        self.p_input.grid(column=x, row=y)
        x = x + 1
        self.i_input = tk.Entry(self)
        self.i_input.grid(column=x, row=y)
        x = x + 1
        self.d_input = tk.Entry(self)
        self.d_input.grid(column=x, row=y)
        x = x + 1
        y = 0
        self.set_button = tk.Button(self, text='SET PID', command=lambda: self.set_pid())
        self.set_button.grid(column=x, row=y, columnspan=1, rowspan=2)
        x = x + 1

        self.save_button = tk.Button(self, text='SAVE PID', command=lambda: self.save())
        self.save_button.grid(column=x, row=y, columnspan=1, rowspan=2)

        self.clear = tk.Button(self, text='Clear Data', command=lambda: self.mah.clear_data(self.controller.graph))
        self.clear.grid(column=x, row=10)

        #self.graph = tk.Label(self, text='', font=LARGE_FONT)
        #self.graph.grid(column=x, row=y)

        self.update_pid()

        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.pack()

    def save(self):
        print "TODO: make a save function"

    def change(self, index):
        self.controller.graph = index
        self.label.config(text=self.get_title(index))
        p = "P: " + str(self.mah.get_pid(self.controller.graph, 0))
        i = "I: " + str(self.mah.get_pid(self.controller.graph, 1))
        d = "D: " + str(self.mah.get_pid(self.controller.graph, 2))
        self.p_value.config(text=p)
        self.i_value.config(text=i)
        self.d_value.config(text=d)

    def update_pid(self):
        p = "P: " + str(self.mah.get_pid(self.controller.graph, 0))
        i = "I: " + str(self.mah.get_pid(self.controller.graph, 1))
        d = "D: " + str(self.mah.get_pid(self.controller.graph, 2))

        self.p_value.config(text=p)
        self.i_value.config(text=i)
        self.d_value.config(text=d)
        self.mah.clear_data(self.controller.graph)

        #self.graph.config(text=str(self.controller.graph))

    def set_pid(self):
        try:
            p = float(self.p_input.get())
            i = float(self.i_input.get())
            d = float(self.d_input.get())
        except:
            return

        self.mah.tune(self.controller.graph, 0, p)
        self.mah.tune(self.controller.graph, 1, i)
        self.mah.tune(self.controller.graph, 2, d)
        self.update_pid()



    def get_title(self, number):
        x = ( number / 6 ) + 1
        y = number - (6 * x) + 6

        if x == 1:
            name = "Freeze: "
        elif x == 2:
            name = "Movement: "
        elif x == 3:
            return "HeightStabilizer"
        if y == 0:
            dof = 'X'
        elif y == 1:
            dof = 'Y'
        elif y == 2:
            dof = 'Z'
        elif y == 3:
            dof = 'Roll'
        elif y == 4:
            dof = 'Pitch'
        elif y == 5:
            dof = 'Yaw'

        return name + dof
