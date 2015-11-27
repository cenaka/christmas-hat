import random
import copy
from itertools import permutations
from flask import render_template, flash, redirect, request, jsonify, url_for
from FlaskWebProject import app

result = []


@app.route('/')
def input_form():
    return render_template("input_form.html")


@app.route('/name', methods=['POST'])
def get_names():
    global result
    names = request.form['names'].split(",")
    not_to_names = request.form['not_to_names'].split(",")
    result = chistmas_hat(names, not_to_names)
    result = dict(zip(names, result))
    return render_template("input_form.html")


@app.route("/christmas_hat")
def public_page():
    return render_template("christmas_hat.html",
                           number_of_people=len(result),
                           names=list(result.keys()))


@app.route("/secret_santa", methods=["POST"])
def secret_santa():
    santa = request.form["name"]
    person = result[santa]
    del result[santa]
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
