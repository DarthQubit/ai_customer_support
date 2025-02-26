from typing import Dict, Any
from agents.ticket_analysis_agent import TicketAnalysisAgent
from agents.response_agent import ResponseAgent


class TicketProcessor:
    def __init__(self):
        self.analysis_agent = TicketAnalysisAgent()
        self.response_agent = ResponseAgent()
        self.context = {}

    async def process_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        try:

            self.context["customer_name"] = ticket.get("customer_info", {}).get("name", "Customer")
            # Optionally, set this flag to True to use custom templates
            self.context["use_custom_template"] = ticket.get("use_custom_template", False)


            analysis = await self.analysis_agent.analyze_ticket(
                ticket.get("content", ""),
                ticket.get("customer_info", {})
            )

            response_templates = {
                "access_issue": (
                    "Hello {name},\n\n"
                    "I understand you're having trouble accessing the {feature}. Let me help you resolve this.\n\n"
                    "{diagnosis}\n\n"
                    "{resolution_steps}\n\n"
                    "Priority Status: {priority_level}\n"
                    "Estimated Resolution: {eta}\n\n"
                    "Please let me know if you need any clarification.\n\n"
                    "Best regards,\n"
                    "Baguette Support"
                ),
                "billing_inquiry": (
                    "Hi {name},\n\n"
                    "Thank you for your inquiry about {billing_topic}.\n\n"
                    "{explanation}\n\n"
                    "{next_steps}\n\n"
                    "If you have any questions, don't hesitate to ask.\n\n"
                    "Best regards,\n"
                    "Baguette Billing Team"
                )
            }
            # Generate response
            response = await self.response_agent.generate_response(analysis, response_templates, self.context)
            return {
                "ticket_analysis": analysis,
                "response": response
            }
        except Exception as e:
            return {"error": str(e)}
