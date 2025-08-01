#!/usr/bin/env python3
"""
Donor Signals Pattern Module
Detects donor behavior patterns for predictive fundraising
"""

from .base_pattern import DomainPattern


def load_donor_patterns():
    """Load all donor-related patterns"""
    patterns = [
        DomainPattern(
            name="major_gift_prospect",
            pattern=r"(donor|prospect).*(capacity|wealth).*(major|significant)",
            domain="donor",
            severity="high",
            agent="donor_intelligence",
            resolution="major_gift_cultivation_cascade",
            force_multiplier=25,
            context_hints=["major_gift", "high_capacity", "cultivation"],
            allowed_sources=["crm_export", "wealth_screening", "internal"],
            compliance_tags=["pii_restricted", "hipaa_compliant", "confidential"]
        ),

        DomainPattern(
            name="donor_engagement_declining",
            pattern=r"(donor|supporter).*(engagement|activity).*(declining|decreased|dropped)",
            domain="donor",
            severity="high",
            agent="donor_intelligence",
            resolution="retention_intervention_cascade",
            force_multiplier=15,
            context_hints=["retention", "at_risk", "engagement"],
            allowed_sources=["crm_export", "engagement_metrics"],
            compliance_tags=["pii_restricted", "hipaa_compliant"]
        ),

        DomainPattern(
            name="recurring_donation_failed",
            pattern=r"(recurring|monthly|subscription).*(donation|gift).*(failed|declined)",
            domain="donor",
            severity="critical",
            agent="donor_intelligence",
            resolution="payment_recovery_cascade",
            force_multiplier=20,
            context_hints=["payment", "recurring", "recovery"],
            allowed_sources=["payment_processor", "donation_platform"],
            compliance_tags=["pii_restricted", "pci_compliant"]
        ),

        DomainPattern(
            name="lapsed_donor_reactivation",
            pattern=r"(lapsed|inactive|former).*(donor|supporter).*(12|18|24) months",
            domain="donor",
            severity="medium",
            agent="donor_intelligence",
            resolution="reactivation_campaign_cascade",
            force_multiplier=12,
            context_hints=["lapsed", "reactivation", "win_back"],
            allowed_sources=["crm_export", "donor_analytics"],
            compliance_tags=["pii_restricted", "hipaa_compliant"]
        ),

        DomainPattern(
            name="upgrade_potential_identified",
            pattern=r"(donor|supporter).*(upgrade|increase).*(potential|opportunity)",
            domain="donor",
            severity="medium",
            agent="donor_intelligence",
            resolution="upgrade_ask_cascade",
            force_multiplier=18,
            context_hints=["upgrade", "increase", "ask_amount"],
            allowed_sources=["predictive_model", "donor_analytics"],
            compliance_tags=["pii_restricted", "model_output"]
        ),

        DomainPattern(
            name="donor_milestone_approaching",
            pattern=r"(donor|supporter).*(anniversary|milestone|years)",
            domain="donor",
            severity="medium",
            agent="donor_intelligence",
            resolution="milestone_recognition_cascade",
            force_multiplier=10,
            context_hints=["milestone", "recognition", "stewardship"],
            allowed_sources=["crm_export", "anniversary_tracker"],
            compliance_tags=["pii_restricted", "celebration"]
        ),

        DomainPattern(
            name="gift_acknowledgment_pending",
            pattern=r"(gift|donation).*(acknowledgment|receipt).*(pending|needed)",
            domain="donor",
            severity="high",
            agent="donor_intelligence",
            resolution="acknowledgment_generation_cascade",
            force_multiplier=8,
            context_hints=["acknowledgment", "receipt", "tax"],
            allowed_sources=["donation_platform", "gift_processing"],
            compliance_tags=["pii_restricted", "irs_compliant"]
        ),

        DomainPattern(
            name="planned_giving_indicator",
            pattern=r"(estate|bequest|planned).*(gift|giving|interest)",
            domain="donor",
            severity="high",
            agent="donor_intelligence",
            resolution="planned_giving_cultivation_cascade",
            force_multiplier=30,
            context_hints=["planned_giving", "estate", "legacy"],
            allowed_sources=["donor_survey", "wealth_screening"],
            compliance_tags=["pii_restricted", "confidential", "legacy"]
        ),

        DomainPattern(
            name="corporate_partnership_signal",
            pattern=r"(corporate|company|business).*(interest|partnership|sponsorship)",
            domain="donor",
            severity="high",
            agent="donor_intelligence",
            resolution="corporate_cultivation_cascade",
            force_multiplier=35,
            context_hints=["corporate", "partnership", "sponsorship"],
            allowed_sources=["business_development", "linkedin_data"],
            compliance_tags=["business_data", "partnership"]
        ),

        DomainPattern(
            name="donor_fatigue_risk",
            pattern=r"(donor|supporter).*(fatigue|oversolicitation|too many)",
            domain="donor",
            severity="high",
            agent="donor_intelligence",
            resolution="communication_optimization_cascade",
            force_multiplier=12,
            context_hints=["fatigue", "oversolicitation", "frequency"],
            allowed_sources=["engagement_metrics", "donor_feedback"],
            compliance_tags=["pii_restricted", "preference_management"]
        )
    ]

    return patterns


# Pattern cascade definitions
DONOR_CASCADES = {
    "major_gift_cultivation_cascade": {
        "steps": [
            "verify_wealth_capacity",
            "analyze_giving_history",
            "identify_connection_points",
            "assign_gift_officer",
            "create_cultivation_plan",
            "schedule_discovery_visit",
            "prepare_impact_portfolio",
            "update_crm_strategy",
            "set_touch_point_reminders",
            "generate_briefing_materials"
        ],
        "estimated_time": 2700,  # 45 minutes
        "outputs": 12
    },

    "retention_intervention_cascade": {
        "steps": [
            "analyze_engagement_metrics",
            "identify_decline_triggers",
            "segment_by_risk_level",
            "personalize_outreach_message",
            "select_communication_channel",
            "schedule_intervention",
            "assign_relationship_manager",
            "create_re_engagement_offer",
            "track_response_metrics"
        ],
        "estimated_time": 1200,  # 20 minutes
        "outputs": 9
    },

    "payment_recovery_cascade": {
        "steps": [
            "identify_failure_reason",
            "check_card_expiration",
            "generate_update_link",
            "send_payment_notification",
            "schedule_follow_up",
            "offer_alternative_methods",
            "update_payment_record",
            "notify_finance_team"
        ],
        "estimated_time": 600,  # 10 minutes
        "outputs": 8
    }
}


def get_donor_cascade(cascade_name: str) -> dict:
    """Get cascade definition for donor domain"""
    return DONOR_CASCADES.get(cascade_name, {})
