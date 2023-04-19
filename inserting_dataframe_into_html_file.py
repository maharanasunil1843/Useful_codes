import pandas as pd

# Create a simple dataframe
data1 = {'Name': ['John', 'Jane', 'Bob'], 'Age': [32, 28, 45]}
df1 = pd.DataFrame(data1)


# Convert the dataframe to an HTML table
html_table1 = df1.to_html()

# Create the HTML page
html1 = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>My Webpage</title>
    </head>
    <body>
        <h1>My Dataframe</h1>
        {html_table1}
    </body>
</html>
"""

# Save the HTML page to a file
with open('templates/my_webpage1.html', 'w') as f:
    f.write(html1)

