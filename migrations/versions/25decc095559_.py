"""empty message

Revision ID: 25decc095559
Revises: 03a492fd63bd
Create Date: 2020-11-20 17:10:24.180930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "25decc095559"
down_revision = "03a492fd63bd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_questions_description", table_name="questions")
    op.create_index(op.f("ix_questions_description"), "questions", ["description"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_questions_description"), table_name="questions")
    op.create_index("ix_questions_description", "questions", ["description"], unique=False)
    # ### end Alembic commands ###