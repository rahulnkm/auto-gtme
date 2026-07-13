# 05 — Repos, Skills & Platform Landscape for auto-gtme

*Researched: May 22, 2026. All star counts and URLs verified via GitHub API or live web fetch.*

---

## PART A — Existing GTM-Engineering Code & Skills on GitHub

### A.1 GTM-Specific AI Agent Skills & Toolkits

#### `chadboyda/agent-gtm-skills`
- **URL:** https://github.com/chadboyda/agent-gtm-skills
- **Stars:** 42 | **Last activity:** 2026-05-21
- **What it does:** 18 discrete AI-agent skills for go-to-market operators. Covers ICP scoring, AI-SDR deployment, enrichment waterfalls, cold email personalization, programmatic SEO, content-led GTM, advertising automation, partner ecosystem management, and n8n/Make/Zapier orchestration.
- **Reference value:** The closest existing analogue to the auto-gtme skill suite. The skill taxonomy (ICP → enrich → sequence → follow-up) directly maps to pipeline stages. Study the skill signatures and prompts; use as a vocabulary reference for naming conventions.

#### `gtm-skills/gtm`
- **URL:** https://github.com/gtm-skills/gtm
- **Stars:** 55 | **Last activity:** 2026-05-22 (active today)
- **What it does:** GTM toolkit for AI agents covering research, intel, outreach, and CRM operations. Likely the most actively maintained pure-GTM agent toolkit at time of writing.
- **Reference value:** High. Actively maintained, covers the full GTM surface. Inspect for any Claude Code skill format compatibility.

#### `orchidautomation/kiln-plugins`
- **URL:** https://github.com/orchidautomation/kiln-plugins
- **Stars:** 0 | **Last activity:** 2026-01-02
- **What it does:** GTM engineering automation plugins for Claude Code. Stale but demonstrates the pattern of packaging GTM logic as Claude Code plugins.
- **Reference value:** Low on code; moderate as a structural template showing how to wire GTM logic into Claude Code's plugin format.

#### `composio-community/awesome-gtm-skills`
- **URL:** https://github.com/composio-community/awesome-gtm-skills
- **Stars:** 1 | **Last activity:** 2026-04-21
- **What it does:** Curated list of GTM skills for AI agents via Composio's tool-calling layer. Sparse, but points toward Composio's managed API-connection approach as an alternative to raw MCP.
- **Reference value:** Low for direct reuse; useful for discovering Composio-hosted integrations (Apollo, HubSpot, Clay) that can back-fill where no MCP server exists.

### A.2 Awesome Lists & Directories

#### `marketinguys/awesome-gtm-engineering`
- **URL:** https://github.com/marketinguys/awesome-gtm-engineering
- **Stars:** 93 | **Last activity:** 2026-05-19
- **What it does:** Curated list of tools, libraries, frameworks, and resources for GTM engineering — automation, attribution, analytics, and experimentation.
- **Reference value:** Best single discovery resource for the broader ecosystem. Use to identify tools missing from the auto-gtme radar.

#### `eliasstravik/awesome-gtm-engineering`
- **URL:** https://github.com/eliasstravik/awesome-gtm-engineering
- **Stars:** 0 | **Last activity:** 2026-05-14
- **What it does:** A competing curated list of GTM engineering resources. Less developed.
- **Reference value:** Low; defer to marketinguys version.

### A.3 MCP Servers for GTM Platforms

#### Clay — Official
- **URL:** https://github.com/clay-inc/clay-mcp
- **Stars:** 31 | **Last activity:** 2026-05-14
- **What it does:** Official Clay MCP server (by `clay-inc`). Enables contact search by title/company/location, interaction search, stats, detailed contact retrieval by ID, adding contacts, and creating notes. Also available as a remote server at `https://mcp.clay.earth/mcp`.
- **Reference value:** Critical. Clay is the enrichment hub in the recommended stack; this MCP is the primary integration path.

#### HubSpot — Community (baryhuang)
- **URL:** https://github.com/baryhuang/mcp-hubspot
- **Stars:** 123 | **Last activity:** 2026-05-20
- **What it does:** MCP server for HubSpot CRM with built-in vector storage and caching to overcome HubSpot API pagination limits. Covers contacts, companies, deals.
- **Reference value:** High. Best-starred HubSpot MCP; use as default if the user's CRM is HubSpot.

#### HubSpot — Community (zekker6, Go binary)
- **URL:** https://github.com/zekker6/mcp-hubspot-go
- **Stars:** 2 | **Last activity:** 2026-05-19
- **What it does:** Single Go binary for HubSpot MCP. Supports read-only mode flag. Docker-compatible.
- **Reference value:** Moderate. Useful for self-hosted deployment; lower stars but clean implementation.

#### Attio — Community (kesslerio)
- **URL:** https://github.com/kesslerio/attio-mcp-server
- **Stars:** 68 | **Last activity:** 2026-05-20
- **What it does:** Most complete Attio MCP server. Covers Deals, Tasks, Lists, People, Companies, Records, Notes. Full CRUD surface. v2.0.0 migration to MCP naming conventions in progress.
- **Reference value:** High. Best Attio integration path for auto-gtme.

#### Attio — Community (hmk)
- **URL:** https://github.com/hmk/attio-mcp-server
- **Stars:** 15 | **Last activity:** 2026-02-16
- **What it does:** Simpler Attio MCP server; good as fallback or lightweight alternative.
- **Reference value:** Moderate.

#### Salesforce — Official (salesforcecli)
- **URL:** https://github.com/salesforcecli/mcp
- **Stars:** 409 | **Last activity:** 2026-05-22
- **What it does:** Official MCP server by Salesforce CLI team. Highest-quality CRM MCP in the ecosystem; direct Salesforce org interaction.
- **Reference value:** High for Salesforce users. Note: Salesforce also has the `sf` CLI (v2, replaces deprecated `sfdx`).

#### Notion — Official (makenotion)
- **URL:** https://github.com/makenotion/notion-mcp-server
- **Stars:** 4,354 | **Last activity:** 2026-05-21
- **What it does:** Official Notion MCP server. Runs via `npx @notionhq/notion-mcp-server`. v2.0.0 migrates to Notion API 2025-09-03 with data sources abstraction. Full page/database/block CRUD.
- **Reference value:** Critical. Notion is the recommended knowledge-base layer; this is the integration path.

#### Notion — Official Claude Code Plugin (makenotion)
- **URL:** https://github.com/makenotion/claude-code-notion-plugin
- **Stars:** 388 | **Last activity:** 2026-05-22
- **What it does:** First-party Claude Code plugin by Notion team. Connects Claude Code directly to Notion workspace. Combines MCP with Claude Code slash commands.
- **Reference value:** Critical and unique. Only tool in this survey with an official Claude Code plugin. Directly usable as-is for knowledge-base intake.

#### Pipedrive — Community
- **URL:** https://github.com/iamsamuelfraga/mcp-pipedrive
- **Stars:** 9 | **Last activity:** 2026-05-13
- **What it does:** Most complete Pipedrive MCP (self-described). Full CRUD for deals, persons, organizations, activities, notes, leads. 36 tools, rate limiting, safety confirmations, soft delete recovery.
- **Reference value:** Moderate. For Pipedrive users only.

#### Apollo.io — Community (thevgergroup)
- **URL:** https://github.com/thevgergroup/apollo-io-mcp
- **Stars:** 15 | **Last activity:** 2026-05-19
- **What it does:** MCP server for Apollo.io API — people search, company search, enrichment.
- **Reference value:** Moderate. Apollo covers both enrichment and sequencing; this MCP covers the enrichment side.

#### Apollo.io — Community (edwardchoh)
- **URL:** https://github.com/edwardchoh/apollo-io-mcp-server
- **Stars:** 13 | **Last activity:** 2026-03-18
- **What it does:** Exposes Apollo.io API functionalities as MCP tools. Older, less active.
- **Reference value:** Low; prefer thevgergroup version.

#### Close CRM — Community CLI + MCP
- **URL:** https://github.com/bcharleson/close-crm-cli
- **Stars:** 1 | **Last activity:** 2026-03-27
- **What it does:** Full-featured CLI *and* MCP server for Close CRM. 160+ commands, 30 resource groups covering the full Close API. "AI agent native." Single repo provides both CLI and MCP surfaces.
- **Reference value:** High pattern value — demonstrates the CLI+MCP dual-surface pattern that auto-gtme should adopt for its own skills.

#### HeyReach — Community MCP
- **URL:** https://github.com/bcharleson/heyreach-mcp
- **Stars:** 5 | **Last activity:** 2026-03-25
- **What it does:** MCP server for HeyReach LinkedIn automation. Same author as close-crm-cli; consistent pattern.
- **Reference value:** Moderate. HeyReach is recommended for LinkedIn sequencing.

#### Fireflies.ai — Community MCP
- **URL:** https://github.com/props-labs/fireflies-mcp
- **Stars:** 5 | **Last activity:** 2025-10-29
- **What it does:** MCP server for Fireflies.ai meeting transcripts and metadata. Fireflies also launched an official MCP server beta in June 2025 (docs at `docs.fireflies.ai/getting-started/docs-mcp-server`).
- **Reference value:** Moderate. Meeting notes layer; prefer Granola for the user's setup.

#### Granola — Community MCP
- **URL:** https://github.com/chrisguillory/granola-mcp
- **Stars:** 0 | **Last activity:** 2026-05-20
- **What it does:** MCP server for Granola AI meeting notes. Granola launched an official MCP in Feb 2026 and expanded it in March 2026 (notes in folders, shared notes). Personal API available on Business/Enterprise plans.
- **Reference value:** Critical. User already has Granola. Meeting context becomes a first-class data source for auto-gtme.

### A.4 Open-Source AI-SDR / Enrichment Frameworks

#### `N8n-automations-works/LinkedIn-Job-Scraping-Lead-Enrichment-Automation`
- **URL:** https://github.com/N8n-automations-works/LinkedIn-Job-Scraping-Lead-Enrichment-Automation
- **Stars:** N/A (private/small) | **Last activity:** 2026-04-15
- **What it does:** n8n workflow: scrapes LinkedIn jobs via Apify, enriches company and contact data, verifies emails, generates AI-driven personalized icebreakers. Represents the "n8n as orchestrator" pattern.
- **Reference value:** Moderate as a workflow pattern. Not a reusable library.

#### `dataCleaningAutomation/lead-enrichment-automation-python`
- **URL:** https://github.com/dataCleaningAutomation/lead-enrichment-automation-python
- **Stars:** N/A | **Last activity:** 2026-04-23
- **What it does:** Python pipeline integrating multiple APIs to transform raw CSV data into structured datasets. Shows multi-provider waterfall enrichment pattern in code.
- **Reference value:** Low. Not agent-native; use as API integration reference only.

---

## PART B — GTM Platform Landscape & Integration Surface

Integration cascade preference: **CLI > MCP > API**

### B.1 CRM

| Platform | Official CLI | MCP Server | Public REST API |
|---|---|---|---|
| **HubSpot** | Yes — `@hubspot/cli` v8.6.0 ([npm](https://www.npmjs.com/package/@hubspot/cli), [GitHub](https://github.com/HubSpot/hubspot-cli)); focused on CMS/theme dev, not CRM data | Community: `baryhuang/mcp-hubspot` (★123), `zekker6/mcp-hubspot-go` (★2) | Yes — [developers.hubspot.com/docs/api](https://developers.hubspot.com/docs/api) |
| **Salesforce** | Yes — official `sf` CLI v2 ([developer.salesforce.com/tools/salesforcecli](https://developer.salesforce.com/tools/salesforcecli)); replaces deprecated `sfdx` | Official: `salesforcecli/mcp` (★409) | Yes — [developer.salesforce.com/docs/atlas.en-us.api_rest.meta](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm) |
| **Attio** | Not found | Community: `kesslerio/attio-mcp-server` (★68), `hmk/attio-mcp-server` (★15) | Yes — [developers.attio.com/docs](https://developers.attio.com/docs) |
| **Pipedrive** | Not found | Community: `iamsamuelfraga/mcp-pipedrive` (★9) | Yes — [developers.pipedrive.com/docs/api](https://developers.pipedrive.com/docs/api) |
| **folk** | Not found | Not found | Yes — [developer.folk.app/api-reference/overview](https://developer.folk.app/api-reference/overview); recently launched, basic coverage |
| **Close** | Community CLI+MCP: `bcharleson/close-crm-cli` (★1, 160+ commands) | Same repo as CLI | Yes — [developer.close.com](https://developer.close.com/) |

### B.2 Enrichment / Waterfall

| Platform | Official CLI | MCP Server | Public REST API |
|---|---|---|---|
| **Clay** | Not found | Official: `clay-inc/clay-mcp` (★31); remote at `mcp.clay.earth/mcp` | Yes (Clay.com enrichment API; undocumented waterfall API; HTTP API available via integration settings) |
| **Apollo.io** | Not found | Community: `thevgergroup/apollo-io-mcp` (★15), `edwardchoh/apollo-io-mcp-server` (★13) | Yes — [docs.apollo.io](https://docs.apollo.io/) |
| **ZoomInfo** | Not found | Not found | Yes — [docs.zoominfo.com](https://docs.zoominfo.com/) (Enterprise API; gated by contract) |
| **Findymail** | Not found | Not found | Yes — REST API with find, verify, enrichment, reverse lookup endpoints; docs at findymail.com |
| **Prospeo** | Not found | Not found | Yes — [prospeo.io/s/lead-generation-api](https://prospeo.io/s/lead-generation-api); 143M+ verified emails |
| **Hunter.io** | Not found | Not found | Yes — [hunter.io/api-documentation](https://hunter.io/api-documentation) (v2) |
| **LeadMagic** | Official CLI ([leadmagic.io/blog/introducing-leadmagic-cli](https://leadmagic.io/blog/introducing-leadmagic-cli)) | Official: `LeadMagic/leadmagic-mcp` (19 tools, `npx leadmagic-mcp-server`) — [github.com/LeadMagic/leadmagic-mcp](https://github.com/LeadMagic/leadmagic-mcp) | Yes — REST, 20+ endpoints; pay-per-result; [leadmagic.io/docs/v1/reference/introduction](https://leadmagic.io/docs/v1/reference/introduction) |
| **Datagma** | Not found | Not found | Yes — [datagmaapi.readme.io](https://datagmaapi.readme.io/reference/getting-started-with-your-api); 50+ attributes; free API key at app.datagma.com |

### B.3 Sequencer / Sender

| Platform | Official CLI | MCP Server | Public REST API |
|---|---|---|---|
| **Smartlead** | Not found | Not found | Yes — [api.smartlead.ai](https://api.smartlead.ai/introduction); base `https://server.smartlead.ai/api/v1`; API key in query param |
| **Instantly** | Not found | Not found | Yes — [developer.instantly.ai](https://developer.instantly.ai/) (v2; v1 deprecated Jan 2026) |
| **lemlist** | Not found | Not found | Yes — [developer.lemlist.com](https://developer.lemlist.com/api-reference/getting-started/overview) |
| **La Growth Machine** | Not found | Community via Composio; no standalone MCP found | Yes — [documenter.getpostman.com/view/2071164/TVCmSkH2](https://documenter.getpostman.com/view/2071164/TVCmSkH2); base `https://apiv2.lagrowthmachine.com/flow` |
| **Salesforge** | Not found | Not found | Yes — `https://api.salesforge.ai/public/v2/workspaces`; API key in headers; docs sparse |
| **Apollo (sequences)** | Not found | Community: `thevgergroup/apollo-io-mcp` | Yes — same `docs.apollo.io` covers sequences |
| **Outreach** | Not found | Not found | Yes — [developers.outreach.io/api](https://developers.outreach.io/api/) |
| **Salesloft** | Not found | Not found | Yes — [developers.salesloft.com](https://developers.salesloft.com/) |

### B.4 Signals / Intent

| Platform | Official CLI | MCP Server | Public REST API |
|---|---|---|---|
| **RB2B** | Not found | Not found | Yes — [rb2b.com/apis](https://www.rb2b.com/apis); V2 Identity APIs (IP→HEM, IP→MAID, HEM enrichment); separate API account + credits required |
| **Trigify** | Not found | Not found | Yes — [help.trigify.io](https://help.trigify.io/en/articles/27-making-api-calls); LinkedIn signal detection API; key in query params |
| **Default** | Not found | Not found | No public API docs found as of May 2026 |
| **Common Room** | Not found | Not found | Yes — [api.commonroom.io/docs/community.html](https://api.commonroom.io/docs/community.html) |
| **Koala** | — | — | **SHUT DOWN Sep 2025** (acqui-hired by Cursor/Anysphere, announced July 2025 — [TechCrunch](https://techcrunch.com/2025/07/18/cursor-snaps-up-enterprise-startup-koala-in-challenge-to-github-copilot/)) |
| **Warmly** | Not found | Not found | Yes — REST API exists (apitracker.io confirms); docs partially public |

### B.5 Meeting Notes / Knowledge Base

| Platform | Official CLI | MCP Server | Public REST API |
|---|---|---|---|
| **Granola** | Not found | Official MCP launched Feb 2026; community `chrisguillory/granola-mcp` (★0); remote MCP available | Yes — Personal API (Business/Enterprise plans) and Enterprise API launched March 2026 |
| **Fireflies.ai** | Not found | Official beta MCP ([docs.fireflies.ai](https://docs.fireflies.ai/getting-started/docs-mcp-server)); community `props-labs/fireflies-mcp` (★5) | Yes — GraphQL + REST at [docs.fireflies.ai](https://docs.fireflies.ai/) |
| **Otter.ai** | Not found | Not found | Yes — Otter API exists; limited public access |
| **Notion** | Not found | Official: `makenotion/notion-mcp-server` (★4,354); Official Claude Code plugin: `makenotion/claude-code-notion-plugin` (★388) | Yes — [developers.notion.com](https://developers.notion.com/) |
| **Gong** | Not found | Community MCP referenced (Glyphic + community builds); no standalone official repo found | Yes — [api.gong.io/v2](https://help.gong.io/docs/what-the-gong-api-provides); Basic Auth or OAuth 2.0; ~1,000 req/hr |

### B.6 LinkedIn / Misc

| Platform | Official CLI | MCP Server | Public REST API |
|---|---|---|---|
| **Unipile** | Not found | Not found | Yes — [developer.unipile.com](https://developer.unipile.com/docs/getting-started); 500+ endpoints; LinkedIn, WhatsApp, Gmail, Outlook; official Node.js, Python, PHP SDKs |
| **PhantomBuster** | Not found | Not found | Yes — [hub.phantombuster.com/docs/api](https://hub.phantombuster.com/docs/api); HTTPS/JSON; API key auth |
| **HeyReach** | Not found | Community: `bcharleson/heyreach-mcp` (★5) | Yes — [documenter.getpostman.com/view/23808049/2sA2xb5F75](https://documenter.getpostman.com/view/23808049/2sA2xb5F75); 300 req/min; API key in `X-API-KEY` header; Campaign API in beta |
| **Octave (octavehq)** | Not found | Not found | Yes — [octave.readme.io/reference/about-octave-api](https://octave.readme.io/reference/about-octave-api); agentic GTM brain; API exists but docs access gated |
| **Persana.ai** | Not found | Not found | No standalone public API docs found; integrates with HubSpot/Salesforce natively; other CRMs via Zapier/Make |

---

## Recommended Platform Stack for auto-gtme

Organized by pipeline stage, with integration path per CLI > MCP > API cascade. User's existing accounts (Clay, Notion, Granola, and a CRM) are prioritized.

### Stage 1 — Intake & Knowledge Base
| Tool | Rationale | Integration Path |
|---|---|---|
| **Notion** | User has account. First-party Claude Code plugin exists (`makenotion/claude-code-notion-plugin`). Official MCP (★4,354) is the highest-quality in the entire survey. | **MCP** via `makenotion/notion-mcp-server` or the Claude Code plugin directly |
| **Granola** | User has account. Official MCP launched Feb 2026; makes meeting transcripts first-class agent context. $1.5B valuation signals long-term support. | **MCP** via Granola's official MCP (remote URL) |

### Stage 2 — CRM
| Tool | Rationale | Integration Path |
|---|---|---|
| **User's existing CRM** | If HubSpot: use `baryhuang/mcp-hubspot` (★123). If Attio: use `kesslerio/attio-mcp-server` (★68). If Salesforce: use official `salesforcecli/mcp` (★409). If Close: use `bcharleson/close-crm-cli` (CLI+MCP dual surface). | **MCP** (all four options have community or official MCP servers) |

### Stage 3 — Enrichment / Waterfall
| Tool | Rationale | Integration Path |
|---|---|---|
| **Clay** | User has account. Official MCP (`clay-inc/clay-mcp`) + remote MCP endpoint. Clay already acts as an enrichment orchestrator over 100+ providers, so routing enrichment through Clay reduces the number of direct API integrations needed. | **MCP** via `clay-inc/clay-mcp` or remote `mcp.clay.earth/mcp` |
| **Apollo.io** (secondary) | Doubles as enrichment + sequencing. MCP available. | **MCP** via `thevgergroup/apollo-io-mcp` |
| **Hunter.io** (fallback) | Clean REST API, free tier of 50 credits/mo ([hunter.io/pricing](https://hunter.io/pricing)), best for email verification in waterfall. | **API** via `hunter.io/api-documentation` |
| **Datagma** (fallback) | Free API key, 50+ attributes, good LinkedIn URL enrichment. | **API** via `datagmaapi.readme.io` |

### Stage 4 — Signals / Intent
| Tool | Rationale | Integration Path |
|---|---|---|
| **RB2B** | Best individual-level website visitor ID tool. REST API V2 available. | **API** via `rb2b.com/apis` |
| **Trigify** | LinkedIn signal detection at scale; REST API in help center. Clay integration available (enrichment pass-through). | **API** via `help.trigify.io` |
| **Common Room** | PLG signal aggregation after Koala shutdown. Core API available. | **API** via `api.commonroom.io` |

### Stage 5 — Sequencing / Sending
| Tool | Rationale | Integration Path |
|---|---|---|
| **Smartlead** (email) | Best API for cold email at scale; full campaign lifecycle. REST API well-documented. | **API** via `api.smartlead.ai` |
| **HeyReach** (LinkedIn) | LinkedIn sequencing with Campaign API beta. Community MCP exists. | **MCP** via `bcharleson/heyreach-mcp` (or **API** if MCP insufficient) |
| **Instantly** (email alt) | API v2 solid; v1 deprecated. Good for multi-inbox cold email. | **API** via `developer.instantly.ai` |

### Stage 6 — Meeting Notes (Loop-back to Intake)
| Tool | Rationale | Integration Path |
|---|---|---|
| **Granola** | Already covered in Stage 1. Meeting notes auto-feed back into Notion and CRM via agent. | **MCP** |

---

## Sources

- https://github.com/chadboyda/agent-gtm-skills
- https://github.com/gtm-skills/gtm
- https://github.com/orchidautomation/kiln-plugins
- https://github.com/marketinguys/awesome-gtm-engineering
- https://github.com/composio-community/awesome-gtm-skills
- https://github.com/eliasstravik/awesome-gtm-engineering
- https://github.com/clay-inc/clay-mcp
- https://github.com/baryhuang/mcp-hubspot
- https://github.com/zekker6/mcp-hubspot-go
- https://github.com/kesslerio/attio-mcp-server
- https://github.com/hmk/attio-mcp-server
- https://github.com/salesforcecli/mcp
- https://github.com/makenotion/notion-mcp-server
- https://github.com/makenotion/claude-code-notion-plugin
- https://github.com/iamsamuelfraga/mcp-pipedrive
- https://github.com/thevgergroup/apollo-io-mcp
- https://github.com/edwardchoh/apollo-io-mcp-server
- https://github.com/bcharleson/close-crm-cli
- https://github.com/bcharleson/heyreach-mcp
- https://github.com/props-labs/fireflies-mcp
- https://github.com/chrisguillory/granola-mcp
- https://github.com/N8n-automations-works/LinkedIn-Job-Scraping-Lead-Enrichment-Automation
- https://github.com/HubSpot/hubspot-cli
- https://www.npmjs.com/package/@hubspot/cli
- https://developer.salesforce.com/tools/salesforcecli
- https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_unified.htm
- https://developers.hubspot.com/docs/api
- https://developers.attio.com/docs
- https://developer.folk.app/api-reference/overview
- https://developer.close.com/
- https://docs.apollo.io/
- https://docs.zoominfo.com/
- https://hunter.io/api-documentation
- https://prospeo.io/s/lead-generation-api
- https://datagmaapi.readme.io/reference/getting-started-with-your-api
- https://api.smartlead.ai/introduction
- https://developer.instantly.ai/
- https://developer.lemlist.com/api-reference/getting-started/overview
- https://documenter.getpostman.com/view/2071164/TVCmSkH2
- https://developers.outreach.io/api/
- https://developers.salesloft.com/
- https://www.rb2b.com/apis
- https://help.trigify.io/en/articles/27-making-api-calls
- https://api.commonroom.io/docs/community.html
- https://developers.notion.com/
- https://docs.fireflies.ai/getting-started/docs-mcp-server
- https://help.gong.io/docs/what-the-gong-api-provides
- https://developer.unipile.com/docs/getting-started
- https://hub.phantombuster.com/docs/api
- https://documenter.getpostman.com/view/23808049/2sA2xb5F75
- https://octave.readme.io/reference/about-octave-api
- https://www.granola.ai/blog/granola-mcp
- https://techcrunch.com/2026/03/25/granola-raises-125m-hits-1-5b-valuation-as-it-expands-from-meeting-notetaker-to-enterprise-ai-app/
- https://www.salesforge.ai/integrations
- https://developers.pipedrive.com/docs/api
- https://datagma.com/api/
