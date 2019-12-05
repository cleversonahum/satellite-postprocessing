import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt

def find_values(filename:str, limit:int) -> np.array:
    preambles = np.array([])
    pilots = np.array([])
    data = np.array([])
    cont=0
    with open(filename) as file:
        for line in file:
            if "Preamble" in line:
                preambles = np.append(preambles, line.split("Phase Error: ",1)[1])
            elif "Pilot" in line:
                pilots = np.append(pilots, line.split("Phase Error: ",1)[1])
            elif "Data" in line:
                data = np.append(data, line.split("Phase Error: ",1)[1])
            cont=cont+1
            if(cont>=limit):
                break
    preambles = np.char.replace(preambles, "\n", "")
    preambles = np.char.replace(preambles, ",", ".")
    pilots = np.char.replace(pilots, "\n", "")
    pilots = np.char.replace(pilots, ",", ".")
    data = np.char.replace(data, "\n", "")
    data = np.char.replace(data, ",", ".")

    preambles = preambles.astype(np.float)
    pilots = pilots.astype(np.float)
    data = data.astype(np.float)

    return(preambles, pilots, data)

[preambles, pilots, data] = find_values("iq1-normal.log", 20000)

plt.figure()
plt.plot(np.arange(len(preambles)), preambles)
plt.title("Preambles")
plt.xlabel("Samples")
plt.ylabel("Phase Error")

plt.figure()
plt.plot(np.arange(len(pilots)), pilots)
plt.title("Pilots")
plt.xlabel("Samples")
plt.ylabel("Phase Error")

plt.figure()
plt.plot(np.arange(10000), data[0:10000])
plt.title("Data")
plt.xlabel("Samples")
plt.ylabel("Phase Error")

plt.show()