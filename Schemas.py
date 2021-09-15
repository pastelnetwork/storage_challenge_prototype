from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Masternodes(BaseModel):
    masternode_id: str
    masternode_ip_address: Optional[str] = None
    total_challenges_issued: Optional[int] = None
    total_challenges_responded_to: Optional[int] = None
    total_challenges_correct: Optional[int] = None
    total_challenges_incorrect: Optional[int] = None
    total_challenges_correct_but_too_slow: Optional[int] = None
    total_challenges_never_responded_to: Optional[int] = None
    challenge_response_success_rate_pct: Optional[float] = None
    class Config:
        orm_mode = True

class Pastel_Blocks(BaseModel):
    block_hash: str
    block_number: Optional[int] = None
    total_challenges_issued: Optional[int] = None
    total_challenges_responded_to: Optional[int] = None
    total_challenges_correct: Optional[int] = None
    total_challenges_incorrect: Optional[int] = None
    total_challenges_correct_but_too_slow: Optional[int] = None
    total_challenges_never_responded_to: Optional[int] = None
    challenge_response_success_rate_pct: Optional[float] = None
    class Config:
        orm_mode = True

class Symbol_Files(BaseModel):
    file_hash: str
    file_length_in_bytes: Optional[int] = None
    total_challenges_for_file: Optional[int] = None
    original_file_path: Optional[str] = None
    class Config:
        orm_mode = True

class XOR_Distance(BaseModel):
    xor_distance_id: int
    masternode_id: Optional[str] = None
    file_hash: Optional[str] = None
    xor_distance: Optional[int] = None
    class Config:
        orm_mode = True

class Challenges(BaseModel):
    challenge_id: str
    challenge_status: str
    datetime_challenge_sent: datetime
    datetime_challenge_responded_to: Optional[datetime] = None
    datetime_challenge_verified: Optional[datetime] = None
    block_hash_when_challenge_sent: str
    challenge_response_time_in_seconds: Optional[float] = None
    challenging_masternode_id: str
    responding_masternode_id: str
    file_hash_to_challenge: str
    challenge_slice_start_index: Optional[int] = None
    challenge_slice_end_index: Optional[int] = None
    challenge_slice_correct_hash: Optional[str] = None
    challenge_response_hash: Optional[str] = None
    class Config:
        orm_mode = True

class Challenge_Messages(BaseModel):
    message_id: str
    message_type: str
    challenge_status: str
    datetime_challenge_sent: Optional[datetime] = None
    datetime_challenge_responded_to: Optional[datetime] = None
    datetime_challenge_verified: Optional[datetime] = None
    block_hash_when_challenge_sent: str
    challenging_masternode_id: str
    responding_masternode_id: str
    file_hash_to_challenge: str
    challenge_slice_start_index: Optional[int] = None
    challenge_slice_end_index: Optional[int] = None
    challenge_slice_correct_hash: Optional[int] = None
    challenge_response_hash: Optional[str] = None
    class Config:
        orm_mode = True
