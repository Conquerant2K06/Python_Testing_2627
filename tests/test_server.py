import pytest
from server import app

# --- LA FIXTURE (nécessaire pour tous les tests) ---
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- TESTS DE LA BRANCHE 1 ---
def test_show_summary_with_unknown_email_should_not_crash(client):
    """Teste qu'un email inconnu ne fait pas planter l'app"""
    response = client.post('/showSummary', data={'email': 'inconnu@test.com'})
    assert response.status_code != 500
    assert response.status_code == 302

# --- NOUVEAU TEST DE LA BRANCHE 2 ---
def test_book_with_invalid_club_or_competition_should_not_crash(client):
    """Teste qu'une URL invalide ne fait pas planter l'app"""
    # On teste avec un club qui n'existe pas
    response = client.get('/book/Spring Festival/Club Inexistant')
    assert response.status_code != 500 
    assert response.status_code == 302 

    # On teste avec une compétition qui n'existe pas
    response = client.get('/book/Competition Inexistante/Simply Lift')
    assert response.status_code != 500
    assert response.status_code == 302

def test_show_summary_with_unknown_email_should_not_crash(client):
    response = client.post('/showSummary', data={'email': 'inconnu@test.com'})
    assert response.status_code != 500
    assert response.status_code == 302    

def test_purchase_places_with_negative_number_should_fail(client):
    """Teste qu'on ne peut pas réserver un nombre de places négatif"""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-5'
    })
    assert response.status_code == 400    

def test_purchase_places_more_than_available_should_fail(client):
    """Teste qu'on ne peut pas réserver plus de places que disponibles"""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '999'
    })
    assert response.status_code == 400    

def test_purchase_places_with_more_points_than_available_should_fail(client):
    """Teste qu'on ne peut pas réserver plus de places que le club n'a de points"""
    # Dans clubs.json, 'Iron Temple' a 4 points.
    # On essaie de réserver 5 places, ce qui devrait échouer.
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '5'
    })
    assert response.status_code == 400

def test_purchase_places_with_more_points_than_available_should_fail(client):
    """Teste qu'on ne peut pas réserver plus de places que le club n'a de points"""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '5'
    })
    assert response.status_code == 400 

def test_purchase_places_more_than_12_should_fail(client):
    """Teste qu'on ne peut pas réserver plus de 12 places par compétition"""
    # 'Simply Lift' a 13 points, on demande 13 places, ce qui doit échouer
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    })
    assert response.status_code == 400

def test_purchase_places_should_update_club_points(client):
    """Teste que les points du club sont bien déduits après une réservation"""
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    assert response.status_code == 200
    # On vérifie que "11" (13 - 2) apparaît dans la page de résumé
    assert b"11" in response.data    