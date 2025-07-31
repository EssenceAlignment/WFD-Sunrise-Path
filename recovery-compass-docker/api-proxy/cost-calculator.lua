-- Cost Calculator for API Usage
-- Tracks estimated costs per API request

local cost_table = {
  charityapi = {
    base_cost = 0.001,  -- $0.001 per request
    live_multiplier = 10  -- 10x cost for live vs test
  },
  airtable = {
    base_cost = 0.0005,  -- $0.0005 per request
    rate_limit = 5  -- 5 requests/second
  },
  perplexity = {
    base_cost = 0.005,  -- $0.005 per request
    token_cost = 0.00002  -- per token (estimated)
  }
}

function calculate_api_cost(api_name, mode, response_size)
  local api_costs = cost_table[api_name]
  if not api_costs then
    return 0
  end

  local cost = api_costs.base_cost

  -- Apply mode multiplier for CharityAPI
  if api_name == "charityapi" and mode == "live" then
    cost = cost * api_costs.live_multiplier
  end

  -- Estimate token cost for Perplexity based on response size
  if api_name == "perplexity" and response_size then
    local estimated_tokens = response_size / 4  -- rough estimate
    cost = cost + (estimated_tokens * api_costs.token_cost)
  end

  return cost
end

-- Export function for use in Envoy
return {
  calculate_cost = calculate_api_cost
}
