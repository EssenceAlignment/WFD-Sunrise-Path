"""
Tests for Context Management and Context-Aware Pattern Analysis
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from main import app, contexts_store  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_contexts():
    """Clear context store before each test"""
    contexts_store.clear()
    yield
    contexts_store.clear()


class TestContextManagement:
    """Test suite for context management endpoints"""

    @pytest.mark.ci_gate
    def test_create_context_success(self):
        """Test successful context creation"""
        request_data = {
            "name": "Development Context",
            "description": "Context for development environment",
            "parameters": {
                "user_role": "developer",
                "project_phase": "implementation"
            },
            "environment_definition": {
                "toolchains": ["git", "CI/CD", "Docker"],
                "documentation_systems": ["Confluence", "Markdown"],
                "communication_platforms": ["Slack"],
                "data_storage_solutions": ["PostgreSQL", "Redis"],
                "cloud_providers": ["AWS"],
                "custom_attributes": {
                    "team_size": 15,
                    "compliance_standards": ["HIPAA", "GDPR"]
                }
            }
        }

        response = client.post("/context/create", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert "context_id" in data
        assert data["context_id"].startswith("ctx-")
        assert data["status"] == "success"
        assert "created successfully" in data["message"]

        # Verify context was stored
        assert data["context_id"] in contexts_store
        stored_context = contexts_store[data["context_id"]]
        assert stored_context["name"] == "Development Context"
        assert stored_context["parameters"]["user_role"] == "developer"
        assert len(stored_context["environment_definition"]["toolchains"]) == 3

    @pytest.mark.ci_gate
    def test_create_context_minimal(self):
        """Test context creation with minimal required fields"""
        request_data = {
            "name": "Minimal Context"
        }

        response = client.post("/context/create", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # Verify minimal context
        context_id = data["context_id"]
        stored_context = contexts_store[context_id]
        assert stored_context["name"] == "Minimal Context"
        assert stored_context["description"] is None
        assert stored_context["parameters"] == {}
        assert stored_context["environment_definition"] is None

    @pytest.mark.ci_gate
    def test_update_context_success(self):
        """Test successful context update"""
        # First create a context
        create_response = client.post(
            "/context/create", json={"name": "Test Context"}
        )
        context_id = create_response.json()["context_id"]

        # Update the context
        update_data = {
            "name": "Updated Context",
            "description": "Now with description",
            "parameters": {"updated": True},
            "environment_definition": {
                "toolchains": ["New Tool"]
            }
        }

        response = client.put(f"/context/{context_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["context_id"] == context_id

        # Verify updates
        stored_context = contexts_store[context_id]
        assert stored_context["name"] == "Updated Context"
        assert stored_context["description"] == "Now with description"
        assert stored_context["parameters"]["updated"] is True
        stored_env = stored_context["environment_definition"]
        assert stored_env["toolchains"] == ["New Tool"]

    def test_update_context_not_found(self):
        """Test updating non-existent context"""
        response = client.put(
            "/context/ctx-nonexistent", json={"name": "Update"}
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @pytest.mark.ci_gate
    def test_get_context_success(self):
        """Test successful context retrieval"""
        # Create a context with full data
        request_data = {
            "name": "Complete Context",
            "description": "Full featured context",
            "parameters": {"test": "value"},
            "environment_definition": {
                "toolchains": ["git", "Docker"],
                "custom_attributes": {"team_size": 10}
            }
        }
        create_response = client.post("/context/create", json=request_data)
        context_id = create_response.json()["context_id"]

        # Retrieve the context
        response = client.get(f"/context/{context_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["context_id"] == context_id
        assert data["name"] == "Complete Context"
        assert data["description"] == "Full featured context"
        assert data["parameters"]["test"] == "value"
        env_def = data["environment_definition"]
        assert env_def["toolchains"] == ["git", "Docker"]
        assert env_def["custom_attributes"]["team_size"] == 10
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_context_not_found(self):
        """Test retrieving non-existent context"""
        response = client.get("/context/ctx-nonexistent")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestContextAwarePatternAnalysis:
    """Test suite for context-aware pattern analysis"""

    @pytest.fixture
    def sample_context_id(self):
        """Create a sample context for testing"""
        request_data = {
            "name": "Analysis Test Context",
            "description": "Context for pattern analysis testing",
            "parameters": {
                "user_role": "developer"
            },
            "environment_definition": {
                "toolchains": ["CI/CD"],
                "custom_attributes": {
                    "team_size": 15
                }
            }
        }
        response = client.post("/context/create", json=request_data)
        return response.json()["context_id"]

    @pytest.mark.ci_gate
    def test_analyze_patterns_with_text(self, sample_context_id):
        """Test pattern analysis with text input"""
        request_data = {
            "context_id": sample_context_id,
            "text_input": (
                "We are implementing environmental sustainability "
                "practices in our recovery programs"
            )
        }

        response = client.post("/patterns/analyze", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check patterns detected
        assert len(data["patterns"]) > 0
        pattern = data["patterns"][0]
        assert "pat-" in pattern["id"]
        assert pattern["confidence"] > 0
        assert pattern["context_adjusted_confidence"] > 0
        assert pattern["erd_alignment_score"] > 0
        assert pattern["insurance_compliance_score"] >= 0
        assert pattern["implementation_time_estimate"] > 0
        assert len(pattern["recommendations"]) > 0

        # Check context analysis metrics
        context_analysis = data["context_analysis"]
        assert context_analysis["applicability_score"] > 0
        assert context_analysis["estimated_time_saved"] > 0
        assert context_analysis["automation_potential"] >= 0

        # Check metadata
        meta = data["meta"]
        assert "text" in meta["input_types"]
        assert meta["processing_time_ms"] > 0
        assert meta["ipe_compliance"] is True
        assert meta["baseline_comparison"]["accuracy_improvement"] == 0.38
        assert meta["baseline_comparison"]["false_positive_reduction"] == 0.42

        # Check quantifiable impact
        impact = data["quantifiable_impact"]
        assert "recovery_compass_metrics" in impact
        assert "operational_efficiency" in impact
        rc_metrics = impact["recovery_compass_metrics"]
        assert rc_metrics["erd_alignment_percentage"] > 0
        op_eff = impact["operational_efficiency"]
        assert "minutes" in op_eff["analysis_time_reduction"]

    @pytest.mark.ci_gate
    def test_analyze_patterns_context_adjustment(self, sample_context_id):
        """Test that context adjusts pattern confidence"""
        # Create another context without CI/CD toolchain
        minimal_context_data = {
            "name": "Minimal Context",
            "parameters": {},
            "environment_definition": {
                "toolchains": [],
                "custom_attributes": {"team_size": 3}
            }
        }
        minimal_response = client.post(
            "/context/create", json=minimal_context_data
        )
        minimal_context_id = minimal_response.json()["context_id"]

        # Same text, different contexts
        text = "Implementing automation for environmental monitoring"

        # Analyze with CI/CD context
        response1 = client.post("/patterns/analyze", json={
            "context_id": sample_context_id,
            "text_input": text
        })

        # Analyze with minimal context
        response2 = client.post("/patterns/analyze", json={
            "context_id": minimal_context_id,
            "text_input": text
        })

        data1 = response1.json()
        data2 = response2.json()

        # Context with CI/CD should have higher confidence for automation
        if data1["patterns"] and data2["patterns"]:
            pattern1 = data1["patterns"][0]
            pattern2 = data2["patterns"][0]

            # Context adjustment should be reflected
            adj_conf1 = pattern1["context_adjusted_confidence"]
            adj_conf2 = pattern2["context_adjusted_confidence"]
            assert adj_conf1 != adj_conf2

            # Team size should affect implementation time
            impl_time1 = pattern1["implementation_time_estimate"]
            impl_time2 = pattern2["implementation_time_estimate"]
            assert impl_time1 < impl_time2

    def test_analyze_patterns_context_not_found(self):
        """Test pattern analysis with non-existent context"""
        request_data = {
            "context_id": "ctx-nonexistent",
            "text_input": "Test text"
        }

        response = client.post("/patterns/analyze", json=request_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @pytest.mark.ci_gate
    def test_analyze_patterns_with_structured_data(self, sample_context_id):
        """Test pattern analysis with structured data"""
        request_data = {
            "context_id": sample_context_id,
            "structured_data": (
                '{"recovery_metrics": {"participants": 150, '
                '"success_rate": 0.78}}'
            ),
            "structured_format": "json"
        }

        response = client.post("/patterns/analyze", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Should detect complex data structure pattern
        assert len(data["patterns"]) > 0
        assert "structured" in data["meta"]["input_types"]

        # Check structured data specific defaults
        pattern = data["patterns"][0]
        assert pattern["erd_alignment_score"] == 0.7
        assert pattern["insurance_compliance_score"] == 0.6
        assert pattern["implementation_time_estimate"] == 20

    def test_analyze_patterns_unsafe_content(self, sample_context_id):
        """Test pattern analysis with unsafe content"""
        request_data = {
            "context_id": sample_context_id,
            "text_input": "This contains malware injection exploit code"
        }

        response = client.post("/patterns/analyze", json=request_data)

        assert response.status_code == 400
        assert "Unsafe content detected" in response.json()["detail"]


class TestQuantifiableImpact:
    """Test suite for verifying quantifiable impact metrics"""

    @pytest.mark.ci_gate
    def test_context_creation_time_impact(self):
        """Verify context creation time savings"""
        start_time = datetime.now()

        response = client.post("/context/create", json={
            "name": "Speed Test Context",
            "environment_definition": {
                "toolchains": ["git", "CI/CD", "Docker", "Kubernetes"],
                "documentation_systems": ["Confluence", "Jira"],
                "custom_attributes": {"team_size": 20}
            }
        })

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        assert response.status_code == 200
        # Context creation should be under 10 seconds (vs 30 minutes manual)
        assert processing_time < 10

        # Message should include processing time
        message = response.json()["message"]
        assert "ms" in message

    @pytest.mark.ci_gate
    def test_pattern_analysis_time_savings(self):
        """Verify pattern analysis time savings"""
        # Create context
        context_response = client.post(
            "/context/create", json={"name": "Time Test"}
        )
        context_id = context_response.json()["context_id"]

        # Analyze patterns
        response = client.post("/patterns/analyze", json={
            "context_id": context_id,
            "text_input": (
                "Environmental sustainability recovery program "
                "implementation"
            )
        })

        assert response.status_code == 200
        data = response.json()

        # Check time saved metric
        time_saved = data["context_analysis"]["estimated_time_saved"]
        assert time_saved >= 14  # Should save at least 14 minutes

        # Processing should be under 1 second
        processing_time_ms = data["meta"]["processing_time_ms"]
        assert processing_time_ms < 1000

        # Verify time reduction is reported
        op_eff = data["quantifiable_impact"]["operational_efficiency"]
        time_reduction = op_eff["analysis_time_reduction"]
        assert "minutes" in time_reduction
        assert float(time_reduction.split()[0]) > 14


@pytest.mark.ci_gate
def test_health_check_includes_features():
    """Test that health check reports all features"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"
    assert "pattern-recognition" in data["features"]
    assert "context-management" in data["features"]
    assert "context-aware-analysis" in data["features"]
