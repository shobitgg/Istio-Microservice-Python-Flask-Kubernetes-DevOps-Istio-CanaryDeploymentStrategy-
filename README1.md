# istio
https://github.com/arunksingh16/istio

https://python.plainenglish.io/istio-traffic-management-demo-using-python-flask-based-webservices-part-1-55cd9390932f | https://arunksingh16.medium.com/istio-canary-deployment-for-python-flask-based-webservices-2eb86c873f64 https://medium.com/codex/getting-started-with-service-mesh-and-istio-3c8af1836454


## How Istio Works 

Following APIs are supported in Istio -

Virtual services [A virtual service lets you configure how requests are routed to service within an Istio service mesh]
Destination rules [How traffic forwarded to the destination
Gateways [manage inbound and outbound traffic for your mesh]
Service entries [add an entry to the service registry that Istio maintains internally]
Sidecars [By default, Istio configures this using Envoy proxy but you can fine grain as well]

![image](https://user-images.githubusercontent.com/41900814/232405586-0f8093e5-8132-4acf-945f-4f301234a3f9.png)

Once the profile is applied, you can see the running required services/pods in your Kubernetes cluster.


![image](https://user-images.githubusercontent.com/41900814/232405651-623d6cb6-a7c4-4798-be76-984e63f9a250.png)


You have to label a namespace with istio-injection=enabledto provide communication control to Istio in the namespace. The istio-injected label on the namespace of the pod is used by the Istio mutating admission controller to determine whether the Istio proxy should be injected into the pod deployment specification.

```
$ kubectl label namespace default istio-injection=enabled
```

![image](https://user-images.githubusercontent.com/41900814/232405758-0c7bb558-d3dd-4075-b10b-985fa70b5048.png)



Now our namespace is ready for demo app deployment.

## Demo App Deployment

Our app has 4 main Kubernetes components.

Kubernetes deployment for flaskfrontend
Kubernetes deployment for flaskbackend
Kubernetes Service for flaskfrontend
Kubernetes Service for flaskbackend

I will deploy this application in the default namespace. The namespace is already labeled and communication in this namespace is being handled by Istio.

``` 
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: flask-gateway
spec:
  selector:
    istio: ingressgateway # use Istio default gateway implementation
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "flask.example.com" # One or more hosts exposed by this gateway. 
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: flaskvirtualservice
spec:
  hosts:
  - "flask.example.com"  # destination hosts to which traffic is being sent. The hosts field applies to both HTTP and TCP services
  gateways:
  - flask-gateway
  http:
  - match:
    - uri:
        prefix: /list
    - uri:
        prefix: /home
    route:
    - destination:
        port:
          number: 5000
        host: flaskfrontend.default.svc.cluster.local
```
![image](https://user-images.githubusercontent.com/41900814/232405987-7f4cf556-7760-488c-8656-9e760fa6cb01.png)

Once deployment is done Istio will inject a sidecar proxy to handle all ingress and egress traffic. So when you list the pods, you can see 2 containers are running inREADY column. The first container is our app and the second one is sidecar Envoy proxy by Istio.

![image](https://user-images.githubusercontent.com/41900814/232406054-134face7-1a11-4cd3-ae0f-153ee25f8679.png)

Coming to the next section of containers in POD, you can seeinjected istio-proxy container. This container is Envoy proxy implementation for Istio. The other one is our application container.

![image](https://user-images.githubusercontent.com/41900814/232406145-a798ced6-13a8-465a-a6e5-128c45eb43e4.png)


Our deployment is ready to be accessed now. We will use port-forwardto access the application. Access the application and traverse to the tab Service Data to verify the backend service call as well.

Till this time everything looks okay. As a matter of fact, the communication started flowing through istio proxies.
![image](https://user-images.githubusercontent.com/41900814/232406200-f54454cf-df96-4240-a29d-61d64691ac4c.png)

## Visualizing Your Mesh


Istio provides integration with several different telemetry applications. These applications can help in viewing the topology of mesh, analyze the health of your mesh and other features. Let’s deploy a few of the following apps for our demo.


### Prometheus
When Istio telemetry is enabled, metrics data is stored in Prometheus. Prometheus is an open-source monitoring system and time series database.
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/addons/prometheus.yaml
```
![image](https://user-images.githubusercontent.com/41900814/232406437-d56f7191-5c50-4423-a968-65ee2c25caad.png)

to publish the Prometheus I am using istioctl utility itself
```
$ istioctl dashboard prometheus
http://localhost:9090
Failed to open browser; open http://localhost:9090 in your browser.
```



### Grafana
Grafana can be used to configure dashboards for Istio for monitoring. There are pre-configured dashboards but you can configure custom dashboards as well. Please note you need to have Prometheus deployed to use as a data source.
```
$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/addons/grafana.yaml
```
![image](https://user-images.githubusercontent.com/41900814/232406658-ec089c3a-8a5a-4d5f-a53b-675360925405.png)

![image](https://user-images.githubusercontent.com/41900814/232406703-cedac361-03e5-4abc-beff-d2d64d5fdd1c.png)


![image](https://user-images.githubusercontent.com/41900814/232406764-d52124a8-3537-4f65-b020-525ea13a6583.png)

Add and test your data source

![image](https://user-images.githubusercontent.com/41900814/232406870-af086210-b4d5-4aee-9d28-63ae16eb3399.png)


![image](https://user-images.githubusercontent.com/41900814/232406929-88b713e8-e47a-48b9-a37e-886873c7fb36.png)


![image](https://user-images.githubusercontent.com/41900814/232407064-81e9251a-3d66-4598-b5d3-1256043cc99f.png)

Kiali
Kiali is a management console for Istio. It retrieves Istio data and configurations, which are exposed through Prometheus and the cluster API. Kiali uses the data stored in Prometheus to figure out the mesh topology, show metrics, calculate health, show possible problems, etc.
```
$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/addons/kiali.yaml

```

![image](https://user-images.githubusercontent.com/41900814/232407191-651d181e-0d13-40aa-a047-66d3eacf5edb.png)


Use istioctl to access the dashboard —


![image](https://user-images.githubusercontent.com/41900814/232407250-132e069d-1953-4294-9fed-8d55f7f5e14f.png)



![image](https://user-images.githubusercontent.com/41900814/232407351-a9e13c8d-4bb8-4eb6-b5c3-d419700c8eda.png)

```
# I use shell script a lot to generate load
$ while true; do curl localhost:5000; sleep 1; done
```


![image](https://user-images.githubusercontent.com/41900814/232407402-336baacf-3466-4855-a196-05da68a95d1b.png)

Apart from this Kiali dashboard has a lot of features that can provide a complete overview of Istio components.


Gateway

Istio supports both ingress and egress gateways. Although service entries provide controlled access to external services, when combined with an Istio egress gateway, you can ensure that all external services are accessed through a single exit point. Having a single exit point allows you to provide specific security constraints on the nodes as well as the pods that all traffic leaving the mesh will pass.

When we deployed the Istio demo profile it has deployed Gateway components as well. We can use this gateway for our service exposure as well.

How to determine default Ingress IP and ports?

```
$ kubectl get svc istio-ingressgateway -n istio-system
```
![image](https://user-images.githubusercontent.com/41900814/232407576-a62e20e8-6757-4843-9068-aea0f8957504.png)



To find out details specific to Istio gateway ingress ports —


```
# INGRESS_PORT
$ kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}'
# SECURE_INGRESS_PORT
$ kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}'
# TCP_INGRESS_PORT
$ kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="tcp")].nodePort}'
# INGRESS_HOST
Your kubernetes worker node address

```

An ingress Gateway describes a load balancer operating at the edge of the mesh that receives incoming HTTP/TCP connections. It is like a door but it does not configure routing rules.
```
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: flask-gateway
spec:
  selector:
    istio: ingressgateway # use Istio default gateway implementation
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "flask.example.com"
```


In Istio routing part is configured using virtual service.


```
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: flaskvirtualservice
spec:
  hosts:
  - "flask.example.com"
  gateways:
  - flask-gateway
  http:
  - match:
    - uri:
        prefix: /list
    - uri:
        prefix: /home
    route:
    - destination:
        port:
          number: 5000
        host: flaskfrontend.default.svc.cluster.local
###########
The gateways list specifies in the above VirtualService manifest that only requests through the flask-gateway are allowed. It is time to deploy both of them in the default namespace.
###########
```


![image](https://user-images.githubusercontent.com/41900814/232407797-f897744c-2fb1-4a35-85d9-07e1910b6c30.png)

Now both of them are in place. Our cluster is not having a Load Balancer so we have the option of using NodePort as a service to test this. I will use curl to generate dummy requests. This time we are entering Service Mesh using Istio Gateway.


```
$ curl -s -I -HHost:flask.example.com http://[node_ip]:[node_port]/list
# please note I have used -H flag to set the Host HTTP header to request. This is required for our ingress Gateway because it was configured to handle - "flask.example.com"
# to find out port value
kubectl get service istio-ingressgateway -n istio-system -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}'
```


![image](https://user-images.githubusercontent.com/41900814/232407938-39d07a9d-e674-4fe3-9051-35a6de0de872.png)

Let’s visualize it in Kiali for better understanding.

# shell script
while true; do curl -HHost:flask.example.com http://10.0.1.6:31688/list; sleep 1; done



![image](https://user-images.githubusercontent.com/41900814/232407992-c8e5e693-1b3d-4443-bf98-42ec4888d501.png)


It's time to verify our existing Istio components and Application state.
![image](https://user-images.githubusercontent.com/41900814/232413041-4ec966da-08eb-47d3-8bf6-b08129951ed6.png)

Using proxy-status you can get an overview of your mesh
```
istioctl proxy-status
```


![image](https://user-images.githubusercontent.com/41900814/232413173-050e18ec-8a91-4dd6-8d4b-1c15251125cd.png)

State of Istio specific components —
```
$ istioctl proxy-config route istio-ingressgateway-5dc645f586-84bvf -n istio-system

```

![image](https://user-images.githubusercontent.com/41900814/232413211-6ba8fc26-19b6-4630-9680-d8c6aa7f6ef9.png)

```
Please note istionctl proxy-config route <pod name> is a very powerful command. It fetches route configuration for the Envoy instance in the specified pod.

Let’s test our service using Gateway.


```
$ curl -s -I -HHost:flask.example.com http://10.0.1.6:31688/home
```

![image](https://user-images.githubusercontent.com/41900814/232413314-57a44d0c-5487-405a-8fc0-385305c24d02.png)

```

Let’s have a visualization in Kiali -
![image](https://user-images.githubusercontent.com/41900814/232413349-b604841e-7cc9-4d4c-931f-48f7026cb228.png)

```



## Canary Deployment
Canary deployment is a deployment strategy that releases an application or service incrementally to a subset of users who are exposed to new updates before others. These users identity the release is good to proceed for full rollout or not.

Istio, as a service mesh supports routing rules to be applied to all services in the mesh, not just to ingress traffic. Using this capability we can implement Canary deployment easily. Canary deployments in Istio cab be configured using following items:

virtual service ( will be used to specify relative weights)
destination rule ( will be used to define subsets of the target service based on version labels.)


I have prepared another docker image v2 of our app with a slight change in text on the home page. This image will be used for target release.

The deployment will be a canary deployment using Istio. We will use Istio to shift traffic from one version of an app to another gradually. We will configure a sequence of routing rules that redirect a percentage of traffic from one destination to another using Virtual Services and Destination Rules.


Steps —

1. Deploy another version of the application without removing the existing application
2. Update existing VirtualService and add another object DestinationRule support weight-based routing. Destination Rule defines additional, version-based policies to the routing rules you are applying to your app.

```
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: flaskvirtualservice
spec:
  hosts:
  - "flask.example.com" # destination hosts to which traffic is being sent. The hosts field applies to both HTTP and TCP services
  gateways:
  - flask-gateway
  http:
  - match:
    - uri:
        prefix: /list
    - uri:
        prefix: /home
    route:
    - destination:
        host: flaskfrontend.default.svc.cluster.local
        subset: v1
        port:
          number: 5000
      weight: 90
    - destination:
        host: flaskfrontend.default.svc.cluster.local
        subset: v2 #  default to pods of the flaskfrontend service with label “version: v1” (i.e., subset v1)
        port:
          number: 5000
      weight: 10
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: flaskdestinationrule
spec:
  host: flaskfrontend.default.svc.cluster.local
  subsets:
  - name: v1
    labels:
      version: v1 # this is latest tag in our image
  - name: v2
    labels:
      version: v2
```

In the above VirtualServiceobject, check the route details for HTTP context root. We have two destination rules defined. One is having a weight of 90 and the subset is v1 and another one is 10 and the subset is v2. DestinationRule defines the labels of the target service based on version labels. So subset v1 is forwarding requests to current version of live application and v2 is the canary which we are releasing in the system gradually.


Let’s do the deployment for new updated app first.
![image](https://user-images.githubusercontent.com/41900814/232413873-76c8ba4d-825d-4d9d-999a-0a5a8b28ef22.png)



Now we can see the 2 pods of the frontend app are running. One with version 1 and another with version 2. It time to play with Istio now.

We will deploy updated Virtual Service and DestinationRules for weight-based routing first. It will modify the route rules and send 90% of connections to v1 of application and 10% to updated version.

![image](https://user-images.githubusercontent.com/41900814/232414003-746aa78b-475f-4182-9d05-646aa12817fd.png)

It’s time to test it. The best way I can advise is to use curl or any load generator. Please note you need to pass one hostname as a header so if you use browser then make sure you have a plugin to add custom header.

Load Generate using curl

This can generate a number of request very quickly. I have filtered the output using grep so that exact version can be printed.

```
$ while true; do curl -s -HHost:flask.example.com http://10.0.1.6:31688/home | grep -i "testing v"; sleep 0.5; done
```
  
  ![image](https://user-images.githubusercontent.com/41900814/232414108-a8fd8972-2ccf-411e-b01d-ec06d7f8d5cd.png)
Load Generate using Hey HTTP load generator

You can use a lightweight load generator hey as well. This tool is pretty powerful and can be used in these scenarios easily.

```
wget https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64
sudo mv hey_linux_amd64 /usr/bin/hey
$ hey -m GET -H "Host: flask.example.com" -z 15s -host "flask.example.com" http://10.0.1.6:31688/home
```
```


![image](https://user-images.githubusercontent.com/41900814/232414189-40d6153b-ecf8-4d70-8cea-80a8ac8c9803.png)


Again similar results we received from Hey as well. But to verify it, we will use Kiali dashboard to display or monitor.
![image](https://user-images.githubusercontent.com/41900814/232414259-16d93b55-b3f2-4951-9e58-ba60bf685c74.png)


Traffic distribution 50/50%
Now update the virtual service again and put 50 in weight for both versions and view in Kiali.

```
route:
    - destination:
        host: flaskfrontend.default.svc.cluster.local
        subset: v1
        port:
          number: 5000
      weight: 50
    - destination:
        host: flaskfrontend.default.svc.cluster.local
        subset: v2 #  default to pods of the flaskfrontend service with label “version: v1” (i.e., subset v1)
        port:
          number: 5000
      weight: 50
```


![image](https://user-images.githubusercontent.com/41900814/232414474-2ea26b47-18be-43c9-a3c1-7a0b44a00000.png)

