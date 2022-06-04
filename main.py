
import tkinter as tk
from tkinter import  Toplevel

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
HISTORY_FONT_STYLE = ("Arial", 14)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class Calculator():
    def __init__(self):    #init method ha ya
        self.window = tk.Tk()
        self.window.geometry("375x667")   #specify the height and witdh of the window
        self.window.resizable(0, 0)       #disable resizing of window
        self.window.title("Calculator")   #window label as calculator

        self.total_expression = ""        #Total expression that display on top of screen with small font
        self.current_expression = ""      #Total expression that display on front of screen with large font
        self.display_frame = self.create_display_frame()        #frame for display
        self.file = open("result.txt", "a+")

        self.history = tk.Button(self.window,
                                 text='History',
                                 bg=LIGHT_BLUE,
                                 fg=LABEL_COLOR,
                                 font=HISTORY_FONT_STYLE,
                                 borderwidth=0,
                                 command = self.view_history).pack(side='top', anchor='nw')

        self.total_label, self.label = self.create_display_labels() #label display

        self.digits = {                         #dictionary to create a digit
            7: (1, 1), 8: (1, 2), 9: (1, 3),    #7:(1,1) 7 place with row 1 coloum 1
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()        #frame for buttons

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def view_history(self):
        top = Toplevel(self.window)

        top.geometry("300x500")
        top.title("History")



        HistoryTextViewer = tk.Text(top, state='disabled', width=44, height=5)
        self.file.seek(0)
        HistoryTextViewer.config(state="normal")
        HistoryTextViewer.insert(tk.END, self.file.read())
        HistoryTextViewer.config(state="disabled")
        HistoryTextViewer.pack(expand=1, fill=tk.BOTH)

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):    #method for displaying labels
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)  # for total expersision  anchor=tk.E will help the position thetext for east side of the fram
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)      #for current experssion
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):        #method to display frames
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)    #since this fram is inside main window so we specify height
        frame.pack(expand=True, fill="both")    #these argument will allow our fram to expand and fill any empty space around it
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self): #method for creating digit button
        for digit, grid_value in self.digits.items():   #digit in dictionary
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW) #pass row grid value 1  and coloum as a grid value 2 nsew(north,south,east west) so button willstick to every sideand fill up the entire grid

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.file.write('square of ' + str(self.current_expression) + ' = ' + str(int(self.current_expression)**2) + '\n')
        self.file.close()
        self.file = open("result.txt", "a+")

        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.file.write('sqrt of ' + str(self.current_expression) + ' = ' + str(int(self.current_expression) ** 0.5) + '\n')
        self.file.close()
        self.file = open("result.txt", "a+")

        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.file.write(self.total_expression + ' = ' + self.current_expression + '\n')
            self.file.close()
            self.file = open("result.txt", "a+")

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):     #method for displaying button
        frame = tk.Frame(self.window)   #create a frame
        frame.pack(expand=True, fill="both") #
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):  #method to run calculator
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()     #object of calculator class
    calc.run()

