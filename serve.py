from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json
from qaptnet.qaptnet import qaptnet

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "./"
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config["UPLOAD_FOLDER"] = "files/"

json_app = FlaskJSON(app)
ptnet = qaptnet()


@as_json
@app.route("/predict_json", methods=["POST"])
def predict_json():

    data = request.get_json()
    if (data["type"] != "text") or ("content" not in data) or ("params" not in data):
        return invalid_request_error(
            None,
            error="One of the following fields of the request is absent: [text, content, params]",
        )

    content = data.get("content")
    params = data["params"]
    if "question" not in params:
        return invalid_request_error(None, error="Question parameter is absent")

    context = content
    question = params["question"]

    try:
        answer = get_answer(context, question)
        output = generate_successful_text_response(answer)
        return output
    except Exception as e:
        text = "An unexpected error ocurred during prediction. If your input text is too long, this may be the cause."
        return generate_failure_response(
            status=404,
            code="elg.service.internalError",
            text=text,
            params=None,
            detail=e.__str__(),
        )


def get_answer(context, question):

    answer = ptnet.query(context=context, question=question)
    return answer


@json_app.invalid_json_error
def invalid_request_error(e, error=""):
    """Generates a valid ELG "failure" response if the request cannot be parsed"""
    raise JsonError(
        status_=400,
        failure={
            "errors": [
                {
                    "code": "elg.request.invalid",
                    "text": "Invalid request message. " + error,
                }
            ]
        },
    )


def generate_successful_text_response(answer):
    response = {"type": "texts", "texts": [{"content": answer}]}
    output = {"response": response}
    return output


def generate_failure_response(status, code, text, params, detail):
    error = {}
    if code:
        error["code"] = code
    if text:
        error["text"] = text
    if params:
        error["params"] = params
    if detail:
        error["detail"] = {"message": str(detail)}

    raise JsonError(status_=status, failure={"errors": [error]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8866)
