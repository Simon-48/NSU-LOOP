import pytest
from django import urls


@pytest.mark.django_db
def test_with_authenticated_client(client, django_user_model, post_form_data):
    username = "simon"
    password = "123"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    #form_url = 'http://127.0.0.1:8000/posts/'
    #response = client.post(form_url, data=post_form_data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_with_authenticated_client(client, django_user_model, comment_form_data):
    username = "simon"
    password = "123"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    #form_url = 'http://127.0.0.1:8000/posts/'
    #response = client.post(form_url, data=comment_form_data)
    assert response.status_code == 200

    

   




    
        


