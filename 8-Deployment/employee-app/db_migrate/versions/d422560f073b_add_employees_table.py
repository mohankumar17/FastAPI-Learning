"""Intial Tables

Revision ID: d422560f073b
Revises: 
Create Date: 2024-09-19 13:53:52.641164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd422560f073b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("employees", 
        sa.Column("emp_id", sa.Integer, primary_key=True),
        sa.Column("emp_name", sa.String(50), nullable=False),
        sa.Column("dob", sa.Date),
        sa.Column("department_id", sa.Integer, nullable=False),
        sa.Column("emp_email", sa.String, nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean, server_default="FALSE")
    )
    pass

def downgrade() -> None:
    op.drop_table('employees')
    pass
