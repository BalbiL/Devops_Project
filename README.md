# DevOps Project
Authors: Lucas BALBI, Elise BRUNETON et Victor DENIS

## Description
This project is a messaging platform that allows users to create accounts, send messages, and manage conversations. 

## I. Work Performed
### 1. Web Application
We created a web application using Python -Flask, HTML/CSS and JS. The data is stored/pulled with a Redis database via GET/POST requests in Flask. 
The app runs on a python virtual environment (venv) on the host machine.

The app features:
   - User Management:
      - Create new users with name, surname, and email.
      - Delete users.
      - View a list of saved accounts.
      - Check for email duplicate when creating a new user

   - Messaging System:
      - Select a user to send messages.
      - View message history.
      - Delete messages.
      - Check for user validity when deleting a message

### 2. CI/CD pipeline
Use of GitHub actions with a ci-cd.yaml file featuring:

   - Continuous integration:
      - Specifies the environment for executing the CI tasks.
      - Uses the actions/checkout action to fetch the repository's code
      - Configures *Python 3.8*
      - Upgrades *pip* and installs the required dependencies listed in `dependances.txt`
      - Starts the Flask application (python app.py) in the background.
      - Checks if the app responds to HTTP requests using curl.

   - Continuous delivery/deployment:
      - Builds a Docker image for the application
      - Deploy with Docker Compose (error pops up)
      - Apply Kubernetes manifest. (error pops up)


This CI/CD pipeline automates testing and deployment for our project to ensure efficiency and reliability. It is triggered by any push or pull request on the main branch. The pipeline has two main jobs: Build and Deploy.

In the Build job, the repository is checked out, *Python 3.8* is set up, and dependencies are installed from `dependances.txt`. The Flask application is then launched and verified using a curl request to ensure it responds correctly. This step ensures that the application runs without errors in a clean environment.

The Deploy job begins after a successful build. It constructs a Docker image of the application and launches it using Docker Compose. Additionally, Kubernetes manifests located in the `kube/` directory are applied to deploy the application on a Kubernetes cluster. The deployment status is monitored to confirm its success.

### 3. Docker image
The app can be built into a docker image with a dockerfile. It can then be run as a container on localhost with the same features described in **1.Web application**.

The docker image was also pushed to DockerHub (and updated as needed). The DockerHub account can be found in part IV-Links.

### 4. Container orchestration with Docker-Compose
Automatization of the build of the app and the redis connection service with a docker-compose.yml file.
The app can now run directly without having to manually start redis services.

### 5. Orchestration using Kubernetes
Creation of MANIFEST YAML files that ensures:
   - Deployments (for Redis and the Flask app)
   - Services (for Redis and the Flask app)
   - persistent volume/persistent volume claim (for Redis)

App can run through a minikube service using a tunnel, exposing it on a displayed port of localhost.

### 6. Configure and provision a virtual environment / IaC approach
Configuration of a Vagrantfile to create an ubuntu VM with the VirtualBox provider, and allow for ssh connection to the VM from the host machine. Also creates a shared folder that contains the app files between the host machine and the VM.

Provisioning the VM with ansible, that allows for:
   - Updating apt packages
   - Installing Python3, Pip3 and python3-venv
   - Installing and starting Redis services
   - Installing and starting Docker services

***Note:*** *The app does not run automatically when connecting to the VM, but you can run it easily using docker or flask python3 (see part **III. Instructions**).*
 
### 7. Make a service mesh using Istio
In this section, we attempted to implement a service mesh using Istio for our Flask application. The objective was to deploy the application using Istio on a Kubernetes cluster and configure traffic routing between two different versions of the application. We also aimed to implement dynamic load balancing, allowing for progressive traffic shifting between the two versions.

**What Could a Service Mesh Have Brought to the Project?**
A service mesh like Istio offers several advantages that go beyond simple service communication. These include:
   - Traffic Management
   - Resilience and Observability
   - Security
   - Ease of Scaling

Incompatibility Between Istio and WSL2:
   - We developed and tested our solution on a Windows environment using WSL2 with Minikube. However, Istio does not always function correctly with WSL2 due to networking issues (limitations of the service tunnel).
   - Traffic shifting could not be verified because Istio services exposed via Minikube were inaccessible from the browser or curl.



## II. Screenshots
All screenshots are stored in the `captures/` folder. Here are the explaination for every screen:

### 1. WebApp
   ![User Creation & Message History](captures/page_web1.jpg)
   ![](captures/page_web2.jpg)

Running app inside a python virtual environment (venv) with python only
   ![Running app](captures/running_webapp.png)  

### 2. CI/CD
   ![](captures/)

### 3. Docker image
   ![](captures/)

### 4. Docker compose
   ![](captures/)

### 5. Orchestration using Kubernetes
   ![](captures/)

### 6. Configure and provision a virtual environment / IaC approach
   ![](captures/)



## III. Instructions

### 1. WebApp


### 2. Docker


### 3. Docker compose  


### 4. Kubernetes


### 5. Vagrant and IaC approach



## IV. Links
DockerHub account with image: https://hub.docker.com/u/balbil


## V. Additional Info
In the requirements, Flask Redis and Werkzeug are on older versions. That is because newer versions are not compatible with vagrant VMs, and Flask depends on Werkzeug so they have to be the same version.

The repository contains a file named `commande_utiles.txt`. This file was a tool to help us out for testing each other's part, as well as gain time and keep track of our progress.
