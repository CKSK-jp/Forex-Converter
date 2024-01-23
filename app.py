import requests
from babel.numbers import format_currency
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

APP_KEY = "4f2aa5fda843ef40ca348191b63de4ea"
BASE_URL = "http://api.exchangerate.host/convert"

app = Flask(__name__)
app.secret_key = "123-456-789"


@app.route("/")
def converter_home():
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", messages=messages)


def get_result(input, output, amount):
    """Checks user input values and returns appropriate errors or request data

    Parameters
    ----------
    input : String Currency Code
    output : String Currency Code
    amount : Positive float value
    """
    api_url = (
        f"{BASE_URL}?access_key={APP_KEY}&from={input}&to={output}&amount={amount}"
    )
    response = requests.get(api_url)
    response_data = response.json()
    print(response_data)

    if "error" in response_data:
        response_code = response_data["error"]["code"]
        if response_code == 401:
            flash(f"Not a valid code: {input}", category="error")
        elif response_code == 402:
            flash(f"Not a valid code: {output}", category="error")
        elif response_code == 403:
            flash(f"Not a valid amount: {amount}", category="error")
        else:
            flash(f"Unexpected error: {response_code}", category="error")
        return None

    result = response_data["result"]
    currency_code = response_data["query"]["to"]
    formatted_result = format_currency(round(float(result), 2), currency_code)
    return formatted_result


@app.route("/convert_me", methods=["POST"])
def render_conversion():
    """
    Renders conversion request to page
    """
    try:
        input_currency = request.form.get("input_currency").upper()
        output_currency = request.form.get("output_currency").upper()
        amount = float(request.form.get("amount"))

        result = get_result(input_currency, output_currency, amount)

        if result is not None:
            flash("Successfully converted!", category="success")
            return render_template(
                "index.html",
                input=input_currency,
                amount=amount,
                result=result,
                messages=get_flashed_messages(with_categories=True),
            )
        else:
            return render_template(
                "index.html", messages=get_flashed_messages(with_categories=True)
            )
    except ValueError as e:
        flash(str(e), category="error")
        return redirect(url_for("converter_home"))


if __name__ == "__main__":
    app.run(debug=True)
