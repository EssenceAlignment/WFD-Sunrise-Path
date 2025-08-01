#!/usr/bin/env python3
"""
Funder Keywords Pattern Module
Detects grant opportunities, RFPs, and funding announcements
"""

from .base_pattern import DomainPattern


def load_funder_patterns():
    """Load all funding-related patterns"""
    patterns = [
        DomainPattern(
            name="rfp_deadline_approaching",
            pattern=r"(RFP|grant).*(deadline|due).*(approaching|soon|days)",
            domain="funding",
            severity="high",
            agent="grant_writer",
            resolution="rfp_analysis_cascade",
            force_multiplier=15,
            context_hints=["deadline", "urgent", "grant"],
            allowed_sources=["grants.gov", "foundation_center", "sam.gov"],
            compliance_tags=["public_data", "no_pii"]
        ),

        DomainPattern(
            name="mental_health_grant",
            pattern=r"(mental health|behavioral health|substance).*(grant|funding|opportunity)",
            domain="funding",
            severity="high",
            agent="grant_writer",
            resolution="mental_health_grant_cascade",
            force_multiplier=20,
            context_hints=["mental_health", "recovery", "funding"],
            allowed_sources=["grants.gov", "samhsa.gov", "foundation_center"],
            compliance_tags=["public_data", "no_pii", "mission_aligned"]
        ),

        DomainPattern(
            name="federal_funding_announcement",
            pattern=r"(federal|SAMHSA|HHS|NIH).*(funding|grant).*(announcement|opportunity)",
            domain="funding",
            severity="high",
            agent="grant_writer",
            resolution="federal_grant_cascade",
            force_multiplier=25,
            context_hints=["federal", "government", "large_grant"],
            allowed_sources=["grants.gov", "sam.gov", "agency_sites"],
            compliance_tags=["public_data", "no_pii", "federal_compliant"]
        ),

        DomainPattern(
            name="foundation_grant_open",
            pattern=r"(foundation|private).*(grant|funding).*(open|accepting|available)",
            domain="funding",
            severity="medium",
            agent="grant_writer",
            resolution="foundation_grant_cascade",
            force_multiplier=12,
            context_hints=["foundation", "private_funding"],
            allowed_sources=["foundation_center", "candid.org"],
            compliance_tags=["public_data", "no_pii"]
        ),

        DomainPattern(
            name="grant_match_score_high",
            pattern=r"(match score|alignment).*(high|excellent|strong).*(grant|opportunity)",
            domain="funding",
            severity="high",
            agent="grant_writer",
            resolution="high_match_pursuit_cascade",
            force_multiplier=18,
            context_hints=["high_probability", "strong_match"],
            allowed_sources=["internal_scoring", "grant_analysis"],
            compliance_tags=["internal_data", "no_pii"]
        ),

        DomainPattern(
            name="capacity_building_grant",
            pattern=r"(capacity building|infrastructure|organizational).*(grant|funding)",
            domain="funding",
            severity="medium",
            agent="grant_writer",
            resolution="capacity_grant_cascade",
            force_multiplier=15,
            context_hints=["infrastructure", "capacity", "organizational"],
            allowed_sources=["grants.gov", "foundation_center"],
            compliance_tags=["public_data", "no_pii"]
        ),

        DomainPattern(
            name="emergency_funding_available",
            pattern=r"(emergency|rapid|urgent).*(funding|grant|assistance).*(available|open)",
            domain="funding",
            severity="critical",
            agent="grant_writer",
            resolution="emergency_funding_cascade",
            force_multiplier=30,
            context_hints=["urgent", "rapid_response", "emergency"],
            allowed_sources=["emergency_funders", "rapid_response_networks"],
            compliance_tags=["public_data", "no_pii", "expedited"]
        ),

        DomainPattern(
            name="recurring_grant_opportunity",
            pattern=r"(annual|recurring|yearly).*(grant|funding).*(cycle|opportunity)",
            domain="funding",
            severity="medium",
            agent="grant_writer",
            resolution="recurring_grant_cascade",
            force_multiplier=10,
            context_hints=["predictable", "annual", "planning"],
            allowed_sources=["grants.gov", "foundation_center"],
            compliance_tags=["public_data", "no_pii"]
        ),

        DomainPattern(
            name="collaboration_funding",
            pattern=r"(collaborative|partnership|coalition).*(grant|funding)",
            domain="funding",
            severity="medium",
            agent="grant_writer",
            resolution="collaboration_cascade",
            force_multiplier=22,
            context_hints=["partnership", "multi_org", "collaborative"],
            allowed_sources=["grants.gov", "foundation_center"],
            compliance_tags=["public_data", "no_pii", "partnership_required"]
        ),

        DomainPattern(
            name="innovation_grant",
            pattern=r"(innovation|pilot|demonstration).*(grant|funding|project)",
            domain="funding",
            severity="medium",
            agent="grant_writer",
            resolution="innovation_grant_cascade",
            force_multiplier=16,
            context_hints=["innovation", "pilot", "new_approach"],
            allowed_sources=["grants.gov", "innovation_funders"],
            compliance_tags=["public_data", "no_pii", "innovation_focus"]
        )
    ]

    return patterns


# Pattern cascade definitions
FUNDING_CASCADES = {
    "rfp_analysis_cascade": {
        "steps": [
            "extract_rfp_requirements",
            "assess_organizational_fit",
            "calculate_roi_score",
            "generate_go_no_go_recommendation",
            "create_proposal_timeline",
            "assign_writing_team",
            "notify_stakeholders"
        ],
        "estimated_time": 1800,  # 30 minutes
        "outputs": 10
    },

    "mental_health_grant_cascade": {
        "steps": [
            "verify_mission_alignment",
            "extract_eligibility_criteria",
            "gather_outcome_data",
            "calculate_competitive_advantage",
            "draft_concept_note",
            "schedule_team_review",
            "prepare_loi_template",
            "update_grant_calendar",
            "notify_clinical_team",
            "archive_opportunity"
        ],
        "estimated_time": 2400,  # 40 minutes
        "outputs": 15
    },

    "federal_grant_cascade": {
        "steps": [
            "verify_sam_registration",
            "check_debarment_status",
            "analyze_cfda_requirements",
            "assess_indirect_cost_impact",
            "evaluate_compliance_burden",
            "calculate_true_cost",
            "generate_executive_summary",
            "create_compliance_checklist",
            "assign_federal_specialist",
            "schedule_go_no_go_meeting",
            "prepare_board_briefing",
            "update_federal_tracker"
        ],
        "estimated_time": 3600,  # 60 minutes
        "outputs": 20
    }
}


def get_funding_cascade(cascade_name: str) -> dict:
    """Get cascade definition for funding domain"""
    return FUNDING_CASCADES.get(cascade_name, {})
