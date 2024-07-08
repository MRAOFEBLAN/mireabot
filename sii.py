f = open("17.txt")
a1 = [int(q) for q in f]
a = [s for s in a1 if s % 55 == 0]
itog = ""
for i in a:
    itog += str(i)
sumi = 0
for z in itog:
    sumi += int(z)
sumi_1 = []
for x in range(len(a1) - 1):
    if a1[x] < sumi and a1[x+1] < sumi:
        sumi_1.append(a1[x] + a1[x+1])
print(len(sumi_1), max(sumi_1))