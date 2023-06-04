import uuid
from django.utils import timezone

# def generate_transaction_id():
#     timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
#     unique_id = uuid.uuid4().hex[:6].upper()  # Generate a random 6-character string
#     transaction_id = f'TXN-{timestamp}-{unique_id}'
#     return transaction_id


def generate_transaction_id():
    # Generate a unique transaction ID using UUID
    return str(uuid.uuid4())