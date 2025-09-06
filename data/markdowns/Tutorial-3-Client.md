# Python Client
Reference source file: `ClientPython.py`

## Python Client Introduction
For this lesson, we are going to write a networked client in Python. This client will interact with the server we build in the previous tutorial, as well as others. We will again start with something simple and build it up from there. It is recommended that you do this in non-interactive mode, incrementally creating a `ClientPython.py` file from scratch as part of following along in this tutorial. If you attempt to simply follow along on the pre-created source file, you may have a hard time identifying which parts of the file correspond to which stages of the tutorial.

## Making a connection
As with the server, we will start with some basic code to set up the client. We will set up a new connection to the server, then send some data and listen for a response.

Since we know we're going to be using the `socket` module, we'll start by including it at the top of the file:

```python
import socket
```

Next, we need to write the main code of our program:
```python
print('Starting client...')
start_client_simple()
```

First we `print` a message that we are starting the client. Then, we call a new function that we will write called `start_client_simple` to handle the work of setting up the connection and handling any input and output. Again, this allows us to better organize our program, by keeping this code together in its own `start_client_simple` function.

As before, prior to the `print` line (but after the `import socket` line), we need to define the `start_client_simple` function:
```python
def start_client_simple():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12345))
    send_data_simple(sock)
    receive_data_simple(sock)
    sock.close()
```

Since this function is really just to help us organize the code, we do not need any arguments. We start by creating a new `socket` with the `socket.socket()` function as before (calling the `socket()` function that is contained in the similarly named `socket` module). As in the server example, we pass `socket.AF_INET` as the first argument to specify an IPv4 socket and `socket.SOCK_STREAM` as the second argument to specify a TCP socket. We need to use the `socket.` format to access these `AF_INET` and `SOCK_STREAM` constant values, since they are contained inside the `socket` module. We store the result of the function (which is the data object that represents the newly created TCP socket) inside a new variable named `sock`.

Once the socket `sock` is created, we need to connect it to the server. To establish this connection, we call the `connect()` method function contained in all socket objects. `connect` takes a _single_ argument, the server address. However, this server address is actually a *tuple* containing 2 items, a text string containing the server hostname or IP address, and the TCP port number. We use `localhost` to connect to a server on our same machine, and `12345` as the port number we established in our server code.

Note that `connect` will not return until the socket is connected, so by the time we get to the next line, we know `sock` has connected. We will deal with what happens if there is an error later. Once the connection is established, we will send the data with a function `send_data_simple`, then listen for a response by calling a function `receive_data_simple`. These are functions that we just made up, so we will need to implement them, above the `start_client_simple` function.

Finally, after we receive the response, we are all done with this connection, so we need to call `sock.close()` to ensure Python properly cleans up all the resources associates with the socket (which also causes it to send the final TCP FIN/ACK packets to terminate the connection properly).

## Sending data
In order to get a working program, we need to define these new sending and receiving functions we made up.
```python
def send_data_simple(sock):
    sock.sendall(b'Hello, world')
```
First, we define the function `send_data_simple` to receive a single argument containing the socket we wish to send data on. This function assumes that this socket is already connected. It is the callers responsibility to make sure that is so. This sort of assumption should be documented. It is common to put such documents in a comment that occurs before the function, along with a description of the function and any arguments or return values, for example:
```python
# send_data_simple sends data on a specified socket, then returns once all data has been sent
# Arguments: sock - specifies the socket to send data on
# Return Value: None
# Assumptions: sock is a valid socket that is already created and connected
def send_data_simple(sock):
    sock.sendall(b'Hello, world')
```
We use the `sendall` method function contained in the socket object `sock` to send the message "Hello, world". Note the `b` in front of the text string "Hello, world" here. If we were to just call `sock.sendall('Hello, world')` we would get an error like:

Output:
```
TypeError: a bytes-like object is required, not 'str'
```
This is because `sock.sendall()` expects data in the form of bytes, not as a string of text. Sockets are designed to handle raw bytes of data, which can be used to send any kind of data, not just text. For example, they might contain pictures or sounds, neither of which are normally represented in ASCII characters. Each byte in a sound file might contain a value from 0 to 255 (the maximum value that can fit in an unsigned byte) that represents the amplitude of the sound wave at each successive point in time (assuming 8-bit sampling quantizing it into one of 256 discrete values). There are not enough letters, numbers, and common symbols available in ASCII characters to represent all 256 values using a single byte-- so this is instead stored as binary data that can contain the full range of values.

A Python *bytes object* is similar to a text string in that it contains a sequence of bytes, but these bytes represent binary data, rather than a text string that contains letters like 'A' or 'k' or numbers like '3' or standard symbols like '$'. Because Python treats binary data sequences and text strings differently, it is important to keep track of which one is used in each variable and function, so the correct type can be used in each situation. To do otherwise will cause an error or unexpected operation of a program.

In this case, placing a `b` before a text string automatically tells Python to treat the following sequence as binary *bytes* data, rather than as a text string like it normally would if we just typed `'Hello, world'` without the leading `b`. This makes it easy to pass a binary *bytes object* containing our message by calling `sock.sendall(b'Hello, world')`.

## Receiving data
We also need to define the function that handles receiving the response:
```python
def receive_data_simple(sock):
    data = sock.recv(1024)
    print('Received:', data)
```
`receive_data_simple` also takes a single argument containing the socket on which to receive data, and prints out any data received.

## Testing the client
Now that we have a complete program, we need to test it to make sure it operates as intended.

We could use `nc` to test the client just as we did with the server. However, since we've already tested the server, we're going to jump straight to testing the client with the working server. Even if we had initially validated the client by testing it with `nc`, we'd still want to test it with the server. It is important to verify that the client and the server work correct together, as they are intended to be used. Programs can sometimes have very complex interactions, and there may be second- or third-order effects that may interact that might not show up in basic tests with `nc`.

First, let's start the server, as before:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
Now, in another tab/window/terminal, start the client:
```bash
python3 ClientPython.py
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 64073)
Received: b'Hello, world'
```
ClientPython Output:
```
Starting client...
Received: b'Hello, world'
```
As we can see, the server correctly receives the client's incoming connection (your port number for the incoming connection may vary), as well as the "Hello, world" message that the client sent. The server then echos this message back to the client. The client correctly prints out the message received, and then exits.

Note that the server is still running and ready to accept new connections, so if you were to run the client again, you would see the additional messages.

## UDP
As previously mentioned, we specified `socket.SOCK_STREAM` as the second argument to the `socket.socket()` function call when creating the socket `sock`, to specify a TCP socket.

Let's try making the client use UDP instead.  To do this, we will define a new version of the `start_client_simple()` function called `start_client_simple_udp()`:
```python
def start_client_simple_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_data_simple_udp(sock)
    receive_data_simple_udp(sock)
    sock.close()
```
As before, we call `socket.socket()` to create the new socket, but for the second argument we instead pass `socket.SOCK_DGRAM` to specify a UDP socket.

Since UDP sockets do not have state, there is no connection process like we had with TCP, we can just send and receive data once the socket is created. Therefore, we do not need the `sock.connect()` call we had in the TCP version.

We will also define UDP versions of `send_data_simple()` and `receive_data_simple()`. Finally, we still need to remember to `close()` the socket once we are finished, so that any memory and other system resources are properly cleaned up.

The definitions of these UDP versions of the functions are similar to the TCP versions with some minor modifications:
```python
def send_data_simple_udp(sock):
    sock.sendto(b'Hello, world', (SERVER_NAME, SERVER_PORT))
```
Instead of calling the function `sock.sendall()`, we use `sock.sendto()`. This allows us to specify a *tuple* containing the destination network address and UDP port directly in the `sendto()` function call. This is not necessary for TCP connections because `sock.connect()` establishes a TCP connection to a specified network address and port already, and all communications over an established TCP socket go to that same destination. However, with UDP, the socket is not connected to any specific destination network address or port (since UDP is stateless, it doesn't really even have a concept of being "connected"). Therefore, we need to specify the destination every time we send data. Note that this means you can use the same UDP socket to send data to many different destinations, if desired.

While we could write `sock.sendto(b'Hello, world', ('localhost', 12345))` to hardcode the destination like we did in the `start_client_simple()` function, it is better coding practice to use variables to specify the network address and port. Therefore, we will define new *global variables* `SERVER_NAME` and `SERVER_PORT` at the top of our Python file, right after the `import` statements:
```python
import socket

SERVER_NAME = 'localhost'
SERVER_PORT = 12345
```
Using variables for the destination tuple instead of hardcoding the specify server name and port number makes it much easier to change these in the future if desired, or if a different port number is passed in on the command line. We could also go back and change this in the `sock.connect()` arguments inside of the `start_client_simple()` function.

Next, we define `receive_data_simple_udp()`:
```python
def receive_data_simple_udp(sock):
    data, address = sock.recvfrom(1024)
    print('Received (from {}):'.format(address), data)
```
Again, since UDP sockets don't have the concept of being "connected" to anything, a UDP socket might receiving data from anywhere, and each new set of data received might come from a different network address and port. Therefore we call `sock.recvfrom()` instead of `sock.recv()`, which also returns the address and port of whereever the data is being received from. While `sock.recvfrom()` takes the same argument as `sock.recv()`, it actually returns 2 result values, not 1. We handle these by providing 2 different variables to store the results in, thus the `data, address = ` nomenclature. The first return value is the received data (as in the `sock.recv()` function), this is stored in a new local variable called `data`. The second return value to `sock.recvfrom()` is a tuple containing the network address and port of the sender, which is stored in a new local tuple variable called `address`. This `address` variable is printed out in the `print` function on the next line.

We might note that `data, address` kind of looks like a *tuple* without any parentheses. In fact, when a function returns multiple arguments, rather than specifying multiple variables to store the results in, we could instead choose to store the results in a tuple:
```python
def receive_data_simple_udp(sock):
    result = sock.recvfrom(1024)
    data = result[0]
    address = result[1]
    print('Received (from {}):'.format(address), data)
```
In this case, both the data and sender information are stored in successive elements of a *tuple* -- a new local variable named result. `data` and `address` are then populated from the appropriate elements of that *tuple*. This is generally harder to read than the previous way, but can be useful if there are a lot of unused return values, or if we wish to pass around the results as one unit, rather than separate variables. For example, if a function returns 10 different results, and we only really care about one, it is probably simpler to use a single tuple to store all the results and just access the one we need. Or if we are calling another function that we need to pass all the results to, we can just pass a single tuple instead of 10 separate individual variables. For most use cases, however, it is generally easier to use the first method of setting multiple individual variables equal to the function (e.g. `r1, r2, r3 = function_name()`).

Now that we defined all the UDP versions of the functions we need, the only thing remaining is the change the last line of our Python client program to use them. That is, change the `start_client_simple()` call at the bottom of the Python file to `start_client_simple_udp()`.

Now we can test our UDP version of the client. Since the server still uses TCP, we will test this using the `nc` program:
```bash
nc -l -u 12345
```
Note that some versions of `nc` might require a `-p` flag to specify a listening port, so if this does not work, we may need to try `nc -l -u -p 12345` instead. On the other hand, some versions of `nc` will only work without the `-p` flag, so check `nc -h` or `man nc` for the appropriate flags for the version in use if there are any issues.

We use the `-l` flag to indicate that `nc` should listen for incoming connections, acting in the server's role. It will print any output it receives.

We use the `-u` flag to indicate that `nc` should use UDP rather than TCP, so `nc -l -u 12345` will cause `nc` to listen for data on UDP port 12345.

Now, in another tab/window/terminal, start the client:
```bash
python3 ClientPython.py
```
Our ClientPython program will automatically send its "Hello, world" message using UDP.

`nc` Output:
```
Hello, world
```
At this point, our ClientPython program is still waiting to receive a response. Since `nc` waits to transmit input until it receives a newline, we need to type out the entire line we wish to send back at once. So directly after the text output by `nc`, we will type a response, then hit return:

`nc` Output with our Response:
```
Hello, worldThis is our typed response
```
This causes our client to print out the message received, along with the senders address and port:

ClientPython Output:
```
Starting client...
Received (from ('127.0.0.1', 12345)): b'This is our typed response\n'
```
While tracking `nc`'s input versus output might be a bit challenging to follow, our client correctly prints out the response we typed into `nc`.

Note that this example was done using the same computer for both the client and server. However as you know, unlike TCP, UDP does not guarantee delivery or ordering and may drop packets rather than retransmitting any missed. So if this test were done between a client and a server separated by an unreliable connection, the result might never arrive. When using UDP we need to either build in our own code for handling any missed or misordered packets, or only use UDP for situations where it is not important if some packets are dropped or if the data arrives in the correct order.

For the rest of this tutorial, we will be using TCP, since it works better for our use case, so let's restore the final line of the program to `start_client_simple()`.
