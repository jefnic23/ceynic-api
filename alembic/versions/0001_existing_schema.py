"""Baseline the existing PostgreSQL schema (audited before Alembic adoption).

Apply to an empty database; an existing database must be verified and stamped
instead of running this upgrade against its populated tables.
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_existing_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "storefronts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subdomain", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="storefronts_pk"),
        sa.UniqueConstraint("subdomain", name="storefronts_unique"),
    )
    op.create_table(
        "mediums",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="mediums_pk"),
    )
    op.create_table(
        "payment_processors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="payment_processors_pk"),
        sa.UniqueConstraint("name", name="payment_processors_unique"),
    )
    op.create_table(
        "contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.Column("about", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["storefront_id"], ["storefronts.id"], name="contents_storefronts_fk"
        ),
        sa.PrimaryKeyConstraint("id", name="contents_pk"),
    )
    op.create_table(
        "paypal_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.String(), nullable=True),
        sa.Column("client_secret", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="paypal_settings_pk"),
    )
    op.execute("CREATE SEQUENCE account_settings_id_seq")
    op.create_table(
        "settings",
        sa.Column(
            "id",
            sa.Integer(),
            server_default=sa.text("nextval('account_settings_id_seq'::regclass)"),
            nullable=False,
        ),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.Column("payment_processor_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["storefront_id"],
            ["storefronts.id"],
            name="account_settings_storefronts_fk",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["payment_processor_id"],
            ["payment_processors.id"],
            name="account_settings_payment_processors_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="account_settings_pk"),
    )
    op.execute("ALTER SEQUENCE account_settings_id_seq OWNED BY settings.id")
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["storefront_id"],
            ["storefronts.id"],
            name="users_storefronts_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="users_pk"),
        sa.UniqueConstraint("email", name="users_unique"),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("medium_id", sa.Integer(), nullable=False),
        sa.Column(
            "date_added",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["medium_id"], ["mediums.id"], name="products_mediums_fk"
        ),
        sa.ForeignKeyConstraint(
            ["storefront_id"],
            ["storefronts.id"],
            name="products_storefronts_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="products_pk"),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.String(), nullable=False),
        sa.Column("authorization_id", sa.String(), nullable=True),
        sa.Column("capture_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("create_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["storefront_id"],
            ["storefronts.id"],
            name="orders_storefronts_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="orders_pk"),
    )
    op.create_table(
        "social_media_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("storefront_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["storefront_id"],
            ["storefronts.id"],
            name="social_media_links_storefronts_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="social_media_links_pk"),
    )
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("expiry_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="refresh_tokens_users_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="refresh_tokens_pk"),
    )
    op.create_table(
        "product_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), server_default="1", nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="product_images_products_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="product_images_pk"),
        sa.UniqueConstraint("product_id", "position", name="product_images_unique"),
    )
    op.create_table(
        "order_products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name="order_products_orders_fk",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="order_products_products_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="order_products_pk"),
    )


def downgrade() -> None:
    for table in (
        "order_products",
        "product_images",
        "refresh_tokens",
        "social_media_links",
        "orders",
        "products",
        "users",
        "settings",
        "paypal_settings",
        "contents",
        "payment_processors",
        "mediums",
        "storefronts",
    ):
        op.drop_table(table)
