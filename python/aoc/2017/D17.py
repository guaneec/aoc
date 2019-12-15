n = 363
a = [0]
c = 0
for i in range(1, 2018):
    c = (c + n + 1) % i
    a = a[:c] + [i] + a[c:]

i = (a.index(2017) + 1) % 2018
print(a[i])

c = 0
x = 1
for i in range(1, 1+50000000):
    c = (c + n) % i + 1
    if (c == 1):
        x = i
print(x)
