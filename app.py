import openai
import json
from flask import Flask, render_template, request, jsonify

# Replace 'YOUR_OPENAI_API_KEY' with your actual API key
openai.api_key = "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"

# Define the 'function_descriptions' dictionary containing function descriptions
function_descriptions = [
    {
        "name": "get_subject_name",
        "description": "check the subject name of the question entered by the user",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic of the question e.g. addition, subtraction, division, multiplication, degree",
                },
                "operator": {
                    "type": "string",
                    "description": "The operator used in question e.g. +, -, *, /, sin, degree, cos, tan, cot, cosec, sec, log",
                },
            },
            "required": ["topic", "operator"],
        },
    }
]

def get_subject_name(topic, operator):
    subject_info = {
        "topic": topic,
        "operator": operator,
    }
    return json.dumps(subject_info)

def check_values_in_dict(dict1, dict2):
    # Extract the values from dict1
    topic_value = dict1["topic"]
    operator_value = dict1["operator"]

    # Check if the values are present in the values of either key in dict2
    for valid_values in dict2.values():
        if topic_value in valid_values or operator_value in valid_values:
            return True
        else: 
            return False


# Sample data with valid topics and operators
data = {
    "valid_topics": [
        "addition", "subtraction", "division", "multiplication", "degree",
        "square", "cube", "cuboid", "cone", "cylinder", "circle", "triangle",
        "parallelogram", "rectangle", "trapezium", "rhomboid", "rhombus"
    ],
    "valid_operators": [
        "+", "-", "*", "/", "sin", "degree", "cos", "tan", "cot", "cosec",
        "sec", "log", "area", "volume", "perimeter", "circumference",
        "radius", "diameter"
    ]
}

# Flask app setup
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    user_message = request.form["msg"]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": user_message}],
        functions=function_descriptions,
        function_call={"name": "get_subject_name"},
    )
    output = completion.choices[0].message
    function_call_data = json.loads(output["function_call"]["arguments"])
    result = check_values_in_dict(function_call_data, data)

    if result:
        return "You are not authorized to ask this question."
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": user_message}],
        )
        assistant_message = response.choices[0].message["content"]
        return jsonify({"assistant_message": assistant_message})

if __name__ == "__main__":
    app.run(debug=True)
