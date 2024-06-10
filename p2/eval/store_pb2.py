# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: store.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bstore.proto\"(\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1e\n\x0bPutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1c\n\x0bGetResponse\x12\r\n\x05value\x18\x01 \x01(\t\"\"\n\x0fSlowDownRequest\x12\x0f\n\x07seconds\x18\x01 \x01(\x05\"#\n\x10SlowDownResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x10\n\x0eRestoreRequest\"\"\n\x0fRestoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty\".\n\x10\x43\x61nCommitRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"&\n\x11\x43\x61nCommitResponse\x12\x11\n\tcanCommit\x18\x01 \x01(\x08\"-\n\x0f\x44oCommitRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1b\n\x0c\x41\x62ortRequest\x12\x0b\n\x03key\x18\x01 \x01(\t2\xa3\x02\n\rKeyValueStore\x12 \n\x03put\x12\x0b.PutRequest\x1a\x0c.PutResponse\x12 \n\x03get\x12\x0b.GetRequest\x1a\x0c.GetResponse\x12/\n\x08slowDown\x12\x10.SlowDownRequest\x1a\x11.SlowDownResponse\x12#\n\x07restore\x12\x06.Empty\x1a\x10.RestoreResponse\x12\x32\n\tcanCommit\x12\x11.CanCommitRequest\x1a\x12.CanCommitResponse\x12$\n\x08\x64oCommit\x12\x10.DoCommitRequest\x1a\x06.Empty\x12\x1e\n\x05\x61\x62ort\x12\r.AbortRequest\x1a\x06.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'store_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PUTREQUEST']._serialized_start=15
  _globals['_PUTREQUEST']._serialized_end=55
  _globals['_PUTRESPONSE']._serialized_start=57
  _globals['_PUTRESPONSE']._serialized_end=87
  _globals['_GETREQUEST']._serialized_start=89
  _globals['_GETREQUEST']._serialized_end=114
  _globals['_GETRESPONSE']._serialized_start=116
  _globals['_GETRESPONSE']._serialized_end=144
  _globals['_SLOWDOWNREQUEST']._serialized_start=146
  _globals['_SLOWDOWNREQUEST']._serialized_end=180
  _globals['_SLOWDOWNRESPONSE']._serialized_start=182
  _globals['_SLOWDOWNRESPONSE']._serialized_end=217
  _globals['_RESTOREREQUEST']._serialized_start=219
  _globals['_RESTOREREQUEST']._serialized_end=235
  _globals['_RESTORERESPONSE']._serialized_start=237
  _globals['_RESTORERESPONSE']._serialized_end=271
  _globals['_EMPTY']._serialized_start=273
  _globals['_EMPTY']._serialized_end=280
  _globals['_CANCOMMITREQUEST']._serialized_start=282
  _globals['_CANCOMMITREQUEST']._serialized_end=328
  _globals['_CANCOMMITRESPONSE']._serialized_start=330
  _globals['_CANCOMMITRESPONSE']._serialized_end=368
  _globals['_DOCOMMITREQUEST']._serialized_start=370
  _globals['_DOCOMMITREQUEST']._serialized_end=415
  _globals['_ABORTREQUEST']._serialized_start=417
  _globals['_ABORTREQUEST']._serialized_end=444
  _globals['_KEYVALUESTORE']._serialized_start=447
  _globals['_KEYVALUESTORE']._serialized_end=738
# @@protoc_insertion_point(module_scope)
