from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import calendar
from datetime import datetime
from flask_session import Session
import openai

app = Flask(__name__)

app.config['SECRET_KEY'] = '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' #replace this with your key
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

budget_data = {
    'January': 0,
    'February': 0,
    'March': 0,
    'April': 0,
    'May': 0,
    'June': 0,
    'July': 0,
    'August': 0,
    'September': 0,
    'October': 0,
    'November': 0,
    'December': 0,
}
expense_log = []
income_log = []
total_income = 0

openai.api_key = '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'


# get a chat AI response
def get_chat_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"You: {user_input}\nChatGPT: ",
        max_tokens=510
    )
    chat_response = response.choices[0].text.strip()
    return chat_response

@app.route('/get-chat-response', methods=['POST'])
def get_chat_response_route():
    user_input = request.form.get('user-input')
    chat_response = get_chat_response(user_input) 
    return jsonify({'chat_response': chat_response})

# parse budget suggestions into a dictionary
def parse_budget_suggestions(budget_suggestions):
    budget_data = {}
    suggestions = budget_suggestions.split(', ')

    for suggestion in suggestions:
        category, percentage = suggestion.split(': ')
        budget_data[category] = float(percentage.replace('%', ''))

    return budget_data


# calculate the remaining budget (based on the initial budget and expenses)
def calculate_remaining_budget():
    initial_budget = session.get('budget', 0)
    total_expenses = sum(expense['amount'] for expense in expense_log)
    remaining_budget = initial_budget - total_expenses

    return remaining_budget

# get budget suggestions from OpenAI GPT-3
def get_budget_suggestions(expense_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"You: {expense_text}\nChatGPT: ",
            max_tokens=100,  # Adjust as needed
        )
        budget_suggestions = response.choices[0].text.strip()
        return budget_suggestions
    except Exception as e:
        return str(e)

@app.route('/expenses/get-suggestions', methods=['POST'])
def get_expense_suggestions():
    expense_text = request.form.get('user-input')
    budget_suggestions = get_budget_suggestions(expense_text)
    return render_template('suggestions.html', user_input=expense_text, suggestions=budget_suggestions)

# get budget suggestions from OpenAI GPT-3
def get_openai_budget_suggestions(expense_log):
    try:
        prompt = "You: Generate budget suggestions based on the input:\n"
        for expense in expense_log:
            date = expense['date']
            amount = expense['amount']
            prompt += f"- Date: {date}, Amount: {amount}\n"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100, 
            stop=None,
        )

        suggestion = response.choices[0].text.strip()
        return suggestion
    except Exception as e:
        # Handle any exceptions that may occur during the API call
        return str(e)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        initial_budget_str = request.form.get('initial-budget')
        if initial_budget_str is not None:
            try:
                initial_budget = float(initial_budget_str)
                session['budget'] = initial_budget
                budget_data['initial'] = initial_budget

                return redirect(url_for('expenses'))
            except ValueError:
                return "Invalid budget value. Please enter a valid number for the budget."

    now = datetime.now()
    num_days = calendar.monthrange(now.year, now.month)[1]
    x_labels = list(range(1, num_days + 1))
    initial_budget = calculate_remaining_budget()

    return render_template(
        'index.html',
        budget=initial_budget,
        initial_budget=initial_budget,
        x_labels=x_labels,
    )


@app.route('/get-remaining-budget', methods=['GET'])
def get_remaining_budget():
    remaining_budget = calculate_remaining_budget()
    return jsonify({'remaining_budget': remaining_budget})


@app.route('/budget-generator', methods=['GET', 'POST'])
def budget_generator():
    budget_param = request.args.get('budget')

    try:
        budget = float(budget_param) if budget_param is not None else 0
        session['budget'] = budget
    except ValueError:
        return "Invalid budget value. Please enter a valid number for the budget."

    if request.method == 'POST':
        user_input = request.form.get('user-input')
        updated_budget_data = generate_updated_budget(user_input, budget)
        return jsonify(budget_data=updated_budget_data)

    budget_data = {
        "Food": 30,
        "Housing": 20,
        "Transportation": 10,
        "Entertainment": 10,
        "Savings": 10,
        "Other": 20,
    }

    return render_template('budget_generator.html', budget=budget, budget_data=budget_data)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    budget = float(request.args.get('budget')) if 'budget' in request.args else session.get('budget', 0)
    selected_month = request.form.get('selected_month', 'January')
    budget_for_selected_month = budget_data.get(selected_month, 0)
    initial_budget = budget
    budget_suggestions_data = {} 

    if request.method == 'POST':
        user_input = request.form.get('user-input')
        budget_suggestions = get_openai_budget_suggestions(expense_log)

        budget_suggestions_data = {
            'user_input': user_input,
            'suggestions': budget_suggestions,
        }

        expense_amount = float(request.form.get('expense-amount', 0))
        expense_date = request.form.get('expense-date')
        expense_reason = request.form.get('expense-reason')

        if expense_amount > 0:
            initial_budget -= expense_amount
            session['budget'] = initial_budget

            entry = {
                'date': datetime.strptime(expense_date, "%Y-%m-%d").strftime("%m/%d/%Y"),
                'reason': expense_reason,
                'amount': expense_amount,
                'month': selected_month
            }

            expense_log.append(entry)
            expense_log.sort(key=lambda x: x['date'], reverse=True)

    chart_data = {
        'initial_budget': initial_budget,
        'expenses': expense_log
    }

    return render_template(
        'expenses.html',
        initial_budget=initial_budget,
        expense_log=expense_log,
        budget_suggestions_data=budget_suggestions_data,
        chart_data=chart_data,
        expenses=expense_log,
    )


@app.route('/expenses/clear', methods=['POST'])
def clear_expenses():
    global expense_log
    expense_log = []
    return redirect('/expenses')


@app.route('/income', methods=['GET', 'POST'])
def income():
    global total_income

    if request.method == 'POST':
        income_source = request.form.get('income-source')
        income_amount = float(request.form.get('income-amount', 0))
        income_date = request.form.get('income-date')

        if income_amount >= 0:
            income_log.append({
                'source': income_source,
                'amount': income_amount,
                'date': income_date
            })

            total_income += income_amount
            income_log.sort(key=lambda x: x['date'], reverse=True)

    return render_template('income.html', total_income=total_income, income_log=income_log)


if __name__ == '__main__':
    app.run(debug=True)
