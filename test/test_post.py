from db import schemas
import pytest

def test_unathurized_get_post(client):
    response = client.get("/posts")
    assert response.status_code == 401
    
def test_unathurized_get_one_post(client,test_post):
    response = client.get(f"/posts/{test_post[0].id}")
    assert response.status_code == 401



    



def test_get_all_post(client,test_post,token):
    response = client.get("/posts",headers={**client.headers,"Authorization": f"Bearer {token}"})
    all_post = [schemas.Show_Posts2(**post) for post in list(response.json())]
    for i in range(len(test_post)):
        assert all_post[i].Post.id == test_post[i].id
        assert all_post[i].Post.title == test_post[i].title
        assert all_post[i].Post.content == test_post[i].content
    assert len(response.json()) == len(test_post)
    assert response.status_code == 200
    
def test_delete_post(client,token,test_post):
    response = client.delete(f"/posts/{test_post[0].id}",headers={**client.headers,"Authorization": f"Bearer {token}"})
    response2 = client.get("/posts",headers={**client.headers,"Authorization": f"Bearer {token}"})
    deleted_post = schemas.Show_Posts(**response.json())
    assert deleted_post.title == test_post[0].title
    assert deleted_post.content == test_post[0].content
    assert len(response2.json()) == 2
    assert response.status_code == 200


def test_delete_post_other_users(client,token,test_post2,test_create_user2):
    response = client.delete(f"/posts/{test_post2[0].id}",headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    
def test_update_post(client,test_post,token):
    post_data ={"title":"Update title","content":"Update content","published":False}
    response = client.put(f"/posts/{test_post[2].id}",json=post_data,headers={**client.headers,"Authorization": f"Bearer {token}"})
    updated_post = schemas.Show_Posts(**response.json())
    assert updated_post.title == post_data["title"]
    assert updated_post.content == post_data["content"]
    assert updated_post.published == post_data["published"]
    assert response.status_code == 202
    
    
    
@pytest.mark.parametrize("title,content,published",[
    ("Fun","this is a test joke",True),
    ("Drama","the earth is going to destroy",True)
])
def test_create_post(client,token,test_create_user,title,content,published):
    post_data ={"title":title,"content":content,"published":published}
    response = client.post("/posts/create",json=post_data,headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.json().get("title") == post_data["title"]
    assert response.json().get("content") == post_data["content"]
    assert response.json().get("published") == post_data["published"]
    assert response.json().get("owner_id") == test_create_user.id
    assert response.status_code == 201
    
    
    
def test_get_current_post(client,test_post,token):
    response = client.get(f"/posts/{test_post[1].id}",headers={**client.headers,"Authorization": f"Bearer {token}"})
    current_post = schemas.Show_Posts2(**response.json())
    assert current_post.Post.id == test_post[1].id
    assert current_post.Post.title == test_post[1].title
    assert current_post.Post.content == test_post[1].content
    assert response.status_code == 200
    
def test_get_current_post_not_exist(client,token):
    response = client.get(f"/posts/8888",headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    
def test_create_post_without_published(client,token):
    post_data ={"title":"Test title","content":"test_content"}
    response = client.post("/posts/create",json=post_data,headers={**client.headers,"Authorization": f"Bearer {token}"})
    assert response.json().get("title") == post_data["title"]
    assert response.json().get("content") == post_data["content"]
    assert response.json().get("published") == True
    assert response.status_code == 201

