from mongoengine import connect

connect(
    db="interneers_lab",
    host="mongodb://root:example@localhost:27019/interneers_lab?authSource=admin"
)