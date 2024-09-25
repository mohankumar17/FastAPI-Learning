"""add dept table

Revision ID: 6874afffb200
Revises: 9dc44a2fc7b6
Create Date: 2024-09-19 14:33:27.337412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6874afffb200'
down_revision: Union[str, None] = '9dc44a2fc7b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(table_name="employees", column_name="department_id", nullable=True)

    op.create_table("departments", 
        sa.Column("dept_id", sa.Integer, primary_key=True),
        sa.Column("dept_name", sa.String, nullable=False, unique=True)
    )

    op.create_foreign_key(constraint_name="emp_dept_fk", source_table="employees", local_cols=["department_id"], referent_table="departments", remote_cols=["dept_id"], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.alter_column(table_name="employees", column_name="department_id", nullable=False)
    op.drop_constraint(constraint_name="emp_dept_fk", table_name="employees")
    op.drop_table("departments")
    pass
