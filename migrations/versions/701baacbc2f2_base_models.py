"""base models

Revision ID: 701baacbc2f2
Revises: 
Create Date: 2024-03-19 21:36:25.741447

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '701baacbc2f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'),
              nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('organization', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_organization_name'),
                              ['name'], unique=False)

    op.create_table('harvest_source',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('notification_emails', postgresql.ARRAY(sa.String()),
              nullable=True),
    sa.Column('organization_id', sa.UUID(), nullable=False),
    sa.Column('frequency', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('schema_type', sa.String(), nullable=False),
    sa.Column('source_type', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'),
              nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('harvest_job',
    sa.Column('harvest_source_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('new', 'in_progress', 'complete',
                                name='job_status'), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_finished', sa.DateTime(), nullable=True),
    sa.Column('records_added', sa.Integer(), nullable=True),
    sa.Column('records_updated', sa.Integer(), nullable=True),
    sa.Column('records_deleted', sa.Integer(), nullable=True),
    sa.Column('records_errored', sa.Integer(), nullable=True),
    sa.Column('records_ignored', sa.Integer(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'),
              nullable=False),
    sa.ForeignKeyConstraint(['harvest_source_id'], ['harvest_source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('harvest_job', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_harvest_job_date_created'),
                              ['date_created'], unique=False)
        batch_op.create_index(batch_op.f('ix_harvest_job_status'),
                              ['status'], unique=False)

    op.create_table('harvest_error',
    sa.Column('harvest_job_id', sa.UUID(), nullable=False),
    sa.Column('harvest_record_id', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('severity', sa.Enum('CRITICAL', 'ERROR', 'WARN',
                                  name='error_serverity'), nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'),
              nullable=False),
    sa.ForeignKeyConstraint(['harvest_job_id'], ['harvest_job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('harvest_error', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_harvest_error_severity'),
                              ['severity'], unique=False)

    op.create_table('harvest_record',
    sa.Column('job_id', sa.UUID(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('ckan_id', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('source_metadata', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'),
              nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['harvest_job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('harvest_record', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_harvest_record_ckan_id'),
                              ['ckan_id'], unique=False)
        batch_op.create_index('ix_job_id_identifier',
                              ['job_id', 'identifier'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('harvest_record', schema=None) as batch_op:
        batch_op.drop_index('ix_job_id_identifier')
        batch_op.drop_index(batch_op.f('ix_harvest_record_ckan_id'))

    op.drop_table('harvest_record')
    with op.batch_alter_table('harvest_error', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_harvest_error_severity'))

    op.drop_table('harvest_error')
    with op.batch_alter_table('harvest_job', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_harvest_job_status'))
        batch_op.drop_index(batch_op.f('ix_harvest_job_date_created'))

    op.drop_table('harvest_job')
    op.drop_table('harvest_source')
    with op.batch_alter_table('organization', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_organization_name'))

    op.drop_table('organization')
    # ### end Alembic commands ###
