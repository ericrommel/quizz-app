import random

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, desc

from . import user
from .forms import UserForm, SetForAQuizForm, SolveQuizForm
from .. import db, LOGGER
from ..models import User, Question, Quiz, Score

results: dict = {"passes": [], "points": 0.0}


def set_results(values: dict) -> None:
    results["passes"] = values.get("passes")
    results["points"] = values.get("points")


def get_results() -> dict:
    return results


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
def edit_users(id):
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

    form = SetForAQuizForm()

    query: Question = Question.query.with_entities(Question.subject).distinct()
    if not query.all():
        LOGGER.info("There is no question yet")
        return render_template("quiz/set-quiz.html", empty=True, form=form, title="Choose your challenge")

    LOGGER.info("Choose the number of questions and the subject")

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
        return redirect(url_for("user.solve_a_new_quiz", user_id=quiz.user_id, quiz_id=quiz.id, question_id=0))

    return render_template("quiz/set-quiz.html", form=form, title="Choose your challenge")


@user.route("/users/<int:user_id>/quizzes/<int:quiz_id>/question/<int:question_id>", methods=["GET", "POST"])
@login_required
def solve_a_new_quiz(user_id, quiz_id, question_id):
    """
    Generate a quiz to solve
    """

    values: dict = get_results()

    LOGGER.info("Solve a quiz")

    quiz_obj: Quiz = Quiz.query.get_or_404(quiz_id)

    questions: list = quiz_obj.questions

    form = SolveQuizForm()

    if len(questions) == question_id:
        values["points"] = round(values["points"] / float(len(questions)), 2)
        set_results(values)
        return redirect(url_for("user.quiz_result", user_id=quiz_obj.user_id, quiz_id=quiz_obj.id))

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
            values["points"] += (1 + questions[question_id].level) * int(form.times_up.data)
            values["passes"].append(form.question.data.strip())
            set_results(values)

        question_id += 1
        return redirect(url_for("user.solve_a_new_quiz", user_id=user_id, quiz_id=quiz_id, question_id=question_id))

    return render_template(
        "quiz/quiz.html",
        question=questions[question_id],
        quiz_id=quiz_obj.id,
        user_id=quiz_obj.user_id,
        question_id=question_id,
        form=form,
        title=f"Question {question_id+1}",
    )


@user.route("/users/<int:user_id>/quizzes/<int:quiz_id>/results", methods=["GET", "POST"])
@login_required
def quiz_result(user_id, quiz_id):
    """
    Generate the quiz result from the user
    """

    values: dict = get_results()

    quiz_obj: Quiz = Quiz.query.get_or_404(quiz_id)
    total_questions: int = len(quiz_obj.questions)
    correct_questions: int = len(values.get("passes"))
    points: float = values.get("points")
    level_achieved: float = (correct_questions * 10) / total_questions
    expertise_level = ""
    if 0 <= level_achieved <= 2:
        expertise_level = (
            "You are Clueless: Don’t be discouraged!\nLearn some more about this topic, and come back" " to try again!"
        )
    elif 2 < level_achieved <= 5:
        expertise_level = (
            "You are Beginner: This is the level most players end up with after answering this quiz for"
            " the first time.\nLearn some more about this topic and come back to try again!"
        )
    elif 5 < level_achieved <= 8:
        expertise_level = (
            "You are Confident: This is the level players are getting pro!\nContinue your progress and" " rock it!"
        )
    else:
        expertise_level = "Expert: This is the highest level achievable!\nThanks for being awesome as you are!"

    score = Score(user_id=user_id, passes=values.get("passes"), points=values.get("points"))

    try:
        # add score to the database
        db.session.add(score)
        db.session.commit()
        flash(f"You have successfully added the score for {user_id}.")
    except Exception as error:
        LOGGER.error(f"Exception: {error}")
        flash("Error: There was an error and this score couldn't be added.")

    values = {"passes": [], "points": 0.0}
    set_results(values)

    return render_template(
        "quiz/result.html",
        user=user_id,
        total=total_questions,
        correct=correct_questions,
        points=points,
        expertise_level=expertise_level,
    )


@user.route("/users/<int:user_id>/dashboard", methods=["GET", "POST"])
@login_required
def dashboard(user_id):
    """
    Generate the user's dashboard
    """

    user_obj: User = User.query.get_or_404(user_id)

    LOGGER.info("Get the the better result made by the user")
    user_score: Score = (
        db.session.query(Score).filter(Score.user_id == user_obj.id).order_by(desc(Score.points)).limit(1)
    )

    LOGGER.info("Get the 10 highest positions in the ranking")
    score_list = (
        db.session.query(User.username, Score.points)
        .join(Score, User.id == Score.user_id)
        .order_by(desc(Score.points))
        .limit(10)
    )

    if not user_score.all():
        return render_template(
            "home/dashboard.html",
            no_result_yet=True,
            first_10=score_list.all(),
            title="Dashboard",
        )

    LOGGER.info("Get the user position in the general ranking")
    sub = db.session.query(Score.user_id, func.row_number().over(order_by=desc(Score.points)).label("pos")).subquery()
    user_position = [position for position in db.session.query(sub.c.pos).filter(sub.c.user_id == user_id).first()]

    return render_template(
        "home/dashboard.html",
        no_result_yet=False,
        user_score=user_score.all()[0].points,
        user_position=user_position[0],
        first_10=score_list.all(),
        title="Dashboard",
    )
