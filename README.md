# 💰 Personal Finance Tracker

A modern, interactive Personal Finance Tracker built with **Streamlit** that helps you manage your income, expenses, budgets, and financial goals with beautiful visualizations and real-time insights.

![Finance Tracker](https://img.shields.io/badge/Streamlit-1.46.0-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

### 📊 **Interactive Dashboard**
- Real-time financial metrics (Income, Expenses, Net Income)
- Beautiful gradient cards with glass morphism effects
- Multiple chart types: Pie charts, Bar charts, Line charts
- Recent transactions overview

### 💳 **Transaction Management**
- Add income and expenses with categories
- Filter transactions by type, category, and date range
- Transaction history with detailed breakdowns
- Currency support in South African Rands (ZAR)

### 🎯 **Budget Tracking**
- Set monthly budgets by category
- Visual progress bars with color-coded alerts
- Budget vs actual spending comparison
- Overspending notifications

### 📈 **Advanced Reports**
- Customizable time periods (30 days, 3 months, 6 months, 1 year, all time)
- Multiple visualization types for spending analysis
- Income vs expenses trends
- Category-wise breakdowns

### 🎨 **Modern UI/UX**
- Responsive design that works on all devices
- Beautiful gradients and animations
- Interactive charts with Plotly
- Professional color scheme

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📱 Usage Guide

### Getting Started
1. **Add Your First Transaction**
   - Go to "Add Transaction" in the sidebar
   - Enter amount in Rands (R)
   - Select transaction type (income/expense)
   - Choose a category
   - Add description and date

2. **Set Up Budgets**
   - Navigate to "Budgets" page
   - Set monthly limits for different categories
   - Monitor spending against budgets

3. **View Reports**
   - Check "Reports" for detailed analysis
   - Select different time periods
   - Explore various chart visualizations

### Features Overview

#### 📊 Dashboard
- **Key Metrics**: Total income, expenses, and net income
- **Spending Analysis**: Pie and bar charts showing category distribution
- **Trends**: Monthly and daily spending patterns
- **Recent Activity**: Latest transactions

#### 💳 Transactions
- **Add New**: Quick form for recording transactions
- **View All**: Filterable transaction history
- **Categories**: Pre-defined categories for easy organization
- **Search & Filter**: Find specific transactions easily

#### 🎯 Budgets
- **Set Limits**: Monthly budgets by category
- **Track Progress**: Visual progress bars
- **Alerts**: Color-coded overspending warnings
- **Comparison**: Budget vs actual spending

#### 📈 Reports
- **Time Periods**: Flexible date ranges
- **Visualizations**: Multiple chart types
- **Trends**: Income vs expenses over time
- **Breakdowns**: Detailed category analysis

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas
- **Database**: SQLite
- **Styling**: Custom CSS with modern design

## 📁 Project Structure

```
personal-finance-tracker/
├── streamlit_app.py          # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .gitignore              # Git ignore rules
├── env.example             # Environment variables example
└── finance_tracker.db      # SQLite database (auto-generated)
```

## 🎨 Customization

### Adding New Categories
Edit the category lists in `streamlit_app.py`:
```python
category = st.selectbox("Category", [
    "Food & Dining", "Transportation", "Housing", "Utilities", 
    "Healthcare", "Entertainment", "Shopping", "Education", 
    "Insurance", "Salary", "Freelance", "Investment", "Business", 
    "Other Income", "Other Expenses"
])
```

### Changing Currency
The app is configured for South African Rands (ZAR). To change currency, update the currency symbol in the code:
```python
# Replace 'R' with your preferred currency symbol
f"R{amount:,.2f}"
```

### Custom Styling
Modify the CSS in the `st.markdown()` section to customize the appearance.

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `env.example`:
```bash
# Copy the example file
cp env.example .env

# Edit with your settings
nano .env
```

## 📊 Data Export

The application stores all data in a local SQLite database (`finance_tracker.db`). You can:
- Export data using SQL queries
- Backup the database file
- Import data from CSV files (future feature)

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud Deployment
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Other Platforms
- **Heroku**: Use the provided `requirements.txt`
- **Docker**: Create a Dockerfile for containerization
- **VPS**: Deploy on any server with Python support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing web app framework
- **Plotly** for interactive visualizations
- **Pandas** for data manipulation
- **SQLite** for lightweight database storage

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/personal-finance-tracker/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🔮 Future Features

- [ ] Data export to CSV/PDF
- [ ] Multiple currency support
- [ ] Recurring transactions
- [ ] Financial goals tracking
- [ ] Investment portfolio tracking
- [ ] Mobile app version
- [ ] Cloud synchronization
- [ ] Advanced analytics and predictions

---

**Made with ❤️ using Streamlit**

*Track your finances, achieve your goals!* 