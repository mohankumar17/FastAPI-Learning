"""Add users table and set foreign key constraints

Revision ID: 9dc44a2fc7b6
Revises: d422560f073b
Create Date: 2024-09-19 14:14:43.636893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '9dc44a2fc7b6'
down_revision: Union[str, None] = 'd422560f073b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table("users", 
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("user_email", sa.String, unique=True, nullable=False),
        sa.Column("user_password", sa.String, nullable=False),
        sa.Column("updated_at", sa.DateTime, default=datetime.now(), onupdate=datetime.now()),
    )

    op.add_column("employees", sa.Column("user_id", sa.Integer, sa.ForeignKey(name="emp_user_fk", column="users.user_id", ondelete="CASCADE"), nullable=False))

    #op.create_foreign_key(constraint_name="emp_user_fk", source_table="employees", local_cols="user_id", referent_table="users", remote_cols="", ondelete="CASCADE")
    
    pass


def downgrade() -> None:
    op.drop_constraint("emp_user_fk", table_name="employees")
    op.drop_table("users")
    op.drop_column("employees", column_name="user_id")
    pass
