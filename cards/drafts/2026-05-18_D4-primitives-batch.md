# Draft cards — D4 primitives batch (2026-05-18, part 3)

Staging file for review. Each card is a JSON block; once approved they'll be split
into individual files under `cards/cc-*.json` and verified.

**Sources used in this batch (all newly added this session):**
- `IETF RFC 4949` (Internet Security Glossary v2, August 2007) — `sha256:7b42adb9c4c8a15aca42d338ec92edae59151004db21510f88e609fea9e53807`
- `NIST SP 800-94` (Guide to IDPS, 2007) — `sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536`
- `NIST SP 800-41 Rev 1` (Guidelines on Firewalls and Firewall Policy, September 2009) — `sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009`

**Counts:** 16 cards (14 verbatim + 2 paraphrased — Datagram and UDP shortened from RFC 4949 entries). All `status: "draft"`.

**Provenance note:** RFC 4949 entries are prefixed with `(I)` (Internet community consensus) — dropped from `source_excerpt` per the same convention used elsewhere (markup, not semantic content). `source_chain` populated where the parent doc explicitly attributes the definition to another publication.

---

## Coverage truth-up — what this batch does NOT close

The wishlist included **Frame, Port (well-known/registered/dynamic), IPv4, IPv6, ARP, VLAN, Network Segmentation**. After surveying all three new sources, **none define those as standalone glossary entries**. Network Segmentation doesn't appear in 800-41r1's narrative either.

Of 8 listed primitives, only **Packet and Datagram** are unblocked. Remaining 6 would need additional sources (RFC 826 for ARP, RFC 8200 for IPv6, IEEE 802.1Q or NIST SP 800-125B for VLAN, etc.).

What the batch DOES deliver: rich D4 depth content (firewall taxonomies, IDPS subtypes, NAT, packet filter vs stateful inspection, anomaly-based vs signature-based detection, false positives/negatives). High-yield exam content despite not matching the "primitives" wishlist line-for-line.

---

## RFC 4949 — Internet Security Glossary (3 cards)

### cc-371fd159 — Packet

```json
{
  "id": "cc-371fd159",
  "front": "Packet",
  "back": "A block of data that is carried from a source to a destination through a communication channel or, more generally, across a network.",
  "source_doc": "IETF RFC 4949",
  "source_section": "Glossary",
  "source_chain": [],
  "source_excerpt": "A block of data that is carried from a source to a destination through a communication channel or, more generally, across a network.",
  "source_hash": "sha256:7b42adb9c4c8a15aca42d338ec92edae59151004db21510f88e609fea9e53807",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-6490e74e — Datagram  *(paraphrased — bracket-inserts dropped)*

```json
{
  "id": "cc-6490e74e",
  "front": "Datagram",
  "back": "A self-contained, independent entity of data carrying sufficient information to be routed from the source to the destination computer without reliance on earlier exchanges between this source and destination computer and the transporting network.",
  "source_doc": "IETF RFC 4949",
  "source_section": "Glossary",
  "source_chain": ["IETF RFC 1983"],
  "source_excerpt": "A self-contained, independent entity of data [i.e., a packet] carrying sufficient information to be routed from the source [computer] to the destination computer without reliance on earlier exchanges between this source and destination computer and the transporting network.",
  "source_hash": "sha256:7b42adb9c4c8a15aca42d338ec92edae59151004db21510f88e609fea9e53807",
  "answer_type": "paraphrased",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-55fd406b — User Datagram Protocol (UDP)  *(paraphrased — RFC ref dropped)*

```json
{
  "id": "cc-55fd406b",
  "front": "User Datagram Protocol (UDP)",
  "back": "An Internet Standard, Transport-Layer protocol that delivers a sequence of datagrams from one computer to another in a computer network.",
  "source_doc": "IETF RFC 4949",
  "source_section": "Glossary",
  "source_chain": ["IETF RFC 768"],
  "source_excerpt": "An Internet Standard, Transport-Layer protocol (RFC 768) that delivers a sequence of datagrams from one computer to another in a computer network.",
  "source_hash": "sha256:7b42adb9c4c8a15aca42d338ec92edae59151004db21510f88e609fea9e53807",
  "answer_type": "paraphrased",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

---

## NIST SP 800-94 — IDPS depth (6 cards)

### cc-8e0b97cd — Anomaly-Based Detection

```json
{
  "id": "cc-8e0b97cd",
  "front": "Anomaly-Based Detection",
  "back": "The process of comparing definitions of what activity is considered normal against observed events to identify significant deviations.",
  "source_doc": "NIST SP 800-94",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "The process of comparing definitions of what activity is considered normal against observed events to identify significant deviations.",
  "source_hash": "sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-41a2f79a — Signature-Based Detection

```json
{
  "id": "cc-41a2f79a",
  "front": "Signature-Based Detection",
  "back": "The process of comparing signatures against observed events to identify possible incidents.",
  "source_doc": "NIST SP 800-94",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "The process of comparing signatures against observed events to identify possible incidents.",
  "source_hash": "sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-eafb4c60 — False Positive

```json
{
  "id": "cc-eafb4c60",
  "front": "False Positive",
  "back": "An instance in which an intrusion detection and prevention technology incorrectly identifies benign activity as being malicious.",
  "source_doc": "NIST SP 800-94",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "An instance in which an intrusion detection and prevention technology incorrectly identifies benign activity as being malicious.",
  "source_hash": "sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-f21f14ad — False Negative

```json
{
  "id": "cc-f21f14ad",
  "front": "False Negative",
  "back": "An instance in which an intrusion detection and prevention technology fails to identify malicious activity as being such.",
  "source_doc": "NIST SP 800-94",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "An instance in which an intrusion detection and prevention technology fails to identify malicious activity as being such.",
  "source_hash": "sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-5a865288 — Host-Based Intrusion Detection and Prevention System (HIDS/HIPS)

```json
{
  "id": "cc-5a865288",
  "front": "Host-Based Intrusion Detection and Prevention System (HIDS/HIPS)",
  "back": "A program that monitors the characteristics of a single host and the events occurring within that host to identify and stop suspicious activity.",
  "source_doc": "NIST SP 800-94",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "A program that monitors the characteristics of a single host and the events occurring within that host to identify and stop suspicious activity.",
  "source_hash": "sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-a9e3dfcc — Network-Based Intrusion Detection and Prevention System (NIDS/NIPS)

```json
{
  "id": "cc-a9e3dfcc",
  "front": "Network-Based Intrusion Detection and Prevention System (NIDS/NIPS)",
  "back": "An intrusion detection and prevention system that monitors network traffic for particular network segments or devices and analyzes the network and application protocol activity to identify and stop suspicious activity.",
  "source_doc": "NIST SP 800-94",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "An intrusion detection and prevention system that monitors network traffic for particular network segments or devices and analyzes the network and application protocol activity to identify and stop suspicious activity.",
  "source_hash": "sha256:4562ebbad30430d7ecd9aca78c165a23fbddedcb14698ad0fe46629f8cabd536",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

---

## NIST SP 800-41 Rev 1 — Firewall depth (7 cards)

### cc-2ca8a8e6 — Packet Filter

```json
{
  "id": "cc-2ca8a8e6",
  "front": "Packet Filter",
  "back": "A routing device that provides access control functionality for host addresses and communication sessions.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "A routing device that provides access control functionality for host addresses and communication sessions.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-c0b539d5 — Stateful Inspection

```json
{
  "id": "cc-c0b539d5",
  "front": "Stateful Inspection",
  "back": "Packet filtering that also tracks the state of connections and blocks packets that deviate from the expected state.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "Packet filtering that also tracks the state of connections and blocks packets that deviate from the expected state.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-f31c9d45 — Network Address Translation (NAT)

```json
{
  "id": "cc-f31c9d45",
  "front": "Network Address Translation (NAT)",
  "back": "A routing technology used by many firewalls to hide internal system addresses from an external network through use of an addressing schema.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "A routing technology used by many firewalls to hide internal system addresses from an external network through use of an addressing schema.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-3d9274a7 — Application-Proxy Gateway

```json
{
  "id": "cc-3d9274a7",
  "front": "Application-Proxy Gateway",
  "back": "A firewall capability that combines lower-layer access control with upper layer-functionality, and includes a proxy agent that acts as an intermediary between two hosts that wish to communicate with each other.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "A firewall capability that combines lower-layer access control with upper layer-functionality, and includes a proxy agent that acts as an intermediary between two hosts that wish to communicate with each other.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-ab9dad6c — Egress Filtering

```json
{
  "id": "cc-ab9dad6c",
  "front": "Egress Filtering",
  "back": "Filtering of outgoing network traffic.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "Filtering of outgoing network traffic.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-3f81e956 — Ingress Filtering

```json
{
  "id": "cc-3f81e956",
  "front": "Ingress Filtering",
  "back": "Filtering of incoming network traffic.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "Filtering of incoming network traffic.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

### cc-26214b0a — Deny by Default

```json
{
  "id": "cc-26214b0a",
  "front": "Deny by Default",
  "back": "To block all inbound and outbound traffic that has not been expressly permitted by firewall policy.",
  "source_doc": "NIST SP 800-41 Rev 1",
  "source_section": "Appendix A — Glossary",
  "source_chain": [],
  "source_excerpt": "To block all inbound and outbound traffic that has not been expressly permitted by firewall policy.",
  "source_hash": "sha256:46fc63d54d9fb5275e6f94ec043203abbc8281d2cd46e704e0dada71c5fae009",
  "answer_type": "verbatim",
  "primary_domain": 4,
  "secondary_domains": [],
  "status": "draft",
  "created_at": "2026-05-18T00:00:00Z",
  "modified_at": null
}
```

---

## Coverage after this batch (projected)

| Domain | Pre-batch | This batch | Post-batch | Exam % | Deck % |
|---|---|---|---|---|---|
| D1 Security Principles | 25 | 0 | 25 | 26% | 23% |
| D2 BC/DR/IR | 13 | 0 | 13 | 10% | 12% |
| D3 Access Controls | 19 | 0 | 19 | 22% | 18% |
| D4 Network Security | 17 | +16 | 33 | 24% | 31% |
| D5 Security Operations | 17 | 0 | 17 | 18% | 16% |
| **Total** | **91** | **+16** | **107** | — | — |

**D4 over-correction note:** post-batch D4 jumps to 31% of deck vs 24% exam weight. That's the inverse of being severely under. Future batches should skew D1, D3, or D5 to rebalance — or accept that D4 is now "well-supported" given how thin it was.
