from app.repositories.customer import CustomerRepository


class CustomerService:
    """Service for customer-related operations"""

    def __init__(self,repository:CustomerRepository):
        self.repository = repository

    def get_customer(self,customer_id:str) -> dict | None:
        return self.repository.get_customer(customer_id)