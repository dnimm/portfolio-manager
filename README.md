# portfolio-manager

Summary of Implemented Features

Database Integration

Database Technology

SQLAlchemy ORM

MySQL backend

In-memory SQLite for testing

ORM Models Implemented

User

Portfolio

Investment

Security

Transaction

Relationships

User → Portfolio (one to many)

Portfolio → Investment (one to many)

Portfolio → Transaction (one to many)

Transaction Logging Feature

Every BUY and SELL order creates a new transaction that stores:

Transaction ID

User ID

Portfolio ID

Security ticker

Type (BUY/SELL)

Quantity

Price

Timestamp

A new “View Transactions” menu option displays these using a rich table.

Running the program

Create virtual environment in project folder

cd portfolioapp

python3 -m venv venv

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Set up MySQL Database

CREATE DATABASE portfolio_db;

Insert admin user and any test securities using SQL query if you want

INSERT INTO user (username, firstname, lastname, password, balance)

VALUES ('admin', 'Admin', 'User', 'admin123', 10000.00);

INSERT INTO security (ticker, issuer, price) VALUES
('AAPL', 'Apple Inc.', 150.00),
('MSFT', 'Microsoft Corporation', 310.00),
('GOOGL', 'Alphabet Inc.', 2800.00),
('AMZN', 'Amazon.com Inc.', 3300.00),
('TSLA', 'Tesla Inc.', 720.00),
('JPM', 'JPMorgan Chase & Co.', 160.00),
('KO', 'The Coca-Cola Company', 60.00);

Configure credentials in config.py:

database_config = {
"user": "root",
"password": "yourpassword",
"host": "localhost",
"port": "3306",
"database": "portfolio_db"
}

Run the application

python3 -m portfolioapp.main

How to Use the Application

Start the app:

python3 -m portfolioapp.main

Running Tests

Create virtual environment outside of project folder

python3 -m venv venv

source venv/bin/activate

Run all tests

pytest

Run tests with coverage

pytest --cov=.

OR

pytest --cov=portfolioapp --cov-report=term-missing

Generate coverage report

pytest --cov=. --cov-report=html

COVERAGE REPORT:

82% Coverage

<img width="2880" height="1800" alt="Screenshot 2025-11-26 at 11 14 57 AM" src="https://github.com/user-attachments/assets/a6e2cbc3-973b-4f6d-8e3a-be299ea82d1c" />
