every file defines a module

every module can define additional (sub) modules. basically the distinction between class/ package / module is lost.

load time: when modules definitions are loaded into memory, their interface is frozen, but their implementation is not

every module defines its mro

there are only expressions (no statements)

all expressions are function calls

the member access operation is an expression (the ".")

this makes the language highly debuggable!!!

provide very nice lifecycle hooks everywhere...this will make the language even MORE debuggable!!!!!!!!!!

all functions are methods of a module

all scopes will have access to the 'this' keyword, which will refer to an object

functions are over-loadable

functions have the (pre) arg, which allows specifying who they're applied to
    "myobj.mymeth(arg1, arg2)" translates to "(call pre (access pre myobj post mymeth) post arg1 then arg2)"
    and "(hisobj.hismeth(3), 3, 'asdf', myobj).mymeth((2,3, yourobj).yourmeth(0))" will translate to
    (call pre (access post ((call pre (access pre hisobj post hismeth) post 3) then 3 then 'asdf' then myobj) pre mymeth) post (call pre (access pre 2 then 3 then yourobj post yourmeth ) post 0))
        -this allows for multi methods - no more OOP undecidedness (that much)


? how do we differentiate between 'classmethods' and normal methods.... do we even need such crap? - not sure we do.
    - we don't! when referring to an object by its load name 'sys.path.append', we refer to the global object.
        - if we want to make another object, we say 'new sys.path', and we get another one.
        - for the global object, only the 'load' method gets called.
        - when creating a new instance, both the 'new' and 'init' methods get called.
        - the 'new' method is for the magic we know and love from django.... but would that even be possible?
            - well all that's required is for the 'new' method not to be restricted in what it returns.... which is impossible
              if we want to preserve the interface

protocol methods:
    'load': on first accessing a member of the module; -define here non-interface, but common members (protected-like)!!!
    'new': on creating a new module instance - responsible for returning a new instance.
    'init': the constructor - initialize an instance of the module
    '[x: int]': getter for myobj[3] - like stuff
    'get': getter for all the object's attributes
    'set': setter for all the object's attributes