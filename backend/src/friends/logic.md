```
[Frontend / App]                                            [FastAPI Backend]
       │                                                           │
       ├────── 1. GET /api/v1/users/search?q=john ────────────────►│
       │                                                           │ (Searches DB by username)
       │◄───── 2. Returns list: [{"id": "uuid-123", ...}] ─────────┤
       │                                                           │
 (User clicks "Connect" on John's card)                            │
       │                                                           │
       ├────── 3. POST /api/v1/connections/request/uuid-123 ─────►│
       │          Header: Authorization Bearer <Sender_JWT>        │ (Extracts Sender from JWT,
       │                                                           │  creates pending connection row)
       │◄───── 4. Returns 201 Created {"status": "pending"} ───────┤
```

You could definitely do it in a single step like POST /friends/request?username=john, but doing Search $\rightarrow$ Send Request with ID is much better for real-world application design.Here is why your initial intuition (searching first, then using the ID) is actually the industry standard:

featuress to impl:
      -check the request status of all response whre sender is curr user and then status is pending
      -remove friend(delete row), block


      