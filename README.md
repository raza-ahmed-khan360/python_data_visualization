# Sales Dashboard

## Overview
The Sales Dashboard is a Streamlit application that provides an interactive visualization of sales data from a supermarket. It allows users to filter data based on city, customer type, and gender, and displays key performance indicators (KPIs) and various charts to analyze sales trends.

## Features
- **Data Loading**: Loads sales data from an Excel file.
- **Interactive Filters**: Users can filter data by city, customer type, and gender.
- **Key Performance Indicators**: Displays total sales, average rating, and average sales per transaction.
- **Visualizations**: 
  - Sales by product line (Bar Chart)
  - Sales by hour (Bar Chart)

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly Express
- OpenPyXL (for reading Excel files)

## Installation
To run this project, you need to have Python installed on your machine. Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sales-dashboard.git
   cd sales-dashboard
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your `supermarkt_sales.xlsx` file in the project directory.

## Usage
To run the application, execute the following command in your terminal:
