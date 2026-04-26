from auth import hash_password, verify_password                                                      
                                                            
hashed = hash_password("mypassword")
print(hashed)
print(verify_password("mypassword", hashed))                                                         
print(verify_password("wrongpassword", hashed))
                                                