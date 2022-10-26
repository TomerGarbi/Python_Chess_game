import numpy as np
import scipy as sc
import matplotlib
import pandas
import cvxopt

print("numpy: ", np.version.version)
print("scipy: ", sc.version.version)
print("matplotlib: ", matplotlib._version.get_versions()['version'])
print("pandas: ", pandas._version.get_versions()['version'])
print("cvxopt: ", cvxopt._version.get_versions()['version'])