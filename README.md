🏏 NL to SQL Query Generator

_________________________________________________________________________________________________________________________________________________

📌 Overview

The NL to SQL Query Generator is a Streamlit-based web application that allows users to upload IPL match data in CSV format and interactively generate SQL queries using Google's Gemini API. Users can ask questions in natural language, and the application will convert them into executable SQL queries to retrieve relevant data.

_________________________________________________________________________________________________________________________________________________

✨ Features

👉 📂 CSV File Upload: Users can upload an IPL matches dataset in CSV format.

👉 🟢 SQLite Database Integration: The uploaded data is loaded into an in-memory SQLite database.

👉 📊 Schema Extraction: Displays table schema and sample data.

👉 🤖 AI-Powered Query Generation: Uses Gemini API to generate SQL queries based on user input.

👉 ⚡ Query Execution: Runs the generated SQL query against the database and displays results.

👉 📥 Download Query Results: Users can download the results as a CSV file.

_________________________________________________________________________________________________________________________________________________

⚙️ Installation

To run this application locally, follow these steps:

🔹 Prerequisites

🔸 Python 3.7+

🔸 pip installed

🔸 Google Gemini API key

🔹 Setup

🔢 Clone the repository or download the script.

git clone https://github.com/Prathapmahi/ipl-query-generator.git
cd ipl-query-generator

🔢 Install required dependencies.

pip install streamlit pandas sqlite3 google-generativeai langchain_core

🔢 Set up your Gemini API key.

🔹 Open the ipl_query_app.py file and replace GEMINI_API_KEY with your own key.

🔹 Alternatively, set it as an environment variable:

export GEMINI_API_KEY='your-api-key'

🔢 Run the Streamlit application.

streamlit run ipl_query_app.py

_________________________________________________________________________________________________________________________________________________

🚀 Usage

📂 📤 Upload CSV: Click on "Upload IPL matches CSV file" and select a valid CSV file.

📝 📃 View Schema: The application will display the database schema and sample data.

💬 📓 Ask Questions: Enter a question related to IPL matches in the text area.

🔄 🔍 Generate SQL Query: The AI will generate an SQL query based on the dataset.

👉 ▶️ Execute Query: Click on the "Execute Query" button to run the query.

📊 📈 View & Download Results: The query results are displayed, and you can download them as a CSV file.

💡 Example Questions

💬 "Show me the highest target runs for each team."

💬 "Count the number of matches won by each team."

💬 "Find matches where the target runs were above 200."

_________________________________________________________________________________________________________________________________________________

🛠️ Troubleshooting

🚨 Ensure your CSV file contains valid IPL match data.

🚨 Check if the dataset includes expected columns.

🚨 If queries fail, verify that the generated SQL query matches the schema.

🚨 If issues persist, restart the application and try again.

_________________________________________________________________________________________________________________________________________________

📝 License

📚 This project is licensed under the MIT License.

