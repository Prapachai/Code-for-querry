import re
import pandas as pd

def find_aggregate_function(sql_query):
    # Regular expression pattern to identify SQL functions with aggregate names
    function_pattern = r'\b(SUM|AVG|COUNT|MIN|MAX)\b\s*\([^)]*\)'
    
    # Find all occurrences of aggregate functions in the SQL query
    aggregate_function_names = re.findall(function_pattern, sql_query, flags=re.IGNORECASE)
    
    # If aggregate function(s) are found
    if aggregate_function_names:
        # Extract the first aggregate function name (without parentheses)
        aggregate_function = aggregate_function_names[0].split('(')[0].strip().upper()
        return aggregate_function
    else:
        return None  # Return None if no aggregate function is detected

# Example SQL queries
sql_query1 = "SELECT SUM(amount) FROM transactions WHERE date > '2024-01-01';"
sql_query2 = "SELECT * FROM users WHERE age > 30;"

# Test the function
aggregate_func_query1 = find_aggregate_function(sql_query1)
aggregate_func_query2 = find_aggregate_function(sql_query2)

# Print results
if aggregate_func_query1:
    print("Aggregate function detected in SQL Query 1:", aggregate_func_query1)
else:
    print("No aggregate function detected in SQL Query 1")

if aggregate_func_query2:
    print("Aggregate function detected in SQL Query 2:", aggregate_func_query2)
else:
    print("No aggregate function detected in SQL Query 2")

if aggregate_func_query2 == None ,:
    # Normal query
    print()
    json_path = 'test.json'

    with open(json_path, 'r') as file:
        data = file.read() 
        df = pd.read_json(data)
        print(df.head())
else:
    # Has Aggregation query
    print()
