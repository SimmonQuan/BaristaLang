import sys
import webbrowser
import pyfiglet
import random

varMap = {} #dictionary to store variables

def menu_request():
    print("No problem! I will open the menu for you now.")
    webbrowser.open("https://www.dunkindonuts.com/en/menu")

def orange_drink_request():
    print("We don't sell orangeDrink silly! Are you Jennifer Lopez?")
    webbrowser.open("https://youtube.com/shorts/zCgWWNIIZHA?si=oMep27rNwdw0_jM9")

emoji_dictionary = {
    "coffee": '☕',
    "matcha": '🍵',
    "orangeDrink": '🍊🥤',
    "donut": '🍩'
}

def display_latte_art(word):
    art = pyfiglet.figlet_format(word)
    print(art)

def print_identifier(line):
    line = line.strip() #remove white space
    if line.startswith("Does your cafe sell any fizzy drinks?"): #syntax that indicates fizzbuzz
        print("well yes we do!, have some fizzbuzz!")
        for i in range(1, 51):
            if i % 3 == 0 and i % 5 == 0: #fizzbuzz
                print("FizzBuzz")
            elif i % 3 == 0:
                print("Fizz")
            elif i % 5 == 0:
                print("Buzz")
            else:
                print(i)

    if line.startswith("If") and "is not in stock, can I get" in line: #syntax that indicates If statement
        currLine = line[3:].strip().rstrip("?")
        fragments = currLine.split(" is not in stock, can I get ")
        out_of_stock = fragments[0].strip() #isolates the menu items inputted by user
        alternate_drink = fragments[1].strip() 
        random_number = random.randint(1, 10) #generates random number between 1-10.
        current_stock = 5
        if random_number < current_stock: #If the random number is < current_stock the cafe is out of stock for that item
            print(f"Sorry! We are currently out of {out_of_stock} but I can get you {alternate_drink}")
        else:
            print(f"Luckily we have {out_of_stock} in stock, here you go!")

    elif line.startswith("Can you show me latte art of my name"): #syntax that indicates ascii art 
        customerName = line.split()[-1].strip('?') 
        display_latte_art(customerName) #prints the desired word in ascii as "latte art"

    elif line.startswith("Can I take a look at your menu?"): #syntax to open menu in default web browser
        menu_request()
    
    elif "orangeDrink" in line: #syntax to open Youtube video of JLO in default web browser
        orange_drink_request()

    elif line.startswith("I would like to order("): #syntax to print
        _, call = line.split("I would like to order(")
        val = call[:-1].strip()
        if val.startswith('"'): 
            mystr = val.split('"')[1]
            print(mystr) #print string
        else:
            value = eval_expr(val)
            print(value) #print if single value

    elif "=" in line:
        var, expr = line.split("=")
        var = var.strip() #remove white space
        expr = expr.strip()
        varMap[var] = eval_expr(expr) #add to varMap
    else:
        pass
    
def parenthesis_simplifier(expr):
     #handle parenthesis for order of operations
    while '(' in expr and ')' in expr: 
        beginning = expr.rfind('(')
        end = expr.find(')', beginning)
        #find parenthesis within expr, solve equation
        inner_result = eval_expr(expr[beginning + 1:end])
        #add the ()'s result back in, replacing original equation
        expr = expr[:beginning] + str(inner_result) + expr[end + 1:]
    return expr

def eval_expr(expr): #mathematical parsing
    expr = expr.strip() #remove white space
    if expr.isdigit():
        return int(expr)
    if expr in varMap:
        return varMap[expr] #if variable is already assigned a value, return the value
    
    try: 
        expr = parenthesis_simplifier(expr)
        opera_tracker = [] #create list to track operands and operations
        num = ""
        for char in expr:
            if char in {"+", "-", "*", "/", "%"}: #outlines legal operations
                if num:
                    opera_tracker.append(num)
                opera_tracker.append(char)
                num = "" #reset
            else:
                num = num + char
        if num:
            opera_tracker.append(num)

        if len(opera_tracker) == 1:
            return eval(opera_tracker[0]) #returns if its a single integer

        solution = eval_math(opera_tracker)
        return solution #output
    except Exception as e:
        raise Exception(f"That is against our corporate policy, my apologies. variable not defined: {expr}")

def eval_math(opera_tracker): #evaluates actual mathematics
    i = 0
    while i < len(opera_tracker):
        if opera_tracker[i] in {"*", "/", "%"}: #for multiplication, division, modulo
            operator = opera_tracker[i] #before add/subtract in order of operations but after ().
            left = opera_tracker[i-1]
            right = opera_tracker[i+1]
            left_value = eval_expr(left) #examines the values to the left and right of operands
            right_value = eval_expr(right)

            if operator == "*":
                result = left_value*right_value #multiply
            elif operator == "/":
                if right_value == 0:
                    raise Exception("That is against our corporate policy, my apologies. error: Dividing by 0 is not allowed")
                result = left_value/right_value #divide
            elif operator == "%":
                if right_value == 0:
                    raise Exception("That is against our corporate policy, my apologies. error: Modulo by 0 is not allowed")
                result = left_value%right_value #modulo

            opera_tracker[i-1:i+2] = [str(result)] #add math results to the list

            i = 0 #restart looping because minimizing parts of equations changes the indexes
        else:
            i = i + 1

    solution = eval_expr(opera_tracker[0])
    i = 1
    while i < len(opera_tracker):
        if opera_tracker[i] in {"+", "-"}: #addition/subtraction
            operator = opera_tracker[i]
            right_value = eval_expr(opera_tracker[i+1])
            if operator == "+":
                solution = solution + right_value #add value from the right
            elif operator == "-":
                solution = solution - right_value #subtract value from the right
        i = i + 2
    return solution

def main():
    file_path = "C:\\Users\\Simmon\\Downloads\\complexProgram.brsta" #replace with file path ending in .brsta
    try:
        with open(file_path) as file: #open file
            lines = file.readlines()
            for line in lines: #read through every line in the file
                try:
                    print_identifier(line) #call print_identifier
                except Exception as e:
                    print(f"error: {e}")
    except FileNotFoundError:
        print(f"error: file '{file_path}' not found") #error checking

    if varMap:
        print("\n---- Receipt ----")
        for key, value in varMap.items(): #prints every variable used by looking through the varMap to print a receipt
            emoji = emoji_dictionary.get(key, "😊")
            print(f"{emoji} {key}: {value}")   #receipt also adds emojis based on emoji dictionary
        print(" ---- Thank you for ordering with us!!! ----")

if __name__ == "__main__":
    main()




    