"""Initial migration

Revision ID: 7fb6abb92b31
Revises: 
Create Date: 2024-11-23 13:09:01.007880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7fb6abb92b31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tariffs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('relevance_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tariffs_relevance_date'), 'tariffs', ['relevance_date'], unique=False)
    op.create_table('material_rates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('material_type', sa.String(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('tariff_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tariff_id'], ['tariffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_material_rates_tariff_id_material_type', 'material_rates', ['tariff_id', 'material_type'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_material_rates_tariff_id_material_type', table_name='material_rates')
    op.drop_table('material_rates')
    op.drop_index(op.f('ix_tariffs_relevance_date'), table_name='tariffs')
    op.drop_table('tariffs')
