from flask import Flask, render_template, url_for, request, session
import random
import csvReader
import csvReaderIrregular

app = Flask(__name__)
app.secret_key = '4e074c033785b0ec6cc2ce3a7b4efc1a2796090ac4de3f9eb123af0adafb7387'


@app.route("/", methods=['GET', 'POST'])
def index():

    listPronouns = ["yo", "tú", "él", "nosotros", "vosotros", "ellos"]

    correspondanceTime = {
        "Conditional": csvReader.Conditional,
        "Futuro": csvReader.Futuro,
        "Presente de indicativo": csvReader.Presente_de_indicativo,
        "Presente de subjonctivo": csvReader.Presente_de_subjonctivo,
        "Pretérito imperfecto de indicativo": csvReader.Preterito_imperfecto_de_indicativo,
        "Pretérito indefinido": csvReader.Preterito_indefinido,
        "Prétero imperfecto de subjonctivo": csvReader.Pretero_imperfecto_de_subjonctivo,
    }

    correspondanceTimeIrregular = {
        "Conditional": csvReaderIrregular.Conditional,
        "Futuro": csvReaderIrregular.Futuro,
        "Presente de indicativo": csvReaderIrregular.Presente_de_indicativo,
        "Presente de subjonctivo": csvReaderIrregular.Presente_de_subjonctivo,
        "Pretérito imperfecto de indicativo": csvReaderIrregular.Preterito_imperfecto_de_indicativo,
        "Pretérito indefinido": csvReaderIrregular.Preterito_indefinido,
        "Prétero imperfecto de subjonctivo": csvReaderIrregular.Pretero_imperfecto_de_subjonctivo,
    }

    reponseUser=""

    if 'time' in session:
        pass

    else:
        session["time"] = "temps"
        session["pronouns"] = "pronoms"
        session["verb"] = 'verbe'

    verif = request.form.get("temps[]")

    if verif == "Futuro" or verif == "Conditional" or verif == "Presente de indicativo" or verif == "Presente de subjonctivo" or verif == "Pretérito imperfecto de indicativo" or verif == "Pretérito indefinido" or verif == "Prétero imperfecto de subjonctivo" :

        session["listActiveTimes"] = request.form.getlist("temps[]")

        session["time"] = random.choice(session["listActiveTimes"])

        session["pronouns"] = random.choice(listPronouns)


    if request.values.get("irreguliers") == "irregulier":

        session["verb"] = csvReaderIrregular.verbChoice()
        session["irregular"] = 6

    elif request.values.get("tous") == "tous":

        aleatoire = random.randint(0,1)
        if aleatoire == 0:
            session["verb"] = csvReaderIrregular.verbChoice()
            session["irregular"] = 6
            session["tous"] = 7

        else:
            session["verb"] = csvReader.verbChoice()
            session["irregular"] = 8
            session["tous"] = 7

    elif request.values.get("reguliers") == "regulier":

        session["verb"] = csvReader.verbChoice()
        session["irregular"] = 8


    if request.form.get("reponse") != None and len(request.form.get("reponse")) >= 0 and session["verb"] != "verbe":

        reponse = request.form.getlist("reponse")
        reponseVerb = reponse[0].lower()

        if session["irregular"] == 6:

            correspondanceVerb = ["dar", "decir", "estar", "haber", "hacer", "ir", "poder", "poner", "querer", "saber", "salir", "ser", "tener", "venir", "ver"]

            correction = correspondanceTimeIrregular[session["time"]]()[listPronouns.index(session['pronouns'])][correspondanceVerb.index(session["verb"])]

            if reponseVerb == correction:
                reponseUser = "✅ Bonne réponse !"

            else:

               reponseUser = "❌ La réponse était: " + str(correction)

            session["verb"] = csvReaderIrregular.verbChoice()

        else:

            termination = str(session["verb"][-2:])

            correspondanceTermination = ["ar", "er", "ir"]

            correction = correspondanceTime[session["time"]]()[listPronouns.index(session['pronouns'])][correspondanceTermination.index(termination)]

            if (reponseVerb == session["verb"][:-2] + correction and session["time"] != "Futuro" and session["time"] != "Conditional") or ((session["time"] == "Futuro" or session["time"] == "Conditional") and reponseVerb == session["verb"] + correction):

                reponseUser = "✅ Bonne réponse !"

            elif (session["time"] == "Futuro" or session["time"] == "Conditional") and reponseVerb != session["verb"] + correction:

                reponseUser = "❌ La réponse était: " + str(session["verb"] + correction)

            else:

                reponseUser = "❌ La réponse était: " + str(session["verb"][:-2] + correction)

            session["verb"] = csvReader.verbChoice()

        if "tous" in session and session["tous"] == 7:

            aleatoire = random.randint(0, 1)
            if aleatoire == 0:
                session["verb"] = csvReaderIrregular.verbChoice()
                session["irregular"] = 6

            else:
                session["verb"] = csvReader.verbChoice()
                session["irregular"] = 8

        session["time"] = random.choice(session["listActiveTimes"])
        session["pronouns"] = random.choice(listPronouns)


    return render_template("home.html", time = session["time"], pronouns = session["pronouns"], verb = session["verb"], reponseUser = reponseUser )


@app.route("/login", methods=['GET', 'POST'])
def login():
    pass

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    pass

@app.route("/newAccount", methods=['GET', 'POST'])
def newAccount():
    pass


if __name__ == "__main__":
    app.run(debug=True)
