"""Record the payment processor used for each order."""

from alembic import op
import sqlalchemy as sa


revision = "0006_record_order_processor"
down_revision = "0005_move_payment_settings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    # Without an order-level history, the current selection is the only known
    # processor for an existing order. Refuse ambiguous or missing selections
    # instead of guessing which processor handled an earlier transaction.
    ambiguous = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1 FROM orders AS o
                JOIN settings AS s ON s.storefront_id = o.storefront_id
                GROUP BY o.storefront_id
                HAVING COUNT(DISTINCT s.id) > 1
            )
            """
        )
    ).scalar_one()
    if ambiguous:
        raise RuntimeError("Multiple settings rows exist for a storefront with orders; resolve before migrating")

    missing = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1 FROM orders AS o
                WHERE NOT EXISTS (
                    SELECT 1 FROM settings AS s
                    WHERE s.storefront_id = o.storefront_id
                      AND s.payment_processor_id IS NOT NULL
                )
            )
            """
        )
    ).scalar_one()
    if missing:
        raise RuntimeError("Orders without a selected payment processor cannot be backfilled automatically")

    op.add_column("orders", sa.Column("payment_processor_id", sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE orders AS o
        SET payment_processor_id = s.payment_processor_id
        FROM settings AS s
        WHERE o.storefront_id = s.storefront_id
        """
    )
    op.alter_column("orders", "payment_processor_id", existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key(
        "orders_payment_processors_fk",
        "orders",
        "payment_processors",
        ["payment_processor_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("orders_payment_processors_fk", "orders", type_="foreignkey")
    op.drop_column("orders", "payment_processor_id")
