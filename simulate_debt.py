#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 12:54:24 2025
Author: Julia Muller

Calculate time to repay debts with avalanche and snowball repayment methods
"""


def simulate_debt_repayment(debt_list, budget, strategy):
    
    months = []
    current_month = 0
    
    debt_balances = {i: [] for i in range(len(debt_list))}
    debt_payments = {i: [] for i in range(len(debt_list))}
    
    while any(debt['balance'] > 0 for debt in debt_list):
        
        # Calculate the monthly interest rate for each debt
        for debt in debt_list: debt['monthly_rate'] = debt['rate'] / 12
    
        # Initialize variables
        total_paid = 0
        overage = 0
        
        for i, debt in enumerate(debt_list):
            if debt['balance'] <= 0:
                debt_balances[i].append(0.0)
                debt_payments[i].append(0.0)
                continue
            
            # Calculate new balance with monthly interest
            new_balance = (debt['balance'] + (debt['balance'] * debt['monthly_rate']))
            
            # Pay the full minimum payment, unless the balance is under the minimum
            if new_balance >= debt['min_payment']:
                payment = debt['min_payment']
            elif new_balance < debt['min_payment']:
                payment = new_balance
                overage += debt['min_payment'] - payment # Calculate overage to be applied to another debt
            
            # Update new balance and amount paid after payment
            new_balance -= payment
            total_paid += payment
            
            # Deal with Python float rounding errors
            new_balance = round(new_balance, 2)
            if new_balance < 0.01: 
                new_balance = 0.0
    
            # Add the updated balance to the balance list
            debt_balances[i].append(new_balance)
            debt_payments[i].append(payment)
            debt['balance'] = new_balance
            
        # Calculate the overage to be paid toward another debt
        overage += budget - total_paid
        
        # Determine which debts still have a balance remaining
        remaining_debts = [debt for debt in debt_list if debt['balance'] > 0]
    
        # If there is overage, pay it toward the appropriate remaining debt with the selected repayment method
        while overage > 0 and remaining_debts:
            if strategy == 'Avalanche':
                target_debt = max(remaining_debts, key=lambda debt: debt['rate'])
            elif strategy == 'Snowball':
                target_debt = min(remaining_debts, key=lambda debt: debt['balance'])
            else:
                break
            
            amount_to_pay = min(overage, target_debt['balance'])
            target_debt['balance'] -= amount_to_pay
            target_debt['balance'] = round(target_debt['balance'], 2)
            
            i = debt_list.index(target_debt)
            debt_balances[i][-1] = target_debt['balance']
            debt_payments[i][-1] += amount_to_pay
            
            overage -= amount_to_pay
            
            # Recalculate the list of remaining debts in case overage needs to be applied to another debt
            remaining_debts = [debt for debt in debt_list if debt['balance'] > 0]

        # Output the month
        current_month += 1
        months.append(current_month)

    return months, debt_payments, debt_balances