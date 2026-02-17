class HelloService:
    """
    Service layer responsible for greeting logic.
    This layer should not depend on Django.
    """

    @staticmethod
    def generate_greeting(name: str) -> dict:
        """
        Generates greeting response.
        """

        # Validation logic
        if not name:
            return {"error": "Name parameter is required"}

        return {"message": f"Hello, {name}!"}
