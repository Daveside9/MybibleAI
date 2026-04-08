"""Add calendar features - teams, leagues, and match updates

Revision ID: add_calendar_features
Revises: 2f28e202067d
Create Date: 2025-12-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_calendar_features'
down_revision = '2f28e202067d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create teams table
    op.create_table('teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('logo', sa.String(length=500), nullable=True),
        sa.Column('country', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)
    op.create_index(op.f('ix_teams_external_id'), 'teams', ['external_id'], unique=True)
    
    # Create leagues table
    op.create_table('leagues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('country', sa.String(length=50), nullable=False),
        sa.Column('logo', sa.String(length=500), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leagues_id'), 'leagues', ['id'], unique=False)
    op.create_index(op.f('ix_leagues_external_id'), 'leagues', ['external_id'], unique=True)
    
    # Add new columns to matches table
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('external_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('home_team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('away_team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('league_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('home_odds', sa.Float(), nullable=True, server_default='1.9'))
        batch_op.add_column(sa.Column('away_odds', sa.Float(), nullable=True, server_default='1.9'))
        batch_op.add_column(sa.Column('draw_odds', sa.Float(), nullable=True, server_default='3.0'))
        batch_op.add_column(sa.Column('last_synced', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        
        # Create indexes
        batch_op.create_index(batch_op.f('ix_matches_external_id'), ['external_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_matches_scheduled_at'), ['scheduled_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_matches_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_matches_league_id'), ['league_id'], unique=False)
        
        # Create foreign keys
        batch_op.create_foreign_key('fk_matches_home_team', 'teams', ['home_team_id'], ['id'])
        batch_op.create_foreign_key('fk_matches_away_team', 'teams', ['away_team_id'], ['id'])
        batch_op.create_foreign_key('fk_matches_league', 'leagues', ['league_id'], ['id'])


def downgrade() -> None:
    # Drop new columns from matches using batch mode
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.drop_constraint('fk_matches_league', type_='foreignkey')
        batch_op.drop_constraint('fk_matches_away_team', type_='foreignkey')
        batch_op.drop_constraint('fk_matches_home_team', type_='foreignkey')
        
        batch_op.drop_index(batch_op.f('ix_matches_league_id'))
        batch_op.drop_index(batch_op.f('ix_matches_status'))
        batch_op.drop_index(batch_op.f('ix_matches_scheduled_at'))
        batch_op.drop_index(batch_op.f('ix_matches_external_id'))
        
        batch_op.drop_column('updated_at')
        batch_op.drop_column('last_synced')
        batch_op.drop_column('draw_odds')
        batch_op.drop_column('away_odds')
        batch_op.drop_column('home_odds')
        batch_op.drop_column('league_id')
        batch_op.drop_column('away_team_id')
        batch_op.drop_column('home_team_id')
        batch_op.drop_column('external_id')
    
    # Drop leagues table
    op.drop_index(op.f('ix_leagues_external_id'), table_name='leagues')
    op.drop_index(op.f('ix_leagues_id'), table_name='leagues')
    op.drop_table('leagues')
    
    # Drop teams table
    op.drop_index(op.f('ix_teams_external_id'), table_name='teams')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')
