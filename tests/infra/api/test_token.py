def test_single_token_acceptance(client):
    """
    GET /chains/solana/tokens/token1
    Should return one summary with correct values.
    """
    response = client.get("/chains/solana/tokens/token1")
    assert response.status_code == 200, response.text

    body = response.json()
    assert body["number_of_pools"] == 1
    assert body["total_liquidity_usd"] == 100.0

    lp = body["largest_pool"]
    assert lp["liquidity"]["usd"] == 100.0

def test_multi_token_acceptance(client):
    """
    GET /chains/solana/tokens?addresses=addr1,addr2
    Should return two summaries in a list, one per token.
    """
    response = client.get("/chains/solana/tokens?addresses=addr1,addr2")
    assert response.status_code == 200, response.text

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2

    summary1 = next(s for s in body if s["largest_pool"]["baseToken"]["address"] == "addr1")
    assert summary1["number_of_pools"] == 1
    assert summary1["total_liquidity_usd"] == 100.0

    summary2 = next(s for s in body if s["largest_pool"]["baseToken"]["address"] == "addr2")
    assert summary2["number_of_pools"] == 1
    assert summary2["total_liquidity_usd"] == 200.0
