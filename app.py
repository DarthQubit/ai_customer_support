import streamlit as st
import asyncio
from agents.ticket_processor import TicketProcessor


def main():
    st.title("AI-Powered Customer Support Ticket Processing")
    st.markdown("Enter ticket details below and click **Process Ticket**.")

    # Use empty strings for `value` and set placeholders
    ticket_id = st.text_input("Ticket ID", value="", placeholder="Enter ticket ID here")
    subject = st.text_input("Subject", value="", placeholder="Enter subject here")
    content = st.text_area("Ticket Content", value="", placeholder="Enter ticket details here...")
    customer_name = st.text_input("Customer Name", value="", placeholder="Enter your name")
    customer_role = st.text_input("Customer Role", value="", placeholder="Enter customer role")
    customer_plan = st.text_input("Customer Plan", value="", placeholder="Enter customer plan")
    customer_company_size = st.text_input("Company Size", value="", placeholder="Enter company size")

    # Checkbox can remain the same
    use_custom_template = st.checkbox("Use Custom Template")

    if st.button("Process Ticket"):
        ticket = {
            "id": ticket_id,
            "subject": subject,
            "content": content,
            "customer_info": {
                "name": customer_name,
                "role": customer_role,
                "plan": customer_plan,
                "company_size": customer_company_size
            },
            "use_custom_template": use_custom_template
        }
        st.info("Processing ticket...")
        processor = TicketProcessor()
        result = asyncio.run(processor.process_ticket(ticket))

        st.subheader("Ticket Analysis")
        analysis = result.get("ticket_analysis")
        if analysis:
            st.json({
                "Category": analysis.category.value,
                "Priority": analysis.priority.name,
                "Key Points": analysis.key_points,
                "Required Expertise": analysis.required_expertise,
                "Sentiment": analysis.sentiment,
                "Urgency Indicators": analysis.urgency_indicators,
                "Business Impact": analysis.business_impact,
                "Suggested Response Type": analysis.suggested_response_type
            })
        else:
            st.error("Error processing ticket analysis.")

        st.subheader("Response Suggestion")
        response = result.get("response")
        if response:
            st.write(response["response_text"])
        else:
            st.error("Error generating response.")


if __name__ == "__main__":
    main()
