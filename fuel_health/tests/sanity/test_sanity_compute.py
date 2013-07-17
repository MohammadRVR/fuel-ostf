from nose.plugins.attrib import attr
from nose.tools import timed

from fuel_health.tests.sanity import base


class SanityComputeTest(base.BaseComputeTest):
    """
    TestClass contains tests check base Compute functionality.
    """
    _interface = 'json'

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_instances(self):
        """Test checks list of instances is available.
        Target component: Nova
        Scenario:
            1. Request list of instances.
            2. Check response status is equal to 200.
            3. Check response contains "servers" section.
        Duration: 0.6-5.6 s.
        """
        resp, body = self.servers_client.list_servers()
        self.verify_response_status(resp.status, u'Nova')
        self.verify_response_body(body, u'servers',
                                  'Servers list is unavailable. '
                                  'Looks like something is broken in Nova.')

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_images(self):
        """Test checks list of images is available.
        Target component: Glance
        Scenario:
            1. Request list of images.
            2. Check response status is equal to 200.
            3. Check response contains "images" section.
        Duration: 0.8-5.6 s.
        """
        resp, body = self.images_client.list_images()
        self.verify_response_status(resp.status, 'Glance')
        self.verify_response_body(body, u'images',
                                  'Images list is unavailable. '
                                  'Looks like something is broken in Glance.')

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_volumes(self):
        """Test checks list of volumes is available.
        Target component: Swift

        Scenario:
            1. Request list of volumes.
            2. Check response status is equal to 200.
            3. Check response contains "volumes" section.
        Duration: 0.6-5.6 s.
        """
        resp, body = self.volumes_client.list_volumes()
        self.verify_response_status(resp.status, 'Swift')
        self.verify_response_body(body, u'volumes',
                                  'Volumes list is unavailable. '
                                  'Looks like something is broken in Swift.')

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_snapshots(self):
        """Test checks list of snapshots is available.
        Target component: Swift

        Scenario:
            1. Request list of snapshots.
            2. Check response status is equal to 200.
            3. Check response contains "snapshots" section.
        Duration: 0.9-5.6 s.
        """
        resp, body = self.snapshots_client.list_snapshots()
        self.verify_response_status(resp.status, 'Swift')
        self.verify_response_body(body, u'snapshots',
                                  'Snapshots list is unavailable. '
                                  'Looks like something is broken in Swift.')

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_flavors(self):
        """Test checks list of flavors is available.
        Target component: Nova

        Scenario:
            1. Request list of flavors.
            2. Check response status is equal to 200.
            3. Check response contains "flavors" section.
        Duration: 1.2-5.6 s.
        """
        resp, body = self.flavors_client.list_flavors()
        self.verify_response_status(resp.status, 'Nova')
        self.verify_response_body(body, u'flavors',
                                  'Flavors list is unavailable. '
                                  'Looks like something is broken in Nova.')

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_rate_limits(self):
        """Test checks list of absolute limits is available.
        Target component: Cinder

        Scenario:
            1. Request list of limits.
            2. Check response status is equal to 200.
            3. Check response contains absolute limits in "limits" section.
        Duration: 1.5-5.6 s.
        """
        resp, body = self.limits_client.get_absolute_limits()
        self.verify_response_status(resp.status, 'Nova')
        self.verify_response_body(body["limits"], u'absolute',
                                  'Limits are unavailable. '
                                  'Looks like something is broken in Nova.')
