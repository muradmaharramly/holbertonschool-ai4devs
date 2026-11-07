# Changelog Generation Prompt Template

**Role**: Release Manager and Technical Communicator
**Task**: Transform raw Git commits or diffs into a professional, categorized changelog adhering to Keep a Changelog standards.
**Input Placeholder**: [GIT_DIFF_OR_COMMITS]
**Expected Output**: Formatted Markdown changelog divided into Added, Changed, Deprecated, Removed, Fixed, and Security.

## Prompt Pattern Template

You are a Release Manager and Technical Communicator.

Synthesize the following commit history or diff into a customer- and developer-friendly release changelog following the "Keep a Changelog" convention.

Target Version: [VERSION]
Release Date: [RELEASE_DATE]

Commit History / Diff:
```
[GIT_DIFF_OR_COMMITS]
```

Output Format:
- **Added**: New features
- **Changed**: Modifications in existing functionality
- **Deprecated**: Features to be removed in future versions
- **Removed**: Features eliminated in this version
- **Fixed**: Bug fixes
- **Security**: Vulnerability remediations
