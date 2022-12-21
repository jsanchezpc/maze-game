from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "xseed"

# envia el template index.html, el contador de los pasos y el background
@app.route("/")
def home():
    if "steps" not in session:
        # background images
        session["forward_bg"] = "/static/img/forward3D.png"
        session["all_bg"] = "/static/img/all3D.png"
        session["right_bg"] = "/static/img/right3D.png"
        session["left_bg"] = "/static/img/left3D.png"
        session["none_bg"] = "/static/img/none3D.png"
        session["exit_bg"] = "/static/img/exit3D.png"
        session["steps"] = 10
        session["path"] = []
        session['img_map']=[
            [0, 0,  session["none_bg"], session["all_bg"],  session["exit_bg"], 0],
            [0, 0,  session["none_bg"], session["forward_bg"],  session["none_bg"], 0],
            [0, session["none_bg"], session["all_bg"],  session["forward_bg"],  session["none_bg"], 0],
            [session["none_bg"],    session["left_bg"], session["forward_bg"],  session["all_bg"],  session["left_bg"], session["none_bg"]],
            [0, 0,    session["none_bg"], session["forward_bg"],   session["forward_bg"],  0]
        ]
        session['posZ']=4
        session['posX']=3
        session["position"]=session["img_map"][int(session["posZ"])][int(session["posX"])]
        session['bg']=session["position"]
    
    return render_template('index.html',  bg=session['bg'], steps=session["steps"], path=session["path"])

@app.route("/test")
def test():
    return session["bg"]

# lee la dirección elegida del form
@app.route("/move", methods=['POST', 'GET'])
def move():
    direction = request.form["direction"]
    while session["steps"] > 0:
        if direction == "FORWARD":
            if(session["posZ"] <= 4 and session["posZ"] >= 0):
                session["posZ"] -= 1
                session["position"]=session["img_map"][session["posZ"]][session["posX"]]
                session["path"].append([session['posZ'],session['posX']])
                session['bg']=session["position"]
                session["steps"] -= 1
                return render_template('index.html',  bg=session['bg'], steps=session["steps"], path=session["path"])
            else:
                return redirect("/error")
        if direction == "BACK":
            if(session["posZ"] < 4 and session["posZ"] >= 0):
                session["posZ"] += 1
                session["position"]=session["img_map"][session["posZ"]][session["posX"]]
                session["path"].append([session['posZ'],session['posX']])
                session['bg']=session["position"]
                session["steps"] -= 1
                print(session["position"])
                return render_template('index.html',  bg=session['bg'], steps=session["steps"], path=session["path"])
            else:
                return redirect("/error")
        if direction == "LEFT":
            if(session["posX"] < 5 and session["posX"] >= 0):
                session["posX"] -= 1
                session["position"]=session["img_map"][session["posZ"]][session["posX"]]
                session["path"].append([session['posZ'],session['posX']])
                session['bg']=session["position"]
                session["steps"] -= 1
                print(session["position"])
                return render_template('index.html',  bg=session['bg'], steps=session["steps"], path=session["path"])
            else:
                return redirect("/error")
        if direction == "RIGHT":
            if(session["posX"] < 5 and session["posX"] >= 0):
                session["posX"] += 1
                session["position"]=session["img_map"][session["posZ"]][session["posX"]]
                session["path"].append([session['posZ'],session['posX']])
                session['bg']=session["position"]
                session["steps"] -= 1
                print(session["position"])
                return render_template('index.html',  bg=session['bg'], steps=session["steps"], path=session["path"])
            else:
                return redirect("/error")
        return redirect("/")
    else: 
        return redirect("gameover")
    
@app.route('/gameover')
def gameover():
    return render_template('gameover.html')

@app.route('/error')
def error():
    return render_template('error.html')
    
@app.route('/reset')
def reset():
    print("Current game is ending.")
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)