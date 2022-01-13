from typing import List
from app import schemas
from fastapi import status


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
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


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/909009")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_posts[0].owner_id
