import streamlit as st
import pandas as pd
import sqlite3
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate

class IPLQueryApp:
    def __init__(self):
        """Initialize the application"""
        self.setup_session_state()
        self.setup_gemini()
        
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'db_conn' not in st.session_state:
            st.session_state.db_conn = None
        if 'table_created' not in st.session_state:
            st.session_state.table_created = False
            
    def setup_gemini(self):
        """Setup Gemini API"""
        GEMINI_API_KEY = 'AIzaSyAZNEYWiW7uPyBZWlKLbq1ie2x1aUuSPDw'  # Replace with your API key
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def load_csv_to_db(self, df: pd.DataFrame) -> None:
        """Load DataFrame into SQLite database"""
        try:
            if st.session_state.db_conn is None:
                st.session_state.db_conn = sqlite3.connect(':memory:', check_same_thread=False)
            
            # Clean column names - remove spaces and special characters
            df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('/', '_')
            
            # Convert date column to proper format if it exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.date
            
            df.to_sql('ipl_matches', st.session_state.db_conn, if_exists='replace', index=False)
            st.session_state.table_created = True
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            raise
        
    def get_schema_info(self) -> str:
        """Get database schema information"""
        try:
            cursor = st.session_state.db_conn.cursor()
            cursor.execute("PRAGMA table_info(ipl_matches)")
            columns = cursor.fetchall()
            
            schema_info = "Table Schema:\n"
            schema_info += "Table name: ipl_matches\n"
            schema_info += "Columns:\n"
            for col in columns:
                schema_info += f"- {col[1]} ({col[2]})\n"
            
            # Add sample data
            sample_data = pd.read_sql("SELECT * FROM ipl_matches LIMIT 3", st.session_state.db_conn)
            schema_info += "\nSample data (first few rows):\n"
            schema_info += str(sample_data)
            
            return schema_info
        except Exception as e:
            st.error(f"Error getting schema: {str(e)}")
            raise
    
    def generate_sql_query(self, schema: str, question: str) -> str:
        """Generate SQL query using Gemini"""
        prompt_template = """You are an SQL expert. Given the following SQL table schema and sample data for IPL matches:
        {schema}
        Generate a SQL query to answer this question: {question}
        Requirements:
        1. Use only the columns and table shown in the schema
        2. Return a valid SQL query that can be executed against the table
        3. Do not use any tables or columns not shown in the schema
        4. Return ONLY the SQL query without any markdown tags or explanations
        5. The table name is 'ipl_matches'
        6. Make sure column names match exactly with the schema
        SQL Query:"""
        
        try:
            prompt = prompt_template.format(schema=schema, question=question)
            response = self.model.generate_content(prompt)
            # Clean the response - remove any markdown or extra formatting
            query = response.text.strip()
            query = query.replace('```sql', '').replace('```', '').strip()
            return query
            
        except Exception as e:
            st.error(f"Error generating query: {str(e)}")
            raise
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            return pd.read_sql_query(query, st.session_state.db_conn)
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
            raise
    
    def run(self):
        """Run the Streamlit application"""
        st.title("IPL Matches Query Generator 🎉")

        # Custom CSS for styling
        st.markdown("""
        <style>
        .css-1v3fvcr {
            background-color: #f7f7f7;
        }
        .css-ffhzg2 {
            font-size: 24px;
            font-weight: bold;
            color: #2d2d2d;
        }
        .stButton button {
            background-color: #3faffa;
            color: white;
            font-size: 18px;
        }
        .stTextInput input {
            font-size: 18px;
            padding: 12px;
        }
        .stTextArea textarea {
            font-size: 18px;
            padding: 12px;
        }
        .stExpanderHeader {
            background-color: #e8f4f8;
            font-size: 18px;
            color: #2d2d2d;
        }
        </style>
        """, unsafe_allow_html=True)

        # File upload
        uploaded_file = st.file_uploader("Upload IPL matches CSV file 📂", type=['csv'])
        
        if uploaded_file:
            try:
                # Load CSV into DataFrame and database
                df = pd.read_csv(uploaded_file)
                self.load_csv_to_db(df)
                st.success("Data loaded successfully! 🎉")
                
                # Display schema information
                schema_info = self.get_schema_info()
                with st.expander("View Schema Details 📊"):
                    st.text(schema_info)
                
                # Query input
                st.write("### Ask questions about IPL matches 🏏")
                st.write("Example questions: ")
                st.write("1. Show me the highest target runs for each team 🎯")
                st.write("2. Count the number of matches won by each team 🏆")
                st.write("3. Find matches where the target runs were above 200 💯")
                
                user_question = st.text_area("Enter your question here 👇:")

                if user_question:
                    # Generate and display SQL query
                    with st.spinner("Generating SQL query... ⏳"):
                        sql_query = self.generate_sql_query(schema_info, user_question)
                        st.write("Generated SQL Query: 📝")
                        st.code(sql_query, language="sql")
                    
                    # Execute query button
                    if st.button("Execute Query 🚀"):
                        with st.spinner("Executing query... ⏳"):
                            results = self.execute_query(sql_query)
                            st.write("Query Results: 📈")
                            st.dataframe(results)
                            st.write(f"Total Records: {len(results)}")
                            
                            # Download results button
                            if not results.empty:
                                csv = results.to_csv(index=False)
                                st.download_button(
                                    label="Download Results as CSV 📥",
                                    data=csv,
                                    file_name="query_results.csv",
                                    mime="text/csv"
                                )
                                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Please try again with a different question or check your data format.")

if __name__ == "__main__":
    app = IPLQueryApp()
    app.run()
