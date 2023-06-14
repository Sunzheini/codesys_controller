import time


# Decorator to print the time result (return) of the method
def print_method_name_time_and_result(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start

        print('method: {} took {} seconds'.format(func.__name__, end))
        print('returned: {}'.format(result))
        return result
    return wrapper
