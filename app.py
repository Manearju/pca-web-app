from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# PCA Coefficients (based on your model)
def calculate_scores(df):
    # Ensure required columns exist
    columns_needed = ['Mat', 'Inn', 'NO', 'Runs', 'HS', 'Avg', 'Hundreds', 'Fifties', 'Duck']
    df = df[columns_needed].copy()

    # Convert all columns to numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()

    # Define L1, L2, L3
    df['L1'] = -df['Mat']*0.388 - df['Inn']*0.399 - df['NO']*0.302 - df['Runs']*0.411 - df['HS']*0.227 \
               - df['Avg']*0.205 - df['Hundreds']*0.376 - df['Fifties']*0.384 - df['Duck']*0.219

    df['L2'] = -df['Mat']*0.25 - df['Inn']*0.197 + df['NO']*0.275 + df['Runs']*0.0975 + df['HS']*0.4402 \
               + df['Avg']*0.5752 + df['Hundreds']*0.2508 + df['Fifties']*0.0263 - df['Duck']*0.475

    df['L3'] = df['Mat']*0.0195 - df['Inn']*0.024 + df['NO']*0.4866 + df['Runs']*0.0235 - df['HS']*0.605 \
               + df['Avg']*0.2173 - df['Hundreds']*0.003 + df['Fifties']*0.1656 - df['Duck']*0.567

    # Compute PWA Score
    df['PWA'] = (df['L1']*62.72 + df['L2']*20.69 + df['L3']*7.06) / 90.47

    # Rank players
    df['Rank'] = df['PWA'].rank(method='min', ascending=True).astype(int)

    return df.sort_values('Rank')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            result = calculate_scores(df)
            return render_template('result.html', tables=result.to_html(classes='table table-bordered table-striped', index=False))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
