"""Replace processor lookup IDs with a PostgreSQL enum."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0007_payment_processor_enum"
down_revision = "0006_record_order_processor"
branch_labels = None
depends_on = None


payment_processor_type = postgresql.ENUM("PayPal", name="payment_processor")


def upgrade() -> None:
    connection = op.get_bind()
    unsupported = connection.execute(
        sa.text("SELECT name FROM payment_processors WHERE name <> 'PayPal'")
    ).scalars().all()
    if unsupported:
        raise RuntimeError(f"Unsupported payment processors must be migrated first: {unsupported}")

    payment_processor_type.create(connection, checkfirst=True)
    op.add_column("settings", sa.Column("payment_processor", payment_processor_type, nullable=True))
    op.add_column("orders", sa.Column("payment_processor", payment_processor_type, nullable=True))
    op.execute(
        """
        UPDATE settings AS s
        SET payment_processor = p.name::payment_processor
        FROM payment_processors AS p
        WHERE s.payment_processor_id = p.id
        """
    )
    op.execute(
        """
        UPDATE orders AS o
        SET payment_processor = p.name::payment_processor
        FROM payment_processors AS p
        WHERE o.payment_processor_id = p.id
        """
    )
    op.alter_column("orders", "payment_processor", existing_type=payment_processor_type, nullable=False)
    op.drop_constraint("account_settings_payment_processors_fk", "settings", type_="foreignkey")
    op.drop_constraint("orders_payment_processors_fk", "orders", type_="foreignkey")
    op.drop_column("settings", "payment_processor_id")
    op.drop_column("orders", "payment_processor_id")
    op.drop_table("payment_processors")


def downgrade() -> None:
    op.create_table(
        "payment_processors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="payment_processors_pk"),
        sa.UniqueConstraint("name", name="payment_processors_unique"),
    )
    op.execute("INSERT INTO payment_processors (id, name) VALUES (1, 'PayPal')")
    op.add_column("settings", sa.Column("payment_processor_id", sa.Integer(), nullable=True))
    op.add_column("orders", sa.Column("payment_processor_id", sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE settings AS s
        SET payment_processor_id = p.id
        FROM payment_processors AS p
        WHERE s.payment_processor::text = p.name
        """
    )
    op.execute(
        """
        UPDATE orders AS o
        SET payment_processor_id = p.id
        FROM payment_processors AS p
        WHERE o.payment_processor::text = p.name
        """
    )
    op.alter_column("orders", "payment_processor_id", existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key(
        "account_settings_payment_processors_fk",
        "settings",
        "payment_processors",
        ["payment_processor_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "orders_payment_processors_fk", "orders", "payment_processors", ["payment_processor_id"], ["id"]
    )
    op.drop_column("settings", "payment_processor")
    op.drop_column("orders", "payment_processor")
    payment_processor_type.drop(op.get_bind(), checkfirst=True)
