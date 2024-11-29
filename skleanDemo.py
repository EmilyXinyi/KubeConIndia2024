# installation step 

# ! nvidia-smi

# GITHUB_USERNAME, BRANCH_NAME = "EmilyXinyi:main".split(":", 1)
# ! git clone --single-branch -b $BRANCH_NAME https://github.com/$GITHUB_USERNAME/scikit-learn.git

# ! cd scikit-learn && pip install wheel numpy scipy cython meson-python ninja --quiet

# ! cd scikit-learn && pip install --editable . --verbose --no-build-isolation --config-settings editable-verbose=true
# ! pip freeze | grep cupy
# ! pip install array-api-compat
# ! python -c "import sklearn; sklearn.show_versions()"
# %pip install scipy==1.14.1

import os
import torch
import numpy as np
from time import perf_counter
from sklearn.linear_model import Ridge
from sklearn import set_config

os.environ["SCIPY_ARRAY_API"] = "1"
set_config(array_api_dispatch=True)

n_samples, n_features = int(2.5e5), int(1e3)
ridge = Ridge(alpha=1.0, solver="svd")

print(f"Generating data with shape {(n_samples, n_features)}...")
X_cuda = torch.randn(n_samples, n_features, device="cuda")
w = torch.randn(n_features, device="cuda")
y_cuda = X_cuda @ w + 0.1 * torch.randn(n_samples, device="cuda")
X_cpu, y_cpu = X_cuda.cpu(), y_cuda.cpu()
X_np, y_np = X_cpu.numpy(), y_cpu.numpy()
print(f"Data size: {X_np.nbytes / 1e6:.1f} MB")

tic = perf_counter()
ridge_cuda = ridge.fit(X_cuda, y_cuda)
print(ridge_cuda.coef_[:5])
toc = perf_counter()
print(f"PyTorch GPU ridge: {toc - tic:.2f} s")

tic = perf_counter()
ridge_np = ridge.fit(X_np, y_np)
print(ridge_np.coef_[:5])
toc = perf_counter()
print(f"NumPy ridge: {toc - tic:.2f} s")