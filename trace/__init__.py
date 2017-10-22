import inspect    


def cls_name(cls):
    return cls.__module__ + '.' + cls.__name__


def type_name(obj):
    return obj.__class__.__module__ + '.' + obj.__class__.__name__


def cls_from_stact(stack):
    locals = stack[0].f_locals
    globals = stack[0].f_globals
    if locals.has_key('self'):
        return locals['self'].__class__
    elif locals.has_key('cls'):
        return locals['cls']
    else:
        clss = filter(lambda x: inspect.isclass(x) and hasattr(x, stack[3]), globals.values())
        if not clss:
            raise BaseException()
        if len(clss) > 1:
            raise AssertionError('Multiple classes has this method: %s' % str(clss))
        return clss[0]


class Trace:
    @staticmethod
    def stack(pointer=1):
        return inspect.stack()[pointer]

    @staticmethod
    def _caller_stack(pointer=2):
        return inspect.stack()[pointer]

    @staticmethod
    def cls(caller_stack=None):
        try:
            stack = caller_stack or Trace._caller_stack()
            cls = cls_from_stact(stack)
            return cls_name(cls)
        except BaseException:
            return Trace.module(stack) + '.' + stack[3]
        except KeyError:
            raise AssertionError('outside of context, no class object')

    @staticmethod
    def method(caller_stack=None):
        stack = caller_stack or Trace._caller_stack()
        cls = cls_from_stact(stack)
        return cls_name(cls) + '.' + stack[3]

    @staticmethod
    def module(caller_stack=None):
        stack = caller_stack or Trace._caller_stack()
        return stack[0].f_globals['__name__']

    @staticmethod
    def func(caller_stack=None):
        stack = caller_stack or Trace._caller_stack()
        if stack[3] == '<module>':
            return AssertionError('No function object')
        return stack[0].f_globals.get('__name__') + '.' + stack[3]

    @staticmethod
    def file(caller_stack=None):
        stack = caller_stack or Trace._caller_stack()
        return stack[0].f_code.co_filename

    @staticmethod
    def line(caller_stack=None):
        stack = caller_stack or Trace._caller_stack()
        return "%s:%s" % (Trace.file(stack), stack[0].f_lineno)


class Traceable(object):
    __clsname = 'Traceable'

    def this(self):
        return type_name(self)

    @classmethod
    def base(cls, level=0):
        cls = cls.__base__ if (level == 0) else cls
        if cls.__base__ == object:
            raise AssertionError("There are no any classes has the attribute: '__clsname'")

        attr_name = '_' + cls.__name__ + '__clsname'
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return cls.__base__.base(level + 1)
