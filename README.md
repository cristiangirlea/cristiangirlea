<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" alt="Cristian Gîrlea — Senior Platform &amp; Backend Engineer" width="1200">
</picture>

<p align="center">
  <a href="https://github.com/cristiangirlea/tidedesk"><img alt="Featured: TideDesk" src="https://img.shields.io/badge/Featured-TideDesk-0E8A8A?style=flat-square&amp;logo=rust&amp;logoColor=white"></a>
  <a href="https://github.com/cristiangirlea/php-python-ai-bridge"><img alt="Featured: PHP–Python AI Bridge" src="https://img.shields.io/badge/Featured-PHP%E2%80%93Python%20AI%20Bridge-777BB4?style=flat-square&amp;logo=php&amp;logoColor=white"></a>
  <a href="#open-source-contributions"><img alt="Public upstream pull requests" src="assets/merged-small.svg?v=34"></a>
</p>

<ul>
  <li>Building <a href="https://tidedesk.app">TideDesk</a>, remote desktop software for reaching your own Windows computers, with screen sharing, input control, and system audio streaming.</li>
  <li>Building <a href="https://github.com/cristiangirlea/php-python-ai-bridge">PHP–Python AI Bridge</a> and <a href="https://github.com/cristiangirlea/claude-sdlc-kit">claude-sdlc-kit</a>: practical AI integrations and reusable development workflows.</li>
  <li>Working across backend services, distributed systems, cloud platforms, and developer tooling. I care about clear interfaces, useful tests, and how systems behave when something fails.</li>
</ul>

<p align="center"><a href="https://cristiangirlea.ro">Portfolio &amp; CV</a> · <a href="https://www.linkedin.com/in/cristian-girlea/">LinkedIn</a> · <a href="mailto:contact@cristiangirlea.ro">Get in touch</a></p>

<h2>Built by me</h2>
<p>Projects I build and maintain, from desktop software to AI integrations and developer tools.</p>

<h3>🖥️ <a href="https://github.com/cristiangirlea/tidedesk"><code>TideDesk</code></a> · Your computers, within reach</h3>
<blockquote><p>Remote desktop for Windows with screen sharing, keyboard and mouse control, system audio streaming, and optional text clipboard sharing.</p></blockquote>
<p>
  <img alt="Rust" src="https://img.shields.io/badge/Rust-CE422B?style=flat-square&amp;logo=rust&amp;logoColor=white">
  <img alt="QUIC transport" src="https://img.shields.io/badge/Transport-QUIC-0969DA?style=flat-square">
  <img alt="Early alpha" src="https://img.shields.io/badge/Status-early%20alpha-BF8700?style=flat-square">
  <img alt="Personal-use license" src="https://img.shields.io/badge/License-personal%20use-0E8A8A?style=flat-square">
</p>
<ul>
  <li>H.264 video and Opus audio over encrypted QUIC connections, with separate streams for screen, input, and sound.</li>
  <li>Windows host and viewer in one application, plus optional clipboard sharing and configurable controls.</li>
  <li>Source-available and free for personal, non-commercial use. Currently an early alpha; other platforms are on the roadmap.</li>
</ul>
<p><a href="https://tidedesk.app">Website</a> · <a href="https://github.com/cristiangirlea/tidedesk/releases">Download for Windows</a> · <a href="https://github.com/cristiangirlea/tidedesk">Source</a></p>

<h3>🧩 <a href="https://github.com/cristiangirlea/php-python-ai-bridge"><code>PHP–Python AI Bridge</code></a></h3>
<blockquote><p>Call Python AI tasks from PHP without holding the original HTTP request open. Submit work, poll progress, receive typed results, and cancel when needed.</p></blockquote>
<p>
  <img alt="PHP 8.2–8.5" src="https://img.shields.io/badge/PHP-8.2%E2%80%938.5-777BB4?style=flat-square&amp;logo=php&amp;logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white">
  <img alt="ONNX Runtime" src="https://img.shields.io/badge/ONNX-Runtime-005CED?style=flat-square">
  <img alt="MCP tools" src="https://img.shields.io/badge/MCP-tools-6E56CF?style=flat-square">
  <img alt="MIT license" src="https://img.shields.io/badge/License-MIT-0F766E?style=flat-square">
</p>
<ul>
  <li>A framework-independent PHP client, a Python task service, and a FrankenPHP worker-mode example.</li>
  <li>Reranking, embeddings, and redaction with optional local ONNX inference; no hosted AI account required.</li>
  <li>Bounded concurrency, cancellation, crash detection, and deterministic fault tests across PHP 8.2–8.5.</li>
  <li>MCP tools expose the same task protocol. Experimental prototype with in-memory jobs; not a production job queue.</li>
</ul>
<p><a href="https://github.com/cristiangirlea/php-python-ai-bridge#try-it-with-docker">Try with Docker</a> · <a href="https://github.com/cristiangirlea/php-python-ai-bridge/blob/main/docs/integration.md">Integration guide</a></p>

<h3>🛠️ <a href="https://github.com/cristiangirlea/claude-sdlc-kit"><code>claude-sdlc-kit</code></a></h3>
<blockquote><p>A reusable software development lifecycle for coding agents: specify, plan, implement, review, verify, ship, and learn.</p></blockquote>
<p>
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-339933?style=flat-square&amp;logo=nodedotjs&amp;logoColor=white">
  <img alt="Shell" src="https://img.shields.io/badge/Shell-4EAA25?style=flat-square&amp;logo=gnubash&amp;logoColor=white">
  <img alt="PowerShell" src="https://img.shields.io/badge/PowerShell-5391FE?style=flat-square">
  <img alt="MIT license" src="https://img.shields.io/badge/License-MIT-0F766E?style=flat-square">
</p>
<ul>
  <li>Reusable skills, roles, procedures, and templates, with a review or verification gate between stages.</li>
  <li>A local Markdown issue tracker and runtime scripts built on the Node.js standard library.</li>
  <li>Generated adapters for Claude Code and Codex from one source tree. Experimental community tooling.</li>
</ul>
<p><a href="https://github.com/cristiangirlea/claude-sdlc-kit#quick-start">Quick start</a> · <a href="https://github.com/cristiangirlea/claude-sdlc-kit/blob/main/docs/WALKTHROUGH.md">Walkthrough</a></p>

<h2>Open-source contributions</h2>
<p>My public contributions span <a href="https://github.com/golang/go">Go</a> (including its network and text libraries), Canonical, Temporal, Weaviate, PrefectHQ, Mondoo, and PostHog. The table distinguishes merged changes, open work, and closed submissions that were not merged.</p>

<p align="center">
  <a href="https://github.com/golang/go/pulls?q=is%3Apr+author%3Acristiangirlea"><img alt="Go contributions" src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&amp;logo=go&amp;logoColor=white"></a>
  <a href="https://github.com/pulls?q=is%3Apr+author%3Acristiangirlea+org%3Acanonical"><img alt="Canonical contributions" src="https://img.shields.io/badge/Canonical-E95420?style=flat-square&amp;logo=ubuntu&amp;logoColor=white"></a>
  <a href="https://github.com/pulls?q=is%3Apr+author%3Acristiangirlea+org%3Atemporalio"><img alt="Temporal contributions" src="https://img.shields.io/badge/Temporal-111827?style=flat-square"></a>
  <a href="https://github.com/weaviate/weaviate-helm/pulls?q=is%3Apr+author%3Acristiangirlea"><img alt="Weaviate contributions" src="https://img.shields.io/badge/Weaviate-187D56?style=flat-square"></a>
  <a href="https://github.com/PrefectHQ/fastmcp/issues/5302"><img alt="PrefectHQ issue report" src="https://img.shields.io/badge/PrefectHQ-20232A?style=flat-square"></a>
  <a href="https://github.com/mondoohq/cnspec/pulls?q=is%3Apr+author%3Acristiangirlea"><img alt="Mondoo contributions" src="https://img.shields.io/badge/Mondoo-6E56CF?style=flat-square"></a>
  <a href="https://github.com/PostHog/posthog-go/pulls?q=is%3Apr+author%3Acristiangirlea"><img alt="PostHog contributions" src="https://img.shields.io/badge/PostHog-F54E00?style=flat-square"></a>
</p>

<!-- merged-prs:start -->
<p align="center">
  <img src="assets/submitted-prs.svg?v=34" alt="34 submitted pull requests">
  <img src="assets/merged-prs.svg?v=3" alt="3 merged pull requests">
  <img src="assets/projects.svg?v=15" alt="15 public upstream repositories">
</p>
<table>
<thead><tr><th>Project</th><th>★</th><th>Merged</th><th>Open</th><th>Closed, unmerged</th></tr></thead>
<tbody>
<tr><td><a href="https://github.com/golang/go"><code>golang/go</code></a></td><td align="right">139,054</td><td align="right"><a href="https://go-review.googlesource.com/q/%28change%3A833064%20OR%20change%3A833584%29">2</a></td><td align="right"><a href="https://go-review.googlesource.com/q/%28change%3A833564%20OR%20change%3A833565%20OR%20change%3A833724%20OR%20change%3A834124%20OR%20change%3A834144%20OR%20change%3A837365%20OR%20change%3A837366%20OR%20change%3A839745%20OR%20change%3A839746%20OR%20change%3A839785%20OR%20change%3A839786%20OR%20change%3A839885%29">12</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/docker/docs"><code>docker/docs</code></a></td><td align="right">4,660</td><td align="right">0</td><td align="right">0</td><td align="right"><a href="https://github.com/docker/docs/pulls?q=is%3Apr+is%3Aclosed+is%3Aunmerged+author%3Acristiangirlea">1</a></td></tr>
<tr><td><a href="https://github.com/canonical/cloud-init"><code>canonical/cloud-init</code></a></td><td align="right">3,823</td><td align="right">0</td><td align="right"><a href="https://github.com/canonical/cloud-init/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">2</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/golang/net"><code>golang/net</code></a></td><td align="right">3,045</td><td align="right">0</td><td align="right"><a href="https://go-review.googlesource.com/q/%28change%3A839805%29">1</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/temporalio/sdk-typescript"><code>temporalio/sdk-typescript</code></a></td><td align="right">925</td><td align="right">0</td><td align="right"><a href="https://github.com/temporalio/sdk-typescript/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/golang/text"><code>golang/text</code></a></td><td align="right">810</td><td align="right">0</td><td align="right"><a href="https://go-review.googlesource.com/q/%28change%3A839825%20OR%20change%3A839845%29">2</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/mondoohq/cnspec"><code>mondoohq/cnspec</code></a></td><td align="right">441</td><td align="right">0</td><td align="right"><a href="https://github.com/mondoohq/cnspec/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/canonical/chisel"><code>canonical/chisel</code></a></td><td align="right">427</td><td align="right">0</td><td align="right"><a href="https://github.com/canonical/chisel/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/canonical/operator"><code>canonical/operator</code></a></td><td align="right">267</td><td align="right">0</td><td align="right"><a href="https://github.com/canonical/operator/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right"><a href="https://github.com/canonical/operator/pulls?q=is%3Apr+is%3Aclosed+is%3Aunmerged+author%3Acristiangirlea">1</a></td></tr>
<tr><td><a href="https://github.com/yiisoft/yii2-framework"><code>yiisoft/yii2-framework</code></a></td><td align="right">234</td><td align="right">0</td><td align="right">0</td><td align="right"><a href="https://github.com/yiisoft/yii2-framework/pulls?q=is%3Apr+is%3Aclosed+is%3Aunmerged+author%3Acristiangirlea">2</a></td></tr>
<tr><td><a href="https://github.com/canonical/pebble"><code>canonical/pebble</code></a></td><td align="right">210</td><td align="right">0</td><td align="right"><a href="https://github.com/canonical/pebble/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/weaviate/weaviate-helm"><code>weaviate/weaviate-helm</code></a></td><td align="right">69</td><td align="right">0</td><td align="right"><a href="https://github.com/weaviate/weaviate-helm/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">3</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/PostHog/posthog-go"><code>PostHog/posthog-go</code></a></td><td align="right">55</td><td align="right"><a href="https://github.com/PostHog/posthog-go/pulls?q=is%3Apr+is%3Amerged+author%3Acristiangirlea">1</a></td><td align="right">0</td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/temporalio/terraform-provider-temporalcloud"><code>temporalio/terraform-provider-temporalcloud</code></a></td><td align="right">26</td><td align="right">0</td><td align="right"><a href="https://github.com/temporalio/terraform-provider-temporalcloud/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right">0</td></tr>
<tr><td><a href="https://github.com/canonical/traefik-k8s-operator"><code>canonical/traefik-k8s-operator</code></a></td><td align="right">17</td><td align="right">0</td><td align="right"><a href="https://github.com/canonical/traefik-k8s-operator/pulls?q=is%3Apr+is%3Aopen+author%3Acristiangirlea">1</a></td><td align="right">0</td></tr>
</tbody></table>
<p id="gerrit-merge-evidence"><strong>Merged through Go Gerrit:</strong> <a href="https://go-review.googlesource.com/c/go/+/833064">golang/go#81545</a>, <a href="https://go-review.googlesource.com/c/go/+/833584">golang/go#81562</a>. GitHub closes these imported PRs without setting its merged flag.</p>
<p><sub>Public upstream PRs authored by me. Open includes 2 drafts; closed, unmerged submissions are not counted as accepted changes. Stars belong to the upstream repositories. <a href="scripts/refresh-profile.py">Selection rules</a> · Refreshed 2026-09-27 16:48 UTC by <a href=".github/workflows/refresh.yml">GitHub Actions</a>.</sub></p>
<!-- merged-prs:end -->

<p><strong>Issue reports:</strong> <a href="https://github.com/PrefectHQ/fastmcp/issues/5302">PrefectHQ / FastMCP</a> — reported a Windows type-checking failure caused by the unavailable <code>fcntl.flock</code> API. Issue reports are separate from the PR totals above.</p>

<h2>Tech</h2>
<p align="center">
  <img alt="Go" src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&amp;logo=go&amp;logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&amp;logo=typescript&amp;logoColor=white">
  <img alt="PHP" src="https://img.shields.io/badge/PHP-777BB4?style=flat-square&amp;logo=php&amp;logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-20232A?style=flat-square&amp;logo=react&amp;logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&amp;logo=docker&amp;logoColor=white">
  <img alt="Kubernetes" src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&amp;logo=kubernetes&amp;logoColor=white">
  <img alt="AWS" src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&amp;logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&amp;logo=postgresql&amp;logoColor=white">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&amp;logo=githubactions&amp;logoColor=white">
</p>

<h2>Contributions</h2>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/snake-dark.svg">
    <img src="assets/snake-light.svg" alt="Animated snake moving through my GitHub contribution graph">
  </picture>
</p>
<p><sub>🐍 Generated daily from my GitHub contribution graph by <a href=".github/workflows/refresh.yml">GitHub Actions</a>.</sub></p>
<hr>
<p>If a project is useful to you, a star, issue, or contribution is always welcome.<br>For backend, platform, or developer-tooling work, <a href="mailto:contact@cristiangirlea.ro">let's talk</a>.</p>
