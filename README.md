# 📈 OI Tracker – NIFTY Option Chain Visualizer

OI Tracker is a web-based tool that fetches and displays real-time Open Interest (OI) data for NIFTY options. It helps traders analyze option chain data using filters and visual cues to make better trading decisions.

## 🚀 Features

- Real-time scraping of NIFTY option chain data from NSE
- Displays Open Interest (OI), Change in OI, Volume, Implied Volatility (IV), and LTP for Calls and Puts
- Strike-wise comparison of Call and Put data
- Searchable and selectable expiry dates
- User-defined filters for:
  - Minimum Open Interest
  - Minimum Implied Volatility
  - Minimum Volume
- Highlights changes in OI with up/down arrows
- Auto-refreshes every 3 minutes for the latest data
- Responsive and clean UI built with HTML/CSS/JavaScript

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Source**: `nsepython` – NSE Option Chain Scraper

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/oi-tracker.git
   cd oi-tracker
