# QOSF-March-2022-Assessment-Task-1
Solution for the Task 1 for the QC Mentorship program \
Draper Adder adds the contents of two quantum registers using Quantum Fourier Transform, in effect : |a>|b> --> |a+b>|b> \
Hence to implement Draper Adder on the index and the value at that index, for the array [5 7 8 9 1], where the indices and values are both represented by 5-bit bitstrings, a quantum register of the size 2 * (5+5) is created. \
The Draper Adder adds the values and their corresponding indices. \
The phase oracle implements a negative amplitude on the required solution state (here 16), and the diffuser function amplifies the amplitdue of the solution state. \
The the indices which give the sum of 16 are added together, and on implementing the phase oracle and diffuer, attain a higher probability of measurement. \
On measurement, the correct indices are printed as an output vector, in their binary bitstring format.
