# Python Basics
Reference source file: `BasicPython.py`

## Python Basics Introduction
In Python, there are two primary ways you interact with the Python interpreter. In *interactive* mode, you run the Python program. For example, in Linux you might type `python3` to start the Python interpreter. If `python3` does not exist, it may be called `python` on your computer. On some operating systems, `python` may run an older version of python, so it's best to try `python3` first, as all the examples in this tutorial assume you are using Python 3 or later. Note that when you run python interactively, it will print out the version number (such as Python 3.9.7). Interactive mode is useful because you will immediately see the result of each line of Python code as you type it. However, when dealing with large or complex or multithreaded programs it can be difficult to work in interactive mode.

You can also run Python in *non-interactive* mode. This is typically done by providing a text file containing the Python program to run to the Python interpreted. For example, if you have Python code in a file called `test.py`, you would run it in non-interactive mode on most Linux systems by typing `python3 test.py`.

It is recommended that you execute the examples below in interactive mode, although the file `BasicPython.py` is provided, should you wish to run the code examples in non-interactive mode.

In the below code, the code you should type into the Python interpreter will be shown like this:
```python
print('This is an example of an entire line you would type in the Python interpreter, including the word print at the beginning and the parenthesis at the end')
```

and, if shown, the expected result will be shown like this:

Output:
```
This is the output you are expected to see, (although not what the above python command would do, this is just an example).
```

With that, let's get started using Python!

## Printing Text
The `print` function is used to output text to the console. For example, the line `print('Hello, world')` will output the string `'Hello, world'`. In this line, the command `print` is what is called a *function* and the text in parenthesis afterwards is called an *argument* or a *parameter* to the function (both words are used, but mean the same thing).  A function calls some other pieces of code to do something, in this case, to print whatever is specified as the argument to `print`. In Python (and C), one or more arguments are specified in parenthesis after the name of the function. This process is called *calling the function* `print`. The argument(s) specified in parenthesis are said to be *passed to the function* `print`.

We can print almost anything we want using the `print` command. You can `print('I am learning Python')` or whatever you want. Note that you **must** enclose your text in quotes. The text is quotes is also known as a *string* (because it is essentially a string of characters, one after another - the letter 'I', followed by a space, followed by the letter 'a', followed by the letter 'm', etc.). Python does not care whether you use single quotes (like 'Hello, world') or double quotes (like "Hello, world"), as long as you use the same type of quote to both start and end the text (i.e. you cannot do "Hello, world'). Note that when we learn C, it is much more particular about only using double quotes for text.

Let's try it now:

```python
print('Hello, world')
```
Output:
```
Hello, world
```

## String Formatting
You can also use placeholders in your strings that get replaced with the arguments you pass to the format function.

For example:

```python
print('Hello, {}'.format('world'))
```
Output:
```
'Hello, world'
```
What is going on here? Well, we're using the same `print` function as before, but our argument is more complex. First, we see a text string as before: `'Hello, {}'`
However, after this text, there is a dot symbol `.`, followed by a function call to `format`, with an argument of `'world'`. In Python, the `.` symbol allows you to access specific *members* of a more complex *object*. While humans don't normally intuitively think of a text string like `'Hello'` as an object that contains multiple things besides the letters themselves, the Python interpreter provides all text strings with some common functions that any text string can use. One of these is the `format` function. The `format` function will substitute any arguments passed to it for any `{}` placeholder symbols in the string. So `'Hello, {}'` is substituted to get `'Hello, world'`, since `'world'` is the argument to `format`.
If instead, you called:
```python
print('Hello, {}'.format('Sam'))
```
it would instead print:
```
Hello, Sam
```

Note that the computer does exactly what you tell it, and only what you tell it. It does not understand spacing or punctuation, so it is critical to ensure that the text string contains these items if you desire them.
If for example, you instead typed:
```python
print('Hello{}'.format('Sam'))
```
it would instead print:
```
HelloSam
```
with no spacing or punctuation. The `print` commmand however does always output a newline character after printing its output.

## Comments
A *comment* in programming is a piece of text that is ignored by the compiler or interpreter. It is often used to provide notes or explanations about the code to anyone reading it, including yourself. Comments can be used to make the code easier to understand, to explain the purpose of a particular section of code, or to temporarily disable a section of code without deleting it.

The syntax for comments varies between programming languages. In Python, anything after a `#` symbol is a comment:
```python
# This is a comment and it is ignored by the Python interpreter: print('This is part of a comment')
print('Not a comment') # This part is also a comment
```
Output:
```
Not a comment
```
As you can see above, the comments are ignored, but the `print` command before the `#` still works properly. Comments are used throughout the example source files to help explain the code, as well as make it easier to follow along with this tutorial.

Documenting your code is a critical part of programming. Even recognizing what your own code does can be hard weeks or years later-- when other people need to use or modify your code, documentation is critical for making this feasible in a reasonable timeframe. Comments can be one way to improve the readibility and documentation of your code, regardless of whether or not you also create external documentation.

## Variables
A *variable* in programming is a named location where a program can store and manipulate data. This location is used to hold the value of an item, such as a number, a character, a string, a boolean value, or more complex data structures. This location is often located in a computer's memory, such as in *Random Access Memory (RAM)*, but can be located other places as well, including onboard the central processor itself (in what is known as a *register*).

You can store values in variables in Python with the `=` sign.

For example:

```python
x = 5
y = 10
```
stores the numbers 5 and 10 in the variables named *x* and *y*, respectively.
We can then use the `print` function, but instead of passing an text string as an argument, we pass the name of the variable `x` (note that there are no quotes):

```python
print(x)
```
Output:
```
5
```
which correctly prints the value we stored in the variable `x`

## Printing Variables
You can print the values of variables using string formatting.
For example:
```python
print('x is {} and y is {}'.format(x, y))
```
Output: 
```
'x is 5 and y is 10'.
```
Note that in this case, `format` has **2** arguments, not just 1. When passing multiple arguments to a function, you separate these arguments by a comma `,` as shown above. The value of the first argument `x` substitutes the value of the variable named `x` (in this case `5`) for the first `{}` symbol. The value of the second argument `y` substitutes the value of the variable named `y` (in this case `10`) for the second `{}` symbol. It is important that the number of arguments to `format` matches the number of `{}` symbols, or else the Python interpreter may produce an error.

## Arithmetic Operations
You can also perform arithmetic operations in Python. For example:
```python
print('x + y = {}'.format(x + y))
```
Output:
```
x + y = 15
```
Since the variable `x` is equal to 5 and the variable `y` is equal to 10, the code correctly outputs the sum `15`.
You can also do this with other mathematical operations, such as multiplication and division. You can store the results of mathematical operations into variables as well.
For example:
```python
z = x*y
print('x * y = {}'.format(z))
```
Output:
```
x * y = 50
```
This code multiplies the variables `x` and `y` and stores the result into a new variable named `z`. It then prints the result by passing `z` as the argument to the `format` function.

Try doing the same thing with division:
```python
d = x/y
print('x / y = {}'.format(d))
```
Output:
```
x / y = 0.5
```
Again, the code divides the variable `x` by the variable `y` and stores the result into a new variable named `d`, then prints the result by passing `d` as the argument to the `format` function.

Up until now, all of the numbers and numerical variables we used were integers. However, the result of dividing 5 by 10 is 0.5, which is not an integer. Python is smart enough to recognize this, so automatically treats the variable `d` as a *floating-point* variable, a variable that can hold not just integers but also fractional values. Python automatically handles conversions between integers and floating-point numbers and variables, so we don't generally need to worry about them, we can just treat all numbers the same way, unless we need to make a distinction for some reason.

## Functions
In addition to the functions that Python provides automatically for certain data types, you can also define your own functions.

For example:
```python
def add(x, y):
    return x + y
```
defines a function named `add` that takes two arguments (also known as *parameters*) and returns their sum. That means that this function `add` will have a *value* equal to the sum of the two arguments.

You can then call this function with:
```python
print("7 plus 3 is: {}".format(add(7, 3)))
```
Output:
```
7 plus 3 is: 10
```
As you can see, the value of 7+3 (10) was output in the text string by passing the *result* of the `add` function to the `format` function. While it may seem confusing to nest all these functions as arguments to other functions, it can actually simply your code considerably, since a single function might contain hundreds of lines of code doing hundreds of different operations. In addition, this means the next time you need to functionality of `add`, you do not need to write the code all over again, you can just call the existing function with new arguments. This can save you a considerable amount of time in a large program.

Note that the arguments that the function uses are defined in parenthesis after the function's name, much as one passes arguments when calling a function. If a function takes no arguments, you can just include empty parentheses instead (i.e. `def printhello():`)

The first line, which starts with the keyword `def` is sometimes called the *function header* or *function signature*. The process of defining it is known as *defining* the function.
All code in a function definition must be properly indented after the function header, so that the Python interpreter knows when the function ends.

The `return` keyword is used in a function definition to specify the result that the function should produce. When Python encounters a return statement, it will immediately exit the function and send the value that follows return back to the place where the function was called. In the above example, that means that the sum of `x` and `y` in the function will be used as the value of `add`.

## Global and Local Variables and Scope
It is important to understand that the `x` and `y` in the `add` function are **NOT** the same as the variables named `x` and `y` that we previously set above. This can be confusing, since they share the same names. The `x` that equals 5 and the `y` that equals 10 are known as *global variables*, which are variables that were declared outside of any functions. However, the arguments to `add` are also named `x` and `y`! These variables are called *local variables* and only have meaning within the `scope` of the `add` function. However, if there are multiple variables with the same name, variables *local* to a function (the most recently declared variables at that point in the code) always take precedence over other variables of the same name. That means that the `x` and `y` used in the line `return x + y` will be the *local* arguments `x` and `y` in the add function, not the *global* variable `x` that has the value of 5 or the *global* variable `y` that has the value of 10.

For example, if you instead defined a function `add2` as:
```python
def add2(a, b):
    return x + y
```
the function would not have any *local* variables named `x` or `y` so would instead use the *global* variables with those names. This means that `add2` would evaluate to 15 (5+10), regardless of what arguments were passed to `add2`.

```python
print("7 plus 3 is NOT: {}".format(add2(7, 3)))
```
Output:
```
7 plus 3 is NOT: 15
```

## Time Formatting
When you use the `{}` placeholder, Python tries its best to guess the format of the output based on the variable you pass. If it is an integer, it will display just the number, with no decimal point or leading zeros. If it is a floating point number like 4.251, it will display it to the precision available (in this case to the thousandanths digit). If you wish to change this behavior you can specify the format inside the `{}` placeholder.
For example, say we want to output time in the mm:ss format. We can use the `{:02d}` placeholder instead of `{}` for each of the minutes and seconds variables. This tells Python that we want to output the variable as a whole decimal number (integer), with at least 2 digits, padding it with zeros as necessary.

Let's break this down:
- `:`  The colon symbol starts the format specification, informing Python that we are going to provide format information for the placeholder.
- `0`  The first zero specifies that the number should be zero-padded.
- `2`  The second number specifies the minimum width of the output. If the number has fewer than 2 digits, it will be padded with zeros on the left to ensure it is at least 2 digits.
- `d`  The letter at the end specifies that the number should be formatted as a decimal number (i.e. an integer)

For example:

```python
minutes = 40
seconds = 9
print("Time elapsed: {:02d}:{:02d}".format(minutes, seconds))
seconds = seconds + 92
print("Time elapsed: {:02d}:{:02d}".format(minutes, seconds))
```
Output:
```
Time elapsed: 40:09
Time elapsed: 40:101
```
As we can see, the first line correctly added a leading zero to indicate 9 minutes. Since the second line already has at least 2 digits for both the minutes and seconds, nothing was added.

But wait! 101 is not a valid number of seconds. We want any number of seconds over 59 to wrap around and advance the minute counter, like a normal clock.

To do this, we will check to see if the variable `seconds` is greater than 59, so we can adjust both the `minutes` and `seconds` variables appropriately.

## Conditionals
You can use `if` statements to perform actions based on conditions. Python will execute the code indented underneath the `if` statement *if and only if* the condition that appears after the word `if` is *True*.

For example:
```python
if (seconds > 60):
    seconds = seconds - 60
    minutes = minutes + 1
print("Time elapsed: {:02d}:{:02d}".format(minutes, seconds))
```
checks if the variable `seconds` is greater than 60, and if so, subtracts 60 from `seconds` and adds 1 to `minutes`, then prints the new result.

Output:
```
Time elapsed: 41:41
```
That looks much better! But what happens if we add so many seconds it increases the number of minutes by more than just 1? The code above wouldn't work. For example:

```python
seconds += 153
print("Time elapsed: {:02d}:{:02d}".format(minutes, seconds))
```
Output:
```
Time elapsed: 41:194
```
The first line here is the exact same thing as writing `seconds = seconds + 153`, but is a common shorthand for adding a number to itself (it also works with `-=`, `*=`, etc.), to save on typing and make the code more compact.

The above output would not have be fixed with the `if` statement, because it wraps around more than once.

Instead, we can use the modulus operator `%`. The modulus operator gives the remainder of a division. For example:
```python
print("The seconds hand is at {:02d}".format(seconds % 60))
```
Output:
```
The seconds hand is at 14
```
prints the current position of the seconds hand (which was equal to 194, or 3 minutes and **14** seconds), ensuring that the value is between 0 and 59.

We also need to figure out how many minutes to increase the `minutes` variable by. To do this, we can divide `seconds` by 60 to figure how many minutes there are in 194 seconds. Note that because Python follows normal mathematical orders of operations (applying multiplication and division before addition and subtraction), we don't need to put the `seconds / 60` in parentheses, although some people prefer to, in order to be clear (e.g. `minutes + (seconds / 60)`).

```python
print("Time elapsed: {:02d}:{:02d}".format(minutes + seconds / 60, seconds % 60))
```
Output:
```
ValueError: Unknown format code 'd' for object of type 'float'
```
As you can see above, this code results in an error. The issue is that we used the `d` formatting character to force Python to print `minutes + seconds / 60` as an integer, but it is a floating point number. Python detects this as an error. You might ask, why Python can't just convert it to an integer on the fly, since it knows that the output is supposed to be an integer. The issue is that there are a lot of common programming bugs where the programmer doesn't realize that they are using a floating-point number as an integer, so Python throws an error instead of guessing, just to be on the safe side. This is often actually quite helpful in tracing down bugs in your code.

So, can we solve this by just removing the formatting? If we instead type:
```python
print("Time elapsed: {}:{:02d}".format(minutes + seconds / 60, seconds % 60))
```
Output:
```
Time elapsed: 44.233333333333334:14
```
This is also not what we want. We already accounted for the remainder in the `seconds % 60` part, we just want the integer part of `minutes + seconds / 60`.

To get this, we can explictly *force* Python to treat `seconds / 60` as an integer by using the *typecasting* operation. This is also known as *casting* for short. *Casting* works by providing the explicit type you want in parentheses, immediately before the variable or expression that you want to cast to that type. For example, `(int)(seconds / 60)` will force Python to treat the expression `(seconds / 60)` as an integer, rather than a floating-point value, as it normally would. This tells Python that we know what we're doing in treating it as an integer, and that it's what we really want, rather than a mistake/bug. Note that we need to add the parentheses, so that this is not the same as the expression `(int)seconds / 60`, which would not fix our problem. While `(int)seconds` would treat the variable `seconds` as an integer (although it already is one), when you divided that integer by 60, the result would still be a floating-point number, so we need to write `(int)(seconds / 60)` instead.

Incorporating this into our previous code:

```python
print("Time elapsed: {:02d}:{:02d}".format(minutes + (int)(seconds / 60), seconds % 60))
```
Output:
```
Time elapsed: 44:14
```
This finally gives us the behavior that we want. It is important to be careful whenever using typecasting, to be sure it's what we really want, and that we're not just accidently overriding legitimate bug detection on Python's part.

## Global variables
Before we move on, let's review the concept of global variables. Even though `x`, `y`, and `z` were set a long while back, they still contain those values they were assigned at the beginning of the program.
```python
print("x={}, y={}, z={}".format(x, y, z))
x = x + 2
print("x={}, y={}, z={}".format(x, y, z))
```
Output:
```
x=5, y=10, z=50
x=7, y=10, z=50
```
As we can see, even though we used *local* variables called `x` and `y` in the time in between, these *global* variables kept their originally assigned values.

When we add 2 to `x` here, it is referring to the *global* variable `x`, so it permanently changes the value of `x` until 7 (unless we change it again later).  Note that even though `z` was originally set equal to `x*y`, it maintains the value 50 that `x*y` was equal to *at the time of assignment*. The fact that `x` has changed since, does not change the value of `z` unless we explicitly assign a new value to `z`.

## Order of operations
As previously mentioned, Python follows the standard mathematical order of operations: 

```python
print("x+1*y-3/z is: {}".format(x+1*y-3/z))
print("(x+1)*(y-3)/z is: {}".format((x+1)*(y-3)/z))
print("z % x*2 is: {}".format(z%x*2))
print("z % (x*2) is: {}".format(z%(x*2)))
```
Output:
```
x+1*y-3/z is: 16.94
(x+1)*(y-3)/z is: 1.12
z % x*2 is: 2
z % (x*2) is: 8 
```
As we can see, on the first line, the multiplication and division occur before the addition or subtraction (7+10-3/50 = 7+10-0.06 = 16.94), as we would expect in math.

The second line uses parentheses to explicitly force the `(x+1)` and `(y-3)` expressions to be evaluated first (8*7/50 = 56/50 = 1.12).

The third line shows that the modulus operator `%` has a higher precedence than multiplication (50%7\*2 = (50%7)\*2 = 1*2 = 2). We can see the difference when we explicitly cause the multiplication to occur first in the fourth line (50%(7\*2) = 50%(14) = 8).

## Lists
You can store multiple values at once in a special type of variable called a *list*, by enclosing the elements inside of `[` and `]` brackets, separating each individual element by a comma `,`. For example:
```python
l = [17, 31, 5, 11, 12, 14, 24]
print(l)
```
Output:
```
[17, 31, 5, 11, 12, 14, 24]
```
creates a list `l` with seven elements. `print`ing the list variable `l` shows them all. Note that Python may show an abbreviated display of lists when they are very long.

### Accessing List Elements
You can access elements in a list by their *index* (their position in the list), by using the `[]` operator. For example:
```python
print(l[0])
```
Output:
```
17
```
will print the first (0th) element of the list `l`.

It is important to note that in Python (and C), the computer always counts starting from **0**, rather than starting from 1 like most humans do. So while the list `l` above has 7 elements inside, they are numbered from **0 to 6**, not from 1 to 7. That is why when we print the **0th** item, it shows the `17` that appears first in the list.

Similarly, if we want to print the last item in the list, we must print the **6th** item. Trying to print the item in position 7 will result in an error, since only items numbered 0 through 6 exist:
```python
print(l[7])
```
Output:
```
IndexError: list index out of range
```
Whereas list index **6** contains the actual list item in the 7 item list:
```python
print(l[6])
```
Output:
```
24
```
For clarity, we will often refer to the 0th numbered item in the list as list *index* 0, the next item as list *index* 1, etc.

You can also use the built-in function `len` to get the length of a *list*:
```python
print("There are {} items".format(len(l)))
```
Output:
```
There are 7 items
```
`len` takes a single argument, the object you wish to get the length of, in this case, our *list* `l`.

### Looping Over Lists
You can loop over the elements in a list using a `for` loop. The keyword `for` causes Python to loop through each item in the object specified after the keyword `in`, executing each line indented underneath the `for` line. These idented lines can access the *local* variable created by supplying a name directly after the word `for` (which in this case is *local* to the `for` loop, rather than to a function). For example:
```python
print("----")
for amount in l:
    print(amount)
```
Output:
```
----
17
31
5
11
12
14
24
```
In this case, the first line prints four dashes to indicate the start of a list. The `for` loop executes the idented `print(amount)` statement 7 times, once for each element of list `l`. On each time through the loop, the *local* variable `amount` will contain the value of successive elements of list `l`: that is, the first time through the loop `amount` will be 17 (the 0th item in the list), the second time through, `amount` will be 31, etc. In this way, the loop will print each element in list `l`, one at a time.

There are many other ways to use loops. Sometimes we might wish to loop through a portion of a list using the index numbers of the items in the list (0, 1, 2, 3, 6, etc. for their relative positions in the list). Python provides another built-in function `range` that automatically generates a list of integers in sequential order. For example, `range(1,3)` creates a list of numbers from 1 to 3. It is critical to note that in Python, the first argument to the `range` function specifies the beginning value and is *inclusive*, but the second argument to the `range` function specifies the ending value and is *exclusive* of this value. So `range(1,3)` results in the list `[1, 2]`. It does **not** include the number 3. This can be confusing, so some people find it helpful to think of the second argument as being the *"end before"* number; that is, the above command would make a list starting with **1** and ending **before 3** (i.e. just 1 and 2). We can use this `range` command to print just the items at index 1 and 2 in the list `l`:
```python
print("----")
for i in range(1,3):
    print(l[i])
```
Output:
```
----
31
5
```
Again, this code starts by printing some lines to indicate the beginning of a new list. It then calls `print(l[i])` on every items in `range(1,3)`. Since this is just `[1, 2]`, this means the indented line will be called just twice. Remember that the list indexes start from **0** rather than 1, so this prints 31 and 5 (elements 1 and 2), but **not** the 0th element that contains the 17.

### List Slicing
You can also get a subset of a list using *slicing*. To *slice* a list, we use the `[]` operator, just as if we wanted to access a single element of the list, but instead we provide the *start* and *end-before* range, separated by a colon `:`.

For example:
```python
print(l[1:3])
```
Output:
```
[31, 5]
```
This prints a *slice* of the list `l`, which is a new list that includes the elements at list index 1 and 2 in `l` (not 0 or 3). Please note that just as with the `range` function, *slicing* is *inclusive* of the starting position in the list, but **exclusive** of the ending position.

### Sorting Lists
You can sort a list using the `sort` function, which is a function that is automatically included as a *member* of any *list* created. Note that a *list* is a complex *object*. It contains an array (also sometimes called a vector) of data elements, but it *also* includes other things, like the *member function* `sort`. `sort` is part of every *list*, but it is **not** part of the actual array of data that you can access by specifying an index and using brackets `[]`. Instead, you access it by using the dot `.` operator. For example, `l.sort()` sorts the list `l` in ascending order:
```python
l.sort()
print(l)
print(l[0])
```
Output:
```
[5, 11, 12, 14, 17, 24, 31]
5
```
It is important to note that the list *member function* `sort` will modify the actual list itself. After calling `sort`, any access to list index 0 (e.g. `l[0]`) will give you the new value 5, not the original value 17 that used to be at index 0.

In addition to *member functions* contained in list objects, there are also *global* built-in functions provided for handling lists. Because these are not contained in the list objects, they are not accessed using the dot `.` operator, they are just called directly. One example is the *global* built-in function `sorted` which can also sort lists:
```python
backwards = sorted(l, reverse=True)
print(backwards)
print(l)
```
Output:
```
[31, 24, 17, 14, 12, 11, 5]
[5, 11, 12, 14, 17, 24, 31]
```
This code uses the `sorted` function to create a new list that is sorted in reverse order, and stores that reversed list in a new list variable `backwards`. It then prints both the new list `backwards` and the original list `l`. The first argument to `sorted` is the list to be sorted.

`sorted` has several additional arguments, but after the first, they are all *optional*. If they are not specified, they keep the default values internally defined by the `sorted` function. Specifying additional arguments will *override* these defaults.

In this case, by default `sorted` will sort a list in ascending order. Since we want to sort it in descending order, we specify `reverse=True` to override this behavior and cause it to sort in reverse (descending). `reverse` is the name of the argument we wish to change -- it is not actually the second argument to the function, but by using its name explicitly like this, we can skip having to specify the actual second argument to `sorted` (which is a more complex argument that will be explained later) and just let that second argument keep its default value, since we only care about the `reverse` argument. When we use the name of an argument explicitly, we no longer have to worry about that argument's order, since Python will automatically map it to the right argument for us. Note that because we don't do this with the first argument `l`, that argument still has to come first.

It is also important to note that **unlike** the list *member function* `.sort()`, the *global* function `sorted()` does not modify the contents of the list `l` to sort it, instead it creates a sorted copy of list `l`. Sometimes we may prefer one behavior over the other, so it is important to remember how they differ.

## Strings
As mentioned before, *strings* are just lists of characters. In fact, in Python you can do many things with *strings* that you can with *list* objects, if you think of each character in the *string* as a successive element in a *list*.

You can also store text directly in strings. For example:
```python
s = "I can code."
print(s)
print("The string is: {}".format(s))
```
Output:
```
I can code.
The string is: I can code.
```
This code stores the *string* `'I can code.'` in the variable `s`. It then prints it, both as a single line and as a variable passed to the `format` function using `{}` placeholders.

### Accessing String Characters
You can access characters in a *string* by their index, as well as *slice* them, just like with a *list*. For example:
```python
print("The string starts with '{}' and the middle is '{}'".format(s[0], s[2:5]))
```
Output:
```
The string starts with 'I' and the middle is 'can'
```
This code prints the first character (at index **0**) and the third through fifth characters (at indexes **2**, **3**, and **4**, but **not** 5) of the *string* `s`.

### Modifying Strings
What if we want to modify a *string*, for example change the first character from `I` to `U`? Let's try the method we can use on lists:
```python
s[0] = 'U'
```
Output:
```
TypeError: 'str' object does not support item assignment
```
While this works for *list* objects, it does **not** work for *strings*.

*Lists* in Python are *mutable*, meaning that you can change their values after they are created. On the other hand, *strings* in Python are *immutable*, meaning you can't change their characters directly after their initial creation. However, you can create a new string and assign it to the same variable. For example:
```python
s = "U" + s[1:]
print(s)
```
Output:
```
U can code.
```
This changes the first character of the *string* `s` to 'U' by creating a new string that combines the string "U" and the *slice* from the second character of `s` to the end of `s`. By leaving the number after the colon `:` operator blank, it indicates we want everything in the *slice* to the very end of the string. The result of the combination of the "U" with the rest of the string `s` is then stored in the variable `s`. This works because you can't modify a string, but you *can* reassign the variable `s` to your newly created, merged, combination string.

Why are strings *immutable*, but lists *mutable*? It is primarily an optimization that Python does for performance reasons. However, sometimes objects are also *immutable* for security reasons or to catch programming bugs. There is not always an easy way to know which types are *immutable* and which are *mutable*, so it is good to consult the appropriate documentation.

### Return Types
Understanding *mutable* vs *immutable* is also important in understanding functions. When a Python function returns a *mutable* type (such as a list), the caller receives a reference to the same object. This means that changes made to the returned object will affect the original object, which is similar to the concept we will see later about returning a type _by reference_ in C. On the other hand, while a Python function returns an *immutable* type, it cannot be modified, so it might as well just be a copy of the original object (and even if in Python's internal implemention it is still a reference to the original object for performance reasons, it does not matter, since it cannot be changed). This is similar to the concept we will see later about returning a type _by value_ in C.

For example, consider the function `increment()` that receives an number as its one argument, adds one to that number, and returns the new result:
```python
def increment(x):
    x = x+1
    return x

original_value = 5
new_value = increment(original_value)

print(original_value)  # Output: 5
print(new_value)       # Output: 6
```
Note that in this example, we passed the `increment()` function an _integer_ variable, and so it returned an _integer_ type as well. But if we passed in a _floating-point_ number such as `5.0` it would have returned that same type, a _floating-point_ number. We call Python a _dynamically-typed_ language because the variable type of these parameters and return values is not known until the function is used, when it will utilize whatever type it is called with.

The `increment()` function returns a new integer that is one greater than the input value. Even though it appears to modify the value of `x` inside the function, in Python integers are *immutable* types, so what is actually happening here is that we are creating a new variable `x` and initializing it with the new value of the old `x` plus `1`. So the `x` that is returned is really a copy, and it does not affect `original_value` outside the function, and only this copy is returned, not the original value. The original value remains unchanged because integers are *immutable*. This may be a bit counterintuitive and confusing, but even though you can assign them to new variables, Python's primitive types like _integers_ and _strings_ are all *immutable*, primarily for performance and predictability reasons, so each time you assign one you are actually creating a copy with the new value and the same name.

In contrast, consider an example with a _list_, which is a *mutable* type. The function `modify_list()` will append a `4` to the end of the _list_ passed in as its one and only argument, then return this same _list_:
```python
def modify_list(lst):
    lst.append(4)
    return lst

original_list = [1, 2, 3]
modified_list = modify_list(original_list)

print(original_list)  # Output: [1, 2, 3, 4]
print(modified_list)  # Output: [1, 2, 3, 4]
```
We create the _list_ `original_list` containing `1`, `2`, and `3`, and pass `original_list` to the function `modify_list()`, storing the result of this function in the variable `modified_list`. When we print `original_list` and `modified_list`, we find that they are the same!

The function `modify_list()` directly modified the *mutable* _list_ passed to it, and when it returned that same _list_ named `lst` as its return value, it was still a reference to `original_list`, so adding the `4` affected `original_list`.

Let's take a look at one more function. The Fibonacci sequence is a mathematical series of numbers where each number is the sum of the two preceding ones (starting with 0 and 1), for example `0 1 1 2 3 5 8 13 ...`. We will write a function `fibonacci()`, which given a number `n` as an argument, returns both the `n`-th and `(n+1)`-th Fibonacci number. In Python, it is perfectly fine for functions to return more than one value, they just must be separated by commas. Remember that Python indicies start from the 0th position, so the 0th number is `0` and the 4th number is `3`.

To implement this function, we need to determine the `n`th value of the Fibonacci sequence. But the only way to do this is to determine the `(n-1)`-th Fibonacci number first. We can call our _own function_ `fibonacci()` with the argument `n-1` to get this value. A self-referencing function is known as _recursive_. It can be very powerful, but we need to make sure there is a _base case_ with a value that we can determine without calling `fibonacci()`, or else we will loop indefinitely until the program runs out of resources. In this case, the _base case_ is when `n` is `0`. We can use a conditional `if` statement to test for this. If it is true, we will return `0` and `1` (separating the two return values with commas), the first two numbers in the Fibonacci sequence:
```python
def fibonacci(n):
    if n == 0:
        return 0, 1
```
If `n` is any other value, the code under the `if` clause will not be executed, meaning the program will not `return`, instead continuing to the next line. On the next line, we can get the two values (`n-1` and `n` from our perspective) that we store into variables `a` and `b` by calling our own `fibonacci()` function and passing `n-1` as the argument:
```python
    a, b = fibonacci(n-1)
    return b, a+b

print(fibonacci(6))  # Output: (8, 13)
```
When we print out `fibonacci(6)`, we correctly see the 6th and 7th numbers in the sequence, `8` and `13`.

Note that we could simplify this function. Since we already know `n` when calling `fibonacci(n-1)`, the function does not really need to return 2 values. But it is a useful exercise for exploring how recursive functions and return values work.
