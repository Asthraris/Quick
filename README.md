# QUICK Backend

jwt,sqlachemy , postgresql

A high-performance, secure backend architecture designed for an ephemeral, "view-once" image-sharing feature. Built using Python and a centralized database model, this project provides the core infrastructure required to manage real-time relationship verification, strict access limitations, and automatic data lifecycles on a dedicated server environment.

---

## 🌟 Project Highlights

* **Anti-Bypass Security Strategy:** Eliminates the common client-side flaws found in ephemeral apps (like the "Airplane Mode Hack"). Media access is tied tightly to active, live database transactions, making it impossible for a user to store or re-watch a piece of media once it has been fetched.
* **Server-First Execution:** The server remains the ultimate source of truth. State updates occur the exact millisecond content is requested rather than waiting for a client-side acknowledgment packet, minimizing network-loss edge cases.
* **Zero-Leak Data Lifecycle:** Storage management is automated entirely at the database infrastructure layer. The application does not rely on scheduled cleanup scripts or manual full-table scans to delete expired content, ensuring the system scales smoothly under heavy usage.

---

## 🏗️ System Architecture & Mechanics

### 1. Two-Step Hybrid Feed Delivery

To optimize network bandwidth and enforce total security, the system separates discovering content from consuming it:

* **The Metadata Pass:** When a user opens their feed, the system compiles and delivers a lightweight text-only summary of available content (sender info, timestamps, and target references). No resource links or media assets are exposed during this phase.
* **The Single-Target Pass:** Media content is fetched strictly one-by-one. When a user intentionally clicks a post, a dedicated isolated request evaluates permissions, permanently marks the item as read, and yields an ephemeral, heavily restricted asset link.

### 2. High-Speed Bidirectional Graph

User relationships utilize a structural double-row synchronization approach. When a friendship is confirmed, the database mirrors the record to represent the link from both perspectives natively. This design optimization guarantees that feed lookups only need to check a single indexed data column to resolve permitted senders at runtime, drastically speeding up application response times.

### 3. Isolated State Journaling

Instead of modifying status markers directly inside a shared media document—which introduces data contention and lock delays when multiple users access items simultaneously—the system uses an atomic audit log (junction table). Every view creates a single, decoupled log entry. A composite index kept in server memory allows the system to check if a specific user has seen a specific post in microseconds.

### 4. Automatic Cascading Expirations

Every piece of content is stamped with an absolute expiration time precisely 24 hours from creation. By establishing cascading rules between core content and tracking logs, a simple database-level daemon can safely remove expired items. The database automatically cleans up and deletes all associated journal rows instantly, keeping the storage layer completely free of dead weight.

---

## 🚀 Media Request Lifecycle

When a user triggers an intention to view an instant image, the backend processes the operations in a strict, sequential workflow to eliminate race conditions:

1. **Constraint Validation:** Runtime Check.
The backend evaluates the user relationship graph and the tracking journal simultaneously to confirm the caller is an active friend of the sender and has not already viewed the file.


2. **Write-First Transaction:** State Commitment.
The backend immediately records the view event to the database journal *before* fetching or exposing the media resource. This ensures that any simultaneous attempts to flood the endpoint fail immediately against database constraints.


3. **Tokenized Authorization:** Asset Exposure.
A temporary, cryptographically signed cloud storage URL is generated for the specific asset. This access window is locked strictly to 20 seconds, preventing external link sharing.


4. **Payload Delivery:** 200 OK Response.
The temporary reference link is safely returned to the device viewport for rendering, bypassing raw binary streaming through the application server entirely.
