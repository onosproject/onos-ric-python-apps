# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import lte_pci_pb2 as lte__pci__pb2


class PciServiceStub(object):
    """The PciService can be used in either autonomous mode or maintenance
    window mode.

    In autonomous mode, PCI conflicts are detected and changes are
    applied in realtime. The client shall use the Subscribe RPC and
    monitor the return stream for any PCI change. If a PCI change
    request is received. the client shall immediately apply the change.
    Once the PCI change is applied, the client shall use the
    ConfirmChange or RejectChange RPC to update eSON.

    In maintenance window mode, PCI changes are only applied during the
    maintenance window. The client shall use the
    RetrieveProposedChanges RPC near the end of the maintenance window
    to obtain a list of suggested PCI changes. Once a PCI change is
    applied, the client shall use the ConfirmChange or RejectChange RPC
    to update eSON.

    If there are multiple clients that subscribe to PCI changes, one
    and only one shall confirm the change.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Subscribe = channel.unary_stream(
                '/com.airhopcomm.eson.lte.pci.v1.PciService/Subscribe',
                request_serializer=lte__pci__pb2.SubscribeRequest.SerializeToString,
                response_deserializer=lte__pci__pb2.Message.FromString,
                )
        self.Allocate = channel.unary_unary(
                '/com.airhopcomm.eson.lte.pci.v1.PciService/Allocate',
                request_serializer=lte__pci__pb2.AllocateRequest.SerializeToString,
                response_deserializer=lte__pci__pb2.AllocateResponse.FromString,
                )
        self.DetectAndResolve = channel.unary_unary(
                '/com.airhopcomm.eson.lte.pci.v1.PciService/DetectAndResolve',
                request_serializer=lte__pci__pb2.DetectAndResolveRequest.SerializeToString,
                response_deserializer=lte__pci__pb2.DetectAndResolveResponse.FromString,
                )
        self.ConfirmChange = channel.unary_unary(
                '/com.airhopcomm.eson.lte.pci.v1.PciService/ConfirmChange',
                request_serializer=lte__pci__pb2.ConfirmChangeRequest.SerializeToString,
                response_deserializer=lte__pci__pb2.ConfirmChangeResponse.FromString,
                )
        self.RejectChange = channel.unary_unary(
                '/com.airhopcomm.eson.lte.pci.v1.PciService/RejectChange',
                request_serializer=lte__pci__pb2.RejectChangeRequest.SerializeToString,
                response_deserializer=lte__pci__pb2.RejectChangeResponse.FromString,
                )
        self.RetrieveProposedChanges = channel.unary_unary(
                '/com.airhopcomm.eson.lte.pci.v1.PciService/RetrieveProposedChanges',
                request_serializer=lte__pci__pb2.RetrieveProposedChangesRequest.SerializeToString,
                response_deserializer=lte__pci__pb2.RetrieveProposedChangesResponse.FromString,
                )


class PciServiceServicer(object):
    """The PciService can be used in either autonomous mode or maintenance
    window mode.

    In autonomous mode, PCI conflicts are detected and changes are
    applied in realtime. The client shall use the Subscribe RPC and
    monitor the return stream for any PCI change. If a PCI change
    request is received. the client shall immediately apply the change.
    Once the PCI change is applied, the client shall use the
    ConfirmChange or RejectChange RPC to update eSON.

    In maintenance window mode, PCI changes are only applied during the
    maintenance window. The client shall use the
    RetrieveProposedChanges RPC near the end of the maintenance window
    to obtain a list of suggested PCI changes. Once a PCI change is
    applied, the client shall use the ConfirmChange or RejectChange RPC
    to update eSON.

    If there are multiple clients that subscribe to PCI changes, one
    and only one shall confirm the change.
    """

    def Subscribe(self, request, context):
        """Subscribe to the PciService for the PCI algorithm messages. Any
        future PCI change will be streamed back through this RPC.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Allocate(self, request, context):
        """Request initial PCI assignment. The newly allocated PCI is
        streamed back through the Subscribe RPC.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DetectAndResolve(self, request, context):
        """Trigger PCI algorithm to detect and resolve PCI conflict. If a
        conflict is detected and a better PCI is found, the new PCI is
        streamed back through the Subscribe RPC.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConfirmChange(self, request, context):
        """Confirm a PCI change request has been applied. eSON updates its
        internal PCI to reflect the change.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RejectChange(self, request, context):
        """Reject a PCI change request if the proposed PCI fails to be
        applied.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveProposedChanges(self, request, context):
        """Retrieve a list of proposed PCI changes. The client shall use
        the ConfirmChange or RejectChange later to update the eSON
        server whether the proposed changes are applied. This RPC may
        take several minutes (the current default is 5 minutes) to
        complete.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PciServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Subscribe': grpc.unary_stream_rpc_method_handler(
                    servicer.Subscribe,
                    request_deserializer=lte__pci__pb2.SubscribeRequest.FromString,
                    response_serializer=lte__pci__pb2.Message.SerializeToString,
            ),
            'Allocate': grpc.unary_unary_rpc_method_handler(
                    servicer.Allocate,
                    request_deserializer=lte__pci__pb2.AllocateRequest.FromString,
                    response_serializer=lte__pci__pb2.AllocateResponse.SerializeToString,
            ),
            'DetectAndResolve': grpc.unary_unary_rpc_method_handler(
                    servicer.DetectAndResolve,
                    request_deserializer=lte__pci__pb2.DetectAndResolveRequest.FromString,
                    response_serializer=lte__pci__pb2.DetectAndResolveResponse.SerializeToString,
            ),
            'ConfirmChange': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfirmChange,
                    request_deserializer=lte__pci__pb2.ConfirmChangeRequest.FromString,
                    response_serializer=lte__pci__pb2.ConfirmChangeResponse.SerializeToString,
            ),
            'RejectChange': grpc.unary_unary_rpc_method_handler(
                    servicer.RejectChange,
                    request_deserializer=lte__pci__pb2.RejectChangeRequest.FromString,
                    response_serializer=lte__pci__pb2.RejectChangeResponse.SerializeToString,
            ),
            'RetrieveProposedChanges': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveProposedChanges,
                    request_deserializer=lte__pci__pb2.RetrieveProposedChangesRequest.FromString,
                    response_serializer=lte__pci__pb2.RetrieveProposedChangesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.airhopcomm.eson.lte.pci.v1.PciService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PciService(object):
    """The PciService can be used in either autonomous mode or maintenance
    window mode.

    In autonomous mode, PCI conflicts are detected and changes are
    applied in realtime. The client shall use the Subscribe RPC and
    monitor the return stream for any PCI change. If a PCI change
    request is received. the client shall immediately apply the change.
    Once the PCI change is applied, the client shall use the
    ConfirmChange or RejectChange RPC to update eSON.

    In maintenance window mode, PCI changes are only applied during the
    maintenance window. The client shall use the
    RetrieveProposedChanges RPC near the end of the maintenance window
    to obtain a list of suggested PCI changes. Once a PCI change is
    applied, the client shall use the ConfirmChange or RejectChange RPC
    to update eSON.

    If there are multiple clients that subscribe to PCI changes, one
    and only one shall confirm the change.
    """

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
        return grpc.experimental.unary_stream(request, target, '/com.airhopcomm.eson.lte.pci.v1.PciService/Subscribe',
            lte__pci__pb2.SubscribeRequest.SerializeToString,
            lte__pci__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Allocate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.pci.v1.PciService/Allocate',
            lte__pci__pb2.AllocateRequest.SerializeToString,
            lte__pci__pb2.AllocateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DetectAndResolve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.pci.v1.PciService/DetectAndResolve',
            lte__pci__pb2.DetectAndResolveRequest.SerializeToString,
            lte__pci__pb2.DetectAndResolveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConfirmChange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.pci.v1.PciService/ConfirmChange',
            lte__pci__pb2.ConfirmChangeRequest.SerializeToString,
            lte__pci__pb2.ConfirmChangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RejectChange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.pci.v1.PciService/RejectChange',
            lte__pci__pb2.RejectChangeRequest.SerializeToString,
            lte__pci__pb2.RejectChangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveProposedChanges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.airhopcomm.eson.lte.pci.v1.PciService/RetrieveProposedChanges',
            lte__pci__pb2.RetrieveProposedChangesRequest.SerializeToString,
            lte__pci__pb2.RetrieveProposedChangesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
