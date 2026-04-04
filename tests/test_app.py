from src.authenticator import _hash_password, _verify_password


def test_password_hash_and_verify():
    pw = "test_password_123"
    hashed = _hash_password(pw)
    assert hashed != pw
    assert _verify_password(pw, hashed) is True


def test_wrong_password_fails():
    hashed = _hash_password("correct")
    assert _verify_password("wrong", hashed) is False


def test_hash_uses_random_salt():
    h1 = _hash_password("same")
    h2 = _hash_password("same")
    assert h1 != h2
    assert _verify_password("same", h1) is True
    assert _verify_password("same", h2) is True
