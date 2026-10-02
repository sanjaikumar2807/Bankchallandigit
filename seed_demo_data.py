import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_challan.settings')
django.setup()

from challan.models import Account, Transaction, Challan
from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created superuser: admin / admin123")

# Create test accounts
accounts_data = [
    {
        'account_number': '123456789012',
        'account_holder_name': 'Rajesh Sharma',
        'account_type': 'savings',
        'balance': 45500.00
    },
    {
        'account_number': '987654321098',
        'account_holder_name': 'Priya Patel',
        'account_type': 'current',
        'balance': 125000.50
    },
    {
        'account_number': '556677889900',
        'account_holder_name': 'Amit Kumar Verma',
        'account_type': 'savings',
        'balance': 12300.00
    }
]

for acc_info in accounts_data:
    account, created = Account.objects.get_or_create(
        account_number=acc_info['account_number'],
        defaults=acc_info
    )
    if created:
        print(f"Created account: {account.account_number} ({account.account_holder_name})")
    
    # Create sample transaction and challan for account
    if not hasattr(account, 'transactions') or not account.transactions.exists():
        txn = Transaction.objects.create(
            account=account,
            transaction_type='deposit',
            amount=5000.00,
            status='completed',
            description='Cash Deposit via Kiosk'
        )
        challan = Challan.objects.create(
            transaction=txn,
            challan_number=f"CH{account.account_number[-6:]}01",
            barcode_number=account.account_number, # allows scanning account number directly!
            content=f"Deposit Challan for {account.account_holder_name} - Rs. 5000.00"
        )
        print(f"Created demo Challan: {challan.challan_number} (Barcode: {challan.barcode_number})")

print("Demo data setup successfully completed!")
