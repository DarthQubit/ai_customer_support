import pytest
from agents.ticket_analysis_agent import TicketAnalysisAgent, Priority, TicketCategory

@pytest.mark.asyncio
async def test_priority_assignment():
    agent = TicketAnalysisAgent()
    ticket_content = "Cannot access admin dashboard. Need this fixed ASAP as payroll is due."
    customer_info = {"role": "Finance Director"}
    analysis = await agent.analyze_ticket(ticket_content, customer_info)
    assert analysis.priority.name == "URGENT"
    assert analysis.category == TicketCategory.ACCESS

@pytest.mark.asyncio
async def test_key_points_extraction():
    agent = TicketAnalysisAgent()
    ticket_content = "Error 404. Access issue. Please resolve promptly."
    analysis = await agent.analyze_ticket(ticket_content)
    assert len(analysis.key_points) > 0
