import pytest # type: ignore
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_show_summary_with_unknown_email_should_not_crash(client):
    response = client.post('/showSummary', data={'email': 'inconnu@test.com'})
    assert response.status_code != 500
    assert response.status_code == 302


def test_book_with_invalid_club_or_competition_should_not_crash(client):
    response = client.get('/book/Spring Festival/Club Inexistant')
    assert response.status_code != 500
    assert response.status_code == 302


def test_points_board_page_should_display_all_clubs(client):
    response = client.get('/points')
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data