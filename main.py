import numpy as np
from functools import reduce
import operator as op
import math
import random

def pack(bit_array):
	return bit_array[bit_array.index(1):]

def ceil_log2(val):
	return math.ceil(math.log2(val))

def shape_from_redundancy(r):
	return [2**x for x in [(r-1)//2, (r-1)//2 + (r-1)%2]]

# Generazione dati casuali
dim = 11
bits = pack(random.sample([0,1]*dim, dim))
print(int(''.join(map(str, bits)), 2), '=>', bits)

# Calcolo del numero di bit di ridondanza richiesti
r = ceil_log2(len(bits)) + 1
r = ceil_log2(r + len(bits)) + 1
rm = 2**ceil_log2(r + len(bits))
print(len(bits), r, rm)

# Aggiungo zeri per completare il blocco
bits = [0]*(rm-r-len(bits)) + bits
#print(int(''.join(map(str, bits)), 2), '=>', bits)

# Calcolo del codice di Hamming
bits = [v if i in [2**p // 2 for p in range(r)] else bits.pop(0) for i,v in enumerate([0]*rm)]
for p in [2**p // 2 for p in range(1, r)]:
	bits[p] = reduce(op.xor, [v for i, v in enumerate(bits) if i & p])
bits[0] = reduce(op.xor, bits)
print(np.array(bits).reshape(shape_from_redundancy(r)))

# Verifica che la sequenza sia valida
res = reduce(op.xor, [i for i, bit in list(enumerate(bits)) if bit])
print('Corretto?', res, '=>', bin(res)[2:], '=>', not reduce(op.xor, bits))

# Simulazione invio con errore
error_bit = 7
bits[error_bit] = not bits[error_bit]

res = reduce(op.xor, [i for i, bit in list(enumerate(bits)) if bit])
print('Errore:', res, '=>', bin(res)[2:], '=>', not reduce(op.xor, bits))
