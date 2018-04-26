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
        self.show_frame(TunePage, 1)


    def show_frame(self, cont, graph):
        self.graph = graph
        frame = self.frames[cont]
        frame.tkraise()

    def update(self):
        if (self.graph != -1):
            x = ( self.graph / 6 ) + 1
            y = self.graph - (6 * x)
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
        button1 = tk.Button(self, text="Tune Pid", command=lambda: controller.show_frame(TunePage, 0))
        button1.pack()

        canvas = FigureCanvasTkAgg(controller.f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()

class TunePage(tk.Frame):
    def __init__(self, parent, controller, mah):
        self.mah = mah
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Tune Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button0 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 0))
        button0.pack()
        button1 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 1))
        button1.pack()
        button2 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 2))
        button2.pack()
        button3 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 3))
        button3.pack()
        button4 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 4))
        button4.pack()
        button5 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 5))
        button5.pack()
        button6 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 6))
        button6.pack()
        button7 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 7))
        button7.pack()
        button8 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 8))
        button8.pack()
        button9 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 9))
        button9.pack()
        button10 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 10))
        button10.pack()
        button11 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 11))
        button11.pack()
        button12 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(TunePage, 12))
        button12.pack()

        canvas = FigureCanvasTkAgg(controller.f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()
