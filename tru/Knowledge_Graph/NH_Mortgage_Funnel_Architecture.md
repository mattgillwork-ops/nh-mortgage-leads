---
status: Verified
agent: Vera (QA) / System Synthesis
date: 2026-05-18
---
# NH Mortgage Funnel Architecture
**STATUS**: IMMUTABLE KNOWLEDGE

## Overview
The NH Mortgage Lead Gen ecosystem consists of three distinct, sovereign layers designed to capture, educate, and convert traffic into leads.

### 1. Top of Funnel: The List / The Review
- **Repository**: `nh-financial-review/`
- **Purpose**: A formal, news-oriented listicle site designed for middle-of-funnel traffic capture.
- **Components**: Top 10 Best Mortgage Lenders list, curated reviews, and localized NH badges. Routes traffic via affiliate links to the engine.

### 2. Middle of Funnel: The Blog
- **Repository**: `mortgage-app/src/app/guides/`
- **Purpose**: High-value Market Intelligence guides.
- **Components**: Educational deep-dives (e.g., NH First-Time Homebuyer Guide, Manchester Trends) designed to build authority and seamlessly transition users to the rate calculator.

### 3. Bottom of Funnel: The Engine / The Funnel
- **Repository**: `mortgage-app/src/app/funnel/` & `NH_Mortgage_Standalone/`
- **Purpose**: The 6-step lead capture engine.
- **Components**: Captures timeline, financials, and contact info to generate a custom NH ROI quote ("Wealth Report"). 

## Navigation Protocol
Agents must reference this topology when asked to scale, audit, or modify the "NH Mortgage Lead" ecosystem. Each layer is structurally isolated to prevent context bleed.
