
def test_unathurized_add_vote(client,test_post):
    response = client.post("/votes/",json={"post_id":test_post[1].id,"dir":1})
    assert response.status_code == 401

def test_vote(client,token,test_post):
    response = client.post("/votes/",json={"post_id":test_post[1].id,"dir":1},headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    
def test_vote2(client,token2,test_post):
    response = client.post("/votes/",json={"post_id":test_post[1].id,"dir":1},headers={**client.headers,"Authorization": f"Bearer {token2}"})
    assert response.status_code == 201
    
def test_vote_agin(client,token,test_post):
    response = client.post("/votes/",json={"post_id":test_post[1].id,"dir":1},headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 409
    
def test_delete_vote(client,token,test_post):
    response = client.post("/votes/",json={"post_id":test_post[1].id,"dir":0},headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    
def test_delete_vote_not_exist(client,token,test_post):
    response = client.post("/votes/",json={"post_id":test_post[1].id,"dir":0},headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    
def test__vote_on_Post_isNoExist(client,token,test_post):
    response = client.post("/votes/",json={"post_id":888,"dir":0},headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    