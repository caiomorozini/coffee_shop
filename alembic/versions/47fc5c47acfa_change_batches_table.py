"""change_batches_table

Revision ID: 47fc5c47acfa
Revises: 
Create Date: 2023-10-03 22:15:50.232032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47fc5c47acfa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Apaga a tabela batches e suas FK e cria novamente com novas colunas """

    op.drop_column("ingredients", "batch_id")

    op.drop_table("batches")

    op.create_table(
        "batches",
        sa.Column(
            "id", sa.Integer, primary_key=True),
        sa.Column(
            "ingredient_id", sa.Integer,
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


def downgrade() -> None:

    op.drop_table("batches")

    op.create_table(
        "batches",
        sa.Column(
            "id", sa.Integer, primary_key=True),
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

    op.add_column("ingredients", sa.Column(
        "batch_id", sa.Integer,
        sa.ForeignKey("batches.id")))

