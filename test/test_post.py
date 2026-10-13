from app import schemas
import pytest
def test_get_post(client, test_posts):
    res = client.get("/post")
    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_create_post_unauthorized(client):
    res = client.post("/post", json = {
        "title" : "Welcome Here",
        "content" : "Learn backend",
        "published" : True
        
        })
    assert res.status_code == 401


@pytest.mark.parametrize("title, content, published", [
    ("Welcome to Unpacking", "Learning the sqlalchemy", True),
    ("Welcome to Beached", "Awesome beaches in Chennai", False),
    ("Welcome to World", "Aliens are awaiting", True)
    
])
def  test_create_post(authorized_client, title, content, published, create_user):
    res = authorized_client.post("/post", json = {
    "title" : title,
    "content" : content,
    "published" : published
    
    })
    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner.id == create_user['id']
    assert res.status_code == 201

def test_get_one_post(client, test_posts):
    res = client.get(f"/post/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

def test_get_one_post_not_exist(client, test_posts):
    res = client.get(f"/post/889")
    assert res.status_code == 404

def test_delete_one_post_unauthorized(client, test_posts):
    res = client.delete(f"/post/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_one_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/post/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/post/773")
    assert res.status_code == 404

def test_update_one_post_unauthorized(client, test_posts):
        data = {
        "title" : "Updated title",
        "content" : "Updated Centent",
        "id" : test_posts[0].id
    }
        res = client.put(f"/post/{test_posts[0].id}", json = data)
        assert res.status_code == 401

def test_update_one_post(authorized_client, test_posts):
    data = {
        "title" : "Updated title",
        "content" : "Updated Centent",
        "id" : test_posts[0].id
    }
    res = authorized_client.put(f"/post/{test_posts[0].id}", json = data)
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data['title']
    assert res.status_code == 200

def test_update_one_post_not_exist(authorized_client, test_posts):
    data = {
            "title" : "Updated title",
            "content" : "Updated Centent",
            "id" : test_posts[0].id
        }
    res = authorized_client.put(f"/post/773", json = data)
    assert res.status_code == 404