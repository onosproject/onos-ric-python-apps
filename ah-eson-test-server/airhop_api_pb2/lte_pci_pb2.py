# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lte_pci.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='lte_pci.proto',
  package='com.airhopcomm.eson.lte.pci.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rlte_pci.proto\x12\x1e\x63om.airhopcomm.eson.lte.pci.v1\"d\n\x10SubscribeRequest\x12\x10\n\x08\x65\x63gi_set\x18\x01 \x03(\x06\x12>\n\x0c\x63onflict_set\x18\x02 \x03(\x0e\x32(.com.airhopcomm.eson.lte.pci.v1.Conflict\"U\n\x07Message\x12\x43\n\nchange_req\x18\x01 \x01(\x0b\x32-.com.airhopcomm.eson.lte.pci.v1.ChangeRequestH\x00\x42\x05\n\x03msg\"f\n\rChangeRequest\x12\x0c\n\x04\x65\x63gi\x18\x01 \x01(\x06\x12\x0b\n\x03pci\x18\x02 \x01(\r\x12:\n\x08\x63onflict\x18\x03 \x01(\x0e\x32(.com.airhopcomm.eson.lte.pci.v1.Conflict\"#\n\x0f\x41llocateRequest\x12\x10\n\x08\x65\x63gi_set\x18\x01 \x03(\x06\"\x12\n\x10\x41llocateResponse\"+\n\x17\x44\x65tectAndResolveRequest\x12\x10\n\x08\x65\x63gi_set\x18\x01 \x03(\x06\"\x1a\n\x18\x44\x65tectAndResolveResponse\"1\n\x14\x43onfirmChangeRequest\x12\x0c\n\x04\x65\x63gi\x18\x01 \x01(\x06\x12\x0b\n\x03pci\x18\x02 \x01(\r\"\x17\n\x15\x43onfirmChangeResponse\"0\n\x13RejectChangeRequest\x12\x0c\n\x04\x65\x63gi\x18\x01 \x01(\x06\x12\x0b\n\x03pci\x18\x02 \x01(\r\"\x16\n\x14RejectChangeResponse\"`\n\x1eRetrieveProposedChangesRequest\x12>\n\x0c\x63onflict_set\x18\x01 \x03(\x0e\x32(.com.airhopcomm.eson.lte.pci.v1.Conflict\"e\n\x1fRetrieveProposedChangesResponse\x12\x42\n\x0b\x63hange_reqs\x18\x01 \x03(\x0b\x32-.com.airhopcomm.eson.lte.pci.v1.ChangeRequest*\x8d\x01\n\x08\x43onflict\x12\x11\n\rCONFLICT_NONE\x10\x00\x12\x1d\n\x19\x43ONFLICT_DIRECT_COLLISION\x10\x01\x12\x16\n\x12\x43ONFLICT_CONFUSION\x10\x02\x12\x1a\n\x16\x43ONFLICT_CRS_COLLISION\x10\x03\x12\x1b\n\x17\x43ONFLICT_DMRS_COLLISION\x10\x04\x32\x8f\x06\n\nPciService\x12j\n\tSubscribe\x12\x30.com.airhopcomm.eson.lte.pci.v1.SubscribeRequest\x1a\'.com.airhopcomm.eson.lte.pci.v1.Message\"\x00\x30\x01\x12o\n\x08\x41llocate\x12/.com.airhopcomm.eson.lte.pci.v1.AllocateRequest\x1a\x30.com.airhopcomm.eson.lte.pci.v1.AllocateResponse\"\x00\x12\x87\x01\n\x10\x44\x65tectAndResolve\x12\x37.com.airhopcomm.eson.lte.pci.v1.DetectAndResolveRequest\x1a\x38.com.airhopcomm.eson.lte.pci.v1.DetectAndResolveResponse\"\x00\x12~\n\rConfirmChange\x12\x34.com.airhopcomm.eson.lte.pci.v1.ConfirmChangeRequest\x1a\x35.com.airhopcomm.eson.lte.pci.v1.ConfirmChangeResponse\"\x00\x12{\n\x0cRejectChange\x12\x33.com.airhopcomm.eson.lte.pci.v1.RejectChangeRequest\x1a\x34.com.airhopcomm.eson.lte.pci.v1.RejectChangeResponse\"\x00\x12\x9c\x01\n\x17RetrieveProposedChanges\x12>.com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesRequest\x1a?.com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesResponse\"\x00\x62\x06proto3'
)

_CONFLICT = _descriptor.EnumDescriptor(
  name='Conflict',
  full_name='com.airhopcomm.eson.lte.pci.v1.Conflict',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CONFLICT_NONE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFLICT_DIRECT_COLLISION', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFLICT_CONFUSION', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFLICT_CRS_COLLISION', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFLICT_DMRS_COLLISION', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=824,
  serialized_end=965,
)
_sym_db.RegisterEnumDescriptor(_CONFLICT)

Conflict = enum_type_wrapper.EnumTypeWrapper(_CONFLICT)
CONFLICT_NONE = 0
CONFLICT_DIRECT_COLLISION = 1
CONFLICT_CONFUSION = 2
CONFLICT_CRS_COLLISION = 3
CONFLICT_DMRS_COLLISION = 4



_SUBSCRIBEREQUEST = _descriptor.Descriptor(
  name='SubscribeRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.SubscribeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecgi_set', full_name='com.airhopcomm.eson.lte.pci.v1.SubscribeRequest.ecgi_set', index=0,
      number=1, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conflict_set', full_name='com.airhopcomm.eson.lte.pci.v1.SubscribeRequest.conflict_set', index=1,
      number=2, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=149,
)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='com.airhopcomm.eson.lte.pci.v1.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_req', full_name='com.airhopcomm.eson.lte.pci.v1.Message.change_req', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='msg', full_name='com.airhopcomm.eson.lte.pci.v1.Message.msg',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=151,
  serialized_end=236,
)


_CHANGEREQUEST = _descriptor.Descriptor(
  name='ChangeRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.ChangeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecgi', full_name='com.airhopcomm.eson.lte.pci.v1.ChangeRequest.ecgi', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pci', full_name='com.airhopcomm.eson.lte.pci.v1.ChangeRequest.pci', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conflict', full_name='com.airhopcomm.eson.lte.pci.v1.ChangeRequest.conflict', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=238,
  serialized_end=340,
)


_ALLOCATEREQUEST = _descriptor.Descriptor(
  name='AllocateRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.AllocateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecgi_set', full_name='com.airhopcomm.eson.lte.pci.v1.AllocateRequest.ecgi_set', index=0,
      number=1, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=342,
  serialized_end=377,
)


_ALLOCATERESPONSE = _descriptor.Descriptor(
  name='AllocateResponse',
  full_name='com.airhopcomm.eson.lte.pci.v1.AllocateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=379,
  serialized_end=397,
)


_DETECTANDRESOLVEREQUEST = _descriptor.Descriptor(
  name='DetectAndResolveRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.DetectAndResolveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecgi_set', full_name='com.airhopcomm.eson.lte.pci.v1.DetectAndResolveRequest.ecgi_set', index=0,
      number=1, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=442,
)


_DETECTANDRESOLVERESPONSE = _descriptor.Descriptor(
  name='DetectAndResolveResponse',
  full_name='com.airhopcomm.eson.lte.pci.v1.DetectAndResolveResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=444,
  serialized_end=470,
)


_CONFIRMCHANGEREQUEST = _descriptor.Descriptor(
  name='ConfirmChangeRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.ConfirmChangeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecgi', full_name='com.airhopcomm.eson.lte.pci.v1.ConfirmChangeRequest.ecgi', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pci', full_name='com.airhopcomm.eson.lte.pci.v1.ConfirmChangeRequest.pci', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=472,
  serialized_end=521,
)


_CONFIRMCHANGERESPONSE = _descriptor.Descriptor(
  name='ConfirmChangeResponse',
  full_name='com.airhopcomm.eson.lte.pci.v1.ConfirmChangeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=523,
  serialized_end=546,
)


_REJECTCHANGEREQUEST = _descriptor.Descriptor(
  name='RejectChangeRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.RejectChangeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecgi', full_name='com.airhopcomm.eson.lte.pci.v1.RejectChangeRequest.ecgi', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pci', full_name='com.airhopcomm.eson.lte.pci.v1.RejectChangeRequest.pci', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=548,
  serialized_end=596,
)


_REJECTCHANGERESPONSE = _descriptor.Descriptor(
  name='RejectChangeResponse',
  full_name='com.airhopcomm.eson.lte.pci.v1.RejectChangeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=598,
  serialized_end=620,
)


_RETRIEVEPROPOSEDCHANGESREQUEST = _descriptor.Descriptor(
  name='RetrieveProposedChangesRequest',
  full_name='com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='conflict_set', full_name='com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesRequest.conflict_set', index=0,
      number=1, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=622,
  serialized_end=718,
)


_RETRIEVEPROPOSEDCHANGESRESPONSE = _descriptor.Descriptor(
  name='RetrieveProposedChangesResponse',
  full_name='com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_reqs', full_name='com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesResponse.change_reqs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=720,
  serialized_end=821,
)

_SUBSCRIBEREQUEST.fields_by_name['conflict_set'].enum_type = _CONFLICT
_MESSAGE.fields_by_name['change_req'].message_type = _CHANGEREQUEST
_MESSAGE.oneofs_by_name['msg'].fields.append(
  _MESSAGE.fields_by_name['change_req'])
_MESSAGE.fields_by_name['change_req'].containing_oneof = _MESSAGE.oneofs_by_name['msg']
_CHANGEREQUEST.fields_by_name['conflict'].enum_type = _CONFLICT
_RETRIEVEPROPOSEDCHANGESREQUEST.fields_by_name['conflict_set'].enum_type = _CONFLICT
_RETRIEVEPROPOSEDCHANGESRESPONSE.fields_by_name['change_reqs'].message_type = _CHANGEREQUEST
DESCRIPTOR.message_types_by_name['SubscribeRequest'] = _SUBSCRIBEREQUEST
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.message_types_by_name['ChangeRequest'] = _CHANGEREQUEST
DESCRIPTOR.message_types_by_name['AllocateRequest'] = _ALLOCATEREQUEST
DESCRIPTOR.message_types_by_name['AllocateResponse'] = _ALLOCATERESPONSE
DESCRIPTOR.message_types_by_name['DetectAndResolveRequest'] = _DETECTANDRESOLVEREQUEST
DESCRIPTOR.message_types_by_name['DetectAndResolveResponse'] = _DETECTANDRESOLVERESPONSE
DESCRIPTOR.message_types_by_name['ConfirmChangeRequest'] = _CONFIRMCHANGEREQUEST
DESCRIPTOR.message_types_by_name['ConfirmChangeResponse'] = _CONFIRMCHANGERESPONSE
DESCRIPTOR.message_types_by_name['RejectChangeRequest'] = _REJECTCHANGEREQUEST
DESCRIPTOR.message_types_by_name['RejectChangeResponse'] = _REJECTCHANGERESPONSE
DESCRIPTOR.message_types_by_name['RetrieveProposedChangesRequest'] = _RETRIEVEPROPOSEDCHANGESREQUEST
DESCRIPTOR.message_types_by_name['RetrieveProposedChangesResponse'] = _RETRIEVEPROPOSEDCHANGESRESPONSE
DESCRIPTOR.enum_types_by_name['Conflict'] = _CONFLICT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SubscribeRequest = _reflection.GeneratedProtocolMessageType('SubscribeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBEREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.SubscribeRequest)
  })
_sym_db.RegisterMessage(SubscribeRequest)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.Message)
  })
_sym_db.RegisterMessage(Message)

ChangeRequest = _reflection.GeneratedProtocolMessageType('ChangeRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.ChangeRequest)
  })
_sym_db.RegisterMessage(ChangeRequest)

AllocateRequest = _reflection.GeneratedProtocolMessageType('AllocateRequest', (_message.Message,), {
  'DESCRIPTOR' : _ALLOCATEREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.AllocateRequest)
  })
_sym_db.RegisterMessage(AllocateRequest)

AllocateResponse = _reflection.GeneratedProtocolMessageType('AllocateResponse', (_message.Message,), {
  'DESCRIPTOR' : _ALLOCATERESPONSE,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.AllocateResponse)
  })
_sym_db.RegisterMessage(AllocateResponse)

DetectAndResolveRequest = _reflection.GeneratedProtocolMessageType('DetectAndResolveRequest', (_message.Message,), {
  'DESCRIPTOR' : _DETECTANDRESOLVEREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.DetectAndResolveRequest)
  })
_sym_db.RegisterMessage(DetectAndResolveRequest)

DetectAndResolveResponse = _reflection.GeneratedProtocolMessageType('DetectAndResolveResponse', (_message.Message,), {
  'DESCRIPTOR' : _DETECTANDRESOLVERESPONSE,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.DetectAndResolveResponse)
  })
_sym_db.RegisterMessage(DetectAndResolveResponse)

ConfirmChangeRequest = _reflection.GeneratedProtocolMessageType('ConfirmChangeRequest', (_message.Message,), {
  'DESCRIPTOR' : _CONFIRMCHANGEREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.ConfirmChangeRequest)
  })
_sym_db.RegisterMessage(ConfirmChangeRequest)

ConfirmChangeResponse = _reflection.GeneratedProtocolMessageType('ConfirmChangeResponse', (_message.Message,), {
  'DESCRIPTOR' : _CONFIRMCHANGERESPONSE,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.ConfirmChangeResponse)
  })
_sym_db.RegisterMessage(ConfirmChangeResponse)

RejectChangeRequest = _reflection.GeneratedProtocolMessageType('RejectChangeRequest', (_message.Message,), {
  'DESCRIPTOR' : _REJECTCHANGEREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.RejectChangeRequest)
  })
_sym_db.RegisterMessage(RejectChangeRequest)

RejectChangeResponse = _reflection.GeneratedProtocolMessageType('RejectChangeResponse', (_message.Message,), {
  'DESCRIPTOR' : _REJECTCHANGERESPONSE,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.RejectChangeResponse)
  })
_sym_db.RegisterMessage(RejectChangeResponse)

RetrieveProposedChangesRequest = _reflection.GeneratedProtocolMessageType('RetrieveProposedChangesRequest', (_message.Message,), {
  'DESCRIPTOR' : _RETRIEVEPROPOSEDCHANGESREQUEST,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesRequest)
  })
_sym_db.RegisterMessage(RetrieveProposedChangesRequest)

RetrieveProposedChangesResponse = _reflection.GeneratedProtocolMessageType('RetrieveProposedChangesResponse', (_message.Message,), {
  'DESCRIPTOR' : _RETRIEVEPROPOSEDCHANGESRESPONSE,
  '__module__' : 'lte_pci_pb2'
  # @@protoc_insertion_point(class_scope:com.airhopcomm.eson.lte.pci.v1.RetrieveProposedChangesResponse)
  })
_sym_db.RegisterMessage(RetrieveProposedChangesResponse)



_PCISERVICE = _descriptor.ServiceDescriptor(
  name='PciService',
  full_name='com.airhopcomm.eson.lte.pci.v1.PciService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=968,
  serialized_end=1751,
  methods=[
  _descriptor.MethodDescriptor(
    name='Subscribe',
    full_name='com.airhopcomm.eson.lte.pci.v1.PciService.Subscribe',
    index=0,
    containing_service=None,
    input_type=_SUBSCRIBEREQUEST,
    output_type=_MESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Allocate',
    full_name='com.airhopcomm.eson.lte.pci.v1.PciService.Allocate',
    index=1,
    containing_service=None,
    input_type=_ALLOCATEREQUEST,
    output_type=_ALLOCATERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DetectAndResolve',
    full_name='com.airhopcomm.eson.lte.pci.v1.PciService.DetectAndResolve',
    index=2,
    containing_service=None,
    input_type=_DETECTANDRESOLVEREQUEST,
    output_type=_DETECTANDRESOLVERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ConfirmChange',
    full_name='com.airhopcomm.eson.lte.pci.v1.PciService.ConfirmChange',
    index=3,
    containing_service=None,
    input_type=_CONFIRMCHANGEREQUEST,
    output_type=_CONFIRMCHANGERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RejectChange',
    full_name='com.airhopcomm.eson.lte.pci.v1.PciService.RejectChange',
    index=4,
    containing_service=None,
    input_type=_REJECTCHANGEREQUEST,
    output_type=_REJECTCHANGERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RetrieveProposedChanges',
    full_name='com.airhopcomm.eson.lte.pci.v1.PciService.RetrieveProposedChanges',
    index=5,
    containing_service=None,
    input_type=_RETRIEVEPROPOSEDCHANGESREQUEST,
    output_type=_RETRIEVEPROPOSEDCHANGESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PCISERVICE)

DESCRIPTOR.services_by_name['PciService'] = _PCISERVICE

# @@protoc_insertion_point(module_scope)