import multiprocessing


def square_list(mylist, result, square_sum):
    """
    function to square a given list
    """
    # append squares of mylist to result array
    for idx, num in enumerate(mylist):
        result[idx] = num * num

        # square_sum value
    square_sum.value = sum(result)

    # print result Array
    print("Result(in process p1): {}".format(result[:]))

    # print square_sum Value
    print("Sum of squares(in process p1): {}".format(square_sum.value))


if __name__ == "__main__":
    # input list
    mylist = [1, 2, 3, 4]

    # creating Array of int data type with space for 4 integers
    result = multiprocessing.Array('i', 4)

    # creating Value of int data type
    square_sum = multiprocessing.Value('i')

    # creating new process
    p1 = multiprocessing.Process(target=square_list, args=(mylist, result, square_sum))

    # starting process
    p1.start()

    # wait until process is finished
    p1.join()

    # print result array
    print("Result(in main program): {}".format(result[:]))

    # print square_sum Value
    print("Sum of squares(in main program): {}".format(square_sum.value))


# ================= EXAMPLE 2: =====================


import multiprocessing as mp

def init(aa, vv):
    global a, v
    a = aa
    v = vv

def worker(i):
    a[i] = v.value * i

if __name__ == "__main__":
    N = 10
    a = Array('i', [0]*N)
    v = mp.Value('i', 3)
    p = mp.Pool(initializer=init, initargs=(a, v))
    p.map(worker, range(N))
    print(a[:])


# ============== EXAMPLE 3: ===============

from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])