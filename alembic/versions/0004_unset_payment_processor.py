"""Allow account settings to have no payment processor selected."""

from alembic import op


revision = "0004_unset_payment_processor"
down_revision = "0003_add_site_settings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("settings", "payment_processor_id", nullable=True)


def downgrade() -> None:
    # Assign a processor to any settings with NULL payment_processor_id first.
    op.alter_column("settings", "payment_processor_id", nullable=False)
