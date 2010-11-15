import os, sys, cPickle, string
from logging import *
from debug import Debug
from math import *

""" Enables catching / logging of exceptions by @errorlog """
Debug.set('BLOCK_EXCEPTIONS',True)

fnt = '\\f(data/FreeSerif.ttf)\\s(48)'
futura = os.path.join('data','Futura Light BT.ttf')
tahoma = os.path.join('data','tahoma.ttf')
pakenham = os.path.join('data','pakenham free.ttf')

def str_to_num(str):
    """ Converts a given string to a number. Returns zero if it is invalid."""
    try:
        return int(str)
    except:
        try:
            return float(str)
        except:
            return 0

def point_in_rect(pt, rect):
    """/fn point_in_rect(pt, rect)
    /brief Returns True if a given point is within a given rect
    @arg pt A point: basically, must be (int, int)
    @arg rect A rectangle: basically, must be (int, int, int, int)
    """ 
    return pt[0] >= rect[0] and \
           pt[0] <= rect[2]+rect[0] and \
           pt[1] >= rect[1] and \
           pt[1] <= rect[3]+rect[1]

def rect_from_obj(obj):
    return (obj['x'], obj['y'], obj['width'] + obj['x'], obj['height'] + obj['y'])
    
def distance(pt1, pt2):
    return (pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2

def load_pickle(pcklfile):
    if os.path.exists('cache_hd_use'):
        file = open(os.path.join('cache_hd_use', pcklfile),'rb')
        data = cPickle.load(file)
        file.close()
    else:
        file = open(os.path.join('cache_ram', pcklfile), 'rb')
        data = cPickle.load(file)
        file.close()
    return data

def getimgwidth(surface):
    return surface.get_rect().width

def getimgheight(surface):
    return surface.get_rect().height
    
# Code from the Python Cookbook to help with string filtering
allchars = string.maketrans('','')
def makefilter(keep):
    delchars = allchars.translate(allchars,keep)
    def thefilter(s):
        return s.translate(allchars, delchars)
    return thefilter
    
filter_unprintable = makefilter(string.printable)

# Concatenates possible strings into a single unicode string, ignoring
# problematic values (like None).
# May later want to make a verbose version that logs when values are missing...

def safe_concat_end(*args):
    str = u''
    for a in args:
        try:
            str += a
        except:
            return u''
    return str

def format_phone(num):
    num = filter(lambda x: ord(x)-ord('0') >= 0 and ord(x)-ord('0') < 10, num)
    if len(num) == 7:    # Format as ###-####
        return "%s-%s" % (num[0:3], num[3:])
    elif len(num) == 10: # Format as (###) ###-####
        return "(%s) %s-%s" % (num[0:3], num[3:6], num[6:])
    elif len(num) == 11: # Format as # (###) ###-####
        return "%s (%s) %s-%s" % (num[0], num[1:4], num[4:7], num[7:])
    else:                # Nothing we can do :(
        return num

def safe_concat_ignore(*args):
    str = u''
    for a in args:
        try:
            str += a
        except:
            try:
                # Try converting to straight ascii, then filter out characters that
                # are breaking the Unicode decoding.
                ascii = filter_unprintable("" + a)
                str += ascii
            except:
                # Failed to convert via either unicode or ascii, skip it
                pass
    return str

# A decorator that catches exceptions in a function and logs them. If an
# exception is raised, it returns the default value passed as its parameter.
# Should *not* be used on functions that are supposed to propagate exceptions!
# Also shouldn't be used on functions that still need to specify a return value.
# 
# This is just a band-aid to prevent gratuitous crashes on unexpected errors --
# any logged exceptions should still be checked and fixed later.
#
# To disable this behavior (e.g. for debugging), set 
def errorlog(retval = None):
    if not Debug("BLOCK_EXCEPTIONS"):
        # Want exceptions to propagate -- do nothing.
        return lambda f: f
            
    def wrap(f):
        def checked(*args, **nargs):
            try:
                return f(*args, **nargs)
            except Exception, e:
                log("Unexpected exception calling " + str(f.func_name) + " with arguments:")
                log(str(args) + " " + str(nargs))
                log("Exception: " + str(e))
                return retval
                
        return checked
    return wrap

def sfmt(s):
    return "$%(#).2f" % {'#': str_to_num(s)/100.0}

def getLatLong(x, y):
    return atan( sinh( pi * (1 - 2 * y) ) ) * 180.0 / pi, \
           x * 360.0 - 180.0

def getCoord(lat, long):
    lat_rad = lat * pi / 180.0
    return ( ( long + 180.0 ) / 360.0 ), \
           ( 1 - ( log( tan( lat_rad ) + 1 / cos( lat_rad ) ) / pi ) ) / 2.0


### CODE TAKEN FROM http://code.activestate.com/recipes/550804/ :)
# The list of symbols that are included by default in the generated
# function's environment
SAFE_SYMBOLS = ["list", "dict", "tuple", "set", "long", "float", "object",
                "bool", "callable", "True", "False", "dir",
                "frozenset", "getattr", "hasattr", "abs", "cmp", "complex",
                "divmod", "id", "pow", "round", "slice", "vars",
                "hash", "hex", "int", "isinstance", "issubclass", "len",
                "map", "filter", "max", "min", "oct", "chr", "ord", "range",
                "reduce", "repr", "str", "type", "zip", "xrange", "None",
                "Exception", "KeyboardInterrupt"]
# Also add the standard exceptions
__bi = __builtins__
if type(__bi) is not dict:
    __bi = __bi.__dict__
for k in __bi:
    if k.endswith("Error") or k.endswith("Warning"):
        SAFE_SYMBOLS.append(k)
del __bi


def createFunction(sourceCode, args="", additional_symbols=dict()):
    """
    Create a python function from the given source code
    
    \param sourceCode A python string containing the core of the
    function. Might include the return statement (or not), definition of
    local functions, classes, etc. Indentation matters !
    
    \param args The string representing the arguments to put in the function's
    prototype, such as "a, b", or "a=12, b",
    or "a=12, b=dict(akey=42, another=5)"
    
    \param additional_symbols A dictionary variable name =>
    variable/funcion/object to include in the generated function's
    closure
    
    The sourceCode will be executed in a restricted environment,
    containing only the python builtins that are harmless (such as map,
    hasattr, etc.). To allow the function to access other modules or
    functions or objects, use the additional_symbols parameter. For
    example, to allow the source code to access the re and sys modules,
    as well as a global function F named afunction in the sourceCode and
    an object OoO named ooo in the sourceCode, specify:
        additional_symbols = dict(re=re, sys=sys, afunction=F, ooo=OoO)
    
    \return A python function implementing the source code. It can be
    recursive: the (internal) name of the function being defined is:
    __TheFunction__. Its docstring is the initial sourceCode string.
    
    Tests show that the resulting function does not have any calling
    time overhead (-3% to +3%, probably due to system preemption aleas)
    compared to normal python function calls.
    """
    # Include the sourcecode as the code of a function __TheFunction__:
    s = "def __TheFunction__(%s):\n" % args
    s += "\t" + "\n\t".join(sourceCode.split('\n')) + "\n"
    
    # Byte-compilation (optional)
    byteCode = compile(s, "<string>", 'exec')  
    
    # Setup the local and global dictionaries of the execution
    # environment for __TheFunction__
    bis   = dict() # builtins
    globs = dict()
    locs  = dict()
    
    # Setup a standard-compatible python environment
    bis["locals"]  = lambda: locs
    bis["globals"] = lambda: globs
    globs["__builtins__"] = bis
    globs["__name__"] = "SUBENV"
    globs["__doc__"] = sourceCode
    
    # Determine how the __builtins__ dictionary should be accessed
    if type(__builtins__) is dict:
        bi_dict = __builtins__
    else:
        bi_dict = __builtins__.__dict__
    
    # Include the safe symbols
    for k in SAFE_SYMBOLS:
        # try from current locals
        try:
            locs[k] = locals()[k]
            continue
        except KeyError:
            pass
        # Try from globals
        try:
            globs[k] = globals()[k]
            continue
        except KeyError:
            pass
        # Try from builtins
        try:
            bis[k] = bi_dict[k]
        except KeyError:
            # Symbol not available anywhere: silently ignored
            pass
    
    # Include the symbols added by the caller, in the globals dictionary
    globs.update(additional_symbols)
    
    # Finally execute the def __TheFunction__ statement:
    eval(byteCode, globs, locs)
    # As a result, the function is defined as the item __TheFunction__
    # in the locals dictionary
    fct = locs["__TheFunction__"]
    # Attach the function to the globals so that it can be recursive
    del locs["__TheFunction__"]
    globs["__TheFunction__"] = fct
    # Attach the actual source code to the docstring
    fct.__doc__ = sourceCode
    return fct
