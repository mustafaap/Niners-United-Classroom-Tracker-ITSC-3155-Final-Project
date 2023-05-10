from tests.e2e.conftest import test_app

def test_load_maps(test_app):
    response = test_app.get('/maps')
    response_data = response.data.decode('utf-8')

    assert '''<h3 class="d-flex justify-content-center my-3">NUTT Map</h3>''' in response_data
