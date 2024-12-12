import os
import torch
import numpy as np
from time import perf_counter
from flask import Flask, render_template_string, jsonify
from sklearn.linear_model import Ridge
from sklearn import set_config

app = Flask(__name__)

os.environ["SCIPY_ARRAY_API"] = "1"
set_config(array_api_dispatch=True)

n_samples, n_features = int(2.5e5), int(1e3)
ridge = Ridge(alpha=1.0, solver="svd")

X_cuda = torch.randn(n_samples, n_features, device="cuda")
w = torch.randn(n_features, device="cuda")
y_cuda = X_cuda @ w + 0.1 * torch.randn(n_samples, device="cuda")
X_cpu, y_cuda = X_cuda.cpu(), y_cuda
X_np, y_np = X_cpu.numpy(), y_cuda.numpy()

@app.route("/")
def helloworld():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ML Benchmark</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background-color: #f0f0f0;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        .btn {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .btn-cpu {
            background-color: #2196F3;
        }
        .btn-cpu:hover {
            background-color: #1E88E5;
        }
        .btn-gpu {
            background-color: #FF9800;
        }
        .btn-gpu:hover {
            background-color: #F57C00;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 100%;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>Train with CPU/GPU</h1>
    <div class="button-container">
        <button id="cpuBtn" class="btn btn-cpu">Use CPU</button>
        <button id="gpuBtn" class="btn btn-gpu">Use GPU</button>
    </div>
    <div id="result">Click a button to run benchmark</div>

    <script>
        document.getElementById('cpuBtn').addEventListener('click', () => runBenchmark('cpu'));
        document.getElementById('gpuBtn').addEventListener('click', () => runBenchmark('gpu'));

        function runBenchmark(type) {
            fetch(`/benchmark/${type}`)
                .then(response => response.text())
                .then(result => {
                    document.getElementById('result').textContent = result;
                })
                .catch(error => {
                    document.getElementById('result').textContent = 'Error: ' + error;
                });
        }
    </script>
</body>
</html>
''')

@app.route("/benchmark/cpu")
def benchmark_cpu():
    try:
        tic = perf_counter()
        ridge_np = ridge.fit(X_np, y_np)
        toc = perf_counter()
        
        result = f"NumPy Ridge Regression Benchmark:\n"
        result += f"First 5 Coefficients: {ridge_np.coef_[:5]}\n"
        result += f"Computation Time: {toc - tic:.2f} seconds"
        
        return result
    except Exception as e:
        return f"CPU Benchmark Error: {str(e)}"

@app.route("/benchmark/gpu")
def benchmark_gpu():
    try:
        if not torch.cuda.is_available():
            return "GPU not available"

        tic = perf_counter()
        ridge_cuda = ridge.fit(X_cuda, y_cuda)
        toc = perf_counter()
        
        result = f"PyTorch GPU Ridge Regression Benchmark:\n"
        result += f"First 5 Coefficients: {ridge_cuda.coef_[:5]}\n"
        result += f"Computation Time: {toc - tic:.2f} seconds"
        
        return result
    except Exception as e:
        return f"GPU Benchmark Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)