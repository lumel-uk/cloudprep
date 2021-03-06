from cloudprep.aws.elements.AwsElement import AwsElement
from ...VpcAttachmentRegistry import VpcAttachmentRegistry


class AwsVpcGatewayAttachment(AwsElement):
    def __init__(self, environment, physical_id, **kwargs):
        super().__init__(environment, "AWS::EC2::VPCGatewayAttachment", physical_id, **kwargs)
        self._vpc = kwargs["vpc"]
        self._vpn_gateway = None
        self._internet_gateway = None

    def set_internet_gateway(self, internet_gateway):
        self._internet_gateway = internet_gateway

    def set_vpn_gateway(self, vpn_gateway):
        self._vpn_gateway = vpn_gateway

    @AwsElement.capture_method
    def capture(self):
        self._element["VpcId"] = self._vpc.make_reference()

        if self._internet_gateway is not None:
            self._element["InternetGatewayId"] = self._internet_gateway.make_reference()

        if self._vpn_gateway is not None:
            self._element["VpnGatewayId"] = self._vpn_gateway.make_reference()

        self.is_valid = True
