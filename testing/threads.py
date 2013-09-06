import threading

# remember in python simple data types are passed by value and objects are passed by reference
#>>> a = 1
#>>> def f(x):
#...   x = x + 1

#>>> f(a)
#>>> a
#1

#>>> class A:
#...    a = 1

#>>> a = A()
#>>> a.a
#1
#>>> a.a = 2
#>>> def f2(o):
#...    o.a += 1

#>>> a.a
#2
#>>> f2(a)
#>>> a.a
#3

class Counter(object):
    _count = 0


def increment_counter(C):
    C._count += 1

my_counter = Counter()

t1 = threading.Thread(target=increment_counter, args=(my_counter, ))
t2 = threading.Thread(target=increment_counter, args=(my_counter, ))
t3 = threading.Thread(target=increment_counter, args=(my_counter, ))  

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print(my_counter._count)
