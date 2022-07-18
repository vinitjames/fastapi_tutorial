
def test_vote(authenticated_client, create_posts):
    res = authenticated_client.post("/votes/", json={"post_id": create_posts[0].id,
                                                     "dir": 1})
    assert res.status_code == 201

def test_vote_unauthenticated_client(client, create_posts):
    res = client.post("/votes/", json={"post_id": create_posts[0].id,
                                       "dir": 1})
    assert res.status_code == 401

def test_remove_vote(authenticated_client, create_votes):
    res = authenticated_client.post("/votes/", json={"post_id": create_votes.post_id,
                                                     "dir": 0})
    assert res.status_code == 201
    
def test_double_vote(authenticated_client, create_votes):
    res = authenticated_client.post("/votes/", json={"post_id": create_votes.post_id,
                                                     "dir": 1})
    assert res.status_code == 409

def test_vote_nonexistent_post(authenticated_client, create_votes):
    res = authenticated_client.post("/votes/", json={"post_id": 88888,
                                                     "dir": 1})
    assert res.status_code == 404
    
