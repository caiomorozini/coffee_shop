import sqlalchemy
import databases

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/coffeeshop_dev"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

batches = sqlalchemy.Table(
    "batches",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "purchase", sqlalchemy.DateTime),
    sqlalchemy.Column(
        "manufacturing", sqlalchemy.DateTime),
    sqlalchemy.Column(
        "expiration", sqlalchemy.DateTime),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.TIMESTAMP(timezone=True),
        server_default=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.TIMESTAMP(timezone=True),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    ),
)

ingredients = sqlalchemy.Table(
    "ingredients",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "name", sqlalchemy.String(50)),
    sqlalchemy.Column(
        "quantity", sqlalchemy.Integer),
    sqlalchemy.Column(
        "batch_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("batches.id")
    ),
    sqlalchemy.Column(
        "observations",
        sqlalchemy.String(500)
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.TIMESTAMP(timezone=True),
        server_default=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.TIMESTAMP(timezone=True),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    ),
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)