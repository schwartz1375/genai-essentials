# C Basics
Reference source file: `ServerC.c`

## Introduction to C
Now that you have a handle on Python programming, we will move onto learning C. We will implement a server in C to work with the `ClientPython.py` code that we previously wrote.

C is a powerful, low-level programming language that serves as the foundation for many modern programming languages and systems. Known for its efficiency and control, C allows developers to write programs that interact directly with hardware, making it a popular choice for system programming, embedded systems, and performance-critical applications. In a sense, it is sort of like a human-readable, universally portable version of machine instructions that allow you to control, in most cases, how your program works on the hardware and operating system. Unlike higher-level languages like Python, C requires you to manage memory manually and explicitly define data types, giving you fine-grained control over how your program operates. This tutorial will introduce you to the basics of C, including its syntax, data types, and fundamental programming constructs, helping you build a strong foundation for writing efficient and robust C programs.

## main function
Every C application program must contain a function named `main` (libraries, drivers, plug-ins, and other extensions may have different entry points). `main` serves as the entry point to the program and is called by the operating system when a program is executed.

C specifies a specific function signature that the operating system uses to call `main()`:
```c
int main(int argc, char* argv[]) {
    return 0;
}
```
This is very similar to a Python function definition, with a few differences. Rather than a colon `:` and indentation in a function definition as in Python, we put the contents of a function instead curly braces `{` and `}`. There is no `def` keyword used in C, but the return type of the function is declared to be an `int` (integer). We put the data type before its use in the declaration: `int` before `main` since the `main()` function's return type is `int`, and `int` before `argc` because `argc's` data type is `int`. The function takes 2 arguments (named `argc` and `argv` in this case), and returns a value of 0 on success. If we return a non-zero value, the operating system will know that our program exited with a failure condition. The meaning of specific codes is typically defined by the operating system and/or the application developer. On Unix-like systems, this return value is accessible using the `$?` variable in the shell after the program exits (`echo $?` will print the return value).

In C, all variables, whether global, local, function parameters, return values, or any other type of variable, are _explicitly typed_ rather than _implicitly typed_ as they are in Python. This means that we need to tell the C compiler exactly what type to use for each variable at compile time, as opposed to Python, where the compiler infers the type of the variable at runtime, based on what is assigned to it or how it is used. While C's _explicit typing_ requires more effort on our part when writing the initial code, it also allows the compiler to better optimize code and detect type-related errors at compile time, rather than at runtime as would happen in Python. For example, the following Python code would generate an `TypeError` `Exception`:
```python
s = "Test"
x = s + 4
```
This is because you cannot add the number 4 (as opposed to the string "4") to a string. Since Python does not resolve the type until run-time, it throws an `Exception` that will cause the program to crash if not caught inside a `try` clause.

In C, since we tell the compiler the type of every variable, it can identify most of these errors at compile-time, potentially saving us time debugging the executable later. This is the trade-off for doing the extra work to _explicitly_ indicate each variable's type.

Keeping this in mind, when we define our `main()` function, we need to declare both the return type of the function as well as the type of each argument (`int` and `char*`):
```c
int main(int argc, char* argv[]) {
    return 0;
}
```
We already discussed the meaning of the `int` returned by `main()`. The `argc` is of data type `int` and contains a value of the number of arguments passed to the program. For example, if our program is called `ServerC`, we might invoke it with a port number from the shell with a command like:
```bash
./ServerC -p 12345
```
In this case, `argc` would be equal to `2`. The second argument `argv`'s data type is an array, which is why it has the brackets `[]` after the argument name. The `char*` before the argument name indicates that they array contains `char*` variables, which are C's versions of strings and are also known as `char` _pointers_. We use the `*` operator after `char` to indicate that it is a _pointer_, which is a memory address where one or more `char`s are stored. We will explain _pointers_ in more detail shortly, but for now the important thing to understand is that a `char*` can be used as a string in C. Therefore `argv` is essentially an array of strings. In the above example, `argv[1]` is the string `-p` and `argv[2]` is the string `12345` that were passed on the command line.

But what about `argv[0]`? Just as in Python, C arrays start counting from `0`. So the first element of the array `argv` is actually the 0th element `argv[0]`. However, the above statements about `argv[1]` and `argv[2]` are still accurate, because the 0th element `argv[0]` contains the name of the program itself, as it was invoked on the command line, `./ServerC`. Note that this string includes the relative path `./` that was used on the command line. If instead an absolute path was used, such as `/usr/bin/ServerC`, then that value would be contained in the string `argv[0]` instead.

As previously discussed, this function returns a value of `0`, since it always exits successfully (since there is no other code yet).

Unlike Python, C also doesn't care how much whitespace we use. For example, the following `main()` functions all compile to the exact same binary code:
```c
int main(int argc, char* argv[]) {
    return 0;
}
```
```c
int    main( int argc , char *argv[])
{
    return 0 ;
}
```
```c
int main(int argc,char* argv[]){return 0;}
```
Since C does not care about indentation or whitespace, it requires a semicolon after every command, in order to tell the compiler that it is at the end of that command. As a result, there must be a semicolon `;` after the `return 0` command before any other commands, but it does not need to be on the same line.

C also uses curly braces `{` and `}` to indicate the beginning and end of a function and/or clause. These are not commands, so are not followed by a semicolon.

C also simplifies and resolves extra parentheses at compile time, so `return 0` is the same as `return(0)` or `return(((((0)))))`. Note that, as in Python, while the keyword `return` does not require parentheses after it, function calls still do require at least one set of parentheses (otherwise the compiler won't know we're calling a function).

Even though the above definition of the `main()` function is the standard function signature used when calling an application program, C will allow us to define this signature differently if we so choose. For example, we can change the names of the argument variables:
```c
int main(int numArgs,char* argList[])
```
In this case, we can refer to the arguments by the names we give them instead of the more commonly used names.

We can also change the types and numbers of arguments. For example, there are some operating systems that support an additional argument with extra information. Or maybe we just don't care about the arguments or the return value. In that case, we can define `main()` as:
```c
void main(void)
```
`void` is a special data type that represents the lack of an argument or return value. It is not a zero, it is an indicator that there is nothing there. When `void` is put before the word `main`, it tells the C compiler that there is no return argument at all. The compiler will therefore raise an error if we try to `return` a value from this function. Similarly, when `void` is used for the argument list, it means that the function has no arguments. In this case, the operating system still passes the same `argc` and `argv` information to our program, since the function signature used by the underlying operating system does not change, but our `main()` function just ignores them.

## Data Types
Before we add additional code, we should understand some of the different data types used in C.

In C, `char`, `short`, `int`, `long`, `long long`, `float`, `double`, `long double`, and `void` are all data types. They differ in the amount of memory they consume and the range of values they can represent. The exact sizes of many of these variables can be platform-dependent, but there are some standards:

`char` is used to store a single character and always requires 1 byte of memory (per the C standards, including ISO C9899, C89, C11, C17, etc.). The range of values is -128 to 127 _(signed)_ or 0 to 255 _(unsigned)_. On most platforms, `char` is _signed_ by default. To explictly treat `char` as _unsigned_, we can use the type `unsigned char` rather than `char`.

`short` is used to store short integers. It is guaranteed to contain _at least_ 2 bytes of memory. The range of values is -32,768 to 32,767. On virtually all common modern platforms it will be exactly 2 bytes of memory, but this is not guaranteed by the C standard, and some old, rare, or obsure platforms may use larger `short`s. We can use the data type `int16_t` to guarantee exactly 16-bits (2 bytes). If we wish to treat a `short` as _unsigned_, we can use the type `unsigned short` rather than `short`, in which case its range of values will be 0 to 65,535.

`int` is used to store an integer. It is guaranteed to contain _at least_ 2 bytes of memory and be at least as large as a `short`. On most modern platforms it uses 4 bytes of memory, in which case the signed range of values is -2,147,483,648 to 2,147,483,647. However, some 64-bit platforms or compilers might use an 8 byte `int` and older or obscure platforms might use a _smaller or larger_ `int`. We can use the data type `int32_t` to guarantee exactly 32-bits (4 bytes) or `int64_t` to guarantee exactly 64-bits (8 bytes). As before, we can also define an `unsigned int` to treat it as _unsigned_.

`long` is used to store a long integer. It is guaranteed to contain _at least_ 4 bytes of memory and be at least as large as a `int`. It is 4 bytes large on many systems (in which case, the range of values is typically -2,147,483,648 to 2,147,483,647), but can be 8 bytes on others, and may be still other sizes on other platforms. As before, we can also define an `unsigned long` to treat it as _unsigned_.

`long long` is used to store a very long integer. It is guaranteed to contain _at least_ 8 bytes of memory and be at least as large as a `long`. As before, we can also define an `unsigned long long` to treat it as _unsigned_.

`float` is used to store a floating-point number (i.e., a number with a decimal point). It is guaranteed to be at least as large as a `char`. On most platforms it contains 4 bytes of memory, where the range of values is approximately ±3.4E-38 to ±3.4E+38 with 6 decimal places of precision. Since unlike integers, floating-point numbers can represent a very wide range of numbers, these differences in size tend to not matter as much as with integers, unless specific precision is required.

`double` is used to store a double-precision floating-point number. It is guaranteed to be at least as large as a `float`. On most platforms it contains 8 bytes of memory, where the range of values is approximately ±1.7E-308 to ±1.7E+308 with 15 decimal places of precision.

`long double` is used to store a long double-precision floating-point number. It is guaranteed to be at least as large as a `double`. On most platforms it contains 10 bytes of memory, but can be 12 or 16 bytes on others, and may be other sizes on more obscure platforms.

When it is important that a number be a specific size, for example when serializing numbers to files or a network packet, it is better to use types such as `int64_t` and `int16_t`, which are portable and guaranteed in size. When this is not important, the native non-portable types such as `short` or `int` can be more efficient, since the compiler can optimize their size based on the architecture, taking advantage of specific processor registers, alignment, and other optimizations.

If portability and consistency across platforms are a concern, using the specific sized types like `int64_t` are generally a better choice because they guarantee the exact same width on all platforms. Note that there are also specific sized types that begin with that letter 'u', like `uint8_t` and `uint32_t`, that represent _unsigned_ types of the specific number of bits indicated.

## Variables
Just as in Python, the scope of C variables can vary based on where and how they are declared. We can declare _global variables_ at the top of a C source code file, before any functions, to ensure that they are in scope for the entire file.

For our server, we want to declare 2 _global variables_, a string to represent the pathname to the file used to store our log data, which we will call `gFilePath`, and an integer to represent the port number our server will listen on, which we will call `gNetworkPort`:
```c
char* gFilePath;
int gNetworkPort;
```
The data type precedes the variable's name, in this case `char*` for a the file path string, and `int` for the port number. Note that we could also use `unsigned short` since TCP & UDP ports range from 0 to 65535, however using `short` could be problematic since it only ranges from -32,768 to 32,767 on most platforms, and TCP & UDP ports can be higher than 32,767. An `int` should generally be large enough on all modern platforms (where it is at least 4 bytes), and allows us to also use negative port numbers if we need to represent various error conditions.

The use of a letter 'g' before _global variable_ names is used by certain programming style standards, but there are many others. The naming conventions for variables will ultimately be driven by the standards used by our organization. Note that C requires a semicolon after each variable declaration, and extra whitespace is ignored.

While not required, it also good programming practice to provide default values for _global variables_. This way, if they are accidently used before they are initialized, they will not have unexpected results, which could include incorrect data values,program crashes, and security vulnerabilities. Therefore, we will initialize them to specific, but clearly invalid, values:
```c
char* gFilePath = NULL;
int gNetworkPort = -1;
```
`NULL` is a special value provided by C that is similar to the special value `None` in Python. However, while `None` is a special object in Python, in C `NULL` literally has a value of zero, which is not a valid string at all and will generally cause a program to crash if it attempts to use that string (with some caveats to be discussed later).

We set the `gNetworkPort` to an initial value of `-1`, which is an invalid port. This will make it easier to see if we accidently use it before initialization when debugging.

## Functions
Let's define a new function to experiment with variables. We will call it `variable_test()`:
```c
void variable_test(void) {
    printf("Test function called\n");
}
```
This function does not return a value, so we use the data type `void` before the function's name in its definition. It also does not take any arguments, so we use `void` again in its parameter list.

As with `main()` the function's code is contained within curly braces `{}`. We start with a single line that prints a messages stating that this function was called to the system's standard output (the console/command line on most systems). This line uses the C library function call `printf()`, which takes as its first parameter the string to be printed. Note that C strings **must** use double quotation marks, unlike in Python where they can be enclosed in either single or double quotation marks. In C, single quotation marks are only used for single character `char`s, not strings. The `\n` at the end of the printed string indicates a newline, which is not automatically printed in C, unless we specify it as we do here. Finally, we include a semicolon `;` after the `printf()` function call to indicate that it is the end of our command.

We also need to add a call to our new `variable_test()` function inside `main()`:
```c
int main(int argc, char* argv[]) {
    variable_test();

    return 0;
}
```
While some older C compilers do support implicit function declarations, many compilers require function headers (also referred to as _function signatures_ or _function prototypes_) to be explicitly declared before their use or definition. Even if a compiler does not require this, it is still a best practice to prevent errors related to functions that might be invoked incorrectly. Therefore, we will also declare our function near the top of our source code file. We will put this after our _global variable_ declarations, but this is not mandatory:
```c
void variable_test(void);
```
A C function declaration typically contains the same header as in the function's definition (although, strictly speaking, the names of parameters are not required), followed by a semicolon to indicate the end of the declaration. Now our `variable_test()` function can be defined and used anywhere below it in the source code file. 

## Compiling
In order to test this code, we need to first _compile_ the program, then to _link_ it to any other code or libraries, and finally to _execute_ the _compiled_ binary. This is in constrast to the standard Python implemention, which _interprets_ Python code at run-time rather than _compiling_ it to a machine-executable binary in advance. _Compiling_ this code translates it from human-readable C source code to binary machine instructions for the platform it is intended to _execute_ on.

If using the popular `gcc` compiler, we can _compile_ and _link_ our program with a single command on the command line:
```bash
gcc -o ServerC ServerC.c
```
The `-o` flag is used to specify the name of the output file (our executable that will be run) `ServerC`. We then supply the names of one or more input files, in this case, just `ServerC.c` for now. Running this command will generate a new executable called `ServerC`. Other compilers or graphical IDEs may provide other ways to perform these or similar actions, such as a "Compile" or "Run" command from a menu.

When we attempt to _compile_ `ServerC.c`, we get an error message that looks something like (line numbers and text may vary slightly):
```
ServerC.c:7:5: error: call to undeclared library function 'printf' with type 'int (const char *, ...)'; ISO C99 and later do not support implicit function declarations [-Wimplicit-function-declaration]
  7 |     printf("Test function called\n");
      |     ^
ServerC.c:7:5: note: include the header <stdio.h> or explicitly provide a declaration for 'printf'
1 error generated.
```
This error is telling us that the function `printf()` is undefined. This is true, since we did not define it anywhere. While it is a function supplied by the standard C library, we still need to include the proper files to use it, just as we did in Python with its modules. `printf()` is defined in a header file called `stdio.h`. In Unix, `man` section 3 contains these library functions, so we can identify the correct header file to include by typing `man 3 printf` on the command line. There are also many websites containing such information, such as https://www.gnu.org/software/libc/

It is important to note that compiler errors are not "bad" things. They prevent run-time errors that are much harder to debug. So we should not be overly concerned with encountering errors during compile time, this is a normal part of the process and it saves us a lot of time debugging later. Fixing issues at compile time is preferable to fixing them at run-time.

## The C Preprocessor
C uses a command `#include` which is similar to Python's `import` command, except that it works at the file level, rather than at the module level. C commands that begin with the `#` symbol are known as _preprocessor directives_ and handled by the C compiler's pre-processor. The C preprocessor is a tool that processes the text of your C source code before it is compiled by the compiler. _Preprocessor directives_ are not actual C code, but are instead instructions for the preprocessor to modify its copy of our source code in its internal buffer before it is passed to the compiler. An `#include` _preprocessor directive_ followed by a file replaces that line with the entire text of the indicated file. It does not actually modify our original source code file, just the C compiler's copy that the preprocessor passes to the compiler. By conversion, `#include` commands are usually put at the top of a C source code, before _global variable_ and _function prototype_ declarations (since the information inside the included files is sometimes needed by these declarations), but this is not a requirement.

We will discuss other _preprocessor directives_ later, but for now, we will `#include` the `stdio.h` header file at the very top of our source code:
```c
#include <stdio.h>
```
When we enclose the file's name in angled brackets `<>` this way tells the preprocessor to look for the indicated file in the system's include directories (e.g. `/usr/include` on Unix-like systems) and is generally used for most system-provided header files. If we instead enclose the file's name in double quotation marks `""`, the preprocessor will first search for the file in the current directory, before falling back on system-defined include paths. This is typically used for custom header files that we write as part of our program.

Now that we included `stdio.h`, let's try again to compile our program:
```bash
gcc -o ServerC ServerC.c
```
The program _compiled_ successfully (no errors were displayed, although depending on our settings, we may not see any indication of success other than the lack of errors and the presense of a new file called `ServerC`).

Let's _execute_ our new exectutable:
```bash
./ServerC
```
Output:
```
Test function called
```
The program works, successfully printing our supplied text string.

## More About Variables
Now, let's try working with our _global variables_. After our first `printf()` call, let's add another `printf()` command to print out the current value of our network port:
```c
printf("gNetworkPort: %d\n", gNetworkPort);
```
This utilizes the `printf()` command using a special placeholder that begins with a percent `%` symbol. This is somewhat similar to the `{}` placeholder symbols used in Python strings. `%d` will be substituted by the decimal number passed as an additional argument to `printf()`. As with Python's `.format()` method, if multiple placeholders are used, multiple additional arguments must be supplied. Other common placeholders include `%s` for a string or `%f` for a floating-point number, but the `man` page for `printf` lists many more, along with various modifiers that can be used with them.

Much as in Python, in addition to _global variables_, we can also use _local variables_ that are more limited in scope.  We declare _local variables_ the same way we declare _global variables_, except we do so inside of the function or scope they will affect:
```c
void variable_test(void) {
    double   f;
    short a=8080, b =         12;
    char   c = a +
              b;
    long d,e,array[10];
    long long total;
    long double matrix[2][5];

    printf("Test function called\n");
    printf("gNetworkPort: %d\n", gNetworkPort);
```
As shown above, C supports a fairly flexible syntax for variable declarations, but does require the data type to explicitly come first. A semicolon is required at the end of each variable declaration statement, but a single statement can contain multiple variable declarations of the same type, separated by commas. We can also initialize the values of these variables in the declaration (although they are _mutable_ and can change later). We can use whitespace whereever we want, including multiple lines, even in a horribly inconsistent manner as shown above, however this is not a good programming practice and it is best to be consistent and adhere to our organization's style guides.

In addition, we can declare arrays in C with brackets after the variable's name, such as `long array[10]` above. The number inside the brackets indicates the size of the array. Arrays declared in C in this manner are fixed in size and generally cannot be resized later. We can also declare multi-dimensional arrays with 2, 3, 4, or even more sets of brackets, each specifying the size of the array in that dimension.

In older versions of C, _local variables_ could only be declared at the beginning of a block of code specified by curly braces `{}` (such as a function's body or an `if` clause containing braces), however virtually all modern C compilers support variable declarations throughout the code.

If next in the function, we print out the values of some of these variables using `printf`:
```c
    printf("a=%d, b=%d, c=a+b=%d, total=%lld\n", a, b, c, total);
```
Then we compile and run the program as we did before:
```bash
gcc -o ServerC ServerC.c
./ServerC
```
We get the output:
```
a=8080, b=12, c=a+b=-100, total=0
```
`a` and `b` make sense, since those are the values we initialized the variables to. `c` should be equal to `a+b`, or 8080+12 = 8092. However, because `c` is of data type `char`, it can only hold a single (signed) byte on most platforms. This means it can't hold a number as large as 8092. In hex, 8092 would normally be represented as 0x1F9C (using big-endian notation). Since a `char` is only 1 byte in size, it only gets the 0x9C. When interpreted as an unsigned value this would be 156 in decimal, or 0b10011100 in binary. However, when interpreted as a signed value, this is -100 in decimal, which is why that value is printed out above. If it is unclear why this is, see "https://en.wikipedia.org/wiki/Two's_complement" for additional explanation on the most common binary representation of negative numbers.

In the above example `total` was printed out as `0`, but it might show any other value when run on many platforms. This is because it was never initialized, so its value is technically undefined. We should never use uninitialized variables, since it might contain data from other variables no longer in use, which might present a serious security vulnerability if the uninitialized value contained a password or secret key or other sensitive data. This is an example of something that we should never do, and some compilers may generate warnings or errors based on this behavior. Note that we use the token `%lld` in the `printf()` function call to specify that this number is a `long long` decimal number.

## Order of Operations
C introduces increment `++` and decrement `--` operators, where `a++;` is like saying `a += 1;` or `a = a + 1;`. However, when the value of `a` is used in conjunction with whether the increment `++` and decrement `--` operators appear before or after the variable in an expression.

For example, let's look at what happens if we add the lines:
```c
    d = a++;
    e = --b;
    f = a + b;
    printf("a=%d, b=%d, d=%ld, e=%ld, f=a+b=%lf\n", a, b, d, e, f);
```
`a` starts at `8080` and `b` at `12`, which they are initialized to in the variable declaration at the top of this function. When we assign `a++` to the _local variable_ `d`, since the `++` occurs _after_ the variable, `d` takes the value of `a` _before_ it is incremented, `8080`. But `a` will be `8081` after this line is executed, the increment simply occurs after its value is assigned to `d`.

On the other hand, since the `--` occurs _before_ the reference to `b`, the _local variable_ `e` takes the value of `b` _after_ it is decremented, `11`. `b` will also be `11`, as expected:
```
a=8080, b=12, c=a+b=-100, total=0
a=8081, b=11, d=8080, e=11, f=a+b=8092.000000
```
Note that appropriate tokens are used with `printf()` to ensure each variable is printed as its correct type.

Note that using an increment or decrement operation on a variable, and then using the same variable later in the same expression is not defined by the C standard, so this behavior should be avoided. For example, `a++;` is fine, but `a = a--;` or `b = a-- + a` can lead to undefined behavior, since it is ambiguous, in addition to being confusing.

As with Python, C generally follows the common mathemetical standards for order of operations. The incremement and decrement operators (`++` and `--`) have a higher precedence than other operators. So if we add the following lines to our function:
```c
    total = ++a - b-- * d / e + d % e;
    printf("a=%d, b=%d, d=%ld, e=%ld, total=%lld\n", a, b, d, e, total);
```
We get the output:
```
a=8080, b=12, c=a+b=-100, total=0
a=8081, b=11, d=8080, e=11, f=a+b=8092.000000
a=8082, b=10, d=8080, e=11, total=8
```
Which is equivalent to the expression:
```c
total = (++a) - ((b--) * d / e) + (d % e);
```
First the values of `++a` and `b--` are evaluated, incrementing `a` to `8082` before using its value, but decrementing `b` to `10` only _after_ using its value of `11`:
```c
total = 8082 - (11 * d / e) + (d % e);
```
Next, C evaluates the `*`, `/`, and `%` operators at same level of precendence, so they are evaluated from left to right. We will substitute in the values to make this easier to follow:
```c
total = 8082 - (11 * 8080 / 11) + (8080 % 11);
total = 8082 - (88880 / 11) + (8080 % 11);
total = 8082 - (8080) + (6);
```
Finally, C evaluates the `-` and `+` operators, which are at same level of precendence, from left to right, when gives us a `total` equal to `8`, as was printed in our output above. Using parentheses in complex arithmatic expressions is highly recommended as a best practice in order to minimize confusion and keep code readable and understandable.

## Arrays and Loops
We also defined some array variables in this function, so let's see how they can be used. First, we will make a loop to count from 0 to 9 to fill each of the 10 elements of the variable `array` (remembering that we start counting from index 0). To do this, we will call the `printf()` function to label the line, then assign a value to and print each element of the array. For purposes of this example, each element in `array` will contain its index:
```c
    printf("Array: ");
    d=0;
    while(d < 10) {
        array[d] = d;
        printf("%ld ", array[d]);
        d++;
    }
    printf("\n");
```
After the initial `printf()` call, we need to loop keeping track of the current index in `array`. Since indicies start from `0`, we set our counter variable `d` to `0`. Next, we use a `while` loop to loop as long as `d < 10`. A `while` loop in C is similar to a Python `while` loop, but it contains an expression of when to end looping, followed by code to execute during each iteration of the loop.

In our example, our `while` loop should continue as long as the variable `d` is still less than `10` before each iteration. This ensures that we will never try to use an index for `array` that is greater than or equal to `10`, which would be larger than its size (since `array` has 10 elememts, going from element index 0 to element index 9). Trying to access elements outside this range could result in a crash, security vulnerability, or other undesirable behavior.

The code after the `while` condition could be a single C statement ending in a semicolon, for example `while(d<10) d++;`, which would count from 0 to 9 without actually doing anything besides incrementing `d`, and then exit when `d` reached `10`. However, in our code above, we want to execute more than one C statement, so we enclose those statements in curly braces `{}` to indicate a multi-statement clause. Note that semicolons are required after each statement in the clause, but the clause itself is not a statement, so does not require a semicolon after it.

The code inside the clause consists of 3 statements. The first assigns the current value of the index `d` to the corresponding element of `array`. The second calls the `printf()` function to print the value of that element, followed by a space for formatting. The third increments the value of `d` by 1 (we could have also used `d += 1` or `d=d+1`). After this clause is finished executing, the `while` loop checks to see if it is still true that `d<10`, in which case executes the clause again. Otherwise, it exits.

Finally, we call `printf()` to print an end-of-line character `\n` after we are done displaying the array elements, to keep this output on its own line. After compiling and running our program, we get the additional output:
```
Array: 0 1 2 3 4 5 6 7 8 9 
```
This correctly prints out each element of `array` in order.

Note that we could also have handled this with a `for` loop instead of a `while` loop. A `for` loop in C is somewhat similar to a `for` loop in Python, with some differences. First the keyword `for` is followed by 3 elements in parentheses, separated by semicolons. The first element contains code to execute before the `for` loop begins, the second contains an expression checked before each iteration of the loop, that when no longer `true` will cause the loop to stop and exit, and the third contains code to execute after each iteration of the loop. So:
```c
for (_preloop initiation code_; _end condition_; _after iteration code_)
```
Any of these 3 sections may also be empty if there is nothing to do in that situation. As with a `while` loop, this is followed by the code to execute _during_ each iteration to the loop, while can either be a single C statement ending with a semicolon, or a clause enclosed in curly braces `{}`.

For example, to use a `for` loop to replace the above `while` loop, we can write:
```c
    printf("Array: ");
    for (int i=0; i<10; i++) {
        array[i] = i;
        printf("%ld ", array[i]);
    }
    printf("\n");
```
After printing the title of the line as before, this `for` loop has 3 parts within its parentheses. First, we initialize an index variable `i` to `0`. While we could have also used the pre-existing variable `d` as we did before, in this case we actually define the variable `i` right inside the initialization part of the `for` loop. This gives it scope that is limited to the `for` loop itself (both the parentheses and the following clause).

Second, we tell the C compiler that we want to keep iterating as long as `i<10`, which is essentially the same condition we used in the `while` loop above, ensuring that we stop after index `9`.

The third component of the `for` parentheses is the code to execute after each iteration. In this case, we increment `i` here using the `++` operator, after each iteration, to move to the next index value.

After the parentheses containing 3 parts, comes the code to execute during each iteration of the `for` loop. In our above example, it is a clause consisting of multiple statements contained inside braces `{}`. As with our previous `while` loop, the first assigns the current value of the index `i` to the corresponding element of `array`. The second calls the `printf()` function to print the value of that element, followed by a space for formatting.

Due to the earlier inclusion of the `i++` in the third section of the `for` loop's parentheses, we do not need to increment `i` inside this clause, since `i` is already going to be incremented after each iteration by the `for` loop itself.

Compiling and running this code produces the same output as using the `while` loop:
```
Array: 0 1 2 3 4 5 6 7 8 9 
Array: 0 1 2 3 4 5 6 7 8 9 
```
The syntax of the `for` loop means it is sometimes easier, less coding, or more clear to represent a loop with `for`, however sometimes a `while` loop might be easier or make more sense. Either loop can be used to accomplish the same tasks, the best choice generally comes down to style and simplicity for a given situation.

We can also utilize such loops to handle multi-dimensional arrays such as the variable `matrix` declared previously. We can think of `matrix` as a 2-dimensional table containing both rows (the first number in brackets) and columns (the second number in brackets). We can utilize _nested_ `for` loops, where the outer loop iterates through the rows while the inner loop iterates through the columns, to iterate through our 2-dimensional `matrix`. In the example below, during each iteration we will grab the value of the corresponding element from the 1-dimensional `array` previously created, then print it, essentially converting the 1-dimensional `array` into a 2-dimensional `matrix`, one element at a time:
```c
    printf("Matrix: \n");
    for (int i=0; i<2; i++) {
        printf("  Row %d: ", i);
        for (int j=0; j<5; j++) {
            matrix[i][j] = array[i*5 + j];
            printf("%Lf ", matrix[i][j]);
        }
        printf("\n");
    }
```
The first `for` loop iterates through both of the 2 rows of `matrix`. The second (inner) `for` loop iterates through each of the 5 columns (starting from index `0`). To get the corresponding element from `array`, we need to use an index to `array` from 0 through 9. We do this by mulitplying the current row number by the total number of columns (5), then adding the column index within that row. So, `matrix[0][0]` corresponds with `array[0]`, `matrix[0][4]` corresponds with `array[4]`, and `matrix[1][1]` corresponds with `array[6]` (1*5+1).

We add a newline after each row is completed. Also note that since the data type for the elements of `matrix` is long double, we need to use the corresponding token `%Lf` when calling `printf()`. The capital `L` indicates a `long double`, rather than `%lf` which indicates a regular `double`.

Once we compile and run our new program, our complete output is:
```
Test function called
gNetworkPort: 0
a=8080, b=12, c=a+b=-100, total=0
a=8081, b=11, d=8080, e=11, f=a+b=8092.000000
a=8082, b=10, d=8080, e=11, total=8
Array: 0 1 2 3 4 5 6 7 8 9 
Array: 0 1 2 3 4 5 6 7 8 9 
Matrix: 
  Row 0: 0.000000 1.000000 2.000000 3.000000 4.000000 
  Row 1: 5.000000 6.000000 7.000000 8.000000 9.000000 
```
