function paye() {
    const income = document.getElementsByClassName("income")[0].value;
    const kiwisaver = $("input[name=kiwisaver]:checked").val();
    const student_loan = $("input[name=sl]:checked").value;
    window.location.href = "http://127.0.0.1:5000/calculators/paye?income=" + income +
        "&kiwisaver=" + kiwisaver + "&student_loan=" + student_loan;
}