import pytest # type: ignore
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_places_with_negative_number_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-5'
    })
    assert response.status_code == 302


def test_purchase_places_more_than_available_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '999'
    })
    assert response.status_code == 302


def test_purchase_places_with_more_points_than_available_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '5'
    })
    assert response.status_code == 302


def test_purchase_places_more_than_12_should_fail(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13'
    })
    assert response.status_code == 302


def test_purchase_places_should_update_club_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    assert response.status_code == 200