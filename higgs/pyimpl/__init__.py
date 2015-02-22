from functools import partial


class HiggsException(Exception):
    pass


class HiggsScopeException(HiggsException):
    pass


class HiggsSyntaxException(HiggsException):
    pass


class HiggsDeclarationException(HiggsSyntaxException):
    pass


def find_in_scope(name, kwargs):
    if name in kwargs:
        return kwargs[name]
    else:
        try:
            return getattr(global_scope, name)
        except AttributeError:
            raise HiggsScopeException(
                u"Couldn't find name {} in any scope".format(name))


class GlobalScope(object):
    importables = {}
    NOT_PROVIDED = object()

    def assign(self, name, value=NOT_PROVIDED, type_decl=NOT_PROVIDED, *args,
               **kwargs):
        interface = find_in_scope('interface', kwargs)
        impl = find_in_scope('impl', kwargs)
        # interface[name] = type(value)

        if value is not self.NOT_PROVIDED:
            impl[name] = value
            interface[name] = type(value)
            return

        if type_decl is self.NOT_PROVIDED:
            raise HiggsDeclarationException(
                u"You must either provide a value for a declaration, "
                u"or explicitly declare a type for it")

        interface[name] = type_decl

    def higgs_import(self, name):
        if name not in self.importables:
            raise ImportError
        return self.importables[name]()


class Module(GlobalScope):
    def inline(self, *args, **kwargs):
        """The code here will execute on import. It will define the interface
        of the module (what names it exports, and their types)

        In Higgs, this won't be a real function, it will consist of the actual
        module code
        """
        pass

    def load(self, inline, *args, **kwargs):
        """Module initialization on import - default behavior.

        By default we don't declare any new attributes here...though we could

        :param inline: The code declared inline, in the module body
        :param args:
        :param kwargs:
        :return:
        """
        assign = find_in_scope('assign', kwargs)

        interface = {}
        impl = {}
        assign = partial(assign, interface=interface, impl=impl)

        inline(assign=assign)

        self.interface = interface
        self.impl = impl

    def __init__(self, *args, **kwargs):
        self.interface = None
        self.impl = None
        self.load(self.inline, *args, **kwargs)


class HiggsObject(object):
    interface = None
    impl = None


class HiggsFunction(HiggsObject):
    interface = {
        'pre': HiggsArgsSpec(),
        'post': HiggsArgsSpec(),
        'rtype': HiggsObject()
    }
    impl = None

    @classmethod
    def create_literal(cls, code=None, pre=None, post=None, rtype=None):
        new_function = cls()
        new_function.interface = {
            'pre': pre,
            'post': post,
            'rtype': rtype
        }
        new_function.impl = code


class HiggsInt(HiggsObject):
    interface = {
        '$add': HiggsFunction.create_literal()
    }

    @classmethod
    def create_literal(cls, value):
        new_int = HiggsInt()


class HiggsArgsList(HiggsObject):
    """Represents an ordered, (immutable?) sequence of HiggsObjects
    """
    interface = {
        '$positional': HiggsList(),
        '$keywords': 0
    }


class HiggsArgsSpec(HiggsObject):
    interface = {

    }


class HiggsList(HiggsObject):
    """Represents an integer indexed, 0-based ordered typed array of HiggsObjects

    The interfaces of the HOs must (at compile time) satisfy the type member
    of the list
    """
    interface = {
        '$get_item': 0,
        '$set_item': 0,
        '$length': 0,
        '$type': 0
    }


class HiggsFrozenDict(HiggsObject):
    """A dictionary that after creation, its keys and values can not be changed

    IDEA:
        Unlike Python dicts, the keys don't have to return the same hash value,
        because their individual object IDs will be used, not their hash value
            -let's see how this works out... it works OK in Python, one must
            simply inherit from types like sets, lists and dicts and use the
            subclass thereof.... why all this nonsense? to provide a hook
            for the user to implement weird behavior
    """
    interface = {
        # need generics :D :(( oh well.. let's work around this

        '$get_item': HiggsFunction.create_literal(post=())
    }


class HiggsDict(HiggsObject):
    interface = {

    }


class HiggsCode(HiggsObject):
    interface = {

    }


class WeirdModule(Module):
    def inline(self, *args, **kwargs):
        assign = find_in_scope('assign', kwargs)
        assign('a', 3)

        def increment(x):
            return x + 1

        assign('increment', increment)
        assign('weird_name', type_decl=str)

        assign('WeirdSubType')


global_scope = GlobalScope()
GlobalScope.importables[WeirdModule.__name__] = WeirdModule
