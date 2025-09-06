# Handling File Operations
Reference source files: `ClientPython.py`, `test.log`, `bad.log`

This tutorial will cover file operations. We will use these to turn our simple Python client into a useful capability: a program that can store and analyze network logging information with the help of a server.

## Reading and Parsing Files
To begin, we want to define a `load_file_data()` function to load a hypothetical server's network log data from a specified file. This log file will be in Comma Separated Value (CSV) format, with one log entry on each line, in the format:
```
username,userIP,serverPort,accessTime,dataSentByUser,dataReceivedByUser,score,server
```
For example, if the user 'Alice' accessed the server 10.2.1.5 on port 8080 from the IP address '10.0.0.9', sending the server 64 bytes of data and receiving 1024 bytes back from the server, the log entry might look like:
```
Alice,10.0.0.9,8080,100,64,1024,1.0,10.2.1.5
```
We want to read each of these lines into a Python _dictionary_ to represent the log entry, which will look something like:
```python
{
    'username': 'Alice',
    'IP': "10.0.0.9",
    'port': 8080,
    'accessTime': 100,
    'dataSent' : 64,
    'dataReceived' : 1024,
    'score' : 1.0,
    'server': "10.2.1.5"
}
```
In order to be able to efficiently process and store large numbers of log entries, we will use the _data structures_ we defined in a previous tutorial module.

To access these, we need to import the `DataStructuresPython` module we created in the earlier lesson (near the top of `ClientPython.py`, after the other `import` commands):
```python
import DataStructuresPython as ds
```
Since `DataStructuresPython` is rather lengthy to type out repeatedly, we use the `as` keyword afterwards, to define a shorter alias `ds` for accessing this module. Now, we can create a `PriorityQueue`, for example, by typing `ds.PriorityQueue()`

We will now define the `load_file_data()` function, which takes a user-specified string `file_path` to indicate the path of the network log file to open, then creates a new `PriorityQueue` to hold the file's network log entries and stores it in the local variable `logs`:
```python
def load_file_data(file_path):
    logs = ds.PriorityQueue()
```
In order to read or write to a file, we must first _open_ it, whcih provides a reference we can use to read or write to that file. Once we _open_ it, we also need to _close_ it when we are done, or else it could prevent others from reading or writing to it or cause the filesystem to lose data in event of a crash or power failure, depending on file permissions and the file system implementation. When we _open_ a file, we need to tell the operating system what sort of access we are looking for.

Python supports a number of combinations of opening modes:
- __Read Mode__ (`'r'`):
  - Opens the file for reading only.
  - The file must exist; otherwise, an error (`FileNotFoundError`) is raised.
  - Attempts to write to the file will result in an error (`io.UnsupportedOperation`).
 
- __Write Mode__ (`'w'`):
  - Opens the file for writing only.
  - If the file exists, it is truncated to zero length (i.e., its content is erased).
  - If the file does not exist, a new file is created.
  - Attempts to read from the file will result in an error (`io.UnsupportedOperation`).

- __Append Mode__ (`'a'`):
  - Works like __Write Mode__, except the file pointer starts at the end of the file, so that new data will be written at the end of the file or _appended_, rather than erasing the existing data.

Python also supports additional characters that can modify the above modes, for example adding a `+` to a mode allows it to perform both reads and writes, so that mode `'r+'` operates like __Read Mode__ but also allows writing to the file (at the current file position) and mode `'a+'` operates like __Append Mode__ but also allows reading from the file. Likewise, adding a `b` to a mode tells Python to treat the file as binary data rather than parsing it as text, so `'r+b'` mode could be used to open a binary file for both reading and writing.

We use the Python function `open()` to obtain a reference to the file we want, passing `file_path` as the first argument to specify its location and `'r'` as the second argument to specify the read/write mode we wish to use to _open_ the file, in this case opening it in _read-only_ mode:
```python
    with open(file_path, 'r') as file:
```
In order to have Python automatically handle _closing_ our file when we are finished, we use the `with` keyword here again, so as soon as the code underneath the clause is complete (or if it exits prematurely due to an `Exception`), it will automatically close the file. If we did not do this, we would need to explictly call `file.close()` when we were finished or if an `Exception` occurred. We also use the `as` keyword to reference our newly opened file by the name `file` within our `with` clause.

Within this `with` clause, we want to loop through each line in the file to parse each successive log entry. We use a `for` loop to accomplish this:
```python
        for line in file:
```
Since Python opened this file as a text file, it automatically can parse it into lines for us. Each iteration through this `for` loop, the variable `line` will contain a string with the successive line in the text file.

We will enclose our processing code for each `line` in a `try`..`except` structure to catch any errors that may occur. Why do we do this inside the `for` loop, rather than outside it? This way if there is an error parsing a single line, it will only affect that line, and the code will continue parsing the rest of the lines on the next iterations of the `for` loop. If we instead put the `try` clause outside of the `for` loop, any exceptions would exit the `for` loop entirely, meaning that an error on one line would stop us from processing the rest of the file. Sometimes that behavior might be desirable, but in this case we want to continue parsing the logs even if some lines are invalid, so we put the `try` clause inside the `for` loop:
```python
            try:
                parsedLine = line.split(',')
                if len(parsedLine) != 8:
                    raise Exception("Wrong number of elements in log entry")
```
For each `line` in the file `file`, we create a list `parsedLine` that contains the different comma-separated pieces of the `line`, using the built-in `.split()` method that is provided for all _string_ objects.

We then check to see how many comma-separated pieces we got from `line`, and if it is not equal to the number we expected, we explictly `raise` an `Exception` to indicate this line could not be parsed properly.

If we have the correct number of elements on the `line`, we then attempt to create a _dictionary_ using those elements, based on their order. We store the resulting _dictionary_ in the variable `logEntry`:
```python
                logEntry = {'username': parsedLine[0].strip(),
                    'IP': parsedLine[1].strip(),
                    'port': int(parsedLine[2].strip()),
                    'accessTime': int(parsedLine[3].strip()),
                    'dataSent' : int(parsedLine[4].strip()),
                    'dataReceived' : int(parsedLine[5].strip()),
                    'score' : float(parsedLine[6].strip()),
                    'server': parsedLine[7].strip()}
```
There are a couple important things to note here. First, we need to process each element of `parsedLine` before storing them in the appropriate _dictionary_ entry. We call the built-in string method `.strip()` which removes any whitespace at the beginning or end of a string (but not in the middle). This ensures that extra spaces, tabs, etc. separating the lines or elements will not be stored. For the numerical data types such as `port`, we also use the built-in `int()` function to convert the stripped strings to integers. This allows us to store them as numbers (which can be used mathematically) rather than strings. The exception is `score`, which is not an integer but a floating-point value, so we use the `float()` function to convert it instead. Finally, if any of these functions fails (for example, if `accessTime` is `"Joe"` instead of a number), it will automatically cause an `Exception` to occur, which will be caught by our `try`..`except` structure and processed in the `except` clause, which we will add shortly. This helps to ensure that our program is robust to invalid or malicious log file entries, by validating that the input data matches the expected format.

In this spirit, we also want to validate that the IP addresses are valid (IPv4 or IPv6). We will check them using a function `is_valid_ip()` that we will define later. If `is_valid_ip()` returns `False`, we will `raise` an `Exception` with an error message. Since the `'server'` field might contain either an IP address or a hostname, we cannot use this function to validate it.
```python
                if not is_valid_ip(logEntry['IP']):
                    raise Exception('Invalid IP: {}'.format(logEntry['IP']))
                
                logs.enqueue(logEntry, logEntry['accessTime'])
```
If the client's IP is validated, we will add the validated `logEntry` into our `PriorityQueue` named `logs`, using its `accessTime` as the index for priority in the queue. This will allow us to more easily filter by time indicies.

If an `Exception` has occurred, the log line was not valid or could not be read or parsed for some reason, so we need to "catch" it in an `except` clause, and print an error message:
```python
            except:
                print('Invalid log line: {}'.format(line))
    return logs
```
Finally, the function returns the `logs` queue, which is already ordered by `accessTime`.

Next we need to define the `is_valid_ip()` function we used above. This function can go right before our `load_file_data()` function in `ClientPython.py`. It takes a string containing the IP address to be validated as its only argument:
```python
def is_valid_ip(ip):
```
First, we check to see if `ip` is a valid IPv4 address by splitting the `ip` string into parts separated by `.`s. If there are not exactly 4 parts, it is not a valid IPv4 address and we will need to check if it is a IPv6 address. If there are exactly 4 parts, it cannot be a IPv6 address (since those are separated by `:`s rather than `.`s), so we will check to make sure each of the 4 parts is a digit from 0 to 255:
```python
    # Check if it's a valid IPv4 address
    parts = ip.split('.')
    if len(parts) == 4:
        for part in parts:
            if not part.isdecimal() or not 0 <= int(part) <= 255:
                return False
        return True
```
The string method `.isdecimal()` returns `True` if the string is all digits, otherwise it returns `False`. Thus this code will return `True` only for a proper numeric IPv4 address; if there is non-numeric data, it will return `False`.

If the string `ip` cannot be split into exactly 4 parts separated by `.`s, it might still be a valid IPv6 address. Since IPv6 allows a much more complex set of values, including abbreviations like `2001:db8::1:0:0:1` and `2001:db8::1` and even `::1`, it is much trickier to manually validate, and we are much more likely to make a mistake in our validation code without extensive testing. Therefore, we will instead use the `socket` module method `socket.inet_pton()` which is designed to convert a IPv6 string into a binary format IPv6 address. While we don't actually care about the output of this function, if it encounters an error in parsing the string as an IPv6 address, it will automatically raise an `socket.error` `Exception`. We can use this to determine if the IPv6 address is valid (in which case no `Exception` will be raised).
```python
    # Check if it's a valid IPv6 address
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False
```
Note that in theory we could just let the calling `load_file_data()` function "catch" the `Exception`, rather than handling it ourselves and returning `False`. However, since we return `False` above for an invalid IPv4 address, it would be inconsistent for `is_valid_ip()` to operate one way for IPv4 addresses and another for IPv6 addresses. It is important that functions be consistent and predictable. Even if we know that only `load_file_data()` will call `is_valid_ip()`, we cannot predict how this code might be used by someone else in another program or even in this program 10 versions later. Keeping a function's behavior as straightforward and consistent as possible helps minimize errors and maximize code reuse potential. In addition, letting `load_file_data()` handle this `Exception` would result in a different format of error messages for IPv4 and IPv6 errors, which is again undesirable.

## Writing and Modifying Files
In addition to reading logs from a file, we also want to be able to keep a local logfile of queries made by the user on a dataset. We will start by writing a function to save a query to our query logfile (not to be confused with the network log files used in `load_file_data()`).

This query logfile will be a text file that starts with a line showing the total number of query filters in the file, followed by a line containing the string for each filter. For example:
```
Total filters: 2
port=443
score > 1
```
Our program must not only add and remove filters from this logfile, but also must update the number on the first line of the file whenever the number of filters (and thus the number of lines in the logfile) change. While technically the query is the initial request criteria and a "filter" is any refinement to filter those query results, this query logfile treats both of these things the same way: as strings that can be used to both query and filter the results.

Before we can write this function, we need to import some additional modules and add some variables at the top of our source code file:
```python
import os

QUERY_LOG_PATH = 'query_log.txt'
filterStack = ds.Stack()
```
First, we `import` the `os` module, which is used as a portable way to access operating system-dependent functionality, such as navigating a filesystem, modifying environment variables, or executing shell commands.

Next, we define a default name for our query logfile, and create a new `Stack` called `filterStack` to store filters we are using on query results.

Now, we can define our function `save_last_query_action()` to store a query passed in as the string `query` to our query logfile:
```python
def save_last_query_action(query):
```
First, we will check to see if the query logfile already exists using the `os` module method `os.path.exists()`. If it returns `False`, it does not exist, so we will call `open()` to create it: 
```python
    # Check if the log file exists. If not, create it
    if not os.path.exists(QUERY_LOG_PATH):
        open(QUERY_LOG_PATH, 'w').close()
```
Calling `open()` with the file mode `'w'` opens a new file for writing, creating it if needed, and truncates it to length zero (empty). Note that since we called `open()` manually rather than as part of a `with` clause, we need to call `close()` as well, which we do immediately after `open()` returns.

Since we know the file at `QUERY_LOG_PATH` exists now, regardless of whether or not it did before, we can now `open()` it using the `'r+'` mode to allow for both reading and writing. Note that if we used `'w+'` instead, it would create the file for us automatically if it did not already exist (so we would not need the previous code), but it would also overwrite all the existing data in the log file, which we do not want. We could have used `'a+'` mode instead for similar behavior without overwriting the file, but since we want to parse the file first before adding to it, we use `'r+'` mode (with the above code to create the file first if it does not exist) instead:
```python
    with open(QUERY_LOG_PATH, 'r+') as file:
```
We again use a `with` clause so that Python closes the file for us automatically when appropriate.

Within that `with` clause, we first read the first line (which should contain the number of filters in the file). We use the `file` method `.readline()` to extract the first line from `file`, then slice off the part of the line containing the text `Total filters: `, leaving just the number of filters, then `.strip()` any whitespace off that to get just the number part of the string and store it in the local variable `first_line`:
```python
        first_line = file.readline()[len('Total filters: '):].strip()
        try:
            num_queries = int(first_line)
        except ValueError:
            num_queries = 0
```
Note that we attempt to use the `int()` function to convert the string `first_line` to an integer `num_queries`, but we need to enclose it in a `try` clause because if it is not a valid integer we want to "catch" the `ValueError` `Exception` and set `num_queries` to `0` instead. This will happen if we just created the file, since it doesn't have a first line yet.

However, regardless of whether we read in the value properly or it did not exist and we set it to `0`, we need to add 1 to `num_queries` for the filter string `query` that was passed into `save_last_query_action()` as its sole parameter. To do this _whether or not_ an `Exception` occurs, we can add a `finally` clause to the `try..except` construct:
```python
        finally:
            num_queries += 1
```
This clause will be executed after the `try` and `except` clauses are finished, regardless or whether or not an Exception occurred. This can be very useful for cleanup, closing files or sockets, disposing of data allocations, etc.

Next, we need to update the first line of the file to reflect the correct number of filters after this update. To do this, we need to change the file position back to the beginning of the file with `file.seek(0)` which sets the file position to the byte offset passed as its first argument (`0` corresponding to the beginning of the file). This allows us to then call `file.write()` with the new string we want to write at the beginning of the file.:
```python
        file.seek(0)
        file.write(f'Total filters: {num_queries:<16}\n')
```
The string we pass as an argument to `file.write()` utilizes a shorthand version of the string `.format()` syntax. Instead of writing out `'Total filters: {:<16}\n'.format(num_queries)`, using a `f` in front of a string allows us to put the variables that would otherwise by passed as arguments to `.format()` directly into the `{}` placeholders in the string. The above code is therefore equivalent, but more compact. Also note that even when using `.format()`, the `{}` is **not** empty. Specifying `:<16` inside of the placeholder `{}` indicates that the substituted variable should be formatted such that it will be padded out to 16 total characters. For a string, this means adding whitespace, so instead of `'4'` it would output:
```
'4               '
```
This is important, because it keeps the first line at a constant length as we add and remove filters to the query log. If it was not constant, every time we updated the file we would need to rewrite all the entries made after the first line, since the length of the first line would change. This is certainly possible (and even desirable in some circumstances), but in this case our approach results in better performance.

After writing the updated first line, we need to jump to the end of the file by again calling `file.seek()`, but we supply a second argument to this method to instruct it to calculate the file position relative to the **end** of the file. This allows us to append our new entry to the end of the existing file:
```python
        file.seek(0, os.SEEK_END)
        file.write(query + '\n')
```
Note that we add a newline character `\n` after the `query` string in order to keep each filter string on its own line.

For debugging purposes, we also want to print the new size of the file to the console to make sure everything worked correctly. We can remove or comment this code out when we finish the program, but it may aid in debugging. To get this size, we use the `os` module method `os.path.getsize()`, which takes a pathname to a file as its parameter, and returns the size of that file in bytes. We then print this size to the console:
```python
        # Print the new size of the file to console
        print(f"Updated query log. New size = {os.path.getsize(QUERY_LOG_PATH)} bytes")
```

We also need a function to remove the most recent query/filter from the query log. In conjunction with the `filterStack` global variable we created at the beginning of our file, this will allow us to maintain a list of recent query filters created, while providing the ability to undo/remove the most recent query/filter added at the user's request.

We define the function `remove_last_query_action()`, which takes no arguments, to accomplish this. It uses a `with` clause to open the file in `'r+'` mode (read mode with writes allowed) as before, to provide automatic closing of the file when finished. In this case, we do not need to check if the file exists or create the file, because the function requires there to be a query to remove (which would not be the case if the query logfile was empty):
```python
def remove_last_query_action():
    with open(QUERY_LOG_PATH, 'r+') as file:
```
When adding a query filter string in the `save_last_query_action()` function, we just had to update the first line, then append the new string to the end of the file. However, this time we want to _remove_ the last string. While we could start at the end of the file, then parse backward to determine where this last string starts, we will instead take a different approach: we will load all the log entries in the file, then rewrite the whole file without the removed data. While it might be a bit slower than the approach we used before, we could also use this new approach if we didn't want to use the whitespace "trick" we used before to guarantee a fixed length for the first line, or if we wanted to insert data in the middle of the file.

First, we use the `.readlines()` method to read each line in `file` into a list of lines named `lines`. Then we extract the number of filter strings from the first line, as we did before:
```python
        lines = file.readlines()
        first_line = lines[0][len('Total filters: '):].strip()
        try:
            num_queries = int(first_line)
        except ValueError:
            num_queries = 0
```
Since the caller should ensure there is at least one query string before calling `remove_last_query_action()`, we should never encounter the situation where there are no queries to remove. However, things often do not go as planned. For example, the query logfile might have been altered or corrupted, or maybe the computer crashed and it was left in an invalid state. It is good error-checking practice to check for errors that should not occur, so that they are quickly exposed (and can be fixed) when they do. Also, lack of error-checking can often lead to security vulnerabilities when people intentionally induce error conditions. So we will verify here that `num_queries` is at least 1, and if not, we will `raise` a `ValueError` `Exception`:
```python
        if num_queries < 1:
            raise ValueError("No queries to remove")
```
Now that we know there is at least one saved query/filter, we can reduce the current query filter string count by 1, then move to the beginning of the file with `file.seek(0)` and rewrite the first line with the new number of filters, as we did before in `save_last_query_action()`:
```python
        num_queries -= 1
        file.seek(0)
        file.write(f'Total filters: {num_queries:<16}\n')
```
Now, instead of jumping to the end of the file, we will just continue on from the current file position, writing all of the lines we read in previously to the list variable `lines`, except for the first and last one, which we exclude via _slicing_ `lines`:
```python
        file.writelines(lines[1:-1])  # Write all lines except the last one
```
Now we want to remove any data in the query logfile after the (updated) last line we have written (removing any entries after this point). To do this, we use `file.truncate()`, which sets the end of the file to the current file position (where we just finished writing):
```python
        file.truncate()
```
Finally, as in `save_last_query_action()`, we want to print out the new size of the updated file. While we could do this as we did previously, we will instead practice an alternate approach using `file.tell()`, which returns the current file position. Since we are currently at the end of our file, this is equal to the file size:
```python
        print(f"Updated query log. New size = {file.tell()} bytes")
```
Either method of getting the file length here could work.

## Applying the File Functions
In order to expose the functions we just wrote to the user, we are going to implement a simple text-based menu to prompt the user for various actions. The user will be able to choose from 7 choices:

1. Upload log file to server
2. Submit new query to server
3. Filter query results
4. Undo last query/filter
5. Display current query results
6. Clear all query results
7. Exit

We will define a function `do_menu()` which takes as its sole argument a socket for communicating with a server, which will initialize local variables to track the current filter string `curFilterString` and a list of results `curResults`, then loop forever, displaying the server's info along with the current query/filter and results, and prompting the user to choose one of the above choices over and over again until they choose "Exit". Before this loop starts, it will also check to see if the query logfile is present, and if so it will clear it by deleting the file using the `os` module's `os.remove()` method, which takes as its argument a path to the file to be deleted:
```python
def do_menu(sock):
    curFilterString = ''
    curResults = []
    if os.path.exists(QUERY_LOG_PATH):
        os.remove(QUERY_LOG_PATH)
    
    while True:
        print('Connected to server {}:{}'.format(SERVER_NAME, SERVER_PORT))
        print('Last filter: {} matching {} results'.format(curFilterString,len(curResults)))
        print('Please choose an option:')
        print('1. Upload log file to server')
        print('2. Submit new query to server')
        print('3. Filter query results')
        print('4. Undo last query/filter')
        print('5. Display current query results')
        print('6. Clear all query results')
        print('7. Exit')
```
If we wanted to support using the same query logfile across multiple client launches (sometimes called "persistence"), instead of deleting the query logfile here we could load it into `filterStack` and re-run the needed queries. This is, however, not needed for the functionality of our client and server, so is left as an exercise to the reader.

To read in the user's choice from the menu, we can use the built-in function `input()`, which takes as its argument the text to display to the user at the prompt, and returns the string that the user enters at that prompt:
```python
        choice = input('Enter choice: ')
```
Once we have the user's input in the local string variable `choice`, we look at the first character to determine the user's selection. We ignore any input after the first character, as some users might type in the entire line rather than just the number. We will start by checking if the user's entry starts with `1`. This indicates we should upload a network log file to the server. Since we haven't written the code for this functionality yet, right now we will load the file data using `load_file_data()` but not actually send it anywhere. We need to again use the `input()` function to prompt the user for the path of the log file to upload, then we can call `load_file_data()` with that path:
```python
        if choice.startswith('1'):
            file_path = input('Enter the path to the log file to upload: ')
            logs = load_file_data(file_path)
            print('Loaded {} log entries successfully'.format(len(logs)))
```
After loading the user-specified file (whose log entries are now stored as dictionaries in the `PriorityQueue` `logs`, ordered by `accessTime`), we will print out the number of log entries read in (which is equal to the length of `logs`).

Once we have the log entries in `logs`, we will send these to the server by calling the `upload_logs()` function, which takes 2 arguments, the socket to send the data over, and the data to send. We will implement the `upload_logs()` function later:
```python
            if (len(logs) > 0):
                # send logs to server
                upload_logs(sock, logs)
```
We will skip menu choice #2 for now, since we don't have the network code for this implemented yet. Menu choice #3 is to filter the results of a query using a user-supplied filter string. To keep the code here readable and maintainable, we will make up some new functions which we will implement later. A `get_filter_string()` function will take no arguments and return a user-supplied filter string, which we can store into the `curFilterString` variable. A `apply_filter()` function will take two arguments, the first being the query results to filter, and the second being the filter string to use. We will update the `curResults` variable with the result of this function:
```python
        elif choice.startswith('3'):
            curFilterString = get_filter_string()
            curResults = apply_filter(curResults, curFilterString)
```
We want to store each successive filter string and the results of that filter on our `filterStack` in case we want to remove recent filter changes. In order to accomplish this, we will `.push()` a tuple where the first element is the new set of filter results and the second element is the current filter string.
```python
            filterStack.push((curResults, curFilterString))
```
For our query logfile, we only need to save the filter string itself, which we can do by passing it to the `save_last_query_action()` function we previously wrote:
```python
            save_last_query_action(curFilterString)
```
Menu choice #4 removes the last applied filter, while keeping any others before it. To implement this, we need to remove it from both `filterStack` and the query logfile. To remove these, assuming there is at least one filter, we can just call the `Stack` `.pop()` method to remove the last entry from the `Stack`, and we conveniently already wrote a `remove_last_query_action()` function to remove the last entry from the query logfile:
```python
        elif choice.startswith('4'):
            # undo last filter
            if len(filterStack) > 0:
                filterStack.pop()
                remove_last_query_action()
```
We also need to restore the previous values to `curResults` and `curFilterString`. These are conveniently stored on `filterStack`, which we could access via `filterStack[-1]`. However, this is not good object-oriented practice, because we shouldn't make assumptions about the internal structure of objects, since they may change over time. Instead we should try to only use the methods provided by the `Stack` object to manipulate it. Some stacks may have a `.peek()` method that allows us to look at the top element of a stack without removing it. We could of course implement such a method in the data structure ourselves. We could also make a _subclass_ of `Stack` that _inherits_ from it but adds the `.peek()` method. However, if that is not possible, we should still try to use the methods that are provided. We can achieve the same result if we `.pop()` the top element off the stack into `curResults` and `curFilterString`, then immediately `.push()` it back on (note that this approach might cause issues in a multithreaded situation, but our client is single-threaded):
```python
                if len(filterStack) > 0:
                    curResults, curFilterString = filterStack.pop()
                    filterStack.push((curResults, curFilterString))
                else:
                    curResults = []
                    curFilterString = ''
            else:
                print('No filters to undo')
```
Note that we also do some error handling here. As previously discussed, the `remove_last_query_action()` function expects there to be at least one query/filter string to remove. Therefore, we need to check to make sure at least one exists, before calling `remove_last_query_action()` (and before calling `.pop()` on the `Stack`). Since we maintain these entries in the `filterStack` variable as well as the query logfile, we can just check `filterStack` for this (unless the file has somehow been corrupted, moved, deleted, or otherwise tampered with, but that is what `Exception` handling will take care of). We need to check this again before restoring the last `curResults` and `curFilterString` values, and if `filterStack` is empty now, we just set them to their empty defaults instead.

Menu choice #5 simply displays the current results (with any filters applied), which can be done by simply printing the `curResults` variable:
```python
        elif choice.startswith('5'):
            # display results
            print('Current query results:')
            print(curResults)
```
Menu choice #6 clears the query and any filters completely. To do this we can simply delete the query logfile using the `os` module's `os.remove()` method, which takes as its argument a path to the file to be deleted. We also need to clear the `filterStack` variable, with we can do with the `Stack` `.clear()` method:
```python
        elif choice.startswith('6'):
            # delete log file
            os.remove(QUERY_LOG_PATH)
            filterStack.clear()
```
Menu choice #7 is chosen to exit the program, so all we have to do is call `return`. We also print an error message if the choice was not valid (meaning it was not handled by one of our `if` clauses):
```python
        elif choice.startswith('7'):
            return
        else:
            print('Invalid choice. Please try again.')
```
In order to integrate our new `do_menu()` function into our existing client, we will define a new `start_client()` function that calls `do_menu():
```python
def start_client():
    with socket.create_connection((SERVER_NAME, SERVER_PORT)) as sock:
        do_menu(sock)
```
Note that this version is slightly different than `start_client_simple()`. Instead of creating a new socket with `socket.socket()` and then calling the `.connect()` method on that socket to establish a connection, it uses the `socket` module's `socket.create_connection()` method to do all of this at once. `socket.create_connection()` returns a new socket that is already automatically connected to the server and port which are passed as a tuple to the `.create_connection()` method. We also use the `with` and `as` keywords here, and call `do_menu()` within the `with` clause. This ensures that Python will automatically `close()` the `socket` for us after this code exits, freeing us from the need to manually call `close()` as we did in `start_client_simple()`. This is particularly useful if the code exits unexpectedly, such as because of an `Exception`.

Remember that we also need to update the bottom of our client file to call our new `start_client()` function instead of the other versions.

We also need to implement the new functions we made up in `do_menu()`. `get_filter_string()` will prompt the user to enter a filter string, and return that string. We should also provide a reasonable explanation of how filter strings work to the user, which we can print out as instructions just before calling the `input()` function. We want to support a lot of flexibilty in filters, so we will support filters that specify multiple criteria, seperated by commas. Each criterion should consist of a single field name (i.e. IP, score, etc) followed by one of the standard comparison/equality operators (i.e. =, !=, >, etc):
```python
def get_filter_string():
    print("Enter filter query as a string with fields separated by commas (i.e. username=Alice, score>4, score<9.5)")
    print("Valid fields: username (client's username), IP (client IP), server (server name/IP), port (server port), accessTime (as an integer), dataSent (bytes sent by client), dataReceived (bytes sent to client), score (floating point)")
    print("Valid operators: =, <, >, <=, >=, !=")
    filter = input('Enter filter: ')
    return filter
```

We also need to define the `apply_filter()` function. Since this isn't directly file-related, we will properly implement this function in a future tutorial. For now, we will just return the same `results` passed in, ignoring the filter/query string:
```python
def apply_filter(results, filter_query):
    return results
```

We also need to define the `upload_logs()` function. We will also implement this in a future tutorial, so for now it will do nothing except `return`:
```python
def upload_logs(sock, logs):
    return
```

## Testing
While we do not have the server or network pieces needed to test everything yet, we can at least test the basic file code now.

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
While the server does not yet have the capacity to handle any of the new menu functions, it still should allow the client to connect, so we should see:

ServerPython Output:
```
Received new connection from  ('127.0.0.1', 64043)
```
ClientPython Output:
```
Starting client...
Connected to server localhost:12345
Last filter:  matching 0 results
Please choose an option:
1. Upload log file to server
2. Submit new query to server
3. Filter query results
4. Undo last query/filter
5. Display current query results
6. Clear all query results
7. Exit
Enter choice: 
```
Let's try some easy tests first. Currently, there is no filter and there are no results, so if we try `4`, let's make sure it does not crash:
```
No filters to undo
```
Perfect! The program correctly checked to make sure there was at least one query/filter string before calling `remove_last_query_action()`.

Next, let's try `5`:
```
Current query results:
[]
```
Again, the program behaves correctly on this trivial case, displaying an empty list of results.

Next, let's try `6`:
```
Last filter:  matching 0 results
```
Again, the program behaves correctly on this trivial case, keeping the list empty with no issues.

Next, let's try `7`. The program successfully exits as intended. Let's run the client again so we can continue testing:
```bash
python3 ClientPython.py
```
What about bad entries? Let's try `8`:
```
Invalid choice. Please try again.
```
We get the same result if we type in some other invalid entry, such as `apples`:
```
Invalid choice. Please try again.
```
Let's also make sure that the program is correctly only looking at the first character. If we type in `41` or `4tables` at the menu prompt, we should still get:
```
No filters to undo
```
Now let's try testing the actual file functionality, starting by selecting `1`, and specifying the `test.log` file from the tutorial repository with provided test data:
```
Enter choice: 1
Enter the path to the log file to upload: test.log
Loaded 30 log entries successfully
```
The program says it loaded 30 log entries successfully from the file, and if we look at the file and count them (either manually or with the `wc` program), there are indeed 30 lines of data in `test.log`. But do we really know if they were parsed and read in correctly? Ideally we'd like to see the actual data extracted, to make sure the program works as intended.

Since we still don't have the network or server code for the menu implemented yet, we need a different approach. Let's temporarily add `print` statements in the `load_file_data()` function after we call `logs.enqueue()` for each entry to make sure each entry was parsed properly:
```python
                logs.enqueue(logEntry, logEntry['accessTime'])
                print("Added logEntry: {}".format(logEntry))
```
Now, when we run the client, we get ClientPython Output:
```
...
Enter choice: 1
Enter the path to the log file to upload: test.log
Added logEntry: {'username': 'Alice', 'IP': '192.168.1.2', 'port': 443, 'accessTime': 1633072800, 'dataSent': 1024, 'dataReceived': 2048, 'score': 1.5, 'server': '10.2.1.5'}
Added logEntry: {'username': 'Bob', 'IP': '2001:0db8:85a3:0000:0000:8a2e:0370:7334', 'port': 443, 'accessTime': 1633072801, 'dataSent': 512, 'dataReceived': 1024, 'score': 2.0, 'server': '10.2.1.5'}
...
```
We can now see that the file log entries are getting read in and parsed into dictionaries correctly. Note that this is generally not information we will want an end user to have to see, so we will comment out the `print` line we just added for now.

We also want to ensure our program is robust, so let's try giving it some bad inputs. We will again select #1 in the client's menu, but instead enter an invalid filename `???`:
```
Enter choice: 1
Enter the path to the log file to upload: ???
Traceback (most recent call last):
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 360, in <module>
    start_client()
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 327, in start_client
    do_menu(sock)
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 246, in do_menu
    logs = load_file_data(file_path)
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 31, in load_file_data
    with open(file_path, 'r') as file:
FileNotFoundError: [Errno 2] No such file or directory: '???'
```
When `open()` was called to open the non-existent file, it raised a `FileNotFoundError` `Exception`. Since we don't have this code in a `try..except` clause of some sort, it causes the program to terminate. One way to address this is to put a `try..except` clause in the `do_menu()` function's `while True` loop, so that it will print an error message and just go back to the main menu if any sort of error occurs:
```python
    ...
    while True:
        try:
            print('Connected to server {}:{}'.format(SERVER_NAME, SERVER_PORT))
    ...
            else:
                print('Invalid choice. Please try again.')
        except Exception as e:
            print('Error: {}'.format(e))

```
Be sure to indent the code inside the `try` clause. Note that all types of Python exceptions are subclasses of `Exception`, so this `except` clause will catch all of them, from network exceptions to file exceptions, and with the `as` keyword we can refer to the triggering `Exception` as `e` within the `except` clause. Therefore, when we `print` `e` it will show the text contained in the triggering `Exception`.

If we only wanted to "catch" and print `FileNotFoundError`s, we could instead make the `except` line:
```python
        except FileNotFoundError as e:
```
This would however cause other (not handled) `Exception`s to terminate the program, so we will not do this.

Now when we run our previous test again, we instead get:
```
Enter choice: 1
Enter the path to the log file to upload: ???
Error: [Errno 2] No such file or directory: '???'
Connected to server localhost:12345
Last filter:  matching 0 results
Please choose an option:
1. Upload log file to server
2. Submit new query to server
3. Filter query results
4. Undo last query/filter
5. Display current query results
6. Clear all query results
7. Exit
Enter choice: 
```
Next, let's test what happens when we intentionally put bad data in our log file. The file `bad.log` from the repository is based on `test.log`, with some modifications (Alice has too few elements, Dave has too many elements, Eve just has a blank for port number, Grace has a bad IP address, Heidi has a word where her score should be, etc.). Let's read in this `bad.log` file instead:
```
Enter choice: 1
Enter the path to the log file to upload: bad.log
Invalid log line: Alice,192.168.1.2,1633072800,1024,2048,1.5,10.2.1.5

Invalid log line: Dave,192.168.1.4,443,1633072903,1024,2048,3.5,10.2.1.5, 80

Invalid log line: Eve,2001:0db8:85a3:0000:0000:8a2e:0370:7335,,1633073102,512,1024,4.0,10.2.1.5

Invalid log line: Eve,2001:0db8:85a3:0000:0000:8a2e:0370:7335,,1633073103,512,1024,4.0,10.2.1.5

Invalid IP: badip
Invalid log line: Grace,badip,443,1633073150,1024,2048,2.5,10.2.1.5

Invalid log line: Heidi,2001:0db8:85a3:0000:0000:8a2e:0370:7336,443,1633073184,512,1024,telephone,10.2.1.5

Loaded 24 log entries successfully
```
Our error checking correctly detects all of the invalid log entries, while still successfully reading in all of the good ones, displaying the appropriate error messages to the user.

We can't test menu option #2 yet, so let's move on to #3. We will start with the filter `port=443`:
```
Enter choice: 3
Enter filter query as a string with fields separated by commas (i.e. username=Alice, score>4, score<9.5)
Valid fields: username (client's username), IP (client IP), server (server name/IP), port (server port), accessTime (as an integer), dataSent (bytes sent by client), dataReceived (bytes sent to client), score (floating point)
Valid operators: =, <, >, <=, >=, !=
Enter filter: port=443
Updated query log. New size = 32 bytes
Connected to server localhost:12345
Last filter: port=443 matching 0 results
Please choose an option:
1. Upload log file to server
2. Submit new query to server
3. Filter query results
4. Undo last query/filter
5. Display current query results
6. Clear all query results
7. Exit
Enter choice: 
```
Since we haven't implemented the function `apply_filter()` yet, any filter string we enter will produce a similar sort of output. Note however, that the last filter is correctly displayed now before the main menu, and we were told the query log was updated with a new size. We can look at the `query_log.txt` file in another terminal to verify this:
```bash
more query_log.txt 
```
Output:
```
Total filters: 1               
port=443
```
So the query log was created and written properly. But what about the size? It may be hard to tell because of the whitespace on the first line, but we can see the individual bytes with `hexdump -C query_log.txt` or with `ls -l query_log.txt`:
```bash
-rw-r--r--  1 user  staff  41 Nov  4 13:12 query_log.txt
```
which shows a file size of 41 bytes, not 32! What is going on here? (Note: some operating systems & Python versions may not produce this result)

Let's take a look back at the `save_last_query_action()` function. The last few lines read:
```python
        file.seek(0, os.SEEK_END)
        file.write(query + '\n')

        # Print the new size of the file to console
        print(f"Updated query log. New size = {os.path.getsize(QUERY_LOG_PATH)} bytes")
```
The `os.path.getsize()` method queries the underlying operating system and returns the file size. On some operating systems, the previous `write()` call that added the last query string may not have actually been written to disk yet due to caching, so `os.path.getsize()` will return the file size before that last `write()` call (32), rather than the correct size (41).

There are two simple ways to fix this. First, we could ensure that the file is closed before checking the file size. We can do this simply by removing one layer of identation from the `print` line:
```python
def save_last_query_action(query):

    # Check if the log file exists. If not, create it
    if not os.path.exists(QUERY_LOG_PATH):
        open(QUERY_LOG_PATH, 'w').close()

    with open(QUERY_LOG_PATH, 'r+') as file:
        first_line = file.readline()[len('Total filters: '):].strip()
        try:
            num_queries = int(first_line)
        except ValueError:
            num_queries = 0

        num_queries += 1
        file.seek(0)
        file.write(f'Total filters: {num_queries:<16}\n')
        file.seek(0, os.SEEK_END)
        file.write(query + '\n')

    # Print the new size of the file to console
    print(f"Updated query log. New size = {os.path.getsize(QUERY_LOG_PATH)} bytes")
```
This ensures that the `print()` and call to `os.path.getsize()` occur outside of the `with` clause, which means the file will automatically `close()` before getting the size. `close()`ing a file automatically flushes any data in the cache.

Another alternative would be to explictly force Python/the underlying operating system to flush the cache before getting the size. We can do this by calling the `file` object's `.flush()` method:
```python
...
        file.seek(0, os.SEEK_END)
        file.write(query + '\n')
        file.flush()

        # Print the new size of the file to console
        print(f"Updated query log. New size = {os.path.getsize(QUERY_LOG_PATH)} bytes")
```
This solves the caching issue and ensures we get the correct size, since everything is written to disk before we get the size.

Let's run the client again:
```
...
Enter choice: 3
Enter filter query as a string with fields separated by commas (i.e. username=Alice, score>4, score<9.5)
Valid fields: username (client's username), IP (client IP), server (server name/IP), port (server port), accessTime (as an integer), dataSent (bytes sent by client), dataReceived (bytes sent to client), score (floating point)
Valid operators: =, <, >, <=, >=, !=
Enter filter: port=443
Updated query log. New size = 41 bytes
Connected to server localhost:12345
Last filter: port=443 matching 0 results
```
Note that the size is now correctly displayed as 41 bytes, which includes writing the filter string and matches the output of `ls -l query_log.txt`. Now let's add another filter line:
```...
Enter choice: 3
Enter filter query as a string with fields separated by commas (i.e. username=Alice, score>4, score<9.5)
Valid fields: username (client's username), IP (client IP), server (server name/IP), port (server port), accessTime (as an integer), dataSent (bytes sent by client), dataReceived (bytes sent to client), score (floating point)
Valid operators: =, <, >, <=, >=, !=
Enter filter: score > 1
Updated query log. New size = 51 bytes
Connected to server localhost:12345
Last filter: score > 1 matching 0 results
```
So far so good. The size is again correct, matching the output of `ls -l query_log.txt`. One more, let's try something non-sensical:
```
Enter choice: 3
Enter filter query as a string with fields separated by commas (i.e. username=Alice, score>4, score<9.5)
Valid fields: username (client's username), IP (client IP), server (server name/IP), port (server port), accessTime (as an integer), dataSent (bytes sent by client), dataReceived (bytes sent to client), score (floating point)
Valid operators: =, <, >, <=, >=, !=
Enter filter: turnip
Updated query log. New size = 58 bytes
Connected to server localhost:12345
Last filter: turnip matching 0 results
```
Our program doesn't care what the string is, so `turnip` works just as well. It updates the size of the query log correctly. Let's check the actual log again:
```bash
more query_log.txt 
```
Output:
```
Total filters: 3               
port=443
score > 1
turnip
```
Everything looks fine here. Now let's try using menu option #4 to remove the last non-sensical entry:
```
Enter choice: 4
Updated query log. New size = 51
Connected to server localhost:12345
Last filter: score > 1 matching 0 results
```
Note that we do not have the same problem we had before with the size output by `remove_last_query_action()`. This is because `remove_last_query_action()` uses `file.tell()` to get the file size, and `.tell()` utilizes the cache, so it does not matter if it has not yet been written/flushed to the disk.

We can verify that the previous query was properly removed by checking the log again:
```bash
more query_log.txt 
```
Output:
```
Total filters: 2               
port=443
score > 1
```
Let's try using menu option #4 again to remove the next-to-last entry:
```
Enter choice: 4
Updated query log. New size = 41 bytes
Connected to server localhost:12345
Last filter: port=443 matching 0 results
```
Looks good. One more time:
```
Enter choice: 4
Updated query log. New size = 32 bytes
Connected to server localhost:12345
Last filter:  matching 0 results
```
The last filter was removed, so should now be empty. By checking the log again:
```bash
more query_log.txt 
```
Output:
```
Total filters: 0               
```
The query logfile is still there, but shows zero filters. Let's make sure we can still properly add new ones (as opposed to adding one when no logfile existed, like we did when the program first started):
```
Enter choice: 3
Enter filter query as a string with fields separated by commas (i.e. username=Alice, score>4, score<9.5)
Valid fields: username (client's username), IP (client IP), server (server name/IP), port (server port), accessTime (as an integer), dataSent (bytes sent by client), dataReceived (bytes sent to client), score (floating point)
Valid operators: =, <, >, <=, >=, !=
Enter filter: new filter
Updated query log. New size = 43 bytes
```
Everything looks good here. Now, instead of removing the filter, let's just clear the queries/logfile completely by selecting menu choice #6:
```
Enter choice: 6
Connected to server localhost:12345
Last filter: new filter matching 0 results
```
We can see that the filter is again empty, but this time if we check the file system we will see that the query logfile is no longer present (just as when the program first starts).

This testing process is important. All developers should try to both test common use cases, as well as a complete of a set of broad test cases and edge cases as possible, as not all bugs are seen in normal operations.
