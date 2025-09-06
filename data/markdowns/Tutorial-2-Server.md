# Python Server
Reference source file: `ServerPython.py`

## Python Server Introduction
For this lesson, we are going to write a networked server in Python. We will start with something simple and build it up from there. It is recommended that you do this in non-interactive mode, incrementally creating a `ServerPython.py` file from scratch as part of following along in this tutorial. If you attempt to simply follow along on the pre-created source file, you may have a hard time identifying which parts of the file correspond to which stages of the tutorial.

## main code
We will begin by writing the core code. In order to more easily be able to change these values as needed, we will use variables to represent the network name of the server `SERVER_NAME` and the port to listen for client connections on `SERVER_PORT`.
```python
SERVER_NAME = 'localhost'
SERVER_PORT = 12345
```
Initially, we will be running the client and server both locally for ease of testing during the early development process, so we set `SERVER_NAME` to `'localhost'` and pick port 12345 to use for `SERVER_PORT`. These can be changed in the future if you wish to use a different address/port.

```python
print(f"Starting server on '{SERVER_NAME}' port {SERVER_PORT}")
```
Next we print out a message to let us know the server is starting and remind us of what network address and port it is on. Rather than using the `print("Starting server on '{}' port {}".format(SERVER_NAME, SERVER_PORT))` technique we used before, we are using a form of Python shorthand to do the same thing. Putting an `f` before the start of the string to be printed is telling Python to do the exact same thing as calling `.format(SERVER_NAME, SERVER_PORT)` on the string, but instead of needed to pass the parameters as arguments to `.format()`, we can put them directly inside the placeholder braces `{}`, as shown above. Which form we use is a matter of personal preference, but some people find this notation easier to read because the variables can be seen directly inside the placeholder braces.

One other thing to note here is that while Python doesn't care whether we use single `'` or double `"` quotation marks for strings, when we want to actually print literal quotation marks, it's easiest to use the ones we do not want to print on the outside. That is, both `print("Hello, world")` and `print('Hello, world')` will output:
```
Hello, world
```
Python doesn't care which one we use. However, if we want to put the word `Hello` in quotes, then `print("'Hello', world")` will output:
```
'Hello', world
```
whereas `print('"Hello", world')` will output:
```
"Hello", world
```
Note that rather than nesting different types of quotation marks, we can also use backslashes to "escape" characters we want to literally print. To do this, simply put a backslash before the character we wish to print. This tells Python that the second and third `'` symbols are literally part of the string to be printed, rather than the closing `'` symbol to match the first opening `'` symbol. For example:
```python
print('\'Hello\', world')
```
will also output:
```
'Hello', world
```

To get back to our code, after printing out the message that the server is starting, we need to setup and start the server itself:
```python
start_server()
```
To make the organization of our program easier, we are going to encapsulate the main server code itself in a function called `start_server`. We now have to define this function:

```python
def start_server():
    listen_socket = initialize_server_socket()
    handle_new_connections_simple(listen_socket)
```
To define a new function, we start with the `def` keyword, then the name of the function, followed by any arguments in parentheses, then a colon symbol `:`. The body of the function is intended below this function header line.

Note that we place this function definition _before_ the main code of our program (the code above that prints a message and calls `start_server()`). This way by the time the Python gets to the main code, it already has the definition of `start_server`. In order, our whole program so far looks like:

```python
SERVER_NAME = 'localhost'
SERVER_PORT = 12345

def start_server():
    listen_socket = initialize_server_socket()
    handle_new_connections_simple(listen_socket)

print(f"Starting server on '{SERVER_NAME}' port {SERVER_PORT}")
start_server()
```

Because this function is really just to organize our code, it doesn't need any arguments. We're going to break down the operations of the server into two main phases-- setting up, and handling new connections. We will call `initialize_server_socket` to obtain a new socket that will listen for incoming connections. We then pass this new `listen_socket` as an argument to the function `handle_new_connections_simple`, which will listen on that socket for any incoming connections, and process them appropriately. Neither of these are existing Python functions-- they are both functions we made up that we will therefore have to define and implement.

## Creating a listening socket
Let's start with defining `initialize_server_socket`:
```python
def initialize_server_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
By convention, this function is also generally placed _before_ `start_server()`, so that `start_server` already knows what `initialize_server_socket()` does. However, as long as a function is declared _before_ it is used in the code, the order of function declarations does not matter in Python. This function does not require any arguments. It first uses the Python `socket` module to request a new socket. The function `socket` is confusingly also the name of a function of the `socket` module itself, which is why it is called as `socket.socket()`. Just as before, we use the `.` symbol to access a function that is part of a larger object. In this case, we are trying to call the `socket()` function contained inside the `socket` module. Normally functions won't have the exact same name as the module that contains them, but `socket` is unfortunately an exception to this general trend.

The `socket.socket()` function takes a few arguments. The first argument specifies what type of network protocol that you want a socket for (the Network Layer in the OSI model). For IPv4, use the value `socket.AF_INET`. For IPv6, you can use the value `socket.AF_INET6`. Some operating systems support other types of network protocols as well. The second argument specifies the type of socket requested within that network protocol (the Transport Layer in the OSI model). In this case, we want a TCP socket, so we use `socket.SOCK_STREAM`. The reason we put the `socket.` in front of all these values is because they are all defined inside of the Python `socket` module, so we need to use the `.` symbol in order to access them inside that module.

Next, we use the `bind` function to bind our new socket to a specific network address and port:
```python
    sock.bind((SERVER_NAME, SERVER_PORT))
```
This line uses the function `bind`, which is a function provided to sockets to be able to attach to a specific network address and port. But why isn't it `socket.bind`, since `bind` is defined as part of the `socket` module? Well, often functions are members of all data variables of a specific type. In Python (and most object-oriented programming languages), data variable types that contain functions or other components that you can access with the `.` symbol are also known as *objects*. In this case, any variable/object that is assigned the value of a socket (such as from the `socket.socket()` function call) will automatically contain functions for operating on that socket. Because these functions are contained in a specific socket `sock`, the `bind` call knows to apply only to the socket `sock`, rather than any other socket.

The other important thing to note here is that there is a single argument to `sock.bind()`. The single argument provided is `(SERVER_NAME, SERVER_PORT)`, which might look like two argument, but it's actually one argument (which is why there are two sets of parentheses after `sock.bind`, rather than one).

In Python, `(item0, item1, item2, etc.)` is used to denote a *tuple*, which is essentially an *immutable* vector containing one or more data items. So `(1, 2, 3)` would be a tuple that contains 3 numbers, and `(SERVER_NAME, SERVER_PORT)` is a tuple that contains 2 variables, `SERVER_NAME` and `SERVER_PORT`. A tuple is treated as a single object, which is why it is the sole argument to `sock.bind()`, despite the fact that the tuple passed as the arugment actually in turn contains 2 different variables.

Finally, we call `sock.listen()` to tell our new socket to listen for incoming connections on the bound port.
```python
    sock.listen(5)
```
Like `bind`, `listen` is a function contained in all socket objects. The argument to `listen` specifies the maximum number of incoming connections to queue at once before refusing new connections (also known as the *backlog*). This line tells Python that if there are already 5 incoming connections waiting to connect to the socket, any additional connections will be refused until that queue is reduced to below 5. If you don't want any incoming connections to wait for the socket to be available, you can pass zero as the argument. Be aware that regardless of what number you specify, the operating system might limit the maximum size of such a backlog queue.

Finally, the function needs to return the newly created and listening socket `sock`.

```python
    return sock
```
Please note that while the `socket` module is provided with pretty much every Python distribution on the planet, it is still not included in your program by default. Attempting to run the above code will result in a Python error such as:
```python
NameError: name 'socket' is not defined
```
In order to prevent this error from occurring, you need to tell Python to include the `socket` module in your program. To do this, at the very top of your Python source code, type:
```python
import socket
```
This will cause Python to include the `socket` module and make it available to your program, to avoid such errors.

## Handling new incoming connections
Again, we will start by defining a function to handle incoming connections:
```python
def handle_new_connections_simple(sock):
```
In this case, our function takes a single argument, `sock`, which specifies the listening socket that we watch for new connections.

*socket* objects provide a function `accept` which can be used to accept new incoming TCP connections. `accept` will block and wait until it receives a new incoming TCP connection. Once such a connection comes in, it will return a new socket created just for that connect, along with the network address that the new connection came from. Our code will loop forever to process every incoming connection, one at a time:
```python
    while True:
        conn, addr = sock.accept()
        print("Received new connection from ", addr)
        handle_client(conn)
```
The `while` keyword creates a loop, similarly to the `for` keyword, except instead of iterating through a list, it will execute the indented code underneath for as long as the condition directly after the word `while` is *True*. In this case, we specify `True` as our `while` condition, so the code will loop, executing the indented code over and over, forever. This is desired because we want our program to continue to accept and process new incoming connections forever, until the program is killed.

The notation `conn, addr = sock.accept()` shows that `sock.accept()` returns not just one argument, but two. By providing multiple variables, separated by commas, we can store the result (the return value) of the function `accept` in a new `conn` variable and a new `addr` variable all at once, with a single line of code.

`conn` contains the new socket created by the `accept` function just for the new incoming connection. This allows the listening socket `sock` to continue listening for and processing additional new connections.

`addr` contains the IP address of the source of the incoming connection. We see this address when it is printed out on the next line of code. The `print` statement there may look slightly different than how we have used `print` before. In this case, we are passing multiple arguments to `print`. This causes print to print each of the arguments, one after another. It does not provide the control and flexibility we get with the `.format` method function, but it can be a quick and easy way to print out a wider variety of data types.

### Nested functions
Finally, we want to actually do something with the new connection we received in `conn`. We are going to write a new function `handle_client` to handle this. Instead of defining a *global* function at the top level of our program, this function will be *local* to the `handle_new_connections_simple` function. This way it will only exist, and can only be accessed, from inside the `handle_new_connections_simple` function, not from anywhere else in the code. This allows us to make our `handle_new_connections_simple` code easier to read by abstracting the handling of new connections away into a sub-function, but to also make it clear that it is associated with `handle_new_connections_simple`, rather than the rest of the program.

Now we need to define the `handle_client` function. This function will watch the new connection for data, print out any data received, then send that same data back to the sender over the network.

We put function this directly underneath the `def handle_new_connections_simple(sock):` line, to indicate it is contained in this function. This is sometimes also referred to as a *nested function*:
```python
    def handle_client(conn):
        while True:
            data = conn.recv(1024)
```
We start with a function definition line as usual, with a single argument `conn` which will be passed the new connection socket returned from the `accept` function. Note that `conn` in `handle_client` is a `conn` variable *local* to the `handle_client` function, and only takes the value passed as an argument to `handle_client`, rather than any `conn` variable that might appear outside of the `handle_client` function. In this case, we actually pass the `conn` variable from the `handle_new_connections_simple` function as the `conn` argument to the `handle_client` function, so they will have the same value for that reason, but it is important to realize that they could be different if `handle_client` was ever called somewhere else, with a different argument passed to it. As you can see, it can sometimes be confusing to name them the same thing in different functions, and you may want to consider picking more unique names for some of your local function variables.

Note that both the `handle_client` function definition and its body of code are all indented by one tab more than normal, since they are inside the `handle_new_connections_simple` function.

### Receiving data
`handle_client` also uses a `while True:` statement to loop forever, so it keeps receiving incoming data as long as it is available. Each pass through the loop, it can receive up to 1024 bytes of incoming data using the `recv` function, which is another method function contained in socket objects. The argument to `recv` is the maximum number of bytes we want to receive at a time, in this case 1024. We could have picked a different number, but too small of a size could make the program less efficient (since we would need a lot more times through the loop to receive the same amount of data), and too large of a size might use too much memory (because Python needs to set aside this many bytes of memory to hold the incoming data), so 1024 is a reasonable value for now. Experimenting with this parameter could allow us to tweak network performance and memory usage further. The result (return value) of the `recv` function is stored in the variable `data`.

Note that just because a client sends us 500 bytes of data at once, doesn't mean we will actually receive all 500 bytes in a single call to the `recv` function, despite that fact that it *can* receive up to 1024 bytes at a time. Due to the ways different operating systems and network stacks are implemented, we might receive all 500 bytes at once, or 10 bytes in the first `recv` call, followed by 470 bytes in the next `recv` call, or any other possible combination of one or many sets of data. Sometimes a network stack or even a hardware NIC itself will buffer incoming data until it receives a certain amount or a certain amount of time has passed. When we test our program locally, we likely will get the data all at once, however in real-world conditions from servers on the other side of the world under heavy load, the situation might be quite different. This is one reason why our testing strategy has to be broad enough to try all sorts of different situations. By using a `while` loop for our `recv` calls, we ensure that no matter how many chunks the data is separated into when we receive it, we will be able to process it all.

If the `recv` function is called after a socket is closed and all data has been received, it will return the special value `None` instead of data. `None` is essential an "empty" variable in Python-- it contains no data. In Python, `None`, `0`, and `False` will all evaluate to `False`, for example in a condition after an `if` or `while` statement. The keyword `not` will negate a `True` or `False` expression. Therefore, `not data` will be `True` if and only if `data` is `False`, `0`, or `None`.
```python
            if not data:
                break
```
The `if` line will check to see if the `data` returned from the `recv` function is empty. If it is, it means the connection has closed and all the outstanding data has been received, and it will execute the command on the indented line: `break`.

### The `break` command
`break` is a special command used to exit the current loop (in this case a `while` loop, but it also works on `for` loops). If you have nested loops (one loop indented inside another), `break` will only exit from the innermost loop it is inside.

In this case, `break` causes the program to stop the `while` loop and continue execution of the code after the `while` loop, when the connection has closed and all the outstanding data has been received.

If `data` is not empty, we will print out the data to the screen, as well as send it back to the sender:
```python
            print('Received:', data)
            conn.sendall(data)
```
`print` allows us to print the `data` returned from the `recv` function. `sendall` is another member function contained in *sockets* that transmits any data passed as its argument through the connected socket. Note that `data` is actually a *bytes* object. This is an *immutable* sequence of characters like a *string*, but it can contain binary data as well as text. We can create our own *bytes* object with `bytes([0, 1, 2])` to specify the bytes contained in its sequence, but we do not have to worry about this here, because `recv` already created the *bytes* object for us.

In the previous `if not data:` line, you might have wondered what would happen if we received a `0` byte over the network, since if `data` is `0` this would cause the `if` condition to be `True`, and the loop to exit. However, because `data` is a *bytes* object, it is not an integer, so will never have a value of `0` itself if it is not empty, even though it might contain 1 or more bytes in its sequence that have a value of `0`. In order words, `data` can contain a `0` without being `0` itself. So we do not need to worry about exiting prematurely just because we receive `0` byte values over the network, because a `0` byte is still a byte of data.

### Closing the socket
Once the `while` loop has been exited, we also need to close the *socket*. To do this, we use the *socket* member function `close`:
```python
        conn.close()
```
It is important to remember to `close` any sockets we create (for example, the ones we created by calling the `socket()` or `accept()` functions), in order to free the resources that both Python and the operating system reserve for each socket. If we do not properly `close` sockets once we are done with them, we may eventually run out of memory or the ability to create or accept new network connections. Failure to `close` a socket also can cause the other side to keep a connection open much longer than it should. For example in our code above, if the incoming connection is not closed by the sender, our code will never exit the loop, and so we will be waiting to receive new data forever (or until the connection times out or our program is killed). 

Note that this line shares the same indentation as the `while` line, so it is not part of the `while` loop, it is only executed after the `while` loop is exited. Since the `while` condition here is always `True`, the loop only exits when the connection is closed and `break` is called.

To see this in context, the entire `handle_new_connections_simple` function in order now looks like this:
```python
def handle_new_connections_simple(sock):
    def handle_client(conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received:', data)
            conn.sendall(data)
        conn.close()

    while True:
        conn, addr = sock.accept()
        print("Received new connection from ", addr)
        handle_client(conn)
```

## Testing the server
Now, let's try running this server:
```bash
python3 ServerPython.py
```
Output:
```
Starting server on 'localhost' port 12345
```
So far, so good! The program correctly prints the port it is listening for new connections on. Let's hit Cntl-C to kill the server.

What if we want to show the proper machine name instead of just 'localhost'? The `socket` module provides a member function for this as well, `socket.gethostname()`. Instead of using localhost, let's set `SERVER_NAME` to this value, right before we call `print` in our code:
```python
SERVER_NAME = socket.gethostname()
print(f"Starting server on '{SERVER_NAME}' port {SERVER_PORT}")
start_server()
```
Let's try running this server again:
```bash
python3 ServerPython.py
```
Output:
```
Starting server on 'server27' port 12345
Traceback (most recent call last):
  File "/usr/local/linuxexamples/basic/ServerPython.py", line 173, in <module>
    start_server()
  File "/usr/local/linuxexamples/basic/ServerPython.py", line 147, in start_server
    listen_socket = initialize_server_socket()
  File "/usr/local/linuxexamples/basic/ServerPython.py", line 141, in initialize_server_socket
    sock.bind((SERVER_NAME, SERVER_PORT))
socket.gaierror: [Errno 8] nodename nor servname provided, or not known
```
This example was created on a machine with a local name of 'server27'. Your output may vary slightly based on your machine name and operating system. While our program correctly output the local name of the machine rather than just 'localhost', the `Traceback` message and everything below it show an error that was encountered. Any error not handled in Python will automatically exit the program. In this case, we can look to the bottom of the message to see the actual error -- errno 8, which means that no valid address was provided to the argument for `sock.bind()`. Above this message, we can see the entire chain of function calls in our program that led to the line of code where the error occurred. This can be useful for pinpointing the source of an error.

Why did this error happen in this case? `sock.bind()` tried to resolve the local machine name 'server27' to an IP address, however, the DNS server used doesn't know who 'server27' is, since it only appears locally on our machine. In a properly configured enterprise network, our local DNS server might be able to resolve these local computer names, in which case a valid IP address would be found and the program would work as intended. Alternatively, on some operating systems, there is a `hosts` file or Control Panel setting where entries can be added. We could add the local machine name to this, to make it resolve to the IP address 127.0.0.1, which would fix the problem.

In this case, for maximum compatibility, we are just going to go back to using `localhost` as the server name, since that is already set up to resolve to 127.0.0.1. Simply remove the `SERVER_NAME = socket.gethostname()` we just added, and run the program again:

```bash
python3 ServerPython.py
```
Output:
```
Starting server on 'localhost' port 12345
```

Let's try to connect to the server. Eventually, we will write another program to be the client, but for testing, we will use the *netcat* program (also called `nc`). `nc` is installed on many operating systems by default, but if it is not, you can download it. In an apt-aware Linux distribution (such as Debian or Ubuntu), you can also install it with `apt-get install netcat`.

Once `nc` is installed, we can use it to connect to our server on port 12345. The first argument to `nc` on the command line is the network address of the host to connect to, and the second argument is the port to connect to. In this case, we use the loopback IP address 127.0.0.1 to specify the local host and port 12345 for our server:
```bash
nc 127.0.0.1 12345
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
```
The server correctly accepts the incoming connection from `nc` and prints its IP address and port. In this case, `nc` is running on the same local host loopback address as the server, and a high-number ephemeral port. Your output will probably show a different port number than the above example, since these ports are generated dynamically and can take different values.

Next, let's type some input into `nc` to send to the server:
```bash
Hello
```
You should see the following:

ServerPython Output:
```
Received: b'Hello\n'
```
The server correctly prints out the data received, before sending it back to the client over the socket.
`nc` Output:
```
Hello
Hello
```
The `nc` program shows what we typed and sent to the server, followed by the message we received back from the server (which is the same as what we typed in `nc`).

You can send more data to experiment further, or press Ctrl-C to kill the `nc` program. You can also instead press Ctrl-D in `nc` at the input prompt, which will send an End-of-File (EOF) message, indicating that no more data exists from the client side of the connection, and will cleanly close the socket. Because the server program does not accept user input, you will need to use Ctrl-C to kill the server. We will discuss this distinction in more detail later.

## Parsing command line arguments
Let's add one more feature to the server before we move on to the client. As we have seen above, we can change the port the server listens on by changing the SERVER_PORT variable in the source code. However, we can make it even easier by allowing this to be set at run-time, as a _command line argument_.

Command line arguments are commonly used in command line programs, for example, the program `ls` to list a directory in Unix:

```bash
ls -l /tmp
```
In this case, there are two arguments to the program `ls`. The first, `-l`, is sometimes also called a flag or option and is used to indicate that `ls` should list files in "long" format, which includes additional information such as owner and group information, modification date, size, and permissions flags. The second argument `/tmp` indicates the directory to list (without specifying this argument, `ls` will just list the current directory).

In a POSIX-style environment such as the standard C library or Python's `sys` package, we refer to the program's name on the command line (`ls` in the above example) as argument #0, the next argument (`-l`) as argument #1, and so forth (making `/tmp` argument #2). While it might seem like the 0th argument is redundant, sometimes it is useful to know or display the exact name of the program as it was invoked, for debugging or error reporting. In Python, we often execute Python programs with a syntax like `python3 ServerPython.py -p 1000`. In this case, the _Python program's name_ `ServerPython.py` will be the 0th argument, the `-p` will be the 1st argument, and so on.

To access these arguments in Python, we need to first include the `sys` package at the top of the source code:

```python
import sys
```

Next, we add a new function `parse_command_line_arguments`, which will return the port to start the server on. We will put this function directly before the first line of the main program, that is, right before the `print(f"Starting server on '{SERVER_NAME}' port {SERVER_PORT}")` line and after the `start_server()` function:
```python
def parse_command_line_arguments():
    port = SERVER_PORT
```
This function does not need any arguments, as these will be provided from the command line. It starts by first setting the local variable `port` to the value of the global variable `SERVER_PORT`. This sets the default value of `port`, that is, the port to start on if there is no command line argument to change it.

Next, we will use the list `sys.argv` provided by the Python `sys` package to look for a `-p` on the command line.
```python
    # Check if -p parameter is provided
    if '-p' in sys.argv:
```
The `in` keyword checks to see if an item is contained in a list or other container variable. If a `-p` appears as any element of the list `sys.argv`, this expression will return _true_ and the following code will be executed:
```python
        index = sys.argv.index('-p')
        if index + 1 < len(sys.argv):
            port = int(sys.argv[index + 1])
```
This first line above tells us which list element contains the `-p` and stores that index number in the local variable `index`. The second line adds one to that index (so that the result refers to the next argument immediately following that index) and checks to make sure it is less than the total number of arguments in the list `sys.argv`. If so, it assigns the argument immediately after the indexed argument to the local variable `port`. For example, if we type:
```bash
python3 ServerPython.py -p 40000
```
The local variable `index` will be 1, since that is the position of `-p` in the list `sys.argv`. The local variable `port` will therefore contain the number at index 2, which is `40000`.

In the above example, `len(sys.argv)` would be 3, since there are 3 command line arguments (at index 0, 1, and 2). Since the argument `40000` is at index 2 of the list `sys.argv`, this is valid and will execute. However:
```bash
python3 ServerPython.py -p
```
would not be valid and so the arguments will be ignored, since `index + 1` (which would be 2) will not be less than `len(sys.argv)` (which would also be 2). The `if index + 1 < len(sys.argv):` check prevents our program from crashing in this situation.

Finally, we need to return the local variable `port`, so it is used later to set up the server on the indicated port number.
```python
    return port
```

Note that this completed `parse_command_line_arguments()` function will only find the first match, if `-p` appears more than once on the command line. This is not an issue for us, since specifying more than one port number is not something that makes sense in this program, but it is something to keep in mind for other situations.

Note that instead of writing `port = sys.argv[index + 1]`, we passed this value to the `int()` function first. This is because `sys.argv[index + 1]` is a character string containing the characters `4`, `0`, `0`, `0`, and `0`. By using the `int()` function on this character string `int(sys.argv[index + 1])`, we force it to be converted to an integer instead. This practice is also known as _casting_ a variable. This is important since we want to make sure the port is a number rather than as a string. If we remove the `int()` call, we will get an error such as:
```bash
python3 ServerPython.py -p 40000
```

ServerPython Output:
```python
TypeError: an integer is required (got type str)
```
On the other hand, with the `port = int(sys.argv[index + 1])` call in place to ensure that `port` is an integer, we get:

ServerPython Output:
```python
Starting server on 'localhost' port 40000
```
Note that for some lower port numbers to work correctly (anything below 1024 on most Unix-like operating systems), the program must have superuser privileges.

## Parsing regular expressions
Anyone who has spent a lot of time with Unix programs will recognize that in addition to the `-p` style flags, many programs also support a more human-readable syntax for passing arguments to programs, of the form `--port=40000`.

To support both syntaxes in our program, we will add some additional code to detect this `--argument=value` syntax.

We replace the last line (`return port`) of our prior `parse_command_line_arguments()` function with:
```python
    # Check if --port= parameter is provided
    for arg in sys.argv:
        match = re.match(r'--port=(\d+)', arg)
        if match:
            port = int(match.group(1))

    return port
```
This code takes a different approach by using Python's regular expression library to match the desired pattern. The `for` loop iterates through each command line argument in the list `sys.argv`. Each time through this loop, it calls the `re.match()` function to detect any matches that start with the form `--port=NUMBER`, which is the regular expression passed as the first argument to `re.match()`. This argument starts with an `r` before the regular expression format string to tell Python that is a regular expression pattern, rather than a normal string. Therefore `r'--port=(\d+)'` tells `re.match()` to match text that starts with the exact text `--port=`, followed by a number. The expression `(\d+)` is a wildcard that matches a group of one or more successive decimal digits (i.e. `0`-`9`). Those not familar with regular expressions may wish to view more detailed documentation of Python's regular expression syntax at https://docs.python.org/3/library/re.html

The second argument to `re.match()` is the string to check for this regular expression (i.e. each successive argument passed on the command line, one during each successive iteration of the `for` loop). If there is a match to a given argument, then the local variable `match` will contain a match object and evaluate to _true_, and the next lines of our function will assign `int(match.group(1))` to the local variable `port`.

The `match` member function `match.group()` is provided by the `re` package to retrieve part of all of a matched regular expression. The argument (`1`) passed to `match.group()` returns the 1st captured group (specified in the regular expression string by '`(\d+)`'). If there were additional captured groups in that regular expression string, they could be returned instead by passing an argument of `2`, `3`, etc. to specify which captured group is desired. In this case, `match.group(1)` returns the number immediately after the character string `--port=`. As before, we use the `int()` function to ensure that this is stored as an integer.

As before, it is not a valid command line argument to use `--port` more than once, so it doesn't matter in this circumstance. However, it is important to understand the implications of ordering in other situations. If the user specifies both the `-p` and `--port` flags, which one gets used? Since the local variable `port` is returned at the end of the function, its last value is all that matters. That means that if `-p` sets the local variable `port` and then the flag `--port` later sets `port` again, only the last value is returned. The same thing occurs if the user uses the `--port` flag more than once on the command line. If we want to only use the first matched value in either case, we can do this by returning `port` immediately after a match in either case, for example:
```python
def parse_command_line_arguments():
    port = SERVER_PORT

    # Check if -p parameter is provided
    if '-p' in sys.argv:
        index = sys.argv.index('-p')
        if index + 1 < len(sys.argv):
            port = int(sys.argv[index + 1])
            return port

    # Check if --port= parameter is provided
    for arg in sys.argv:
        match = re.match(r'--port=(\d+)', arg)
        if match:
            port = int(match.group(1))
            return port

    return port
```
Again, this doesn't really matter for this program, but thinking about the implications of unexpected situations (such as a user specifying multiple `--port` flags where we only expect one, or passing an invalid argument such as a `-p` that is not followed by a number) is important for security, since many exploits are based around providing inputs that a program was not designed for.

Note that we also need to import the `re` package at the top of the source file in order for this function to work:
```python
import re
```
Now we can test our new function:
```bash
python3 ServerPython.py --port=40000
```
ServerPython Output:
```python
Starting server on 'localhost' port 40000
```
We can see that the server correctly starts on the specified port.