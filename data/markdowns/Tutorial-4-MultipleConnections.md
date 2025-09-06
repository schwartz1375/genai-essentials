# Handling Multiple Simultaneous Connections
Reference source file: `ServerPython.py`

## Multiple Simultaneous Connections Introduction
Most real-world servers need to be able to handle many different clients connecting at the same time. Let's try testing 2 connections at once with our server. This is hard since the client finishes and exits so quickly. One option would be to put a delay into the client program to make it easier. However, an easier choice is to just use `nc` again to connect.

First, let's start the server, as before:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, start a simulated client using `nc`:
```bash
nc 127.0.0.1 12345
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
```
The server correctly accepts the incoming connection from `nc` and prints its IP address and port. In this case, `nc` is running on the same local host loopback address as the server, and a high-number ephemeral port. Again, your output will probably show a different port number than the above example, since these ports are generated dynamically and can take different values. Note that you can pass `localhost` as the network address or `127.0.0.1` and it will have the same result. `socket.connect()` and similar calls will automatically resolve the domain names such as `localhost` to the proper IP address (in this case `127.0.0.1`).

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

So far so good. We did all this before in an earlier example. However, this time instead of closing `nc`'s connection, let's try adding an additional client while the `nc` "client" is still connected to the server.

In another tab/window/terminal, launch the client:
```bash
python3 ClientPython.py
```
Note that ServerPython will not output anything. It is still handling the connection from `nc`, so it will not accept a new connection until the original one is terminated.

If we kill the `nc` program, we will then see the expected output on the server, as the new ClientPython connection is allowed to connect after `nc`'s connection is terminated:

ServerPython Output:
```
Received new connection from  ('127.0.0.1', 64073)
Received: b'Hello, world'
```
So how do we fix this? While handling one connection at a time makes thing simpler, a server isn't very useful for most real-world situations if it can only handle one client connecting at a time and it makes all other clients wait. Imagine if Google did this; it could take hours or even days for it to be our turn to perform a search.

There are several ways to solve this problem. One of the more straightforward solutions in Python is to use threads.

## Multithreading
In Python, threading allows for the execution of multiple operations at once within a single process.

A thread is a separate flow of execution. This means that your program will have two or more things happening at once. For most Python implementations, the different threads do not actually execute at the same time, they merely appear to, and the computer is actually rapidly switching between executing the different threads. Some operating system-level thread implementations will instead offload each thread onto a separate core on a multicore processor, which means the threads are truly executing at the same time on different cores of the processor.

Threads are lighter in terms of resource usage than processes, and share the same memory space, which facilitates data sharing. This can lead to problems due to simultaneous access of data (known as a race condition). To prevent race conditions, threading provides a number of synchronization primitives including locks, condition variables, and others which will be discussed later.

For now, let's define a new function to replace `handle_new_connections_simple()` with a version using threads:
```python
def handle_new_connections_threads(sock):
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
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()
```
This function is almost identical to the `handle_new_connections_simple()` version, except we replaced the final line that called `handle_client(conn)` with 2 lines involving threads.

The first of these uses the `threading` module member function `.Thread()` to create a new thread and stores the result in a new local variable we call, appropriately enough, `thread`. `threading.Thread()` can take many arguments to specify particular thread attributes and behavior, but we only care about 2 of them, so we specify the names of the parameters we care about, `target` and `args`. The `target` parameter to `threading.Thread()` specifies the function that the thread will execute when started, in this case `handle_client()`. By default, Python threads will not start execution until you call their `.start()` method function, which occurs on the following line. Since a Python thread is also an object, it contains many useful member functions like `.start()`.

We also specify the `args` parameter to `threading.Thread()`, which is a *tuple* that contains the arguments to the `handle_client()` function we specified as the `target` parameter. It could be empty (or we could just leave out the parameter) if `handle_client()` had no arguments. However, `handle_client()` has exactly one argument. Because of this, instead of providing the parameter `args=(conn)`, which the Python interpreter would internally simplify to `args=conn` like it normally does with parentheses, we need to put at least one comma in the parentheses to show Python that it is a *tuple*, so we write `args=(conn,)`. While this may look a bit strange, we are essentially saying that this is a *tuple* with only one element (the second element is blank/non-existent, so there is nothing after the comma). This forces Python to keep this parameter as a *tuple*, which then has its elements mapped to the parameters of `handle_client()`. If we instead just passed `conn` directly without a *tuple*, the program would fail because Python does not know how to map a *socket* object to the parameters of a function, only how to map *tuples* to function parameter lists. A *tuple* with only a single element is sometimes also known as a *singleton tuple*, however this is not to be confused with a *singleton object/class/design pattern* which we will cover later.

Looking again at the above code, `handle_new_connections_threads()` will loop forever `while True`, calling `sock.accept()` to wait for a new incoming connection each time, just as before. The difference is that `handle_new_connections_simple()` would immediately handle each new incoming connection by calling `handle_client()` directly, which blocked any additional connections until `handle_client()` returned. Instead, `handle_new_connections_threads()` creates and then starts a new *thread* for *each* new incoming connection, which takes almost no time at all, then goes back to listening for more new connections by calling `sock.accept()` again at the next iteration through the `while` loop. Meanwhile, *each* newly created *thread* in turn calls `handle_client()` for that thread's incoming connection, allowing both the main (listening) thread and all the threads created for each successive incoming connection to all run *at approximately the same time*. There is no noticeable delay in this process, so nobody has to really wait on anyone else. This allows the threaded version of the server to handle many clients all at once, instead of one at a time.

Note that `handle_client()` is a *local* function to the new `handle_new_connections_threads()` function. The old `handle_new_connections_simple()` function also has its own *local* `handle_client()` function. While in this case the code for both functions is identical, each `handle_new_connections_` function calls its own *local* version of `handle_client()`. This allows each one to be customized for its particular use case, despite them both having the same name. If we wanted to, we could instead remove these 2 *local* `handle_client()` functions and have a *global* `handle_client()` function instead in the main body of the code. In that case, every function that called `handle_client()` would be calling the same code, and there would only be one version of the function to maintain.

Finally, we need to change the `start_server()` function to call `handle_new_connections_threads()` instead of `handle_new_connections_simple()`:
```python
def start_server():
    listen_socket = initialize_server_socket()
    # handle_new_connections_simple(listen_socket)
    handle_new_connections_threads(listen_socket)
```
Rather than just changing the function name, we will comment the old line out and add a new one. This way, we can easily switch back between non-threaded and threaded modes for testing.

Now, let's try running the revised server program:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, again start a simulated client using `nc`:
```bash
nc 127.0.0.1 12345
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
```
Next, let's type some input into `nc` to send to the server:
```bash
Hello
```
ServerPython Output:
```
Received: b'Hello\n'
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
Even though the `nc` "client" is still connected to the server, the server properly handles the ClientPython program's connection, echos back the data, and ClientPython completes and exits, all while `nc` is still connected to the server.

To validate that `nc` is still connected, we can send additional data through `nc`'s connection by typing additional lines into the `nc` program:
```
Still here!
```
ServerPython Output:
```
Received: b'Still here!\n'
```
Note that the server does not show any new connections occurring, it simply prints the message we just sent from `nc`, showing that `nc` was still connected to the server the entire time.

## Race Conditions
Now we will add a feature to track the total number of messages received from the clients.

To do this, we will add code in the `while True` loop of the `handle_client()` function after printing the data received, to both increment the variable `messageCounter` and print a running total of the number of messages received. We do this by setting the _local variable_ `nextCount` to the number after the current value of `messageCounter`, then setting `messageCounter` to that new value. We insert a delay in the middle of this process to simulate some network latency, using `threading.Event().wait(0.1)`, a function provided by the `threading` module that pauses the thread for the indicated number of seconds (in this case, 0.1 seconds):
```python
    def handle_client(conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received:', data)
            nextCount = messageCounter + 1
            threading.Event().wait(0.1)
            messageCounter = nextCount
            print('Total messages received:', messageCounter)
            conn.sendall(data)
        conn.close()
```
`messageCounter` will be a _global variable_, so that it can be accessed by any thread or function, so we also need to initialize `messageCounter` to zero at the beginning of the source file, with our other global initializations:
```python
SERVER_NAME = 'localhost'
SERVER_PORT = 12345
messageCounter = 0
```
In this case, we use a different format for the variable name to indiciate that this variable may change regularly during the program, but this is a stylistic decision, rather than a Python rule.

Now let's try testing the new program:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, start the client:
```bash
python3 ClientPython.py
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.9/threading.py", line 973, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.9/threading.py", line 910, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/linuxexamples/basic/ServerPython.py", line 57, in handle_client
    messageCounter += 1
UnboundLocalError: local variable 'messageCounter' referenced before assignment
```
As with all _Exceptions_, your output may vary slightly, especially with regard to file paths and line numbers.

What happened here? By default if you set a variable inside of a function, Python assumes you want it to be a _local variable_ to that function. Since we want to modify this _global variable_, rather than a local variable named `messageCounter` inside of the `handle_client()` function, we need to tell Python inside that function that any references to `messageCounter` refer to the _global variable_ rather than a _local_ one with the same name.

To do this, we _declare_ the variable in the `handle_client()` function we modify it in. This ensures that Python treats it as a _global variable_ rather than a _local variable_. For organizational and readability purposes, we put this declaration at the top of the function, but it can appear anywhere in the function, as long as it is before it is used.
```python
def handle_client(conn):
    global messageCounter
```

Now when we test it, we get a more expected output:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, start the client:
```bash
python3 ClientPython.py
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
```

To better explore issues with simultaneously executing code, let's run the client continuously 100 times in a row.

On Unix-like operating systems with `bash` or a similar shell, we can do this using some simple shell code on the command line:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```

On Windows, we can create a `.bat` file, for example `script.bat`:
```bat
@echo off
for /L %%i in (1,1,100) do (
   python ClientPython.py
)
```
we then can execute this `script.bat` program. The examples below will use the Unix/`bash` script syntax, but we can substitute this Windows `script.bat` file for this line, if running on Windows.

```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49842)
Received: b'Hello, world'
Total messages received: 100
```
While the output is quite lengthy, the important thing to note is that at the end, the server correctly reports that 100 messages were received.

Now, let's try running two of these 100-client sequences at the same time.
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
Now quickly, in yet another tab/window/terminal, run the another set of clients 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49942)
Received: b'Hello, world'
Total messages received: 109
```
The exact number of messages reported at the end may vary, but notice that it is far less than the 200 that should be reported. If we look back at the output, we will see numerous cases where the same number of total messages received is reported twice.

Since two connections to the server are often occurring simultaneously, two instances of the `handle_client()` function are executing at the same time. This means that sometimes, Thread 1 might execute the first 2 lines below, but then Thread 2 might execute at last the first line, before Thread 1 finishes the last line:
```python
            nextCount = messageCounter + 1
            threading.Event().wait(0.1)
            messageCounter = nextCount
```
For example, if messageCounter is zero, the following sequence of events might occur in this order:
```
messageCounter = 0
Thread 1: nextCount[Thread 1] = ((messageCounter=0) + 1) = 1
Thread 1: wait 0.1 seconds
Thread 2: nextCount[Thread 2] = ((messageCounter=0) + 1) = 1
(Thread 1 is still in its 0.1 seconds of waiting here...)
Thread 2: wait 0.1 seconds
Thread 1: messageCounter = nextCount[Thread 1] = 1
Thread 2: messageCounter = nextCount[Thread 2] = 1
```
Since `nextCount` is a _local variable_, each thread has its own version of `nextCount`, so there is no conflict. However, since both threads use the same _global variable_ `messageCounter`, in this case they can both end up trying to update it at the same time, which creates what is known as a _race condition_, a condition when multiple code paths executing at the same time might finish in a different order than expected, which can cause bugs and security issues due to unanticipated behavior.

While the 0.1 second delay added makes this problem far more obvious, even if we removed this delay the problem would still occasionally occur (although it might be far less frequent and more difficult to spot). It is worth noting that even removing the `nextCount` variable entirely and replacing it and the delay with `messageCounter = messageCounter + 1` does not solve this problem, since it is still possible for one thread to load and increment messageCounter after the other thread has loaded the initial value of messageCounter, but before it is able to store the incremented value. Operations like this that can be interrupted by another thread, are called _non-atomic_ operations.

The most common (CPython) implementations of Python guarantee that certain Python operations, such as basic assignment (`x = 5`) and list appending (`l.append(4)`) are atomic, meaning that they cannot be interrupted before completion by another thread, so they cannot result in these race conditions on their own. However, since alternative Python implementations may not guarantee the same atomicity of operations, best practices are normally to use thread synchronization techniques such as _locks_ even on operations that are atomic in CPython.

## Locks
The simplest way to deal with this sort of _race condition_ is to use a _lock_ around the critical section of code. A _lock_ is a synchronization primitive used in multithreading to ensure that only one thread can access a particular section of code or a shared resource at a time. In this case, we will create a new _global variable_ `messageCounterLock` to prevent more than one thread from accessing the global variable `messageCounter` at the same time, and initialize it with the other global variables at the beginning of the program:
```python
messageCounterLock = threading.Lock()
```
This requests a new _lock_ from the `threading` module and stores it in the _global variable_ `messageCounterLock`.

To prevent more than one thread from accessing the global variable `messageCounter` at the same time, we modify the section of the `handle_new_connections_threads()` function where `messageCounter` is used:
```python
            messageCounterLock.acquire()
            nextCount = messageCounter + 1
            threading.Event().wait(0.1)
            messageCounter = nextCount
            messageCounterLock.release()
```
Before we first access `messageCounter`, we acquire the _lock_ with the _lock_ member function `.acquire()`. This pauses or "blocks" the thread until the _lock_ `messageCounterLock` can be acquired for our thread's exclusive use. We then can access and increment `messageCounter` without any worry that another thread will modify it out from under us, since we know that no other thread can have this _lock_ until we release it. Once we have finished incrementing `messageCounter`, we then release the _lock_ with the _lock_ member function `.release()`, which allows other threads to acquire the lock again.

Python allows a simplified syntax for locking these critical code sections by using the `with` keyword:
```python
            with messageCounterLock:
                nextCount = messageCounter + 1
                threading.Event().wait(0.1)
                messageCounter = nextCount
```
This acquires the _lock_ `messageCounterLock` automatically before executing the code underneath and releases the _lock_ automatically when that code is exited or finished. Using `with` for locking is generally preferred in Python, because it saves us from having to remember to `release` the _lock_. If we forget to `release` the _lock_ when we are finished, it can cause a _deadlock_ situation, where other threads are waiting on the _lock_ forever because it is never released, bringing program execution to a halt. In addition, using `with` to manage the _lock_ automatically handles error situations, such as _Exceptions_ (which we will cover later) or a thread unexpectedly exiting, by automatically releasing the _lock_ gracefully when those situations occur.

Let's test out new locking code out:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
Now quickly, in yet another tab/window/terminal, run the another set of clients 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49942)
Received: b'Hello, world'
Total messages received: 200
```
The _lock_ ensures that only on thread increments the message counter at a time, so the final total is correct.

## Condition Variables
_locks_ are very useful as a simple tools for thread synchronization to prevent _race conditions_. However, if a thread needs to access a variable that is changed inside of a _lock_, it may end up spending a lot of time acquiring the _lock_ just to check the value. Each time it does, all the other threads that use it will end up waiting on that _lock_ to be released, which can significantly impact performance over time. In addition, _deadlock_ can occur due to faulty program logic if there is a situation where 2 threads end up waiting on each other indefinitely for a certain circumstance to occur (such as a variable having a certain value), with neither moving ahead to cause that circumstance because they are both waiting on the other indefintely.

To address both the performance issues of _locks_ along with certain potential _deadlock_ situations, Python also provides _condition variables_ in the `threading` module. _condition variables_ allow a thread to wait (aka block) until a certain condition is met, instead of having to constantly acquire and release a _lock_ just to check to see if a variable has reached a certain value.

For example, say we want to print out a special message when the `messageCounter` hits 100, so we create a new thread just to handle this message. With the _locks_ implemented above, this special message thread would need to wait on the _lock_ being available every time it checked:
```python
    def notify_100():
        while True:
            with messageCounterLock:
                if messageCounter >= 100:
                    print('*** 100 messages received ***')
                    return  # Exit the thread

    notifyThread = threading.Thread(target=notify_100)
    notifyThread.start()
```
We add this function right before the main `while True` loop of the `handle_new_connections_threads()` function. We also add the code before that loop to create the new `notifyThread` and start it.

Note that by acquiring `messageCounterLock` using the `with` keyword, we do not have to manually release it. If we instead manually got the _lock_ through `.acquire()`, it would be very easy to forget to `.release()` the _lock_ before calling `return`, since it occurs in the middle of the function, rather than at the end (where a `.release()` would also be needed). This could result in _deadlock_, since no other thread would ever be able to acquire the _lock_ if we don't release it before exiting the `notify_100()` function.

Not only is this thread itself using CPU resources to continuously iterate through the above loop, but every time it acquires the _lock_, it also blocks all other threads from executing their _lock_-protected code segment, which slows down the rest of the program as well. The astute reader will note that since we know that `messageCounterLock` is strictly increasing, and since `notify_100()` does not need to modify `messageCounterLock`, we _could_ just not acquire the lock at all, and instead continually check to see if `messageCounterLock` has reached 100, without creating a _race condition_. While this is true in this particular circumstance, it will not always be the case, and many times a _lock_ will be needed. In addition, even just looping constantly without a lock will still consume some CPU resources.

To avoid these performance losses, we instead use a _condition variable_. First, we need to initialize it at the top of the source file with the other global variables:
```python
condition = threading.Condition()
```
This uses the `threading` module method function `threading.Condition()` to request a new _condition variable_, and stores it in the _global variable_ `condition`.

Then, we will modify the `notify_100()` function to wait on the new _condition variable_ before checking if the value of `messageCounter` has reached 100:
```python
    def notify_100():
        with condition:
            condition.wait()
            if messageCounter >= 100:
                print('*** 100 messages received ***')
            else:
                print('Error: notify_100() called before 100 messages received')
```
First, `notify_100()` must acquire (and later release) the _condition variable_ `condition`, much like a _lock_ must be acquired, before the related code can be executed. We again use the `with` keyword so that Python automatically acquires and releases `condition` for the code segment underneath it. Then, the function waits on `condition` to be triggered by calling the `condition` member function `.wait()`. Note that the function must have acquired `condition` before it can call `condition.wait()`, or else errors could occur. `condition.wait()` will block this thread until `condition` has been notified that `messageCounter` has reached 100. It will then resume executing as soon as it can re-acquire `condition`, print the special message, and exit. Why then do we check to see if `messageCounter` >= 100? Well, we don't technically have to in this case, but it's a good idea as a safety precaution, to make sure `condition` has really occurred. Sometimes bugs occur when a notification might happen incorrectly, and this extra check makes our code more robust against those kinds of bugs. If `condition` has not been met and the check fails, we want to display an error message, so we use the `else` keyword to define what lines of code are executed if the `if` condition is false (i.e. `messageCounter` has not reached 100). If `messageCounter` >= 100, the line under the `if` will be executed and the special message will be displayed. If `messageCounter` < 100, the lines under the `else` will be executed instead, and the error message will be displayed.

Finally, we need to actual notify our `notifyThread` when the condition has been reached. To do this, we add the following code to the `handle_client()` function inside the locked section of code:
```python
            with messageCounterLock:
                nextCount = messageCounter + 1
                threading.Event().wait(0.1)
                messageCounter = nextCount
                if messageCounter == 100:
                    with condition:
                        condition.notify_all()
```
if `messageCounter` is 100, then it will acquire `condition`, then notify it that the condition has been met, which will cause `notifyThread` to continue execution (after `handle_client()` releases `condition`, which happens automatically due to the last `with` clause).

We can verify that our new code is working:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
Now quickly, in yet another tab/window/terminal, run the another set of clients 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49842)
Received: b'Hello, world'
Total messages received: 100
*** 100 messages received ***
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49942)
Received: b'Hello, world'
Total messages received: 200
```
Instead of constantly acquiring and releasing a _lock_, the `notifyThread` now waits until it is notified that `messageCounter` is 100, allowing other threads to continue unimpeded.

## Select
As we can see, threading is a powerful tool, and can be straightforward to use in many circumstances. However, in other cases, with many interacting _threads_ and _locks_ it can also get quite complicated and confusing to prevent _race conditions_ and _deadlock_. In addition, the overhead of creating and releasing many _threads_ and _locks_ all of the time can impede a program's performance. For example, if a million clients were all connecting to the server at once, our server would need a million threads.

To deal with these issues, sometimes an alternative method for handling many simultaneous connections is preferable. One such method uses a feature known as `select`. Rather than running each connection in its own thread, `select` allows us to use a single thread to handle multiple connections by checking the status of each socket and performing the necessary operations, in rapid succession. The `select.select()` function itself checks multiple file descriptors (which are in this case, sockets that hold the various connections to clients) to see if they are ready for IO (Input/Output) operations. We can then quickly act on only those sockets that have data to receive or send immediately, and then go back to checking for new socket activity without a noticable delay. While this approach only allows us to do one thing at a time, we can process this data quickly enough that it _seems_ like we are doing multiple things at once, since we don't have to block execution to wait on data from the network. The approach also falls under the category of `non-blocking IO`, since there is no blocking of program execution while we are waiting to send or receive data.

To use Python's `select` functionality, we need to first include the `select` module at the top of the source code. We also will need the `queue` module in a minute, so let's include that as well here:

```python
import select
import queue
```

To implement a version of `handle_new_connections` using `select`, we will define a new function `handle_new_connections_select()`, which takes a socket `sock` as an argument, just like the `handle_new_connections_simple()` and `handle_new_connections_threads()` functions:
```python
def handle_new_connections_select(sock):
    global messageCounter
    
    inputs = [sock]
    outputs = []
    message_queues = {}
```
As before, we need to tell Python that any references to `messageCounter` within this function are referring to the _global variable_, not a similarly named _local variable_. We are also going to track 3 primary local variables in this function, which are initialized here. The first variable `inputs` is a list that contains all of the sockets we which to monitor the inputs of, that is, sockets that we want to read data from. Since the server starts with a listening socket, but no clients connected, the list `inputs` is initialized to only contain the listening socket passed into the function as `sock` at first. The second variable `outputs` is a list that contains all of the sockets we which to monitor the outputs of, that is, sockets that we want to write data to. Since the server starts without any clients connected, the list `outputs` is initialized to an empty list. The third variable `message_queues` is a _dictionary_ used to map each socket to a queue of messages (data) to be sent through that socket. Since we do not start with any queued messages, `message_queues` is initialized to an empty _dictionary_ with the `{}` operator. A _dictionary_ is sort of like a _list_, except that instead of consisting of items ordered by an index number (0, 1, 2, ...), it consists of essentially unordered items accessed by _keys_. When we insert items into a _list_, their index is determined by what order they are placed in. When we insert items into a _dictionary_, we provide a _key:value_ pair, for example if we wanted to keep track of people's bank balances we might use `myDictionary = { "Alice": 5000, "Bob": 3000 }`. We use braces when defining a _dictionary_ instead of brackets, which define a _list_. When we want to access a specific item in the _dictionary_, we instead use brackets just as we do with a _list_, but we use the item's _key_ instead of an index number (e.g. `myDictionary["Bob"]` will equal `3000`). Thus we could have also declared `myDictionary` as:
```python
myDictionary = {}
myDictionary["Alice"] = 5000
myDictionary["Bob"] = 3000
```
A Python _dictionary_ is also an implementation of a _hash table_, which we will explore more in a later tutorial. In the `message_queues` _dictionary_, the _keys_ will be the sockets, and the _values_ will be the corresponding message queues.

Now that we have initialized these variables, we create a `while` loop that will continue as long as there are sockets on which we are interested in receiving data (i.e. as long as the list `inputs` is not empty). Since `inputs` will contain at least the listening socket for as long as the server is operational, this loop will continue as long as the server is running. Each iteration through this loop, we call `select.select()` to see if there are any sockets with data available for reading or writing, and if there are any sockets which encounter socket exceptions, which are unexpected behavior (usually errors). We pass a list of the sockets we want to check for each of these 3 states as the 3 respective arguments to `select.select()`. We can use the same list `inputs` both to check for data available for reading in the first argument and to check for socket exceptions in the third argument, since we will not put any sockets in the list `outputs` unless they are also in the list `inputs`, so including `outputs` in the third argument would be redundant.
```python
    while inputs:
        results = select.select(inputs, outputs, inputs)
        readable = results[0]
        writable = results[1]
        exceptional = results[2]
```
`select.select()` returns a _multi-dimensional list_, which we store in the _local variable_ `results`. A _multi-dimensional list_ is essential a list of lists for a 2-dimensional list, a list of lists of lists for a 3-dimensional list, and so on. In this case, `results` is a 2-dimensional list, where each of the 3 elements of the list `results` is itself a list. To make it easier to work with this output, we assign each one of the 3 lists contained in `results` to new _local variables_. The first element (at index 0) of `results` contains a list of any sockets ready for reading data from, so is stored in the _local variable_ `readable`. The second element (at index 1) of `results` contains a list of any sockets ready for writing data to, so is stored in the _local variable_ `writable`.  The third element (at index 2) of `results` contains a list of any sockets that have socket exceptions (an error or a closed connection), so is stored in the _local variable_ `exceptional`. Note that these 3 new _local variables_ are defined purely for readability and convienence. We could instead directly access all of the elements of all 3 lists from the `results` variable if wished. For example, to access the second element in the `readable` list, we could type `results[0][1]`, which would specify the second element (which is at index 1) in the first (at index 0) list in `results`. We could also just write `results[0]` instead of `readable`. However, both of these methods would make our code harder to understand and follow, so we store the lists contained in `results` in their own _local variables_ instead.

We can also take advantage of the multiple-outputs notation we learned previously to simplify this code and instead write:
```python
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
```
This is often simpler than dealing with multi-dimensional arrays.

Once we get the results of `select.select()`, we need to act on any sockets that are ready. For each of the 3 lists of ready sockets returned (`readable`, `writable`, and `exceptional`), we will use a `for` loop to iterate through each item in the respective list. Let's start with `readable`:
```python
        for s in readable:
            if s is sock:
                conn, addr = s.accept()
                print("Received new connection from ", addr)
                inputs.append(conn)
                message_queues[conn] = queue.Queue()
```
For each item that `select.select()` returned in the `readable` list, we assign that item to the variable `s` in the `for` loop, then check to if `s` is our listening socket `sock`. If it is, we have a new client connection, so we call `s.accept()` to create a new socket for this new client, and store it in the _local variable_ `conn`, much as we did before. We then add this new socket `conn` to the `inputs` list, so that `select.select()` will check for any data or socket exceptions on it, when next we pass `inputs` as an argument to `.select()`. We also create a new `Queue` to contain any messages we want to send over this connection, and store this `Queue` in the _dictionary_ `message_queues` under the _key_ `conn`.

A `Queue` is somewhat like a _list_ except that it is designed to follow the First-In-First-Out (FIFO) principle, meaning that the first element added to the queue will be the first one to be removed as well. We can also think of it as new items being added to the end of the queue, while items retreived are removed from the front of the queue. The `queue` module in Python provides a `Queue` class that we can obtain (initially empty) by calling `queue.Queue()`. We will explore queue data structures in more detail in a later tutorial.

It should also be noted that Python's `Queue` implementation is _thread-safe_, meaning that it uses various internal concurrency mechanisms (such as _locks_) to guarantee that it will work properly even if multiple threads are using a `Queue` at the same time, as long as we use it in a way consistent with its documentation. However, since our current function is single-threaded, we are not really taking advantage of this feature of `Queue`.

If the current item `s` from the `readable` list is not our listening socket `sock`, then we know that it must be one of the sockets assigned to a connecting client. The code below occurs underneath an `else` clause in order to only execute in this situation:
```python
            else:
                data = s.recv(1024)
```
We call `s.recv()` on the client socket `s` in order to retrieve data from that client. We know that there is data ready for reading immediately, since it was in the `readable` list returned from `select.select()`, so this line will execute quickly, without blocking execution. If we did not have the benefit of `select` and had called `s.recv()`, there would be a chance there would be no data immediately available for reading on this client socket, which would cause the entire program to wait and block further execution until data was available or the socket disconnected. `select` allows us to prevent this blocking delay, without using `threading`.

Once we receive data and store it in the _local variable_ `data`, we need to check if it is empty or not. When the socket member function `.recv()` returns without error, but no data is returned, this means the connection was terminated because the socket was closed (by the client), and therefore there is no more data to receive. This will not occur at any other time, since while the connection is open, `.recv()` will wait for at least 1 byte of data before returning. Therefore, if the _local variable_ `data` is anything but zero, we will print it out, then increment `messageCounter` and print its new total out. Note that it is possible `data` may be non-zero because it contains one of more bytes of data, but those bytes themselves are all zeros (e.g. `data` is `b'\0'`). That would still be at least 1 byte of data, so the _local variable_ `data` itself would still resolve to `True`, and execute the below code:
```python
                if data:
                    print('Received:', data)
                    nextCount = messageCounter + 1
                    messageCounter = nextCount
                    print('Total messages received:', messageCounter)
```
We then need to store the received `data` to be echoed back to the client later. Note that we cannot simply call `.sendall()` to send the data back immediately like we did in our original code, because the client socket `s` might not be ready to send data, and if it is not, calling `.sendall()` will cause it to wait and block execution of the entire program until the socket is ready to send data. Therefore, we instead put it into `message_queues[s]`, that is, the `Queue` that was stored in the _dictionary_ `message_queues` with the _key_ contained in the variable `s` (e.g. the client socket itself). `Queue` provides a member function `.put()` to do this.
```python
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
```
We then need to wait until the client socket `s` is ready to write data before sending it. To do this, we again rely on `select` by adding `s` to the `outputs` list passed to future calls to `select.select()`, if it is not already in that list. This ensures that `s.send()` is not called on the client socket until it is ready to send data and `select.select()` returns `s` in the `writable` list, avoiding blocking.
 
Otherwise, we will use an `else` clause to handle the situation where `data` is empty:
```python
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]
```
If zero bytes were received (`data` is `False`), but no error was returned by `s.recv()`, then the client closed the connection. In this case, we need to remove the closed client socket `s` from the `outputs` list, if it is in that list, and we also need to remove it from the `inputs` list (which we know if is in), before closing the socket with `s.close()`. This ensures that future calls to `select.select()` will never contain `s`, as trying to read or write to a closed socket can result in various errors. We also need to remove the `Queue` corresponding to `s` from the _dictionary_ `message_queues`. If we do not, it could end up using unnecessary memory. Little bits of memory left dangling can add up over time, causing _memory leaks_ that can seriously degrade performance over time or even crash a program. The `del` keyword removes the indicated _dictionary_ entry from the _dictionary_, in this case, the `Queue` stored at `message_queues[s]`.

Now that we have handled all the sockets with data waiting to be read from, we will handle those that are ready to send data, using a `for` loop over the `writable` list of sockets returned by `select.select()`:
```python
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                sent = s.send(next_msg)
```
Inside the `for` loop, the code attempts to retrieve the next message to be sent through the client socket `s` from the `Queue` stored in the _dictionary_ `message_queues` for that socket, `message_queues[s]`. The `Queue` member function `.get_nowait()` retrieves the first item in the `Queue` (also removing it and storing it in the variable `next_msg`) if this can be done without blocking program execution. Why would retrieving an item from a `Queue` block execution? This will happen if we try to retrieve an item from an empty `Queue` using the `Queue` member function `.get()`, as that *will* block until an item has been added or until a timeout occurs. Since we do not want to block program execution (which would freeze out all the other client connections), we instead use the `.get_nowait()` version to retrieve the first item from the `Queue`. If we call `.get_nowait()` on an empty `Queue`, instead of blocking program execution, it will "throw" or "raise" a Python _exception_ (which is a separate Python-specific language concept from the socket exceptions in the `exceptional` list provided by `select.select()`). This particular Python _exception_ thrown is called `queue.Empty`, as it is provided by the `queue` module.

A Python _exception_ is an unexpected condition (often an error) that occurs during execution of Python code. These errors, if not handled, will generally cause Python programs to crash, resulting in traceback output like what we saw when we neglected to include the `global messageCounter` declaration earlier in this tutorial.

This code uses the keyword `try` to tell Python that if a Python _exception_ (we will hereafter refer to Python _exceptions_ simply as _exceptions_, and socket exceptions specifically as "socket exceptions" to differentiate the two concepts) occurs while inside the `try` clause, instead of crashing the program, Python should first look for the `except` keyword and if the condition after `except` keyword matches the _exception_ type, execute the code in that `except` clause, instead of crashing. In this example, if an _exception_ occurs during the line `next_msg = message_queues[s].get_nowait()`, Python will check to see if the _exception_ is of type `queue.Empty`, and if so, will execute the line inside the `except` clause. In this case, the only _exception_ that generally will occur inside our `try` clause will indeed be a `queue.Empty` _exception_, so instead of crashing, Python will execute `outputs.remove(s)`, which will remove the client socket `s` from the `outputs` list, preventing future iterations of this `select` loop from trying to write to client socket `s` when there is no data in `message_queues[s]` to write for this socket. Decreasing the size of the `outputs` list in this way also increases the speed of future calls to `select.select()`. Of course, if new data is queued for client socket `s` in the future, it will also be added back to the `outputs` list so it can write that data.

There is also an `else:` clause directly in line with the `try` and `except` clauses. This executes the code under it if the `except` clause does not execute and if there are no _exceptions_. For example, if `message_queues[s].get_nowait()` successfully retrieves an item from the `Queue` because it was not empty, the `else:` clause will execute. This allows the retrieved data in the variable `next_msg` to be sent the the client using `s.send(next_msg)`, and stores the result (the number of bytes actually sent) in the _local variable_ `sent`. Since `select.select()` already told us that client socket `s` was ready to send data, this will NOT result in blocking the entire program while waiting to send data. Note however that we use the socket member function `.send()` rather than `.sendall()` as we did before. This is because `.send()` will attempt to send whatever it can. It can still block if the socket's send buffer is full, so it is important to wait until `select.select()` indicates it is ready. However, in some cases `.send()` might only result in part of the data being sent immediately. On the other hand, `.sendall()` will block as needed until *all* of the data passed to it has been sent. Even if `select.select()` indicates that the socket is currently available to send data, this does not mean that the entire message can be sent completely right now, so if only a partial send happens, `.sendall()` may wait and block execution until it is able to send the rest of the data, _even if_ the socket was available to send _some_ data immediately.

But what happens if `.send()` doesn't actually send all of the data we wanted? In this case, we need to make sure that the next data sent (before other messages) is whatever wasn't transmitting during the `.send()` call. We can compare its return value in the _local variable_ `sent` to the total length of `next_msg` to see if it was only partially sent. If this is true, we will _slice_ `next_msg` after the number of bytes actually sent, and store any untransmitted portion remaining in a _local variable_ `remaining_msg`. We will then put this back into the _queue_ `message_queues[s]`, except at the _front_ of the queue:
```python
                if sent < len(next_msg):
                    remaining_msg = next_msg[sent:]
                    # Put the remaining message back at the front of the queue
                    message_queues[s].queue.appendleft(remaining_msg)
```
Because we need to make sure the remaining part of `next_msg` gets sent before any other messages that may be in the queue, we have to add it to the front/beginning of the queue, rather than the end as queues normally work with `.put()`. This requires us to actually access one of the _queue_ `message_queues[s]`'s underlying data fields, which is also confusingly named `queue`, and call a special method of its named `.appendLeft()` to add something to the front of it, rather than at the end. So yes, Python's `queue` module has a object type `Queue` which itself has a data field named `queue`, which has a method `.appendLeft()`. While we don't normally access the data fields of Python objects like `Queue` directly, as it is normally simpler and safer and more consistent to use their class methods like `.put()`, it is necessary in this case since there is no class method of `Queue` that accomplishes what we need. The only other way to accomplish this would be to create a new queue with our `remaining_msg` added first, and then to remove all the elements of the old queue and put them in the new queue, in order, which is also not a bad approach, but might be slow.

Also note that many other variations of `try... except` constructs are possible in Python. For example, if the clause just said `except:` with no condition after it, it would match ALL _exceptions_ not previously matched, and not just `queue.Empty`. We can also have multiple `except X:` clauses, in which case the code under the appropriate type for the exception that occurred will execute. Most commonly, `try` and `except` clauses will not include an `else` clause, but sometimes will include a `finally` clause, which executes no matter what, whether or not an _exception_ occurs, which is useful for doing cleanup such as closing a socket or file. We will see a lot more examples of these constructs and their variations in future tutorials.

Next, we need to handle any sockets that socket exceptions occurred for (meaning there was probably an error triggered at the operating system or library level), using a `for` loop over the `exceptional` list of sockets returned by `select.select()`:
```python
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
```
Our strategy for handling any socket exceptions returned by `select.select()` is simply to close the offending socket. We first remove the socket `s` from the `inputs` list using `inputs.remove(s)`, to ensure the server no longer attempts to read from a socket that has encountered an error. We then check if the socket `s` is in the `outputs` list, if so, we removes it from the `outputs` list as well, so the server does not attempt to write to a socket that has encountered an error. Once we have ensured no future code will access the socket, we then call `s.close()` to close the connection. Since an error has occurred, this may fail or be unnecessary because the connection might already have been closed, but if the connection is still open we want to make sure we close it if possible, so that the other side realizes that it is no longer communicating with the server, and can move on. Then, we remove the socket's `Queue` from the _dictionary_ `message_queues` by using the `del` keyword, to free any memory being used to store queued up messages for the socket `s` and help prevent memory leaks.

It is worth noting that because our `handle_new_connections_select()` function's main loop is `while inputs`, if the server ever closes all the connections (including the listening socket for new connections, which would only close in case of an error), this loop will also cause the program to exit, since the list `inputs` would be empty.

Finally, we need to add our `handle_new_connections_select()` function to `start_server()`, and comment out the previous versions.
```python
def start_server():
    listen_socket = initialize_server_socket()
    # handle_new_connections_simple(listen_socket)
    # handle_new_connections_threads(listen_socket)
    handle_new_connections_select(listen_socket)
```
Let's make sure this works:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
Now quickly, in yet another tab/window/terminal, run the another set of clients 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49942)
Received: b'Hello, world'
Total messages received: 200
```
As we can see, the program correctly handles simultaneous client connections while avoiding _race conditions_ without using _locks_.

## Polling
`select` is a very useful tool in certain circumstances, but it can suffer some performance limitations with large numbers of sockets or file descriptors that result from its continual checking of a long list of sockets. `poll` does this more efficiently, and also supports a wider range of socket events than just reads and writes. However, `select` is more universally supported and portable. Fortunately, Python's `select` module also provides access to the system `poll` function through the poll object returned by `select.poll()`.
```python
def handle_new_connections_poll(sock):
    global messageCounter

    message_queues = {}
    fd_to_socket = {sock.fileno(): sock}
    timeout = 1000
```
We will therefore define a new `handle_new_connections_poll()` function, which will initialize a `message_queues` _dictionary_ as before, as well as initialize a _local variable_ `timeout` variable to 1000, which will be used to tell `.poll()` not to wait more than 1000ms (or 1 second) before returning. As before, we need to use the `global` keyword to tell Python that any references to `messageCounter` within this function are referring to the _global variable_, not a similarly named _local variable_. We also create a _dictionary_ `fd_to_socket` to keep track of the mappings bewteen file descriptors (which are integers) and their corresponding socket objects, because `.poll()` only reports the file descriptor numbers when events occur, rather than providing the actual socket objects. We initialize `fd_to_socket` to contain the _key:value_ pair `sock.fileno(): sock` to start, that is the _key_ is the file descriptor number of the listening socket passed into our function as `sock`, and the _value_ is that listening socket object itself.

Next, we assign the `select.poll()` function (which returns a pollng object) to a _local variable_ `poller` to make it easier to use and read:
```python
    poller = select.poll()
    poller.register(sock, select.POLLIN)
```
We also use `poller`'s `.register()` member function to register our server's listening socket with the poll object `poller` so that future calls to `poller.poll()` will monitor this socket for incoming data.

Next, we loop forever with a `while True` loop, calling `poller.poll()` with a 1000ms timeout value to check for activity on all registered sockets. This will block for up to 1000ms or until at least one registered socket is ready to process IO activity:
```python
    while True:
        events = poller.poll(timeout)
        for fd, flag in events:
            s = fd_to_socket[fd]
```
The result of `poller.poll()` is a list of _tuples_ in the format `(FILE_DESCRIPTOR, EVENT_FLAG)`. We therefore use a `for` loop to iterate through this `events` list. In each iteration, we retrieve the socket corresponding to the file descriptor number in the _tuple_, using the `fd_to_socket` _dictionary_, and storing the resulting socket in the _local variable_ `s`.

The `flag` variable contains the event flags from the same tuple as the socket `s`. These event flags are a series of binary values where each bit corresponds to a different piece of information about activity on that socket, which can be tested by bitwise-ANDing `flag` with the appropriate _bitmask_. For example, the bit corresponding to the _bitmask_ `0b00000001` will be set if there is data on the socket ready for reading (which is provided by the `select` module as `select.POLLIN`) and the bit corresponding to the _bitmask_ `0b00000100` will be set if there is data on the socket ready for writing (which is provided by the `select` module as `select.POLLOUT`). If `s` is only ready to read data from, then `flag` (in big-endian notation) would be `0b00000001`. If `s` is ready both both immediately reading and writing data, both _bitmasks_ would be present and `flag` would therefore equal `0b00000101`. In the latter case, both `(flag & select.POLLIN)` and `(flag & select.POLLOUT)` would be `True`. There are also additional event flag _bitmasks_ such as `select.POLLPRI` (which indicates that `s` not only has data ready for reading but that it was marked "urgent") and `select.POLLERR` (which indicates that some sort of error occurred, much like the "socket exceptions" provided by `select.select()`).

First, we will check to see if `flag` indicates the socket `s` has data ready for reading, by checking it against both `select.POLLIN` and `select.POLLPRI`:
```python
            if flag & (select.POLLIN | select.POLLPRI):
                if s is sock:
                    conn, addr = s.accept()
                    print("Received new connection from ", addr)
                    # conn = setup_ssl(conn)
                    fd_to_socket[conn.fileno()] = conn
                    poller.register(conn, select.POLLIN)
                    message_queues[conn] = queue.Queue()
```
If `s` has data available for reading, we again check to see if it is the listening socket for new connections passed into this function as `sock`. If it is, we again use `s.accept()` to establish a new connection, assigned to a new socket `conn`. We then need to find our new `conn`'s file descriptor number so that we can store it, along with `conn` itself in the _dictionary_ `fd_to_socket` for later lookup. Next, we register our new `conn` socket using `poller.register()` to be sure future calls to `.poll()` notify us when `conn` has data ready for reading. The first argument to `poller.register()` is the socket we wish to monitor, and the second argument is the _bitmask_ (or combinations of _bitmasks_ together) of the event(s) we want to monitor for that socket, in this case just `select.POLLIN`. Additionally, just as with `select.select()`, we use `queue.Queue()` to create a new message `Queue` for `conn` and store it in the `message_queues` _dictionary_.

If `s` is not our listening socket `sock`, then it is a client socket connected to us, so we execute the code in the `else` clause:
```python
                else:
                    data = s.recv(1024)
                    if data:
                        print('Received:', data)
                        nextCount = messageCounter + 1
                        messageCounter = nextCount
                        print('Total messages received:', messageCounter)
                        message_queues[s].put(data)
                        poller.modify(s, select.POLLIN & select.POLLOUT)
                    else:
                        poller.unregister(s)
                        s.close()
                        del message_queues[s]
```
Again we use `s.recv(1024)` to receive up to 1024 bytes on the client socket `s`, and store it in the _local variable_ `data`. If `data` is more than zero bytes, we print the data received, increment and print the total `messageCounter`, then add the `data` to the `Queue` for the client socket `s`: `message_queues[s]` with `.put()`. Additionally, we call `poller.modify()` to modify the flags for the already registered client socket `s`, to notify us about both the socket's readiness to read AND to write, by passing the bitwise-OR of both the `select.POLLIN` and `select.POLLOUT` bitmasks as the second argument of `poller.modify()`.

If `data` is zero (i.e. a zero-length `data` was received), this means the client has closed the connection, so under this `else` clause, we first remove `s` from being registered with `poller` so that `.poll()` will no longer trigger for this socket, then we `.close()` the socket and delete the socket's `Queue` from `message_queues`, as before.

If the bit of `flag` is set that indicates the socket `s` is ready for writing data (using the _bitmask_ `select.POLLOUT`), we use the same `try... except... else` construct we did when using `.select()` to retrieve the first piece of data to write from the `Queue` stored in `message_queues[s]` using the non-blocking member function `.get_nowait()`:
```python
            if flag & select.POLLOUT:
                try:
                    next_msg = message_queues[s].get_nowait()
                except queue.Empty:
                    poller.modify(s, select.POLLIN)
                else:
                    sent = s.send(next_msg)
                    if sent < len(next_msg):
                        remaining_msg = next_msg[sent:]
                        # Put the remaining message back at the front of the queue
                        message_queues[s].queue.appendleft(remaining_msg)
```
If the `Queue` for socket `s` is empty, this will trigger a `queue.Empty` _exception_, causing the `poller.modify(s, select.POLLIN)` line to be executed, which tells `poller` to go back to only notifying us about new incoming data ready on the socket `s`. Otherwise, the `else` clause is executed, which sends the data stored in `next_msg` out on the ready socket `s` (and in the case of an incomplete `.send()`, adds any unsent data back to the front of the queue), but leaves `poller` to also notify us when `s` is ready to send additional outgoing data again.

Next, we check to see if the bit of `flag` is set that indicates an error on socket `s` (similar to the "socket exceptions" reported by `select.select()`):
```python
            if flag & select.POLLERR:
                poller.unregister(s)
                s.close()
                del message_queues[s]
```
If this bit is set, we remove the socket `s` from `poller` entirely, so it does not trigger `s` on future calls to `.poll()`, then close the socket, and finally delete its `Queue` from `message_queues` to free any memory being used for the socket and help prevent memory leaks.

Finally, we need to add our `handle_new_connections_poll()` function to `start_server()`, and comment out the previous versions.
```python
def start_server():
    listen_socket = initialize_server_socket()
    # handle_new_connections_simple(listen_socket)
    # handle_new_connections_threads(listen_socket)
    # handle_new_connections_select(listen_socket)
    handle_new_connections_poll(listen_socket)
```
Now, let's test our code out:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
Now quickly, in yet another tab/window/terminal, run the another set of clients 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49942)
Received: b'Hello, world'
Total messages received: 200
```
As before, the server correctly handles multiple simultaneous client connections without the use of _threads_ or _locks_.

## Thread Pools
Whether `threading`, `.select()`, or `.poll()` is the best choice depends on many factors. Each has its advantages in different use cases. For some flows of control, one will be simpler and more straightforward to use than others. For extremely large numbers of network connections, a single-threaded server using `.poll()` might outperform a server using multithreading. Using `.select()` or `.poll()` also can let us avoid the complexities of dealing with thread synchronization, _race conditions_, and _deadlock_, which can get quite difficult to follow and debug. On the other hand, sometimes `threading` can be used to make handling multiple things at once much easier. In addition, most operating systems will attempt to spread threads out amongst multiple cores in a processor, whereas a single-threaded program will generally only run on a single core. This means that in many modern CPUs, which might have 8 or more cores even on the embedded processor in a cell phone, a server is essentially not effectively utilizing the CPU if it only runs in one thread (and thus only uses one core). Note however that the default Python implementation (CPython) does not do this with Python `threading`, so the utility might be limited in Python (although Python does have other modules such as `multiprocessing` that can facilitate running on multiple cores), but there are Python implementations that will run threads on multiple cores. In C however, using the `pthreads` library (which stands for POSIX threads, not Python threads), most operating systems will distribute these threads across cores in a CPU. A server can also use both threads AND `.select()` or `.poll()`. Why would we want to do this, it makes things even more complicated? Well, if using `pthreads` in C, we can create one thread per core (or 2 per core on a CPU using hyperthreading) to full utilize all of the cores, but still run `.poll()` inside some of those threads to maintain its scalability advantage, and also use some of those threads as "worker threads" that we can offload work to.

There are several ways to improve the performance of `threading`. More recent versions of Python 3 include a `ThreadPoolExecutor` that creates a pool of worker threads that can be used repeatedly without the overhead of constantly creating and destroying threads every time a new client connects. It can also keep track of and manage all the running threads, and shut them down gracefully if needed.

Another optimization takes advantage of the fact that, as previously discussed, adding a value to a list is atomic in the default Python implementation (CPython, which uses something known as a Global Interpreter Lock or GIL internally to ensure this atomicity). This mean that we can actually remove the _locks_ and their associated overhead from our server even when using threads. Relying on implementation-specific features such as the GIL is not recommended as a best practice, since it is not as portable and may change in future versions of Python, but it does illustrate the principle of atomicity.

We will demonstrate these concepts by writing a `handle_new_connections_thread_pool()` function that uses thread pools and atomicity to maximize performance. First, we need to import the `ThreadPoolExecutor` class from the `concurrent.futures` module with our other imports at the top of the source code file:
```python
from concurrent.futures import ThreadPoolExecutor
```
Since we only want to use `ThreadPoolExecutor`, and not the entire `concurrent` module, we can import just `concurrent.futures.ThreadPoolExecutor` with the above command. The `from` keyword tells Python to look inside the `concurrent.futures` module and the `import` command after it tells Python we want to import just the `ThreadPoolExecutor` class. This also allows us to access `ThreadPoolExecutor` member functions by typing just `ThreadPoolExecutor` instead of `concurrent.futures.ThreadPoolExecutor` each time.

Now, let's define our new `handle_new_connections_thread_pool()` function. We will declare `global messageCounter` at the top to let Python know we are referring to the _global variable_ `messageCounter` in this function, since we will be modifying it inside `handle_new_connections_thread_pool()` directly.
```python
def handle_new_connections_thread_pool(sock):
    global messageCounter
```
Note that because (as before) `handle_client()` is a nested function inside of `handle_new_connections_thread_pool()`, this `global` declaration applies to it as well, so we do not need to declare `global messageCounter` again inside the `handle_client()` function.
```python
    def handle_client(conn):

        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received:', data)
            messageCounter.append(data)
            print('Total messages received:', len(messageCounter))
            conn.sendall(data)
        conn.close()
```
This `handle_client()` function is very similar to the one in `handle_new_connections_threads()`. It loops continually until `conn.recv()` returns a zero-length `data`, then it closes the socket. Every time new data is received, it prints it out (and later sends it back over the client socket `conn`). However instead of using a _lock_ to manage `messageCounter`, this version maintains `messageCounter` as a list, appending the `data` received to the end of this list. Since using a list's `.append()` member function is an _atomic_ operation, we do not need to use a lock to accomplish this, and can just call `messageCounter.append(data)` (in the standard CPython implementation). To figure out how many messages have been received so far, we just have to look at the length of the `messageCounter` list, which we can get by calling `len(messageCounter)`. This also has the added benefit of tracking messages previously received, so we could display previous messages if desired. It does, however, take a lot more memory than the single integer that was our `messageCounter` in previous functions.

To write the main part of the `handle_new_connections_thread_pool()` function, we first initialize the _global variable_ `messageCounter` to an empty list, since we now want to use `messageCounter` as a list, rather than as a number:
```python
    messageCounter = []
    with ThreadPoolExecutor(max_workers=10) as pool:
```
We then use the `ThreadPoolExecutor` class that we imported to create a new _thread pool_ with a maximum of 10 worker threads. We only want a maximum of 10 threads at a time to keep the server from being overloaded. This will allow us up to 10 clients connecting at the same time. The `sock.listen(5)` call in the `initialize_server_socket()` function means that the server will block the next 5 incoming connections until they are processed. If this backlog is full, the server will just refuse any new connections until it is decreased. We could tweak these 2 numbers to fine-tune our server's performance. Note that if we did not specify this first `max_workers` argument to `ThreadPoolExecutor()`, by default it would use a maximum number of threads based on the number of CPU cores. The exact algorithm for determining this value varies from version to version, but is Python's attempt to guess the best setting for the computer it is running on. See https://docs.python.org/3/library/concurrent.futures.html for specific details.

We use the `with` keyword as before to ensure that the _thread pool_ is automatically cleaned up if this code is exited (whether naturally or through an _exception_). Otherwise, we would need to make sure to call `pool.shutdown()` before exiting, to make sure we exit gracefully, without leaving threads or memory leaks. The `as pool` part of this `with` statement assigns the newly created _thread pool_ executor to the variable `pool` within this clause.

To make sure we can properly deal with any _exceptions_ (such as the user pressing Control-C on the console to kill the server), we enclose the below code within a `try` clause:
```python
        try:
            while True:
                conn, addr = sock.accept()
                print("Received new connection from ", addr)
                # conn = setup_ssl(conn)
                pool.submit(handle_client, conn)
```
The `try` block continuously accepts new connections using `sock.accept()`, as before. When it receives a new client connection, it creates a new socket `conn` for that client, then prints a message, then calls the `pool` member function `.submit()` to tell the `ThreadPoolExecutor` to have one of its worker threads execute the `handle_client()` function. The second argument to `.submit()` tells it to pass `conn` as the first argument to `handle_client()`. The `ThreadPoolExecutor` will then either create a new thread (if `pool` has not yet reached its maximum limit) or find a free thread from those in `pool` and have that thread call `handle_client()`. If no threads in `pool` are available (because they are all busy doing tasks already), `.submit()` will still not block execution of the main function (so it can continue to process new connections), but the `ThreadPoolExecutor` will queue up the request in the background and have the next available thread call `handle_client()` when it is available.

If an _exception_ occurs (which happens when the user presses Control-C, for example), the server will immediately jump to the `except` clause, and print its shutdown message:
```python
        except:
            print("Shutting down gracefully...")
```
Since we used the `with ThreadPoolExecutor` construct above, it will automatically take care of shutting down the _thread pool_ (and the associated threads and their data structures), otherwise we would also call `pool.shutdown()` here.

Finally, we need to add our `handle_new_connections_threadpool()` function to `start_server()`, and comment out the previous versions.
```python
def start_server():
    listen_socket = initialize_server_socket()
    # handle_new_connections_simple(listen_socket)
    # handle_new_connections_threads(listen_socket)
    # handle_new_connections_select(listen_socket)
    # handle_new_connections_poll(listen_socket)
    handle_new_connections_thread_pool(listen_socket)
```
Now, let's test our code out:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
Now quickly, in yet another tab/window/terminal, run the another set of clients 100 times in a row:
```bash
for i in {1..100}; do python3 ClientPython.py; done
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 49743)
Received: b'Hello, world'
Total messages received: 1
...
<<< abbreviated for space >>>
...
Received new connection from  ('127.0.0.1', 49942)
Received: b'Hello, world'
Total messages received: 200
```
If we press Control-C to kill the server, instead of crashing with an _exception_, we get the message:
```
^CShutting down gracefully...
```
The server correctly handles multiple simultaneous client connections without the use of _locks_, thanks to the atomicity of the list `.append()` function. The use of the thread pool allows us to use threading without the constant overhead of creating and destroying threads for every new client connection.

Those that want more background on threading and concurrency in Python may wish to check out Jason Brownlee's free site/book at https://superfastpython.com which has a ton of tutorials on the subject and covers many other Python concurrency techniques as well.
