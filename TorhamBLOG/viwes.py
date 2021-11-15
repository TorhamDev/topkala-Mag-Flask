from flask import Flask , request , session , make_response, redirect
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy.orm import query
from sqlalchemy.sql.elements import Label
from TorhamBLOG import app
from TorhamBLOG.models import articles ,USER
from TorhamBLOG import db
import os
import random
from datetime import datetime, timedelta


app.secret_key = "1214342212"
app.permanent_session_lifetime = timedelta(hours=3)

#set path user articles for save title photo articls
uploads_path = os.path.join("./TorhamBLOG/static/img/user_photo/article_title_photo")
os.makedirs(uploads_path, exist_ok=True)

### set Home page
@app.route("/")
def home():
#### use a random articles for 4 block top in title index page
    # sum all articles
    article_sum=[]
    # query in datbase for get all article
    nambers= articles.query.all()
    usage_articles = []
    for i in range(0,99999999):
        random_articles = random.randrange(1,len(nambers))
        if len(usage_articles) == 4:
            break
        if random_articles not in usage_articles:
            usage_articles.append(random_articles)

    article_1 = articles.query.filter_by(id=usage_articles[0])
    article_2 = articles.query.filter_by(id=usage_articles[1])
    article_3 = articles.query.filter_by(id=usage_articles[2])
    article_4 = articles.query.filter_by(id=usage_articles[3])
    print("********** " , usage_articles[1])
    sum_articles = len(nambers)
    # return f'{sum_articles}'
    sum_articles = int(sum_articles)
    article_small_1 = articles.query.filter_by(id = sum_articles)
    article_small_2 = articles.query.filter_by(id = sum_articles-1)
    article_small_3 = articles.query.filter_by(id = sum_articles-2)
    article_small_4 = articles.query.filter_by(id = sum_articles-3)

    return render_template("index.html",article_1 = article_1 , article_2 = article_2,
    article_3 = article_3 , article_4 = article_4,
    article_small_1 = article_small_1 , article_small_2 = article_small_2 , article_small_3 = article_small_3 , article_small_4 = article_small_4)









@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/search-results")
def search_results():
    return render_template("search-results.html")


@app.route("/single-post/<id>")
def single_spost(id):

    id = str(f"{id}")
    title = articles.query.filter_by(title=id)
    photo_title = ''
    for photo in title:
        photo_title = photo.photo_title_name


    valid_title  = ''
    for t in title:
        valid_title = t.title

    if valid_title == id:
        return render_template("single-post.html" , article_info=title , photo_in_title=photo_title)

    if valid_title != id :
        return render_template("404.html")




@app.route("/addarticle", methods=["POST"])
def addarticle():
    if not session.get("user_email"):
        return render_template("login.html")
    else:
        athoder_name = request.form["athoder_name"]
        text_title = request.form["text_title"]
        text_tag = request.form["text_tag"]
        if text_tag == 'none' or text_tag == "NONE":
            return "sorry your tag not valid"
        article_text = request.form["text_editor1"]
        photo_title = request.files["photo_title"]
        char="qwertyuioplkjhgfdsazxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM"
        char_set = ''
        now = datetime.now()
        time_now = now.strftime("%D")
        for i in range(0,70):
            str_random = random.randrange(0,62)
            char_set += char[str_random]

        try:
            information= articles (text=article_text,name=athoder_name,title=text_title,article_tag=text_tag,photo_title_name=f"{char_set}.png",publish_time = time_now)
            db.session.add(information)
            db.session.commit()
            goal_path = os.path.join(uploads_path, f"{char_set}.png")
            photo_title.save(goal_path)
            return "saved your article"
        except Exception as ex:
            return f"ERROR <br> {ex}"



@app.route("/edit_article", methods=["POST"])
def edit_article():
    for_edit = request.form["for_edit"]
    for_edit = int(for_edit) - 121
    article_for_edit=articles.query.filter_by(id=for_edit).first()
    return render_template("/admin_page/forms/editors_for_edit.html",articl_edit=article_for_edit)






@app.route("/EDITarticle", methods=["POST"])
def EDITarticle():
    article_namber = request.form["article_namber"]
    athoder_name = request.form["athoder_name"]
    text_title = request.form["text_title"]
    text_tag = request.form["text_tag"]
    if text_tag == 'none' or text_tag == "NONE":
        return "sorry your tag not valid"
    article_text = request.form["text_editor1"]
    photo_title = request.files["photo_title"]
    char_set = photo_title

    try:
        for_delet = article_namber
        for_delet = int(for_delet) - 453
        article_for_delet=articles.query.filter_by(id=for_delet).first()
        information= articles (text=article_text,name=athoder_name,title=text_title,article_tag=text_tag,photo_title_name=f"{char_set}")
        db.session.add(information)
        db.session.delete(article_for_delet)
        db.session.commit()
        goal_path = os.path.join(uploads_path, f"{char_set}.png")
        photo_title.save(goal_path)
        return "edit your article"
    except Exception as ex:
        return f"ERROR <br> {ex}"







@app.route("/delet_article",methods=["POST"])
def delet_article():
    if not session.get("user_email"):
        return render_template("login.html")
    else:
        try:
            for_delet = request.form["for_delet"]
            for_delet = int(for_delet) - 87
            article_for_delet=articles.query.filter_by(id=for_delet).first()
            db.session.delete(article_for_delet)
            db.session.commit()
            return str(f"dleted {article_for_delet}")
        except Exception as ex:
            return f"اوه به ارور خوردیم <br><br>{ex}"


@app.route("/register")
def register():
    return render_template("register.html")
   
###########################
# start admin page config #
###########################
@app.route("/admin")
def admin_page():
    if session.get("user_email"):
        return render_template("admin_index.html")
    else:
        return render_template("login.html")


######### charts --->
@app.route("/chartjs")
def admin_chartjs():
    if not session.get("user_email"):
        return render_template("login.html")
    else:    
        return render_template("/admin_page/charts/chartjs.html")


@app.route("/flot")
def admin_flot():
    if not session.get("user_email"):
        return render_template("login.html")
    else:    
        return render_template("/admin_page/charts/flot.html")



@app.route("/inline")
def admin_inline():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/charts/inline.html")


@app.route("/morris")
def admin_morris():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/charts/morris.html")


######## examples --->
@app.route("/404")
def admin_404():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/404.html")

@app.route("/500")
def admin_500():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/500.html")


@app.route("/blank")
def admin_blank():
    if not session.get("user_email"):
        
        return render_template("login.html")
    else: 
        submit_articles = articles.query.all()
        return render_template("/admin_page/examples/blank.html",all_article=submit_articles)



@app.route("/invoice-print")
def admin_invoice_print():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/invoice-print.html")


@app.route("/invoice")
def admin_invoice():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/invoice.html")


@app.route("/lockscreen")
def admin_lockscreen():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/lockscreen.html")


@app.route("/pace")
def admin_pace():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/pace.html")

@app.route("/profile")
def admin_profile():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/profile.html")

@app.route("/registr_admin")
def admin_registr():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/examples/registr.html")
######## forms --->
@app.route("/advanced")
def admin_advanced():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/forms/advanced.html")

@app.route("/editors")
def admin_editors():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/forms/editors.html")

@app.route("/general")
def admin_general():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/forms/general.html")

######## layout --->
@app.route("/top-nav")
def layout_top_nav():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/layout/top-nav.html")

@app.route("/fixed")
def admin_fixed():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/layout/fixed.html")


@app.route("/collapsed-sidebar")
def admin_collapsed_sidebar():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/layout/collapsed-sidebar.html")


@app.route("/boxed")
def admin_boxed():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/layout/boxed.html")

####### mailbox --->

@app.route("/compose")
def admin_compose():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/mailbox/compose.html")


@app.route("/mailbox")
def admin_mailbox():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/mailbox/mailbox.html")

@app.route("/read-mail")
def admin_read_mail():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/mailbox/read-mail.html")

####### tables --->
@app.route("/data")
def admin_data():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/tables/data.html")

@app.route("/sipmle")
def admin_simple():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/tables/simple.html")

###### UI --->
@app.route("/buttons")
def admin_buttons():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/UI/buttons.html")

@app.route("/UIgeneral")
def admin_UIgeneral():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/UI/general.html")


@app.route("/icons")
def admin_icons():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/UI/icons.html")


@app.route("/modals")
def admin_modals():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/UI/modals.html")

@app.route("/sliders")
def admin_sliders():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/UI/sliders.html")


@app.route("/timeline")
def admin_timeline():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/UI/timeline.html")

####### admin-page --->

@app.route("/calendar")
def admin_calendar():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/calendar.html")


@app.route("/widgets")
def admin_widgets():
    if not session.get("user_email"):
        return render_template("login.html")
    else: 
        return render_template("/admin_page/widgets.html")
############################
# finish admin page config #
############################




@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/crate_user", methods=["POST"])
def crate_user():
    email = request.form["email"]
    user_name = request.form["user_name"]
    password = request.form["password"]
    re_password = request.form["re_password"]
    try:
        response = make_response(redirect(url_for("home")))

        if password != re_password:
            return render_template("register.html" , ststus = False)
        
        session["user_email"] = email
        session.permanent = True

        return response

    except Exception as ex:
        return f"sorry not successful the error was  : {ex} "






@app.route("/admin_index_2")
def admin_page_2():
    return render_template("admin_index2.html")




@app.errorhandler(404)
def error_404(error):
    return render_template("404.html")
