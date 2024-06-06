# College Budget App

A comprehensive college budget application that tracks expenses, income, and budget while providing AI-driven suggestions.

## Overview

The College Budget App leverages OpenAI to assist users in managing their finances. The AI is integrated into the app in two primary ways:
1. **AI Financial Advisor**: Available on the home page for real-time financial advice and assistance.
2. **Expense Suggestions**: Provides tailored advice based on recent expense data.

## Features

### Home Page (index.html)
- **Initial Budget Entry**: Users can input their initial budget, which is then used across other pages.
- **Live Chat Feature**: An AI Financial Advisor powered by Chat GPT to answer user queries and concerns.
- **Navigation Buttons**: Direct links to other pages of the app.

### Budget Generator (budget_generator.html)
- **Sample Budget Creation**: Automatically divides the initial budget into categories such as housing, entertainment, and food.
- **Graphical Display**: Visual representation of budget allocation using a pie chart.

### Expenses (expenses.html)
- **Expense Logging**: Users can record expenses by entering the date, reason, and amount, which are saved in an expense table.
- **Clear Log Feature**: Option to clear the expense log and reset the initial budget.
- **Expense Visualization**: Plots expense entries on a graph to visualize spending patterns.
- **AI Suggestions**: Users can get AI-driven suggestions and advice based on their logged expenses.

### Suggestions (suggestions.html)
- **Redirect for Advice**: Users are redirected here for tailored suggestions based on their expense data.

### Income (income.html)
- **Income Entry**: Space for users to log their income sources, such as scholarships and paychecks.

## Styling
- **General Style Guidelines**: Background, button colors, and fonts are defined in `styles.css`.

## Setup Instructions

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shjangada/CollegeBudgetApp.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd CollegeBudgetApp
   ```
3. **Install dependencies**:
   ```bash
   npm install
   ```
4. **Run the development server**:
   ```bash
   npm start
   ```

## Usage

1. **Start on the Home Page**: Enter your initial budget.
2. **Generate a Budget**: Navigate to the budget generator to see your budget divided into categories.
3. **Log Expenses**: Go to the expenses page to log your spending and visualize it on a graph.
4. **Get Suggestions**: Use the AI feature on the expenses page for tailored advice.
5. **Enter Income**: Record your income on the income page.
