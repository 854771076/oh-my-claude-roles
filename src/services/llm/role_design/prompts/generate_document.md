Now generate the complete role specification document in Markdown format with YAML frontmatter.

All collected information:

name: {state.name}
display_name: {state.display_name}
description: {state.description}
category: {state.category}
tags: {', '.join(state.tags)}
target_domain: {state.target_domain}
tech_stack:

{state.tech_stack}

coding_standards:

{state.coding_standards}

project_scale: {state.project_scale}
team_size: {state.team_size}
compliance_requirements: {state.compliance_requirements}

custom_content:

{state.custom_content}

Requirements:
- Start with YAML frontmatter containing name, display_name, description, category, tags, version 1.0.0
- Include all collected information (project scale, team size, compliance requirements) in the frontmatter
- Then write the full document with proper Markdown formatting following this structure:

## 一、核心技术栈与定位

All collected information about the role domain. For **technical roles**:
- Research the latest **industry-standard best practice technology stack** for this domain
- Create a comprehensive table showing: Technology / Version Requirements / Core Positioning & Usage Guidelines
- Follow the principle: "Don't reinvent the wheel - use mature, production-proven frameworks, no hand-rolled implementations"
- Strictly follow: "Only build what you can't buy" - every capability should use the best existing library/framework

## 二、核心开发铁则（最高优先级）

Enumerate the core development rules that engineers must follow for this role, following this pattern:
- **"Always async when possible"**: All I/O operations must use async/await, no blocking calls in async context
- **"Use framework don't reinvent"**: Don't write custom code when a mature framework already exists
- **"Type safety mandatory"**: Full type hints for all code, Pydantic for all data validation
- **"Testable"**: Design for testability, proper dependency injection
- **"Maintainable"**: Clear naming, clean organization, documentation

Adapt these rules to the specific role domain (e.g., for frontend roles it would emphasize component composition, state management best practices, etc.)

## 三、企业级项目目录结构

Show the recommended project directory structure with comments explaining what each directory contains, following standard conventions for this technology domain.

## 四、代码书写规范

Document naming conventions, comment standards, formatting rules, best practices. Include:
- Naming conventions for files, variables, functions, classes, constants
- Comment requirements (when to comment, what to comment)
- Formatting rules (line width, indentation, imports order)
- Prohibited practices (what you must NOT do)

## 五、核心模块开发规范

Provide specific guidelines for developing each type of module following clean architecture principles (e.g., for backend: API layer, schema layer, service layer, CRUD layer, task layer, utils layer).

## 六、测试规范

Explain testing requirements:
- Core testing principles (don't mock internal core dependencies, test in the right pyramid levels)
- Test environment specifications
- Test naming conventions
- Coverage requirements (what percentage coverage is required)

## 七、代码提交规范

Follow the Conventional Commits standard:
- Commit format
- Type description
- Scope description
- Subject requirements
- Pre-commit requirements

## 八、安全与运维规范

Security best practices:
- Configuration management
- Authentication/authorization requirements
- Input/output validation
- Sensitive data handling
- Deployment best practices (containerization, process management, monitoring)

## 九、附录

- Prohibited practices list (what must NOT be done)
- Reference documentation links

Include all collected information from the user into the appropriate sections.

Output should be ready to save directly as a finished role document:
- Must include all sections listed above
- Must follow the formatting exactly
- Do not add any extra explanations outside the document
- Output only the final Markdown document
