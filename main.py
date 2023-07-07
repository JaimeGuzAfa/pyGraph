"""
Pygraph Graphing Calculator
AP CSP Performance Task

Built using Python and Brython Graphics on CodeHS
Additional graphics made using Canva.com and FireAlpaca.com. 
"""

"""
PyGraph is a graphic calculator, its works by asking the user for an equation
in either quadratic standard form or linear slope-intercept form. Then, each term
of the equation is separated into its corresponding variable. Later, they are plotteed
using multiple small circles that are placed in the desired shape (parabolas or lines) and
positioned based on the equation(s) entered
"""


import math 

# These variables assign the values given to set up the dimensions of the graph.
width = 576
height = 630

# This function sets the size of the canvas.
set_size(width, height)

# a dictionary used by the graph() function that contains all x-positions on the graph
x_coords = {}

# a dictionary that contains all the colors in which the equations can be plotted.
# However, it also holds functionality in other parts of the program that require colors
colors = {1: Color.red, 2: Color.blue, 3: Color.green}

# the following lists store all important values given by the inputs entered
current_equations = []
equation_information = []
stored_colors = []

# times the pop-up button has been clicked, used to determine if to display the pop-up or hide it
pop_up_times_clicked = 0


"""
These variables assigned a boolean value which will allow a function to process
whether a button is functional or not. 
"""
can_click_tutorial = True
can_click_back_from_tutorial = False
can_click_to_start = True

can_click_amount = False
can_click_1 = False
can_click_2 = False
can_click_3 = False

can_click_for_info = False
can_click_restart = False


"""
This function is the responsible for assigning each graph position from 
-18 to 18 to its respective canvas position and from coordinates 0-576 in  
the x axis.
""" 
def translate_canvas_cords_to_graph_cords():
    j = 0
    for i in range(37*64):
        j += 0.015625
        x_coords[-18.25 + j] = i / 4 


# This functions sets up the graph.
def set_up_graph():
    translate_canvas_cords_to_graph_cords()
    
    # Makes the vertical lines.
    for x in range(height):
        # % 16 becuase every 16 brython-units, a line should be added
        if x % 16 == 0:
            line = Line(x, 0, x, 576)
            line.set_color(Color.gray)
            add(line)
            
    # Makes the horizontal lines.
    for y in range(width + 1):
        if y % 16 == 0:
            line = Line(0, y, 576, y)
            line.set_color(Color.gray)
            add(line)
    
    # Makes the y axis.
    rect = Rectangle(3, 576)
    rect.set_position(286, 0)
    add(rect)
    
    # Makes the x axis.
    rect = Rectangle(width, 3)
    rect.set_position(0, 286)
    add(rect)
    
    
    """
    This for loop adds the numbers into each point in the graph from the
    x axis, randing from -17 to 17, effectively setting up the entire scale of the 
    graph.
    """
    for x in range(-17, 18):
        if x != 0:
            num = Text(str(x))
            num.set_position(x_coords[x] - 10, 298)
            num.set_font("6pt Arial")
            add(num)

    # This code adds the 18 to the x-axis scale
    # This is added seperately becuase the spacing in the for loop hides it.
    x_num_negative_18 = Text("-18")
    x_num_negative_18.set_position(x_coords[-18] - 5, 298)
    x_num_negative_18.set_font("6pt Arial")
    add(x_num_negative_18)
    
    # This code adds the negative 18 to the x-axis scale
    # This is added seperately becauase the spacing in the for loop hides it.
    x_pos_negative_18 = Text("18")
    x_pos_negative_18.set_position(x_coords[18] - 15, 298)
    x_pos_negative_18.set_font("6pt Arial")
    add(x_pos_negative_18)
    
    # y_axis_counter exists so that numbers are added from the top to the bottom of the graph
    y_axis_counter = 16
    for y in range(18, -18, -1):
        if y != 0:
            num = Text(str(y))
            num.set_position(290, y_axis_counter*16-250)
            y_axis_counter += 1
            num.set_font("6pt Arial")
            add(num)
        # The zero is placed with different spacing, which is the reason why it's
        # seperated
        else:
            zero = Text("0")
            zero.set_position(291, 297)
            zero.set_font("6pt Arial")
            add(zero)
            y_axis_counter += 1
            
    # This code adds the negative 18 to the y-axis scale.
    # This is added seperately becuase the spacing in the for loop hides it.
    y_num_negative_18 = Text("-18")
    y_num_negative_18.set_position(290, 574)
    y_num_negative_18.set_font("6pt Arial")
    add(y_num_negative_18)

"""
This function creates an invalid input background which 
indicates that the entered input is invalid, meaning it's not an equation. 
""" 
def invalid_input(incorrect_input):
    make_white_background()
    
    invalid_txt = Text("Invalid input!")
    invalid_txt.set_font("60pt Arial")
    invalid_txt.set_position(69,200)
    invalid_txt.set_color(Color.red)
    add(invalid_txt)
    
    error_text = Text(f"'{incorrect_input}' is not a valid input!")
    error_text.set_position(110, 245)
    error_text.set_color(Color.red)
    error_text.set_font("24pt Arial")
    add(error_text)
    
    invalid_subtext = Text("Please restart the program.")
    invalid_subtext.set_font("16pt Arial")
    invalid_subtext.set_position(150,280)
    invalid_subtext.set_color(Color.red)
    add(invalid_subtext)
 
 
# This function is used when the input is blank, it is a copy of invalid input.   
def blank_input():
    make_white_background()
    invalid_txt = Text("Invalid input!")
    invalid_txt.set_font("60pt Arial")
    invalid_txt.set_position(69,200)
    invalid_txt.set_color(Color.red)
    add(invalid_txt)
    
    invalid_subtext = Text("Please restart the program.")
    invalid_subtext.set_font("16pt Arial")
    invalid_subtext.set_position(150,280)
    invalid_subtext.set_color(Color.red)
    add(invalid_subtext)


# This function draws a white background for any time its needed 
def make_white_background():
    white_background = Rectangle(630, 630)
    white_background.set_position(0, 0)
    white_background.set_color("#FFF")
    add(white_background)


# This function checks for an invalid input.
def check_for_invalid_input(ax, bx, c):
    original_bx = bx
    original_ax = ax
    
    try:
        """
        If the c variable can't be converted to a float, 
        it means it's type: string. Strings are not vaid inputs, so an error
        page is displayed to the user
        """
        float(c)
    except Exception:
        invalid_input(c)
        add_graph_buttons(False)
             
    
    """
    If the input contains the letter x, the supposed error will be stored in the 
    bx variable. This segment checks if there is an invalid input in bx.
    """ 
    try:
        """
        First,all 'x's are eliminated, 
        Then it checks for an error becuase if any letter other than x is 
        present, it will be evaluated as an invalid input. 
        """
        bx = str(bx).replace("x", "")
        if bx == "" or bx == "-":
            return None
            # if what's left in bx is a nothing or a negative sign, the program is stoped
            # by returning None, 
        float(bx)
    except Exception:
        invalid_input(original_bx)
        add_graph_buttons(False)
        
        
    # works the same as the try-except block above but also removes the "^"
    try:
        ax = str(ax).replace("x", "")
        ax = str(ax).replace("^", "")
        if bx == "" or bx == "-":
            return None
        float(ax)
    except Exception:
        invalid_input(original_ax)
        add_graph_buttons(False)

            
"""
This function fixes the equation by adding spaces between each +, - or =, as these
are the ones that separate each term of the equation. This facilitates the separation
of the equation. 
"""
def fix_equation(equation):
    equation = list(equation)
    for i in range(len(equation)):
        if equation[i] in ["+", "-", "="]:
            equation[i] = " " + equation[i] + " "
    return "".join(equation)


"""
This function extracts the coefficients and costants from the input and assigns each one to its 
respective variable. 
"""
def extract_coefficients(ax=0, bx=0, c=0):
    ax_coefficient = ""
    bx_coefficient = ""
    c_constant = c
    
    ax = str(ax)
    bx = str(bx)
    
    if ax != 0:
        # if ax is just 'x', then it means that ax should be 1
        if ax[0] == "x":
            ax_coefficient = 1
        else:
            """For every iteration, each character in the ax variable will be 
            added to the ax_coefficient variable, if the current character is an x, then it means that
            the loop should stop iterating as it has reached the end and the ax_coefficient
            variable has been defined; however, if after the iteration, the only character
            present in the ax_coefficient variable is a negative sign, ax_coefficient should be a -1"""
            for char in ax:
                if char == "x":
                    if ax_coefficient == "-":
                        ax_coefficient = -1
                    ax_coefficient = float(ax_coefficient)
                    break
                ax_coefficient += char
    
    # The exact same thing happens here as in the code segment as above, 
    # The only difference is that this applies for the bx and bx_coefficient variables
    if bx != 0:
        if bx[0] == "x":
            bx_coefficient = 1
        else:
            for char in bx:
                if char == "x":
                    if bx_coefficient == "-":
                        bx_coefficient = -1
                    bx_coefficient = float(bx_coefficient)
                    break
                bx_coefficient += char
    
    return ax_coefficient, bx_coefficient, c_constant


"""
This function seperates each element of the equation and assigns them to their 
variables. The function also eliminates all unneseary characters
""" 
def separate_equation(equation):
    ax = 0
    bx = 0
    c = 0
    
    equation = fix_equation(equation)

    """this line separates each term and operator of the equation and adding it to a list
    everytime the loop encouters a space, thats why the fix_equation() function exist,
    it adds a space in every term so that this line can separate it
    """
    equation = [char for char in equation.split() if equation.strip() and char != ""]

    if "y" in equation:
        equation.remove("y")
    if "=" in equation:
        equation.remove("=")
        
    # in this loop, an element represents term and operators
    for i, element in enumerate(equation):
        """if the current element of the equation is a negative sign, then to the term
        a negative sign should be added to indicate that the term is negative, 
        thats done with string interpolation, then the negative sign will be removed from the list
        becuase it will no longer be needed"""
        if element == "-":
            equation[i + 1] = f"-{equation[i + 1]}"
            equation.pop(i)
        # if the current element is just a addition sign, then it will be removed because its not necesary
        if element == "+":
            equation.pop(i)
    
    # this loop iterated though every term and assigns it to its respective value varibale depending
    # on its charactes inside
    for term in equation:
        if "^" in term:
            ax = term
        elif "x" in term and "^" not in term:
            bx = term
        else:
            c = term

    check_for_invalid_input(ax, bx, c)

    ax, bx, c = extract_coefficients(ax, bx, c)
    
    return float(ax), float(bx), float(c)


# This functions graphs the equation based on the variables given.
def graph(ax, bx, c, color):
    for x in range(-1150, 1150):
        x *= 0.015625
        y_position = ax*x**2 + bx*x + c
        dot = Circle(2)
        dot.set_position(x_coords[x] - 3.4, - y_position * 16 + 286) 
        dot.set_color(color)
        add(dot)
        
        
"""
This function is made to to exctract the x-intercepts from a given input using
the quadratic formula
""" 
def quadratic_formula(a, b, c):
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return "None"
    discriminant_sqrt = math.sqrt(discriminant)
    
    root_1 = round((-b + discriminant_sqrt) / (2 * a), 2)
    root_2 = round((-b - discriminant_sqrt) / (2 * a), 2)
    """
    If root_1 and root_2 are the same, then there is only one x-intercept and 
    only one is returned as a float.
    """
    if root_1 == root_2:
        return root_1
    # If root_1 and root_2 are different, both are returned as a tuple.
    return (root_1, root_2)


"""
This function extracts the elements of the equations and returns its information
info the equation_information list. The elements returned are: y-intercept, x-intercept(s),
Domain, Range and depending if its are quadratic or not, the axis of symmetry and
the vertex
"""
def extract_elements(ax, bx, c):
    y_intercept = c
    domain = "All Real Numbers"
    
    if ax == 0 and bx != 0:
        x_intercepts = round(-c/bx, 2)
    elif bx == 0:
        x_intercepts = "None"
    else:
        x_intercepts = 0
    graph_range = "(-∞, ∞)"
    axis = None
    vertex = None
    
    if ax != 0:
        x_intercepts = quadratic_formula(ax, bx, c)

        axis = -bx/(2*ax)
        # the axis could be -0.0, in this case its turned into just 0.0
        if axis == -0.0:
            axis = 0.0
        axis = round(axis, 3)
        vertex_y = round((ax*axis**2 + bx*axis + c), 2)
        vertex = f"({axis}, {vertex_y})"
        
        if ax > 0:
            graph_range = f"[{vertex_y}, ∞)"
        elif ax < 0:
            graph_range = f"(-∞, {vertex_y}]"
            
    return (y_intercept, x_intercepts, domain, graph_range, axis, vertex)


# This function erases the stored values for the user to enter a new set of equations
# and graph it.
def restart_program():
    global current_equations, equation_information, stored_colors
    current_equations = []
    equation_information = []
    stored_colors = []
    background_start()


# This function uses a pop up to display information about the given inputs. 
def pop_up():
    width = 180*len(equation_information)
    pop_up = Rectangle(width, 170)
    pop_up.set_position(15, 50)
    pop_up.set_color("#e3e3e3")
    add(pop_up)
    

    for i, info in enumerate(equation_information):
        text_x_pos = 20+180*i
        
        if i != 0:
            line = Line(15+180*i, 55, 15+180*i, 215)
            add(line)
        
        function_num = Text(f"Function {i+1}")
        function_num.set_position(text_x_pos, 75)
        function_num.set_font("15pt Helvetica")
        function_num.set_color(colors[stored_colors[i]])
        add(function_num)
        
        
        y_int = Text(f"Y-Intercept: (0, {info[0]})")
        y_int.set_position(text_x_pos, 105)
        y_int.set_font("9pt Arial")
        add(y_int)
        
        # Checks if the element for x-intercept is an int or float, if it is
        # it means that there is only one x-intercept and there should just be
        # one pair of parenthesis.
        if isinstance(info[1], (int, float)):
            x_int = Text(f"X-Intercept: ({info[1]}, 0)")
            x_int.set_position(text_x_pos, 125)
            x_int.set_font("9pt Arial")
            add(x_int)
        # Checks if the elememnt for x-intercept is a string, if it is, then
        # no parenthesis will be placed for that text slot, just the "None" text.
        elif isinstance(info[1], str):
            x_int = Text(f"X-Intercept: {info[1]}")
            x_int.set_position(text_x_pos, 125)
            x_int.set_font("9pt Arial")
            add(x_int)
        # If neither a number or string is in the slot for x-intercept, then
        # it must be a tuple, and two sets of parenthesis are added to indicate
        # that there are two x-intercepts.
        else:
            x_int = Text(f"X-Intercept(s): ({info[1][0]}, 0) & ({info[1][1]}, 0)")
            x_int.set_position(text_x_pos, 125)
            x_int.set_font("8pt Arial")
            add(x_int)
        
        # This code adds the domain. The domain will always be All Real Numbers.
        domain = Text(f'Domain: {info[2]}')
        domain.set_position(text_x_pos, 145)
        domain.set_font("9pt Arial")
        add(domain)
        
        # If any range that is not "(-∞, ∞)" is returned by the extract_elements 
        # function, then it means that the function is a quadratic, and the
        # axis of symmetry and the vertex should be displayed
        if info[3] != "(-∞, ∞)":
            # displays the range into the pop-up screen
            equation_range = Text(f"Range: {info[3]}")
            equation_range.set_position(text_x_pos, 165)
            equation_range.set_font("9pt Arial")
            add(equation_range)
            
            # Displays the axis of symmetry into the pop-up screen
            axis = Text(f"Axis of Symmetry: x = {info[4]}")
            axis.set_position(text_x_pos, 185)
            axis.set_font("9pt Arial")
            add(axis)
            
            # Displays the vertex into the pop-up screen
            vertex = Text(f"Vertex: {info[5]}")
            vertex.set_position(text_x_pos, 205)
            vertex.set_font("9pt Arial")
            add(vertex)
        # If the range returned is "(-∞, ∞)", than the function is linear
        # and the range displayed will be "(-∞, ∞)""
        else:
            equation_range = Text(f"Range: {info[3]}")
            equation_range.set_position(text_x_pos, 165)
            equation_range.set_font("9pt Arial")
            add(equation_range)
            

"""
This function adds the image of the start screen. It was made using 
Canva, and resized using FireAlpaca. 
"""
def background_start():
    START = "https://codehs.com/uploads/dc6c1816865f1a580fa59eb06d9da6a0"
    START_WIDTH = width
    START_HEIGHT = height 
    image = Image(START)
    image.set_position(0, 0)
    image.set_size(START_WIDTH, START_HEIGHT)
    add(image)


"""
This function adds the image of the tutorial page. It was made using 
Canva, and resized using FireAlpaca. 
"""
def tutorial_page():
    TUTORIAL = "https://codehs.com/uploads/c1024f4a84ff240380298a3de10684d5"
    TUTORIAL_WIDTH = width 
    TUTORIAL_HEIGHT = height 
    image = Image(TUTORIAL)
    image.set_position(0, 0)
    image.set_size(TUTORIAL_WIDTH, TUTORIAL_HEIGHT)
    add(image)


"""
This function adds the image to select how many equations will be graphed. 
It was made using Canva, and resized using FireAlpaca. 
"""
def amount_equations():
    AMOUNT = "https://codehs.com/uploads/4a25b6f218455f0ac40c8176c9e68713"
    AMOUNT_WIDTH = width
    AMOUNT_HEIGHT = height 
    image = Image(AMOUNT)
    image.set_position(0,0)
    image.set_size(AMOUNT_WIDTH, AMOUNT_HEIGHT) 
    add(image)


"""
This function create the "Get Info" and "Restart" button when the graph is displayed. 
If it is an invalid input, the "Get Info" button it isn't displayed. 
""" 
def add_graph_buttons(allow_show_info_button):
    global can_click_for_info
    button_texts = ["Get Info", "Restart"]
    
    button_area = Rectangle(576, 54)
    button_area.set_position(0, 576)
    button_area.set_color(Color.white)
    add(button_area)
    
    if allow_show_info_button:
        for i in range(2):
            button = Rectangle(110, 45)
            button.set_position(20+130*i, 580)
            button.set_color(colors[2+i])
            add(button)
        
            txt = Text(button_texts[i])
            txt.set_position(30+135*i, 610)
            txt.set_font("18pt Arial")
            add(txt)
    else:
        can_click_for_info = False
        
        restart_button = Rectangle(110, 45)
        restart_button.set_position(150, 580)
        restart_button.set_color(Color.green)
        add(restart_button)
    
        restart_txt = Text("Restart")
        restart_txt.set_position(165, 610)
        restart_txt.set_font("18pt Arial")
        add(restart_txt)

"""
This function assigns parameters to where and when buttons are functional 
to run the program. 
"""
def button_logic(x, y):
    global can_click_tutorial, can_click_back_from_tutorial, can_click_to_start 
    global can_click_amount, can_click_1, can_click_2, can_click_3 
    global can_click_restart, can_click_for_info, pop_up_times_clicked
    
    """
    Start button becomes functional once program is ran, every other button
    is false
    """
    if 140 < x < 420 and 433 < y < 483 and can_click_to_start:
        amount_equations() 
        can_click_to_start = False
        can_click_tutorial = False
        can_click_back_from_tutorial = False 
        can_click_amount = True 
        can_click_for_info = True
        can_click_restart = True

    # Tutorial page is accessed, every other button becomes false. 
    elif 140 < x < 420 and 508 < y < 578 and can_click_tutorial:
        tutorial_page()
        can_click_to_start = False
        can_click_tutorial = False
        can_click_back_from_tutorial = True
    
    # Back button to start screen is accessed, every other button is false.
    elif 200 < x < 400 and 525 < y < 590 and can_click_back_from_tutorial:
        background_start()
        can_click_to_start = True
        can_click_tutorial = True
        can_click_back_from_tutorial = False
    
    # User clicks 1, meaning every other button is false. 
    elif 40 < x < 190 and 270 < y < 430 and can_click_amount:
        can_click_amount = False
        can_click_1 = True 
        can_click_2 = False
        can_click_3 = False
        on_start()
    
    # User clicks 2, meaning every other button is false. 
    elif 215 < x < 365 and 270 < y < 430 and can_click_amount:
        can_click_amount = False
        can_click_1 = False 
        can_click_2 = True 
        can_click_3 = False
        on_start()
    
    # User clicks 3, meaning every other button is false.     
    elif 400 < x < 550 and 270 < y < 430 and can_click_amount:
        can_click_amount = False
        can_click_1 = False 
        can_click_2 = False 
        can_click_3 = True 
        on_start()

    # User clicks the get info button, meaning the pop_up function is enabled
    elif 20 < x < 130 and 580 < y < 625 and can_click_for_info:
        pop_up_times_clicked += 1
        if pop_up_times_clicked % 2 == 1:
            pop_up()
        else:
            make_white_background()
            set_up_graph()
            graph_current_equations()


    # Restart button can be accessed, meaning every other button is false. 
    elif 150 < x < 260 and 580 < y < 625 and can_click_restart:
        restart_program()
        can_click_to_start = True
        can_click_tutorial = True
        can_click_back_from_tutorial = False 
  
        
# This function calls the graph() function for every equation entered.
def graph_current_equations():
    for equation in current_equations:
        graph(equation[0], equation[1], equation[2], colors[equation[3]])
    add_graph_buttons(True)
        

# This function set's up the graph and gets the input from the user.
def on_start():
    make_white_background()
    set_up_graph()
    count_number = 0 
    if can_click_1:
        count_number = 1
    
    elif can_click_2:
        count_number = 2 
        
    elif can_click_3:
        count_number = 3
    # This loop asks the user for the equation they will add.    
    for i in range(count_number):
        color_index = 0 
        equation = input(f"""Enter equation number {i+1} in:
                Quadratic Standard form: y = ax^2 + bx + c 
                or in
                Linear Slope-intercept form: y = mx + b 
                
NOTE: Fractions are not supported! Use decimals instead.""")
        # If the equation is empty, it is considered an invalid input.
        if equation == "":
            blank_input()
            add_graph_buttons(False)
            # this return exist so that nothing more is executed after the invaid input screen
            return None
        # This while loop asks the user the color of their graph.
        while True:
            color_index = input("""Choose the index for the color of your graph!:
            1: Red
            2: Blue
            3: Green
            """)
            
            # This if loop evaluates if the index is less than 0 or more than 4.
            if color_index.isdigit() and 0 < int(color_index) < 4:
                color_index = int(color_index)
                stored_colors.append(color_index)
                break
        
        ax, bx, c = separate_equation(equation)
        current_equations.append((ax, bx, c, color_index))
        equation_information.append(extract_elements(ax, bx, c))
    graph_current_equations()
    
    
# These functions enables the program to start. 
background_start()
add_mouse_click_handler(button_logic)
