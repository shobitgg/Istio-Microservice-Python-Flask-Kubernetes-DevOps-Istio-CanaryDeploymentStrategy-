# istio
The repository is to support a Medium blog post on Istio. 

PART 1: https://arunksingh16.medium.com/istio-traffic-management-demo-using-python-flask-based-webservices-part-1-55cd9390932f

PART 2: https://arunksingh16.medium.com/istio-canary-deployment-for-python-flask-based-webservices-2eb86c873f64

Using pipenv in Mac
```
python3 -m pipenv install 
```

### Istioctl Setup

```
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
```
### Istio deployement and profile setup
Instio profile https://istio.io/latest/docs/setup/additional-setup/config-profiles/

```
istioctl install --set profile=demo -y
istioctl profile dump
kubectl label namespace default istio-injection=enabled

```
