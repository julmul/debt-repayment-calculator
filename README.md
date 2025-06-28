# Debt Repayment Calculator

This interactive web app helps you simulate and visualize debt repayment strategies using [Bokeh](https://bokeh.org/).

You can enter multiple debts, set interest rates, minimum payments, and your monthly budget. The app shows how your debts will be paid off over time with either the Avalanche or Snowball payoff strategy.

---

## Features

- Supports up to 5 debts simultaneously  
- Compare Avalanche vs. Snowball payoff methods  
- Visualize debt balances over time in an interactive line plot  
- View monthly payment allocations in a dynamic table  
- Customizable inputs for balances, interest rates, minimum payments, and total monthly budget  

---

## Installation & Setup

1. Clone the repository:

```bash
   git clone https://github.com/julmul/debt-repayment-calculator.git
   cd debt-repayment-calculator
```

2. Ensure you have [Docker](https://www.docker.com/get-started) installed.

3. Run the following bash script to build the Docker image and run the container:

```bash
   ./start.sh
```

4. Open a web browser and go to `http://localhost:5006/main`.