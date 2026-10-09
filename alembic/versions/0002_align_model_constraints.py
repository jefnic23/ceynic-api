"""Enforce model nullability and one-to-one relationships on the existing schema.

Review and resolve duplicate rows and NULL values before applying to any
database other than the audited one. PostgreSQL runs these changes in a
transaction, so failed constraints do not partially apply.
"""

from alembic import op


revision = "0002_align_model_constraints"
down_revision = "0001_existing_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for table, column in (
        ("contents", "about"),
        ("paypal_settings", "client_id"),
        ("paypal_settings", "client_secret"),
        ("product_images", "width"),
        ("product_images", "height"),
        ("settings", "payment_processor_id"),
        ("refresh_tokens", "user_id"),
        ("social_media_links", "name"),
        ("social_media_links", "url"),
        ("storefronts", "city"),
        ("storefronts", "name"),
    ):
        op.alter_column(table, column, nullable=False)

    op.create_foreign_key(
        "paypal_settings_storefronts_fk",
        "paypal_settings",
        "storefronts",
        ["storefront_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "uq_contents_storefront_id", "contents", ["storefront_id"]
    )
    op.create_unique_constraint(
        "uq_paypal_settings_storefront_id", "paypal_settings", ["storefront_id"]
    )
    op.create_unique_constraint(
        "uq_refresh_tokens_user_id", "refresh_tokens", ["user_id"]
    )

    # Reordering images requires this constraint to be deferred until commit.
    op.drop_constraint("product_images_unique", "product_images", type_="unique")
    op.create_unique_constraint(
        "uq_product_images_product_id_position",
        "product_images",
        ["product_id", "position"],
        deferrable=True,
        initially="DEFERRED",
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_product_images_product_id_position", "product_images", type_="unique"
    )
    op.create_unique_constraint(
        "product_images_unique", "product_images", ["product_id", "position"]
    )
    op.drop_constraint("uq_refresh_tokens_user_id", "refresh_tokens", type_="unique")
    op.drop_constraint(
        "uq_paypal_settings_storefront_id", "paypal_settings", type_="unique"
    )
    op.drop_constraint("uq_contents_storefront_id", "contents", type_="unique")
    op.drop_constraint(
        "paypal_settings_storefronts_fk", "paypal_settings", type_="foreignkey"
    )

    for table, column in (
        ("contents", "about"),
        ("paypal_settings", "client_id"),
        ("paypal_settings", "client_secret"),
        ("product_images", "width"),
        ("product_images", "height"),
        ("settings", "payment_processor_id"),
        ("refresh_tokens", "user_id"),
        ("social_media_links", "name"),
        ("social_media_links", "url"),
        ("storefronts", "city"),
        ("storefronts", "name"),
    ):
        op.alter_column(table, column, nullable=True)
