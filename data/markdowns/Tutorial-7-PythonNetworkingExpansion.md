# Python Networking Expansion
Reference source files: `ClientPython.py`, `ServerPython.py`

This tutorial will complete the functionality of the client, making it usable (when paired with an equally functional server, which will be written later) for real-world capabilities by adding the networking and logic code necessary for it to exchange query and log data with a server. This will also allow us to explore additional features and nuances of networking in Python.

## Using SSL to secure connections
Before we start changing the client significantly, we should cover using encrypted network connections. While this tutorial primarily uses unencrypted network connections to make learning and debugging easier, as well as to allow the use of tools like `nc` and `wireshark`, in the real world we will want to encrypt most, if not all, of our network connections.

To create a server.crt (certificate) and server.key (private key) file, we can use OpenSSL, a widely used software library for applications that secure communications over computer networks.

First, we need to generate a private key:
```bash
openssl genrsa -out server.key 2048
```
This command generates a 2048-bit RSA private key and writes it to a file named `server.key`.

Next, we need to generate a self-signed certificate, which is a public key that can be shared, based on the private `server.key`:
```bash
openssl req -new -x509 -key server.key -out server.crt -days 365 -subj "/CN=localhost"
```
This command generates a self-signed certificate for the hostname `localhost` that is valid for 365 days. The certificate is written to a file named `server.crt`.

To use these certificates in our code, we will establish an encrypted SSL connection from the client to the server. First, we need to `import` the `ssl` module at the top of our Python file:
```python
import ssl
```
Next, we will define a new function `create_ssl_socket()` to create an SSL-encrypted `socket` that "wraps" a normal `socket`. This means that when we read from or write to the "outer" wrapped `socket`, it automatically encrypts any data written then sends the encrypted data over the original "inner" `socket`. It also automatically decrypts any data read by reading from the "inner" `socket` and then decrypting the result. This allows us to use the "outer" wrapped `socket` and have it handle all the SSL encryption/decryption for us without having to worry about it.

A `ssl.SSLContext` object has a method called `.wrap_socket()` that will return such as wrapped socket, given a `socket` to wrap as its first parameter. It also accepts additional parameters to specify options, such as a `server_hostname` parameter that specifies the hostname of a server to connect to (in this case, our _global variable_ `SERVER_NAME`).

In order to call `.wrap_socket()`, we first need a `ssl.SSLContext`. An SSL context is an environment that holds various settings, certificate chains, and configurations for SSL/TLS operations. Python makes a default context available that is automatically configured with settings suitable for most applications, designed to be a reasonable balance between compatibility and security, through the `ssl` module's method `ssl.create_default_context()`. If a specific configuration is desired, we could instead call `ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)` to create our own custom `SSLContext` and manually configure all of these settings and certificate trust chains.
```python
def create_ssl_socket(sock):
    context = ssl.create_default_context()
    return context.wrap_socket(sock, server_hostname=SERVER_NAME)
```
We can now create a new `start_client` function called `start_client_simple_ssl()` that calls `create_ssl_socket()` to get a wrapped socket, before sending and receiving data over it:
```python
def start_client_simple_ssl():
    with socket.create_connection((SERVER_NAME, SERVER_PORT)) as sock:
        with create_ssl_socket(sock) as ssock:
            send_data_simple(ssock)
            receive_data_simple(ssock)
```
Finally, we need to change the main line at the bottom of the Python client from `start_client()` to `start_client_simple_ssl()` so that this version is used.

On the server side, we need to also modify `ServerPython.py` to utilize SSL. Again, the first step is to `import` the `ssl` module at the top of `ServerPython.py`:
```python
import ssl
```
We can then create a "wrapped" `socket` much like we did on the client size, inside a new `setup_ssl()` function that we write for the server:
```python
def setup_ssl(sock):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    return context.wrap_socket(sock, server_side=True)
```
Note a few differences here between the server and the client. First, we need to pass `ssl.Purpose.CLIENT_AUTH` as an argument to `ssl.create_default_context()` to let it know that we want the `SSLContext` to be for a server (whose purpose is to authenticate a client, thus the name `CLIENT_AUTH`). If we do not specify this argument, the default value is `ssl.Purpose.SERVER_AUTH` which would be used for a client trying to authenticate a server. We also need to load the server's certificate and private key from the specified files (`server.crt` and `server.key`), which we can do by calling the `ssl.SSLContext` method `.load_cert_chain()` with the above parameters. Finally, we need to pass `server_side=True` when we call `wrap_socket()` to let it know that this is the server's side of the `socket`. Note that we do not need to specify `server_hostname` like we did on the client, since that is only used by the client side (to specify/verify that the correct hostname, and thus the correct SSL certificate is used during the handshake process).

But wait-- why are we creating a new `ssl.SSLContext` every time a client connects to the server? This could create extra overhead, which is small but could impact performance across thousands of clients/connections. Since we want all connections to use the same SSL parameters, it would be better to only create the `ssl.SSLContext` once, and then reuse it for each connection (note that `.wrap_socket()` will still generate unique encryption keys for each SSL connection, so connections will not be able to eavesdrop on each other).

## Singletons
To implement this behavior, we will define a `SSLContextSingleton` class. the _Singleton_ design pattern ensures that only one instance of the class is ever created (no matter how many times it is used/called) and provides a global point of access to that instance. This way, every new connection will utilize the same single `SSLContextSingleton` class, using the same `ssl.SSLContext` to create the new wrapped socket for that connection. First, we define the class and create a _class variable_ `_instance` to hold the single instance of the `SSLContextSingleton` class. Initially, it is set to None, indicating that no instance has been created yet:
```python
class SSLContextSingleton:
    _instance = None
```
Next, we define a `__new__()` method for our class. Note that `__new__()` is already a built-in method provided to all classes in Python, that returns a new instance of the class (before calling `__init__()`). Since we are defining our own `__new__()` method, it _overrides_ the built-in `__new__()` method, meaning it will no longer be called (and so no object will be created by default). `__new__()` takes its `self` instance as the first parameter, and variable argument lists as additional parameters:
```python
    def __new__(cls, *args, **kwargs):
```
Next, we check to see if `cls._instance` is `None`, meaning that the is the first time anyone has asked for a `SSLContextSingleton` since the progrm started. If `cls._instance` exists, we simply return it, since it already exists, and thus no new object is created, we are just returning the existing `_instance` no matter how many times `__new__()` is called. However, if there is no existing `_instance`, then we need to create it. The first thing we do is call the _superclass_ `__new__()` method to create the base object. While `SSLContextSingleton` does not explicitly _inherit_ from another class, **all** Python classes automatically inherit from the base Python _object_, which will implement `__new__()`. Once this _object_ exists and is stored in `cls._instance`, we initialize it with a `ssl.create_default_context` and call `.load_cert_chain()` to load the specified certificates, using the same parameters we previously did in the `setup_ssl()` function above:
```python
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            cls._instance.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        return cls._instance
```
Now, we can modify `setup_ssl()` to use this _Singleton_ class when calling `.wrap_socket()`:
```python
def setup_ssl(sock):
    ssl_context = SSLContextSingleton()
    return ssl_context.context.wrap_socket(sock, server_side=True)
```
This ensures that only a single `ssl.SSLContext` is created no matter how many times `setup_ssl()` is called.

We can then call `setup_ssl()` to create an encrypted "wrapped" socket in any (or all) of our `handle_new_connections` functions, by adding it after the `.accept()` call:
```python
                conn, addr = sock.accept()
                print("Received new connection from ", addr)
                conn = setup_ssl(conn)
```
At a minimum, do this inside `handle_new_connections_thread_pool()`, but it can be done in every variation fo `handle_new_connections` if desired. This uses the _Singleton_ design pattern to create a new wrapped socket every time we get a new connection from `sock.accept()`, without having to create a new `ssl.SSLContext` each time.

Now, we can test the SSL code:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client:
```bash
python3 ClientPython.py
```
ClientPython Output:
```
Starting client...
Traceback (most recent call last):
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 378, in <module>
    start_client_simple_ssl()
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 337, in start_client_simple_ssl
    with create_ssl_socket(sock) as ssock:
  File "/usr/local/linuxexamples/basic/ClientPython.py", line 306, in create_ssl_socket
    return context.wrap_socket(sock, server_hostname=SERVER_NAME)
  File "/opt/anaconda3/lib/python3.9/ssl.py", line 500, in wrap_socket
    return self.sslsocket_class._create(
  File "/opt/anaconda3/lib/python3.9/ssl.py", line 1040, in _create
    self.do_handshake()
  File "/opt/anaconda3/lib/python3.9/ssl.py", line 1309, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate (_ssl.c:1129)
```
Whoops, that's not good. Your output may vary slightly, but regardless we have an `SSLCertVerificationError` `Exception` during the SSL handshake process. This means that the client's `SSLContext` is unable to verify the server's SSL certificate. This typically occurs because the certificate was not signed by a trusted Certificate Authority (CA), the certificate is expired, the hostname in the certificate does not match, or it is otherwise invalid. In this case, we are told specifically that it is due to a self signed certificate, meaning that a trusted CA did not sign the server's certificate (which makes sense because we just generated it ourselves).

## Certificate Verification
The default `SSLContext` returned by `ssl.create_default_context()` has a _member variable_ `check_hostname` set to `True` and a _member variable_ `verify_mode` set to `ssl.CERT_REQUIRED`, which enhances the security of the SSL/TLS connection by ensuring that the server's identity is properly verified. When `check_hostname` is set to `True`, the `SSLContext` will verify that the hostname of the server matches the hostname specified in the server's SSL certificate. This is an important security measure to prevent man-in-the-middle attacks, where an attacker could intercept the connection and present a fraudulent certificate.

For example, if you are connecting to `https://example.com`, the `SSLContext` will check that the certificate presented by the server is indeed issued to `example.com`. If the hostname in the certificate does not match, the connection will be aborted.

When `verify_mode` is set to `ssl.CERT_REQUIRED`, the `SSLContext` will require a valid SSL certificate from the server. The client will verify the server's certificate against a list of trusted CAs to ensure its authenticity. This setting ensures that the server is who it claims to be and that the connection is secure. If the server does not present a valid certificate, the connection will be aborted.

But we never had a trusted CA sign `server.crt`. So this code is likely failing due to the certificate not being considered "valid" by the above criteria.

We can test this theory by disabling certificate verification for the client. We do this by explictly modifying our SSL `context` in `ClientPython.py` to set the `verify_mode` to `ssl.CERT_NONE`, which indicates that the client should not validate the server's certificate. It will still use the certificate provided by the server for encryption, it just won't check to see if it is valid. It won't check to see that it is properly signed/trusted, if it's hostname matches, or even if it is expired. As such, this is not recommended for production use as it can cause serious security issues, but it is useful in debugging the current issue. If we do this, we also need to set `check_hostname` to `False`, since if `check_hostname` is `True` it will automatically change the `verify_mode` to `ssl.CERT_REQUIRED`:
```python
def create_ssl_socket(sock):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context.wrap_socket(sock, server_hostname=SERVER_NAME)
```
Let's try testing again:
```bash
python3 ServerPython.py
```
ServerPython Output:
```
Starting server on 'localhost' port 12345
```
In another tab/window/terminal, run the client:
```bash
python3 ClientPython.py
```
ClientPython Output:
```
Starting client...
Received: b'Hello, world'
```
ServerPython Output:
```
Received new connection from  ('127.0.0.1', 52167)
Received: b'Hello, world'
Total messages received: 1
```
Now it works, verifying that the issue was indeed due to the self-signed certificate. We can also capture the network traffic using wireshark if desired to verify that it is indeed sent encrypted, rather than as plaintext.

While this works for testing, for a production server, we would typically use a certificate issued by a trusted Certificate Authority (CA). If we do not have a CA to use, there is a widely-used, free, non-profit CA called *Let's Encrypt* available at https://letsencrypt.org/getting-started/. This public CA can be used to sign a certificate so that it passes the verification process.

In addition, we could theoretically create our own local CA certificate and then use that to sign `server.crt`. This approach works for testing and internal deployments but is not generally viable for public/mass market software, since most people will not have (or trust) a CA that we just made up. However, if we did have such a CA (perhaps that we deploy to our own enterprise network), we could call `context.load_verify_locations(<our CA certificate path>)` to have our client utilize it for certificate verification purposes.

For now, let's change the last line of `ClientPython.py` back to `start_client()` so we can work on the full featured client again.

## Sending and Receiving Binary Data
In order to complete the implementation of menu choice #1 (Upload log file to server), we need to implement the `upload_logs()` function. Since sometimes we will be uploading logs and other times we will be sending queries to the server, we need a way to differentiate what sort of data we are sending, so that the server can act appropriately in each case.

A simple way to do this is the send a predefined command code or message to the server before transmitting any other data. We will define a special `class` near the top of the file (it can appear anywhere in the source file as long as it is before it is used) called `SERVER_COMMANDS` which will define these options:
```python
class SERVER_COMMANDS:
    UPLOAD_CMD = 0x0001
    QUERY_CMD = 0x0002
```
Since we only have two types of data we are transmitting to the server, we only need to define two commands here, but we could easily expand the protocol by defining more later. Each is given a numeric value, which will be the 2-byte value that is actually transmitted over the network to determine the use case. We could define a larger size to allow for larger numbers of commands, or use a 1-byte value (or even just one single bit that was combined with other data like the size of the transmission) to minimize bandwidth usage, since we only have two commands, but this is a good starting point.

The first thing our `upload_logs()` function will do is to call `sock.sendall()` to transmit the 2-byte `SERVER_COMMANDS.UPLOAD_CMD` to the server, letting it know that an upload is coming. It will then follow that with a 4-byte length that contains the number of log entries in the log that we are uploading. We can then transmit the logs and the server knows how many log entries to expect. When transmitting the 2-byte command code and the 4-byte length, we also need to take into account the _endianess_ of this data.

### Endianess
_Endianness_ refers to the order in which bytes are arranged within larger data types (such as integers) when stored in memory or transmitted over a network. There are two main common types of endianness:
- Big-endian: The most significant byte (the "big end") is stored or transmitted first. This is also the way that hexidecimal numbers are generally written in human language documentation. For example, the decimal number 415 in hex is 0x019F, which would be represented in a big-endian data stream as: `01 9F ...` Historically, many architectures were big-endian (including the Motorola 68000, PDP-10, and IBM System/360) and TCP/IP uses big-endian for all network data transmittion.

- Little-endian: The least significant byte (the "little end") is stored or transmitted first. For example, the decimal number 415 in hex is 0x019F, which would be represented in a little-endian data stream as: `9F 01 ...` The x86 architecture is little-endian.

Some processors can operate in either mode, such as MIPS, SPARC, PowerPC, and most ARM processors, although usually the operating system dictates the use of one or the other. Some platforms can even alternate endianess per instruction, or mix endianess, but most uses we will encounter are either big-endian or little-endian.

Since our Python code may run on many different architectures, we want it to work properly in either case. In addition, our client and server might be running on platforms with opposite endianess. Therefore, we need to make sure our data is sent to the network in big-endian format. Thankfully, the socket object provides methods for this. We can call `sock.htons()` to convert a number from our host computer's endianess to a 2-byte chunk of data in network byte order (which is big-endian) . `htons` stands for Host TO Network Short. Similarly `htonl` or Host TO Network Long can be used for a 4-byte number. These methods will work regardless if our host is little-endian (in which case it will reverse the byte order of the data) or big-endian (in which case it doesn't actually do anything):
```python
def upload_logs(sock, logs):
    # send a 2-byte integer with the command
    sock.sendall(sock.htons(SERVER_COMMANDS.UPLOAD_CMD))
    # send a 4-byte integer with the number of log entries
    upLen = sock.htonl(len(logs))
    sock.sendall(upLen)
```
Once we have converted our command and number of log entries to network byte order, we call `.sendall()` to transmit them to the server.

Next, we loop through the `PriorityQueue` `logs` parsing one `logEntry` at a time in order of the queue through `.dequeue()`, until the length of the `PriorityQueue` `logs` is zero (meaning it is empty, and there are no more log entries to send):
```python
    while len(logs) > 0:
        logEntry = logs.dequeue()
        print('Uploading log entry: {}'.format(logEntry))
        # send log entry to server
        send_log_entry(sock, logEntry)
```
For testing and debugging, we will print out each `logEntry` before sending it with the function `send_log_entry()`.

### Data Serialization
Next, we need to actually write the `send_log_entry()` function. First, let's review what information is in a log entry and figure out the best way to send it. We recall that each log entry was parsed into a Python _dictionary_ that looks something like:
```python
{
    'username': 'Alice',    # string, variable length
    'IP': "10.0.0.9",       # string, variable length
    'port': 8080,           # 2-bytes (short), fixed length
    'accessTime': 100,      # 4-bytes (long), fixed length
    'dataSent' : 64,        # 4-bytes (long), fixed length
    'dataReceived' : 1024,  # 4-bytes (long), fixed length
    'score' : 1.0,          # 4-bytes (float), fixed length
    'server': "10.2.1.5"    # string, variable length
}
```
Some of our data fields are variable length (like strings), while others have a fixed size (like the numbers). While we could theoretically try to represent the `IP` address and `server` as a fixed length value, there are some issues with this. First, `server` can also be a hostname like `localhost` or `tutorial.example.com`. Second, while the `IP` example above could be coded into a 4-byte hex value relatively easily, this would not necessarily work for a IPv6 address, unless we used 16 bytes, which is doable but would be a waste of space for many addresses.

For the numerical data fields, we need to determine how big each needs to be. TCP and UDP explicitly specify 2 bytes for their ports, so we only need 2 bytes for that field. For most other values, 4 bytes is a good starting point, although if we wanted to support extremely large amounts of data transmission in the logs (>4GB) or time indicies that span more than 136 years in seconds (or for shorter periods if in milliseconds or nanoseconds), we might want to consider using 8 bytes or even more.

In addition, `score` is a floating-point number. We will store this using 4 bytes (which can represent around 7 decimal digits of precision, so should be plenty for our use case), but if we wanted additional floating point precision, we might want to consider a larger size.

For the variable-sized data fields (like _strings_), we will first send a 2-byte length for each _string_, so that the server knows how long each _string_ is. For example, to transmit the _string_ `'Amy'`, we would send the following bytes (shown in hex), in order:
```
00 - Most Significant Byte of string length 3
03 - Least Significant Byte of string length 3
41 - The character 'A'
6D - The character 'm'
79 - The character 'y'
```
Since we are sending 3 strings at once, we will send all 3 _string_ lengths (6 bytes total), followed by all 3 strings themselves. We send all of the lengths first (instead of one at a time) so that the server knows exactly how big the entire rest of the log entry is.

In order to send the _strings_ as binary data in Python (rather than as text), we need to _encode_ them first to a byte format, such as UTF-8 (which is an encoding standard backwards-compatible with ASCII that allows representation of any Unicode character). We can call the _string_ method `.encode('utf-8')` on any _string_ in Python to get the UTF-8 byte data that corresponds to that _string_. To make our code simpler, we will handle and transmit all the _strings_ together (even though the various data fields containing _strings_) are not contiguous. The receiver will need to assign them to its own data structure anyway, and we are also writing the receiver code, so there is no harm to changing the order in which we transmit these fields to make our code easier to write and understand (although if we were operating with a server that expected them in their naturally occurring order, we would not be able to do this and would need to code to that server's standard instead):
```python
def send_log_entry(sock, logEntry):
    # Pack the username, IP, and server as separate fields
    username = logEntry['username'].encode('utf-8')
    ip = logEntry['IP'].encode('utf-8')
    server = logEntry['server'].encode('utf-8')
```
After encoding each _string_ into UTF-8 byte data, we store each set of bytes in an appropriately named _local variable_ (which is a Python `bytes` object).

We could just call `.sendall()` to send each data field separately. This would work, but it could result in wasted space and might be slower, since most of our data fields are fairly small and TCP packets contain overhead, so sending many small packets might result in lower performance (although some operating system network caches and algorithms may compensate for this to some degree). To avoid this, we will _pack_ all of our data fields for a single log entry into a single block of data before sending.

Python provides the `struct` module to assist with _packing_ and _unpacking_ data to various binary data buffers (technically, also a Python `bytes` object). Before finishing our function, we need to `import` the `struct` module at the top of our source code:
```python
import struct
```
Now, we can use the `struct` module method `struct.pack()`, which takes as its arguments a _format string_, followed by each piece of data to be _packed_, as specified in the _format string_.

The _format string_ specifies the layout of the data in the packed buffer by listing the elements in order as a _string_, using various characters to represent different data types:

- `!`: This character specifies that the byte order of the resulting data stream will be network byte order (big-endian). By including this symbol `.pack()` automatically takes care of the endianess conversion for us, so we do not need to call functions like `.htons()`
- `H`: This represents an unsigned short (2 bytes).
- `I`: This represents an unsigned int (4 bytes).
- `f`: This represents a float (4 bytes).
- `s`: This represents a string of bytes. The length of the string is specified by the preceding number (i.e. `5s` for a 5 character string). If a string is longer or shorter than the specified length, it will be truncated or padded with null '\0' bytes at the end to match the specified length.
- Several other symbols are supported. See https://docs.python.org/3/library/struct.html#format-strings for complete documentation.

So for example, `struct.pack("!H10sI", len(userString), userString, 123456)` would return a Python `bytes` object in network (big-endian) byte order, that contained a 2 byte integer containing the length of the _string_ `userString`, followed by a 10 character version of `userString` itself (truncated or with padding if it is not already exactly 10 characters long), followed by a 4 byte integer containing the number 123,456.

Applying this to our `logEntry` data fields, we can continue writing the `send_log_entry()` function by first defining the _format string_ to use for _packing_, using the _string_ `.format()` method to fill in the proper sizes for each _string_:
```python
    # Create a format string for the struct
    fmt = '!HHH{}s{}s{}sHIIIf'.format(len(username), len(ip), len(server))
```
When we use this _format string_ `fmt` to call `struct.pack()`, this produces a network byte order `bytes` object, containing the length of `username`, followed by the lengths of `ip` and `server`, followed by the UTF-8 encodings of these 3 _strings_, followed by the 2-byte port number from `port`, followed by 4-byte integers for `accessTime`, `dataSent`, and `dataReceived`, followed by the 4-byte float `score`:
```python
    # Pack all the data into a single binary structure
    packed_data = struct.pack(fmt,
                                len(username), len(ip), len(server),
                                username, ip, server,
                                logEntry['port'],
                                logEntry['accessTime'],
                                logEntry['dataSent'],
                                logEntry['dataReceived'],
                                logEntry['score'])

    # Send the packed data
    sock.sendall(packed_data)
```
Finally, we send the _packed_ `bytes` object data by calling `.sendall()`. When reviewing and trying to understand the line setting `fmt`, it may be helpful to match each character specifier against the corresponding arguments passed to `struct.pack()`. Encoding structured data in this way, commonly done when sending data over a network or writing it to a file, is known as _data serialization_.

### Data De-serialization
Since we will also need to receive log entry data back from the server for other functionality, let's also write a `recv_log_entry()` function using a similar _format string_. This function will receive the same format of log entry data that was sent in `send_log_entry()`, and then reconstruct a _dictionary_ object from the _serialized_ data, a process also known as _de-serializaton_. But there is no equivalent to `.sendall()` that we can call-- `recv()` may return fewer bytes than we ask it for. How do we ensure that we wait until the entire log entry has arrived?

We will write a helper function `recv_all()` that acts similarly to `.sendall()`, repeatedly calling `.recv()` until we have reached the full expected length, or until the socket is disconnected. Since it is our function, rather than a method of the _socket object_, we will need to pass it both the socket to use, as well as the number of bytes we want to wait for:
```python
def recv_all(sock, length):
```
This function will start with an empty stream of bytes, in a Python `bytes` object. In Python we can create a constant valued `bytes` object by simply prepending the character `b` before the quotes we use around a _string_. For example, `s = 'Amy'` sets the variable `s` to the text _string_ `Amy`. However, `s = b'Amy'` instead sets the variable `s` to the binary data `bytes` containing the ASCII encoding of the text `Amy`, which in hex looks something like `41 6D 79`. (For ASCII characters this is identical to the UTF-8 encoding, however UTF-8 also supports numerous non-ASCII characters, such as non-Roman foreign characters).

We will define a _local variable_ `data` to hold our received data, and initialize it to an empty `bytes` object (containing 0 bytes), using this syntax on an empty string:
```python
    data = b''
```
Next, we will loop while our received data buffer `data` is less than `length` in size. Each time through the loop we will call `sock.recv()` using the numbers of bytes still needed (`length` minus the size of `data` so far), storing the number of bytes received on this iteration of our loop in a _local variable_ `more`:
```python
    while len(data) < length:
        more = sock.recv(length - len(data))
```
If `more` is ever empty, this means the connection was closed, so we need to stop our loop (or else it will wait forever and the program will hang). If this happens we will `raise` an `Exception` of type `EOFError` to indicate we are waiting for more data, but there is nothing left to read. If `more` is not empty, then the `.recv()` returned at least some data, so we will append this new data to our received data buffer `data`:
```python
        if not more:
            raise EOFError('Socket connection broken')
        data += more
    return data
```
Once the loop has completed the buffer `data` now is of size of `length` so we have all the data we were expecting, and can `return` the full received data buffer `data`.

But how do we know how many bytes to pass to `recv_all()` in the first place, since we do not know how long the 3 _strings_ will be until we read in their lengths? Because of this, we need to read in the _string_ lengths first. For efficiency, we will read in all 3 lengths at once. We will then be able to determine the full length of the log entry, including the 3 variable-length _strings_.

We will start by declaring our `recv_log_entry()` function, which takes the connected socket as its only argument, and creates a _format string_ of `!HHH` which specifies that we want to parse 3 2-byte numbers in a row, all in network byte order (big-endian):
```python
def recv_log_entry(sock):
    # Receive the length of the username, IP, and server fields
    lengths_fmt = '!HHH'
```
We can then call our `recv_all()` function with the size of these 3 numbers. While we know that this is 6 bytes in total (2 bytes each), it is a better practice to call the `struct` method `struct.calcsize()` and pass it the _format string_ `lengths_fmt`. This method will automatically determine the size of the data specifies by the _format string_, so the code will still work without modification if we later modify the _format string_. If we hardcoded the length as 6, we (or maybe even someone else updating the code years later) would need to remember to update this 6 to a new value when changing the _format string_:
```python
    lengths_data = recv_all(sock, struct.calcsize(lengths_fmt))
```
Once we have these 6 bytes read in to `lengths_data`, we can call `struct.unpack()` to parse it into _local variables_ containing the 3 corresponding string lengths:
```python
    username_len, ip_len, server_len = struct.unpack(lengths_fmt, lengths_data)
```
Now, we can create a format string for the rest of the data in the log entry (all of the actual data fields themselves). Here, we use the same strategy as in `send_log_entry()`, but using the compact `f''` notation we learned, instead of `.format()`:
```python
    # Create a format string for the struct with the received lengths
    fmt = f'!{username_len}s{ip_len}s{server_len}sHIIIf'
```
Now, we can use our `fmt` _format string_ to calculate the length of the rest of the data, and pass it to `recv_all()` to get the rest of the log entry from the network socket. Then, we can use this same `fmt` _format string_ to `unpack()` the received data buffer into a big _tuple_ containing each of the log entry data fields: 
```python
    # Unpack the data from the socket
    data = recv_all(sock, struct.calcsize(fmt))
    unpacked_data = struct.unpack(fmt, data)
```
To get the _string_ data out of the _tuple_ `unpacked_data` as text _strings_, rather than as a stream of bytes, we need to `.decode()` this data, in the reverse of the way we `.encode()` it to UTF-8 before sending:
```python
    # Extract the fields from the unpacked data
    username = unpacked_data[0].decode('utf-8')
    ip = unpacked_data[1].decode('utf-8')
    server = unpacked_data[2].decode('utf-8')
```
Finally, we can create a _dictionary_ for the log entry, with each field from `unpacked_data` in the right place, then `return` the completed log entry _dictionary_:
```python
    # Create a dictionary with the extracted fields
    logEntry = {
        'username': username,
        'IP': ip,
        'port': unpacked_data[3],
        'accessTime': unpacked_data[4],
        'dataSent': unpacked_data[5],
        'dataReceived': unpacked_data[6],
        'score': unpacked_data[7],
        'server': server
    }

    return logEntry
```

## Querying the Server
Next, we will implement menu choice #2 in `do_menu()` to submit a new query to the server. We can put this `elif` clause in between the choice for #1 and #3. First, we call the `get_filter_string()` we previous wrote to get the query from the user, then we will pass our socket along with this query string to a new function we create called `submit_query()` that returns the results of this query. We then will save both the results and the query string itself on `filterStack` by calling `.push()` do support undos later. Finally, we need to write the query string to the query log file by calling the `save_last_query_action()` function we previously wrote:
```python
            elif choice.startswith('2'):
                curFilterString = get_filter_string()
                curResults = submit_query(sock, curFilterString)
                filterStack.push((curResults, curFilterString))
                save_last_query_action(curFilterString)
```
Now we need to write the `submit_query()` function. The first argument will be the socket we use to communicate with the server, and the second argument will be the query string to send. We start by sending `QUERY_CMD` from the `class SERVER_COMMANDS` (rather than the `UPLOAD_CMD` we sent in the `upload_logs()` function) to let the server know this is a query, rather than a log upload, again making sure we use network byte ordering. Next, we `.encode()` the query text _string_ and store it in the _local variable_ `queryData`. Then we use `.sendall()` to transmit the length of `queryData` as a 4-byte integer, so the server knows how much data to expect. We then call `.sendall()` again to send `queryData` itself:
```python
def submit_query(sock, query):
    sock.sendall(sock.htons(SERVER_COMMANDS.QUERY_CMD))
    queryData = query.encode('utf-8')
    sock.sendall(sock.htonl(len(queryData)))
    sock.sendall(queryData)
```
Why don't we need to worry about endianess when we transmit `query`? Normally we would, but UTF-8 encoding is a string of individual bytes, so there are no multi-byte variables that would be different between endianess. That is, 0xFF8A could appear as `FF 8A` or `8A FF` depending on endianess. However, a single byte `8A` will be the same whether big-endian or little-endian. UTF-8 encoding is one byte at a time (even when encoding larger types) so there is no endianess issue like when we send a multi-byte integer.

After sending the query to the server, we will wait and listen for a response, which should be the results of the query. We will first listen for a 4 byte integer containing the number of results, using `sock.ntohl()` to change the 4 bytes of data received to host byte order (Network TO Host Long). Once we know the number of results (which we store in a _local variable_ `num_results`), we create a new _list_ named `results` to store these results in, then for each one, we call `recv_log_entry()` to get the entry, then `.append()` it to the _list_ `results` and `return` it:
```python
    num_results = recv_all(sock, 4)
    num_results = sock.ntohl(num_results)
    results = []
    for i in range(num_results):
        logEntry = recv_log_entry(sock)
        results.append(logEntry)
    return results
```
Alternatively, we could have used a different data structure, such as `ds.HashTable`, to index the log entries using a specific field, so that they could be accessed and filtered more quickly, if we expected that field to be used frequently.

## Optimizing Regular Expression Processing
We also need to finish implementing the `apply_filter()` function that we previously left empty. This will allow us to actual filter the results of the query we get back from the server, according to multiple user-specified criteria.

We will utilize the same `re` module was used before to help parse the filter. First, we need to make sure to `import` it at the top of our source code file:
```python
import re
```
Rather than calling `re.match()` as we did when parsing the server's command line paramaters, we will build a _regular experession object_ that can be reused to perform our regular expression matching operations by calling `re.compile()` with the regular expression string as the sole parameter. Compiling the pattern once and reusing it is more efficient than rebuilding the pattern matcher every time we need to match it with `re.match()`. We will store this in a global variable near our other global declarations at the top of our source file:
```python
FILTER_PATTERN = re.compile(r'([a-zA-Z ]+)([=<>!]+)([^,]+)')
```
Let's break down the regular expression used above. Our filter strings obtained from the user through the `get_filter_string()` function consist of a series of comma-separated expressions, each consisting of a log entry data field, followed by some sort of comparision operator, follwed by the value to compare them to. For example, `score>4.0` or `username = Amy, accessTime>= 6000`. Names might include spaces in the middle, such as `Amy Brown`. We also want to support white space before/after the commas and comparison operators.

The above regular expression starts by matching One or more letters or spaces `[a-zA-Z ]+`. The plus sign means it should match one more more instances of the characters in the brackets `[]`. The `a-z` matches any lowercase letter from `a` to `z`, and the `A-Z` matches the capital letters, which the space afterwards matches a space character, allowing spaces to occur anywhere in this part of the matched substring. Next, it looks for a one or more comparison operators, consisting of a continuous sequence of the characters `=<>!` in the brackets `[]`. Since our first portion `[a-zA-Z ]+` included a space character, there can be spaces occuring before the comparison operators. Finally, the last portion `[^,]+` matches one of more instances of any character _other than_ a `,`. The carat `^` indicates the inverse of the expression that follows, so anything besides a commma will match this, including letters, numbers, and spaces. This portion of the matched sequence will therefore end when it either encounters a comma or the end of the _string_.

When we implement the `apply_filter()` function, we can now call `FILTER_PATTERN.findall()` with our filter string `filter_query` to extract the matches, which are returned as a list of _tuples_ that we store in the _local variable_ `matches`. We will also initialize an empty list to store the filtered results. For each element of the list to filter (which is passed in via the parameter `results`), we will iterate through and check that element (referring to it as `item` with a `for..in` construct):
```python
def apply_filter(results, filter_query):
    matches = FILTER_PATTERN.findall(filter_query)
    filtered_results = []
    for item in results:
```
First, since we have to make sure an item matches **all** provided criteria, we need to keep track of how many criteria we have left to match for each item, so we will store this value (derived from the size of the _list_ `matches`) in a _local variable_ `matchCount`. We then loop through each criteria using another `for..in` construct. For ease of use, instead of using a _tuple_ directly, we will use multiple variables to store the contents of the _tuple_ corresponding to each criteria in the _list_ `matches`, which are the data field, comparison operator, and value matched from the regular expression above:
```python
        matchCount = len(matches)
        for field, operator, value in matches:
```
For each criteria, we need to check if `item` matches it. First, we decrement `matchCount` to keep track of how many criteria we have left. When `matchCount` is zero, we are on the last criteria. Next, we need to `.strip()` the `field` and `value` portions of the criteria, since they might have spaces before or after them (as in our examples above). Note that since `operator` only matches the symbols themselves and no spaces, we do not need to `.strip()` `operator`:
```python
            matchCount -= 1
            field = field.strip()
            value = value.strip()
```
Next, we need to check if `field` (which is the first element of the _tuple_ from `matches`, corresponding to a log entry's data field name) is actually present in the _dictionary_ `item`. If not, we will `raise` a `ValueError` `Exception`. If it is present, we will store the corresponding value for that field in a _local variable_ `entry_value`:
```python
            if not field in item:
                raise ValueError("Field not found: {}".format(field))
            entry_value = item[field]
```
If `entry_value` is a _string_, we only support the comparisons `=` (equal) and `!=` (not equal). We can determine if `entry_value` is a type of _string_ by calling the built-in Python function `isinstance()`, which takes our variable as its first argument and the type to check as its second argument. If it is a _string_, we check the `operator` and then see if the condition is _not_ met. If the condition is not met, it breaks out of the inner loop because the criteria does not match. So for example, if our `operator` is `!=`, we only want to `break` out of the loop if `entry_value` is _equal to_ the criteria `value`. Note that calling `break` only breaks out of the innermost `for` loop, so it will still continue on in the outer `for` loop, to examine the next `item` in the _list_ `results`. On the other hand, if `item` matches the criteria, we want to continue to the next line of code:
```python
            if isinstance(entry_value, str):
                if operator == '=' and entry_value != value:
                    break
                elif operator == '!=' and entry_value == value:
                    break
```
If `entry_value` is an _int_ _(integer)_ or a _float_, it converts the filter `value` to a float and performs the appropriate comparison based on the `operator`, supporting additional operators, such as `>=`. If the condition is not met, it breaks out of the inner loop. Note that we use the built-in `float` casting function to force `value` to be converted to a _floating point_ number and Python's `float()` function returns a 64-bit _floating point_ number (in the default implementation), which is sufficient to represent both 32-bit _floats_, and 32-bit _integers_ which are all we transmit anyway, so we can use this for both the _int_ and _float_ case. If we instead were using larger numbers, we might need a separate `elif` clause for the _integer_ case:
```python
            elif isinstance(entry_value, int) or isinstance(entry_value, float):
                if operator == '=' and entry_value != float(value):
                    break
                elif operator == '!=' and entry_value == float(value):
                    break
                elif operator == '<' and entry_value >= float(value):
                    break
                elif operator == '>' and entry_value <= float(value):
                    break
                elif operator == '<=' and entry_value > float(value):
                    break
                elif operator == '>=' and entry_value < float(value):
                    break
```
If `entry_value` is not _int_, _float_, or _string_, we will catch it in an `else` clause at the end and `raise` a `ValueError` `Exception`:
```python
            else:
                raise ValueError("Invalid value type: {}".format(type(entry_value)))
```
If we did not `break` and no `Exception` has occurred in our loop yet (including the `Exception`s that would be triggered implicitly by Python if we tried to convert a bad `value` to a _float_, for example), then we have satisfied the current criteria and reached the end of this iteration through the inner loop. We will check `matchCount` to see if this is the last criteria to match, and if so, we will `.append()` `item` to the `filtered_results` _list_. Otherwise, the inner `for` loop will continue on, and repeat with the next criteria in `matches`. Finally, once we have iterated through every `item` in the original `results` argument, the outer `for` loop will exit, and we can `return` the completed `filtered_results` _list_ with all the items that matched every criteria:
```python
            if matchCount == 0:
                filtered_results.append(item)

    return filtered_results
```

We will not be able to test this code until we complete at least part of the corresponding server, in a future tutorial module.
