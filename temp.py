import matplotlib.pyplot as plt

xs = [x for x in range(-4, 10)]
ys = [x**3 - 0.8*x**2 - 1.5*x + 5.4 for x in xs]

plt.plot(xs, ys, 'r-')
plt.show()
