from flask import Flask, jsonify, render_template
from flask_cors import CORS
from Configuration.DbConection.queries import daily_sellers_sales_query, monthly_sellers_sales_query, dated_sellers_sales_query
from Configuration.DbConection.DbConnect import DbConnection
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

class SalesDataLoader:
    def __init__(self, sales_query):
        self.sales_query = sales_query

    def get_sales_data(self, sales_codes):
        load_dotenv()    
        db_conn = DbConnection(
            host=os.environ.get('HOST', False), 
            port=os.environ.get('PORT', False), 
            dbname=os.environ.get('DBNAME', False), 
            user=os.environ.get('USER', False), 
            password=os.environ.get('PASSWD', False)
            )

        if not db_conn.connect(): 
            return [], {'error': str(db_conn.error)}

        sales_data = {}
        for code in sales_codes:
            sales_data[code] = db_conn.sqlquery(self.sales_query, (code, code))[0]

        if db_conn.error: 
            return [], {'error': str(db_conn.error)}
        
        return sales_data, None

@app.route('/daily', methods=['GET'])
def get_daily_scores():
    daily_loader = SalesDataLoader(daily_sellers_sales_query)
    sales_codes = ('000054', '000095', '000090', '000019')
    sales_data, error = daily_loader.get_sales_data(sales_codes)

    if error:
        return jsonify(error), 500

    breno_goal = 5000
    kathleen_goal = 5000
    arthur_goal = 3750
    marcelo_goal = 5000

    scores = [
        {'name': 'Marcelo', 'sales': sales_data['000019']['total'], 'sales_goal': marcelo_goal},
        {'name': 'Breno', 'sales': sales_data['000054']['total'], 'sales_goal': breno_goal},
        {'name': 'Arthur', 'sales': sales_data['000090']['total'], 'sales_goal': arthur_goal},
        {'name': 'Kathleen', 'sales': sales_data['000095']['total'], 'sales_goal': kathleen_goal}
    ]

    scores.sort(key=lambda score: score['sales'], reverse=True)
    return jsonify({'scores': scores})

@app.route('/monthly', methods=['GET'])
def get_monthly_scores():
    monthly_loader = SalesDataLoader(monthly_sellers_sales_query)
    sales_codes = ('000054', '000095', '000090', '000019')
    sales_data, error = monthly_loader.get_sales_data(sales_codes)

    if error:
        return jsonify(error), 500

    breno_goal = 120000
    kathleen_goal = 120000
    arthur_goal = 90000
    marcelo_goal = 120000

    scores = [
        {'name': 'Marcelo', 'sales': sales_data['000019']['total'], 'sales_goal': marcelo_goal},
        {'name': 'Breno', 'sales': sales_data['000054']['total'], 'sales_goal': breno_goal},
        {'name': 'Arthur', 'sales': sales_data['000090']['total'], 'sales_goal': arthur_goal},
        {'name': 'Kathleen', 'sales': sales_data['000095']['total'], 'sales_goal': kathleen_goal}
    ]

    scores.sort(key=lambda score: score['sales'], reverse=True)
    return jsonify({'scores': scores})

@app.route('/daily/<date>', methods=['GET'])
def get_daily_scores_by_date(date):
    date = date.replace('-', '/')
    daily_loader = SalesDataLoader(dated_sellers_sales_query.format(date, date))
    sales_codes = ('000054', '000095', '000090', '000019')
    sales_data, error = daily_loader.get_sales_data(sales_codes)

    if error:
        return jsonify(error), 500

    breno_goal = 5000
    kathleen_goal = 5000
    arthur_goal = 3750
    marcelo_goal = 5000

    scores = [
        {'name': 'Marcelo', 'sales': sales_data['000019']['total'], 'sales_goal': marcelo_goal},
        {'name': 'Breno', 'sales': sales_data['000054']['total'], 'sales_goal': breno_goal},
        {'name': 'Arthur', 'sales': sales_data['000090']['total'], 'sales_goal': arthur_goal},
        {'name': 'Kathleen', 'sales': sales_data['000095']['total'], 'sales_goal': kathleen_goal}
    ]

    scores.sort(key=lambda score: score['sales'], reverse=True)
    return jsonify({'scores': scores})


@app.route('/rank', methods=['GET'])
def show_rank():
    return render_template('rank.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5900')
