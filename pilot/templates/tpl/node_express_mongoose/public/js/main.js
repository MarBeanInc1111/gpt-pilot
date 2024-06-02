// A simple JavaScript function that takes a number as input and returns its double
function double(number) {
  return number * 2;
}

// A JavaScript function that takes an array of numbers as input and returns the sum of all the numbers
function sumArray(numbers) {
  let sum = 0;
  for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i];
  }
  return sum;
}

// An example usage of the above functions
const result = double(sumArray([1, 2, 3, 4]));
console.log(result); // Output: 20

