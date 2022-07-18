from app.schemas.post import PostResp, PostWithVoteResp

def test_get_all_post(authenticated_client, create_posts):
    res = authenticated_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(create_posts)

def test_get_all_post_unauthenticated_client(client, create_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_single_post(authenticated_client, create_posts):
    res = authenticated_client.get(f"/posts/{create_posts[0].id}")
    assert res.status_code == 200
    post = PostWithVoteResp(**res.json())
    assert post.Post.id == create_posts[0].id
    assert post.Post.title == create_posts[0].title
    assert post.Post.content == create_posts[0].content
    assert post.Post.published == create_posts[0].published
    assert int(post.Post.owner.id) == create_posts[0].owner_id

def test_get_single_nonexistent_post(authenticated_client, create_posts):
    res = authenticated_client.get("/posts/88888")
    assert res.status_code == 404


def test_get_single_post_unauthenticated_client(client, create_posts):
    res = client.get(f"/posts/{create_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authenticated_client, create_posts):
    res = authenticated_client.delete(f"/posts/{create_posts[0].id}")
    assert res.status_code == 204

def test_delete_nonexistent_post(authenticated_client, create_posts):
    res = authenticated_client.delete(f"/posts/88888")
    assert res.status_code == 404

def test_delete_post_unauthenticated_client(client, create_posts):
    res = client.delete(f"/posts/{create_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_wrong_user(authenticated_client, create_posts):
    res = authenticated_client.delete(f"/posts/{create_posts[4].id}")
    assert res.status_code == 403


def test_update_post(authenticated_client, create_posts):
    updated_post = {"title" : "updated_title",
                    "content": "updated_content"}
    
    res = authenticated_client.put(f"/posts/{create_posts[0].id}",
                                   json = updated_post)
    assert res.status_code == 200
    post = PostResp(**res.json())
    assert post.id == create_posts[0].id
    assert post.title == updated_post["title"]
    assert post.content == updated_post["content"]

def test_update_post_unauthenticated_client(client, create_posts):
    updated_post = {"title" : "updated_title",
                    "content": "updated_content"}
    res = client.put(f"/posts/{create_posts[0].id}", json=updated_post)
    assert res.status_code == 401

def test_update_post_wrong_user(authenticated_client, create_posts):
    updated_post = {"title" : "updated_title",
                    "content": "updated_content"}
    res = authenticated_client.put(f"/posts/{create_posts[4].id}", json=updated_post)
    assert res.status_code == 403


    
    
    
    
    
    
    
    
