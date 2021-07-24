from flask import *
from flask_sqlalchemy import *
from models.Users import User
from models.Questions import Question
from models.Answers import Answer
from config import *

@app.route('/upvote/question/<int:q_id>/<int:u_id>')
def upvote_q(q_id, u_id):
    if not("logged_in" in session and session["logged_in"]):
        flash("You need to log in first!")
        return redirect(url_for('login'))

    qs = Question.query.filter_by(q_id=q_id).first()
    u = User.query.filter_by(u_id=qs.author_u_id).first()
    u.reputation += 10

    if qs.upvoters:
        if "+" + str(u_id) + " " in qs.upvoters:
            flash("You cannot upvote/downvote twice!")
            return redirect(url_for('question',q_id=q_id))
        elif "-" + str(u_id) + " " in qs.upvoters:
            qs.upvoters = qs.upvoters.replace("-" + str(u_id) + " ", "")
        else:
            qs.upvoters += "+" + str(u_id) + " "
    else:
        qs.upvoters = "+" + str(u_id) + " "
    qs.upvotes += 1
    db.session.commit()
    db.session.close()
    return redirect(url_for('question',q_id=q_id))

@app.route('/downvote/question/<int:q_id>/<int:u_id>')
def downvote_q(q_id, u_id):
    if not("logged_in" in session and session["logged_in"]):
        flash("You need to log in first!")
        return redirect(url_for('login'))

    qs = Question.query.filter_by(q_id=q_id).first()
    u = User.query.filter_by(u_id=qs.author_u_id).first()
    u.reputation -= 5

    if qs.upvoters:
        if "-" + str(u_id) + " " in qs.upvoters:
            flash("You cannot upvote/downvote twice!")
            return redirect(url_for('question',q_id=q_id))
        elif "+" + str(u_id) + " " in qs.upvoters:
            qs.upvoters = qs.upvoters.replace("+" + str(u_id) + " ", "")
        else:
            qs.upvoters += "-" + str(u_id) + " "
    else:
        qs.upvoters = "-" + str(u_id) + " "
    qs.upvotes -= 1
    db.session.commit()
    db.session.close()
    return redirect(url_for('question',q_id=q_id))

@app.route('/upvote/answer/<int:a_id>/<int:u_id>')
def upvote_a(a_id, u_id):
    if not("logged_in" in session and session["logged_in"]):
        flash("You need to log in first!")
        return redirect(url_for('login'))

    ans = Answer.query.filter_by(a_id=a_id).first()
    u = User.query.filter_by(u_id=ans.author_u_id).first()
    u.reputation += 10
    q_id = ans.q_id

    if ans.upvoters:
        if "+" + str(u_id) + " " in ans.upvoters:
            flash("You cannot upvote/downvote twice!")
            return redirect(url_for('question',q_id=q_id))
        elif "-" + str(u_id) + " " in ans.upvoters:
            ans.upvoters = ans.upvoters.replace("-" + str(u_id) + " ", "")
        else:
            ans.upvoters += "+" + str(u_id) + " "
    else:
        ans.upvoters = "+" + str(u_id) + " "
    ans.upvotes += 1
    db.session.commit()
    db.session.close()
    return redirect(url_for('question',q_id=q_id))


@app.route('/downvote/answer/<int:a_id>/<int:u_id>')
def downvote_a(a_id, u_id):
    if not("logged_in" in session and session["logged_in"]):
        flash("You need to log in first!")
        return redirect(url_for('login'))

    ans = Answer.query.filter_by(a_id=a_id).first()
    u = User.query.filter_by(u_id=ans.author_u_id).first()
    u.reputation -= 5
    q_id = ans.q_id

    if ans.upvoters:
        if "-" + str(u_id) + " " in ans.upvoters:
            flash("You cannot upvote/downvote twice!")
            return redirect(url_for('question',q_id=q_id))
        elif "+" + str(u_id) + " " in ans.upvoters:
            ans.upvoters = ans.upvoters.replace("+" + str(u_id) + " ", "")
        else:
            ans.upvoters += "-" + str(u_id) + " "
    else:
        ans.upvoters = "-" + str(u_id) + " "
    ans.upvotes -= 1
    db.session.commit()
    db.session.close()
    return redirect(url_for('question',q_id=q_id))
