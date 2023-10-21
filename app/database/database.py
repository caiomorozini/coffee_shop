import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
import databases

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/coffeeshop_dev"

database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

ingredients = sa.Table(
    "ingredients",
    metadata,
    sa.Column(
        "id", sa.Integer, primary_key=True),
    sa.Column(
        "name", sa.String(50)),
    sa.Column(
        "observations",
        sa.String(500)
    ),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)

input_table = sa.Table(
    "input",
    metadata,
    sa.Column(
        "id", sa.Integer, primary_key=True),
    sa.Column(
        "id_ingredient", sa.Integer,
        sa.ForeignKey("ingredients.id")),
    sa.Column(
        "quantity", sa.Integer),
    sa.Column(
        "unit_price", sa.Float),
    sa.Column(
        "date", sa.DateTime),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)

output_table = sa.Table(
    "output",
    metadata,
    sa.Column(
        "id", sa.Integer, primary_key=True),
    sa.Column(
        "id_ingredient", sa.Integer,
        sa.ForeignKey("ingredients.id")),
    sa.Column(
        "quantity", sa.Integer),
    sa.Column(
        "date", sa.DateTime),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)

batches = sa.Table(
    "batches",
    metadata,
    sa.Column(
        "id", sa.Integer, primary_key=True),
    sa.Column(
        "ingredient", sa.Integer,
        sa.ForeignKey("ingredients.id")),
    sa.Column(
        "quantity", sa.Integer),
    sa.Column(
        "expiration", sa.DateTime),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)

products = sa.Table(
    "products",
    metadata,
    sa.Column(
        "id", sa.Integer, primary_key=True),
    sa.Column(
        "name", sa.String(50)),
    sa.Column(
        "price", sa.Float),
    sa.Column(
        "ingredients",
        sa.Integer,
        sa.ForeignKey("ingredients.id")
    ),
    sa.Column(
        "descript",
        sa.String(500)
    ),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)

order_products = sa.Table(
    "order_products",
    metadata,
    sa.Column(
        "order_id", sa.Integer,
        sa.ForeignKey("orders.id")),
    sa.Column(
        "product_id", sa.Integer,
        sa.ForeignKey("products.id"))
)

orders = sa.Table(
    "orders",
    metadata,
    sa.Column(
        "id", sa.Integer, primary_key=True),
    sa.Column(
        "products",
        sa.ARRAY(
            sa.Integer,
            sa.ForeignKey("products.id")),
        ),
    sa.Column(
        "price",
        sa.Float,
    ),
    sa.Column(
        "observations",
        sa.String(500)
    ),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
)

# Crie índices para a tabela 'ingredients'
sa.Index('idx_ingredients_name', ingredients.c.name)

# Crie índices para a tabela 'input'
sa.Index('idx_input_id_ingredient', input_table.c.id_ingredient)
sa.Index('idx_input_date', input_table.c.date)

# Crie índices para a tabela 'output'
sa.Index('idx_output_id_ingredient', output_table.c.id_ingredient)
sa.Index('idx_output_date', output_table.c.date)

# Crie índices para a tabela 'batches'
sa.Index('idx_batches_ingredient', batches.c.ingredient)
sa.Index('idx_batches_expiration', batches.c.expiration)

# Crie índices para a tabela 'products'
sa.Index('idx_products_name', products.c.name)
sa.Index('idx_products_ingredients', products.c.ingredients)

# Crie índices para a tabela 'orders'
sa.Index('idx_orders_products', orders.c.products)

engine = sa.create_engine(DATABASE_URL)

metadata.create_all(engine)