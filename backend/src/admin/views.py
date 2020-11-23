import pathlib
from collections import OrderedDict

import xlrd
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import admin
from .forms import QuestionForm
from .. import db, LOGGER, current_dir, allowed_file
from ..models import User, Question
from ..admin.forms import UserForm


def get_excel_data(excel_file):
    sheet, columns = "", ""
    data_list = []
    try:
        workbook = xlrd.open_workbook(excel_file)
        sheet = workbook.sheet_by_index(0)
        columns = sheet.row_values(0)
    except FileNotFoundError as error:
        LOGGER.error(f"FileNotFoundException: {error}")
        abort(400, error)

    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        data[columns[0]] = row_values[0]
        data[columns[1]] = row_values[1]
        data[columns[2]] = row_values[2]
        data[columns[3]] = row_values[3]
        data[columns[4]] = row_values[4]
        data[columns[5]] = row_values[5]
        data[columns[6]] = row_values[6]
        data_list.append(data)

    return data_list


def check_admin():
    """
    Prevent non-admins from accessing the page
    """

    LOGGER.info("Check if user is an admin")
    if not current_user.is_admin:
        abort(403)


@admin.route("/admin/questions", methods=["GET", "POST"])
@login_required
def list_questions():
    """
    List all questions
    """

    check_admin()

    LOGGER.info("List all questions")
    all_questions = Question.query.all()
    return render_template("admin/questions/questions.html", questions=all_questions, title="List Questions")


@admin.route("/questions/bulk", methods=["POST"])
@login_required
def add_questions_bulk():
    """
    Add questions in bulk
    """

    check_admin()

    LOGGER.info("Import questions in bulk from a excel file")
    data_file = pathlib.Path(current_dir, "static", "sample_questions.xlsx")

    if request.method == "POST":
        request_fields = request.get_json() if request.get_json() else request.files

        data = {}
        if "xlsx_upload" in request_fields:
            LOGGER.info("Request has a file part. Using it.")
            data_file = request.files["xlsx_upload"]
            if not allowed_file(data_file.filename):
                abort(400, "Format file not allowed")

            filename = secure_filename(data_file.filename)
            data_file.save(pathlib.Path(current_dir, "static", filename))
            data_file.close()
            data_file = pathlib.Path(current_dir, "static", filename)

            data = get_excel_data(data_file)
        else:
            abort(400, "'xlsx_upload' key not found.")

        levels = {"Beginner": 1, "Easy": 1.5, "Normal": 2, "Hard": 2.5, "Very Hard": 3, "Fiendish": 5}
        for d in data:
            question = Question(
                description=d.get("QuestionText"),
                correct_answer=d.get("Answer"),
                subject=d.get("Subject"),
                false_answer_1=d.get("False1"),
                false_answer_2=d.get("False2"),
                false_answer_3=d.get("False3"),
                level=levels.get(d.get("Level")),
            )
            try:
                # add questions to the database
                db.session.add(question)
                db.session.commit()
                flash("You have successfully added a new question.")
            except Exception as error:
                LOGGER.error(f"Exception: {error}")
                flash("Error: There was an error and this question couldn't be added. Check each item and try again")

        return {"message": "The questions have successfully been imported."}, 201

    else:
        abort(405)


@admin.route("/admin/questions/add", methods=["GET", "POST"])
@login_required
def add_question():
    """
    Add a question to the database
    """

    check_admin()

    LOGGER.info("Add a question")
    add_a_question = True

    LOGGER.info("Open the question form")
    form = QuestionForm()
    if form.validate_on_submit():
        LOGGER.info("Question form has been validated. Add to database")
        question = Question(
            description=form.description.data,
            correct_answer=form.correct_answer.data,
            subject=form.subject.data,
            false_answer_1=form.false_answer_1.data,
            false_answer_2=form.false_answer_2.data,
            false_answer_3=form.false_answer_3.data,
            level=form.level.data,
        )
        try:
            # add questions to the database
            db.session.add(question)
            db.session.commit()
            flash("You have successfully added a new question.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this question couldn't be added. Check each item and try again")

        # redirect to questions page
        return redirect(url_for("admin.list_questions"))

    # load question template
    return render_template(
        "admin/questions/question.html",
        action="Add",
        add_question=add_a_question,
        form=form,
        title="Add Question",
    )


@admin.route("/admin/questions/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_question(id):
    """
    Edit a question
    """

    check_admin()

    edit_a_question = True

    question = Question.query.get_or_404(id)

    LOGGER.info(f"Edit question: {question.id}")
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.description = form.description.data
        question.correct_answer = form.correct_answer.data
        question.subject = form.subject.data
        question.false_answer_1 = form.false_answer_1.data
        question.false_answer_2 = form.false_answer_2.data
        question.false_answer_3 = form.false_answer_3.data
        question.level = form.level.data

        try:
            # edit question in the database
            db.session.commit()
            flash("You have successfully edited the question.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this question couldn't be edited. Check each item and try again")

        # redirect to the questions page
        return redirect(url_for("admin.list_questions"))

    form.description.data = question.description
    form.correct_answer.data = question.correct_answer
    form.subject.data = question.subject
    form.false_answer_1.data = question.false_answer_1
    form.false_answer_2.data = question.false_answer_2
    form.false_answer_3.data = question.false_answer_3
    form.level.data = question.level
    return render_template(
        "admin/questions/question.html",
        action="Edit",
        edit_question=edit_a_question,
        form=form,
        question=question,
        title="Edit Question",
    )


@admin.route("/admin/questions/delete/<int:id>", methods=["GET", "DELETE"])
@login_required
def delete_question(id):
    """
    Delete a question from the database
    """

    check_admin()

    question = Question.query.get_or_404(id)

    LOGGER.info(f"Delete question: {question.id}")
    db.session.delete(question)
    db.session.commit()
    flash("You have successfully deleted the question.")

    # redirect to the question page
    return redirect(url_for("admin.list_questions"))


@admin.route("/admin/users", methods=["GET", "POST"])
@login_required
def list_users():
    """
    List all users
    """

    check_admin()

    LOGGER.info("List all users")
    all_users = User.query.all()
    return render_template("admin/users/users.html", users=all_users, title="List Users")


@admin.route("/admin/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_users(id):
    """
    Edit a user
    """

    check_admin()

    edit_a_user = False

    user = User.query.get_or_404(id)

    LOGGER.info(f"Edit user: {user.fullname}")
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.fullname = form.fullname.data
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = True if form.is_admin.data == "True" else False

        try:
            # edit user in the database
            db.session.commit()
            flash("You have successfully edited the user.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this user couldn't be edited. Check each item and try again")

        # redirect to the users page
        return redirect(url_for("admin.list_users"))

    form.fullname.data = user.fullname
    form.username.data = user.username
    form.email.data = user.email
    form.is_admin.data = str(user.is_admin)
    return render_template(
        "admin/users/user.html",
        action="Edit",
        edit_user=edit_a_user,
        form=form,
        user=user,
        title="Edit User",
    )
