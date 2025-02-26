from transformers import pipeline
from agents.ticket_analysis_agent import Priority

class ResponseAgent:
    def __init__(self):
        self.generator = pipeline("text-generation", model="distilgpt2") #tiiuae/falcon-7b-instruct

    def create_custom_template(self, ticket_analysis, context):
        # Prompt for generating a custom template
        prompt = (
            f"Create a professional and concise customer support response template for a ticket classified as {ticket_analysis.category.value} "
            f"with {ticket_analysis.priority.name} priority. Include placeholders for customer name, diagnosis, resolution steps, and estimated resolution time. "
            "Format the response with line breaks and end with 'Best regards,\\nBaguette Support'."
        )
        custom_template_result = self.generator(
            prompt,
            max_length=100,
            truncation=True,
            do_sample=False,
            num_return_sequences=1
        )
        custom_template = custom_template_result[0]['generated_text']

        if prompt in custom_template:
            custom_template = custom_template.split(prompt)[-1].strip()
        return custom_template

    async def generate_response(
        self,
        ticket_analysis: any,
        response_templates: dict,
        context: dict
    ) -> dict:
        try:

            if context.get("use_custom_template", False):
                template = self.create_custom_template(ticket_analysis, context)
            else:
                if ticket_analysis.category.value == "access":
                    template = response_templates.get("access_issue", "")
                elif ticket_analysis.category.value == "billing":
                    template = response_templates.get("billing_inquiry", "")
                else:
                    template = (
                        "Hello {name},\n\nThank you for your message. We are looking into your issue and will get back to you shortly.\n\nBest regards,\nSupport Team"
                    )


            customer_name = context.get("customer_name", "Customer")
            diagnosis = "We have identified the issue based on your report."
            resolution_steps = "Our team is working to resolve the problem."
            priority_level = ticket_analysis.priority.name
            eta = "within 2 hours" if ticket_analysis.priority == Priority.URGENT else "within 24 hours"
            billing_topic = "your billing query"
            explanation = "Here is the detailed explanation regarding your billing question."
            next_steps = "Please review the details and let us know if you have further questions."

            response_text = template.format(
                name=customer_name,
                feature="the requested feature",
                diagnosis=diagnosis,
                resolution_steps=resolution_steps,
                priority_level=priority_level,
                eta=eta,
                billing_topic=billing_topic,
                explanation=explanation,
                next_steps=next_steps
            )

            # Generate final response with controlled parameters
            generated = self.generator(
                response_text,
                max_length=150,
                truncation=True,
                do_sample=False,
                num_return_sequences=1
            )
            final_response = generated[0]["generated_text"]

            if "Estimated Resolution:" in final_response:
                final_response = final_response.replace("Estimated Resolution:", "\nEstimated Resolution:")

            if "Best regards," in final_response:
                parts = final_response.split("Best regards,")
                final_response = final_response.split("Best regards,")[0] + "Best regards,\nBaguette Support"

            return {
                "response_text": final_response,
                "confidence_score": 0.9,
                "requires_approval": False,
                "suggested_actions": ["Follow-up call", "Email confirmation"]
            }
        except Exception as e:
            raise Exception(f"Error in ResponseAgent.generate_response: {str(e)}")
