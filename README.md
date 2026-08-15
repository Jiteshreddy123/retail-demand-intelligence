# Retail Demand Intelligence & Forecasting System

An end-to-end retail analytics and demand forecasting system built using Python, PostgreSQL, SQL, Machine Learning, Power BI, FastAPI, and Google Gemini.

## Problem

Retail businesses need to understand historical sales patterns, identify high-performing stores and departments, and estimate future demand to support inventory and operational decisions.

## Solution

This project builds an end-to-end pipeline that:

- ingests and cleans retail sales data
- combines sales, store, and external feature datasets
- stores processed data in PostgreSQL
- performs business analytics using SQL
- predicts weekly sales using machine learning
- evaluates forecasts using time-based validation
- visualizes business performance in Power BI
- exposes business metrics through FastAPI
- generates grounded business insights using Gemini

## Architecture

```text
Walmart Retail Dataset
        ↓
Python ETL Pipeline
        ↓
Cleaned Dataset
        ↓
PostgreSQL
        ↓
SQL Business Analytics
        ↓
ML Feature Engineering
        ↓
Demand Forecasting Model
        ↓
Power BI Dashboard
        ↓
FastAPI
        ↓
Gemini Business Insights
