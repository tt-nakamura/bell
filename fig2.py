import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit

circuits = []
for i in range(3):
    c = QuantumCircuit(2, name='circuit%d'%i)
    c.h(0); c.cx(0,1)
    circuits.append(c)

circuits[0].ry( pi/3, 0)
circuits[1].ry(-pi/3, 1)
circuits[2].ry( pi/3, 0)
circuits[2].ry(-pi/3, 1)
for c in circuits: c.measure_all()

for c in circuits:
    ax = plt.figure().add_subplot()
    c.draw('mpl', ax=ax)
