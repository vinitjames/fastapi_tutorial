def test_get_all_post(authenticated_client):
    res = authenticated_client.get("/posts/")
    assert res.status_code == 200
    print (res.json())
    
    
