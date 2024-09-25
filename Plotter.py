import numpy as np
import matplotlib.pyplot as plt


def plot_graph(t, left, right):
    # Convert lists to numpy arrays for plotting
    left = np.array(left)
    right = np.array(right)

    # Add axis titles
    plt.xlabel('Time [Sec]')
    plt.ylabel('Angle [Rad]')


    # Change the background color of the plot
    fig = plt.gcf()
    fig.patch.set_facecolor((13 / 255, 17 / 255, 23 / 255))
    ax = plt.gca()
    ax.set_facecolor((13 / 255, 17 / 255, 23 / 255))

    # Set text color to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.title.set_color('white')

    # Plot the angles of the dipoles over time
    plt.plot(t, left, "c")
    plt.plot(t, right, "m")
    plt.show()

def save_as_image(system, filename, xmin, ymin, xmax, ymax):
		fig, ax = plt.subplots()
		ax.set_xlim(xmin, xmax)
		ax.set_ylim(ymin, ymax)

		for id, magnet in system.magnets:
			for dipole_idx in range(magnet.dipole_number):
				pos = magnet.getDipolePosition(dipole_idx,magnet.theta)
				mom = magnet.getDipoleMoment(dipole_idx,magnet.theta)
				mom*=(xmax-xmin)/(30*abs(mom))
				ax.quiver(pos.x, pos.y, mom.x, mom.y, angles='xy', scale_units='xy', scale=1)

		plt.savefig(filename)
		plt.close(fig)
