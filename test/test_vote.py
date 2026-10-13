import pytest
from app import models

@pytest.fixture
def  test_vote(create_user, test_posts, session):
    new_vote = models.Vote( post_id = test_posts[0].id, user_id = create_user['id'])
    session.add(new_vote)
    session.commit()
   

def test_vote_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json = { "post_id" : test_posts[0].id, "dir" : 1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json = { "post_id" : test_posts[0].id, "dir" : 1})
    assert res.status_code == 409

def test_delete_vote_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json = { "post_id" : test_posts[0].id, "dir" : 0})
    assert res.status_code == 201

def test_delete_vote_post_not_exists(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json = { "post_id" : 23, "dir" : 0})
    assert res.status_code == 404

def test_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json = { "post_id" : 989, "dir" : 1})
    assert res.status_code == 404

def test_vote_post_unauthorized(client, test_posts):
    res = client.post("/vote/", json = { "post_id" : test_posts[0].id, "dir" : 1})
    assert res.status_code == 401