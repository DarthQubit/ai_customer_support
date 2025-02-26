import pytest
from agents.response_agent import ResponseAgent
from agents.ticket_analysis_agent import TicketAnalysis, TicketCategory, Priority

@pytest.mark.asyncio
async def test_response_generation():
    agent = ResponseAgent()
    ticket_analysis = TicketAnalysis(
        category=TicketCategory.BILLING,
        priority=Priority.HIGH,
        key_points=["Billing discrepancy noted"],
        required_expertise=["Billing Specialist"],
        sentiment=0.5,
        urgency_indicators=[],
        business_impact="normal",
        suggested_response_type="standard"
    )
    response_templates = {
        "billing_inquiry": (
            "Hi {name},\n\n"
            "Thank you for your inquiry about {billing_topic}.\n\n"
            "{explanation}\n\n"
            "{next_steps}\n\n"
            "Best regards,\n"
            "Baguette Billing Team"
        )
    }
    context = {"customer_name": "Test User"}
    response = await agent.generate_response(ticket_analysis, response_templates, context)
    assert "response_text" in response
    assert response["confidence_score"] > 0
