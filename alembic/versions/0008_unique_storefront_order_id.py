"""Prevent duplicate local orders for one external checkout."""

from alembic import op


revision = "0008_unique_storefront_order_id"
down_revision = "0007_payment_processor_enum"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_orders_storefront_order_id", "orders", ["storefront_id", "order_id"])


def downgrade() -> None:
    op.drop_constraint("uq_orders_storefront_order_id", "orders", type_="unique")
