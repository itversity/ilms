#!/usr/bin/env python
# coding: utf-8

# # Bonus - Setup Exclusive Labs
# 
# As part of this section, we are going to see the details related to setting up exclusive labs on GCP leveraging $300 credit.
# 
# * Overview of GCP
# * Provisioning Virtual Machine
# * Setup Docker and Key Concepts
# * Using Docker CLI
# * Setup Jupyter Lab Environment
# * Setup Postgresql Database
# * Overview of psql CLI
# * SQL Integration - Jupyter Lab
# * Conclusion

# ## Overview of GCP
# 
# Let us get an overview of GCP and the credit provided by Google.
# * Sign up to GCP (you need to have credit card to use it).
# * Overview of GCP Web Console
# * Understanding GCP Pricing
#   * Virtual Machine (Variable cost)
#   * Storage (Fixed cost)
#   * Static IP (Fixed cost)
# * You also need to understand how to get the billing details.
# * Keep in mind that you do not open up ports unnecessarily as the server can be hijacked by malware and can dry out your credits.

# ## Provisioning Virtual Machine
# 
# Let us understand how to provision a virtual machine from GCP.
# * We need to go to Virtual Machines
# * Overview of different operating systems
# * Choose the server configuration
# * Choose OS - Ubuntu 18.04
# * Choose the size of hard drive (32 GB should suffice)
# * Once the virtual machine is created you need to spend some time understand how to manage it.
#   * Stopping the virtual machine
#   * Starting the virtual machine
#   * Restarting the virtual machine
#   * Deleting the virtual machine
#   * Connecting to running server
#   * Configuring Firewall Rules (it will be covered in later topics a bit in detail)
# * Make sure the virtual machine is stopped when you are not using it, otherwise you will run out of credits fast.

# ## Setup Docker and Key Concepts
# 
# As our VM is up and running, let us make sure to setup docker and validate. Also we will get into some of the key concepts related to docker.
# * Follow any standard article to setup Docker on Ubuntu 18.04. These are the commands that are used to setup Docker.
# 
# ```
# sudo apt update
# sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
# sudo apt update
# apt-cache policy docker-ce
# sudo apt install docker-ce
# sudo systemctl status docker
# ```
# 
# * Make sure to add the user you logged in to a group called as **docker**. It is primarily to not to use sudo to manage docker containers. Run `sudo usermod -aG docker ${USER}`
# * Once the user is added to the group, you might have to reconnect to the session.
# 
# **Docker Key Concepts**
# Here are some of the key concepts related to docker.
# * Ephemeral - if no service is running in the container, it will be in stopped state.
# * Image - a file which will have light weight OS kernel in hibernate or paused state.
# * Container - a process which is created using an image or images and might be in one of running, stopped, exit (error) status.
# * Here are the steps to have a container for process such as nginx.
#   * Download nginx image
#   * Start the container with entry point
#   * Once the container is started, you can stop at any point in time.
#   * For containers like hello world where there is no active application associated with, they will go to stopped state after performing the designated tasks.
# * Here are some of the usage scenarios for docker containers.
#   * Maintain databases for development activities. It is not recommended to use docker to maintain production databases.
#   * Maintain web or application servers for development activities. We can even run production applications as part of docker containers.
#   * Run ad hoc batch data processing applications or data pipelines in development or production.

# ## Using Docker CLI
# 
# Let us get an overview about Docker CLI to manage docker components such as images, containers etc.
# * `docker images` is the main command to manage images.
#   * `docker image pull` or `docker pull`
# * `docker container` is the main command to manage containers.
# * We can use `docker run` command to quickly start the container.
#   * It will pull the image from docker hub, if the image is not already available.
#   * Creates the container, if the container is not already created.
#   * Starts the container, if the container is not started.
#   * If there is no server running the container, it will just come out of the container.
# * `docker run --name hw hello-world` will pull the **hello-world** image, creates the container with name **hw**, starts the container and stops it after printing Hello message as there is no service associated with it. You can run below commands using Linux Terminal.

# In[1]:


get_ipython().run_cell_magic('sh', '', '\ndocker ps -a')


# In[2]:


get_ipython().run_cell_magic('sh', '', '\ndocker images -a')


# In[3]:


get_ipython().run_cell_magic('sh', '', '\ndocker run --name hw hello-world')


# In[6]:


get_ipython().run_cell_magic('sh', '', '\ndocker images -a')


# In[1]:


get_ipython().run_cell_magic('sh', '', '\ndocker ps -a')


# ## Setup Jupyter Lab Environment
# 
# To get similar experience as demonstrated in the course content, we would recommend to setup Jupyter Lab Environment.
# * Connect to the Virtual Machines provisioned from GCP.
# * Make sure Python 3 is installed in the Virtual Machine. Use `python3` to validate
# * Make sure pip is installed in the Virtual Machine.
# * Install Jupyter Lab using pip `python3 -m pip install jupyterlab`.
# * You can launch Jupyter Lab using `jupyter lab --ip 0.0.0.0` and it will start with default port number **8888**.
# * We need to open the port number by going to Network and then Firewall for the Virtual Machine.
# * Make sure you can access Jupyter Lab using the browser on your laptop.
# 
# ```
# sudo apt install python3-pip -y
# python3 -m pip install jupyter lab
# jupyter lab --ip 0.0.0.0
# ```

# ## Setup Postgresql Database
# 
# Let us setup Postgresql Database using Docker.
# * Pull the image
# * Start the container
# * You need to understand all the key arguments used for creating the container.

# ## Overview of psql CLI
# 
# As the container is ready let us make sure that we can connect to the container using psql CLI.
# 
# * We can use `docker exec` command to connect to running container or run a single command.
# * First, we need to ensure that container is up and running. We can use `docker ps`.
# * Fetch the container name.
# * Use `docker exec -it pg_db bash` to connect to the container's console.
# * We can also run indiviual commands - example: `docker exec -it pg_db ls -ltr`.
# * To connect to psql CLI either we can use bash and then psql or we can directly run psql command - `docker exec -it pg_db psql -U postgres`
# * Here are the some of the commands you can run to get comfortable with `psql` CLI via docker.
#   * List databases - `\l`
#   * List tables - `\d`
#   * Check the current database - `SELECT current_database()`
#   * Create new database - `CREATE DATABASE test_db;`
#   * Change to database - `\c test_db`
#   * Create table - `CREATE TABLE t (i INT)`
#   * Describe table - `\d t`

# ## SQL Integration - Jupyter Lab
# 
# It might not be comfortable to use psql to learn more about SQL using Postgresql. We can either use SQL Alchemy or Jupyter Lab to accelerate our learning process.
# 
# Let us understand how we can integrate Jupyter Lab with Postgresql.
# * Install **ipython-sql** - `pip install ipython-sql`
# * Install **SQLAlchemy** - `pip install sqlalchemy`
# * Load the magic command as extension to Python 3 kernel.
# * Validate by connecting to database and then running some queries.

# ## Conclusion

# In[ ]:




