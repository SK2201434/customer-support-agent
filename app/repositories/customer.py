from app.database.connection import get_connection

class CustomerRepository:
    """repository for accessing customer data. """

    def get_customer(self,customer_id:str) -> dict | None:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id,name,email,plan FROM customers WHERE id = ?""",(customer_id,),)
        row = cursor.fetchone()
        connection.close()
        if row is None:
            return None

        return{
            "id":row[0],
            "name":row[1],
            "email":row[2],
            "plan":row[3]
        }