from app.infrastructure.password import encrypt_password

def test_encrypt_password():
    password = "cachorro_bananinha"
    expected_hash = "87ec165034ec6bbf63c9423f1a226b53d4d1fbef98297483e0bbb1c7f3bf46de"
    
    hashed_password = encrypt_password(password)
    
    assert hashed_password == expected_hash