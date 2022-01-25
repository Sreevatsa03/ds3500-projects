"""
type_checker.py:  A class for type checking function parameters and return values
against type hints.
"""



class TypeChecker:
    """ A type checking class.  Type-hinted Functions decorated with @TypeChecker.check will
    be validated with additional type checking """

    class InvalidParameterTypeException(Exception):
        pass

    class InvalidReturnTypeException(Exception):
        pass

    @staticmethod
    def check(f):
        """ The type checking decorator """
        def wrapper(*args, **kwargs):

            # It might be useful to convert f.__annotations__ to a list of tuples.

            # Check the type of each paraemter
            for i in range(len(args)):
                # compare the expected and actual type for each argument
                # raise an exception if an inconsistency is detected
                pass


            # Call the function to compute the return value
            val = f(*args, **kwargs)

            # Now check the type of the return value
            # raise an exception if an inconsistency is detected
            
            # Return the value if no problems were detected
            return val
        
        return wrapper

