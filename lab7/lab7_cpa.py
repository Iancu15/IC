# Test CPA
# Authors: Marios Choudary, Razvan Smadu

# %%
from utils import hamming_weight, s_box
import numpy as np
import matplotlib.pyplot as plt


# %%
# Load previously generated data
# 'M': vector of plaintexts of length 50,000
# 'X' vector of leakage traces of length 50,000
# 'K': key used for all traces
data = np.load("simdata.npy", allow_pickle=True).item()
M, X, K = data["M"].reshape(-1), data["X"].reshape(-1), data["K"].item()

# Get number of leakage points/plaintexts
N = X.shape[0]

print("Size of M:", M.shape)
print("Size of X:", X.shape)
print("K:", K)  # This is supposed to be found by you

# %%
# Set possible candidate values from 0-255
target_values = np.arange(256)
nr_values = target_values.shape[0]

# Set Hamming Weight as leakage model for each value in simulated data
lmodel = hamming_weight(target_values)

# %%
# Plot leakage data for first 1000 values
plt.figure(figsize=(15, 5))
idx = np.arange(1000)  # x-axis
X1 = X[idx]  # y-axis
plt.plot(idx, X1)
plt.xlabel("Sample index")
plt.ylabel("Leakage")
plt.show(block=False)

# %%
# Compute hamming weight value of S-box output for one key value
k = 0                                           # The key hypothesis (i.e., the first key)
V = s_box[np.bitwise_xor(target_values[k], M)]  # The output of the S-box, on the first key
L = lmodel[V]                                   # The Hamming Weight model

# %%
# Plot hamming weight leakage for S-box output of given key hypothesis
plt.figure(figsize=(15, 5))
plt.plot(idx, L[idx])
plt.xlabel("Sample index")
plt.ylabel("Hamming weight leakage for k=%d" % k)
plt.show(block=False)

# %%
# Compute correlation coefficient for this key hypothesis
c = np.corrcoef(X, L)
c = c[0, 1]
print("Correlation coefficient is: %f\n" % c)

# %% TODO: compute the correlation for each possible candidate
# You can initialize a vector like this:
# cv = np.zeros(N)  # vector with N elements
cv = np.zeros(nr_values)
keys = range(nr_values)
X_part = X[:1000]
M_part = M[:1000]
for k in range(nr_values):
    V = s_box[np.bitwise_xor(target_values[k], M_part)]
    L = lmodel[V]
    c = np.corrcoef(X_part, L)
    cv[k] = c[0, 1]

cv_list = cv.tolist()
print("Correct key: \n", cv_list.index(max(cv_list)))

# %% TODO: plot correlation coefficient for each candidate
plt.figure(figsize=(15, 5))
plt.plot(keys, cv)
plt.xlabel("Key value")
plt.ylabel("Correlation coefficient")
plt.show(block=False)

# %% TODO: Compute success rate for different nuber of traces used in attack
# Success rate is computed as the frequency of times the correct
# key is classified first.
# For this, use variable amounts of traces (e.g. 10, 20, 50, 100, 200, 500, 1000),
# and for each iteration select that number of traces at random from the whole
# dataset

n_iter = 50
ntraces = [10, 20, 50, 100, 200, 500, 1000] # This should be variable (e.g., 10, 20, 50, ...)
rng = np.random.default_rng()

success_rates = np.zeros(len(ntraces))
success_rates_index = 0
for ntrace in ntraces:
    number_of_correct_guesses = 0
    for i in range(n_iter):
        sel_idx = rng.choice(N, ntrace)
        Mi = M[sel_idx]
        Xi = X[sel_idx]

        # TODO: obtain correlation vector for each selection of traces,
        # then compute success rate
        cv = np.zeros(nr_values)
        keys = range(nr_values)
        for k in range(nr_values):
            V = s_box[np.bitwise_xor(target_values[k], Mi)]
            L = lmodel[V]
            c = np.corrcoef(Xi, L)
            cv[k] = c[0, 1]
        cv_list = cv.tolist()
        guessed_key = cv_list.index(max(cv_list))
        if guessed_key == 208:
            number_of_correct_guesses += 1
    
    success_rates[success_rates_index] = number_of_correct_guesses / n_iter
    success_rates_index += 1

# %% TODO: plot success rate as a function of number of traces used in attack
plt.figure(figsize=(15, 5))
plt.plot(ntraces, success_rates)
plt.xlabel("N")
plt.ylabel("SR")
plt.show(block=False)

# %%
# Make sure that the program does not exit without showing the plots
plt.show()
