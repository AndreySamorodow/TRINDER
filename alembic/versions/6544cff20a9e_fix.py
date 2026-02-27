"""fix

Revision ID: 6544cff20a9e
Revises: 4b20372f8dfd
Create Date: 2026-02-27 18:30:55.726052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6544cff20a9e'
down_revision: Union[str, Sequence[str], None] = '4b20372f8dfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
