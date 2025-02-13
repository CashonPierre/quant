import pandas as pd
from flask import Flask, jsonify, request, send_file
import io
# load csv
df = pd.read_csv('constituents-financials_csv.csv')

app = Flask(__name__)

@app.route('/Sector')
def unique_sectors():
    unique_sector = df['Sector'].unique().tolist()
    return jsonify({'sectors': unique_sector})

@app.route('/EBITDA')
def ebitda():
    sector = request.args.get('Sector')  # Get the 'Sector' parameter from the URL
    ebitda_values = df[df['Sector'] == sector]['EBITDA'].tolist()
    return jsonify(ebitda_values)  # Return the list of EBITDAs as JSON


@app.route('/download_csv', methods=['GET'])
def download_csv():
    return send_file('constituents-financials_csv.csv')

def main():
    app.run(debug=True, port=5000)  # Change port to 5000

if __name__ == '__main__':
    main()  # Call the main function to run the app
