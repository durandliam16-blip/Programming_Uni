## Numpy
import numpy as np

# Création
notes = np.array([12, 15, 18, 10])
data = np.array([[1, 2, 3], 
                 [4, 5, 6],
                 [7, 8, 9]])

# Fonctions de base
print(data.ndim)
print(data.shape)
print(data.dtype)

# Opérations
print(data+10)

# Slicing
print(data[1:2] )
print(data[0:2, 1:])

# Agrégations 
print(np.mean(data))
print(np.std(data[0]))
print(np.min(data[0]))
print(np.max(data[0]))
print(np.mean(data, axis=0))

## Pandas