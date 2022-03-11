import matplotlib.pyplot as plt

import numpy as np
from qiskit import Aer, transpile, ClassicalRegister
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import DraperQFTAdder, CPhaseGate
from qiskit.visualization import plot_histogram


input_array = [5, 7, 8, 9, 1]

L = 5  # length of array

l = 5  # length of binary representation of required sum (16)

N = 2 ** (l + L)

# binary representation of the states in the form |index>|value at index>
# init_vec = [1000000101, 0100000111, 0010001000, 0001001001, 0000100001]

# ### init_vec = [100000101, 010000111, 001001000, 000101001, 000010001]

#INITIALISATION VECTOR
init_vec = [0] * N
init_vec[517] = 1 / np.sqrt(5)
init_vec[263] = 1 / np.sqrt(5)
init_vec[136] = 1 / np.sqrt(5)
init_vec[73] = 1 / np.sqrt(5)
init_vec[33] = 1 / np.sqrt(5)

init_vec_1 = [0] * N
init_vec_1[263] = 1 / np.sqrt(4)
init_vec_1[136] = 1 / np.sqrt(4)
init_vec_1[73] = 1 / np.sqrt(4)
init_vec_1[33] = 1 / np.sqrt(4)

#DOUBLE SIZE QUANTUM REGISTERS
value_bits = QuantumRegister(2 * (l + L), name='v')

#CLASSICAL REGISTER FOR STORING THE MEASUREMENT OUTCOME
classical = ClassicalRegister(L)

#CREATE THE QUANTUM CIRCUIT
qcircuit = QuantumCircuit(value_bits, classical)

#INITIALISE BOTH HALVES OF THE QUANTUM REGISTER WITH THE INDICES AND THEIR VALUES
qcircuit.initialize(init_vec, value_bits[:l + L])
qcircuit.initialize(init_vec_1, value_bits[l + L:])

#CREATE A DRAPER ADDER INSTANCE
DraperAdder = DraperQFTAdder(l + L, 'fixed', 'DraperAdder')

#APPEND THE DRAPER ADDER TO THE CIRCUIT
qcircuit.append(DraperAdder, value_bits)
# qcircuit.append(DraperAdder, value_bits)

# PHASE ORACLE
for i in range(0, l-1):
    qcircuit.x(value_bits[l + L + i])

qcircuit.append(CPhaseGate(np.pi, None).control(l - 2, None, 7), value_bits[l + L:2 * l + L])

for i in range(0, l-1):
    qcircuit.x(value_bits[l + L + i])


# DIFFUSER DEFINITION (FROM QISKIT DOCUMENTATION OF GROVER ALGORITHM)
def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits - 1)
    qc.mct(list(range(nqubits - 1)), nqubits - 1)  # multi-controlled-toffoli
    qc.h(nqubits - 1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "U_s"
    return U_s


#APPEND DIFFUSER TO THE CIRCUIT
qcircuit.append(diffuser(l), value_bits[l + L:2 * l + L])


# qcircuit.measure_all()  # measure all qubits

#MEASURE THE QUBITS CONTAINING THE ADDED INDICES AND STORE IN THE CLASSICAL REGISTER
qcircuit.measure(value_bits[2*l+L:], classical)
print(qcircuit.draw(output='text'))  # print the circuit and gates
# simulate the circuit
sim = Aer.get_backend('aer_simulator')  # simulator
t_qc = transpile(qcircuit, sim)
nshots = 1000
counts = sim.run(t_qc, shots=nshots).result().get_counts()

#OUTPUT VECTOR FOR STORING THE RESULTS
output_vector = []


counts_values = list(counts.values())
counts_keys = list(counts.keys())

for i in range(len(counts_values)):
    if counts_values[i] > 0.05*nshots:
        print(counts_keys[i])
        output_vector.append(counts_keys[i])

print(output_vector)

#PLOT THE STATES AND THEIR PROBABILITES ON MEASUREMENT
# plot_histogram(counts)
# plt.tight_layout()
#
# plt.show()
