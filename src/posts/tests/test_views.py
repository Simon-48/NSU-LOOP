import pytest
from django import urls

@pytest.mark.parametrize('param', [
    ('home-view')
])

def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


