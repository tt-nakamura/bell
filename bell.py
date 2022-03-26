# verify Bell's inequality violation on quantum computer
# reference:
#   J. J. Sakurai, "Modern Quantum Mechanics" section 3.9

from math import pi
from qiskit import QuantumCircuit, IBMQ, execute
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor

circuits = []
for i in range(3):
    c = QuantumCircuit(2, name='circuit%d'%i)
    c.h(0); c.cx(0,1) # Bell state
    circuits.append(c)

# rotate direction of measurements
circuits[0].ry( pi/3, 0)
circuits[1].ry(-pi/3, 1)
circuits[2].ry( pi/3, 0)
circuits[2].ry(-pi/3, 1)
for c in circuits: c.measure_all()

# get your token at https://quantum-computing.ibm.com
IBMQ.enable_account('__paste_your_token_here__')
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend_filter = lambda b:((not b.configuration().simulator)
                           and (b.configuration().n_qubits >= 2)
                           and (b.status().operational))
backend = least_busy(provider.backends(filters=backend_filter))
print('Jobs will run on', backend.name())

shots = 8192
job = execute(circuits, backend=backend, shots=shots)
job_monitor(job, interval=2)
result = job.result()

counts = [result.get_counts(c) for c in circuits]
Q = [(c['01'] + c['10'])/shots for c in counts]
bell = Q[0] + Q[1] - Q[2] # LHS-RHS of inequality
print(counts)
print('Q_1 + Q_2 - Q_3 =', bell)
if bell < 0: print("Bell's inequality violated")
