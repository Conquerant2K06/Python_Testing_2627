import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

bookings_tracker = {}


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    matching_clubs = [
        club for club in clubs
        if club['email'] == request.form.get('email')
    ]
    if not matching_clubs:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))

    club = matching_clubs[0]
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        'welcome.html', club=club, competitions=competitions, today=today
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_clubs = [c for c in clubs if c['name'] == club]
    found_competitions = [
        c for c in competitions if c['name'] == competition
    ]

    if found_clubs and found_competitions:
        return render_template(
            'booking.html',
            club=found_clubs[0],
            competition=found_competitions[0]
        )
    else:
        flash("Something went wrong - please try again")
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [
        c for c in competitions
        if c['name'] == request.form.get('competition')
    ][0]
    club = [
        c for c in clubs if c['name'] == request.form.get('club')
    ][0]

    try:
        places_required = int(request.form.get('places'))
    except (ValueError, TypeError):
        flash("Veuillez entrer un nombre valide.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    competition_date = datetime.strptime(
        competition['date'], "%Y-%m-%d %H:%M:%S"
    )
    if competition_date < datetime.now():
        flash("Cette compétition est déjà terminée, vous ne pouvez plus "
              "réserver.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    if places_required <= 0:
        flash("Le nombre de places doit être supérieur à zéro.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    available_places = int(competition['numberOfPlaces'])
    if places_required > available_places:
        flash("Il n'y a pas assez de places disponibles pour cette "
              "compétition.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    club_points = int(club['points'])
    if places_required > club_points:
        flash("Vous n'avez pas assez de points pour réserver autant de "
              "places.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    booking_key = f"{club['name']}|{competition['name']}"
    already_booked = bookings_tracker.get(booking_key, 0)

    if places_required > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places par "
              "compétition.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    if already_booked + places_required > 12:
        flash(f"Vous avez déjà réservé {already_booked} places. Vous ne "
              f"pouvez pas dépasser 12 places au total.")
        return redirect(url_for(
            'book', competition=competition['name'], club=club['name']
        ))

    bookings_tracker[booking_key] = already_booked + places_required
    competition['numberOfPlaces'] = available_places - places_required
    club['points'] = club_points - places_required

    flash('Great-booking complete!')
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        'welcome.html', club=club, competitions=competitions, today=today
    )


@app.route('/points')
def show_points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
