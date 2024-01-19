from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_dance.contrib.github import make_github_blueprint, github



from random import randint
from jdatetime import datetime

from flask_sqlalchemy import SQLAlchemy
from database import db  

from config import *
from models import * 

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

app.config["GITHUB_OAUTH_CLIENT_ID"] = GITHUB_OAUTH_CLIENT_ID
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = GITHUB_OAUTH_CLIENT_SECRET




db.init_app(app)



def currentDate():
    return datetime.now().strftime("14%y/%m/%d")

def currentTime(seconds=False):
    if not seconds:
        return datetime.now().strftime("%H:%M")
    else:
        return datetime.now().strftime("%H:%M:%S")


def deletePost(postID):
    post = Post.query.get(postID)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect("/")


github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login-github")

@app.route('/')
def index():
    db.create_all()
    if "userName" in session: 
        posts = Post.query.all()      
        Tpost = Post.query.order_by(Post.views.desc()).all()
        rdf_data = {
        "@context": "http://schema.org",
        "@type": "WebPage",
        "name": "Home Page",
        "description": "Welcome to Our Website",
        "url": f"{request.url}",
        "keywords": "home, index, main, website",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": f"{url_for('index')}",
                        "name": "Home"
                    }
                }
            ]
        }
    }
        return render_template('index.html', posts=posts,Tpost = Tpost,rdf_data=rdf_data)
    else:
        return redirect("/welcome")

@app.route('/welcome')
def welcome():
    rdf_data = {
        "@context": "http://schema.org",
        "@type": "WebPage",
        "name": "Welcome to Our Website",
        "description": "Explore and Discover",
        "url": f"{request.url}",
        "keywords": "welcome, introduction, explore, discover",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": f"{url_for('index')}",
                        "name": "Home"
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": f"{url_for('welcome')}",
                        "name": "Welcome"
                    }
                }
            ]
        }
    }
    return render_template('welcome.html',rdf_data=rdf_data)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "userName" in session:
        flash("شما قبلا وارد شده اید", "error")
        return redirect("/")
    else:        
        if request.method == "POST":   
            username = request.form['userName']
            email = request.form['email']
            password = request.form['password']
            res=User.query.filter_by(userName=username.lower()).first()
            if res:
                flash("این نام کاربری قبلاً استفاده شده است", "error")
                return render_template("signup.html")
            res=User.query.filter_by(email=email).first()
            if res:
                return render_template("signup.html", error="این ایمیل قبلاً استفاده شده است.")         
            newUser = User(
                userName=username.lower(),
                email=email,
                password=password, 
                role="user"
                )
            db.session.add(newUser)
            db.session.commit()
            session["userName"] = username
            flash(f"ثبت نام با موفقیت انجام شد {username} عزیز خوشامدید:)", "success")
            return redirect(f"/user/{username}")
        
        rdf_data = {
        "@context": "http://schema.org",
        "@type": "WebPage",
        "name": "signup Page",
        "description": "signup to Website",
        "url": f"{request.url}",
        "keywords": "signup, authentication, user signup",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": f"{url_for('index')}",
                        "name": "Home"
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": f"{url_for('signup')}",
                        "name": "signup"
                    }
                }
            ]
        }
    }
        return render_template("signup.html", hideSignUp=True,rdf_data=rdf_data)

@app.route("/login-github")
def login_github_acc():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    session["userName"] = resp.json()["login"]
    flash("ورود موفقیت آمیز بود خوشامدید", "success")
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "userName" in session:
        flash("شما قبلا وارد شده اید", "error")
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            username = request.form['userName']
            password = request.form['password']
            user = User.query.filter_by(userName=username.lower()).first()
            if user and user.password == password:
                session["userName"] = username.lower()
                flash("ورود موفقیت آمیز بود خوشامدید", "success")
                return redirect(url_for('index'))
            else:
                flash("شناسه کاربری یا رمز عبور نامعتبر است", "error")
                return redirect('login')
            
        rdf_data = {
        "@context": "http://schema.org",
        "@type": "WebPage",
        "name": "Login Page",
        "description": "Login to Website",
        "url": f"{request.url}",
        "keywords": "login, authentication, user login",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": f"{url_for('index')}",
                        "name": "Home"
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": f"{url_for('login')}",
                        "name": "Login"
                    }
                }
            ]
        }
    }
        return render_template("login.html",rdf_data=rdf_data)


@app.route('/logout')
def logout():
    if "userName" in session:
        flash("شما از حساب خود خارج شدید", "success")
        session.clear()
        return redirect("/")
    else:
        flash("شما هنوز وارد اکانت نشدید", "error")
        return redirect(url_for("login"))

@app.route("/user/<userName>")
def user(userName):
    user = User.query.filter_by(userName=userName).first()
    
    if user:
        try:
            posts = Post.query.filter_by(author=str(user.userName))
            views = sum(post.views for post in posts)
        except:
            posts = False
            views = 0
        
        rdf_data = {
        "@context": "http://schema.org",
        "@type": "Person",
        "name": f"{userName}",
        "role": f"{user.role}",
        "url": f"{request.url}",
        "email": f"{user.email}",
        "memberOf": {
            "@type": "Organization",
            "name": "website"
        }
        }

        return render_template(
            "user.html",
            user=user,
            views=views,
            posts=posts,
            rdf_data=rdf_data
        )
    else:
        return render_template("404.html")

@app.route("/createpost", methods=["GET", "POST"])
def createPost():
    if "userName" in session:
        user = User.query.filter_by(userName=session["userName"]).first()
        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            if postContent == "":
                flash("محتوای مطلب نمی تواند خالی باشد", "error")
            else:
                newPost = Post(
                    title = postTitle,
                    tags = postTags,
                    content = postContent,
                    author = session["userName"],
                    date = currentDate(),
                    time = currentTime(),
                    views = 0,
                    lastEditDate = currentDate(),
                    lastEditTime = currentTime()
                )
                db.session.add(newPost)
                db.session.commit()
                flash("مطلب شما اضافه شد", "success")
                return redirect(f"/post/{newPost.id}")
        
        rdf_data = {
        "@context": "http://schema.org",
        "@type": "WebPage",
        "name": "Create new Post",
        "description": "Create a new post on our website",
        "url": f"{request.url}",
        "keywords": "create post, new post, blog, article"
        }

        return render_template("createPost.html",rdf_data=rdf_data)
    else:
        flash("برای اضافه کردن مطلب ابتدا وارد اکانت خود شوید", "error")
        return redirect(url_for("login"))


@app.route("/editpost/<int:postID>", methods=["GET", "POST"])
def editPost(postID):
    if "userName" in session:
        post = Post.query.get(postID)
        if post:
            if post.author == session["userName"]:
                if request.method == "POST":
                    postTitle = request.form["postTitle"]
                    postTags = request.form["postTags"]
                    postContent = request.form["postContent"]
                    if postContent == "":
                        flash("محتوای مطلب نمی تواند خالی باشد!", "error")
                    else:
                        post.title = postTitle
                        post.tags = postTags
                        post.content = postContent
                        post.lastEditDate = currentDate()
                        post.lastEditTime = currentTime()
                        db.session.commit()
                        flash("مطلب شما ویرایش شد", "success")
                        return redirect(f"/post/{post.id}")
                
                rdf_data = {
                    "@context": "http://schema.org",
                    "@type": "WebPage",
                    "name": "Edit Post",
                    "description": "Edit an existing post on our website",
                    "url": f"{request.url}",
                    "keywords": "edit post, update post, blog, article"
                }
                
                return render_template(
                    "editPost.html",
                    post=post,
                    rdf_data=rdf_data
                )
            else:
                flash("نویسنده این مطلب شما نیستید!", "error")
                return redirect("/")
        else:
            return render_template("404.html")
    else:
        flash("برای ویرایش مطلب ابتدا وارد اکانت شوید", "error")
        return redirect(url_for("login"))


@app.route("/post/<int:postID>", methods=["GET", "POST"])
def post(postID):
    post = Post.query.get(postID)
    if post:
        post.views +=1
        db.session.commit()
        if request.method == "POST":
            if "postDeleteButton" in request.form:
                deletePost(postID)
                return redirect(f"/")
        
        rdf_data = {
        "@context": "http://schema.org",
        "@type": "Article",
        "headline": f"{post.title}",
        "description": f"{post.content}",
        "url": f"{request.url}",
        "datePublished": f"{post.date}",
        "dateModified": f"{post.lastEditDate}",
        "author": {
            "@type": "Person",
            "name": f"{post.author}"
        },
        "articleBody": f"{post.content}",
        "publisher": {
            "@type": "Organization",
            "name": "website"
        }
    }
        
        return render_template(
            "post.html",
            post=post,
            rdf_data=rdf_data
        )
    else:
        return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)
