# Portfolio Manager 
Doyel Nimmagadda

A command-line portfolio management application built with Python and Rich library for enhanced user interface.

## 🚀 Features

- **User Authentication**: Login/Logout with role-based access control
- **User Management**: Admin can view, add, and delete users (admin-only feature)
- **Portfolio Management**: Create, view, and delete investment portfolios
- **Investment Operations**: Buy securities and harvest (liquidate) investments
- **Marketplace**: Browse available securities and place buy orders
- **Portfolio Analytics**: View performance metrics and sector breakdown
- **Transaction History**: Track all buy/sell transactions
- **Error Handling**: Comprehensive exception handling with meaningful error messages



## 🔧 Installation & Setup
**Clone the repository**:
   ```bash
# 1. Clone repository
git clone https://github.com/dnimm/portfolio-manager.git
cd portfolioapp

# 2. Checkout assignment branch
git checkout assignment-1

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Run the application
python3 -m main

   For admin access:
   username: admin
   password: admin123
