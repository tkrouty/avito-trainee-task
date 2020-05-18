db.createUser(
  {
    user : "user",
    pwd : "password",
    roles : [
      {
        role : "dbOwner",
        db : "test_db"
      },
      "dbOwner"
    ]
  }
)

