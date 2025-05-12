# BubbleMaps Trending API 

## Architecture

Architecture diagram: [Link to diagram](https://lucid.app/lucidspark/d43fcdde-9195-49a0-90b1-045cc3eef87b/edit?viewport_loc=-2603%2C-656%2C3326%2C1553%2C0_0&invitationId=inv_b3fca50b-81b2-49d3-aa49-6757510b549c)

- src/ 
  - domain/ : business logic decoupled from Web framework (models / types, business services, repositories)
  - infra/ : http layer using fastapi framework to render data through REST API + could contain DB repo implementation and everything that is infra-related (celery workers ...)
- tests/ : Unit Tests (Business Logic + TDD) + Acceptance Tests (passes through HTTP layer)

## Relevant Endpoints 
- ```/api/chains/{chain_id: str}/tokens/{token_address:str}```: retrieve token information given the network and token address 
- ```/api/chains/{chain_id: str}/tokens?addresses={addr1: str, addr2: str ...}```: list tokens information given the network and token addresses 
