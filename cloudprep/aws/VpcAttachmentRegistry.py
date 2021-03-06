class VpcAttachmentRegistry:

    __registry = {}

    @staticmethod
    def register_attachment(vpc, subject, attachment):
        """ Register an attachment.
         * vpc: The VPC that will be attached
         * subject: The thing that will be attached (e.g. IGW, TGW)
         * attachment: The attachment we'd like to register.
        """
        vpc_id = vpc.logical_id
        subject_id = subject.logical_id

        if vpc_id not in VpcAttachmentRegistry.__registry:
            VpcAttachmentRegistry.__registry[vpc_id] = {}

        VpcAttachmentRegistry.__registry[vpc_id][subject_id] = attachment

    @staticmethod
    def get_attachment(vpc_logical_id, subject_logical_id):
        if vpc_logical_id not in VpcAttachmentRegistry.__registry:
            return None

        if subject_logical_id not in VpcAttachmentRegistry.__registry[vpc_logical_id]:
            return None

        return VpcAttachmentRegistry.__registry[vpc_logical_id][subject_logical_id]
