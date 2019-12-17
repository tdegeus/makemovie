
import matplotlib.pyplot as plt

filenames = []

for i in range(5):

    filename = 'image_{0:d}.png'.format(i)
    filenames += [filename]

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    plt.savefig(filename)


import makemovie

makemovie.trim(filenames, verbose=False)
