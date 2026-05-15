# Infrastructure Map: NH Mortgage Lead Pipeline
**Version**: 1.0
**Architect**: Alex (CEO)
**Status**: DRAFT

## 🏛️ System Overview
A sovereign lead generation pipeline designed for high-trust data handling and autonomous local export.

---

## 1. 📥 Ingestion Layer (Lead Intake)
- **API Framework**: FastAPI (running on port 8001).
- **Validation**: Pydantic models for strict data types (ensures no corrupted lead data).
- **Security**: 
    - CORS policy restricted to local/trusted origins.
    - Input sanitization to prevent SQL injection.
    - [PENDING] PII Encryption (AES-256) for Email/Phone fields before storage.

## 2. 💾 Persistence Layer (Sovereign Vault)
- **Database**: SQLite (`tru/Data/mortgage_leads.db`).
- **Data Model**:
    - `leads`: Core PII and loan qualification data.
    - `audit_logs`: Tracking submission attempts and export history.
- **Persistence Strategy**: All database files reside within the `tru/` vault to ensure data sovereignty and easy backup/migration.

## 3. ⚙️ Processing Layer (Intelligence)
- **Lead Scoring Engine**: A logic module to categorize leads (e.g., "Hot", "Warm", "Cold") based on credit score and loan amount.
- **Export Engine**: Pandas-based CSV generator (`lead_manager.py`).
- **Notification Bridge**: [FUTURE] Automated trigger to notify the mortgage company owner (User's Brother) when a "Hot" lead arrives.

## 4. 🚀 DevOps & Maintenance
- **Process Management**: Managed by `heartbeat_daemon.py` to ensure the API stays online.
- **Environment**: Python 3.14 Venv with locked dependencies (`requirements.txt`).
- **Backup**: Vault-wide Git commits for versioning data/state changes.

## 5. 🛡️ Security Protocol (Iron Sentry)
- **Encryption at Rest**: PII data must be encrypted using a local secret key.
- **Sanitized Exports**: Exported CSVs must be stored in protected vault subdirectories.

---

## Next Infrastructure Tasks:
1. [ ] Implement AES-256 encryption for Email/Phone in `lead_manager.py`.
2. [ ] Add `LeadScorer` class to categorize leads.
3. [ ] Configure `heartbeat_daemon.py` to monitor the mortgage API.

[[Mortgage_LeadGen_NH_MOC]] | [[CURRENT_TASKS]]
