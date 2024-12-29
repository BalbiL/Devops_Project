# DevOps Project
Lucas Balbi, Elise Bruneton et Victor Denis

## Description
This project is a messaging platform that allows users to create accounts, send messages, and manage conversations. 

## I. Work Performed
### 1. Web Application

We created a web application using Python -Flask, HTML/CSS and JS. 
The data is stored/pulled with a Redis database via GET/POST requests in Flask. The app runs on a python virtual environment (venv) on the host machine.

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

Use of GitHub actions with a workflow.yaml file featuring:
   - Continuous integration:
      - Specifies the environment for executing the CI tasks.
      - Uses the actions/checkout action to fetch the repository's code
      - Configures Python 3.8
      - Upgrades pip and installs the required dependencies listed in `dependances.txt`
      - Starts the Flask application (python app.py) in the background.
      - Checks if the app responds to HTTP requests using curl.

   - Continuous delivery/deployment:
      - Builds a Docker image for the application
      - Deploy with Docker Compose
      - Apply Kubernetes manifest.

### 3.Docker image

The app can be built into a docker image with a dockerfile. It can then be run as a container on localhost with the same features described in **1. Web Application**.

The docker image was also pushed to DockerHub (and updated as needed). The DockerHub account can be found in part IV-Links.

### 4.Container orchestration with Docker-Compose

Automatization of the build of the app and the redis connection service with a docker-compose.yml file.
The app can now run directly without having to manually start redis services.

### 5.Orchestration using Kubernetes

Creation of MANIFEST YAML files that ensures:
   - Deployments (for Redis and the Flask app)
   - Services (for Redis and the Flask app)
   - persistent volume/persistent volume claim (for Redis)

App can run through a minikube service using a tunnel, exposing it on a displayed port of localhost.

### 6.Configure and provision a virtual environment / IaC approach

Configuration of a Vagrantfile to create an ubuntu VM with the VirtualBox provider, and allow for ssh connection to the VM from the host machine. Also creates a shared folder that contains the app files between the host machine and the VM.

Provisioning the VM with ansible, that allows for:
   - Updating apt packages
   - Installing Python3, Pip3 and python3-venv
   - Installing and starting Redis services
   - Installing and starting Docker services

***Note:*** *The app does not run automatically when connecting to the VM, but you can run it easily using docker or flask python3 (see part **III. Instructions**).*
 

## II. Screenshots
All screenshots are stored in the `captures/` folder. Here are the explaination for every screen:

### 1. WebApp
   ![User Creation & Message History](captures/page_web1.jpg)
   (captures/page_web2.jpg)

   ![Running app](captures/running_webapp.png.jpg)  
   Running app inside a python virtual environment (venv) with python only

### 2. CI/CD

### 3. Docker image

### 4. Docker compose

### 5. Orchestration using Kubernetes

### 6. Configure and provision a virtual environment / IaC approach


## III. Instructions




### Prerequisites
1. Docker installed on your machine.
2. Python 3.9 or above.
3. Redis.
4. 

1. First Step:
- Clone the repository:
   ```bash
   git clone https://github.com/BalbiL/Devops_Project.git
- Navigate to the `WebApp/` directory.
- Install dependencies:
   ```bash
      pip install -r dependances.txt

2. Redis:
- Start redis
   ```bash
      sudo service redis start
- Open the Redis shell:
   ```bash
      redis-cli
- Test server response:
   ```bash
      redis-cli ping

3. Docker:
- Start Redis:
   ```bash
      sudo service redis start
- Build the app image: 
   ```bash
      docker build -t flask-webapp
- Run the app via Docker:
   ```bash
      docker run --network="host" -e REDIS_HOST=127.0.0.1 -d flask-webapp
- Check if the container is running:
   ```bash
      docker ps
- The container runs in the background thanks to the -d option in the run command. To stop the container:
   ```bash
      docker stop idcontainer
*The container ID is displayed with docker ps*

4. Docker compose:
- Start the container:
   ```bash
      docker-compose up -d
***Note!*** *Redis is started by docker-compose. Ensure to stop any existing Redis services before running: sudo service redis stop*
- Debugging:
   ```bash
      docker-compose logs -f
*Allows you to view the container logs.*
- Verify the container is running:
   ```bash
      docker-compose ps
- Stop the container:
   ``bash
      docker-compose down

## IV. Links

## V. Additional Info