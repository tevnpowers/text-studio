# Python timing module inspired by tutorial provided at:
# https://www.zopyx.de/andreas-jung/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
# https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d

import timeit
import time


def timer(method):
    def timed(*args, **kw):
        time_start = timeit.default_timer()
        result = method(*args, **kw)
        time_end = timeit.default_timer()
        return result, time_end - time_start

    return timed


# Example uses
class Foo(object):
    @timer
    def foo(self, a=2, b=3):
        time.sleep(0.2)


@timer
def f1():
    time.sleep(1)


@timer
def f2(a):
    time.sleep(2)


@timer
def f3(a, *args, **kw):
    time.sleep(0.3)


if __name__ == "__main__":
    result_f1, secs_f1 = f1()
    result_f2, secs_f2 = f2(42)
    result_f3, secs_f3 = f3(42, 43, foo=2)
    result_foo, secs_foo = Foo().foo()

    print("Execution time for f1: {} seconds".format(secs_f1))
    print("Execution time for f2: {} seconds".format(secs_f2))
    print("Execution time for f3: {} seconds".format(secs_f3))
    print("Execution time for foo: {} seconds".format(secs_foo))
