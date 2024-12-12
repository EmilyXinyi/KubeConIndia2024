# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for building scikit-learn
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set up GitHub repository and install dependencies
RUN set -ex \
    && GITHUB_REPO="EmilyXinyi:main" \
    && GITHUB_USERNAME=$(echo $GITHUB_REPO | cut -d':' -f1) \
    && BRANCH_NAME=$(echo $GITHUB_REPO | cut -d':' -f2) \
    && git clone --single-branch -b $BRANCH_NAME https://github.com/$GITHUB_USERNAME/scikit-learn.git \
    && cd scikit-learn \
    && pip --default-timeout=1000 install wheel numpy scipy cython meson-python ninja torch

WORKDIR /app

RUN cd scikit-learn && pip --default-timeout=1000 install --editable . --verbose --no-build-isolation --config-settings editable-verbose=true
# RUN pip freeze | grep cupy
RUN pip install array-api-compat
RUN python -c "import sklearn; sklearn.show_versions()"
RUN pip install scipy==1.14.1

# Install any additional requirements for the Flask app
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to ensure output is sent to terminal
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]