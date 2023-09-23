# Stock Analysis Project

## Table of Contents

- [Stock Analysis Project](#stock-analysis-project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [ETL Pipeline](#etl-pipeline)
  - [PostgreSQL Database](#postgresql-database)
  - [Django Web Application](#django-web-application)
  - [JavaScript Sorting Functionality](#javascript-sorting-functionality)
  - [Installation and Setup](#installation-and-setup)
  - [Usage](#usage)
  - [License](#license)

## Introduction

This project aims to provide an in-depth analysis of stock data. It comprises an ETL (Extract, Transform, Load) pipeline, a PostgreSQL database, a Django web application, and client-side JavaScript functionalities.

## ETL Pipeline

The ETL pipeline is responsible for sourcing stock data, transforming it for analysis, and loading it into a PostgreSQL database. The pipeline is built using Python and utilizes various data manipulation libraries.

## PostgreSQL Database

The PostgreSQL database stores the stock data ingested by the ETL pipeline. It is optimized for performance and is accessed using Django's ORM (Object-Relational Mapping) functionalities.

## Django Web Application

The Django web application serves as the frontend for this project. It queries the PostgreSQL database to retrieve stock data and renders it using HTML templates. 

## JavaScript Sorting Functionality

The frontend includes JavaScript code that allows users to sort tables based on different attributes. The sorting logic is both numerical and alphabetical, based on the column type.

## Installation and Setup

Detailed instructions for setting up the project are included in the `requirements.txt` file for Python dependencies and a separate README file within the Django web application directory.

## Usage

After installation, run the ETL pipeline to populate the PostgreSQL database. Then, launch the Django web application to start interacting with the stock data.


## License

MIT License