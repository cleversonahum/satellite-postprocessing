import numpy as np
import numpy.matlib

# Generating preamble
n_repetitions = 10
barker_code   = np.array([-1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j,  1.0000 + 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j, -1.0000 - 1.0000j])

preamble = np.matlib.repmat(barker_code, 1, n_repetitions)[0]
magn_preamble = np.sqrt(np.sum(np.power(np.abs(preamble),2)))

def magn(ind_preamble: int, preambles: np.array) -> np.float:
    magn_val = np.sqrt(np.sum(np.power(np.abs(preambles[ind_preamble]),2)))
    return magn_val

def phase(original_preambles: np.array, captured_preambles: np.array) -> np.float:
    phases_diff = np.abs(np.arctan(original_preambles.imag/original_preambles.real)-np.arctan(captured_preambles.imag/captured_preambles.real))
    return phases_diff

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

            

#print(phase(preamble, captured_preamble[1]))
elements = find_values("preamble.log", "COMECO\n", 130)