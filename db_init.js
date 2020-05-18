// Creates a Mongo User credentials that will be used by
// python Mongo driver for authentication. User and Pwd fields must match
// MONGO_USER and MONGO_PASSWORD variables from docker-compose.yml

db.createUser(
  {
    user : "taori",
    pwd : "iroat1221",
    roles : [
      {
        role : "dbOwner",
        db : "test_db"
      },
      "dbOwner"
    ]
  }
)
