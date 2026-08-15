-- Retail Demand Intelligence & Forecasting System
-- SQL Business Analytics


-- total sales
SELECT
    ROUND(SUM("Weekly_Sales")::numeric, 2) AS total_sales
FROM sales_fact;

--sales by year
SELECT
    "Year",
    ROUND(SUM("Weekly_Sales")::numeric, 2) AS total_sales
FROM sales_fact
GROUP BY "Year"
ORDER BY "Year";

--sales by month
SELECT
    "Month",
    ROUND(SUM("Weekly_Sales")::numeric, 2) AS total_sales
FROM sales_fact
GROUP BY "Month"
ORDER BY "Month";

--top 10 departments
SELECT
    "Dept",
    ROUND(SUM("Weekly_Sales")::numeric, 2) AS total_sales
FROM sales_fact
GROUP BY "Dept"
ORDER BY total_sales DESC
LIMIT 10;

--top 10 stores
SELECT
    "Store",
    ROUND(SUM("Weekly_Sales")::numeric, 2) AS total_sales
FROM sales_fact
GROUP BY "Store"
ORDER BY total_sales DESC
LIMIT 10;

--holiday and non holiday sales
SELECT
    "IsHoliday",
    ROUND(AVG("Weekly_Sales")::numeric, 2) AS avg_weekly_sales
FROM sales_fact
GROUP BY "IsHoliday"
ORDER BY "IsHoliday";