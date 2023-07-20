from bokeh.palettes import Purples
from flask import Blueprint, render_template, request


calculators_bp = Blueprint("calculators",
                           __name__,
                           template_folder="templates",
                           static_folder="static",
                           static_url_path="/calculators/static")


def calculate_tax(income):
    tax_owed = 0

    # Tax rates and income brackets for New Zealand as of the knowledge cutoff (2021)
    tax_brackets = [(0, 14_000, 0.105),
                    (14_001, 48_000, 0.175),
                    (48_001, 70_000, 0.3),
                    (70_001, 180_000, 0.33),
                    (180_001, float('inf'), 0.39)]

    for lower, upper, rate in tax_brackets:
        if income <= lower:
            break
        taxable_amount = min(income, upper) - lower
        tax_owed += taxable_amount * rate

    return tax_owed


@calculators_bp.route("/paye")
def paye():
    income = request.args.get("income", default="0")
    kiwisaver = request.args.get("kiwisaver", default="0.03")
    student_loan = request.args.get("student_loan", default="no")

    tax = calculate_tax(int(income))
    acc = int(income) * 0.0153
    kiwisaver_contributions = int(income) * float(kiwisaver)

    if student_loan == "yes" and int(income) > 22828:
        student_loan_repayments = (int(income) - 22828) * 0.12
    else:
        student_loan_repayments = 0

    takehome_pay = int(income) - tax - acc - kiwisaver_contributions - student_loan_repayments

    labels = ["Tax", "KiwiSaver", "Student Loan", "ACC", "Take Home Pay"]
    data = [tax, kiwisaver_contributions, student_loan_repayments, acc, takehome_pay]
    colours = list(Purples[5])

    return render_template("paye.html",
                           income=income,
                           kiwisaver=kiwisaver,
                           student_loan=student_loan,
                           labels=labels,
                           data=data,
                           colours=colours)
