import subprocess

alphabet = "0123456789abcdef0123456789abcdef"
l = 32

def test(v, i):
    x = list(alphabet[0]*32)
    x[i] = v
    z = subprocess.check_output("./LosT.x32 -b "+"".join(x), shell=True)
    if z[i] == '1':
        return True
    return False

r = ""
for i in range(l):
    for j in alphabet:
        if test(j, i):
            r += j
            break

print r
