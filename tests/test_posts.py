from turtle import title
import pytest
from app import schemas
from fastapi import status


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    posts = res.json()

    # validate post
    validated_posts = []
    for post in posts:
        validated_posts.append(schemas.PostOut(**post))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == status.HTTP_200_OK

    for index in range(len(validated_posts)):
        assert validated_posts[index].Post.id == test_posts[index].id
        assert validated_posts[index].Post.title == test_posts[index].title
        assert validated_posts[index].Post.content == test_posts[index].content
        assert validated_posts[index].Post.owner_id == test_posts[index].owner_id


def test_unauthorized_user_get_all_posts(client):
    res = client.get('/posts/')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get('/posts/909009')
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_posts[0].owner_id


@pytest.mark.parametrize('title, content, published', [
    ('outstanding title', 'outstanfing content', True),
    ('excelcior', 'Magic hidden super content', False),
    ('just happy to be happy', 'to be happy is more than to be ok', True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        '/posts/', json={'title': title, 'content': content, 'published': published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    post = {'title': 'i am just a title',
            'content': 'Be cool, smart and honest'}
    res = authorized_client.post('/posts/', json=post)
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == post['title']
    assert created_post.content == post['content']
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_get_create_post(client):
    post = {'title': 'i am just a title',
            'content': 'Be cool, smart and honest'}
    res = client.post('/posts/', json=post)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_delete_Post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete(f'/posts/{214123500}')
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_posts):
    post = {
        'title': 'Updated title',
        'content': 'Updated content',
        'id': test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=post)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == post['title']
    assert updated_post.content == post['content']
    assert updated_post.id == post['id']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    post = {
        'title': 'Updated title',
        'content': 'Updated content',
        'id': test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=post)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_update_Post(client, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_post_non_exist(authorized_client, test_posts):
    post = {
        'title': 'Updated title',
        'content': 'Updated content',
        'id': test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{214123500}', json=post)
    assert res.status_code == status.HTTP_404_NOT_FOUND
