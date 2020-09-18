# mycompany-docker-flask-gunicorn
- Example Python3 app using flask and gunicorn
- Note: I used an arbitrary name: `myapp` in this example--use your service and repo name instead.
- This was done to create an internal company/cloud specific template for developers at my present employer.
  - As noted in the Dockerfile, this project was created for our internal use based on:
    - *[dockerizing-flask-with-postgres-gunicorn-and-nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)*
  - were we configure and use: 
    - Ingress Nginx L7 TLS on ELB
    - External DNS manged Route53 (via ingress annotations)
    - etc. 

### Requirements 
- For mycompany environments we should have all of these in place:
  - Cloud: Kube cluster with Ingress Nginx and requisite certs for L7 term at ELB/ingress.
  - Client: Terraform, tfenv, docker, etc.
  - Global recursive replace `mycompany.com` and `myapp` with your working top-level domain and requisite app/service name.
  - External DNS configured in your K8S cluster, etc. 

### Build tag and push to remote AWS ECS repo (locally)
- build script requires one arg which is the version to build/tag/push, etc.
  - Note:  this would be for one-off builds, regular builds should be done in CI/CD (jenkins) using dedicated project.
```console
./build 0.1.1
```
- Push tagged one-off local build to Dev Kube cluster
```console
k apply --recursive -f ./k8s -n myapp
```

### NOTE: Apps should have at least dummy '/alive' and '/ready' routes
##### This allows kube to know if the app is healthy/available
- I.e. see `./services/web/project/__init__.py`
```console
# define your app/service routes here
@app.route("/")
def hello_world():
    return jsonify(hello="world")

# Liveliness check
@app.route("/alive")
def alive():
    return 'OK'

# Mock readiness check
@app.route("/ready")
def ready():
    return jsonify(
        backend='ready',
        db='ready',
        queue='ready'
    )
```
- This also allows us to curl the above URI's and get the expected output:
  - I.e.:
    - curl https://myapp.dev.mycompany.com/alive
    - curl https://myapp.dev.mycompany.com/ready


#### myapp app Kube resources should look like this:
```console
k get all -n myapp
NAME                         READY   STATUS    RESTARTS   AGE
pod/myapp-754b4c46bf-whml2   1/1     Running   0          29m
pod/myapp-754b4c46bf-zq77v   1/1     Running   0          29m

NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/myapp   ClusterIP   172.20.226.37   <none>        80/TCP    29m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp   2/2     2            2           29m

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/myapp-754b4c46bf   2         2         2       29m
```

#### myapp Ingress looks like this
```console
k get ing -A | grep myapp
myapp                 myapp                  myapp.dev.mycompany.com                 a123laa2asd6adsa9asdasdasdsadasd-123456789.us-west-2.elb.amazonaws.com   80      128m
```

#### Refactoring Options
- enable the provided commented out HPA horizontal pod autoscaler
- add nginx, and other layers/requirements as needed, etc.
