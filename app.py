
from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary data storage
students = [
    {"id": 1, "name": "Rahul", "course": "Python"},
    {"id": 2, "name": "Priya", "course": "Java"}
]


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student REST API",
        "available_routes": [
            "GET /students",
            "GET /students/<id>",
            "POST /students",
            "PUT /students/<id>",
            "DELETE /students/<id>"
        ]
    })


# GET: View all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)


# GET: View one student
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404


# POST: Add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("course"):
        return jsonify({
            "error": "Name and course are required"
        }), 400

    new_id = max(
        [student["id"] for student in students],
        default=0
    ) + 1

    new_student = {
        "id": new_id,
        "name": data["name"],
        "course": data["course"]
    }

    students.append(new_student)

    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201


# PUT: Update student details
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}

    for student in students:
        if student["id"] == student_id:

            if "name" in data:
                student["name"] = data["name"]

            if "course" in data:
                student["course"] = data["course"]

            return jsonify({
                "message": "Student updated successfully",
                "student": student
            })

    return jsonify({"error": "Student not found"}), 404


# DELETE: Delete a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)

            return jsonify({
                "message": "Student deleted successfully"
            })

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
