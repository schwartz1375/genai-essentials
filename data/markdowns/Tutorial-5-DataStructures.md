# Data Structures
Reference source file: `DataStructuresPython.py`

In this tutorial, we'll walk through the implementation of a few data structures in Python. While Python provides modules for many of these, understanding how to implement them yourself (and how other people commonly implement them) can be crucial for understanding how things work in Python. We will also learn how to implement classes in Python.

## Priority Queue
A priority queue is a special type of queue, much like the `Queue` class we saw, before, but where each element is associated with a numerical priority level. Elements with higher priorities are dequeued before those with lower priorities. If two elements have the same priority, they are dequeued in the order they were enqueued (FIFO - First In, First Out), like a normal queue.

We will implement a `PriorityQueue` class. Keeping all of the functions associated with using a `PriorityQueue` in a single class structure helps better organize our code, and make it easier to use in practice.

Declaring a class works somewhat like declaring a function, but we use the `class` keyword:
```python
class PriorityQueue:
    def __init__(self):
        self.queue = []
```
Much like we can declare functions inside of another function, we can also declare functions inside of a `class`, which are sometimes known as _member functions_, _class methods_, _class functions_, or simply _methods_. Python automatically passes the `class` object that a function is called from as the first argument to that function. Therefore the first argument to all of our _class methods_ will always be `self`, so we can use this argument to reference variables within the class. While we could theoretically use any valid name other than `self`, this naming is a standard Python naming convention and makes code easier to read and follow.

In this case, we declare the `__init__()` _method_, which initializes the priority queue by creating an empty list and assigning it to the _class variable_ `queue`. A _class variable_ is somewhat like a _local variable_, except it is valid anywhere in the scope of the `class` it is declared in, or can be referenced through the class. For example, if we have a `PriorityQueue` object called `pq`, its class variable `queue` can be referenced by `pq.queue`. However, in order to reference this from _within_ the class, such as in the `__init__()` function, we use the `self` argument passed in. Thus to initialize the `PriorityQueue` _class variable_ `queue` to an empty list, we say `self.queue = []`.

While such a _method_ is not mandatory, if a `class` contains a _method_ named `__init__()`, Python will automatically call this _method_ whenever anyone creates a new object of this `class`. This is very handy for doing initialization-related tasks and allocating memory if needed.

Next, we'll define the `enqueue()` _class method_ to add items to the `PriorityQueue`. This method takes two additional arguments after `self`: `item` and `priority`. This is not a special _method_ like `__init__()`-- both the _method_ and its arguments can be named whatever we like (but note that Python will still always set the first argument to the object itself).
```python
    def enqueue(self, item, priority):
        # insert item in priority queue based on priority
        # higher priority number = higher priority
        # if priority is same, then FIFO
        # if priority is different, then insert in order
        i = 0
        while (i < len(self.queue)) and (priority <= self.queue[i][1]):
            i += 1
        self.queue.insert(i, (item, priority))
```
We start by initializing an _local variable_ `i` to `0`, to be used as an index to the _class variable_ `queue` within this method. Each item in this list `queue` will be a _tuple_ consisting of the item and its priority (e.g. `(item, priority)`). We then iterate through `queue` to find the correct position to insert the new item (which is provided by the argument `item`) based on its priority (which is provided by the argument `priority`). If we have not yet reached the end of the list `queue` (i.e. `i < len(self.queue)`) and the `priority` of the new `item` is less than or equal to the priority of the current item at index `i` in list `queue` (i.e. `priority <= self.queue[i][1]`), we continue to the next item.

Once the correct position is found (our new `item`'s `priority` is greater than that of the next item in `queue`), we insert our new `item` and `priority` as a _tuple_ into `queue` at that position using `self.queue.insert(i, (item, priority))`. The first argument to the list method `.insert()` is the index `i` in the list at which we wish to place the new item/priority, and the second argument is the element to be placed in the list (in this case a _tuple_ consisting of `(item, priority)`).

Note that if the `while` loop terminated because we reached the end of the list `queue` (i.e. `i < len(self.queue)` is `False` because `i` now is equal to `len(self.queue)`), we will insert our new _tuple_ `(item, priority)` here. Since it is the last element in the list, we know that there is no element after it with a higher priority, and we would not have gotten to this point if it had been a higher priority than any of the other elements in `queue`.

Now, we'll define the `dequeue()` _method_ to remove and return the item with the highest priority from the `PriorityQueue`:
```python
    def dequeue(self):
        # remove item with highest priority from priority queue
        return self.queue.pop(0)
```
Since the _class variable_ `queue` is always sorted by priority (since we insert items in their proper place), the item with the highest priority is always the first item in the list. The list _method_ `.pop()` removes and returns the item in a list at the index provided in its first argument. Therefore, all we have to do is call `self.queue.pop(0)` to remove and return the 0th item in the list `queue` _class variable_.

Next, we will define a _method_ to get the number of items currently in the `PriorityQueue`:
```python
    def __len__(self):
        return len(self.queue)
```
The `__len__()` _method_ returns the length of the list `queue` using the built-in len function, which will return the number of items in our priority queue. Note that `__len__()` is another special _method_ name, like `__init__()`. If there is a `PriorityQueue` object named `pq`, and someone writes `len(pq)`, Python will automatically attempt to use a _class method_ named `__len__()` if one exists.

Finally, we will define a _method_ to clear the queue, and destroy all of its contents:
```python
    def clear(self):
        self.queue = []
```
To do this, all we need to do is set the _class variable_ `queue` back to an empty list. Python automatically destroys all of the old list elements that were previously in `queue` when we do this.

## Stack
A stack is a collection of elements that follows the Last In, First Out (LIFO) principle. This means that the last element added to the stack will be the first one to be removed. This is basically the inverse of what a standard queue (not a priority queue) does.

As before, first we declare the `Stack` class and declare an `__init__()` _class method_ to initialize a _class variable_ `stack` with an empty list to store our stack elements:
```python
class Stack:
    def __init__(self):
        self.stack = []
```

Next, we define the `push()` _method_ to add items to the stack. New items are added to the end of our list `stack`, also known as the _top_ of the stack (if you stack each new item on top of the previous, the newest will be at the top). Similarly, the first item in our list is also known as the _bottom_ of the stack. The `push()` _class method_ takes one additional parameter after `self`: the `item` to be added:
```python
    def push(self, item):
        # add item to stack
        self.stack.append(item)
```
Since the _class variable_ `stack` is a list, all we need to do to add it to the end of the list is call the list _method_ `.append()`.

Now, we define the `pop()` _method_ to remove and return the most recently added item from the stack (also referred to as the _top_ of the stack):
```python
    def pop(self):
        # remove last item from stack
        return self.stack.pop()
```
Since the stack follows the LIFO principle, the `pop()` _class method_ removes the most recently added item from the stack (which was added to the end of the list `stack`) using the list `pop()` _method_ of the list `stack`, which removes the last item in the list and returns it.

We also define a _method_ `popMany()` to remove and return multiple items from the stack at once, where the second argument `n` is the number of items to pop off the _top_ of the stack at once:
```python
    def popMany(self, n):
        # remove last n items from stack
        result = self.stack[-n:]
        del self.stack[-n:]
        return(result)
```
Again, since the newest items (the _top_) in the stack are at the end of our list `stack` _class variable_, all we need to do is remove the last `n` items from the end of the list `stack`. To do this, we can use a variant of the slicing feature of lists we learned previously.

`self.stack[-n:]` refers to the last `n` items of our list. The `-n` index tells Python to start from the `n`th item, counting _backwards_ from the end of the list. The lack of anything after the `:` operator tells Python to continue to the end of the list. For example, if `self.stack` is `[1, 2, 3, 4, 5]` and `n` is 3, then `self.stack[-3:]` will return `[3, 4, 5]`.

Using this syntax, our `popMany()` _method_ stores these last `n` items in a new list `result` and then deletes them from the list `self.stack` _class variable_ using the `del` keyword. Finally, we return `result` to the caller, with a list of the items that were just removed from the _top_ of the stack.

As before, we also define a _method_ using the special name `__len__()` to get the number of items currently in the stack:
```python
    def __len__(self):
        return len(self.stack)
```
All we need to do to implement this _method_ is to return the length of our _class variable_ `stack`.

Finally, we will also define a _method_ to clear the stack, and destroy all of its contents:
```python
    def clear(self):
        self.stack = []
```
Again, all we need to do here is set the _class variable_ `stack` to an empty list. Python automatically destroys all of the old list elements that were previously in `stack` when we do this.

### Stack Overflows
It is worth noting that using a Python list to implement our `Stack` class makes things easier but does have a performance cost, since Python lists result in memory being allocated or freed as the lists grow and shrink. Using a fixed-length array would allievate this need and could improve performance by eliminating the memory allocate steps, however it would also open us up to the possibility of _stack overflows_ (sometimes also called _stack overruns_). For example if our stack was the fixed size array of length 5: `[1, 2, 3, 4, 5]` and we wanted to add an additional item to the top of the stack, it could crash our program when we attempted to write past the end of the array. While Python would throw an _exception_ in this case, a language like C could end up overwriting critical program memory in this situation, creating potential security vulnerabilities. Similarly, if our fixed size array contained elements of 2 bytes each, imagine if instead of adding the last element `5` we added an item that was 8 bytes long, such as: `[0x0001, 0x0002, 0x0003, 0x0004, 0x9090909090905FC3]` (represented as hex). Since 6 of the bytes of the last element extend past the end of the fixed size array, this could overwrite other data or potentially even code, which is a potential vector for exploitation. By using Python lists, we avoid these issues and the security or stability consequences of stack overflows, since lists will grow dynamically and memory is allocated for a list element before adding it to the list, to ensure there is enough space to prevent overruns. It is still possible though to eventually add so many items that we starve the system for memory, which could have other consequences as programs run out of memory. We can prevent this by checking to see if we've hit some limit before adding a new item to the stack, for example in the _class method_ `push()`:
```python
    def push(self, item):
        # add item to stack if it does not exceed a defined max size
        if len(self.stack) < MAX_SIZE:
            self.stack.append(item)
        else:
            raise OverflowError("Stack overflow: cannot push item, stack is full")
```
The `raise` keyword manually triggers an _exception_ of the indicated type, if `stack` reaches the maximum size defined in the _global variable_ `MAX_SIZE`. This will cause the program to crash and exit, if it is not caught with something such as a `try... except` clause.

## Hash Table
A _hash table_ is a data structure that maps _keys_ to _values_ for efficient lookup (typically in an amortized _constant_ time order of magnitude, O(1)). The _keys_ are _hashed_ to generate an index, which determines where the corresponding _value_ is stored in the table. A Python _dictionary_ is an implementation of a _hash table_.

For example, say we want to store the _key:value_ pairs to represent various people's ages: {'Alice':21, 'Barry':58, 'Bob':37}. In this example, the _key_ is a person's name and the corresponding _value_ is that person's age. A very simple _hash function_ might just look at the first letter in the name and return a number (i.e. 1 for 'A', 2  for 'B', etc.). This _hash table_ would be divided into 26 "buckets" of data, one representing names that start with each letter of the alphabet. Therefore, this _hash table_ might look something like this:
```
Bucket #        Entries
1               ('Alice',21)
2               ('Barry',58), ('Bob',37)
...
```
In order to store or retrieve a particular entry, we just have to look at the first letter of the name, and we can quickly get the entries for the appropriate bucket. If there is only one item in a given bucket, things are quick and easy, we have our _value_. _Hash tables_ work well when this is the case, for example if you do not have many people whose names start with the same letter. Sometimes we can select the optimal number of buckets for a _hash table_ based on known characteristics of the data, like this.

If, on the other hand, we have Alice and Barry in our _hash table_ above, and then we try to add Bob, we get what is known as a _hash collision_, when two different _keys_ are hashed to the same "bucket" (bucket #2, in this case). To deal with these situations, we need a data structure inside each bucket to be able to find the appropriate _value_ in the bucket. We can do something naive and simple, like implement each bucket as a list and iterate through that list until we find the correct _(key, value)_ pair. Or we can do something more complex like have each bucket be its own _hash table_ that hashes on the 2nd letter in the _key_ (and its buckets being _hash tables_ that hash on the 3rd letter in the _key_, etc). These are trade-offs of simplicity and memory usage versus speed.

First, we define the `HashTable` class and its `__init__()` method which initializes it with a specified number of "buckets":
```python
class HashTable:
    def __init__(self, buckets):
        self.table = [None] * buckets
```
The `__init__()` _method_ creates a _class variable_ list called `table`. Instead of initializing it to an empty list, we want to initialize it to a list with a number of elements equal to the number of buckets. Each of these elements will initially be empty. To do this, we use the Python feature of being able to multiply a list by an integer. This takes a list `[None]` of length 1, which contains a single element `None` (which is an empty element), and expands this list to repeat `buckets` times. In other words, it makes a list of length `buckets`, where each element in that list is `None`. This essentially creates a list that contains `buckets` number of empty buckets.

To explore this more, let's define our _hash function_ as a _class method_:
```python
    def hash(self, key):
        # return hash of key
        return key % len(self.table)
```
The _hash()_ method takes a _key_, and returns a _hash_ of that _key_, that is, an index to the bucket that corresponds to that particular _key_. We implemented an extremely simple _hash function_ that simply takes the modulus of the _key_ with the number of buckets in the `HashTable`. This has the effect of essentially using a round-robin approach to matching _keys_ and buckets. For example, if we have a `HashTable` with 3 buckets, the following keys will correspond to these buckets (counting from 0):
```
Key     Bucket
---     ------
0       0
1       1
2       2
3       0
4       1
5       2
6       0
...
```
This works fine if our _keys_ are evenly distributed, so there are similar numbers in each bucket. However, not all data follows this sort of distribution. If 99% of our data ends up all in bucket 1, then our `HashTable` data structure is not very efficient and we lose most of the benefit. Ideally we want a _hash function_ that spreads our _keys_ out amongst the available buckets as evenly is possible, that is, a _hash function_ that has little to no pattern in correspondence between the value of the _key_ and the bucket number. It turns out that cryptographic _hash functions_ (also known as _secure hash functions_) work really well for this purpose, since they are specifically designed to eliminate this correspondence, to prevent anyone from being able to reconstruct the original _key_ given a _hash_ value, which makes them _collision-resistant_. Python provides many common _secure hash functions_, such as SHA-256, SHA3-256, etc. through the `hashlib` module.

Python also provides a generic _hash function_ that operates on most basic data types, such as strings, integers, tuples, and floating point numbers. The exact algorithm used by this _hash function_ is implementation-dependent, but it is often something like a polynomial rolling _hash function_ that iterates over the characters or digits in the string or number and combines their values (possibly also with a random seed or prime number) using a polynomial function. This default _hash function_ may allow some _collisions_ and is not cryptographically secure, but is still sufficiently variable to use for most _hash table_ implementations that are not relied upon for security and are just trying to spread _keys_ across buckets. Using Python's built-in _hash function_, we can rewrite the last line of our `hash()` method to reduce the likely number of collisions:
```python
        return hash(key) % len(self.table)
```
Note that we still apply the modulus function to the result of Python's built-in _hash function_, to ensure that it returns a result appropriate for the number of buckets in our `HashTable`. Also note that this _hash function_ supports many data types, while our original _hash function_ only worked on _keys_ that were integers.

Next, we define an `insert()` method to add a _key:value_ pair to our `HashTable`. For this example we are just going to implement each bucket as a list. This allows us to trade away performance, to get significant ease of implementation:
```python
    def insert(self, key, value):
        # insert value into table based on key, handling any collisions without losing data
        if (self.table[self.hash(key)] == None):
            self.table[self.hash(key)] = [(key,value)]
```
`insert()` takes two additional arguments, the `key` and `value` that we want to insert into the `HashTable`. First, we use `self.table[self.hash(key)]` to get the bucket that our _hash function_ associates with the given _key_. Then, we check to see if that bucket is empty. If it is, we set it equal to a new list that we create, with just the current `(key,value)` pair in it from `insert()`'s arguments.

If the bucket for our _key_ is not empty, then we first need to check to see if it is already in that bucket:
```python
        else: # bucket is not empty
            # check if key already exists
            for k,v in self.table[self.hash(key)]:
                if k == key:
                    # key already exists, replace value
                    v = value
                    return
            self.table[self.hash(key)].append((key,value))
```
We use the `for`...`in` construct from before to iterate through all _key:value_ pairs in our bucket. During each iteration through the `for` loop, the variable `k` will contain the _key_ and `v` will contain the _value_ for the current iteration. If `k` matches our new `key`, then we replace its _value_ with the new `value` passed in as an argument to `insert()`. After we replace it, we immediately return from the method, as we have already completed our work.

On the other hand, if the `for` loop successfully completes, that means we have iterated through the entire bucket and not found `key`. If this happens, we call `.append()` on our bucket (which is a list) to add the new `(key,value)` pair to the bucket. This last case is an example of a hash _collision_, since we now have at least 2 _keys_ that are used that are mapped to the same bucket.

We also define a `remove()` method to delete a _key:value_ pair from the `HashTable`:
```python
    def remove(self, key):
        # remove first value from table that matches key
        l = self.table[self.hash(key)]
```
As before, the first step is to retrieve the bucket from `table` that our _hash function_ maps `key` to. We store this bucket in the _local variable_ `l`.

Next we check to see if this bucket `l` is empty. If it is, we just return immediately because there is nothing to remove, just the bucket is empty:
```python
        if l == None:
            return
```
Note that we could also print an error message or raise an _exception_ here, if desired.

If the bucket `l` is not empty, we iterate through it as before:
```python
        else:
            for k,v in l:
                if k == key:
                    l.remove((k,v))
                    return
```
If we find `key` in the bucket during our `for` loop, we call `.remove()` on the bucket to remove that _key:value_ pair from the bucket. If not, that means there was no entry for `key`, so there was nothing in the bucket to remove, so no additional code is needed, since the function ends here anyway.

Next, we define a `get()` method to retrieve the _value_ associated with a given _key_:
```python
    def get(self, key):
        # return value from table based on key, or None if it is not found
        l = self.table[self.hash(key)]
```
As before, we start by retrieving the proper bucket for the given `key` using our _hash function_, and storing that bucket in the _local variable_ `l`.

If this bucket `l` is empty, the `key` is not in our `HashTable`, so we return `None` from our function to signify this:
```python
        if l == None:
            return None
```
Again, if bucket `l` is not empty, we iterate through the bucket using a `for` loop:
```python
        else:
            for k,v in l:
                if k == key:
                    return v
            return None
```
If we find `key` in bucket `l`, we return the _value_ `v` associated with it. If the `for` loop ends without returning, this means `key` was nowhere in bucket `l`, so we again return `None` to signify that `key` is not in the `HashTable`.

We also define a method to return the item at a particular index of the `HashTable`, based on where it is in the `HashTable` rather than on its _key_. We call this method `getnthitem()`, and it takes an additional argument `n` to specify the desired position:
```python
    def getnthitem(self, n):
        # return nth item in table
        count = 0
        for l in self.table:
            if l != None:
                for k,v in l:
                    if count == n:
                        return (k,v)
                    else:
                        count += 1
        return None
```
This method uses a `for`...`in` construct to iterate through the buckets in the _class variable_ `table` (storing the current iteration's bucket in the variable `l`). If a given bucket `l` is not empty, we then use a nested `for` loop to iterate through that bucket `l`. On each iteration through this inner `for` loop, we check to see if the current position in bucket `l` is the `n`th item in the `HashTable` (which we keep track of with the _local variable_ `count`). If it is, we return that _key:value_ pair. If not, we increment the local variable `count` and continue until `count` is equal to the position we seek `n`. If we get to the end of the entire `HashTable` and have not yet reached `n`, we return `None`.

Next, we define the special `__len__()` method to return the total number of items currently in the hash table:
```python
    def __len__(self):
        # count number of items in table
        count = 0
        for l in self.table:
            if l != None:
                count += len(l)
        return count
```
This method again iterates through each bucket in the _class variable_ `table`, but we do not need to count one by one here, we can instead add the length of each successive bucket to our running total `count`, which is much faster than iterating through each individual item in each bucket.

Finally, we define a method `clear()` to clear the hash table and dispose of all the associated memory:
```python
    def clear(self, buckets):
        self.table = [None] * buckets
```
As before, all we need to do here is set the _class variable_ `table` back to a list of empty buckets. Python automatically destroys all of the old list elements that were previously in `table` when we do this. Note that this method can change the number of buckets in `table` if a different number is passed in as the `buckets` argument.

## Unit Testing
To test our implementation of these data structures, we will use _Unit Tests_. Unit tests are a type of software testing where individual units or components of a program are tested in isolation. A unit, in this context, refers to the smallest testable part of a software application, typically a function, method, or class. The purpose of unit tests is to validate that each unit of the software performs as designed. This is in contrast to functional/integration testing, which verifies that the software functions as a whole according to the specified requirements and that different parts or modules work together correctly. Both forms of testing are important, as unit testing allows specific issues to be identified and isolated, while functional and integration testing allow us to make sure everything works together properly as well.

A _modular_ design, where functionality and data can be broken into separate functions or classes, makes it much easier for us to perform unit testing, as well as to modify one part while not affecting others, reuse these parts in other code, and to delegate out different parts of the overall development effort. This is in contrast to a _monolithic_ design, which is more like building a single large system, which can sometimes be simpler or more performant, but can make unit testing and tracking down bugs challenging, and makes the code harder to modify and maintain over time.

Continuous Integration (CI) is a development practice where developers frequently integrate code changes into a shared repository, often multiple times a day. Each integration is automatically verified by running tests and other checks. The goal is to detect and address issues early, improve code quality, and reduce the time to release new features. CI relies heavily on automated testing to ensure that new code changes do not break existing functionality. Unit tests, integration tests, and other automated checks are run as part of the CI pipeline. This gives developers immediate feedback and in theory keeps the program in a usable state at all times, however it can require significant investment in infrastructure and time to ensure that tests are kept up-to-date. CI can also make significant design changes difficult, since such changes will often break many different parts of the code, and so it can sometimes promote smaller incremental improvements at the cost of rarely getting major architectural design-level improvements.

Some key characteristics of unit tests include:

- **Isolation:** Unit tests are designed to be isolated from the rest of the system. They focus on testing a specific unit of code independently of other components. This isolation ensures that the cause of any failure can be pinpointed to the unit under test.

- **Automation:** Unit tests are often automated or can be automated, meaning they can be executed automatically without human intervention. This allows for frequent and consistent testing during the development process.

- **Independence:** Unit tests should be independent of each other, meaning the success or failure of one test should not impact the results of other tests. This independence allows for easier identification and resolution of issues.

- **Fast Execution:** Unit tests are expected to run quickly. Fast execution is essential to facilitate running the tests frequently, especially during development and continuous integration processes.

- **Repeatable:** Unit tests should produce the same results consistently. A test should not pass or fail intermittently; it should provide reliable and repeatable outcomes.

- **Thorough Coverage:** The goal is to achieve high test coverage, ensuring that a significant portion of the codebase is tested. However, 100% coverage does not necessarily guarantee that all possible issues are caught, and the focus should be on testing critical and complex parts of the code, rather than achieving 100% coverage of each line.

- **Simple and Clear:** Unit tests should be simple, clear, and easy to understand. A well-written test can also serve as documentation, explaining how a unit of code is expected to behave.

- **Early Detection of Issues:** Unit tests help catch and identify issues early in the development process, reducing the likelihood of bugs and regressions making their way into the final product.

The process of creating unit tests involves writing test cases that cover various scenarios, including normal and edge cases. Test cases typically include inputs, expected outputs, and assertions to verify that the actual output matches the expected outcome.

Unit testing is a fundamental practice in modern software development, often integrated into continuous integration (CI) and continuous deployment (CD) pipelines. It provides confidence to developers that their code works as intended and aids in maintaining the reliability and stability of software applications.

We will write a set of unit tests to cover various aspects of each class's functionality, including inserting and retrieving items, handling collisions, removing items, retrieving the nth item, clearing the data structures, and more. We can run these tests to ensure that our classes are working as expected.

Python provides functionality to support writing and running unit tests through the `unittest` module. Therefore the first thing we need to do is `import` this module in our source code file:
```python
import unittest
```

Next, we define a new test `class` named `TestHashTable` that _inherits_ from `unittest.TestCase`. This `class` will contain individual test methods for the `HashTable` `class`.
```python
class TestHashTable(unittest.TestCase):
```
_Inheritance_ is a fundamental concept in object-oriented programming (OOP) that allows a class to inherit attributes and methods from another class. The class that _inherits_ is called the _subclass_ or _derived class_, and the class being inherited from is called the _superclass_ or _base class_. For example, we might have a class `Animal` that represents an animal and create a _subclass_ `Dog` than _inherits_ from `Animal`, since a dog is a specific type of animal.

In this case, our new class `TestHashTable` _inherits_ from the `unittest.TestCase` class provided by Python's `unittest` module. This means that it automatically starts with all of the _class variables_ and _class methods_ defined in the `unittest.TestCase` class. Our `TestHashTable` class is a more specific type of `unittest.TestCase`, namely a unit test that only tests our `HashTable` class, rather than a general unit test like `unittest.TestCase`.

Next, we define a test method within the `TestHashTable` `class`, named `test_insert_and_get()`:
```python
    def test_insert_and_get(self):
```
Each test method must start with the word "test", so that the `unittest` framework can automatically discover and run these methods when testing. This method will test the insertion and retrieval functionality of the `HashTable class`.

This test method first creates an instance of the `HashTable class` with 10 buckets, to be used for testing:
```python
        hash_table = HashTable(buckets=10)
```

Next, we insert some example key-value pairs into the `HashTable` using the `insert()` method:
```python
        hash_table.insert("key1", "value1")
        hash_table.insert("key2", "value2")
```

Next, we need to check to make sure that these two `hash_table.insert()` calls worked correctly. To do this, we use an _inherited_ method from the original `unittest.TestCase` superclass called `assertEqual()`, which compares two values:
```python
        self.assertEqual(hash_table.get("key1"), "value1")
        self.assertEqual(hash_table.get("key2"), "value2")
```
These lines use the `assertEqual()` method to check if the values retrieved from the hash table using the `get()` method match the expected values. If the two values passed to `assertEqual()` are equal, then nothing happens and execution continues. If they are not equal, then `assertEqual()` will trigger an _exception_ with an error message showing they are not equal.

Next, we define another test method `test_collision_handling()`, which focuses on testing how the `HashTable class` handles collisions:
```python
    def test_collision_handling(self):
        hash_table = HashTable(buckets=1)
```
This method creates a new instance of the `HashTable class` with only one bucket, which should be guaranteed to cause collisions once 2 entries are made into the `HashTable`.

Next, we insert 2 example entries:
```python
        hash_table.insert("key1", "value1")
        hash_table.insert("key2", "value2")
```
There should be a collision when the second entry is made. After that, we check to see if the `HashTable` still reports both entries correctly using `assertEqual()`:
```python
        self.assertEqual(hash_table.get("key1"), "value1")
        self.assertEqual(hash_table.get("key2"), "value2")
```
Similar to the previous test, these lines use `assertEqual()` to check if the _values_ retrieved from the hash table (which contains a collision) match the expected _values_.

Next, we want to test removing an entry from a `HashTable`, so we define a method `test_remove()`:
```python
    def test_remove(self):
        hash_table = HashTable(buckets=10)
        hash_table.insert("key1", "value1")
        hash_table.remove("key1")
```
This method creates a new `HashTable` and inserts a sample key-value pair, then removes it on the next line using the `remove()` method.

At this point, `key1` should no longer be in the `HashTable`, so we test this by calling `hash_table.get()`:
```python
        self.assertIsNone(hash_table.get("key1"))
```
This line uses the _inherited_ method `assertIsNone()`, which checks to see if the argument passed to it is `None`. If it is not `None` (meaning that `key1` still has an entry in the `HashTable`), it raises an _exception_.

Next we define a test method `test_getnthitem()` to test the ability to get an entry from a specific numbered position in our `HashTable`:
```python
    def test_getnthitem(self):
        hash_table = HashTable(buckets=10)
        hash_table.insert("key1", "value1")
        hash_table.insert("key2", "value2")
```
These lines create a `HashTable` and insert two example _key:value_ pairs. We then check to see if the results of calling `hash_table.getnthitem()` with index 0 and index 1 are the two entries we just added:
```python
        self.assertEqual(hash_table.getnthitem(0), ("key1", "value1"))
        self.assertEqual(hash_table.getnthitem(1), ("key2", "value2"))
        self.assertIsNone(hash_table.getnthitem(-1))
        self.assertIsNone(hash_table.getnthitem(2))
```
These lines use `assertEqual()` to check if the `getnthitem()` method returns the correct `key:value` pair. We also use `assertIsNone()` to make sure `getnthitem()` returns `None` when we pass it an invalid index to `hash_table`.

Finally, we define a `test_clear()` method to test the clear functionality of the `HashTable class`:
```python
    def test_clear(self):
        hash_table = HashTable(buckets=10)
        hash_table.insert("key1", "value1")
        hash_table.clear(5)
```
These lines creates a new `HashTable` and insert a sample _key:value_ pair. We then call `clear()` to test clearing it, with a different number of buckets than we created it with.

We then check if attempting to retrieve the value associated with `key1` after clearing `hash_table` results in `None`, which is should if `hash_table` is now empty of entries:
```python
        self.assertIsNone(hash_table.get("key1"))
        self.assertEqual(len(hash_table), 5)
```
We also use `assertEqual()` to make sure that our cleared `hash_table` now has 5 buckets instead of 10, and also to test the `__len__()` method's functionality when we retrieve its length.



The remaining test classes (`TestStack` and `TestPriorityQueue`) and their respective test methods follow a similar structure, focusing on testing different aspects of the `Stack` and `PriorityQueue` classes. Each test method within a class tests a specific functionality of the corresponding class, and assert statements are used to verify the expected behavior.

Finally, we can test all of the test methods we defined by calling `unittest.main()`, which serves as the entry point for test execution when our code is run:
```python
if __name__ == '__main__':
    unittest.main()
```
We put the `unittest.main()` call underneath the `if` statement that checks to see if the special variable `__name__` is `__main__`. In Python, every script has a built-in variable called `__name__`. When a script is run, `__name__` is set to `__main__`. When a script is imported as a module into another script, `__name__` is set to the name of the module. Since we only want to run these unit tests when our code is invoked directly, and not when another program is just importing our data structure classes, this check ensures that `unittest.main()` will only be called if our code is being run directly as the main program.

Let's try this now:
```bash
python3 DataStructuresPython.py
```
Output:
```
----------------------------------------------------------------------
Ran 10 tests in 0.000s

OK
```
`unittest.main()` executes all of the unit tests, and they were all successful. However, on modern versions of Python you might sometimes get this result and sometimes instead get an error that look something like:
```
..F.......
======================================================================
FAIL: test_getnthitem (__main__.TestHashTable)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/linuxexamples/basic/DataStructuresPython.py", line 147, in test_getnthitem
    self.assertEqual(hash_table.getnthitem(0), ("key1", "value1"))
AssertionError: Tuples differ: ('key2', 'value2') != ('key1', 'value1')

First differing element 0:
'key2'
'key1'

- ('key2', 'value2')
?      ^         ^

+ ('key1', 'value1')
?      ^         ^


----------------------------------------------------------------------
Ran 10 tests in 0.002s

FAILED (failures=1)
```
What is going on here? And why does it work sometimes but not others (or fail completely or always succeed, when using different Python implementations)?

Bugs that only occur sometimes can be very difficult to track down and debug. In this case, the first step is to attempt to reliably reproduce the bug, or if that is not possible, to analyze in which situations the bug occurs. In this case, the culprit is Python's built-in `hash()` function, which in modern implementations will return different hashes for the same object during different runs of a program. These in turn result in the `HashTable` keys going into different buckets. This is not a bug exactly, since Python's `hash()` function is not guaranteed to be deterministic. However relying on determinism when using this function is a bug, since it does not have that property. In this case, we can either change our `HashTable.hash()` method to use a deterministic hash function, or we can change the unit test code to not require determinism.  For example:
```python
    def test_getnthitem(self):
        # Test retrieving the nth item from the hash table
        hash_table = HashTable(buckets=10)
        hash_table.insert("key1", "value1")
        hash_table.insert("key2", "value2")
        item0 = hash_table.getnthitem(0)
        item1 = hash_table.getnthitem(1)
        self.assertTrue((item0 == ("key1", "value1")) and (item1 == ("key2", "value2")) or (item1 == ("key1", "value1")) and (item0 == ("key2", "value2")))
        self.assertIsNone(hash_table.getnthitem(-1))
        self.assertIsNone(hash_table.getnthitem(2))
```
Now the test doesn't care which order `key1` and `key2` appear in the hash table, as long as they both appear exactly once, with the correct corresponding _value_. The _inherited_ `assertTrue()` method tests if the expression passed as its argument is `True`. In this case it checks to see if `hash_table` contains the first pair we inserted followed by the second pair we inserted OR the second pair we inserted following by the first pair.

We can do a repeated test to make sure this is fixed:
```bash
for i in {1..100}; do python3 DataStructuresPython.py; done
```
Output:
```
----------------------------------------------------------------------
Ran 10 tests in 0.000s

OK
----------------------------------------------------------------------
Ran 10 tests in 0.000s

OK
----------------------------------------------------------------------
Ran 10 tests in 0.000s

OK
...
----------------------------------------------------------------------
Ran 10 tests in 0.000s

OK
```
