#!/usr/bin/env python
# coding: utf-8

# # Getting Started
# 
# As part of this section we will primarily understand different ways to get started with Postgres.
# * Connecting to Database
# * Using psql
# * Setup SQL Alchemy
# * SQL Alchemy + Postgres
# * SQL Alchemy Features
# * Setup Postgres using Docker
# * Data Loading Utilities

# ## Connecting to Database
# 
# We will be using JupyterHub based environment to master Postgresql. Let us go through the steps involved to get started using JupyterHub environment.
# * We will use Python Kernel with sql magic command and for that we need to first load the sql extension.
# * Create environment variable `DATABASE_URL` using SQL Alchemy format.
# * Write a simple query to get data from information schema table to validate database connectivity.

# In[1]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


get_ipython().run_line_magic('env', 'DATABASE_URL=postgresql://training:itversity!23@localhost:5432/training_sms')


# In[3]:


get_ipython().run_line_magic('sql', 'SELECT * FROM information_schema.tables LIMIT 10')


# ## Using psql
# 
# Let us understand how to use `psql` utility to perform database operations.
# * We need to have at least Postgres Client installed on the server from which you want to use psql to connect to Postgres Server.
# * If you are on the server where **Postgres Database Server** is installed, `psql` will be automatically available.
# * We can run `sudo -u postgres psql -U postgres` from the server provided you have sudo permissions on the server. Otherwise we need to go with `psql -U postgres -W` which will prompt for the password.
# * **postgres** is the super user for the postgres server and hence typically developers will not have access to it in non development environments.
# * As a developer, we can use following command to connect to a database setup on postgres server using user credentials.
# 
# ```
# psql -U sms_user -h <host_ip_or_dns_alias> -d <db_name> -W
# ```
# * We typically use `psql` to troubleshoot the issues in non development servers. IDEs such as **SQL Alchemy** might be better for regular usage as part of development and unit testing process.
# * For this course, we will be primarily using Jupyter based environment for practice.

# ## Setup SQL Alchemy

# ## SQL Alchemy + Postgres

# ## SQL Alchemy Features

# ## Setup Postgres using Docker

# ## Data Loading Utilities
