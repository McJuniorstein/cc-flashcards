# Draft cards — Final light batch (2026-05-19)

Staging file for review. Each card is a JSON block; once approved they'll be split
into individual files under `cards/cc-*.json` and verified.

**Sources used in this batch (all already in /sources/, no new additions):**
- `CNSSI 4009` — `sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c`
- `NIST SP 800-53 Rev 5` (post-DAC-fix) — `sha256:44a04031e41bb2e32fe3b8b94a2b915b0d40c8fb1f2d803e464f3c383b375d5a`

**Counts:** 9 cards (8 verbatim + 1 paraphrased). All `status: "draft"`.

**Selection rationale (vs the wishlist):**
- **D3 (2):** Access Enforcement (the core "what does access control actually do" concept), Identification (process counterpart to Identifier which we already have).
- **D4 (2):** Internal/External Network from 800-53r5 glossary — small but plugs the "what's a private network vs public network" gap without needing new sources. Did not add SP 800-125B for a 1-card VLAN entry; the cost-to-coverage ratio wasn't worth it.
- **D5 (5):** Three Audit cards (Log, Record, Trail) — AU family bedrock. Plus Vulnerability Assessment and Continuous Monitoring (SI/RA territory).

---

## Domain 3 — Access Controls (2 cards)

### cc-88122c47 — Access Enforcement

```json
{
  "id": "cc-88122c47",
  "front": "Access Enforcement",
  "back": "Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.",
  "source_doc": "NIST SP 800-53 Rev 5",
  "source_section": "AC-3",
  "source_chain": [],
  "source_excerpt": "Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.",
  "source_hash": "sha256:44a04031e41bb2e32fe3b8b94a2b915b0d40c8fb1f2d803e464f3c383b375d5a",
  "answer_type": "verbatim",
  "primary_domain": 3,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

### cc-8e325674 — Identification

```json
{
  "id": "cc-8e325674",
  "front": "Identification",
  "back": "The process of discovering the true identity (i.e., origin, initial history) of a person or item from the entire collection of similar persons or items.",
  "source_doc": "CNSSI 4009",
  "source_section": "Terms and Definitions",
  "source_chain": ["FIPS PUB 201-1"],
  "source_excerpt": "The process of discovering the true identity (i.e., origin, initial history) of a person or item from the entire collection of similar persons or items.",
  "source_hash": "sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c",
  "answer_type": "verbatim",
  "primary_domain": 3,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

---

## Domain 4 — Network Security (2 cards)

### cc-935c5152 — Internal Network  *(paraphrased — shortened)*

```json
{
  "id": "cc-935c5152",
  "front": "Internal Network",
  "back": "A network where the establishment, maintenance, and provisioning of security controls are under the direct control of organizational employees or contractors. Typically organization-owned, though it may be organization-controlled without being organization-owned.",
  "source_doc": "NIST SP 800-53 Rev 5",
  "source_section": "Appendix A",
  "source_chain": [],
  "source_excerpt": "A network where the establishment, maintenance, and provisioning of security controls are under the direct control of organizational employees or contractors. Cryptographic encapsulation or similar security technology implemented between organization-controlled endpoints provides the same effect (at least regarding confidentiality and integrity). An internal network is typically organization-owned yet may be organization-controlled while not being organization-owned.",
  "source_hash": "sha256:44a04031e41bb2e32fe3b8b94a2b915b0d40c8fb1f2d803e464f3c383b375d5a",
  "answer_type": "paraphrased",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

### cc-8a1d929c — External Network

```json
{
  "id": "cc-8a1d929c",
  "front": "External Network",
  "back": "A network not controlled by the organization.",
  "source_doc": "NIST SP 800-53 Rev 5",
  "source_section": "Appendix A",
  "source_chain": [],
  "source_excerpt": "A network not controlled by the organization.",
  "source_hash": "sha256:44a04031e41bb2e32fe3b8b94a2b915b0d40c8fb1f2d803e464f3c383b375d5a",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

---

## Domain 5 — Security Operations (5 cards)

### cc-02e96731 — Audit Log

```json
{
  "id": "cc-02e96731",
  "front": "Audit Log",
  "back": "A chronological record of system activities. Includes records of system accesses and operations performed in a given period.",
  "source_doc": "CNSSI 4009",
  "source_section": "Terms and Definitions",
  "source_chain": ["NIST SP 800-53 Rev 4"],
  "source_excerpt": "A chronological record of system activities. Includes records of system accesses and operations performed in a given period.",
  "source_hash": "sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c",
  "answer_type": "verbatim",
  "primary_domain": 5,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

### cc-8890f36a — Audit Record

```json
{
  "id": "cc-8890f36a",
  "front": "Audit Record",
  "back": "An individual entry in an audit log related to an audited event.",
  "source_doc": "CNSSI 4009",
  "source_section": "Terms and Definitions",
  "source_chain": ["NIST SP 800-53 Rev 4"],
  "source_excerpt": "An individual entry in an audit log related to an audited event.",
  "source_hash": "sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c",
  "answer_type": "verbatim",
  "primary_domain": 5,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

### cc-515cb541 — Audit Trail

```json
{
  "id": "cc-515cb541",
  "front": "Audit Trail",
  "back": "A chronological record that reconstructs and examines the sequence of activities surrounding or leading to a specific operation, procedure, or event in a security relevant transaction from inception to final result.",
  "source_doc": "CNSSI 4009",
  "source_section": "Terms and Definitions",
  "source_chain": ["NIST SP 800-47"],
  "source_excerpt": "A chronological record that reconstructs and examines the sequence of activities surrounding or leading to a specific operation, procedure, or event in a security relevant transaction from inception to final result.",
  "source_hash": "sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c",
  "answer_type": "verbatim",
  "primary_domain": 5,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

### cc-48c5e322 — Vulnerability Assessment

```json
{
  "id": "cc-48c5e322",
  "front": "Vulnerability Assessment",
  "back": "Systematic examination of an information system or product to determine the adequacy of security measures, identify security deficiencies, provide data from which to predict the effectiveness of proposed security measures, and confirm the adequacy of such measures after implementation.",
  "source_doc": "CNSSI 4009",
  "source_section": "Terms and Definitions",
  "source_chain": [],
  "source_excerpt": "Systematic examination of an information system or product to determine the adequacy of security measures, identify security deficiencies, provide data from which to predict the effectiveness of proposed security measures, and confirm the adequacy of such measures after implementation.",
  "source_hash": "sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c",
  "answer_type": "verbatim",
  "primary_domain": 5,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

### cc-55138823 — Continuous Monitoring

```json
{
  "id": "cc-55138823",
  "front": "Continuous Monitoring",
  "back": "Maintaining ongoing awareness to support organizational risk decisions.",
  "source_doc": "CNSSI 4009",
  "source_section": "Terms and Definitions",
  "source_chain": ["NIST SP 800-137"],
  "source_excerpt": "Maintaining ongoing awareness to support organizational risk decisions.",
  "source_hash": "sha256:666c24d645010d5cae0bb2f9da0c7e1d6d26cdb5e842d216526168209267464c",
  "answer_type": "verbatim",
  "primary_domain": 5,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-19T00:00:00Z",
  "modified_at": null
}
```

---

## Coverage after this batch (projected)

| Domain | Pre-batch | This batch | Post-batch | Exam % | Deck % |
|---|---|---|---|---|---|
| D1 Security Principles | 25 | 0 | 25 | 26% | 22% |
| D2 BC/DR/IR | 13 | 0 | 13 | 10% | 11% |
| D3 Access Controls | 19 | +2 | 21 | 22% | 18% |
| D4 Network Security | 33 | +2 | 35 | 24% | 30% |
| D5 Security Operations | 17 | +5 | 22 | 18% | 19% |
| **Total** | **107** | **+9** | **116** | — | — |

**Lands in the target range (110-130 cards).** D3 remains slightly under exam weight (-4 points); D4 still over by 6. The remaining D3 gap could be closed with a 4-5 card follow-on (Identification was the last clean D3 add I could find from existing sources without doing narrative paraphrases).
