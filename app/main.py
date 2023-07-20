from flask import Flask
from blueprints.dashboard.routes import dashboard_bp
from blueprints.transactions.routes import transactions_bp
from blueprints.kiwisaver.routes import kiwisaver_bp
from blueprints.calculators.routes import calculators_bp
from blueprints.portfolio.routes import portfolio_bp

app = Flask(__name__, template_folder="templates")

app.register_blueprint(dashboard_bp)
app.register_blueprint(transactions_bp, url_prefix="/transactions")
app.register_blueprint(kiwisaver_bp, url_prefix="/kiwisaver")
app.register_blueprint(calculators_bp, url_prefix="/calculators")
app.register_blueprint(portfolio_bp, url_prefix="/portfolio")


@app.template_filter()
def ymd_to_dmy(date):
    return f"{date[8:]}/{date[5:7]}/{date[2:4]}"


# Invalid URL handler
@app.errorhandler(404)
def error_404(e):
    return e


# Internal Server Error handler
@app.errorhandler(500)
def error_500(e):
    return e


if __name__ == "__main__":
    app.run(debug=True)
