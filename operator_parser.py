from tabulate import tabulate
import numpy as np
from tabulate import tabulate

def getOperators(grammar):
    operators = []
    operators.append("#")
    for key in grammar:
        for production in grammar[key]:
            for char in production:
                if char in "+-*/&|!^%@()":
                    operators.append(char)
    for key in grammar:
        for production in grammar[key]:
            if production.islower():
                operators.append(production)
    return operators

def getPrecedence(operators):
    precedence = {}
    for i, operator in enumerate(operators):
        precedence[operator] = i
    return precedence

def PrecedenceTable(precedence):
    table = []
    headers = [""] + list(precedence.keys())
    table.append(headers)
    for key in precedence:
        row = [key]
        for key2 in precedence:
            
            if precedence[key] > precedence[key2]:
                row.append(">")
            elif precedence[key] < precedence[key2]:
                row.append("<")
            else:
                if precedence[key] == 0:
                    row.append("A")
                elif precedence[key] == len(precedence) - 1:
                    row.append("=")
                else:
                    row.append(">")
        table.append(row)
    return table


def checkString(string, grammar, precedence):
    table = []
    stack = []
    stack.append("#")
    stack.append(string[0])

    headers = ["stack", "input", "action"]
    table.append(headers)
    string = list(string)
    string.append("#")
    string.reverse()

    while len(string) > 0:
        stack_str = ""
        for i in stack:
            stack_str += i
        input_str = ""
        for i in string:
            input_str += i
        if stack[-1] in precedence and string[-1] in precedence:
            if precedence[stack[-1]] < precedence[string[-1]]:
                stack.append(string.pop())
                action = "Shift"
            elif precedence[stack[-1]] > precedence[string[-1]]:
                stack.pop()
                action = "Reduce"
            else:
                stack.pop()
                string.pop()
                action = "Reduce"
        else:
            stack.append(string.pop())
            action = "Shift"
        table.append([stack_str, input_str, action])
    
    if len(stack) == 0 and len(string) == 0:
        table.append(["-", "-", "String Accepted"])
    else:
        table.append(["-", "-", "String Rejected"])
    return table

def main():
    print("To input epsilion enter #")
    no_of_productions = int(input("Enter the no of productions: "))
    grammar = {}
    for _ in range(no_of_productions):
        non_terminal = input("Enter Non terminal: ")
        production = input(f"Enter production of {non_terminal}: ")
        grammar[non_terminal] = production.split("|")
        grammar[non_terminal] = [production.replace(" ", "") for production in grammar[non_terminal]]

    print("\nThis is the input grammar::")
    print(grammar)
    print("")
    
    operators = getOperators(grammar)
    precedence = getPrecedence(operators)
    
    print(operators)
    print(precedence)
    table = PrecedenceTable(precedence)
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    string = input("Enter the string to check: ")
    table = checkString(string, grammar, precedence)
    print(tabulate(table, headers="firstrow", tablefmt="grid"))


if __name__ == "__main__":
    main()