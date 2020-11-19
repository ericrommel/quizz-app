import random

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from . import user
from .forms import UserForm, SetForAQuizForm, SolveQuizForm
from .. import db, LOGGER
from ..models import User, Question, Quiz

result = 0


@user.route("/users", methods=["GET", "POST"])
@login_required
def user_details():
    """
    Show the user detail
    """

    LOGGER.info("Show user details")
    user_obj = User.query.get_or_404(current_user.id)

    return render_template("user/users.html", user=user_obj, title="User Details")


@user.route("/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    """
    Edit a user
    """

    LOGGER.info("Edit user details")

    edit_a_user = True
    user_obj = User.query.get_or_404(id)
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
        return redirect(url_for("user.solve_a_quiz", id=quiz.id, question_id=0))

    return render_template("quiz/set-quiz.html", form=form, title="Choose your challenge")


@user.route("/users/quizzes/<int:id>/question/<int:question_id>", methods=["GET", "POST"])
@login_required
def solve_a_quiz(id, question_id):
    """
    Generate a quiz to solve
    """

    global result

    LOGGER.info("Solve a quiz")

    quiz_obj: Quiz = Quiz.query.get_or_404(id)

    questions: list = quiz_obj.questions

    q = question_id

    if len(questions) == q:
        result = round(float(result / q), 2)
        return redirect(url_for("user.quiz_result", user_id=id, final_result=result))

    form = SolveQuizForm()
    choices = [
        questions[q].correct_answer,
        questions[q].false_answer_1,
        questions[q].false_answer_2,
        questions[q].false_answer_3,
    ]

    random.shuffle(choices)

    form.question.label = questions[q].description
    form.question.choices = choices

    if form.validate_on_submit():
        LOGGER.info("Check and save the answer by the user")
        if form.question.data.strip().lower() == questions[q].correct_answer.strip().lower():
            result += 1 + questions[q].level

        q += 1
        return redirect(url_for("user.solve_a_quiz", id=id, question_id=q))

    return render_template("quiz/quiz.html", question=questions[q], form=form, title=f"Question {q+1}")


@user.route("/users/<int:user_id>/results/", methods=["GET", "POST"])
@login_required
def quiz_result(user_id, final_result):
    """
    Generate the quiz result from the user
    """

    global result
    LOGGER.debug(f"User: {user_id} - Result: {result}")

    result = 0

    LOGGER.debug(f"Result: {result}")
    return render_template("home/index.html")
