from statistics import mode
import pytest
from fastapi import status
from app import models


@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_posts[3].id, 'voted': True})
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_posts[3].id, 'voted': True})
    assert res.status_code == status.HTTP_409_CONFLICT


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_posts[3].id, 'voted': False})
    assert res.status_code == status.HTTP_201_CREATED


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': test_posts[3].id, 'voted': False})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': 999999, 'voted': False})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        '/vote/', json={'post_id': test_posts[3].id, 'voted': True})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
