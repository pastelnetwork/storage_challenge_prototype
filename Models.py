from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.types import DateTime, Float, Integer, Text
from Database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Masternodes(Base):
    __tablename__ = 'masternodes'
    masternode_id = Column(Text, primary_key=True, index=True)
    masternode_ip_address = Column(Text) #, unique=True
    total_challenges_issued = Column(Integer)
    total_challenges_responded_to = Column(Integer)
    total_challenges_correct = Column(Integer)
    total_challenges_incorrect = Column(Integer)
    total_challenges_correct_but_too_slow = Column(Integer)
    total_challenges_never_responded_to = Column(Integer)
    challenge_response_success_rate_pct = Column(Float)

class Pastel_Blocks(Base):
    __tablename__ = 'pastel_blocks'
    block_hash = Column(Text, primary_key=True, index=True)
    block_number = Column(Integer)
    total_challenges_issued = Column(Integer)
    total_challenges_responded_to = Column(Integer)
    total_challenges_correct = Column(Integer)
    total_challenges_incorrect = Column(Integer)
    total_challenges_correct_but_too_slow = Column(Integer)
    total_challenges_never_responded_to = Column(Integer)
    challenge_response_success_rate_pct = Column(Float)
    
class Symbol_Files(Base):
    __tablename__ = 'symbol_files'
    file_hash = Column(Text, primary_key=True, index=True)
    file_length_in_bytes = Column(Integer)
    total_challenges_for_file = Column(Integer)
    
class Challenges(Base):
    __tablename__ = 'challenges'
    challenge_id = Column(Text, primary_key=True, index=True)
    challenge_status = Column(Text)
    datetime_challenge_sent = Column(DateTime)   
    datetime_challenge_responded_to = Column(DateTime)   
    datetime_challenge_verified = Column(DateTime)   
    block_hash_when_challenge_sent = Column(Text)
    challenge_response_time_in_seconds = Column(Float)
    challenging_masternode_id = Column(Text)
    responding_masternode_id = Column(Text)
    file_hash_to_challenge = Column(Text, ForeignKey('symbol_files.file_hash'))
    challenge_slice_start_index = Column(Integer)
    challenge_slice_end_index = Column(Integer)
    challenge_slice_correct_hash = Column(Text)
    challenge_response_hash = Column(Text)

class Challenge_Messages(Base):
    __tablename__ = 'challenge_messages'
    message_id = Column(Text, primary_key=True, index=True)
    message_type = Column(Text)
    challenge_status = Column(Text)
    datetime_challenge_sent = Column(DateTime)
    datetime_challenge_responded_to = Column(DateTime)   
    datetime_challenge_verified = Column(DateTime)    
    block_hash_when_challenge_sent = Column(Text, ForeignKey('pastel_blocks.block_hash'))
    challenging_masternode_id = Column(Text, ForeignKey('masternodes.masternode_id'))
    responding_masternode_id = Column(Text, ForeignKey('masternodes.masternode_id'))
    file_hash_to_challenge = Column(Text, ForeignKey('symbol_files.file_hash'))
    challenge_slice_start_index = Column(Integer)
    challenge_slice_end_index = Column(Integer)
    challenge_slice_correct_hash = Column(Text)
    challenge_response_hash = Column(Text)
    challenge_id = Column(Text, ForeignKey('challenges.challenge_id'))
