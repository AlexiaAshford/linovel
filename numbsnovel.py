import glob

t = 0
for i in glob.glob('./novel/*.epub'):
    print(i)
    t += 1
print(t)
print(len(glob.glob('./novel/*.epub')))