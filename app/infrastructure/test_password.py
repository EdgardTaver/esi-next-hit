from password import encrypt_password

def test_encrypt_password():
    password = "my_password"
    expected_hash = "f6e248ea994f3e342f61141b8b8e3ede86d4de53257abc8d06ae07a1da73fb39"
    
    hashed_password = encrypt_password(password)
    
    assert hashed_password == expected_hash