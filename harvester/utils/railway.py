from functools import partial, reduce

### result class
# can use data classes for brevity ( https://docs.python.org/3/library/dataclasses.html ) 

class Fail:
    def __init__( self, exception, func, *args, **kwargs ):
        self.exception = exception
        self.func = func 
        self.args = args
        self.kwargs = kwargs
    
### basic functions
def try_catch(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e: # add ruff ignore?
        return Fail(exception=e, func=fn.__name__, args=args, kwargs=kwargs)

def wrapper(rail_fn, fn, *args, **kwargs):
    if len(args) and isinstance(args[0], Fail): # fail track
        return args[0]

    return rail_fn(fn, *args, **kwargs) # success track

def tracks(fn):

    # fn = extract main
    """Railway Oriented Programming decorator

    Wraps a function into a two-tracked function.

    Taking the Fail track when there is an exception.
    """

    return partial(wrapper, try_catch, fn)

def pipe(*sequence):

    """         we're here
         C           E          T           L
    --S--\/     --S--\/     --S--\/      /--S--\/
    --F--/\     --F--/\     --F--/\      /--F--/\


    extract information flow example:
        - test_extract_dcatus ( extract main() ) 
            - railway.track decorating extract main()
                - uses partial function of wrapper func using try_catch and main as static/default args
                - wrapper checks if the "data" is a Fail instance ( fail track ) otherwise proceed with succeed track
    """

    # usage: pipe( {harvest_source_job}, compare, extract, transform, load ) 

    """Combines a sequence of an input arg and following functions,
    from left-to-right. The output from the first function is the input
    for the next one"""
    return reduce(lambda arg, fn: fn(arg), sequence[1:], sequence[0])
