from app.models import run_ai_logic

class SportsAIController:
    @staticmethod
    def process_query(query: str):
        try:
            # We explicitly cast to string here as a final safety check
            result = run_ai_logic(query)
            
            return {
                "status": "success",
                "data": str(result)
            }
        except Exception as e:
            # By returning a dictionary instead of raising an error, 
            # we keep the HTTP status code as 200 (Success) but show the error message.
            return {
                "status": "error",
                "data": f"Internal Controller Error: {str(e)}"
            }