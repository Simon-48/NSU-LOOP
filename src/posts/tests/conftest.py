import pytest


@pytest.fixture
def post_form_data():
    return {'content': 'Hi', 'image':'http://127.0.0.1'} 

@pytest.fixture
def comment_form_data():
    return {'body': 'Hi'}    

