import random
import copy
from itertools import permutations
from flask import render_template, flash, redirect, request, jsonify, url_for
from FlaskWebProject import app
import pickle
import ast


@app.route('/')
def input_form():
    return render_template("input_form.html")


@app.route('/name', methods=['POST'])
def get_names():
    names = request.form['names'].split(",")
    not_to_names = request.form['not_to_names'].split(",")
    result = chistmas_hat(names, not_to_names)
    result = dict(zip(names, result))
    write_to_file(result)
    return redirect(render_template("christmas_hat.html",
                           names=list(result.keys())), code=307)


@app.route("/christmas_hat")
def public_page():
    result = read_from_file()
    return render_template("christmas_hat.html",
                           names=list(result.keys()))


@app.route("/secret_santa", methods=["POST"])
def secret_santa():
    santa = request.form["name"]
    result = read_from_file()
    person = result[santa]
    del result[santa]
    write_to_file(result)
    return render_template("result.html", name=person)


def chistmas_hat(people, not_to_people):
    shuffle = copy.deepcopy(people)
    random.shuffle(shuffle)
    
    for shuffle_names in permutations(shuffle):
        flag = True
        for j, name in enumerate(shuffle_names):
            if name == people[j]:
                flag = False
                break
            elif name == not_to_people[j]:
                flag = False
                break
        if flag:
            return list(shuffle_names)
    return None


def write_to_file(value, filepath="FlaskWebProject/static/result.pkl"):
    with open(filepath, 'wb') as f:
        pickle.dump(value, f)

def read_from_file(filepath="FlaskWebProject/static/result.pkl"):
    with open(filepath, 'rb') as f:
        value = pickle.load(f)
    return value

if __name__ == "__main__":
    filepath = "static/result.pkl"
    write_to_file(filepath, str({"a":1, "b":2}))
    value = read_from_file(filepath)
    print(ast.literal_eval(value))
