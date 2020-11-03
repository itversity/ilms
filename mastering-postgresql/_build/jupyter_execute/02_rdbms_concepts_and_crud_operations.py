#!/usr/bin/env python
# coding: utf-8

# # RDBMS Concepts and CRUD Operations
# 
# Let us understand how to perform CRUD operations using Postgresql.
# 
# * Normalization Principles
# * Tables as Relations
# * Database Operations - Overview
# * CRUD Operations
# * Creating Table
# * Inserting Data
# * Updating and Deleting Data
# * Overview of Transactions
# * Exercise - CRUD Operations

# ## Normalization Principles

# ## Tables as Relations

# ## Database Operations - Overview
# 
# Let us get an overview of Database Operation we typically perform on regular basis. They are broadly categorized into the following:
# 
# * DDL - Data Definition Language
#   * CREATE/ALTER/DROP Tables
#   * CREATE/ALTER/DROP Indexes
#   * Add constraints to tables
#   * CREATE/ALTER/DROP Views
#   * CREATE/ALTER/DROP Sequences
# * DML - Data Manipulation Language
#   * Inserting new data into the table
#   * Updating existing data in the table
#   * Deleting existing data from the table
# * DQL - Data Query Language
#   * Read the data from the table
# 
# On top of these we also use TCL (Transaction Control Language). As part of this section we will primarily focus on CRUD Operations which includes DML and basic DDL.

# ## CRUD Operations
# 
# Let us get an overview of CRUD Operations. They are nothing but DML and queries to read the data while performing database operations.
# 
# * CRUD is widely used from application development perspective.
# * C - CREATE (INSERT)
# * R - READ (READ)
# * U - UPDATE (UPDATE)
# * D - DELETE (DELETE)
# 
# As part of the application development process we perform CRUD Operations using REST APIs.

# ## Creating Table
# 
# Before getting into action with respect to basic DML and queries or CRUD operations, we need to prepare tables.
# 
# At this time we have not covered DDL (to create objects such as table) yet. For now just create the table by copy pasting and we will get into concepts as part of the subsequent sections.
# * Connect to the database.
# * Create the table.

# In[1]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


get_ipython().run_line_magic('env', 'DATABASE_URL=postgresql://training:itversity!23@localhost:5432/training_sms')


# In[3]:


get_ipython().run_line_magic('sql', 'SELECT * FROM information_schema.tables LIMIT 10')


# In[4]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nCREATE TABLE users (\n  user_id SERIAL PRIMARY KEY,\n  user_first_name VARCHAR(30) NOT NULL,\n  user_last_name VARCHAR(30) NOT NULL,\n  user_email_id VARCHAR(50) NOT NULL,\n  user_email_validated BOOLEAN DEFAULT FALSE,\n  user_password VARCHAR(200),\n  user_role VARCHAR(1) NOT NULL DEFAULT 'U', --U and A\n  is_active BOOLEAN DEFAULT FALSE,\n  create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n  last_updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);")


# * Let us connect to psql and check the output of `\d`. You will see **users table** as well as **sequence for user_id** created.

# In[5]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# ## Inserting Data
# 
# Let us see how to insert the data into the table.
# * We need to use INSERT clause to insert the data. Here is the sample syntax.
# ```
# INSERT INTO <table_name> (col1, col2, col3)
# VALUES (val1, val2, val3)
# ```
# * If we don't pass columns after table name then we need to specify values for all the columns. It is not good practice to insert records with out specifying column names.
# * If we do not specify value for `SERIAL` field, a sequence generated number will be used.
# * It is not mandatory to pass the values for those fields where `DEFAULT` is specified. Values specified in `DEFAULT` clause will be used.
# * It is mandatory to specify columns and corresponding values for all columns where `NOT NULL` is specified.

# In[6]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nINSERT INTO users (user_first_name, user_last_name, user_email_id)\nVALUES ('Scott', 'Tiger', 'scott@tiger.com')")


# In[7]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nINSERT INTO users (user_first_name, user_last_name, user_email_id)\nVALUES ('Donald', 'Duck', 'donald@duck.com')")


# In[8]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# In[9]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nINSERT INTO users (user_first_name, user_last_name, user_email_id, user_role, is_active)\nVALUES ('Mickey', 'Mouse', 'mickey@mouse.com', 'U', true)")


# In[10]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# In[11]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nINSERT INTO users \n    (user_first_name, user_last_name, user_email_id, user_password, user_role, is_active) \nVALUES \n    ('Gordan', 'Bradock', 'gbradock0@barnesandnoble.com', 'h9LAz7p7ub', 'U', true),\n    ('Tobe', 'Lyness', 'tlyness1@paginegialle.it', 'oEofndp', 'U', true),\n    ('Addie', 'Mesias', 'amesias2@twitpic.com', 'ih7Y69u56', 'U', true)")


# In[12]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# ## Updating Data
# 
# Let us see how we can update data in the table.
# * Typical syntax
# ```
# UPDATE <table_name>
# SET
#     col1 = val1,
#     col2 = val2
# WHERE <condition>
# ```
# * If `WHERE` condition is specified all rows in the table will be updated.
# * For now we will see basic examples for update. One need to have good knowledge about `WHERE` clause to take care of complex conditions.

# * Set user role for user_id 1 as 'A'

# In[13]:


get_ipython().run_line_magic('sql', "UPDATE users SET user_role = 'A' WHERE user_id = 1")


# In[14]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# * Set user_email_validated as well as is_active to true for all users

# In[15]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nUPDATE users\nSET\n    user_email_validated = true,\n    is_active = true')


# In[16]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# ## Deleting Data
# 
# Let us understand how to delete the data from a table.
# * Typical Syntax - `DELETE FROM <table> WHERE <condition>`.
# * If we do not specify condition, it will delete all the data from the table.
# * It is not recommended to use delete with out where condition to delete all the data (instead we should use `TRUNCATE`).
# * For now we will see basic examples for update. One need to have good knowledge about `WHERE` clause to take care of complex conditions.

# * Delete all those records from users where the password is not set. We need to use `IS NULL` as condition to compare against Null values.

# In[17]:


get_ipython().run_line_magic('sql', 'DELETE FROM users WHERE user_password IS NULL')


# In[18]:


get_ipython().run_line_magic('sql', 'SELECT * FROM users')


# ## Overview of Transactions
# 
# Let us go through the details related to transactions.
# * In Postgresql by default each DML operation is automatically committed.
# * To ensure that group of operations are committed together, we need to first initiate a transaction.

# ## Exercise - CRUD Operations

# In[ ]:




