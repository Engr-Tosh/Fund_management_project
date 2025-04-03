from django.db import models, transaction
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError

# User Deposit 
class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Deposit(user={self.user}, amount={self.amount})"
    
    # When a deposit is made it has to affect the balance
    def save(self, *args, **kwargs):
        """Update user balance on deposit"""
        balance, _= Balance.objects.get_or_create(user=self.user)
        balance.amount += self.amount
        balance.save()
        super().save(*args, **kwargs)

        #It also has to update the transaction log
        TransactionLog.objects.create(
            type = "deposit",
            user = self.user,
            amount = self.amount,
            deposit_transaction = self,
            status = "successful"
        )    

# User Withdrawal
class Withdrawal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # when a withdrawal is made it also has to affect the balance
    def save(self, *args, **kwargs):
        """Update user balance on withdrawal"""
        with transaction.atomic():            
            balance = Balance.objects.filter(user=self.user).first()
            if balance and balance.amount >= self.amount:
                balance.amount -= self.amount
                balance.save()
                super().save(*args, **kwargs)

                # Transaction Log also needs to be updated
                TransactionLog.objects.create(
                    type = "withdrawal",
                    user = self.user,
                    amount = self.amount,
                    withdrawal_transaction = self,
                    status = "successful"
                )

            else:
                raise ValidationError("Insufficient balance")  

    def __repr__(self):
        return f"Withdrawal(user={self.user}, amount={self.amount})"

# User Balance
class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="balance")
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)


# Total Balance (Admin record/view of all users funds)
class TotalBalance(models.Model):
    """
    Stores the total balance of funds being held 
    by the admin after personal usage
    """
    total_deposits = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    total_withdrawals = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    personal_usage = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    displayed_total_balance = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    admin_total_balance = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def update_personal_usage(cls):
        """
        Calculates personal usage dynamically:
        (Total Admin Withdrawals - Refunded Amounts)
        """
        total_deductions= PersonalUsage.objects.filter(type='deduction').aggregate(models.Sum('amount'))['amount__sum'] or Decimal('0.00')
        total_refunds = PersonalUsage.objects.filter(type='refund').aggregate(models.Sum('amount'))['amount__sum'] or Decimal('0.00')
        personal_usage = total_deductions - total_refunds
        
        # Get the latest balance if it exists
        total_balance = cls.objects.order_by('-updated_at').first()

        if not total_balance:
            # Create a new TotalBalance if none exists
            total_balance = cls.objects.create(
                personal_usage=personal_usage,
                displayed_total_balance=Decimal('0.00'),
                admin_total_balance=Decimal('0.00')
            )

        if total_balance:
            total_balance.personal_usage = personal_usage
            total_balance.displayed_total_balance = total_balance.total_deposits - total_balance.total_withdrawals
            total_balance.admin_total_balance = total_balance.total_deposits - total_balance.total_withdrawals - personal_usage
            total_balance.save()
        
# Personal Usage 
class PersonalUsage(models.Model):
    """
    Tracks admin deduction and refunds without affecting 
    the users balances
    """

    USAGE_TYPE = [
        ('deduction', 'Deduction'),
        ('refund', 'Refund'),
    ]

    type = models.CharField(max_length=10, choices=USAGE_TYPE, default='deduction')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save() to automatically update TotalBalance
        when a record is added.
        """
        super().save(*args, **kwargs) # Saves the entry first
        TotalBalance.update_personal_usage()    # Automatically update total balance

    def delete(self, *args, **kwargs):
        """
        Override delete() to ensure balances are updated when
        automatically update TotalBalance when an entry is removed.
        """
        super().delete(*args, **kwargs)
        TotalBalance.update_personal_usage()


# Transaction Log 
class TransactionLog(models.Model):
    """
    This table logs every transactions for auditing purposes
    """

    TRANSACTION_TYPE = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('refund', 'Refund'),
        ('personal_usage', 'Personal Usage')
    ]

    STATUS_TYPE = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    deposit_transaction = models.ForeignKey(Deposit, on_delete=models.SET_NULL, blank=True, null=True, related_name="deposits")
    withdrawal_transaction = models.ForeignKey(Withdrawal, on_delete=models.SET_NULL, blank=True, null=True, related_name="withdrawals")
    is_admin_only = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_TYPE)
    updated_at = models.DateTimeField(auto_now=True)
