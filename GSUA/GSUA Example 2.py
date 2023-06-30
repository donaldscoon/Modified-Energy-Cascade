
##################################################################################
##################################################################################
import numpy as np
import matplotlib.pyplot as plt

from SALib.sample import saltelli
from SALib.analyze import sobol
'''
this one does SA on the parabola 
f(x)= a+b(x^2) specifically a and b
'''
# Defining the problem
def parabola(x, a, b):
    """Return y=a+b*x**2"""
    return a + b*x**2

# describing the problem
problem = {
    'num_vars': 2,
    'names': ['a', 'b'],
    'bounds': [[0, 1]]*2
}

#sampling
param_values = saltelli.sample(problem, 2**6)

# evaluate
x = np.linspace(-1, 1, 100) # Returns num evenly spaced samples, calculated over the interval [start, stop].
y = np.array([parabola(x, *params) for params in param_values])

# analyze
sobol_indices = [sobol.analyze(problem, Y) for Y in y.T]

# Now we can extract the first-order Sobol indices for
# each bin of x and plot:

S1s = np.array([s['S1'] for s in sobol_indices])

fig = plt.figure(figsize=(10, 6), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax0 = fig.add_subplot(gs[:, 0])
ax1 = fig.add_subplot(gs[0, 1])
ax2 = fig.add_subplot(gs[1, 1])

for i, ax in enumerate([ax1, ax2]):
    ax.plot(x, S1s[:, i],
            label=r'S1$_\mathregular{{{}}}$'.format(problem["names"][i]),
            color='black')
    ax.set_xlabel("x")
    ax.set_ylabel("First-order Sobol index")

    ax.set_ylim(0, 1.04)

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.legend(loc='upper right')

ax0.plot(x, np.mean(y, axis=0), label="Mean", color='black')

# in percent
prediction_interval = 95

ax0.fill_between(x,
                 np.percentile(y, 50 - prediction_interval/2., axis=0),
                 np.percentile(y, 50 + prediction_interval/2., axis=0),
                 alpha=0.5, color='black',
                 label=f"{prediction_interval} % prediction interval")

ax0.set_xlabel("x")
ax0.set_ylabel("y")
ax0.legend(title=r"$y=a+b\cdot x^2$",
           loc='upper center')._legend_box.align = "left"

plt.show()

##################################################################################
##################################################################################

# from SALib import ProblemSpec
# from SALib.test_functions import Ishigami
# from SALib.plotting.bar import plot as barplot

# import matplotlib.pyplot as plt
# import numpy as np


# # By convention, we assign to "sp" (for "SALib Problem")
# sp = ProblemSpec(
#     {
#         "names": ["x1", "x2", "x3"],  # Name of each parameter
#         "bounds": [[-np.pi, np.pi]] * 3,  # bounds of each parameter
#         "outputs": ["Y"],  # name of outputs in expected order
#     }
# )

# (
#     sp.sample_saltelli(512, calc_second_order=True)
#     .evaluate(Ishigami.evaluate)
#     .analyze_sobol()
# )

# # Display results in table format
# print(sp)

# # First-order indices expected with Saltelli sampling:
# # x1: 0.3139
# # x2: 0.4424
# # x3: 0.0

# # Basic plotting of results
# sp.plot()

# plt.title("Basic example plot")


# # More advanced plotting

# # Plot functions actually return matplotlib axes objects
# # In the case of the Sobol' method if `calc_second_order=True`, there will be
# # 3 axes (one each for Total, First, and Second order indices)
# axes = sp.plot()

# # These can be modified as desired.
# # Here, for example, we set the Y-axis to log scale
# for ax in axes:
#     ax.set_yscale("log")

# axes[0].set_title("Example custom plot with log scale")

# # Other custom layouts can be created in the usual matplotlib style
# # with the basic bar plotter.

# # Example: Direct control of plot elements
# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 16))

# # Get result DataFrames
# total, first, second = sp.to_df()

# ax1 = barplot(total, ax=ax1)
# ax2 = barplot(first, ax=ax2)
# ax3 = barplot(second, ax=ax3)

# ax1.set_yscale("log")
# ax2.set_yscale("log")

# ax1.set_title("Customized matplotlib plot")
# plt.show()


# # Plot sensitivity indices as a heatmap
# # Note that plotting methods return a matplotlib axes object
# ax = sp.heatmap("Y")
# ax.set_title("Basic heatmap")
# plt.show()


# # Another heatmap plot with more fine-grain control
# # Displays Total and First-Order sensitivities in separate subplots
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
# sp.heatmap("Y", "ST", "Total Order Sensitivity", ax1)
# sp.heatmap("Y", "S1", "First Order Sensitivity", ax2)
# plt.show()


# # Yet another heatmap example
# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
#     2, 2, figsize=(10, 6), sharex=True, constrained_layout=True
# )
# sp.heatmap("Y", "ST", "Total Order", ax=ax1)
# sp.heatmap("Y", "ST_conf", "Total Order Conf.", ax=ax2)
# sp.heatmap("Y", "S1", "First Order", ax=ax3)
# sp.heatmap("Y", "S1_conf", "First Order Conf.", ax=ax4)
# plt.show()