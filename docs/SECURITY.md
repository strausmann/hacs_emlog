# Security Status

## NPM Audit Vulnerabilities

### Current Status

- **6 low-severity vulnerabilities** found in development dependencies
- **0 vulnerabilities** in runtime/production code

### Vulnerability Details

#### tmp Package Vulnerability (GHSA-52f5-9888-hmc6)

- **Severity:** Low
- **Type:** Arbitrary temporary file/directory write via symbolic link
- **Affected:** `tmp@<=0.2.3`
- **Chain:** `tmp` → `external-editor` → `inquirer@8.x` → `commitizen@4.3.1`
- **Impact:** Development/build environment only (not in production)
- **Status:** No fix available from upstream (commitizen still depends on inquirer 8.x)

### Why Not Critical

1. **Dev-Only Dependencies:** All vulnerabilities are in `devDependencies`
   - Not bundled in production code
   - Not used by end-users
   - Only affects developer machines during builds

2. **No Production Impact:**
   - Custom component code (`custom_components/emlog/`) has no dependencies
   - Mock server only uses Flask + standard library
   - Integration is pure Python (no npm packages)

3. **Isolated Environment:**
   - Builds run in GitHub Actions isolated containers
   - Developer machines use local node_modules
   - No exposure to package download attacks

### Remediation Plan

#### Short Term

- ✅ Enabled Dependabot for automatic updates
- ✅ Added `.npmrc` configuration for audit reporting
- ✅ Created security documentation

#### Medium Term

- Monitor for `commitizen@5.x` release (removes this dependency chain)
- Update once available
- Consider alternatives: `cz-cli` or native git hooks

#### Long Term

- Evaluate moving to simpler commit tools
- Consider GitHub Actions native semantic versioning
- Reduce dev dependency footprint

### Monitoring

Dependabot is configured to:

- ✅ Check weekly for updates
- ✅ Auto-create PRs for security fixes
- ✅ Alert on new vulnerabilities
- ✅ Track npm, pip, and GitHub Actions

### References

- [npm audit report](../../security/dependabot)
- [GHSA-52f5-9888-hmc6](https://github.com/advisories/GHSA-52f5-9888-hmc6)
- [commitizen issues](https://github.com/commitizen/cz-cli/issues)

---

**Last Updated:** 2026-01-14  
**Next Review:** Weekly (via Dependabot)
