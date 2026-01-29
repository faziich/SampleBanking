from datetime import datetime
from typing import List,Dict,Optional

class BankingSystem:
    """Complete banking system"""
    def __init__(self):
        self.accounts: Dict[str,'Bank Account']={}
        self.customers: Dict[str,'Customer']={}

    def add_customer(self, customer_id:str, name:str, email: str):
        """Add New Customer"""
        if customer_id in self.customers:
            raise ValueError(f"Customer {customer_id} already exist")

        self.customers[customer_id]={
            "name":name,
            "email":email,
            "account":[]
        }
        print(f"Customer{name} added")
        return True

    def create_account(self,account_id:str,customer_id:str,account_type:str='savings'):
        """Create New Account for Customer"""
        try:
            if account_type in self.accounts:
                raise ValueError(f"Account {account_id} alredy exist")
            if customer_id in self.customers:
                raise ValueError(f"Customer {customer_id} not found")

            self.accounts[account_id]={
                "customer_id": customer_id,
                "type":account_type,
                "balance":0,
                "transcation":[],
                "created_at":datetime.now()
            }
            self.customers[account_id]["accounts"].append(account_id)
            print(f"Account {account_id} Created")
            return True

        except ValueError as e:
            print(f"Error:{e}")
            return False

    def deposit(self, account_id: str, amount: float):
            """Deposit money"""
            try:
                if account_id not in self.accounts:
                    raise ValueError(f"Account {account_id} not found")
                if amount <= 0:
                    raise  ValueError("Amount must be positive")

                self.accounts[account_id]["balance"] += amount
                self.accounts[account_id]["transactions"].append({
                "type": "deposit",
                "amount": amount,
                "timestamp": datetime.now(),
                "balance_after": self.accounts[account_id]["balance"]
                   })

                print(f"✓✓ Deposited $ Deposited ${amount: .2f}")
                return True
            except ValueError as e:
             print(f"✗✗ Error: Error: {e}")
            return False
    def withdraw(self,account_id:str, amount:float):
        """Withdraw request"""
        try:
            if account_id not in self.accounts:
                raise ValueError(f"Account {account_id} not found")
            if amount<=0:
                raise ValueError(f"Amount must be positive")
            if amount > self.accounts[account_id]["balance"]:
                raise ValueError("Insufficient balance")
            self.accounts[account_id]["balance"]-= amount
            self.accounts[account_id]["transactions"].append({
                "type":"withdrawal",
                "amount":amount,
                "timestamp":datetime.now(),
                "balance_after":self.accounts[account_id]["balance"]
            })
            print(f"Withdraw {amount:2f}")
            return True
        except ValueError as e:
            print(f"Error{e}")
            return False

    def transfer(self, from_account: str, to_account: str, amount: float):
        """Transfer between accounts"""
        try:
            if from_account not in self.accounts:
                raise ValueError (f"From account {from_account} not found")

            if to_account not in self.accounts:
             raise ValueError(f"Toaccount{to_account}not found")

            if from_account == to_account:
                raise ValueError("Cannot transfer to same account")

            if amount <= 0:
                raise ValueError ("Amount must be positive")

            if amount > self.accounts[from_account]["balance"]:
                raise ValueError("Insufficient balance")

            # Perform transfer
            self.accounts[from_account]["balance"] -= amount
            self.accounts[to_account]["balance"] += amount

            # Record transactions d transactions
            self.accounts[from_account]["transactions"].append({
            "type": "transfer_out",
            "to": to_account,
            "amount": amount,
            "timestamp": datetime.now()
            })
            self.accounts[to_account]["transactions"].append({
            "type": "transfer_in",
            "from": from_account,
            "amount": amount,
            "timestamp": datetime.now()
            })
            print(f"✓✓ TTransferred $ ransferred ${amount: .2f} from {from_account} to {to_account}")
            return True

        except ValueError as e:
         print(f"✗✗ Error: Error: {e}")
        return False


    def get_balance(self, account_id: str) -> Optional[float]:
        """Get account balance"""
        if account_id in self.accounts:
            return self.accounts[account_id]["balance"]
        return None

    def get_transaction_history(self, account_id: str, limit: int = 10):
        """Get transaction history"""

        if account_id not in self.accounts:
            print(f"Account {account_id} not found")
            return []
        transactions = self.accounts[account_id]["transactions"]
        return transactions[-limit:]

    def print_account_statement(self, account_id: str):
        """Print complete account statement"""
        if account_id not in self.accounts:
         print(f"Account {account_id} not found")
         return

        account = self.accounts[account_id]
        customer_id = account["customer_id"]
        customer = self.customers[customer_id]
        print(f"\n{'=' * 60}")
        print(f"ACCOUNT STATEMENT")
        print(f"{'=' * 60}")
        print(f"Customer: {customer['name']} ({customer['email']})")
        print(f"Account ID: {account_id}")
        print(f"Account Type: ype: {account['type']}")
        print(f"Created: {account['created_at'].strftime('%Y-%m-%d %H:%M')}")
        print(f"Current Balance: ${account['balance']:,.2f}")
        print(f"\n{'TYPE':<15} {'FROM/T':<15} {'AMOUNT':<12} {'BALANCE':<12}")
        print(f"{'-' * 60}")
        print("=" * 60)

        for txn in account['transactions'][-10:]:


            if txn['type'] == 'deposit':
                print(
                    f"{'Deposit':<15} "
                    f"{'-':<15} "
                    f"${txn['amount']:<14,.2f} "
                    f"${txn.get('balance_after', account['balance']):<14,.2f}"
                )

            elif txn['type'] == 'withdrawal':
                print(
                    f"{'Withdrawal':<15} "
                    f"{'-':<15} "
                    f"${txn['amount']:<14,.2f} "
                    f"${txn.get('balance_after', account['balance']):<14,.2f}"
                )

            elif txn['type'] == 'transfer_out':
                print(
                    f"{'Transfer Out':<15} "
                    f"{txn['to']:<15} "
                    f"${txn['amount']:<14,.2f} "
                    f"${txn.get('balance_after', account['balance']):<14,.2f}"
                )

            elif txn['type'] == 'transfer_in':
                print(
                    f"{'Transfer In':<15} "
                    f"{txn['from']:<15} "
                    f"${txn['amount']:<14,.2f} "
                    f"${txn.get('balance_after', account['balance']):<14,.2f}"
                )

        print("=" * 60)


# Usage Example
if __name__ == "__main__":

    print("SIMPLE BANKING SYSTEM")
    print("=" * 60)

    # Create banking system
    bank = BankingSystem()

    # 1. Adding customers
    print("\n1. Adding Customers...")
    bank.add_customer("CUST001", "Fazal Ur Rehman", "fazal@example.com")
    bank.add_customer("CUST002", "Alice Johnson", "alice@example.com")
    bank.add_customer("CUST003", "Bob Smith", "bob@example.com")

    # 2. Creating accounts
    print("\n2. Creating Accounts...")
    bank.create_account("ACC001", "CUST001", "checking")
    bank.create_account("ACC002", "CUST001", "savings")
    bank.create_account("ACC003", "CUST002", "checking")
    bank.create_account("ACC004", "CUST003", "savings")

    # 3. Performing transactions
    print("\n3. Performing Transactions...")
    bank.deposit("ACC001", 5000)
    bank.deposit("ACC003", 3000)
    bank.deposit("ACC004", 10000)

    # 4. Transfers
    print("\n4. Transfers...")
    bank.transfer("ACC001", "ACC003", 1000)
    bank.transfer("ACC004", "ACC002", 500)

    # 5. Failed transactions (testing error handling)
    print("\n5. Failed Transactions...")
    bank.withdraw("ACC001", 10000)       # Should fail (insufficient balance)
    bank.transfer("ACC001", "ACC999", 100)  # Should fail (account not found)

    # 6. Account statements
    print("\n6. Account Statements...")
    bank.print_account_statement("ACC001")
    bank.print_account_statement("ACC003")
