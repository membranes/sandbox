"""Module main.py"""
import argparse
import logging
import os
import sys

import boto3
import torch


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Set up
    setup: bool = src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()
    if not setup:
        src.functions.cache.Cache().exc()
        sys.exit('No Executions')

    # Device Selection: Setting a graphics processing unit as the default device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info('Device: %s', device)

    # Hence
    src.algorithms.interface.Interface().exc(architecture=architecture)
    src.transfer.interface.Interface(service=service, s3_parameters=s3_parameters).exc()

    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Activate graphics processing units
    os.environ['CUDA_VISIBLE_DEVICES']='0'

    # Modules
    import src.algorithms.interface
    import src.elements.arguments
    import src.functions.cache
    import src.functions.expecting
    import src.functions.service
    import src.s3.s3_parameters
    import src.setup
    import src.transfer.interface

    expecting = src.functions.expecting.Expecting()
    parser = argparse.ArgumentParser()
    parser.add_argument('--architecture', type=expecting.architecture,
                        help='The name of the architecture in focus.')
    args = parser.parse_args()

    # Default architecture?
    architecture = 'distil' if args.architecture is None else args.architecture

    # S3 S3Parameters, Service Instance
    connector = boto3.session.Session()
    s3_parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
    service = src.functions.service.Service(connector=connector, region_name=s3_parameters.region_name).exc()



    main()
