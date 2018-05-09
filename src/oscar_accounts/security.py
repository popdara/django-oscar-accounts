from oscar.core.loading import get_model
from ipware import get_client_ip

IPAddressRecord = get_model('oscar_accounts', 'IPAddressRecord')


def record_failed_request(request):
    client_ip = get_client_ip(request)
    client_ip = client_ip if client_ip is not None else '127.0.0.1'
    record, __ = IPAddressRecord.objects.get_or_create(ip_address=client_ip)
    record.increment_failures()


def record_successful_request(request):
    try:
        client_ip = get_client_ip(request)
        client_ip = client_ip if client_ip is not None else '127.0.0.1'
        record, __ = IPAddressRecord.objects.get_or_create(ip_address=client_ip)
    except IPAddressRecord.DoesNotExist:
        return
    record.reset()


def record_blocked_request(request):
    try:
        client_ip = get_client_ip(request)
        client_ip = client_ip if client_ip is not None else '127.0.0.1'
        record, __ = IPAddressRecord.objects.get_or_create(ip_address=client_ip)
    except IPAddressRecord.DoesNotExist:
        return
    record.increment_blocks()


def is_blocked(request):
    try:
        client_ip = get_client_ip(request)
        # well, that's embarassing
        if client_ip is None:
            return True
        record = IPAddressRecord.objects.get(
            ip_address=client_ip)
    except IPAddressRecord.DoesNotExist:
        record = IPAddressRecord(ip_address=client_ip)
    return record.is_blocked()
