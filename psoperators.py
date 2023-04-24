# Isaac Dahle
# Colaborators: Vishal


from typing import Dict
from colors import *
from psexpressions import StringValue, DictionaryValue, CodeArrayValue, Value

class PSOperators:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.scope = scoperule

        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    """
        Helper function. Finds the static link given a variable name.
    """
    def staticLink(self, name, index):
        if name[0] != '/':
            name = '/' + name
        dic = self.dictstack[index][1]
        if name in dic:
            return index
        elif index == 0:
            print("staticLink")
            raise KeyError 
        else:
            return self.staticLink(name, self.dictstack[index][0])

    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """
    def dictPop(self) -> tuple[int, dict]:
        try:
            x = self.dictstack[len(self.dictstack) - 1]
            self.dictstack.pop(len(self.dictstack) -1)
            return x
        except:
            raise IndexError


    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,t :tuple ):
        if isinstance(t, tuple):
            self.dictstack.append(t)
        else:
            print("dictPush")
            raise ValueError

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self,name, value):
        # if the stack is empty add an empty dict to it
        if len(self.dictstack) == 0:
            newDict = {}
            index = 0
            tup = (index, newDict)
            self.dictPush(tup)
        # add/update the name:value pair
        tup = self.dictPop()
        tup[1][name] = value
        self.dictPush(tup)

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):


        # get the last index
        index = len(self.dictstack) - 1

        while(True):
            if (name[0] != '/'):
                name = '/' + name
            # get the current dictionary
            dic = self.dictstack[index][1]

            # at end of stack
            if index == 0:
                if name in dic:
                    return dic[name]
                else:
                    print("error in lookup: item not found")
                    return None

            elif name in dic:
                return dic[name]
            
            # update index 
            if self.scope == "dynamic":
                index -= 1
            else:
                index = self.dictstack[index][0]


    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 - op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 * op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 % op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of the StringValue objects;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 == op2)
            elif (isinstance(op1, StringValue) and isinstance(op2, StringValue)):
                self.opPush(op1.value == op2.value)
            elif (isinstance(op1, DictionaryValue) and isinstance(op2, DictionaryValue)):
                self.opPush(op1 == op2)
                # flag = True
                # for (key, value) in op1.value.items():
                #     for (key2, value2) in op2.value.items():
                #         if key != key2 or value != value2:
                #             flag = False
                # self.opPush(flag)
            else:
                print("Error: the values are not comparable")
                self.opPush(False)
        else:
            print("Error: add expects 2 operands")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 > op2)
            elif (isinstance(op1, StringValue) and isinstance(op2, StringValue)):
                self.opPush(op1.value > op2.value)
            elif (isinstance(op1, DictionaryValue) and isinstance(op2, DictionaryValue)):
                self.opPush(op1.value > op2.value)
                # flag = True
                # for (key, value) in op1.value.items():
                #     for (key2, value2) in op2.value.items():
                #         if key != key2 or value != value2:
                #             flag = False
                # self.opPush(flag)
            else:
                print("Error: the values are not comparable")
                self.opPush(False)
        else:
            print("Error: add expects 2 operands")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values.
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 < op2)
            elif (isinstance(op1, StringValue) and isinstance(op2, StringValue)):
                self.opPush(op1.value < op2.value)
            elif (isinstance(op1, DictionaryValue) and isinstance(op2, DictionaryValue)):
                self.opPush(op1.value < op2.value)
                # flag = True
                # for (key, value) in op1.value.items():
                #     for (key2, value2) in op2.value.items():
                #         if key != key2 or value != value2:
                #             flag = False
                # self.opPush(flag)
            else:
                print("Error: the values are not comparable")
                self.opPush(False)
        else:
            print("Error: add expects 2 operands")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value.
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print(OKGREEN+"===**opstack**===")
        for item in reversed(self.opstack):
            print(item)
        print(""+CEND)
        print(RED+"===**dictstack**===")
        count = len(self.dictstack)-1
        for tup in reversed(self.dictstack):
            print("----num:", count,"----link:",tup[0],"----")
            for name in tup[1]:
                print(name,": ", tup[1][name])
            count -= 1
        print("=========="+ CEND)


    """
       Copies the top element in opstack.
    """
    def dup(self):
        item = self.opPop()
        self.opPush(item)
        self.opPush(item)

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        number = self.opPop()
        lst = list()
        if isinstance(number, int):
            # loop over the opstack backwards and add it to lst 
            for i in range(number):
                lst.append(self.opstack[len(self.opstack) - 1 - i])
            # push items onto the stack
            for item in reversed(lst):
                self.opPush(item)
        else:
            print("Error: copy argument is not integer")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        self.opstack.clear() 
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        item1 = self.opPop()
        item2 = self.opPop()

        self.opPush(item1)
        self.opPush(item2)

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        number = self.opPop()
        string = '('
        for i in range(number):
            string += '\0'
        string += ')'
        stringVal = StringValue(string)
        self.opPush(stringVal)
    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        self.opPop()
        self.opPush(DictionaryValue({}))

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictionaryValue and StringValue values.
    """
    def length(self):
        item = self.opPop()
        if isinstance(item, StringValue) :
            # subtract 2 to account for ()
            self.opPush(len(item.value) - 2)
        elif isinstance(item, DictionaryValue):
            count = 0
            # count the number of keys
            for key in item.value.keys():
                count +=1

            self.opPush(count) 
        else:
            raise TypeError

    """ Pops either:
         -  "A (zero-based) index and an StringValue value" from opstack OR 
         -  "A `name` (i.e., a key) and DictionaryValue value" from opstack.  
        If the argument is a StringValue, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictionaryValue, gets the value for the given `name` from DictionaryValue's dictionary value and pushes it onto the opstack
    """
    def get(self):
        val1 = self.opPop()
        val2 = self.opPop()
        # is a stringVAlue 
        if isinstance(val2, StringValue):
            pos = val1
            string = val2.value[1:-1]
            try: 
                self.opPush(ord(string[pos]))
            except:
                raise IndexError
        # is a dictionaryVAlue
        elif isinstance(val2, DictionaryValue):
            name = val1
            try:
                value = val2.value[name]
                self.opPush(value)
            except:
                raise LookupError
        else:
            raise TypeError
   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StringValue value from  opstack", OR
    - "An `item`, a `name`, and a DictionaryValue value from  opstack". 
    If the argument is a StringValue, replaces the character at `index` of the StringValue's string with the character having the ASCII value of `item`.
    If the argument is an DictionaryValue, adds (or updates) "name:item" in DictionaryValue's dictionary `value`.
    """
    def put(self):
        item = self.opPop()
        location = self.opPop()
        structure = self.opPop()

        if isinstance(structure, StringValue) and isinstance(item,int) and isinstance(location, int):
            # remove ()
            string = structure.value[1:-1]
            # get the character
            char = chr(item)
            # insert the character
            string = string[:location] + char + string[location + 1:]
            # update the StringValue
            structure.value = '(' + string + ')'
        elif isinstance(structure, DictionaryValue):
            # update the dictionary value
            structure.value[location] = item
        else:
            raise TypeError
    """
    getinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a `count`, a (zero-based) `index`, and an StringValue value from  opstack, and 
    extracts a substring of length count from the `value` of StringValue starting from `index`,
    pushes the substring back to opstack as a StringValue value. 
    """ 
    def getinterval(self):
        count = self.opPop()
        index = self.opPop()
        strVal = self.opPop()
        if isinstance(strVal, StringValue) and isinstance(count,int) and isinstance(index,int):
            try:
                # get the designated interval
                string = strVal.value[index + 1: index + count + 1]
            except:
                raise IndexError
            else:
                # prep string to be pushed back on the stack
                string = '(' + string + ')'
                self.opPush(StringValue(string))
        else:
            raise TypeError

    """
    putinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a StringValue value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StringValue's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        substring = self.opPop()
        index = self.opPop()
        strVal = self.opPop()
        if isinstance(strVal, StringValue) and isinstance(substring,StringValue) and isinstance(index,int):
            try:
                string = strVal.value
                # remove the ()
                substring = substring.value[1:-1]
                # put the substring in the designated interval
                string = string[:index + 1] + substring + string[index + len(substring) +1:] 
                strVal.value = string
            except:
                raise IndexError
        else:
            raise TypeError

    """
    search is a string only operator, i.e., works only with StringValue values. 
    Pops two StringValue values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StringValue values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        delimiter = self.opPop()
        inputstr = self.opPop()
        if isinstance(delimiter, StringValue) and isinstance(inputstr, StringValue):
            # remove ()
            delim = delimiter.value[1:-1]
            inpt = inputstr.value[1:-1]
            # split the string
            words = inpt.split(delim)
            # if the delimiter is not present
            if len(words) == 1:
                self.opPush(inputstr)
                self.opPush(False)
            #if the delimiter is present
            else:
                # split the string at the first occurence
                firsthalf = words[0]
                words.remove(firsthalf)
                secondhalf = ""
                for word in words:
                    if not word is words[-1]:
                        secondhalf += word + delim
                    else:
                        secondhalf += word
                # prepare to push results to opstack
                firsthalf = '(' + firsthalf + ')'
                secondhalf = '(' + secondhalf + ')'
                #push to opstack
                self.opPush(StringValue(secondhalf))
                self.opPush(delimiter)
                self.opPush(StringValue(firsthalf))
                self.opPush(True)
        else:
            raise TypeError

    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictionaryValue value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        dic = self.opPop()
        if isinstance(dic, DictionaryValue):
            self.dictPush(dic.value)
        else:
            raise TypeError

    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        self.dictPop()

    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        value = self.opPop()
        name = self.opPop()
        # check to see if there is a dictionary on the opstack
        if len(self.dictstack) > 0:
            d = self.dictPop()[1]
        else:
            d = {}
        d[name] = value
        self.dictPush((0,d))


    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a CodeArrayValue object and a boolean value, if the value is True, executes (applies) the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        block = self.opPop()
        boolen = self.opPop()
        if isinstance(boolen, bool) and isinstance(block, CodeArrayValue):
            if boolen:
                block.apply(self)
        else:
            print("psIf")
            raise ValueError 

    """ ifelse operator
        Pops two CodeArrayValue objects and a boolean value, if the value is True, executes (applies) the bottom CodeArrayValue otherwise executes the top CodeArrayValue.
        Will be completed in part-2. 
    """
    def psIfelse(self):
        else_block= self.opPop()
        if_block = self.opPop()
        boolen = self.opPop()

        if isinstance(boolen, bool) and isinstance(else_block, CodeArrayValue) and isinstance(if_block, CodeArrayValue):
            if boolen:
                if_block.apply(self)
            else:
                else_block.apply(self)
        else:
            print("psIfElse")
            raise ValueError
        



    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a CodeArrayValue object, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the CodeArrayValue. 
       Will be completed in part-2. 
    """ 
    #TODO: make this work
    def psFor(self):
        code_array = self.opPop() 
        end_index = self.opPop() 
        increment = self.opPop() 
        begin_index = self.opPop() 
        if isinstance(end_index, int) and isinstance(increment,int) and isinstance(begin_index, int) and isinstance(code_array, CodeArrayValue):
            current_index = begin_index
            while(True):
                self.opPush(current_index)
                index = self.staticLink("for", len(self.dictstack)-1)
                code_array.apply(self, index)
                current_index += increment
                if(current_index == end_index):
                    self.opPush(current_index)
                    code_array.apply(self, index)
                    break


        else:
            print("psFor")
            raise ValueError

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

