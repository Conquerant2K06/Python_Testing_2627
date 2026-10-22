import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    matching_clubs = [club for club in clubs if club['email'] == request.form.get('email')]
    if not matching_clubs:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    
    club = matching_clubs[0]
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('welcome.html', club=club, competitions=competitions, today=today)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_clubs = [c for c in clubs if c['name'] == club]
    found_competitions = [c for c in competitions if c['name'] == competition]
    
    if found_clubs and found_competitions:
        return render_template('booking.html', club=found_clubs[0], competition=found_competitions[0])
    else:
        flash("Something went wrong - please try again")
        return redirect(url_for('index'))

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form.get('competition')][0]
    club = [c for c in clubs if c['name'] == request.form.get('club')][0]
    
    try:
        placesRequired = int(request.form.get('places'))
    except (ValueError, TypeError):
        flash("Veuillez entrer un nombre valide.")
        return redirect(url_for('book', competition=competition['name'], club=club['name'])), 400

    # 1. Vérification de la date de la compétition
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("Cette compétition est déjà terminée, vous ne pouvez plus réserver.")
        return redirect(url_for('book', competition=competition['name'], club=club['name'])), 400

    # 2. Vérification des nombres négatifs ou nuls
    if placesRequired <= 0:
        flash("Le nombre de places doit être supérieur à zéro.")
        return redirect(url_for('book', competition=competition['name'], club=club['name'])), 400

    # 3. Vérification des places disponibles
    available_places = int(competition['numberOfPlaces'])
    if placesRequired > available_places:
        flash("Il n'y a pas assez de places disponibles pour cette compétition.")
        return redirect(url_for('book', competition=competition['name'], club=club['name'])), 400

    # 4. Vérification des points du club
    club_points = int(club['points'])
    if placesRequired > club_points:
        flash("Vous n'avez pas assez de points pour réserver autant de places.")
        return redirect(url_for('book', competition=competition['name'], club=club['name'])), 400

    # 5. Limite de 12 places
    if placesRequired > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places par compétition.")
        return redirect(url_for('book', competition=competition['name'], club=club['name'])), 400

    # Si tout est OK, on met à jour
    competition['numberOfPlaces'] = available_places - placesRequired
    club['points'] = club_points - placesRequired
    
    flash('Great-booking complete!')
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('welcome.html', club=club, competitions=competitions, today=today)

@app.route('/points')
def show_points():
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)