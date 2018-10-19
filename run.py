"""Run file runs our application"""
from app import app
from app.products import view
from app.sales import view

if __name__ == '__main__':
    app.run(debug=True, port=8080)
