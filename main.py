# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return first and last names of employees who work in the Boston office
df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName
FROM employees AS e
JOIN offices AS o
    ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
ORDER BY e.firstName, e.lastName
""", conn)

# STEP 2
# Find offices that have no employees
df_zero_emp = pd.read_sql("""
SELECT o.officeCode, o.city
FROM offices AS o
LEFT JOIN employees AS e
    ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL
""", conn)

# STEP 3
# Return all employees with the city and state of their office
df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees AS e
LEFT JOIN offices AS o
    ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Return customer contacts who have no placed any orders
df_contacts = pd.read_sql("""
SELECT
    c.contactFirstName,
    c.contactLastName,
    c.phone,
    c.salesRepEmployeeNumber
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName, c.contactFirstName
""", conn)

# STEP 5
# Return all customer contacts with payment date and amount
df_payment = pd.read_sql("""
SELECT 
    c.contactFirstName,
    c.contactLastName,
    p.paymentDate,
    p.amount
FROM customers AS c
JOIN payments AS p
    ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Return employees whose customers have an average credit limit over 90000
df_credit = pd.read_sql("""
SELECT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    COUNT(c.customerNumber) AS n_customers
FROM employees AS e
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY n_customers DESC
""", conn)

# STEP 7
# Return product sales totals and number of orders per product
df_product_sold = pd.read_sql("""
SELECT
    p.productName,
    COUNT(od.orderNumber) AS numorders,
    SUM(od.quantityOrdered) AS totalunits
FROM products AS p
JOIN orderdetails AS od
    ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
""", conn)

# STEP 8
# Return how many different customers purchased each product
df_total_customers = pd.read_sql("""
SELECT
    p.productName,
    p.productCode,
    COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products AS p
JOIN orderdetails AS od
    ON p.productCode = od.productCode
JOIN orders AS o
    ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Return how many customers each office has
df_customers = pd.read_sql("""
SELECT
    COUNT(c.customerNumber) AS n_customers,
    o.officeCode,
    o.city
FROM offices AS o
LEFT JOIN employees AS e
    ON o.officeCode = e.officeCode
LEFT JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY o.officeCode
""", conn)

# STEP 10
# Return employees who sold products purchased by fewer than 20 customers
df_under_20 = pd.read_sql("""
WITH low_customer_products AS (
    SELECT
        od.productCode
    FROM orderdetails AS od
    JOIN orders AS o
        ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)
SELECT DISTINCT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    ofc.city,
    ofc.officeCode
FROM employees AS e
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders AS o
    ON c.customerNumber = o.customerNumber
JOIN orderdetails AS od
    ON o.orderNumber = od.orderNumber
JOIN offices AS ofc
    ON e.officeCode = ofc.officeCode
WHERE od.productCode IN (
    SELECT productCode
    FROM low_customer_products
)
ORDER BY e.lastName, e.firstName
""", conn)

conn.close()