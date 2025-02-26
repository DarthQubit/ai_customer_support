import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from transformers import pipeline

class TicketCategory(Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    FEATURE = "feature"
    ACCESS = "access"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class TicketAnalysis:
    category: TicketCategory
    priority: Priority
    key_points: List[str]
    required_expertise: List[str]
    sentiment: float
    urgency_indicators: List[str]
    business_impact: str
    suggested_response_type: str

class TicketAnalysisAgent:
    def __init__(self):
        # Zero-shot classification model for categorization
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        # Sentiment analysis using a fine-tuned DistilBERT model
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    async def analyze_ticket(
        self,
        ticket_content: str,
        customer_info: Optional[Dict[str, Any]] = None
    ) -> TicketAnalysis:
        # Raise exception if None is passed
        if ticket_content is None:
            raise Exception("Ticket content cannot be None")
        try:
            # If content is empty or whitespace only, return a default analysis
            if not ticket_content.strip():
                return TicketAnalysis(
                    category=TicketCategory.TECHNICAL,  # default category
                    priority=Priority.LOW,
                    key_points=[],
                    required_expertise=[],
                    sentiment=0.0,
                    urgency_indicators=[],
                    business_impact="normal",
                    suggested_response_type="standard"
                )

            # Zero-shot classification for ticket category
            candidate_labels = [label.value for label in TicketCategory]
            classification = self.classifier(ticket_content, candidate_labels)
            best_label = classification["labels"][0]
            category = TicketCategory(best_label.lower())

            # Identify urgency keywords
            urgency_keywords = ["asap", "urgent", "immediately", "crashed", "error", "system down"]
            urgency_indicators = [word for word in urgency_keywords if word in ticket_content.lower()]

            # Set priority based on customer role
            role_priority = Priority.LOW
            if customer_info and "role" in customer_info:
                role = customer_info["role"].lower()
                if any(title in role for title in ["director", "ceo", "cfo", "cto", "vp", "chief"]):
                    role_priority = Priority.HIGH

            # Check for business impact keywords
            business_impact = "normal"
            if "payroll" in ticket_content.lower() or "revenue" in ticket_content.lower():
                business_impact = "critical"
                role_priority = Priority.URGENT

            overall_priority = Priority.URGENT if urgency_indicators else role_priority


            sentences = re.split(r'\.|\n', ticket_content)
            key_points = [s.strip() for s in sentences if s and len(s.split()) >= 3]


            #sentiment_result = self.sentiment_pipeline(ticket_content)
            #sentiment = sentiment_result[0]['score'] if sentiment_result[0]['label'] == 'POSITIVE' else -sentiment_result[0]['score']
            # Perform sentiment analysis and return a word instead of a numeric score
            sentiment_result = self.sentiment_pipeline(ticket_content)
            sentiment_label = sentiment_result[0]['label']
            sentiment = "Positive" if sentiment_label.upper() == "POSITIVE" else "Negative"


            # Map category to required expertise
            expertise_mapping = {
                TicketCategory.TECHNICAL: ["Technical Support"],
                TicketCategory.BILLING: ["Billing Specialist"],
                TicketCategory.FEATURE: ["Product Manager"],
                TicketCategory.ACCESS: ["IT Support"]
            }
            required_expertise = expertise_mapping.get(category, [])

            suggested_response_type = "standard" if overall_priority != Priority.URGENT else "immediate"

            return TicketAnalysis(
                category=category,
                priority=overall_priority,
                key_points=key_points,
                required_expertise=required_expertise,
                sentiment= sentiment,
                urgency_indicators=urgency_indicators,
                business_impact=business_impact,
                suggested_response_type=suggested_response_type
            )
        except Exception as e:
            raise Exception(f"Error in TicketAnalysisAgent.analyze_ticket: {str(e)}")
