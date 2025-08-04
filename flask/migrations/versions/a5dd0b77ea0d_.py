"""empty message

Revision ID: a5dd0b77ea0d
Revises: 9cf08cdd329e
Create Date: 2025-08-03 23:08:00.868681

"""

from alembic import op
import sqlalchemy as sa

revision        = 'a5dd0b77ea0d'
down_revision   = '9cf08cdd329e'
branch_labels   = None
depends_on      = None


def upgrade():
    op.create_table(
        'resumos_semanais',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('texto', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='feedback_classifier'
    )


def downgrade():
    op.drop_table('resumos_semanais', schema='feedback_classifier')
