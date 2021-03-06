# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import lte_pb2 as lte__pb2
import lte_registration_pb2 as lte__registration__pb2


class RegistrationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Subscribe = channel.unary_stream(
                '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/Subscribe',
                request_serializer=lte__registration__pb2.SubscribeRequest.SerializeToString,
                response_deserializer=lte__registration__pb2.Message.FromString,
                )
        self.Register = channel.stream_stream(
                '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/Register',
                request_serializer=lte__pb2.Cell.SerializeToString,
                response_deserializer=lte__registration__pb2.RegisterResponse.FromString,
                )
        self.Unregister = channel.unary_unary(
                '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/Unregister',
                request_serializer=lte__registration__pb2.UnregisterRequest.SerializeToString,
                response_deserializer=lte__registration__pb2.UnregisterResponse.FromString,
                )
        self.AddNeighbor = channel.unary_unary(
                '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/AddNeighbor',
                request_serializer=lte__registration__pb2.AddNeighborRequest.SerializeToString,
                response_deserializer=lte__registration__pb2.AddNeighborResponse.FromString,
                )
        self.RemoveNeighbor = channel.unary_unary(
                '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/RemoveNeighbor',
                request_serializer=lte__registration__pb2.RemoveNeighborRequest.SerializeToString,
                response_deserializer=lte__registration__pb2.RemoveNeighborResponse.FromString,
                )


class RegistrationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Subscribe(self, request, context):
        """Subscribe to the RegistrationService messages.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Register(self, request_iterator, context):
        """Register cells with eSON. The client shall use this RPC to
        register a new cell with the eSON Server or to update parameters
        of an existing cell.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Unregister(self, request, context):
        """Unregister cells from eSON. The client shall use this RPC when
        cells are decommissioned from the network.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddNeighbor(self, request, context):
        """Add neighbors to a cell. The client shall use this RPC when new
        neighbors are added to a cell's NRT.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveNeighbor(self, request, context):
        """Remove neighbors from a cell. The client shall use this RPC when
        neighbors are removed from a cell's NRT.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegistrationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Subscribe': grpc.unary_stream_rpc_method_handler(
                    servicer.Subscribe,
                    request_deserializer=lte__registration__pb2.SubscribeRequest.FromString,
                    response_serializer=lte__registration__pb2.Message.SerializeToString,
            ),
            'Register': grpc.stream_stream_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=lte__pb2.Cell.FromString,
                    response_serializer=lte__registration__pb2.RegisterResponse.SerializeToString,
            ),
            'Unregister': grpc.unary_unary_rpc_method_handler(
                    servicer.Unregister,
                    request_deserializer=lte__registration__pb2.UnregisterRequest.FromString,
                    response_serializer=lte__registration__pb2.UnregisterResponse.SerializeToString,
            ),
            'AddNeighbor': grpc.unary_unary_rpc_method_handler(
                    servicer.AddNeighbor,
                    request_deserializer=lte__registration__pb2.AddNeighborRequest.FromString,
                    response_serializer=lte__registration__pb2.AddNeighborResponse.SerializeToString,
            ),
            'RemoveNeighbor': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveNeighbor,
                    request_deserializer=lte__registration__pb2.RemoveNeighborRequest.FromString,
                    response_serializer=lte__registration__pb2.RemoveNeighborResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.airhopcomm.eson.lte.registration.v1.RegistrationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RegistrationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Subscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/Subscribe',
            lte__registration__pb2.SubscribeRequest.SerializeToString,
            lte__registration__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Register(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/Register',
            lte__pb2.Cell.SerializeToString,
            lte__registration__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Unregister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/Unregister',
            lte__registration__pb2.UnregisterRequest.SerializeToString,
            lte__registration__pb2.UnregisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddNeighbor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/AddNeighbor',
            lte__registration__pb2.AddNeighborRequest.SerializeToString,
            lte__registration__pb2.AddNeighborResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveNeighbor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.registration.v1.RegistrationService/RemoveNeighbor',
            lte__registration__pb2.RemoveNeighborRequest.SerializeToString,
            lte__registration__pb2.RemoveNeighborResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
