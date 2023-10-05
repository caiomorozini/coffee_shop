"""remove_quantity_from_ingredients

Revision ID: 65b472f10586
Revises: 47fc5c47acfa
Create Date: 2023-10-04 19:13:26.447438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65b472f10586'
down_revision: Union[str, None] = '47fc5c47acfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Remove a coluna quantity da tabela ingredients """
    op.drop_column("ingredients", "quantity")


def downgrade() -> None:
    """ Adiciona a coluna quantity na tabela ingredients """
    op.add_column(
        "ingredients",
        sa.Column(
            "quantity", sa.Integer, nullable=False, server_default="0"
        ),
    )
