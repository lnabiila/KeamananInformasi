import random

initalPermutation = [58, 50, 42, 34, 26, 18, 10, 2,
                    60, 52, 44, 36, 28, 20, 12, 4,
                    62, 54, 46, 38, 30, 22, 14, 6,
                    64, 56, 48, 40, 32, 24, 16, 8,
                    57, 49, 41, 33, 25, 17, 9, 1,
                    59, 51, 43, 35, 27, 19, 11, 3,
                    61, 53, 45, 37, 29, 21, 13, 5,
                    63, 55, 47, 39, 31, 23, 15, 7]

finalPermutation = [40, 8, 48, 16, 56, 24, 64, 32,
                    39, 7, 47, 15, 55, 23, 63, 31,
                    38, 6, 46, 14, 54, 22, 62, 30,
                    37, 5, 45, 13, 53, 21, 61, 29,
                    36, 4, 44, 12, 52, 20, 60, 28,
                    35, 3, 43, 11, 51, 19, 59, 27,
                    34, 2, 42, 10, 50, 18, 58, 26,
                    33, 1, 41, 9, 49, 17, 57, 25]

expansionDBox = [32, 1, 2, 3, 4, 5, 4, 5,
                6, 7, 8, 9, 8, 9, 10, 11,
                12, 13, 12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21, 20, 21,
                22, 23, 24, 25, 24, 25, 26, 27,
                28, 29, 28, 29, 30, 31, 32, 1]

straightPermutation = [16,  7, 20, 21,
                        29, 12, 28, 17,
                        1, 15, 23, 26,
                        5, 18, 31, 10,
                        2,  8, 24, 14,
                        32, 27,  3,  9,
                        19, 13, 30,  6,
                        22, 11,  4, 25]

def binerHex(teks):
    angka = int(teks, 2)
    return(hex(angka))

def hexBiner(teks):
    angka = int(teks, 16)
    biner = bin(angka)[2:]
    return biner.zfill(64)

def permutasi(blok, table):
    return ''.join(blok[i - 1] for i in table)

def xor(a, b):
    tmp = ""
    for i in range(len(a)):
        if a[i] == b[i]: tmp += "0"
        else: tmp += "1"
    return tmp

def fungsiFeistel(kanan, key):
    ekspansiKanan = permutasi(kanan, expansionDBox)
    hasilXor = xor(ekspansiKanan, key)
    return permutasi(hasilXor, straightPermutation)

def putaran(kiri, kanan, key):
    kananBaru = xor(kiri, fungsiFeistel(kanan, key))
    return kanan, kananBaru

def blokData(blok, key):
    blok = permutasi(blok, initalPermutation)
    kiri, kanan = blok[:32], blok[32:]
    for _ in range(16): kiri, kanan = putaran(kiri, kanan, key)
    blokBaru = kanan + kiri
    return permutasi(blokBaru, finalPermutation)

def enkripsi(teks, key):
    blokBiner = ''.join(format(ord(c), '08b') for c in teks.ljust(8))
    blokEnkripsi = blokData(blokBiner, key)
    return binerHex(blokEnkripsi)

def dekripsi(teksEnkripsi, key):
    blokBiner = hexBiner(teksEnkripsi)
    blokDekripsi = blokData(blokBiner, key)
    return ''.join(chr(int(blokDekripsi[i:i+8], 2)) for i in range(0, len(blokDekripsi), 8)).rstrip()

def keyGenerator():
    return ''.join(random.choice('01') for _ in range(48))

teks1 = input("Teks yang ingin dienkripsi (maks 8 karakter): ")
key = keyGenerator() 
print("Generated Key:", binerHex(key))
print("Hasil Enkripsi:", enkripsi(teks1, key))

teks2 = input("Teks yang ingin didekripsi: ")
print("Hasil Dekripsi:", dekripsi(teks2, key))
