#!/usr/bin/env python
# coding: utf-8

# # Writing Basic SQL Queries
# 
# As part of this section we will primarily focus on writing basic queries.
# 
# * Standard Transformations
# * Overview of Data Model
# * Define Problem Statement – Daily Product Revenue
# * Preparing Tables
# * Selecting or Projecting Data
# * Filtering Data
# * Joining Tables – Inner
# * Joining Tables – Outer
# * Performing Aggregations
# * Sorting Data
# * Solution – Daily Product Revenue

# ## Standard Transformations
# 
# Here are some of the transformations we typically perform on regular basis.
# * Projection of data
# * Filtering data
# * Performing Aggregations
# * Joins
# * Sorting
# * Ranking (will be covered as part of advanced queries)

# ## Overview of Data Model
# 
# We will be using retail data model for this section. It contains 6 tables.
# * Table list
#   * orders
#   * order_items
#   * products
#   * categories
#   * departments
#   * customers
# * **orders** and **order_items** are transactional tables.
# * **products**, **categories** and **departments** are non transactional tables which have data related to product catalog.
# * **customers** is a non transactional table which have customer details.
# * There is 1 to many relationship between **orders** and **order_items**.
# * There is 1 to many relationship between **products** and **order_items**. Each order item will have one product and product can be part of many order_items.
# * There is 1 to many relationship between **customers** and **orders**. A customer can place many orders over a period of time but there cannot be more than one customer for a given order.
# * There is 1 to many relationship between **departments** and **categories**. Also there is 1 to many relationship between **categories** and **products**.
# * There is hierarchical relationship from departments to products - **departments** -> **categories** -> **products**

# ## Define Problem Statement – Daily Product Revenue
# 
# Let us try to get daily product revenue using retail tables.
# * daily is derived from orders.order_date.
# * product has to be derived from products.product_name.
# * revenue has to be derived from order_items.order_item_subtotal.
# * We need to join all the 3 tables, then group by order_date, product_id as well as product_name to get revenue using order_item_subtotal.
# * Get Daily Product Revenue using products, orders and order_items data set.
# * We have following fields in **orders**.
#   * order_id
#   * order_date
#   * order_customer_id
#   * order_status
# * We have following fields in **order_items**.
#   * order_item_id
#   * order_item_order_id
#   * order_item_product_id
#   * order_item_quantity
#   * order_item_subtotal
#   * order_item_product_price
# * We have following fields in **products**
#   * product_id
#   * product_category_id
#   * product_name
#   * product_description
#   * product_price
#   * product_image
# * We have one to many relationship between orders and order_items.
# * **orders.order_id** is **primary key** and **order_items.order_item_order_id** is foreign key to **orders.order_id**.
# * We have one to many relationship between products and order_items.
# * **products.product_id** is **primary key** and **order_items.order_item_product_id** is foreign key to **oproducts.product_id**
# * By the end of this module we will explore all standard transformation and get daily product revenue using following fields.
#   * **orders.order_date**
#   * **order_items.order_item_product_id**
#   * **products.product_name**
#   * **order_items.order_item_subtotal** (aggregated using date and product_id).
# * We will consider only **COMPLETE** or **CLOSED** orders.
# * As there can be more than one product names with different ids, we have to include product_id as part of the key using which we will group the data.

# ## Preparing Tables
# 
# Let us ensure we have all the tables are ready to come up with the solution for the problem statement.
# * Ensure that we have required database and user for retail data. We might provide the database as part of our labs.
# 
# ```
# psql -U postgres -h localhost -p 5433 -W
# 
# CREATE DATABASE itversity_retail_db;
# CREATE USER itversity_retail_user WITH ENCRYPTED PASSWORD 'retail_password';
# GRANT ALL ON DATABASE itversity_retail_db TO itversity_retail_user;
# ```
# 
# * Create Tables using the script provided. You can either use `psql` or **SQL Alchemy**.
# 
# ```
# psql -U itversity_retail_user \
#   -h localhost \
#   -p 5433 \
#   -d itversity_retail_db \
#   -W
# 
# \i retail_db/create_db_tables_pg.sql
# ```
# 
# * Data shall be loaded using the script provided.
# 
# ```
# \i retail_db/load_db_tables_pg.sql
# ```
# 
# * Run queries to validate we have data in all the 3 tables.

# In[1]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


get_ipython().run_line_magic('env', 'DATABASE_URL=postgresql://itversity_retail_user:retail_password@localhost:5433/itversity_retail_db')


# In[3]:


get_ipython().run_line_magic('sql', 'SELECT current_database()')


# In[4]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT * FROM information_schema.tables \nWHERE table_catalog = 'itversity_retail_db' \n    AND table_schema = 'public' \nLIMIT 10")


# In[5]:


display(result_set)


# In[6]:


get_ipython().run_line_magic('sql', 'SELECT * FROM orders LIMIT 10')


# In[7]:


get_ipython().run_line_magic('sql', 'SELECT * FROM order_items LIMIT 10')


# In[8]:


get_ipython().run_line_magic('sql', 'SELECT * FROM products LIMIT 10')


# In[9]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM orders')


# In[10]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM order_items')


# In[11]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM products')


# ## Selecting or Projecting Data
# 
# Let us understand different aspects of projecting data. We primarily using `SELECT` to project the data.
# * We can project all columns using `*` or some columns using column names.
# * We can provide aliases to a column or expression using `AS` in `SELECT` clause.
# * `DISTINCT` can be used to get the distinct records from selected columns. We can also use `DISTINCT *` to get unique records using all the columns.
# * As part of `SELECT` clause we can have aggregate functions such as `count`, `sum` etc.

# In[12]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[13]:


get_ipython().run_line_magic('env', 'DATABASE_URL=postgresql://itversity_retail_user:retail_password@localhost:5433/itversity_retail_db')


# In[14]:


get_ipython().run_line_magic('sql', 'SELECT * FROM orders LIMIT 10')


# In[15]:


get_ipython().run_line_magic('sql', "SELECT * FROM information_schema.columns WHERE table_catalog = 'itversity_retail_db' AND table_name = 'orders'")


# In[16]:


get_ipython().run_line_magic('sql', 'SELECT order_customer_id, order_date, order_status FROM orders LIMIT 10')


# In[17]:


get_ipython().run_line_magic('sql', "SELECT order_customer_id, to_char(order_date, 'yyyy-MM'), order_status FROM orders LIMIT 10")


# In[18]:


get_ipython().run_line_magic('sql', "SELECT order_customer_id, to_char(order_date, 'yyyy-MM') AS order_month, order_status FROM orders LIMIT 10")


# In[19]:


get_ipython().run_line_magic('sql', "SELECT DISTINCT to_char(order_date, 'yyyy-MM') AS order_month FROM orders")


# In[20]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM orders')


# In[21]:


get_ipython().run_line_magic('sql', "SELECT count(DISTINCT to_char(order_date, 'yyyy-MM')) AS distinct_month_count FROM orders")


# ## Filtering Data
# 
# Let us understand how we can filter the data as part of our queries.
# * We use `WHERE` clause to filter the data.
# * All comparison operators such as `=`, `!=`, `>`, `<`, etc can be used to compare a column or expression or literal with another column or expression or literal.
# * We can use operators such as `LIKE` with % and `regexp_matches` for pattern matching.
# * Boolan `OR` and `AND` can be performed when we want to apply multiple conditions.
#   * Get all orders with order_status equals to COMPLETE or CLOSED. We can also use IN operator.
#   * Get all orders from month 2014 January with order_status equals to COMPLETE or CLOSED
# * We need to use `IS NULL` and `IS NOT NULL` to compare against null values.

# In[22]:


get_ipython().run_line_magic('sql', "SELECT * FROM orders WHERE order_status = 'COMPLETE' LIMIT 10")


# In[23]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM orders')


# In[24]:


get_ipython().run_line_magic('sql', "SELECT count(1) FROM orders WHERE order_status = 'COMPLETE'")


# In[25]:


get_ipython().run_line_magic('sql', "SELECT * FROM orders WHERE order_status IN ('COMPLETE', 'CLOSED') LIMIT 10")


# In[26]:


get_ipython().run_line_magic('sql', "SELECT count(1) FROM orders WHERE order_status IN ('COMPLETE', 'CLOSED')")


# In[27]:


get_ipython().run_line_magic('sql', "SELECT count(1) FROM orders WHERE order_status = 'COMPLETE' OR order_status = 'CLOSED'")


# In[28]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT * FROM orders \nWHERE order_status IN ('COMPLETE', 'CLOSED')\n    AND to_char(order_date, 'yyyy-MM-dd') LIKE '2014-01%'\nLIMIT 10")


# In[29]:


display(result_set)


# In[30]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT * FROM orders \nWHERE order_status IN ('COMPLETE', 'CLOSED')\n    AND to_char(order_date, 'yyyy-MM') = '2014-01'\nLIMIT 10")


# In[31]:


display(result_set)


# In[32]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT count(1) FROM orders \nWHERE order_status IN ('COMPLETE', 'CLOSED')\n    AND to_char(order_date, 'yyyy-MM-dd') LIKE '2014-01%'")


# In[33]:


display(result_set)


# In[34]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT count(1) FROM orders \nWHERE order_status IN ('COMPLETE', 'CLOSED')\n    AND to_char(order_date, 'yyyy-MM') = '2014-01'")


# In[35]:


display(result_set)


# ## Joining Tables – Inner
# 
# Let us understand how to join data from multiple tables.
# 
# * We will primarily focus on ASCII style join (**JOIN with ON**).
# * There are different types of joins.
#   * INNER JOIN - Get all the records from both the datasets which satisfies JOIN condition.
#   * OUTER JOIN - We will get into the details as part of the next topic
# * Example for INNER JOIN
# 
# ```
# SELECT o.order_id,
#     o.order_date,
#     o.order_status,
#     oi.order_item_subtotal
# FROM orders o JOIN order_items oi
#     ON o.order_id = oi.order_item_order_id
# LIMIT 10
# ```
# 
# * We can join more than 2 tables in one query. Here is how it will look like.
# 
# ```
# SELECT o.order_id,
#     o.order_date,
#     o.order_status,
#     oi.order_item_subtotal
# FROM orders o JOIN order_items oi
#     ON o.order_id = oi.order_item_order_id
#     JOIN products p
#     ON p.product_id = oi.order_item_product_id
# LIMIT 10
# ```
# 
# * If we have to apply additional filters, it is recommended to use WHERE clause. ON clause should only have join conditions.
# * We can have non equal join conditions as well, but they are not used that often.
# * Here are some of the examples for INNER JOIN:
#   * Get order id, date, status and item revenue for all order items.
#   * Get order id, date, status and item revenue for all order items for all orders where order status is either COMPLETE or CLOSED.
#   * Get order id, date, status and item revenue for all order items for all orders where order status is either COMPLETE or CLOSED for the orders that are placed in the month of 2014 January.

# In[36]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_subtotal\nFROM orders o JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nLIMIT 10')


# In[37]:


display(result_set)


# In[38]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM orders')


# In[39]:


get_ipython().run_line_magic('sql', 'SELECT count(1) FROM order_items')


# In[40]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT count(1)\nFROM orders o JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id')


# In[41]:


display(result_set)


# In[42]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_subtotal\nFROM orders o JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE o.order_status IN ('COMPLETE', 'CLOSED')\nLIMIT 10")


# In[43]:


display(result_set)


# In[44]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT count(1)\nFROM orders o JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE o.order_status IN ('COMPLETE', 'CLOSED')\nLIMIT 10")


# In[45]:


display(result_set)


# In[46]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_subtotal\nFROM orders o JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE o.order_status IN ('COMPLETE', 'CLOSED')\n    AND to_char(order_date, 'yyyy-MM') = '2014-01'\nLIMIT 10")


# In[47]:


display(result_set)


# In[48]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT count(1)\nFROM orders o JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE o.order_status IN ('COMPLETE', 'CLOSED')\n    AND to_char(order_date, 'yyyy-MM') = '2014-01'\nLIMIT 10")


# In[49]:


display(result_set)


# ## Joining Tables - Outer
# 
# Let us understand how to perform outer joins using SQL. There are 3 different types of outer joins.
# * `LEFT OUTER JOIN` (default) - Get all the records from both the datasets which satisfies JOIN condition along with those records which are in the left side table but not in the right side table.
# * `RIGHT OUTER JOIN` - Get all the records from both the datasets which satisfies JOIN condition along with those records which are in the right side table but not in the left side table.
# * `FULL OUTER JOIN` - left union right
# * When we perform the outer join (lets say left outer join), we will see this.
#   * Get all the values from both the tables when join condition satisfies.
#   * If there are rows on left side tables for which there are no corresponding values in right side table, all the projected column values for right side table will be null.
# * Here are some of the examples for outer join.
#     * Get all the orders where there are no corresponding order items.
#     * Get all the order items where there are no corresponding orders.

# In[50]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_order_id,\n    oi.order_item_subtotal\nFROM orders o LEFT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nLIMIT 10')


# In[51]:


display(result_set)


# In[52]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT count(1)\nFROM orders o LEFT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id')


# In[53]:


display(result_set)


# In[54]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_order_id,\n    oi.order_item_subtotal\nFROM orders o LEFT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE oi.order_item_order_id IS NULL\nLIMIT 10')


# In[55]:


display(result_set)


# In[56]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT count(1)\nFROM orders o LEFT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE oi.order_item_order_id IS NULL')


# In[57]:


display(result_set)


# In[58]:


get_ipython().run_cell_magic('sql', 'result_set <<', "\nSELECT count(1)\nFROM orders o LEFT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE oi.order_item_order_id IS NULL\n    AND o.order_status IN ('COMPLETE', 'CLOSED')")


# In[59]:


display(result_set)


# In[60]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_order_id,\n    oi.order_item_subtotal\nFROM orders o RIGHT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nLIMIT 10')


# In[61]:


display(result_set)


# In[62]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT count(1)\nFROM orders o RIGHT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id')


# In[63]:


display(result_set)


# In[64]:


get_ipython().run_cell_magic('sql', 'result_set <<', '\nSELECT o.order_id,\n    o.order_date,\n    o.order_status,\n    oi.order_item_order_id,\n    oi.order_item_subtotal\nFROM orders o RIGHT OUTER JOIN order_items oi\n    ON o.order_id = oi.order_item_order_id\nWHERE o.order_id IS NULL\nLIMIT 10')


# In[65]:


display(result_set)


# ## Performing Aggregations

# ## Sorting Data

# ## Solution – Daily Product Revenue
