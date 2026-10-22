import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ================= BRANCHE 1 =================
def test_show_summary_with_unknown_email_should_not_crash(client):
    response = client.post('/showSummary', data={'email': 'inconnu@test.com'})
    assert response.status_code != 500
    assert response.status_code == 302

# ================= BRANCHE 2 =================
def test_book_with_invalid_club_or_competition_should_not_crash(client):
    response = client.get('/book/Spring Festival/Club Inexistant')
    assert response.status_code != 500 
    assert response.status_code == 302

# ================= BRANCHE 3 =================
def test_purchase_places_with_negative_number_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-5'
    })
    assert response.status_code == 400

# ================= BRANCHE 4 =================
def test_purchase_places_more_than_available_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '999'
    })
    assert response.status_code == 400

# ================= BRANCHE 5 =================
def test_purchase_places_with_more_points_than_available_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '5'
    })
    assert response.status_code == 400

# ================= BRANCHE 6 =================
def test_purchase_places_more_than_12_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    })
    assert response.status_code == 400

# ================= BRANCHE 7 =================
def test_purchase_places_should_update_club_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    assert response.status_code == 200
    assert b"11" in response.data

# ================= BRANCHE 8 (Phase 2) =================
def test_points_board_page_should_display_all_clubs(client):
    response = client.get('/points')
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data