import sympy


class Stack:
    ''' Class of stack
    methods:
      __init__ - constructor of this class
      push - method which add item on top of stack
      pop - method which remove item from top of stack
    '''
    def __init__(self):
        ''' constructor of this class it prepare stack as empty list
        return: Stack Class Object
        '''
        self.stack = []

    def push(self, item):
        ''' function which add item on top of stack
        arguments:
          item - item to put on stack
        return: None
        '''
        self.stack.append(item)

    def pop(self):
        ''' function which remove item from top of stack
        return: 'item from top of stack'
        '''
        return self.stack.pop()


class BinaryTree:
    ''' Class of binary tree
    methods:
      __init__ - constructor of this class
      insert_left - method which add left child for node
      insert_right - method which add right child for node
      set_root_val - method which set value of node
      get_root_val - method which check value of node
      get_right_child - method which check right child
      get_left_child - method which check left child
    '''
    def __init__(self, root):
        ''' constructor of this class it prepare root node of tree
        arguments:
          root - value for root node
        return: BinaryTree Class Object
        '''
        self.right_child = None
        self.left_child = None
        self.key = root

    def insert_left(self, new_node):
        ''' function which add left child for node
        arguments:
          new_node - added left child to parent node
        return: None
        '''
        if self.left_child is None:
            self.left_child = BinaryTree(new_node)

        else:
            temp = BinaryTree(new_node)
            temp.left_child = self.left_child
            self.left_child = temp

    def insert_right(self, new_node):
        ''' function which add right child for node
        arguments:
          new_node - added right child to parent node
        return: None
        '''
        if self.right_child is None:
            self.right_child = BinaryTree(new_node)

        else:
            temp = BinaryTree(new_node)
            temp.right_child = self.right_child
            self.right_child = temp

    def set_root_val(self, key):
        ''' function which set value of node
        arguments:
          obj - value added to node
        return: None
        '''
        self.key = key

    def get_root_val(self):
        ''' function which check value of node
        return: 'value of node'
        '''
        return self.key

    def get_right_child(self):
        ''' function which check right child
        return: 'right child'
        '''
        return self.right_child

    def get_left_child(self):
        ''' function which check left child
        return: 'left child'
        '''
        return self.left_child


def parse_tree(function):
    ''' function which create tree of mathematical expressions
    arguments:
      function - mathematical expression to represent as tree
    return: 'tree representation of function'
    '''
    if type(function) != str:
        raise TypeError('function must be string.')

    al_tokens = ['+', '-', '*', '/', '**', ')', 'sin(', 'cos(', 'log(', 'exp(']
    tokens = function.split()
    tree = BinaryTree('')
    stack = Stack()

    stack.push(tree)
    for token in tokens:
        if token == '(':
            tree.insert_left('')
            stack.push(tree)
            tree = tree.get_left_child()

        elif token not in al_tokens:
            if len(token) == 1 and token.isalpha():
                tree.set_root_val(sympy.Symbol(token))

            else:
                tree.set_root_val(int(token))

            parent = stack.pop()
            tree = parent

        elif token in ['+', '-', '*', '/', '**']:
            tree.set_root_val(token)
            tree.insert_right('')
            stack.push(tree)
            tree = tree.get_right_child()

        elif token in ['sin(', 'cos(', 'log(', 'exp(']:
            tree.set_root_val(token)
            tree.insert_right('')
            stack.push(tree)
            tree = tree.get_right_child()

        elif token == ')':
            tree = stack.pop()

        else:
            raise ValueError('Wrong token')

    return tree


def evaluate(parse_tree):
    right = parse_tree.get_right_child()
    left = parse_tree.get_left_child()

    if left or right:
        operator = parse_tree.get_root_val()

        if operator == '+':
            return evaluate(left) + evaluate(right)

        elif operator == '-':
            return evaluate(left) - evaluate(right)

        elif operator == '*':
            return evaluate(left) * evaluate(right)

        elif operator == '/':
            return evaluate(left) / evaluate(right)

        elif operator == '**':
            return evaluate(left) ** evaluate(right)

        elif operator == 'sin(':
            return sympy.sin(evaluate(right))

        elif operator == 'cos(':
            return sympy.cos(evaluate(right))

        elif operator == 'log(':
            return sympy.ln(evaluate(right))

        elif operator == 'exp(':
            return sympy.Symbol('e') ** evaluate(right)

    else:
        return parse_tree.get_root_val()


def derivative(parse_tree, variable='x'):
    right = parse_tree.get_right_child()
    left = parse_tree.get_left_child()

    if left or right:
        operator = parse_tree.get_root_val()

        if operator == '+':
            return derivative(left, variable) + derivative(right, variable)

        elif operator == '-':
            return derivative(left, variable) - derivative(right, variable)

        elif operator == '*':
            return (derivative(left, variable)*evaluate(right)
                    + evaluate(left)*derivative(right, variable))

        elif operator == '/':
            return ((derivative(left, variable)*evaluate(right) -
                      evaluate(left)*derivative(right, variable))
                      /evaluate(right)**2)

        elif operator == '**':
            r = right.get_root_val()
            l = left.get_root_val()

            de_r = derivative(right, variable)
            de_l = derivative(left, variable)
            ev_r = evaluate(right)
            ev_l = evaluate(left)

            if type(l) == int or type(l) == float:
                if type(r) == int:
                    return 0
                else:
                    return de_r*sympy.ln(l) * l**ev_r

            elif type(r) == int or type(r) == float:
                return ev_r*de_l * ev_l**(ev_r - 1)

            else:
                return ev_l**ev_r * (de_r*sympy.ln(ev_l) + (ev_r*de_l) / ev_l)

        elif operator == 'sin(':
            return derivative(right, variable) * sympy.cos(evaluate(right))

        elif operator == 'cos(':
            return -derivative(right, variable) * sympy.sin(evaluate(right))

        elif operator == 'log(':
            return derivative(right, variable) * 1/evaluate(right)

        elif operator == 'exp(':
            return (derivative(right, variable)
                    *sympy.Symbol('e')**evaluate(right))

    else:
        if parse_tree.get_root_val() == sympy.Symbol(variable):
            return 1
        else:
            return 0


if __name__ == '__main__':
    list_of_functions = [
        ('( x + 1 )', 'x'),
        ('( 5 - x )', 'x'),
        ('( ( x - 3 ) + ( x + 1 ) )', 'y'),
        ('( ( x * y ) + y )', 'y'),
        ('( x * x )', 'x'),
        ('( x / ( z + 1 ) )', 'z'),
        ('sin( ( ( 5 * x ) - y ) )', 'x'),
        ('cos( sin( ( 1 / x ) ) )', 'x'),
        ('exp( ( ( x ** 2 ) * 3 ) )', 'x'),
        ('( log( log( y ) ) * ( 1 / x ) )', 'y'),
        ('( ( 3 ** y ) * ( 2 ** x ) )', 'x'),
        ('( 5 ** sin( ( x / 3 ) ) )', 'x'),
        ('( ( sin( x ) ** 3 ) ** 2 )', 'x'),
        ('( sin( x ) ** sin( x ) )', 'x'),
        ('( ( x ** x ) ** x )', 'x')
    ]

    for function in list_of_functions:
        print(function[0].replace(' ', '') + "'" + function[1] + ': ',
          sympy.simplify(derivative(parse_tree(function[0]), function[1])))

    print('')
    print(sympy.simplify(derivative(parse_tree('x'), 'x')))
