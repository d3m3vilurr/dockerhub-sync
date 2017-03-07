import time
import docker

def sync(image, to):
    client = docker.from_env()
    name_and_tag = image.rsplit(':')
    if not len(name_and_tag):
        return False
    if len(name_and_tag) == 1:
        name_and_tag.append('latest')
    name, tag = name_and_tag[:2]
    res = '/'.join((to, name))
    target = ':'.join(name_and_tag)
    print 'sync %s to %s' % (target, res)
    try:
        image = client.images.pull(target)
    except docker.errors.ImageNotFound:
        return False
    image.tag(res, tag)
    print client.images.push(res, tag)

def sync_all(images, to, interval=300):
    max_idx = len(images) - 1
    for idx, image in enumerate(images):
        sync(image, config['to'])
        if idx < max_idx:
            time.sleep(interval)

if __name__ == '__main__':
    import sys
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description='sync docker images')
    parser.add_argument('--daemon', '-d', action='store_true',
                        help='daemon mode')
    parser.add_argument('--config', '-c', type=str,
                        default='config.yml',
                        help='override config value (default: config.yml)')
    parser.add_argument('--interval', '-i', type=int,
                        default=300,
                        help='sleep sec interval each actions')
    args = parser.parse_args()

    if not args.daemon:
        with open(args.config) as f:
            config = yaml.safe_load(f)
            sync_all(config['images'], config['to'], args.interval)
            sys.exit(0)
    print 'daemon mode...'
    while True:
        with open(args.config) as f:
            config = yaml.safe_load(f)
            sync_all(config['images'], config['to'], args.interval)
            time.sleep(args.interval)
