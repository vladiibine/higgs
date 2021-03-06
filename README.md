Higgs aims to be a language that is:
    - statically typed where possible, dynamic where needed
    - highly reflexive
    - object oriented, functional, prototypal
    - designed for composition over inheritance
    - actually duck-typed
    - no statements, only expressions
    - all expressions are function calls
    - multi-method enabled
    - designed for extensibility
    - designed with as few primitives as possible
    - designed to separate the documentation from the code (where it makes sense)
    
    extra ideas:
        - queryable (jquery style) module/object hierarchy

every file defines a module

every module can define values through a mapping of a name to a value, in the module scope, (or through special syntax which
 is synonymous to the name assignment in every way).
 The module body is composed of expressions, some of which declare names in the module body. If such a declaration occurs, 
  then the compile time makes sure the interface of the object declared is fully determined.
 All of the assignment and declaration expressions are evaluated at compile time, in order to fully determine all the 
  member interfaces exported by the module.
    Ex:
        a = 3
        int x
    These 2 declarations, at the module level, will make the module forever export 2 objects of type int. One of them
     will have the value 3, the other will be null. The values are not part of the module interface (thus can be changed) but
     the types are part of the interface (thus they'll always be called 'a' and 'x' and be of type int)
    The interface of the module can always be investigated. It's the module.$intf member
    This member is initialized when the module is loaded. The module loading process means executing the code in the module's
    body.
    
     
    Ex:
        here's how you'd write the sum function, that logs its action:
            num sum(num a, num b): {
                console.log('we are summing stuff')
                a + b                                       # returns the result of the last expression
            }
        What happens here though is something like this:
            num sum(num a, num b)
            sum.code = {console.log('we are summing stuff'); a + b}     # the implementation step
        Perhaps later we'd like to change the implementation:
            sum.code = {a+b}    # all works well. Everyone using `sum(3,4)` will still get the desired answer
                                # However those that had used `sum.code(3,4)` will also log
        But the interface can never be changed after the module loading, because what really takes place when defining the
        sum function is something like this:
            sum = function(name='sum')    # declaration, and generic initialization
            sum.signature = signature(a=num, b=num, return=num)  # after this assignment, the .signature member can never be changed
            sum.code = {console.log('we are summing stuff'); a + b}  # this is a literal code object. such things exist
                                
            
            
        If you wanted to  
        a = 3                                           # name declaration, type inference and initialization
        subtract = function float(float x, float y):  x - y  # all that and function implementation
        multiply = function num(num x, num y): {            # function interface and multiline implementation
                     console.log('something interesting')
                     x * y
                   }
        num divide(num x, num y):{                          # returns the result of the last line 
            console.log('something even more interesting')
            x / y
        }
        # The next 3 only hint towards the fact that the interface and implementation definition are separate steps
        int x                                           # name declaration
        add_intf_only = function int(int x, int y)     # name declaration, function definition, type inference, initialization
        str myfunc(str original, int times)             # (func) name declaration
        


a value can be an object, because everything in Higgs is an object.
    However special types of objects such as a 'function' will ring a bell for many people.

objects are mappings of string names to other values. In this sense, a module is an object.

    #These next 2 lines are questionable now... there's no classes, only objects in Higgs
    classes are objects with at least a member called '$init' which is a function
        -they might also define additional protocol member functions

load time: when modules definitions are loaded into memory, their interface is frozen, but their implementation is not

every module defines its mro

there are only expressions (no statements)

all expressions are function calls

the member access operation is an expression (the ".")

this makes the language highly debuggable!!!

provide very nice lifecycle hooks everywhere...this will make the language even MORE debuggable!!!!!!!!!!

all functions are methods of a module

all scopes will have access to the 'this' keyword, which will refer to an object

functions are NOT over-loadable

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
    
    
Low level sketches:
Object hierarchy:
    Object {$as_string: <make the object printable>, $prototype: <an object which served as the template for this one>}
      - Code {$lines: [a list of lines], $names: [a list of names used in this code block], $module: <module obj>}  # a runnable code object
      - Module {$file: str, $name: str, $module: <the parent module where this was defined>}
      - Type {$name: str, $module: <module object>, $members: {object mapping names to built-in or custom types}}
      - Signature {$pre: <object mapping names to types>, $post: <object mapping names to types>, $rtype: type}  # func signature
      - Function {$name: str, $signature: signature object, $module: <the module where this was defined>, $code: <a code obj>}

Module required attributes:

{
 $name: 'some name',
 $file: 'some file',
 $code: code-object,
 $intf: <all the exported members -> module interface -> available after loading>
 $call: <a function. would make the module object callable>

}


Syntax sketches:
================

Module Example:
---------------
a = 3

def sum(x: num, y: num): num {
    x + y
}

##
# classic animal object (not class). This is actually the instance. The
# class vs object, static method, class method, weird singleton thing has to stop!
object Animal {
    str name
    def specific_sound: str {
        'whif!'
    }
    def respond(name: str): str {
        if name == this().name {
            console.log('the animal recognized its name')
            'HUUH?!?!'
        } else {
            '...'
        }
    }
}

##
#
#
object Dog(Animal) {

}

Dog.name = 'Speedy'  # assign new object with the same interface
Dog.specific_sound.$code = {'WooF!!!'}  # mutate the object - this can violate the interface (to not return the proper type)
# don't forget to talk about closures... they're nothing but the scope with level >= 3 (0 being the code object, 1 being the formal params, 2 being
# wait a minute... we plan on doing block level scope. therefore, scope level 0 is the innermost scope, in current block that the 
# expression is located. level 1, the scope enveloping that, 2 envelopes that in turn... and so on, until we get to the top of the current code block
# From here, there's 3 ways to get up:
# 0 Obviously, use the formal parameters... but that's only going to work for 1 more level...and then:
# 1 Closure scope: use the scope where the code object was created in
# 2 Object scope: use the scope of the object that the code obj is a member of
# >> So let's do as the ancients do, but allow for customization from the hackers.
# >> The ancients put the closure scope(s) first
# >> We'll customize for the hackers, by providing the .($)scopes method, and some parameters. It just returns an iterator
# >> that is used for resolving a name in a scope. Well, that's not good enough, because we need to keep alive all the objects in most of the scopes then
# >> so that's why Python deals so brutally with scope: cuz if you don't, you can't garbage collect almost anything...or can you?


#How assigning to the function works:
#object Object{
#  def set(name: str, value: Object){
#    if real(this().name){
#      if real(this().name.$signature){  #of course, we can do this better...i think
#        this().name.$code = value  #The name is NOT!!!final, the interface is final, so we can only ever change the implementation anyway
#      }
#    }
#  }
#}