#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 10:51:36 2025
Author: Julia Muller

Set up Bokeh app interface for debt repayment calculator
"""

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import NumericInput, ColumnDataSource, Div, HoverTool, CrosshairTool, Span, DataTable, TableColumn, Select, Legend, LegendItem, NumberFormatter
from bokeh.plotting import figure
from simulate_debt import simulate_debt_repayment


"""
Set up widgets
"""
n_debts = NumericInput(title = 'Number of Debts (Max. 5)', value = 2, low = 1, high = 5, width = 200)

balances = [NumericInput(title = f'Debt {i+1} Balance', value = 0) for i in range(5)]
rates = [NumericInput(title = f'Debt {i+1} Interest Rate (Annual %)', value = 5, mode = 'float') for i in range(5)]
minimums = [NumericInput(title = f'Debt {i+1} Minimum Monthly Payment', value = 0) for i in range(5)]

budget = NumericInput(title = 'Planned Total Monthly Payment', value = 600)
repayment_strategy = Select(title = 'Payoff Strategy', value = 'Avalanche', options = ['Avalanche', 'Snowball'])

output = Div()


"""
Set up data sources and defaults
"""
balance_source = ColumnDataSource(data=dict(month=[]))
payment_source = ColumnDataSource(data=dict(month=[]))

balances[0].value = 10000
rates[0].value = 5.0
minimums[0].value = 250

balances[1].value = 5000
rates[1].value = 10.0
minimums[1].value = 100


"""
Set up line plot of debt balances over time
"""

balance_plot = figure(
    # title = 'Debt Balances Over Time',
    x_axis_label = 'Month', y_axis_label = 'Balance Remaining ($)',
    height = 500, width = 900,
    tools = 'pan,wheel_zoom,box_zoom,reset',
    toolbar_location = None
)

renderers = []

for i in range(5):
    line = balance_plot.line(
        'month', f'b{i+1}', 
        source = balance_source, 
        line_width = 2, 
        color = ['blue', 'green', 'red', 'orange', 'purple'][i])
    renderers.append(line)

balance_plot.add_tools(
    CrosshairTool(overlay = Span(dimension = 'height', line_dash = 'dotted', line_width = 2))
)


"""
Set up table of monthly payment allocations
"""
columns = [TableColumn(field = 'month', title = 'Month')]

for i in range(5):
    columns.append(TableColumn(
        field = f'p{i+1}', 
        title = f'Debt {i+1} Payment',
        formatter = NumberFormatter(format = '$0,0.00')))

data_table = DataTable(
    source = payment_source,
    columns = columns,
    width = 500, height = 500,
    index_position = None,
    scroll_to_selection = True
)


"""
Set up callback functions
"""
def update_plot(attr, old, new):
    
    # Generate list of dictionaries of debts based on provided input values
    debt_list = []
    for i in range(n_debts.value):
        balance_input = balances[i].value
        rate_input = rates[i].value / 100
        minimum_input = minimums[i].value
        if balance_input > 0 and minimum_input > 0:
            debt_list.append({'balance': balance_input, 'rate': rate_input, 'min_payment': minimum_input})

    # Get the budget and sum of monthly minimum payments
    budget_input = budget.value
    total_minimums = sum(debt['min_payment'] for debt in debt_list)
    
    # Return error message if no debts are inputted
    if len(debt_list) == 0:
        output.text = "<b style='color:red;'>Please enter at least one debt with balance and minimum payment.</b>"
        payment_source.data = dict(month=[])
        balance_source.data = dict(month=[])
        return

    # Return error message if the budget is less than the sum of the minimum payments
    if budget_input < total_minimums:
        output.text = "<b style='color:red;'>Budget must be at least the sum of minimum payments</b>"
        payment_source.data = dict(month=[])
        balance_source.data = dict(month=[])
        return

    # Apply the repayment simulation function with the selected repayment strategy
    if repayment_strategy.value == 'Avalanche':
        months, debt_payments, debt_balances = simulate_debt_repayment(debt_list, budget_input, 'Avalanche')
    elif repayment_strategy.value == 'Snowball':
        months, debt_payments, debt_balances = simulate_debt_repayment(debt_list, budget_input, 'Snowball')

    data = dict(month = months)
    for i in range(len(debt_list)):
        data[f'p{i+1}'] = debt_payments[i]
        data[f'b{i+1}'] = debt_balances[i]
    for i in range(len(debt_list), 5):
        data[f'p{i+1}'] = [0]*len(months)
        data[f'b{i+1}'] = [0]*len(months)

    payment_source.data = data
    balance_source.data = data

    # Calculate and print the total amount paid and time to repay debts
    total_paid = sum(sum(payments) for payments in debt_payments.values())
    output.text = (
        f"<b>Total Loan Repayment Time:</b> {len(months)//12} years, {len(months)%12} months<br>"
        f"<b>Total Amount Paid:</b> ${total_paid:,.2f}"
    )
    
    
def update_legend():
    # Remove existing legend items
    balance_plot.legend.items = []

    items = []
    n = n_debts.value
    for i in range(n):
        items.append(LegendItem(label = f'Debt {i+1}', renderers = [renderers[i]]))

    legend = Legend(items = items, location = 'top_right')
    balance_plot.add_layout(legend)


def update_visible_loans(attr, old, new):
    for i in range(5):
        visible = (i < n_debts.value)
        balances[i].visible = visible
        rates[i].visible = visible
        minimums[i].visible = visible
        debt_inputs[i].visible = visible
        renderers[i].visible = visible
        data_table.columns[i+1].visible = visible

    update_legend()
    update_hover_tool()
    update_plot(None, None, None)
    
    
def update_hover_tool():
    tools = [tool for tool in balance_plot.tools if not isinstance(tool, HoverTool)]
    balance_plot.tools = tools
    
    tooltip_fields = [('Month', '@month')]
    for i in range(n_debts.value):
        tooltip_fields.append((f'Debt {i+1} Balance', f'$@b{i+1}{{0,0.00}}'))    

    hover = HoverTool(
        tooltips = tooltip_fields,
        mode = 'vline',
        renderers = renderers[:n_debts.value]
    )

    balance_plot.add_tools(hover)

    
"""
Set up app layout
"""
debt_inputs = []

for i in range(5):
    debt_inputs.append(
        column(
            Div(text=f'<b>Debt {i+1}</b>'),
            balances[i], rates[i], minimums[i]
        )
    )

top_row = row(
    column(n_debts, width = 220),
    *debt_inputs,
    column(Div(text = '<b>Budget</b>'), budget, repayment_strategy)
)

layout = column(
    top_row,
    row(
        column(Div(text = '<b>Debt Balances Over Time</b>'), balance_plot), 
        column(Div(text = '<b>Monthly Payment Allocations</b>'), data_table)
    ),
    output
)

# Initial visibility based on default value
update_visible_loans(None, None, None)

# Attach callbacks
n_debts.on_change('value', update_visible_loans)

for widget in balances + rates + minimums + [budget, repayment_strategy]:
    widget.on_change('value', update_plot)

curdoc().add_root(layout)
curdoc().title = 'Debt Repayment Calculator'

# Initial render
update_plot(None, None, None)

