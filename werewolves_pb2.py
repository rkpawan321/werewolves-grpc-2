# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: werewolves.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10werewolves.proto\x12\nwerewolves\"\x1e\n\nPlayerInfo\x12\x10\n\x08username\x18\x01 \x01(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"+\n\x0bVoteRequest\x12\r\n\x05voter\x18\x01 \x01(\t\x12\r\n\x05votee\x18\x02 \x01(\t\"\x1f\n\x0cVoteResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xd5\x01\n\x0eWerewolvesGame\x12>\n\x07\x43onnect\x12\x16.werewolves.PlayerInfo\x1a\x1b.werewolves.MessageResponse\x12\x39\n\x04Vote\x12\x17.werewolves.VoteRequest\x1a\x18.werewolves.VoteResponse\x12H\n\x0fReceiveMessages\x12\x16.werewolves.PlayerInfo\x1a\x1b.werewolves.MessageResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'werewolves_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PLAYERINFO']._serialized_start=32
  _globals['_PLAYERINFO']._serialized_end=62
  _globals['_MESSAGERESPONSE']._serialized_start=64
  _globals['_MESSAGERESPONSE']._serialized_end=98
  _globals['_VOTEREQUEST']._serialized_start=100
  _globals['_VOTEREQUEST']._serialized_end=143
  _globals['_VOTERESPONSE']._serialized_start=145
  _globals['_VOTERESPONSE']._serialized_end=176
  _globals['_WEREWOLVESGAME']._serialized_start=179
  _globals['_WEREWOLVESGAME']._serialized_end=392
# @@protoc_insertion_point(module_scope)
