# Import libraries
from flask import Flask, request
from flask import url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date": "2025-07-01", "amount": 100.0},
    {"id": 2, "date": "2025-07-02", "amount": -200.0},
    {"id": 3, "date": "2025-07-03", "amount": 300.0}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

#Total Balance operation
@app.route('/total_balance')
def total_balance():
    total = sum(t['amount'] for t in transactions)
    return render_template('transactions.html', transactions=transactions, total=total)

# Create operation
@app.route('/add', methods=['POST','GET'])
def add_transaction():
    if request.method == 'POST':
        new_id = len(transactions) + 1
        new_date = request.form['date']
        new_amount = float(request.form['amount'])
        transactions.append({"id": new_id, "date": new_date, "amount": new_amount})
        return redirect(url_for('get_transactions'))
    return render_template('form.html')

# Update operation
@app.route('/edit/<int:transaction_id>')
def edit_transaction(transaction_id):
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    if transaction is None:
        return {"message" : "Transaction not found"}, 404
    if request.method == 'POST':
        transaction['date'] = request.form['date']
        transaction['amount'] = float(request.form['amount'])
        return redirect(url_for('get_transactions'))
    return render_template('edit.html', transaction=transaction)

# Delete operation
@app.route('/delete/<int:transaction_id>', methods=['POST', 'GET'])
def delete_transaction(transaction_id):
    transaction = [t for t in transactions if t['id'] == transaction_id]
    transactions.remove(transaction[0])
    return redirect(url_for('get_transactions'))


#Search operation based on min and max transaction amount
@app.route('/search', methods=['GET','POST'])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        filtered_transactions = [t for t in transactions if min_amount <= t['amount'] <= max_amount]
        return render_template('transactions.html', transactions=filtered_transactions)
    return render_template('search.html')




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)