from nose.plugins.attrib import attr
from nose.tools import timed

from fuel_health.common.utils.data_utils import rand_name
from fuel_health.tests.smoke import base

class VolumesTest(base.BaseComputeTest):

    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(VolumesTest, cls).setUpClass()
        cls.client = cls.servers_client
        resp, server = cls.create_server(name='ost1_test-instance',
                                         wait_until='ACTIVE',
                                         adminPass='password')
        resp, server['addresses'] = cls.client.list_addresses(server['id'])
        cls.server_id = server['id']
        cls.server_address = server['addresses']
        cls.device = 'vdb'

    @classmethod
    def tearDownClass(cls):
        super(VolumesTest, cls).tearDownClass()

    @attr(type=["fuel", "smoke"])
    @timed(60.5)
    def test_volume_create(self):
        """Test volume can be created.
        Target component: Compute

        Scenario:
            1. Create a new small-size volume.
            2. Check response status equals 200.
            3. Check response contains "id" section.
            4. Check response contains "display_name" section.
            5. Check volume has expected name.
            6. Wait for "available" volume status.
            7. Attach volume to instance.
            8. Check response status equals 200.
            9. Check volume status is "in use".
            10. Get created volume information by its id.
            11. Check operation response status equals 200.
            12. Check attachments section contains correct device.
            13. Check attachments section contains correct server id.
            14. Check attachments section contains correct volume id.
            15. Detach volume from instance.
            16. Check volume has "available" status.
            17. Delete volume.
            18. Check response status equals 200.
        Duration: 47.1-60.5 s.
        """
        v_name = rand_name('ost1_test-test')
        metadata = {'Type': 'work'}

        #Create volume
        resp, volume = self.volumes_client.create_volume(size=1,
                                                         display_name=v_name,
                                                         metadata=metadata)
        self.verify_response_status(resp.status, 'Compute')

        self.verify_response_body(volume, 'id',
                                  'Volume is not created. '
                                  'Looks like something is broken in Storage.')
        self.verify_response_body(volume, 'display_name',
                                  'Volume is not created. '
                                  'Looks like something is broken in Storage.')

        self.verify_response_body_content(v_name,
                                          volume['display_name'],
                                          ("The created volume"
                                           " name is not equal "
                                           "to the requested"
                                           " name"))

        #Wait for Volume status to become AVAILABLE
        self.volumes_client.wait_for_volume_status(volume['id'], 'available')

        # Attach the volume to the server
        device = '/dev/%s' % self.device
        resp, body = self.servers_client.attach_volume(self.server_id,
                                                       volume['id'],
                                                       device=device)
        self.verify_response_status(resp.status, 'Nova Compute')

        self.volumes_client.wait_for_volume_status(volume['id'], 'in-use')

        self.attached = True

        resp, body = self.volumes_client.get_volume(volume['id'])
        self.verify_response_status(resp.status, 'Storage Objects')

        for attachment in body['attachments']:
            self.verify_response_body_content('/dev/%s' % self.device,
                                              attachment['device'],
                                              ('Device is not equal, '
                                               'Volume attachment failed'))

            self.verify_response_body_content(self.server_id,
                                              attachment['server_id'],
                                              ('Server id is not equal,'
                                               'Volume attachment failed'))

            self.verify_response_body_content(volume['id'],
                                              attachment['volume_id'],
                                              'Wrong volume is attached')

        # detach volume
        self.servers_client.detach_volume(self.server_id, volume['id'])
        self.volumes_client.wait_for_volume_status(volume['id'], 'available')

        # delete volume
        resp, body = self.volumes_client.delete_volume(volume['id'])
        self.verify_response_status(resp.status, 'Storage Object')
