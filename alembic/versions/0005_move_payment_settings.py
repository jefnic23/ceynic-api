"""Move per-storefront PayPal credentials into account settings JSONB."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0005_move_payment_settings"
down_revision = "0004_unset_payment_processor"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "settings",
        sa.Column(
            "payment_processor_settings",
            postgresql.JSONB(),
            server_default=sa.text("'{\"processors\": {}}'::jsonb"),
            nullable=False,
        ),
    )
    # Copy even when PayPal is not the active processor; switching back should retain credentials.
    op.execute(
        """
        UPDATE settings AS s
        SET payment_processor_settings = jsonb_set(
            s.payment_processor_settings,
            '{processors,PayPal}',
            jsonb_build_object('client_id', p.client_id, 'client_secret', p.client_secret)
        )
        FROM paypal_settings AS p
        WHERE p.storefront_id = s.storefront_id
        """
    )
    # All PayPal rows must have an account settings row before dropping the old table.
    connection = op.get_bind()
    orphaned = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1 FROM paypal_settings AS p
                WHERE NOT EXISTS (
                    SELECT 1 FROM settings AS s WHERE s.storefront_id = p.storefront_id
                )
            )
            """
        )
    ).scalar_one()
    if orphaned:
        raise RuntimeError("PayPal settings without account settings cannot be migrated")

    op.drop_table("paypal_settings")


def downgrade() -> None:
    op.create_table(
        "paypal_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.String(), nullable=False),
        sa.Column("client_secret", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["storefront_id"], ["storefronts.id"], name="paypal_settings_storefronts_fk", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="paypal_settings_pk"),
        sa.UniqueConstraint("storefront_id", name="uq_paypal_settings_storefront_id"),
    )
    # The old table has no ID sequence; assign fresh IDs to one row per storefront.
    op.execute(
        """
        INSERT INTO paypal_settings (id, storefront_id, client_id, client_secret)
        SELECT row_number() OVER (ORDER BY storefront_id), storefront_id, client_id, client_secret
        FROM (
            SELECT DISTINCT ON (s.storefront_id)
                s.storefront_id,
                s.payment_processor_settings #>> '{processors,PayPal,client_id}' AS client_id,
                s.payment_processor_settings #>> '{processors,PayPal,client_secret}' AS client_secret
            FROM settings AS s
            WHERE s.payment_processor_settings #> '{processors,PayPal}' IS NOT NULL
            ORDER BY s.storefront_id, s.id
        ) AS credentials
        """
    )
    op.drop_column("settings", "payment_processor_settings")
