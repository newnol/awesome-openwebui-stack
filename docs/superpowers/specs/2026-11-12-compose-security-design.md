# Compose Security Refresh — Design (2026-11-12)

**Goal:** Keep the four-service reference stack while removing insecure out-of-box defaults and documenting a current release upgrade path.

**Selected approach:** Preserve volumes and external network, require nonempty credentials, loopback-bind host services, remove the database host port, propose upstream release tags, and document compatibility and backup requirements.

**Alternatives considered:** Rebuild as a production platform (too large for this sample); update only documentation (retains insecure defaults).

**Non-goals:** Runtime deployment, migration of live databases, certifying the stack, or an automatic merge. Compose config and static tests do not prove compatibility; pinned tags are not verified OCI digests.
