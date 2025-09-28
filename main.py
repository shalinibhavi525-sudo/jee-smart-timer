from flask import Flask, render_template, request, redirect, url_for
import time, csv, os
import matplotlib.pyplot as plt

app = Flask(__name__)
CSV_FILE = "data/sessions.csv"

# Store active timer in memory
active_timer = {"start": None}

def init_csv():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Question_No", "Time_Taken(s)", "Result"])

def log_result(q_no, duration, result):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([q_no, round(duration, 2), result])

def get_stats():
    times, results = [], []
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            times.append(float(row["Time_Taken(s)"]))
            results.append(1 if row["Result"] == "correct" else 0)

    if not times:
        return None

    avg_time = sum(times) / len(times)
    accuracy = (sum(results) / len(results)) * 100

    # Graph
    plt.plot(range(1, len(times)+1), times, marker="o", label="Time per Question (s)")
    plt.axhline(avg_time, color="red", linestyle="--", label=f"Avg Time ({avg_time:.2f}s)")
    plt.title("JEE Practice Timer Stats")
    plt.xlabel("Question Number")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.savefig("static/sample.png")
    plt.close()

    return {
        "attempted": len(times),
        "avg_time": avg_time,
        "accuracy": accuracy
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    active_timer["start"] = time.time()
    return redirect(url_for("index"))

@app.route("/stop", methods=["POST"])
def stop():
    if active_timer["start"] is None:
        return redirect(url_for("index"))

    duration = time.time() - active_timer["start"]
    active_timer["start"] = None
    result = request.form.get("result", "wrong")
    q_no = sum(1 for _ in open(CSV_FILE))  # count rows
    log_result(q_no, duration, result)
    return redirect(url_for("stats"))

@app.route("/stats")
def stats():
    stats_data = get_stats()
    return render_template("stats.html", stats=stats_data)

if __name__ == "__main__":
    init_csv()
    app.run(debug=True)
