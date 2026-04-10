# Queue Layer

Redis is used for:

- Job queue transport (BullMQ in backend, Celery broker in workers)
- Result backend for Celery
- Response caching in backend

In production, replace single-node Redis with managed Redis (TLS, auth, persistence).
