"""Add JSONB site settings to account settings."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0003_add_site_settings"
down_revision = "0002_align_model_constraints"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "settings",
        sa.Column(
            "site_settings",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("settings", "site_settings")
