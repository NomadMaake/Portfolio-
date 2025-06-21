import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
    }
    
    .stDateInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
def init_db():
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  amount REAL NOT NULL,
                  description TEXT NOT NULL,
                  category TEXT NOT NULL,
                  transaction_type TEXT NOT NULL,
                  date TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  month TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('finance_tracker.db')

# Initialize database
init_db()

# Sidebar navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <h2>💰 Finance Tracker</h2>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Add Transaction", "View Transactions", "Budgets", "Reports"]
)

# Dashboard page
if page == "Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Financial Dashboard</h1>
        <p>Track your income, expenses, and financial goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get data
    conn = get_connection()
    transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
    budgets_df = pd.read_sql_query("SELECT * FROM budgets", conn)
    conn.close()
    
    if not transactions_df.empty:
        # Calculate metrics
        total_income = transactions_df[transactions_df['transaction_type'] == 'income']['amount'].sum()
        total_expenses = transactions_df[transactions_df['transaction_type'] == 'expense']['amount'].sum()
        net_income = total_income - total_expenses
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #4CAF50;">R{total_income:,.2f}</div>
                <div class="metric-label">Total Income</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #f44336;">R{total_expenses:,.2f}</div>
                <div class="metric-label">Total Expenses</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            color = "#4CAF50" if net_income >= 0 else "#f44336"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">R{net_income:,.2f}</div>
                <div class="metric-label">Net Income</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts Section 1
        st.subheader("📊 Spending Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📈 Spending by Category (Pie Chart)**")
            if not transactions_df[transactions_df['transaction_type'] == 'expense'].empty:
                expense_by_category = transactions_df[transactions_df['transaction_type'] == 'expense'].groupby('category')['amount'].sum()
                fig_pie = px.pie(values=expense_by_category.values, names=expense_by_category.index, 
                               title="Expense Distribution by Category")
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expense data available")
        
        with col2:
            st.write("**📊 Spending by Category (Bar Chart)**")
            if not transactions_df[transactions_df['transaction_type'] == 'expense'].empty:
                expense_by_category = transactions_df[transactions_df['transaction_type'] == 'expense'].groupby('category')['amount'].sum().sort_values(ascending=True)
                fig_bar = px.bar(x=expense_by_category.values, y=expense_by_category.index, 
                               orientation='h', title="Expense by Category (Bar Chart)")
                fig_bar.update_layout(xaxis_title="Amount (R)", yaxis_title="Category")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No expense data available")
        
        # Charts Section 2
        st.subheader("📈 Income vs Expenses Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📊 Monthly Trends**")
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])
            transactions_df['month'] = transactions_df['date'].dt.to_period('M')
            monthly_data = transactions_df.groupby(['month', 'transaction_type'])['amount'].sum().reset_index()
            
            if not monthly_data.empty:
                fig_monthly = px.bar(monthly_data, x='month', y='amount', color='transaction_type',
                                   title="Monthly Income vs Expenses", barmode='group')
                fig_monthly.update_layout(yaxis_title="Amount (R)")
                st.plotly_chart(fig_monthly, use_container_width=True)
            else:
                st.info("No monthly data available")
        
        with col2:
            st.write("**📈 Daily Spending Trend**")
            daily_spending = transactions_df[transactions_df['transaction_type'] == 'expense'].groupby('date')['amount'].sum()
            if not daily_spending.empty:
                fig_daily = px.line(daily_spending, title="Daily Expenses Trend")
                fig_daily.update_layout(yaxis_title="Amount (R)", xaxis_title="Date")
                st.plotly_chart(fig_daily, use_container_width=True)
            else:
                st.info("No daily expense data available")
        
        # Recent transactions
        st.subheader("🕒 Recent Transactions")
        recent_transactions = transactions_df.sort_values('date', ascending=False).head(10)
        st.dataframe(recent_transactions[['date', 'description', 'category', 'transaction_type', 'amount']], 
                    use_container_width=True)
    
    else:
        st.info("No transactions found. Add your first transaction to get started!")

# Add Transaction page
elif page == "Add Transaction":
    st.markdown("""
    <div class="main-header">
        <h1>➕ Add New Transaction</h1>
        <p>Record your income or expenses</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_transaction"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (R)", min_value=0.01, step=0.01)
            transaction_type = st.selectbox("Type", ["expense", "income"])
        
        with col2:
            date = st.date_input("Date", value=datetime.now())
            category = st.selectbox("Category", [
                "Food & Dining", "Transportation", "Housing", "Utilities", 
                "Healthcare", "Entertainment", "Shopping", "Education", 
                "Insurance", "Salary", "Freelance", "Investment", "Business", 
                "Other Income", "Other Expenses"
            ])
        
        description = st.text_input("Description", placeholder="e.g., Grocery shopping, Salary payment")
        
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted and amount and description:
            conn = get_connection()
            c = conn.cursor()
            c.execute("""
                INSERT INTO transactions (amount, description, category, transaction_type, date)
                VALUES (?, ?, ?, ?, ?)
            """, (amount, description, category, transaction_type, date.strftime('%Y-%m-%d')))
            conn.commit()
            conn.close()
            st.success("Transaction added successfully!")

# View Transactions page
elif page == "View Transactions":
    st.markdown("""
    <div class="main-header">
        <h1>📋 All Transactions</h1>
        <p>View and manage your transaction history</p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = get_connection()
    transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    
    if not transactions_df.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transaction_type_filter = st.selectbox("Filter by Type", ["All", "income", "expense"])
        
        with col2:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(transactions_df['category'].unique()))
        
        with col3:
            date_range = st.date_input("Date Range", value=(datetime.now() - timedelta(days=30), datetime.now()))
        
        # Apply filters
        filtered_df = transactions_df.copy()
        
        if transaction_type_filter != "All":
            filtered_df = filtered_df[filtered_df['transaction_type'] == transaction_type_filter]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df['date'] = pd.to_datetime(filtered_df['date'])
            filtered_df = filtered_df[(filtered_df['date'].dt.date >= start_date) & 
                                    (filtered_df['date'].dt.date <= end_date)]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Summary
        if not filtered_df.empty:
            st.subheader("📊 Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Transactions", len(filtered_df))
            
            with col2:
                total_amount = filtered_df['amount'].sum()
                st.metric("Total Amount", f"R{total_amount:,.2f}")
            
            with col3:
                avg_amount = filtered_df['amount'].mean()
                st.metric("Average Amount", f"R{avg_amount:,.2f}")
    
    else:
        st.info("No transactions found. Add some transactions to see them here!")

# Budgets page
elif page == "Budgets":
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Budget Management</h1>
        <p>Set and track your spending limits</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Budgets")
        conn = get_connection()
        budgets_df = pd.read_sql_query("SELECT * FROM budgets", conn)
        transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
        conn.close()
        
        if not budgets_df.empty:
            # Calculate budget vs actual
            budget_vs_actual = []
            for _, budget in budgets_df.iterrows():
                category_expenses = transactions_df[
                    (transactions_df['category'] == budget['category']) & 
                    (transactions_df['transaction_type'] == 'expense')
                ]['amount'].sum()
                
                percentage_used = (category_expenses / budget['amount']) * 100 if budget['amount'] > 0 else 0
                
                budget_vs_actual.append({
                    'Category': budget['category'],
                    'Budget': budget['amount'],
                    'Spent': category_expenses,
                    'Remaining': budget['amount'] - category_expenses,
                    'Percentage Used': percentage_used
                })
            
            budget_df = pd.DataFrame(budget_vs_actual)
            
            # Display budget progress
            for _, row in budget_df.iterrows():
                st.write(f"**{row['Category']}**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Budget", f"R{row['Budget']:,.2f}")
                
                with col2:
                    st.metric("Spent", f"R{row['Spent']:,.2f}")
                
                with col3:
                    st.metric("Remaining", f"R{row['Remaining']:,.2f}")
                
                # Progress bar
                progress_color = "green" if row['Percentage Used'] <= 80 else "orange" if row['Percentage Used'] <= 100 else "red"
                st.progress(row['Percentage Used'] / 100)
                st.write(f"{row['Percentage Used']:.1f}% used")
                st.divider()
        
        else:
            st.info("No budgets set. Add budgets to start tracking!")
    
    with col2:
        st.subheader("Add Budget")
        with st.form("add_budget"):
            category = st.selectbox("Category", [
                "Food & Dining", "Transportation", "Housing", "Utilities", 
                "Healthcare", "Entertainment", "Shopping", "Education", "Insurance"
            ])
            amount = st.number_input("Monthly Budget (R)", min_value=0.01, step=0.01)
            month = st.date_input("Month", value=datetime.now()).strftime('%Y-%m')
            
            submitted = st.form_submit_button("Add Budget")
            
            if submitted and amount:
                conn = get_connection()
                c = conn.cursor()
                c.execute("""
                    INSERT OR REPLACE INTO budgets (category, amount, month)
                    VALUES (?, ?, ?)
                """, (category, amount, month))
                conn.commit()
                conn.close()
                st.success("Budget added successfully!")

# Reports page
elif page == "Reports":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Financial Reports</h1>
        <p>Detailed analysis of your financial data</p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = get_connection()
    transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    
    if not transactions_df.empty:
        # Convert date column
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        
        # Time period selector
        period = st.selectbox("Select Time Period", ["Last 30 days", "Last 3 months", "Last 6 months", "Last year", "All time"])
        
        # Filter data based on period
        if period == "Last 30 days":
            filtered_df = transactions_df[transactions_df['date'] >= datetime.now() - timedelta(days=30)]
        elif period == "Last 3 months":
            filtered_df = transactions_df[transactions_df['date'] >= datetime.now() - timedelta(days=90)]
        elif period == "Last 6 months":
            filtered_df = transactions_df[transactions_df['date'] >= datetime.now() - timedelta(days=180)]
        elif period == "Last year":
            filtered_df = transactions_df[transactions_df['date'] >= datetime.now() - timedelta(days=365)]
        else:
            filtered_df = transactions_df
        
        if not filtered_df.empty:
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_income = filtered_df[filtered_df['transaction_type'] == 'income']['amount'].sum()
                st.metric("Total Income", f"R{total_income:,.2f}")
            
            with col2:
                total_expenses = filtered_df[filtered_df['transaction_type'] == 'expense']['amount'].sum()
                st.metric("Total Expenses", f"R{total_expenses:,.2f}")
            
            with col3:
                net_income = total_income - total_expenses
                st.metric("Net Income", f"R{net_income:,.2f}")
            
            with col4:
                transaction_count = len(filtered_df)
                st.metric("Transactions", transaction_count)
            
            # Charts Section 1
            st.subheader("📊 Spending Visualizations")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📈 Spending by Category (Pie Chart)**")
                expense_df = filtered_df[filtered_df['transaction_type'] == 'expense']
                if not expense_df.empty:
                    category_spending = expense_df.groupby('category')['amount'].sum()
                    fig_pie = px.pie(values=category_spending.values, names=category_spending.index, 
                                   title="Expense Distribution")
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No expense data for selected period")
            
            with col2:
                st.write("**📊 Top Spending Categories (Bar Chart)**")
                expense_df = filtered_df[filtered_df['transaction_type'] == 'expense']
                if not expense_df.empty:
                    category_spending = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
                    fig_bar = px.bar(x=category_spending.values, y=category_spending.index, 
                                   orientation='h', title="Top Spending Categories")
                    fig_bar.update_layout(xaxis_title="Amount (R)", yaxis_title="Category")
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No expense data for selected period")
            
            # Charts Section 2
            st.subheader("📈 Trend Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📊 Monthly Income vs Expenses**")
                monthly_data = filtered_df.groupby(['date', 'transaction_type'])['amount'].sum().reset_index()
                monthly_data['month'] = monthly_data['date'].dt.to_period('M')
                monthly_summary = monthly_data.groupby(['month', 'transaction_type'])['amount'].sum().reset_index()
                
                if not monthly_summary.empty:
                    fig_monthly = px.bar(monthly_summary, x='month', y='amount', color='transaction_type',
                                       title="Monthly Income vs Expenses", barmode='group')
                    fig_monthly.update_layout(yaxis_title="Amount (R)")
                    st.plotly_chart(fig_monthly, use_container_width=True)
                else:
                    st.info("No monthly data available")
            
            with col2:
                st.write("**📈 Daily Spending Trend**")
                daily_spending = filtered_df[filtered_df['transaction_type'] == 'expense'].groupby('date')['amount'].sum()
                if not daily_spending.empty:
                    fig_daily = px.line(daily_spending, title="Daily Expenses Trend")
                    fig_daily.update_layout(yaxis_title="Amount (R)", xaxis_title="Date")
                    st.plotly_chart(fig_daily, use_container_width=True)
                else:
                    st.info("No daily expense data available")
            
            # Detailed breakdown
            st.subheader("📋 Detailed Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Income by Category**")
                income_by_category = filtered_df[filtered_df['transaction_type'] == 'income'].groupby('category')['amount'].sum()
                if not income_by_category.empty:
                    st.dataframe(income_by_category, use_container_width=True)
                else:
                    st.info("No income data for selected period")
            
            with col2:
                st.write("**Expenses by Category**")
                expense_by_category = filtered_df[filtered_df['transaction_type'] == 'expense'].groupby('category')['amount'].sum()
                if not expense_by_category.empty:
                    st.dataframe(expense_by_category, use_container_width=True)
                else:
                    st.info("No expense data for selected period")
        
        else:
            st.info(f"No data available for {period}")
    
    else:
        st.info("No transactions found. Add some transactions to generate reports!") 