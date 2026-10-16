"""Add user names for the admin welcome message."""

from alembic import op
import sqlalchemy as sa


revision = "0009_add_user_names"
down_revision = "0008_unique_storefront_order_id"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("first_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(), nullable=True))

    op.get_bind().execute(
        sa.text(
            "UPDATE users SET first_name = :first_name, last_name = :last_name "
            "WHERE email = :email"
        ),
        {"first_name": "Jeff", "last_name": "Nicholas", "email": "jefnic23@gmail.com"},
    )


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
