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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bstore.proto\x12\x10\x64istributedstore\"(\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1e\n\x0bPutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"+\n\x0bGetResponse\x12\r\n\x05value\x18\x01 \x01(\t\x12\r\n\x05\x66ound\x18\x02 \x01(\x08\"\"\n\x0fSlowDownRequest\x12\x0f\n\x07seconds\x18\x01 \x01(\x05\"#\n\x10SlowDownResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x10\n\x0eRestoreRequest\"\"\n\x0fRestoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty2\xba\x02\n\rKeyValueStore\x12\x42\n\x03put\x12\x1c.distributedstore.PutRequest\x1a\x1d.distributedstore.PutResponse\x12\x42\n\x03get\x12\x1c.distributedstore.GetRequest\x1a\x1d.distributedstore.GetResponse\x12Q\n\x08slowDown\x12!.distributedstore.SlowDownRequest\x1a\".distributedstore.SlowDownResponse\x12N\n\x07restore\x12 .distributedstore.RestoreRequest\x1a!.distributedstore.RestoreResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'store_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PUTREQUEST']._serialized_start=33
  _globals['_PUTREQUEST']._serialized_end=73
  _globals['_PUTRESPONSE']._serialized_start=75
  _globals['_PUTRESPONSE']._serialized_end=105
  _globals['_GETREQUEST']._serialized_start=107
  _globals['_GETREQUEST']._serialized_end=132
  _globals['_GETRESPONSE']._serialized_start=134
  _globals['_GETRESPONSE']._serialized_end=177
  _globals['_SLOWDOWNREQUEST']._serialized_start=179
  _globals['_SLOWDOWNREQUEST']._serialized_end=213
  _globals['_SLOWDOWNRESPONSE']._serialized_start=215
  _globals['_SLOWDOWNRESPONSE']._serialized_end=250
  _globals['_RESTOREREQUEST']._serialized_start=252
  _globals['_RESTOREREQUEST']._serialized_end=268
  _globals['_RESTORERESPONSE']._serialized_start=270
  _globals['_RESTORERESPONSE']._serialized_end=304
  _globals['_EMPTY']._serialized_start=306
  _globals['_EMPTY']._serialized_end=313
  _globals['_KEYVALUESTORE']._serialized_start=316
  _globals['_KEYVALUESTORE']._serialized_end=630
# @@protoc_insertion_point(module_scope)
