// JavaScript test file
class Calculator {
    constructor() {
        this.result = 0;
    }

    add(x, y) {
        return x + y;
    }

    subtract(x, y) {
        return x - y;
    }

    multiply(x, y) {
        return x * y;
    }

    divide(x, y) {
        if (y === 0) {
            throw new Error("Division by zero!");
        }
        return x / y;
    }
}

// Create calculator instance
const calc = new Calculator();

// Test calculations
console.log("Addition: " + calc.add(5, 3));
console.log("Subtraction: " + calc.subtract(10, 4));
console.log("Multiplication: " + calc.multiply(6, 7));
console.log("Division: " + calc.divide(20, 5));

// Async function example
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Arrow function example
const square = (x) => x * x;

// Array methods
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(num => num * 2);
const sum = numbers.reduce((acc, curr) => acc + curr, 0);

console.log("Doubled numbers:", doubled);
console.log("Sum of numbers:", sum); 