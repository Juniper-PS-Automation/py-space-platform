import logging.config

from jnpr.space import rest, factory

def main():
    # Create a Space REST end point
    my_space = rest.Space(url='http://localhost:8080',
                          user='super', passwd='juniper123')

    devices_list = my_space.device_management.devices.get()
    for d in devices_list:
        print d.name, d.ipAddr, d.platform, d.serialNumber
        c = d.configurations.expanded.post(xpaths=['configuration/snmp/location'])
        if c.configuration.location:
            tag_device(my_space, d, c.configuration.location)

def tag_device(spc, device, tag_name):
    try:
        # Check if a tag exists already with the given name
        tag = spc.tag_management.tags.get(filter_={'name': tag_name})[0]
    except:
        # Create a new public tag with the given name
        tag = factory.make_resource('tag_management.tag', spc)
        tag.name, tag.type = tag_name, 'public'
        tag = spc.tag_management.tags.post(tag)

    """
    Create a new target for this tag, pointing to the given device.
    In other words, assign this tag to this device
    """
    target = factory.make_resource('tag_management.target', spc)
    target.href = device.href
    tag.targets.post(target)

if __name__ == "__main__":
    # Initialize logging
    logging.config.fileConfig('./logging.conf')
    main()