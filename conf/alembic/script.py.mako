"""${message}.

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade database."""
    print(f'Запуск миграции {revision}')
    ${upgrades if upgrades else "pass"}
    print(f'Завершение миграции {revision}')


def downgrade() -> None:
    """Downgrade database."""
    print(f'Откат миграции к {down_revision}')
    ${downgrades if downgrades else "pass"}
    print(f'Завершение отката миграции к {down_revision}')
