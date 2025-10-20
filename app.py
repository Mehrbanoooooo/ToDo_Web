from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

tasks_file = "tasks.csv"

# خواندن کارها از CSV


def load_tasks():
    tasks = []
    try:
        with open(tasks_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        pass
    return tasks

# ذخیره کارها در CSV


def save_tasks(tasks):
    with open(tasks_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Name", "Description", "Priority"])
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)


@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        priority = request.form["priority"]
        tasks.append(
            {"Name": name, "Description": description, "Priority": priority})
        save_tasks(tasks)
        return redirect("/")
    return render_template("index.html", tasks=tasks)


@app.route("/delete/<name>")
def delete(name):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["Name"] != name]
    save_tasks(tasks)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
