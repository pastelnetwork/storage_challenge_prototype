import hashlib, sqlite3, glob, os, io, time, random, base64, functools, warnings, platform, sys, signal, json, shutil, imghdr, logging, math, requests #Python stdlib
from random import randint
import scipy
import numpy as np
import pandas as pd
from configparser import ConfigParser
from datetime import datetime
from secrets import choice
import string
import uuid
import asyncio  
import nest_asyncio
import requests
import json
from dateutil.parser import parse
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import event
import Models, Schemas
from Database import SessionLocal, engine
if 0:
    from pyinstrument import Profiler
    profiler = Profiler()
    profiler.start()

nest_asyncio.apply()
folder_path_containing_sample_raptorq_symbol_files = './sample_raptorq_symbol_files/'
rqsymbol_file_storage_data_folder_path = './rqsymbol_files_stored_by_masternodes/'

Models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_sha256_hash_of_input_data_func(input_data_or_string):
    if isinstance(input_data_or_string, str):
        input_data_or_string = input_data_or_string.encode('utf-8')
    sha256_hash_of_input_data = hashlib.sha3_256(input_data_or_string).hexdigest()
    return sha256_hash_of_input_data

def generate_fake_block_hashes_func(number_of_blocks_to_make):
    list_of_block_hashes = [get_sha256_hash_of_input_data_func(str(x)) for x in range(number_of_blocks_to_make)]
    return list_of_block_hashes

def generate_fake_pastel_mn_id_func():
    fake_id = 'jX'
    fake_id = fake_id + ''.join([choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(84)])
    return fake_id
        
if 0:
    list_of_pastel_masternode_ids = [generate_fake_pastel_mn_id_func() for x in range(25)]

list_of_pastel_masternode_ids = ['jX2Oo9VqcP4hPOTNJVC5eGqnY5tXNoSdDdHEIuKcaUQ6VKw68CGmqhG9FWb5XU67YAzVMtDf9Io8HLfVpCp1Pc',
                                 'jXS9NIXHj8pd9mLNsP2uKgIh1b3EH2aq5dwupUF7hoaltTE8Zlf6R7Pke0cGr071kxYxqXHQmfVO5dA4jH0ejQ',
                                 'jX8oThrVrg0ZYhz3qXzv698LZOy2QG33R9w4eXTzKzCKBEWW9TU6R13TnjxDJAshEsWxFkRE0pPwoIvPEJJu6I',
                                 'jX6K2iP24sWtyU9wCnE99emxbz4QxCk2n43WfRuBweYTVvv0AencLFhXwUUu33G1siQIE3LQaiZh2ZSxgGcHEG',
                                 'jXRXfG5kV1FYWKABT88mupZaDm6LCMgHUGtMjRYgYG1AYxvWk5hkTDRBov4H2Ksn0USNxGuX61c4OYbP9uqg4I',
                                 'jXOvtvYxXUMCc83kWWvdOwUk4do4PCeRHcONECxu9TMwpqJ6l0b5fkUCby4AKBUEumt5tzWrytAoGgZBRL6WHq',
                                 'jXxveMgUk0VrYSYOD3Pt4Vqo2GtPMfWW6NO6WUpieKcT1PGeeXDk4TSqifIGumxRvQE5YuJDzXlYmHISgljt98',
                                 'jXEZVtIEVmSkYw0v8qGjsBrrELBOPuedNYMctelLWSlw6tiVNljFMpZFir30SN9r645tEAKwEAYfKR3o4Ek5YM',
                                 'jXVmx86fiMALiMr1HwkcS6fLpdHZkIRxZ111wPyfuZtrmqtaupxg5EVV2HNgEW71tzrCQoAS0lOV35mpqAqvsE',
                                 'jXYiHNqO9B7psxFQZb1thEgDNykZjL8GkHMZNPZx3iCYre1j3g0zHynlTQ9TdvY6dcRlYIsNfwIQ6nVXBSVJis',
                                 'jXpDb5K6S81ghCusMOXLP6k0RvqgFhkBJSFf6OhjEmpvCWGZiptRyRgfQ9cTD709sA58m5czpipFnvpoHuPX0F',
                                 'jXqBzHsk8P1cuRFrsRkQR5IhPzwFyCxE369KYqFLSITr8l5koLWcabZZDUVltIJ8666bE53G5fbtCz4veU2FCP',
                                 'jX4E9LLzsP3Q8lVbT8QxFsgKf1ggDAKaC9EJoM1CvNFlhD81NmgpFLjCcQhP99UvheIid7NwYDQR9QvzRrwuSA',
                                 'jXLzzFEMzls4IpwFpN1QC5mQFFhACgH1A3jRCkZ1OE3s0gxOndMtdFI9UOFkIzTDOTl6omYThNOFcbz3ajqYX4',
                                 'jXdDgE3szIzRHzXUJZBlk8f097Peqje7Kz92vzsDuCtNDHLJxw2dqQZRlQXTGjpR2pw13Rpct3xe0XFhFJlNuv',
                                 'jX5jep6veu2fvSR9CJbCAsi1Y0g6SuOV1p7GVTf1BOWwvyfs0hsO7ZxA9eqWsjrVbdg80IjCFlhBrFF8EHqFFa',
                                 'jXNtmNRYVQoRCZK3BURcJ1mqusS856p9OX4eZH8iTPhDaFPV2OiTf875JzAwZs1sbIbQSYCrBFstUP4FNTheBb',
                                 'jXTqmW8sZgDbCnNNdhAqoBBDyP5zHD2VK2fw4FURPyi7oDx0w41Ifb0RA0ny3hvTvQHcOnFdmiyqHE5Sp3gbIa',
                                 'jXljm8vYKP41PCXixn7pHge75nuPy7sVLiwvNTwvMv4QHBAoUvnpXTNJOwGJNlEqKViLqe5qrjJ95Oj1qg4xtv',
                                 'jXzriQGf1FY5GOy7vyA0tOUUscfwugzUutPL5NyFuhCIeYNd7AAbsHxdnSS8Pgxoxd4hU6e16sWI6gh0CpegZv',
                                 'jXTwS1eCNDopMUIZAQnvpGlVe9lEnbauoh8TNDRoZcRTJVxCmZu1oSySBM1UwwyHDh7npbn01tZG0q2xyGmVJr',
                                 'jXl8wiIuix4QxZsdhtnxye7bJn5z1M3yBEw0JxsB8vAb3Yb6VCrfHH3al8iCvcJjQTVdsMOCppEfVfk0TgfQ5r',
                                 'jXD8SVytGpv7qDzCY0rjUNE2gi24jLpdihupm5pD7u1plOBL6fB7zFIddA8ezubp0Bl2dnxfptQSFhdCOYwqq2',
                                 'jXIC54zVCSUqITW3bAZw5rvu2lUwl5c9qMeI1hxm3VRBlYG7v71aGRTX55JbVonKsk80DdCv23VSLiKq2ao3V7',
                                 'jXlzy0y3L1gYG04DBEZSKI9KV5BReiRzrW5bDBls3M2gtS6R0Ed8MHrEW9hzzgi4aW1taxNzChPSHEgJY4aTbw']    

total_number_of_masternode_ids = len(list_of_pastel_masternode_ids)
list_of_raptorq_symbol_file_paths = glob.glob(folder_path_containing_sample_raptorq_symbol_files + '*')
total_number_of_raptorq_symbol_files = len(list_of_raptorq_symbol_file_paths)


def get_hash_from_file_path_func(path_to_file):
    try:
        with open(path_to_file,'rb') as f:
            file_binary_data = f.read()
        sha256_hash_of_file = get_sha256_hash_of_input_data_func(file_binary_data)
        return sha256_hash_of_file
    except Exception as e:
        print('Error: '+ str(e))
        
class MyTimer():
    def __init__(self):
        self.start = time.time()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = '({time} seconds to complete)'
        print(msg.format(time=round(runtime,2)))        

def datetime_parser_func(value):
    if isinstance(value, dict):
        for k, v in value.items():
            value[k] = datetime_parser_func(v)
    elif isinstance(value, list):
        for index, row in enumerate(value):
            value[index] = datetime_parser_func(row)
    elif isinstance(value, str) and value:
        try:
            value = parse(value)
        except (ValueError, AttributeError):
            pass
    return value

def compute_elapsed_time_in_seconds_between_two_datetimes_func(start_datetime, end_datetime):
    time_delta = (end_datetime - start_datetime)
    total_seconds_elapsed = time_delta.total_seconds()
    return total_seconds_elapsed

def string_to_binary_func(input_string):
    input_as_binary = ''.join(format(x, 'b') for x in bytearray(input_string, 'utf-8'))
    return input_as_binary

def bytes_to_int_func(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def compute_xor_distance_between_two_strings_func(string_1, string_2):
    string_1_hash = hashlib.sha3_256(string_1.encode('utf-8')).hexdigest()
    string_2_hash = hashlib.sha3_256(string_2.encode('utf-8')).hexdigest()
    string_1_hash_as_bytes = np.frombuffer(string_1_hash.encode('utf-8'), dtype='uint8')
    string_2_hash_as_bytes = np.frombuffer(string_2_hash.encode('utf-8'), dtype='uint8')
    xor_distance = (string_1_hash_as_bytes ^ string_2_hash_as_bytes).tobytes()
    xor_distance_as_int = bytes_to_int_func(xor_distance)
    return xor_distance_as_int

def compute_masternode_id_to_file_hash_xor_distance_matrix_func(list_of_pastel_masternode_ids, list_of_raptorq_symbol_file_hashes):
    print('Generating XOR distance matrix...')
    with MyTimer():
        xor_distance_df = pd.DataFrame(np.zeros((len(list_of_raptorq_symbol_file_hashes), len(list_of_pastel_masternode_ids))))
        xor_distance_df.columns = list_of_pastel_masternode_ids
        xor_distance_df.index = list_of_raptorq_symbol_file_hashes
        for idx1, current_masternode_id in enumerate(list_of_pastel_masternode_ids):
            for idx2, current_file_hash in enumerate(list_of_raptorq_symbol_file_hashes):
                xor_distance_df.iloc[idx2,idx1] = compute_xor_distance_between_two_strings_func(current_masternode_id, current_file_hash)
    return xor_distance_df

def get_n_closest_file_hashes_to_a_given_masternode_id_func(n, xor_distance_df, masternode_id_string):
    xor_distance_df__filtered__sorted = xor_distance_df[masternode_id_string].sort_values(ascending=True)
    top_n_closest_file_hashes = xor_distance_df__filtered__sorted[0:n].index.tolist()
    return top_n_closest_file_hashes

def get_n_closest_masternode_ids_to_a_given_file_hash_func(n, xor_distance_df, file_hash_string):
    xor_distance_df__filtered__sorted = xor_distance_df[xor_distance_df.index==file_hash_string].T.sort_values(file_hash_string, ascending=True)
    top_n_closest_masternode_ids = xor_distance_df__filtered__sorted[0:n].index.tolist()
    return top_n_closest_masternode_ids

def get_n_closest_masternode_ids_to_a_given_comparison_string_func(n, comparison_string, list_of_pastel_masternode_ids):
    xor_distance_df = pd.DataFrame(np.zeros((1, len(list_of_pastel_masternode_ids))))
    xor_distance_df.columns = list_of_pastel_masternode_ids
    xor_distance_df.index = [comparison_string]
    for idx, current_masternode_id in enumerate(list_of_pastel_masternode_ids):
        xor_distance_df.iloc[0, idx] = compute_xor_distance_between_two_strings_func(current_masternode_id, comparison_string)
    xor_distance_df__sorted = xor_distance_df.T.sort_values(comparison_string, ascending=True)
    top_n_closest_masternode_ids = xor_distance_df__sorted[0:n].index.tolist()
    return top_n_closest_masternode_ids

def get_n_closest_file_hashes_to_a_given_comparison_string_func(n, comparison_string, list_of_file_hashes):
    xor_distance_df = pd.DataFrame(np.zeros((1, len(list_of_file_hashes))))
    xor_distance_df.columns = list_of_file_hashes
    xor_distance_df.index = [comparison_string]
    for idx, current_filehash in enumerate(list_of_file_hashes):
        xor_distance_df.iloc[0, idx] = compute_xor_distance_between_two_strings_func(current_filehash, comparison_string)
    xor_distance_df__sorted = xor_distance_df.T.sort_values(comparison_string, ascending=True)
    top_n_closest_file_hashes = xor_distance_df__sorted[0:n].index.tolist()
    return top_n_closest_file_hashes

def get_storage_challenge_slice_indices_func(total_data_length_in_bytes, file_hash_string, block_hash_string, challenging_masternode_id):
    step_size_for_indices = int(str(int(block_hash_string, 16))[-1] + str(int(block_hash_string, 16))[0])  #it's pretty slow if we use a step-size of 1
    comparison_string = block_hash_string + file_hash_string + challenging_masternode_id
    list_of_xor_distances_of_indices_to_block_hash = [compute_xor_distance_between_two_strings_func(str(x), comparison_string) for x in range(0, total_data_length_in_bytes, step_size_for_indices)]
    list_of_sorted_indices = np.argsort(list_of_xor_distances_of_indices_to_block_hash)
    list_of_sorted_indices_with_step_size = np.array([x for x in range(0, total_data_length_in_bytes, step_size_for_indices)])[list_of_sorted_indices].tolist()
    first_two_sorted_indices = list_of_sorted_indices_with_step_size[0:2]
    challenge_slice_start_index = min(first_two_sorted_indices)
    challenge_slice_end_index = max(first_two_sorted_indices)
    return challenge_slice_start_index, challenge_slice_end_index

def get_file_path_from_file_hash_func(file_hash_string, list_of_raptorq_symbol_file_hashes, list_of_raptorq_symbol_file_paths):
    file_hash_to_path_dict = dictionary = dict(zip(list_of_raptorq_symbol_file_hashes, list_of_raptorq_symbol_file_paths))
    file_path = file_hash_to_path_dict[file_hash_string]    
    return file_path

def compute_hash_of_file_slice_func(file_data, challenge_slice_start_index, challenge_slice_end_index):
    challenge_data_slice = file_data[challenge_slice_start_index:challenge_slice_end_index]
    hash_of_data_slice = get_sha256_hash_of_input_data_func(challenge_data_slice)
    return hash_of_data_slice

def generate_test_folders_and_files_func(xor_distance_df):
    global number_of_files_each_masternode_should_store
    global list_of_raptorq_symbol_file_paths
    global rqsymbol_file_storage_data_folder_path
    global folder_path_containing_sample_raptorq_symbol_files
    global number_of_challenge_replicas
    list_of_raptorq_symbol_file_hashes = xor_distance_df.index.tolist()
    list_of_pastel_masternode_ids = xor_distance_df.columns.tolist()
    list_of_all_sample_rqsymbol_file_paths = glob.glob(folder_path_containing_sample_raptorq_symbol_files + '*')
    if not os.path.exists(rqsymbol_file_storage_data_folder_path):
        try:
            os.mkdir(rqsymbol_file_storage_data_folder_path)
        except:
            pass
        for current_masternode_id in list_of_pastel_masternode_ids:
            try:
                current_masternode_folder_path = rqsymbol_file_storage_data_folder_path + current_masternode_id
                os.mkdir(current_masternode_folder_path)
            except:
                pass
    print('Assigning ' + str(len(list_of_all_sample_rqsymbol_file_paths)) + ' files to ' + str(len(list_of_pastel_masternode_ids)) + ' different masternodes...')
    with MyTimer():
        for current_file_path in list_of_all_sample_rqsymbol_file_paths:
            current_file_hash = get_hash_from_file_path_func(current_file_path)
            masternode_ids_that_should_store_current_file = get_n_closest_masternode_ids_to_a_given_file_hash_func(number_of_challenge_replicas, xor_distance_df, current_file_hash)
            for idx, current_masternode_id in enumerate(masternode_ids_that_should_store_current_file):
                current_masternode_folder_path = rqsymbol_file_storage_data_folder_path + current_masternode_id
                renamed_destination_file_name = current_file_hash + '.rqs'
                try:
                    shutil.copy(current_file_path, current_masternode_folder_path + os.sep + renamed_destination_file_name)
                except:
                    pass
    print('Done generating test folder structure and files!')


def reset_folder_state_func():
    global rqsymbol_file_storage_data_folder_path
    shutil.rmtree(rqsymbol_file_storage_data_folder_path, ignore_errors=True)
    print('Resetting rqsymbol storage folders (and files) by deleting them!')

def check_for_local_filepath_for_file_hash_func(masternode_id, file_hash):
    global rqsymbol_file_storage_data_folder_path
    masternode_storage_path = rqsymbol_file_storage_data_folder_path + masternode_id + os.sep
    masternode_storage_path_glob_matches = glob.glob(masternode_storage_path + file_hash + '.rqs')
    filepath_for_file_hash = ''
    if len(masternode_storage_path_glob_matches) > 0:
        filepath_for_file_hash = masternode_storage_path_glob_matches[0]
    return filepath_for_file_hash
        
def update_db_with_message_func(storage_challenge_message_dict):
    x = storage_challenge_message_dict
    db_record_update = Models.Challenge_Messages(
        message_id = x['message_id'],
        message_type = x['message_type'],
        challenge_status = x['challenge_status'],
        datetime_challenge_sent = x['datetime_challenge_sent'],
        datetime_challenge_responded_to = x['datetime_challenge_responded_to'],
        datetime_challenge_verified = x['datetime_challenge_verified'],
        block_hash_when_challenge_sent = x['block_hash_when_challenge_sent'],
        challenging_masternode_id = x['challenging_masternode_id'],
        responding_masternode_id = x['responding_masternode_id'],
        file_hash_to_challenge = x['file_hash_to_challenge'],
        challenge_slice_start_index = x['challenge_slice_start_index'],
        challenge_slice_end_index = x['challenge_slice_end_index'],
        challenge_slice_correct_hash = x['challenge_slice_correct_hash'],
        challenge_response_hash = x['challenge_response_hash'],
        challenge_id = x['challenge_id'],
        )
    with SessionLocal() as db:
        db.add(db_record_update)
        db.commit()
        challenge_id_input_data = x['challenging_masternode_id'] + x['responding_masternode_id'] + x['file_hash_to_challenge'] + str(x['challenge_slice_start_index']) + str(x['challenge_slice_end_index']) + str(x['datetime_challenge_sent'])
        challenge_id = get_sha256_hash_of_input_data_func(challenge_id_input_data)
        db_record_update2 = Models.Challenges(
            challenge_id = challenge_id,
            challenge_status = x['challenge_status'],
            datetime_challenge_sent = x['datetime_challenge_sent'],
            datetime_challenge_responded_to = x['datetime_challenge_responded_to'],
            datetime_challenge_verified = x['datetime_challenge_verified'],
            block_hash_when_challenge_sent = x['block_hash_when_challenge_sent'],
            challenging_masternode_id = x['challenging_masternode_id'],
            responding_masternode_id = x['responding_masternode_id'],
            file_hash_to_challenge = x['file_hash_to_challenge'],
            challenge_slice_start_index = x['challenge_slice_start_index'],
            challenge_slice_end_index = x['challenge_slice_end_index'],
            challenge_slice_correct_hash = x['challenge_slice_correct_hash'],
            )    
        db.merge(db_record_update2)
        db.commit()
        db.close()
    
def add_files_to_db_func():
    global folder_path_containing_sample_raptorq_symbol_files
    list_of_file_paths = glob.glob(folder_path_containing_sample_raptorq_symbol_files + '*')
    with SessionLocal() as db:
        for current_file_path in list_of_file_paths:
            with open(current_file_path, 'rb') as f:
                challenge_file_data = f.read()
            challenge_data_size = len(challenge_file_data)
            input_file_hash = get_sha256_hash_of_input_data_func(challenge_file_data)
            db_record_update = Models.Symbol_Files(file_hash = input_file_hash, file_length_in_bytes = challenge_data_size, )
            db.merge(db_record_update)
        db.commit()
        db.close()

def add_masternodes_to_db_func(xor_distance_df):
    list_of_pastel_masternode_ids = xor_distance_df.columns.tolist()
    list_of_file_paths = glob.glob(folder_path_containing_sample_raptorq_symbol_files + '*')
    with SessionLocal() as db:
        for current_masternode_id in list_of_pastel_masternode_ids:
            masternode_ip_address = '192.1.1.2'
            db_record_update = Models.Masternodes(masternode_id = current_masternode_id, masternode_ip_address = masternode_ip_address, )
            db.merge(db_record_update)
        db.commit()
        db.close()

def add_blocks_to_db_func(list_of_block_hashes):
    with SessionLocal() as db:
        for blocknumber, current_block_hash in enumerate(list_of_block_hashes):
            db_record_update = Models.Pastel_Blocks(block_hash = current_block_hash, block_number = blocknumber + 1, )
            db.merge(db_record_update)
        db.commit()
        db.close()

def generate_storage_challenges_func(challenging_masternode_id, xor_distance_df, current_block_hash, challenges_per_masternode_per_block):
    global number_of_challenge_replicas
    global number_of_files_each_masternode_should_store
    global null_date
    list_of_message_ids = []
    list_of_raptorq_symbol_file_hashes = xor_distance_df.index.tolist()
    list_of_pastel_masternode_ids = xor_distance_df.columns.tolist()
    list_to_check_if_file_contained_by_local_masternode  = [z!='' for z in [check_for_local_filepath_for_file_hash_func(challenging_masternode_id, x) for x in list_of_raptorq_symbol_file_hashes]]
    list_of_file_hashes_stored_by_challenger = [list_of_raptorq_symbol_file_hashes[idx] for idx, x in enumerate(list_to_check_if_file_contained_by_local_masternode ) if x==True]
    comparison_string_for_file_hash_selection = current_block_hash + challenging_masternode_id 
    list_of_file_hashes_to_challenge = get_n_closest_file_hashes_to_a_given_comparison_string_func(challenges_per_masternode_per_block, comparison_string_for_file_hash_selection, list_of_file_hashes_stored_by_challenger)
    list_of_masternodes_to_challenge = ['' for x in list_of_file_hashes_to_challenge]
    print('Challenging Masternode ' + challenging_masternode_id + ' is now selecting file hashes to challenge this block, and then for each one, selecting which Masternode to challenge...')
    with MyTimer():
        for idx, current_file_hash_to_challenge in enumerate(list_of_file_hashes_to_challenge):
            list_of_masternodes_storing_file_hash = get_n_closest_masternode_ids_to_a_given_file_hash_func(number_of_challenge_replicas, xor_distance_df, current_file_hash_to_challenge)
            list_of_masternodes_storing_file_hash_excluding_challenger = [x for x in list_of_masternodes_storing_file_hash if x!=challenging_masternode_id]
            comparison_string_for_masternode_selection = current_block_hash + current_file_hash_to_challenge + challenging_masternode_id + get_sha256_hash_of_input_data_func(str(idx))
            responding_masternode_id = get_n_closest_masternode_ids_to_a_given_comparison_string_func(1, comparison_string_for_masternode_selection, list_of_masternodes_storing_file_hash_excluding_challenger)[0]
            list_of_masternodes_to_challenge[idx] = responding_masternode_id
    for idx, current_file_hash_to_challenge in enumerate(list_of_file_hashes_to_challenge):
        filepath_for_challenge_file_hash = check_for_local_filepath_for_file_hash_func(challenging_masternode_id, current_file_hash_to_challenge)
        if len(filepath_for_challenge_file_hash) > 0:
            with open(filepath_for_challenge_file_hash, 'rb') as f:
                challenge_file_data = f.read()
            challenge_data_size = len(challenge_file_data)
            if challenge_data_size > 0:
                responding_masternode_id = list_of_masternodes_to_challenge[idx]
                challenge_status = 'Pending'
                challenge_slice_start_index, challenge_slice_end_index = get_storage_challenge_slice_indices_func(challenge_data_size, current_file_hash_to_challenge, current_block_hash, challenging_masternode_id)
                challenge_data_slice = challenge_file_data[challenge_slice_start_index:challenge_slice_end_index]
                datetime_challenge_sent = datetime.now()
                message_id_input_data = challenging_masternode_id + responding_masternode_id + current_file_hash_to_challenge + str(datetime_challenge_sent) + challenge_status
                message_id = get_sha256_hash_of_input_data_func(message_id_input_data)
                list_of_message_ids = list_of_message_ids + [message_id]
                challenge_id_input_data = challenging_masternode_id + responding_masternode_id + current_file_hash_to_challenge + str(challenge_slice_start_index) + str(challenge_slice_end_index) + str(datetime_challenge_sent)
                challenge_id = get_sha256_hash_of_input_data_func(challenge_id_input_data)
                storage_challenge_message_dict = {'message_id': message_id,
                                                  'message_type': 'storage_challenge_issuance_message',
                                                  'challenge_status': challenge_status,
                                                  'datetime_challenge_sent': datetime_challenge_sent,
                                                  'datetime_challenge_responded_to': None,
                                                  'datetime_challenge_verified': None,
                                                  'block_hash_when_challenge_sent': current_block_hash,
                                                  'challenging_masternode_id': challenging_masternode_id,
                                                  'responding_masternode_id': responding_masternode_id,
                                                  'file_hash_to_challenge': current_file_hash_to_challenge,
                                                  'challenge_slice_start_index': challenge_slice_start_index,
                                                  'challenge_slice_end_index': challenge_slice_end_index,
                                                  'challenge_slice_correct_hash': None,
                                                  'challenge_response_hash': None,
                                                  'challenge_id': challenge_id}
                update_db_with_message_func(storage_challenge_message_dict)
                print('\nMasternode ' + challenging_masternode_id + ' issued a storage challenge to Masternode ' + responding_masternode_id + ' for file hash ' + current_file_hash_to_challenge + ' (start index: ' + str(challenge_slice_start_index) + '; end index: ' + str(challenge_slice_end_index) + ')')
            else:
                print('\nMasternode ' + challenging_masternode_id + ' encountered an invalid file while attempting to generate a storage challenge for file hash ' + current_file_hash_to_challenge)
        else:
            print('\nMasternode ' + challenging_masternode_id + ' encountered an error generating storage challenges')
    return list_of_message_ids

def update_masternode_stats_in_db_func(xor_distance_df):
    list_of_pastel_masternode_ids = xor_distance_df.columns.tolist()
    total_challenges_issued = 0
    total_challenges_responded_to = 0
    total_challenges_correct = 0
    total_challenges_incorrect = 0
    total_challenges_correct_but_too_slow = 0
    challenges_never_responded_to = 0
    with SessionLocal() as db:
        for current_masternode_id in list_of_pastel_masternode_ids:
            challenges_issued = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.responding_masternode_id==current_masternode_id).filter(Models.Challenge_Messages.message_type=='storage_challenge_issuance_message').all()
            total_challenges_issued = len(challenges_issued)
            challenges_responded_to = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.responding_masternode_id==current_masternode_id).filter(Models.Challenge_Messages.challenge_status=='Responded').all()
            total_challenges_responded_to = len(challenges_responded_to)
            challenges_correct = db.query(Models.Challenges).filter(Models.Challenges.responding_masternode_id==current_masternode_id).filter(Models.Challenges.challenge_status=='Successful response').all()
            total_challenges_correct = len(challenges_correct)
            challenges_incorrect = db.query(Models.Challenges).filter(Models.Challenges.responding_masternode_id==current_masternode_id).filter(Models.Challenges.challenge_status=='Failed because of incorrect response').all()
            total_challenges_incorrect = len(challenges_incorrect)
            challenges_correct_but_too_slow = db.query(Models.Challenges).filter(Models.Challenges.responding_masternode_id==current_masternode_id).filter(Models.Challenges.challenge_status=='Failed--Correct but response was too slow').all()
            total_challenges_correct_but_too_slow = len(challenges_correct_but_too_slow)
            challenges_never_responded_to = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.responding_masternode_id==current_masternode_id).filter(Models.Challenge_Messages.challenge_status=='Failed because response never arrived').all()
            total_challenges_never_responded_to = len(challenges_never_responded_to)            
            if total_challenges_issued > 0:
                challenge_response_success_rate_pct = total_challenges_correct/total_challenges_issued
            else:
                challenge_response_success_rate_pct = 1.0
            db_record_update = Models.Masternodes(masternode_id = current_masternode_id, total_challenges_issued = total_challenges_issued, total_challenges_responded_to = total_challenges_responded_to, total_challenges_correct = total_challenges_correct, total_challenges_incorrect = total_challenges_incorrect, total_challenges_correct_but_too_slow = total_challenges_correct_but_too_slow, total_challenges_never_responded_to = total_challenges_never_responded_to, challenge_response_success_rate_pct = challenge_response_success_rate_pct)
            db.merge(db_record_update)
        db.commit()
        db.close()

def update_block_stats_in_db_func(list_of_block_hashes):
    total_challenges_issued = 0
    total_challenges_responded_to = 0
    total_challenges_correct = 0
    total_challenges_incorrect = 0
    total_challenges_correct_but_too_slow = 0
    challenges_never_responded_to = 0
    with SessionLocal() as db:
        for current_block_hash in list_of_block_hashes:
            challenges_issued = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.block_hash_when_challenge_sent==current_block_hash).filter(Models.Challenge_Messages.message_type=='storage_challenge_issuance_message').all()
            total_challenges_issued = len(challenges_issued)
            challenges_responded_to = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.block_hash_when_challenge_sent==current_block_hash).filter(Models.Challenge_Messages.challenge_status=='Responded').all()
            total_challenges_responded_to = len(challenges_responded_to)
            challenges_correct = db.query(Models.Challenges).filter(Models.Challenges.block_hash_when_challenge_sent==current_block_hash).filter(Models.Challenges.challenge_status=='Successful response').all()
            total_challenges_correct = len(challenges_correct)
            challenges_incorrect = db.query(Models.Challenges).filter(Models.Challenges.block_hash_when_challenge_sent==current_block_hash).filter(Models.Challenges.challenge_status=='Failed because of incorrect response').all()
            total_challenges_incorrect = len(challenges_incorrect)
            challenges_correct_but_too_slow = db.query(Models.Challenges).filter(Models.Challenges.block_hash_when_challenge_sent==current_block_hash).filter(Models.Challenges.challenge_status=='Failed--Correct but response was too slow').all()
            total_challenges_correct_but_too_slow = len(challenges_correct_but_too_slow)
            challenges_never_responded_to = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.block_hash_when_challenge_sent==current_block_hash).filter(Models.Challenge_Messages.challenge_status=='Failed because response never arrived').all()
            total_challenges_never_responded_to = len(challenges_never_responded_to)            
            if total_challenges_issued > 0:
                challenge_response_success_rate_pct = total_challenges_correct/total_challenges_issued
            else:
                challenge_response_success_rate_pct = 1.0
            db_record_update = Models.Pastel_Blocks(block_hash = current_block_hash, total_challenges_issued = total_challenges_issued, total_challenges_responded_to = total_challenges_responded_to, total_challenges_correct = total_challenges_correct, total_challenges_incorrect = total_challenges_incorrect, total_challenges_correct_but_too_slow = total_challenges_correct_but_too_slow, total_challenges_never_responded_to = total_challenges_never_responded_to, challenge_response_success_rate_pct = challenge_response_success_rate_pct)
            db.merge(db_record_update)
        db.commit()
        db.close()

def respond_to_storage_challenges_func(responding_masternode_id):
    global rqsymbol_file_storage_data_folder_path
    list_of_message_ids = []
    with SessionLocal() as db:
        list_of_pending_challenge_ids = [z.asdict()['challenge_id'] for z in db.query(Models.Challenges).filter(Models.Challenges.responding_masternode_id==responding_masternode_id).filter(Models.Challenges.challenge_status=='Pending').all()]
        pending_challenge_messages = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.message_type=='storage_challenge_issuance_message').filter(Models.Challenge_Messages.challenge_id.in_(list_of_pending_challenge_ids)).all()
    for current_challenge_message in pending_challenge_messages:
        x = current_challenge_message.asdict()
        y = x.copy()
        y['message_type'] = 'storage_challenge_response_message'
        filepath_for_challenge_file_hash = check_for_local_filepath_for_file_hash_func(responding_masternode_id, x['file_hash_to_challenge'])
        print('\nMasternode ' + responding_masternode_id + ' found a new storage challenge for file hash ' + x['file_hash_to_challenge'] + ' (start index: ' + str(x['challenge_slice_start_index']) + '; end index: ' + str(x['challenge_slice_end_index']) + '), responding now!')
        if len(filepath_for_challenge_file_hash) > 0:
            with open(filepath_for_challenge_file_hash, 'rb') as f:
                challenge_file_data = f.read()
            y['challenge_response_hash'] = compute_hash_of_file_slice_func(challenge_file_data, x['challenge_slice_start_index'], x['challenge_slice_end_index'])
            challenge_status = 'Responded'
            y['challenge_status'] = challenge_status
            message_id_input_data = y['challenging_masternode_id'] + y['responding_masternode_id'] + y['file_hash_to_challenge'] + str(datetime.now()) + y['challenge_status']
            message_id = get_sha256_hash_of_input_data_func(message_id_input_data)
            y['message_id'] = message_id
            y['datetime_challenge_responded_to'] = datetime.now()
            try:
                update_db_with_message_func(y)
                list_of_message_ids = list_of_message_ids + [message_id]
                time_to_respond_to_storage_challenge_in_seconds = compute_elapsed_time_in_seconds_between_two_datetimes_func(x['datetime_challenge_sent'], datetime.now())
                print('\nMasternode ' + responding_masternode_id + ' responded to storage challenge for file hash ' + x['file_hash_to_challenge'] + ' in ' + str(time_to_respond_to_storage_challenge_in_seconds) + ' seconds!')
            except BaseException as e:
                print('Encountered Error: '+ str(e))
        else:
            print('\nMasternode ' + responding_masternode_id + ' was unable to respond to storage challenge because it did not have the file for file hash ' + x['file_hash_to_challenge'])
    return list_of_message_ids

def verify_storage_challenge_responses_func(challenging_masternode_id):
    global rqsymbol_file_storage_data_folder_path
    global max_seconds_to_respond_to_storage_challenge
    list_of_message_ids = []
    with SessionLocal() as db:
        list_of_responded_challenge_ids = [z.asdict()['challenge_id'] for z in db.query(Models.Challenges).filter(Models.Challenges.challenging_masternode_id==challenging_masternode_id).filter(Models.Challenges.challenge_status=='Responded').all()]
        responded_challenge_messages = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.message_type=='storage_challenge_response_message').filter(Models.Challenge_Messages.challenge_id.in_(list_of_responded_challenge_ids)).all()
    for idx, current_challenge_response_message in enumerate(responded_challenge_messages):
        x = current_challenge_response_message.asdict()
        print('\nMasternode ' + challenging_masternode_id + ' found a storage challenge response for file hash ' + x['file_hash_to_challenge'] + ' (start index: ' + str( x['challenge_slice_start_index']) + '; end index: ' + str(x['challenge_slice_end_index']) + ') from responding Masternode ' +  x['responding_masternode_id'] + ', verifying now!')
        y = x.copy()
        y['message_type'] = 'storage_challenge_verification_message'
        filepath_for_challenge_file_hash = check_for_local_filepath_for_file_hash_func(challenging_masternode_id, x['file_hash_to_challenge'])
        if len(filepath_for_challenge_file_hash) > 0:
            with open(filepath_for_challenge_file_hash, 'rb') as f:
                challenge_file_data = f.read()
            y['challenge_slice_correct_hash'] = compute_hash_of_file_slice_func(challenge_file_data, x['challenge_slice_start_index'], x['challenge_slice_end_index'])
            time_to_verify_storage_challenge_in_seconds = compute_elapsed_time_in_seconds_between_two_datetimes_func(x['datetime_challenge_sent'], datetime.now())
            if (y['challenge_slice_correct_hash'] == x['challenge_response_hash']) and (time_to_verify_storage_challenge_in_seconds <= max_seconds_to_respond_to_storage_challenge):
                challenge_status = 'Successful response'
                print('\nMasternode ' + x['responding_masternode_id'] + ' correctly responded in ' + str(time_to_verify_storage_challenge_in_seconds) + ' seconds to a storage challenge for file ' + x['file_hash_to_challenge'])
            elif y['challenge_slice_correct_hash'] == x['challenge_response_hash']:
                challenge_status = 'Failed--Correct but response was too slow'
                print('\nMasternode ' + x['responding_masternode_id'] + ' correctly responded in ' + str(time_to_verify_storage_challenge_in_seconds) + ' seconds to a storage challenge for file ' + x['file_hash_to_challenge'] + ', but was too slow so failed the challenge anyway!')
            else:
                challenge_status = 'Failed because of incorrect response'
                print('\nMasternode ' + x['responding_masternode_id'] + ' failed by incorrectly responding to a storage challenge for file ' + x['file_hash_to_challenge'])
        else:
            print('\nChallenging Masternode ' + challenging_masternode_id + ' was unable to verify the storage response, but it was the fault of the Challenger, so voidng challenge!')
            challenge_status = 'Void'
        y['challenge_status'] = challenge_status
        y['datetime_challenge_verified'] = datetime.now()
        message_id_input_data = y['challenging_masternode_id'] + y['responding_masternode_id'] + y['file_hash_to_challenge'] + str(datetime.now()) + y['challenge_status']
        message_id = get_sha256_hash_of_input_data_func(message_id_input_data)
        y['message_id'] = message_id
        try:
            update_db_with_message_func(y)
            list_of_message_ids = list_of_message_ids + [message_id]
        except BaseException as e:
            print('Encountered Error: '+ str(e))
    with SessionLocal() as db:
        list_of_unresponded_challenge_ids = [z.asdict()['challenge_id'] for z in db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.challenging_masternode_id==challenging_masternode_id).filter(Models.Challenge_Messages.challenge_status=='Pending').all()]
        unresponded_challenge_messages = db.query(Models.Challenge_Messages).filter(Models.Challenge_Messages.challenge_id.in_(list_of_unresponded_challenge_ids)).all()
    for current_challenge_response_message in responded_challenge_messages:
        x = current_challenge_response_message.asdict()
        time_since_storage_challenge_issued_in_seconds = compute_elapsed_time_in_seconds_between_two_datetimes_func(x['datetime_challenge_sent'], datetime.now())
        if time_since_storage_challenge_issued_in_seconds >= max_seconds_to_respond_to_storage_challenge:
            y = x.copy()
            y['message_type'] = 'storage_challenge_verification_message'
            y['challenge_status'] = 'Failed because response never arrived'
            y['datetime_challenge_verified'] = datetime.now()
            message_id_input_data = y['challenging_masternode_id'] + y['responding_masternode_id'] + y['file_hash_to_challenge'] + str(datetime.now()) + y['challenge_status']
            y['message_id'] = get_sha256_hash_of_input_data_func(message_id_input_data)
            try:
                update_db_with_message_func(y)
            except BaseException as e:
                print('Encountered Error: '+ str(e))
    return list_of_message_ids

def simulate_dishonest_masternode_func(dishonest_masternode_id, approximate_percentage_of_responsible_files_to_ignore):
    global rqsymbol_file_storage_data_folder_path
    dishonest_masternode_folder_path = rqsymbol_file_storage_data_folder_path + dishonest_masternode_id + os.sep
    list_of_responsible_files = glob.glob(dishonest_masternode_folder_path + '*')
    list_of_responsible_files_to_randomly_delete = [x for x in list_of_responsible_files if random.random() <= approximate_percentage_of_responsible_files_to_ignore]
    _ = [os.remove(x) for x in list_of_responsible_files_to_randomly_delete]

if 1:
    number_of_blocks_to_make = 1000
    number_of_storage_replicas = 5
    number_of_challenge_replicas = 10
    number_of_files_each_masternode_should_store = math.ceil((total_number_of_raptorq_symbol_files/total_number_of_masternode_ids)*number_of_challenge_replicas)
    list_of_block_hashes = generate_fake_block_hashes_func(number_of_blocks_to_make)
    list_of_raptorq_symbol_file_hashes = [get_hash_from_file_path_func(x) for x in list_of_raptorq_symbol_file_paths]
    xor_distance_df = compute_masternode_id_to_file_hash_xor_distance_matrix_func(list_of_pastel_masternode_ids, list_of_raptorq_symbol_file_hashes)
    print('Adding files to database...')
    add_files_to_db_func()
    print('Done!')
    add_masternodes_to_db_func(xor_distance_df)
    add_blocks_to_db_func(list_of_block_hashes)
    
if 0:
    challenger_mn_1 = list_of_pastel_masternode_ids[0]
    challenged_mn_1 = list_of_pastel_masternode_ids[5]
    challenging_masternode_id = challenger_mn_1
    challenging_masternode_id = challenger_mn_1
    masternode_id_string = challenged_mn_1
    responding_masternode_id = challenged_mn_1
    current_block_hash = list_of_block_hashes[0]
    
if 0:
    reset_folder_state_func()
    generate_test_folders_and_files_func(xor_distance_df)
    dishonest_masternode_id = list_of_pastel_masternode_ids[-1]
    approximate_percentage_of_responsible_files_to_ignore = 0.35
    print('Selected masternode ' + dishonest_masternode_id + ' to be a dishonest node that deleted ' + str(approximate_percentage_of_responsible_files_to_ignore*100) + '% of its raptorq symbol files...')
    simulate_dishonest_masternode_func(dishonest_masternode_id, approximate_percentage_of_responsible_files_to_ignore)

    dishonest_masternode_id = list_of_pastel_masternode_ids[-8]
    approximate_percentage_of_responsible_files_to_ignore = 0.75
    print('Selected masternode ' + dishonest_masternode_id + ' to be a dishonest node that deleted ' + str(approximate_percentage_of_responsible_files_to_ignore*100) + '% of its raptorq symbol files...')
    simulate_dishonest_masternode_func(dishonest_masternode_id, approximate_percentage_of_responsible_files_to_ignore)

    dishonest_masternode_id = list_of_pastel_masternode_ids[5]
    approximate_percentage_of_responsible_files_to_ignore = 0.15
    print('Selected masternode ' + dishonest_masternode_id + ' to be a dishonest node that deleted ' + str(approximate_percentage_of_responsible_files_to_ignore*100) + '% of its raptorq symbol files...')
    simulate_dishonest_masternode_func(dishonest_masternode_id, approximate_percentage_of_responsible_files_to_ignore)

    dishonest_masternode_id = list_of_pastel_masternode_ids[14]
    approximate_percentage_of_responsible_files_to_ignore = 0.05
    print('Selected masternode ' + dishonest_masternode_id + ' to be a dishonest node that deleted ' + str(approximate_percentage_of_responsible_files_to_ignore*100) + '% of its raptorq symbol files...')
    simulate_dishonest_masternode_func(dishonest_masternode_id, approximate_percentage_of_responsible_files_to_ignore)


if 1:
    number_of_masternodes_to_issue_challenges_per_block = len(list_of_pastel_masternode_ids)
    challenges_per_masternode_per_block = len(list_of_pastel_masternode_ids)
    max_seconds_to_respond_to_storage_challenge = 10

    for block_number, current_block_hash in enumerate(list_of_block_hashes):
        print('\n\n_____________________________________________________________________________________________________________\n\n')
        print('\n\nWaiting for next block...') 
        print('\n\nCurrent Block Number: ' + str(block_number + 1) + ' | Block Hash: ' + current_block_hash)
        list_of_challenging_masternode_ids_for_block = get_n_closest_masternode_ids_to_a_given_comparison_string_func(number_of_masternodes_to_issue_challenges_per_block, current_block_hash, list_of_pastel_masternode_ids)
        for current_masternode_id in list_of_challenging_masternode_ids_for_block:
            generate_storage_challenges_func(current_masternode_id, xor_distance_df, current_block_hash, challenges_per_masternode_per_block)
            _ = [respond_to_storage_challenges_func(x) for x in list_of_pastel_masternode_ids]
            _ = [verify_storage_challenge_responses_func(x) for x in list_of_pastel_masternode_ids]
            update_masternode_stats_in_db_func(xor_distance_df)
            update_block_stats_in_db_func(list_of_block_hashes)
            print('\n_____________________________________________________________________________________________________________\n')
            time.sleep(0.1)


if 0:
    masternode_id_string = list_of_pastel_masternode_ids[0]
    file_hash_string = list_of_raptorq_symbol_file_hashes[0]
    n = 15
    top_n_closest_file_hashes = get_n_closest_file_hashes_to_a_given_masternode_id_func(n, xor_distance_df, masternode_id_string)
    top_n_closest_masternode_ids = get_n_closest_masternode_ids_to_a_given_file_hash_func(n, xor_distance_df, file_hash_string)
    

# profiler.stop()
# profiler.print()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    