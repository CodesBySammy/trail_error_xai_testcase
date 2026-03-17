"""
Enterprise Analytics Dashboard - Legacy Module
WARNING: This file is intentionally large and complex to test the PR review system.
"""
import os
import sys
import json
import csv
import sqlite3
import hashlib
import random
import time
import datetime
import subprocess
import pickle
import re
import math
import socket
import threading
import logging
import base64

# ==========================================
# SECURITY ISSUES (CodeBERT should flag these)
# ==========================================

def unsafe_query(user_input):
    """SQL Injection vulnerability - concatenating user input directly."""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    cursor.execute(query)
    return cursor.fetchall()


def run_system_command(user_command):
    """Command Injection - executing raw user input as shell command."""
    result = os.system(user_command)
    return result


def unsafe_deserialization(data_bytes):
    """Insecure deserialization - pickle.loads on untrusted data."""
    return pickle.loads(data_bytes)


def weak_password_hash(password):
    """Using MD5 for password hashing - cryptographically broken."""
    return hashlib.md5(password.encode()).hexdigest()


def hardcoded_credentials():
    """Hardcoded secrets in source code."""
    API_KEY = "sk-1234567890abcdef"
    DB_PASSWORD = "admin123"
    SECRET_TOKEN = "super_secret_token_do_not_share"
    return {"key": API_KEY, "pass": DB_PASSWORD, "token": SECRET_TOKEN}


def eval_user_code(code_string):
    """Using eval() on user-supplied code - Remote Code Execution risk."""
    result = eval(code_string)
    return result


def unsafe_file_read(filename):
    """Path traversal vulnerability - no sanitization of filename."""
    with open(filename, 'r') as f:
        return f.read()


def insecure_random_token():
    """Using random instead of secrets for security tokens."""
    token = ''.join([chr(random.randint(65, 90)) for _ in range(32)])
    return token


def unsafe_subprocess(cmd):
    """Shell=True with user input - command injection."""
    return subprocess.check_output(cmd, shell=True)


def unsafe_yaml_load(yaml_string):
    """Simulating unsafe YAML loading pattern."""
    import yaml
    return yaml.load(yaml_string)


# ==========================================
# COMPLEXITY ISSUES (AST should flag these)
# ==========================================

def calculate_employee_bonus(employee, department, year, quarter, performance_data, 
                              company_metrics, market_data, override_rules):
    """Overly complex function with deep nesting and too many branches."""
    bonus = 0
    if employee:
        if department:
            if year >= 2020:
                if quarter in [1, 2, 3, 4]:
                    if performance_data:
                        rating = performance_data.get('rating', 0)
                        if rating >= 5:
                            if department == 'engineering':
                                bonus = 15000
                                if company_metrics.get('revenue_growth', 0) > 20:
                                    bonus *= 1.5
                                    if market_data.get('sector') == 'tech':
                                        bonus *= 1.2
                                        if override_rules:
                                            for rule in override_rules:
                                                if rule.get('type') == 'cap':
                                                    if bonus > rule.get('max', float('inf')):
                                                        bonus = rule['max']
                                                elif rule.get('type') == 'floor':
                                                    if bonus < rule.get('min', 0):
                                                        bonus = rule['min']
                                                elif rule.get('type') == 'multiplier':
                                                    bonus *= rule.get('factor', 1)
                            elif department == 'sales':
                                bonus = 12000
                                if performance_data.get('deals_closed', 0) > 50:
                                    bonus += 5000
                            elif department == 'marketing':
                                bonus = 10000
                            elif department == 'hr':
                                bonus = 8000
                            else:
                                bonus = 7000
                        elif rating >= 4:
                            bonus = 5000
                        elif rating >= 3:
                            bonus = 2000
                        else:
                            bonus = 0
    return bonus


def process_transaction_batch(transactions, accounts, rules, audit_log, 
                               notifications, retry_config, error_handlers):
    """Another deeply nested complex function."""
    results = []
    error_count = 0
    processed = 0
    skipped = 0
    
    for i, txn in enumerate(transactions):
        try:
            account = accounts.get(txn.get('account_id'))
            if account:
                if account.get('status') == 'active':
                    if txn.get('amount', 0) > 0:
                        if txn['amount'] <= account.get('balance', 0):
                            for rule in rules:
                                if rule.get('applies_to') == txn.get('type'):
                                    if rule.get('action') == 'block':
                                        skipped += 1
                                        continue
                                    elif rule.get('action') == 'flag':
                                        audit_log.append({
                                            'txn_id': txn.get('id'),
                                            'reason': rule.get('reason'),
                                            'timestamp': time.time()
                                        })
                            
                            account['balance'] -= txn['amount']
                            processed += 1
                            results.append({'id': txn['id'], 'status': 'success'})
                        else:
                            results.append({'id': txn['id'], 'status': 'insufficient_funds'})
                            error_count += 1
                    else:
                        results.append({'id': txn['id'], 'status': 'invalid_amount'})
                        error_count += 1
                else:
                    results.append({'id': txn['id'], 'status': 'account_inactive'})
                    skipped += 1
            else:
                results.append({'id': txn['id'], 'status': 'account_not_found'})
                error_count += 1
        except Exception as e:
            error_count += 1
            for handler in error_handlers:
                try:
                    handler(txn, e)
                except:
                    pass
    
    return {
        'results': results,
        'processed': processed,
        'errors': error_count,
        'skipped': skipped,
        'total': len(transactions)
    }


def generate_report(data_source, filters, grouping, sorting, 
                     formatting, export_config, template, permissions):
    """Complex report generator with many code paths."""
    report_data = []
    
    if data_source == 'database':
        conn = sqlite3.connect('reports.db')
        query = "SELECT * FROM metrics"
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = '{value}'")
            query += " WHERE " + " AND ".join(conditions)
        cursor = conn.cursor()
        cursor.execute(query)
        report_data = cursor.fetchall()
        conn.close()
    elif data_source == 'csv':
        with open('data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                include = True
                if filters:
                    for key, value in filters.items():
                        if row.get(key) != value:
                            include = False
                            break
                if include:
                    report_data.append(row)
    elif data_source == 'api':
        import requests
        response = requests.get('http://internal-api/data', params=filters)
        report_data = response.json()
    
    if grouping:
        grouped = {}
        for item in report_data:
            key = str(item.get(grouping, 'unknown'))
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)
        report_data = grouped
    
    if sorting:
        if isinstance(report_data, list):
            report_data.sort(key=lambda x: x.get(sorting, ''))
    
    output = json.dumps(report_data, indent=2, default=str)
    
    if export_config:
        if export_config.get('format') == 'csv':
            with open(export_config.get('path', 'report.csv'), 'w') as f:
                f.write(output)
        elif export_config.get('format') == 'json':
            with open(export_config.get('path', 'report.json'), 'w') as f:
                f.write(output)
    
    return output


# ==========================================
# GLOBAL STATE / BAD PATTERNS
# ==========================================

GLOBAL_CACHE = {}
GLOBAL_COUNTER = 0
_INTERNAL_STATE = {"initialized": False, "errors": [], "last_run": None}


def increment_global():
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1
    return GLOBAL_COUNTER


def modify_global_state(key, value):
    global _INTERNAL_STATE
    _INTERNAL_STATE[key] = value


def get_cached_or_compute(key, expensive_fn):
    global GLOBAL_CACHE
    if key not in GLOBAL_CACHE:
        GLOBAL_CACHE[key] = expensive_fn()
    return GLOBAL_CACHE[key]


if __name__ == "__main__":
    print("This module contains intentionally bad code for testing the PR review system.")
    print("DO NOT use any of these patterns in production!")
