# trace

```
>>> from trace import Trace, Traceable
>>>
>>> print Trace.module()          # this module name
__main__
>>> print Trace.file()            # this file name
<stdin>
>>> def func():
...     print Trace.func()        # this function name
...
>>> func()
__main__.func
>>>
>>> class A(Traceable):
...     def __init__(self):
...         print Trace.cls()     # this class name
...         print Trace.method()  # this method name
...         print Trace.line()    # this line no
...
>>> a = A()
__main__.A
__main__.A.__init__
<stdin>:5
>>>
>>> class B(A):
...     __clsname = 'A'
...
>>> class C(B):
...     def __init__(self):
...         print self.this()    # this class name
...         print self.base()    # the name of the first supper class that has attribute '__clsname'
...
>>> c = C()
__main__.C
__main__.A
>>>
```
