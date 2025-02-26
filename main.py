import asyncio
from agents.ticket_processor import TicketProcessor

SAMPLE_TICKETS = [
    {
        "id": "TKT-001",
        "subject": "Cannot access admin dashboard",
        "content": """
Hi Support,
Since this morning I can't access the admin dashboard. I keep getting a 403 error.
I need this fixed ASAP as I need to process payroll today.
Thanks,
John Smith
Finance Director
""",
        "customer_info": {
            "name": "John Smith",
            "role": "Finance Director",
            "plan": "Enterprise",
            "company_size": "250+"
        },
        "use_custom_template": True
    },
    {
        "id": "TKT-002",
        "subject": "Question about billing cycle",
        "content": """
Hello,
Our invoice shows billing from the 15th but we signed up on the 20th.
Can you explain how the pro-rating works?
Best regards,
Sarah Jones
""",
        "customer_info": {
            "name": "Sarah Jones",
            "role": "Billing Admin",
            "plan": "Professional",
            "company_size": "50-249"
        },
        "use_custom_template": False
    }
]

async def main():
    processor = TicketProcessor()
    for ticket in SAMPLE_TICKETS:
        result = await processor.process_ticket(ticket)
        print(f"Ticket ID: {ticket['id']}")
        if "error" in result:
            print("Error:", result["error"])
        else:
            analysis = result["ticket_analysis"]
            response = result["response"]
            print("Ticket Analysis:", analysis)
            print("Response Suggestion:", response)
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
