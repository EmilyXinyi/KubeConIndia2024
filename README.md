# KubeConIndia2024
Tutorial: An Accelerated Introduction to AI Model Deployment with Cloud Native

## Resources

- [Google Colab Notebook](https://colab.research.google.com/drive/1KsMEhuEUhVvVDaZFoOKhik81PfZftMo5?usp=sharing)
- [Slide Deck](https://docs.google.com/presentation/d/17yRO_Qz0R5xHGI3grxSIiSKYNGZOSZkU0BFEb0cFzDE/edit?usp=sharing)
- [Docker](https://docs.docker.com/engine/install/)
- [KinD](https://kind.sigs.k8s.io/)

## Cloud Native demos

### Building and running a simple Flask app with Docker

```bash
cd flask-app-hello-world
```

Build the docker image for the Hello KubeCon app:

```bash
docker build -t hello-kubecon:latest .
```

Run the app as a container in your machine:

```bash
docker run -p 3000:5000 hello-kubecon:latest
```

Visit [http://localhost:3000](http://localhost:3000) to see the app running!

### Running the flask app on Kubernetes

The yaml config for running the hello world app on your Kubernetes cluster:

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-kubecon
  namespace: default
  labels:
    app: hello-kubecon
spec:
  containers:
  - name: hello-kubecon
    image: fillerink/kubecon-india-talk:hello-kubecon
    ports:
    - containerPort: 5000
```

Once you've set up your cluster, apply the Pod manifest on your cluster:

```bash
kubectl apply -f pod.yaml
```

We now need to expose the Pod as a Service to be able to access it. This exposes the Pod to the network internal to the cluster:

```bash
kubectl expose pod hello-kubecon --port 5000 --type=ClusterIP
```

Since the Pod is only exposed within the cluster, we need to forward its port to our localhost to be able to access it from our machines:

```bash
kubectl port-forward service/hello-kubecon 3000:5000
```
Access [localhost:3000](http://localhost:3000) in your machine to see the application.

### Building and running the scikit-learn code with Docker

```bash
cd flask-app-scikit-learn
```

Build the docker image:

```bash
docker build -t kubecon-scikit-learn:latest .
```

Run the docker image locally in your machine:

```bash
docker run -p 3000:5000 kubecon-scikit-learn:latest
```

### Running the flask app on Kubernetes

The yaml config for running the hello world app on your Kubernetes cluster:

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubecon-scikit-learn
  namespace: default
  labels:
    app: kubecon-scikit-learn
spec:
  containers:
  - name: kubecon-scikit-learn
    image: fillerink/kubecon-india-talk:scikit-learn
    ports:
    - containerPort: 5000
```

Once you've set up your cluster, apply the Pod manifest on your cluster:

```bash
kubectl apply -f pod.yaml
```

We now need to expose the Pod as a Service to be able to access it. This exposes the Pod to the network internal to the cluster:

```bash
kubectl expose pod kubecon-scikit-learn --port 5000 --type=ClusterIP
```

Since the Pod is only exposed within the cluster, we need to forward its port to our localhost to be able to access it from our machines:

```bash
kubectl port-forward service/kubecon-scikit-learn 3000:5000
```

Access [localhost:3000](http://localhost:3000) in your machine to see the application.
