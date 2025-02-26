import pytest
from agents.ticket_analysis_agent import TicketAnalysisAgent

@pytest.mark.asyncio
async def test_invalid_input_error_handling():
    agent = TicketAnalysisAgent()
    analysis = await agent.analyze_ticket("")
    assert analysis is not None

@pytest.mark.asyncio
async def test_exception_handling_in_analysis():
    agent = TicketAnalysisAgent()
    with pytest.raises(Exception):
        await agent.analyze_ticket(None)
