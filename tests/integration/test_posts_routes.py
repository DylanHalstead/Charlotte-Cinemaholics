def test_get_all_posts(test_app):
    res = test_app.get('/posts/')
    assert res.status_code == 200
    assert b'posts' in res.data

def test_create_post(test_app):
    with test_app.session_transaction() as session:
        session['user'] = {
            'email': "testing@uncc.edu",
            'username': "urmum",
            'user_id': 1,
            'pfp': "default_user.png"
        }
    res = test_app.post('/posts', data={
        'title': 'Title',
        'body': 'Body',
        'time': '2021-05-01 12:00:00',
    }, follow_redirects = True)

    assert res.status_code == 200
    assert b'Title' in res.data
    assert b'Body' in res.data

def test_create_reply(test_app):
    with test_app.session_transaction() as session:
        session['user'] = {
            'email': "testing@uncc.edu",
            'username': "urmum",
            'user_id': 1,
            'pfp': "default_user.png"
        }
    res = test_app.post('/posts/1', data={
        'body': 'Body',
    }, follow_redirects = True)

    assert res.status_code == 200
    assert b'Body' in res.data

def test_create_quote_reply(test_app):
    with test_app.session_transaction() as session:
        session['user'] = {
            'email': "testing@uncc.edu",
            'username': "urmum",
            'user_id': 1,
            'pfp': "default_user.png"
        }
    res = test_app.post('/posts/1/reply/1/quote', data={
        'body': 'Quote body',
    }, follow_redirects = True)

    assert res.status_code == 200
    assert b'Quote body' in res.data  


def test_edit_post(test_app):
    with test_app.session_transaction() as session:
        session['user'] = {
            'email': "testing@uncc.edu",
            'username': "urmum",
            'user_id': 1,
            'pfp': "default_user.png"
        }
    res = test_app.post('/posts/1/edit', data={
        'title': 'Edited Title',
        'body': 'Edited Body',
        'reason': 'typo',
    }, follow_redirects = True)

    assert res.status_code == 200
    assert b'Edited Title' in res.data
    assert b'Edited Body' in res.data  
    assert b'typo' in res.data 

def test_edit_reply(test_app):
    with test_app.session_transaction() as session:
        session['user'] = {
            'email': "testing@uncc.edu",
            'username': "urmum",
            'user_id': 1,
            'pfp': "default_user.png"
        }
    res = test_app.post('/posts/1/reply/1/edit', data={
        'body': 'Edited reply body',
    }, follow_redirects = True)

    assert res.status_code == 200
    assert b'Edited reply body' in res.data  

def test_delete_reply(test_app):
    with test_app.session_transaction() as session:
        session['user'] = {
            'email': "testing@uncc.edu",
            'username': "urmum",
            'user_id': 1,
            'pfp': "default_user.png"
        }
    res = test_app.post('/posts/1/reply/2/delete', follow_redirects = True)

    assert res.status_code == 200
    assert b'Quote body' not in res.data  