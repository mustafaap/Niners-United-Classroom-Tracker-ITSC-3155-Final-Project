from tests.e2e.conftest import test_app

def test_load_maps(test_app):
    response = test_app.get('/maps')