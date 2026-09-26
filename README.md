# 📊 Sales & Customer Analytics Dashboard

An interactive Business Intelligence dashboard built with **Python, Pandas, Plotly, and Streamlit** to analyze sales performance, profitability, customer behavior, RFM segmentation, discounts, and delivery performance.

## 🚀 Live Dashboard

Run the dashboard locally using:

```bash
python -m streamlit run dashboard/app.py

🎯 Project Objective

The goal of this project is to transform raw sales data into meaningful business insights.

The dashboard helps analyze:

Sales performance
Profitability
Customer behavior
Customer segmentation
RFM analysis
Discount and profit relationships
Product and category performance
Delivery performance
Loss-making customers
🛠️ Technologies Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Plotly
Streamlit
Jupyter Notebook
Git & GitHub

📂 Project Structure

sales-customer-analytics/
│
├── data/
│   ├── superstore.csv
│   └── processed/
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│
├── src/
│   └── data_analysis.py
│
└── README.md

🧹 Data Cleaning

The raw dataset contains 51,290 records.

Data preparation included:

Converting date columns into datetime format
Converting sales values into numeric format
Checking duplicate records
Checking missing values
Checking negative and zero sales
Creating delivery-day calculations
Creating profit-margin metrics
Excluding records with missing or zero sales from sales-based analysis

After cleaning, 48,659 records were used for sales-based analysis.

📊 Dashboard Features
KPI Analysis

The dashboard displays:

Total Sales
Total Profit
Total Customers
Total Orders
Profit Margin
📈 Sales Analysis
Monthly sales trends
Sales by category
Sales performance by customer segment
Top customers by sales
💰 Profitability Analysis
Profitability by category
Profitability by sub-category
Loss-making customers
Discount vs profit analysis
👥 Customer Analytics

The project uses RFM Analysis:

Recency — how recently a customer purchased
Frequency — how frequently a customer purchased
Monetary — how much the customer spent

Customers are segmented into:

High Value
Loyal Customers
Potential Customers
At Risk
Needs Attention
🚚 Delivery Analysis

The dashboard analyzes average delivery time across different shipping modes.

🔍 Business Insights

The dashboard can help identify:

High-value customers
Customers at risk of becoming inactive
Loss-making customers
High-performing categories
Profitable and unprofitable sub-categories
Relationships between discounts and profitability
Differences in delivery performance
🎛️ Interactive Filters

Users can filter the dashboard by:

Product Category
Customer Segment

The charts and KPIs dynamically update based on the selected filters.

📦 Dataset

The dataset contains sales transaction information including:

Order details
Customer information
Product information
Sales
Quantity
Discount
Profit
Shipping cost
Shipping mode
Region
Category
Sub-category
Order dates

▶️ How to Run
1. Clone the repository
git clone https://github.com/laiba2607/sales-customer-analytics.git
2. Open the project
cd sales-customer-analytics

3. Install dependencies
pip install pandas numpy matplotlib seaborn plotly streamlit openpyxl
4. Run the dashboard
python -m streamlit run dashboard/app.py

The dashboard will open in your browser.

## 👩‍💻 Author

**Laiba Mudassir**

BS Computer Science | AI & Data Science Enthusiast

GitHub: `laiba2607`

---


⭐ If you find this project useful, consider giving the repository a star

### Built with Python, Pandas & Streamlit

**© 2026 Laiba Mudassir**