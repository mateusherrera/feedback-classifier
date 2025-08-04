"""empty message

Revision ID: 9cf08cdd329e
Revises: 
Create Date: 2025-08-03 21:48:25.241928

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision        = '9cf08cdd329e'
down_revision   = None
branch_labels   = None
depends_on      = None


def upgrade():
    op.create_table(
        'comentario',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('texto', sa.Text(), nullable=False),
        sa.Column('categoria', sa.String(length=50), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('confianca', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='feedback_classifier'
    )

    op.create_table(
        'user',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        schema='feedback_classifier'
    )


def downgrade():
    op.drop_table('user', schema='feedback_classifier')
    op.drop_table('comentario', schema='feedback_classifier')
