"""
BB Creative Ads Agent
Powered by Claude claude-opus-4-6 with adaptive thinking and tool use.
"""

import json
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Tool definitions ────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "generate_ad_copy",
        "description": (
            "Generate compelling ad copy variants for a given product or campaign. "
            "Returns headline, description, and call-to-action options."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "string",
                    "description": "Product or service name to advertise",
                },
                "audience": {
                    "type": "string",
                    "description": "Target audience description",
                },
                "tone": {
                    "type": "string",
                    "enum": ["professional", "playful", "urgent", "inspirational"],
                    "description": "Desired tone of the ad copy",
                },
                "platform": {
                    "type": "string",
                    "enum": ["google", "meta", "display", "youtube"],
                    "description": "Advertising platform",
                },
            },
            "required": ["product", "audience", "tone", "platform"],
        },
    },
    {
        "name": "analyze_ad_performance",
        "description": (
            "Analyze ad performance metrics and return insights and recommendations. "
            "Simulates fetching live campaign data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_id": {
                    "type": "string",
                    "description": "Campaign identifier to analyze",
                },
                "metric": {
                    "type": "string",
                    "enum": ["ctr", "cpc", "roas", "impressions", "conversions", "all"],
                    "description": "Metric to focus the analysis on",
                },
            },
            "required": ["campaign_id", "metric"],
        },
    },
    {
        "name": "suggest_creative_improvements",
        "description": (
            "Review existing ad creative and suggest data-driven improvements "
            "based on industry best practices."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "headline": {"type": "string", "description": "Current ad headline"},
                "description": {"type": "string", "description": "Current ad description"},
                "cta": {"type": "string", "description": "Current call-to-action text"},
            },
            "required": ["headline", "description"],
        },
    },
    {
        "name": "get_audience_insights",
        "description": "Retrieve demographic and interest-based insights for a target audience segment.",
        "input_schema": {
            "type": "object",
            "properties": {
                "segment": {
                    "type": "string",
                    "description": "Audience segment name or description",
                },
                "region": {
                    "type": "string",
                    "description": "Geographic region (e.g. 'US', 'EU', 'global')",
                },
            },
            "required": ["segment"],
        },
    },
]


# ── Tool implementations ─────────────────────────────────────────────────────

def generate_ad_copy(product: str, audience: str, tone: str, platform: str) -> dict:
    """Stub: in production, call your copy-generation service or database."""
    templates = {
        "google": {
            "headlines": [
                f"Discover {product} Today",
                f"Best {product} for {audience}",
                f"Get {product} — Limited Time",
            ],
            "descriptions": [
                f"Find the perfect {product} for your needs. Shop now and save.",
                f"Top-rated {product} loved by {audience}. Free shipping available.",
            ],
            "ctas": ["Shop Now", "Learn More", "Get Started"],
        },
        "meta": {
            "headlines": [
                f"Why {audience} Love {product}",
                f"Transform Your Life with {product}",
                f"{product}: See What Everyone's Talking About",
            ],
            "descriptions": [
                f"Join thousands of {audience} who trust {product}. Click to explore.",
                f"Ready to experience {product}? Tap to discover more.",
            ],
            "ctas": ["Shop Now", "Sign Up", "Learn More"],
        },
    }
    base = templates.get(platform, templates["google"])
    return {
        "platform": platform,
        "tone": tone,
        "variants": base,
        "character_limits": {"headline": 30, "description": 90, "cta": 15},
    }


def analyze_ad_performance(campaign_id: str, metric: str) -> dict:
    """Stub: in production, query your ads API (Google Ads, Meta, etc.)."""
    mock_data = {
        "campaign_id": campaign_id,
        "period": "last 30 days",
        "metrics": {
            "ctr": {"value": 3.2, "unit": "%", "benchmark": 2.1, "trend": "+0.4%"},
            "cpc": {"value": 1.45, "unit": "USD", "benchmark": 1.80, "trend": "-$0.12"},
            "roas": {"value": 4.8, "unit": "x", "benchmark": 3.5, "trend": "+0.6x"},
            "impressions": {"value": 245_000, "unit": "count", "trend": "+12%"},
            "conversions": {"value": 1_820, "unit": "count", "trend": "+8%"},
        },
    }
    if metric != "all":
        selected = mock_data["metrics"].get(metric, {})
        mock_data["metrics"] = {metric: selected}
    return mock_data


def suggest_creative_improvements(headline: str, description: str, cta: str = "") -> dict:
    """Stub: in production, run creative scoring models."""
    issues = []
    suggestions = []

    if len(headline) > 30:
        issues.append("Headline exceeds 30 characters")
        suggestions.append("Shorten headline to ≤30 characters for Google Ads compliance")

    if not any(word in headline.lower() for word in ["you", "your", "free", "new", "best", "top"]):
        suggestions.append("Add a power word (e.g. 'you', 'free', 'best') to increase CTR")

    if len(description) < 60:
        issues.append("Description may be too short")
        suggestions.append("Expand description to 60–90 characters with a clear value proposition")

    if not cta:
        suggestions.append("Add a clear call-to-action (e.g. 'Shop Now', 'Get Started')")

    return {
        "score": max(0, 100 - len(issues) * 15 - (10 if not cta else 0)),
        "issues": issues,
        "suggestions": suggestions,
        "original": {"headline": headline, "description": description, "cta": cta},
    }


def get_audience_insights(segment: str, region: str = "global") -> dict:
    """Stub: in production, query your DMP or platform audience APIs."""
    return {
        "segment": segment,
        "region": region,
        "size_estimate": "2.1M – 4.8M",
        "demographics": {
            "age_range": "25–44",
            "gender_split": {"female": "54%", "male": "44%", "other": "2%"},
            "income_bracket": "Middle to upper-middle",
        },
        "top_interests": ["technology", "lifestyle", "sustainability", "travel"],
        "best_ad_times": ["Tue–Thu 10:00–14:00", "Sat 09:00–12:00"],
        "recommended_placements": ["Search", "YouTube", "Gmail"],
    }


# ── Tool dispatcher ───────────────────────────────────────────────────────────

def execute_tool(name: str, tool_input: dict) -> str:
    if name == "generate_ad_copy":
        result = generate_ad_copy(**tool_input)
    elif name == "analyze_ad_performance":
        result = analyze_ad_performance(**tool_input)
    elif name == "suggest_creative_improvements":
        result = suggest_creative_improvements(**tool_input)
    elif name == "get_audience_insights":
        result = get_audience_insights(**tool_input)
    else:
        result = {"error": f"Unknown tool: {name}"}
    return json.dumps(result, indent=2)


# ── Agentic loop ──────────────────────────────────────────────────────────────

def run_ads_agent(user_request: str) -> str:
    """Run the ads agent with an agentic tool-use loop."""
    print(f"\n{'='*60}")
    print(f"User: {user_request}")
    print("=" * 60)

    messages = [{"role": "user", "content": user_request}]

    system = (
        "You are an expert digital advertising strategist and creative director "
        "for BB Creative, a premium advertising agency. You have deep expertise in "
        "Google Ads, Meta Ads, programmatic display, and YouTube advertising. "
        "Use the available tools to provide data-driven, actionable advertising advice. "
        "Always be specific, cite metrics where relevant, and tailor recommendations "
        "to the client's goals."
    )

    while True:
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=system,
            tools=TOOLS,
            messages=messages,
        ) as stream:
            response = stream.get_final_message()

        # Collect text output from this turn
        for block in response.content:
            if block.type == "thinking":
                print(f"\n[Agent thinking... ({len(block.thinking)} chars)]")
            elif block.type == "text" and block.text:
                print(f"\nAgent: {block.text}")

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason != "tool_use":
            break

        # Execute tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\n[Tool call: {block.name}({json.dumps(block.input)})]")
                result = execute_tool(block.name, block.input)
                print(f"[Tool result preview: {result[:120]}...]")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        # Append assistant turn + tool results
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    # Return final text response
    final_texts = [b.text for b in response.content if b.type == "text" and b.text]
    return "\n".join(final_texts)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo_requests = [
        (
            "Generate Google Search ad copy for our new AI-powered project management tool "
            "targeting startup founders aged 25–40. Use a professional tone."
        ),
        (
            "Analyze the performance of campaign CAM-2024-Q1 focusing on ROAS, "
            "then suggest creative improvements for headline 'Boost Your Productivity' "
            "and description 'Try our tool'."
        ),
        (
            "Get audience insights for 'eco-conscious millennials' in the US and recommend "
            "the best ad formats and messaging approach for a sustainable fashion brand."
        ),
    ]

    for request in demo_requests:
        run_ads_agent(request)
        print("\n" + "-" * 60 + "\n")
