def fibonacci(n):
    """
    Calculate the nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

class TestClass:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
        return self.value

# Test the code
if __name__ == "__main__":
    # Create an instance
    test = TestClass()
    
    # Print some Fibonacci numbers
    for i in range(10):
        print(f"Fibonacci({i}) = {fibonacci(i)}")
        
    # Test the class
    print(f"Value after increment: {test.increment()}") 