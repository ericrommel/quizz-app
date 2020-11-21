import random

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from . import user
from .forms import UserForm, SetForAQuizForm, SolveQuizForm
from .. import db, LOGGER
from ..models import User, Question, Quiz

results: dict = {"fails": [], "points": 0.0}


@user.route("/users", methods=["GET", "POST"])
@login_required
def user_details():
    """
    Show the user detail
    """

    LOGGER.info("Show user details")
    user_obj: User = User.query.get_or_404(current_user.id)

    return render_template("user/users.html", user=user_obj, title="User Details")


@user.route("/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    """
    Edit a user
    """

    LOGGER.info("Edit user details")

    edit_a_user = True
    user_obj: User = User.query.get_or_404(id)
    form = UserForm(obj=user_obj)

    # ToDo: Implement change Password
    if form.validate_on_submit():
        user_obj.fullname = form.fullname.data
        user_obj.username = form.username.data
        user_obj.email = form.email.data

        try:
            # edit user in the database
            db.session.commit()
            flash("You have successfully edited the user.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this user cannot be edited. Check each item and try again")

        # redirect to the user page
        return redirect(url_for("user.user_details"))

    form.fullname.data = user_obj.fullname
    form.username.data = user_obj.username
    form.email.data = user_obj.email

    return render_template(
        "user/user.html",
        action="Edit",
        form=form,
        user=user_obj,
        title="Edit User",
    )


@user.route("/users/quizzes", methods=["GET", "POST"])
@login_required
def generate_a_quiz():
    """
    Generate a quiz to solve
    """

    LOGGER.info("Choose the number of questions and the subject")

    form = SetForAQuizForm()

    query: Question = Question.query.with_entities(Question.subject).distinct()
    subjects = [row.subject for row in query.all()]

    form.subject.choices = subjects

    if form.validate_on_submit():
        LOGGER.info("Quiz form has been validated. Generate a quiz")

        query: Question = (
            db.session.query(Question)
            .filter(Question.subject == form.subject.data)
            .order_by(func.random())
            .limit(form.number_of_questions.data)
        )

        quiz: Quiz = Quiz(questions=query.all(), user_id=current_user.id)
        try:
            # add quiz to the database
            db.session.add(quiz)
            db.session.commit()
            flash(f"You have successfully added a new quiz for the user {current_user.id}.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this question couldn't be added. Check each item and try again")

        # redirect to questions page
        return redirect(url_for("user.solve_a_new_quiz", quiz_id=quiz.id, question_id=0))

    return render_template("quiz/set-quiz.html", form=form, title="Choose your challenge")


@user.route("/users/quizzes/<int:quiz_id>/question/<int:question_id>", methods=["GET", "POST"])
@login_required
def solve_a_new_quiz(quiz_id, question_id):
    """
    Generate a quiz to solve
    """

    global results

    LOGGER.info("Solve a quiz")

    quiz_obj: Quiz = Quiz.query.get_or_404(quiz_id)

    questions: list = quiz_obj.questions

    form = SolveQuizForm()

    if len(questions) == question_id:
        results["points"] = round(results["points"] / float(len(questions)), 2)
        return redirect(url_for("user.quiz_result", quiz_id=quiz_id, final_result=results))

    choices = [
        questions[question_id].correct_answer,
        questions[question_id].false_answer_1,
        questions[question_id].false_answer_2,
        questions[question_id].false_answer_3,
    ]

    random.shuffle(choices)

    form.question.label = questions[question_id].description
    form.question.choices = choices

    if form.validate_on_submit():
        LOGGER.info(f"Check and save the answer by the user. Solved in {form.times_up.data}s")
        if form.question.data.strip().lower() == questions[question_id].correct_answer.strip().lower():
            results["points"] += (1 + questions[question_id].level) * int(form.times_up.data)
            results["passes"].append(form.question.data.strip())
            LOGGER.debug(f"Point: {results}")

        question_id += 1
        return redirect(url_for("user.solve_a_new_quiz", quiz_id=quiz_id, question_id=question_id))

    return render_template(
        "quiz/quiz.html",
        question=questions[question_id],
        quiz_id=quiz_id,
        question_id=question_id,
        form=form,
        title=f"Question {question_id+1}",
    )


@user.route("/users/quizzes/quiz_id/results/<float:final_result>", methods=["GET", "POST"])
@login_required
def quiz_result(quiz_id, final_result):
    """
    Generate the quiz result from the user
    """

    global results

    quiz_obj: Quiz = Quiz.query.get_or_404(quiz_id)

    LOGGER.debug(f"User: {quiz_obj.user_id} - Result: {final_result}")

    LOGGER.info("Choose the number of questions and the subject")

    form = SetForAQuizForm()

    query = Question.query.with_entities(Question.subject).distinct()
    subjects = [row.subject for row in query.all()]

    form.subject.choices = subjects

    if form.validate_on_submit():
        LOGGER.info("Quiz form has been validated. Generate a quiz")

        query = (
            db.session.query(Question)
            .filter(Question.subject == form.subject.data)
            .order_by(func.random())
            .limit(form.number_of_questions.data)
        )

        LOGGER.debug(f"QUERY: {query.all()}")
        quiz = Quiz(questions=query.all(), user_id=current_user.id)
        try:
            # add quiz to the database
            db.session.add(quiz)
            db.session.commit()
            flash(f"You have successfully added a new quiz for the user {current_user.id}.")
        except Exception as error:
            LOGGER.error(f"Exception: {error}")
            flash("Error: There was an error and this question couldn't be added. Check each item and try again")

        # redirect to questions page
        return redirect(url_for("user.solve_a_new_quiz", quiz_id=quiz.id, question_id=0))

    results = 0

    LOGGER.debug(f"Result: {final_result}")
    return render_template("home/index.html")
