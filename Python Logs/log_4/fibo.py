# Fibonacci numbers module

# Write Fibonacci numbers up to n
def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=" ")
        a, b = b, a + b
    print()

# return Fibonacci numbers up to n
def fib2(n):
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result

if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
    print(fib2(int(sys.argv[1])))