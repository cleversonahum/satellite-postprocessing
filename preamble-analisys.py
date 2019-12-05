import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt

# Generating preamble
n_repetitions = 10
barker_code   = np.array([-1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j,  1.0000 + 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j, -1.0000 - 1.0000j])

preamble = np.matlib.repmat(barker_code, 1, n_repetitions)[0]
magn_preamble = np.sqrt(np.sum(np.power(np.abs(preamble),2)))

def magn(ind_preamble: int, preambles: np.array) -> np.float:
    magn_val = np.abs(np.sqrt(np.sum(np.power(np.abs(preambles[ind_preamble]),2))) - magn_preamble)
    return magn_val

def phase(original_preambles: np.array, captured_preambles: np.array) -> np.float:
    phases_diff = np.abs(np.arctan(original_preambles.imag/original_preambles.real)-np.arctan(captured_preambles.imag/captured_preambles.real))
    return phases_diff

def snr(original_preambles: np.array, captured_preambles: np.array) -> np.float:
    snr_values = 10* np.log10(np.mean(np.power(original_preambles, 2))/np.mean(np.abs(np.power(original_preambles, 2)-np.power(captured_preambles, 2))))
    return snr_values

def find_values(filename:str, keyword:str, n_elements: int) -> np.array:
    elements = np.array([])
    ind = -1
    count = 0
    with open(filename) as file:
        for line in file:
            if(line==keyword):
                count = count+1
                ind=0
                continue
            if(ind>=0 and ind<=n_elements):
                elements = np.append(elements, line)
                ind=ind+1
                if(ind==n_elements):
                    ind = -1
    elements = np.char.replace(elements, "j", "")
    elements = np.char.replace(elements, "+ -", "-")
    elements = np.char.replace(elements, "\n", "j")
    elements = np.char.replace(elements, ",", ".")
    elements = np.char.replace(elements, " ", "")
    
    elements = np.reshape(elements.astype(np.complex), (count, n_elements))
    return(elements)

captured_preambles = find_values("preamble.log", "COMECO\n", 130)

magn_preambles = np.array([])
phase_error_preambles = np.array([])
snr_preambles = np.array([])
for i in range(captured_preambles.shape[0]):
    magn_preambles = np.append(magn_preambles, magn(i, captured_preambles))
for i in range(captured_preambles.shape[0]):
    phase_error_preambles = np.append(phase_error_preambles, phase(preamble, captured_preambles[i]))
for i in range(captured_preambles.shape[0]):
    snr_preambles = np.append(snr_preambles, snr(preamble, captured_preambles[i]))
    
plt.figure()
plt.plot(range(captured_preambles.shape[0]), magn_preambles)
plt.xlabel("Preamble Number")
plt.ylabel("Magnitude")

plt.figure()
plt.plot(range(captured_preambles.shape[0]*captured_preambles.shape[1]), phase_error_preambles)
plt.xlabel("samples")
plt.ylabel("Phase Error")

plt.figure()
plt.plot(range(captured_preambles.shape[0]), snr_preambles)
plt.xlabel("samples")
plt.ylabel("SNR")
plt.show()