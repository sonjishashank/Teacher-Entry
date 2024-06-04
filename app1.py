from flask import Flask, request, render_template
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

app = Flask(__name__)

# PostgreSQL database credentials
db_credentials = {
    'dbname': 'bang_lore',
    'user': 'bang_lore_user',
    'password': 'GB9o29yszCItLrOGGBj5WgauI3E4ckfu',
    'host': 'dpg-cpest0v79t8c73bdet8g-a.singapore-postgres.render.com',
    'port': '5432'
}

# Create PostgreSQL database engine
engine = create_engine(f'postgresql://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}', echo=True)

def create_or_update_table(class_name):
    # Define table name based on the class
    table_name = f'class_{class_name}'

    # Check if the table exists
    meta = MetaData()
    meta.reflect(bind=engine)
    if table_name not in meta.tables:
        # Define the table with specified columns
        table = Table(
            table_name, meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('student_id', String),
            Column('subject', String),
            Column('marks', Integer),
            Column('test_no', Integer),
            Column('topic', String),
            Column('study_hours', Integer),
            Column('basic_requirements', String),  # New column added
        )
        meta.create_all(engine)
    else:
        table = meta.tables[table_name]

    return table

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    class_name = request.form['class']
    student_id = request.form['studentId']
    subject = request.form['subject']
    marks = request.form['marks']
    test_no = request.form['testNo']
    topic = request.form['topic']
    study_hours = request.form['Study Hours']
    basic_requirements = request.form['Basic Requirements']  # Get value for new column

    # Create or update the table
    table = create_or_update_table(class_name)

    # Create a DataFrame to insert into the database
    df = pd.DataFrame({
        'student_id': [student_id],
        'subject': [subject],
        'marks': [marks],
        'test_no': [test_no],
        'topic': [topic],
        'study_hours': [study_hours],
        'basic_requirements': [basic_requirements],  # Include new column data
    })

    # Insert data into the database
    df.to_sql(table.name, con=engine, if_exists='append', index=False)

    return "Data submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
