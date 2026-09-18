# ⚽ FIFA World Cup 2026 Analytics & Prediction Dashboard

An interactive data science and visualization suite designed to analyze, simulate, and predict match outcomes for the **FIFA World Cup 2026**. 

This project combines a **Python data engine** (Monte Carlo simulations, statistical modeling, positional telemetry generation) with a **web dashboard** featuring an HTML5 pitch canvas, Chart.js visualizers, and dynamic group stage projections.

---

## 🌟 Key Features

- **🎲 10,000-Run Monte Carlo Simulation Engine**:
  - Simulates individual match fixtures and full group stages using **Poisson distribution algorithms** parameterized by official **FIFA Ratings** and home-field adjustments.
  - Predicts exact scoreline matrices, win/draw/loss probabilities, and expected goals ($xG$).

- **🎯 Tactical Pitch Telemetry**:
  - **Positional Heatmap**: Kernel Density Estimation (KDE) maps showing team activity and field dominance.
  - **Pass Vectors**: Directional progression arrows indicating passing tendencies in attacking channels.
  - **Shot Map & Expected Goals ($xG$)**: Dynamic shot plotting where bubble size corresponds to shot quality calculated via exponential distance decay $xG = e^{-0.14 \times d}$.

- **📊 Group Stage & Standings Projections**:
  - Simulates tournament schedules across 12 groups (A through L) to project final standings, goal differences, and knockout stage advancement odds.

- **⚔️ Custom Head-to-Head (H2H) Tool**:
  - Compare any two national teams side-by-side with radar charts, win probability donuts, and statistical breakdown metrics.

---

## 🛠️ Tech Stack

### Python Data Engine
- **Python 3.8+**
- **Pandas & NumPy**: Data processing and Monte Carlo vector operations.
- **Matplotlib & Seaborn**: Tactical pitch rendering and statistical visual overlays.

### Web Dashboard
- **HTML5 & Vanilla JavaScript**: Single-file web interface with Canvas pitch rendering.
- **Tailwind CSS**: Modern UI styling.
- **Chart.js**: Probability charts, goal distributions, and tactical radar plots.

---

## 📁 Repository Structure

```text
├── Football Prediction Analysis.py      # Core Python analytics & Matplotlib dashboard engine
├── index.html                           # Single-file web dashboard UI
├── world-cup-2026-team-schedules.csv   # Tournament schedule and match metadata dataset
└── README.md                            # Project documentation
```

---

## 🚀 Getting Started

### Option 1: Web Application (No Setup Required)
Simply double-click or open `index.html` in any modern web browser to launch the web app.

### Option 2: Python Data & Analysis Engine

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MuhammadAhmedSubhani/Football-Prediction-Analysis.git
   cd Football-Prediction-Analysis
   ```

2. **Install Required Packages**:
   ```bash
   pip install numpy pandas matplotlib seaborn
   ```

3. **Run the Interactive CLI Dashboard**:
   ```bash
   python "Football Prediction Analysis.py"
   ```

---

## 📐 Mathematical Model & Methodology

### 1. Match Outcome Expected Goals ($\lambda$)
Match probabilities are computed using Poisson goal distribution parameters derived from FIFA Rating differences ($\Delta R$):

$$\lambda_{\text{Team}} = \max\left(0.4, 1.4 + \frac{\Delta R}{350}\right)$$

$$\lambda_{\text{Opponent}} = \max\left(0.4, 1.2 - \frac{\Delta R}{350}\right)$$

### 2. Expected Goals ($xG$) Formula
Shot probability is modeled based on Euclidean distance $d$ (in yards) from the goal center $(120, 40)$:

$$xG = e^{-0.14 \times d}$$

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).