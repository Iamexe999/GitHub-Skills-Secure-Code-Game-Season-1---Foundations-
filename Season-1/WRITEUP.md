# Secure Code Game — Season 1: Foundations

Season 1 showed me how code can pass normal tests while still being vulnerable to malicious input. I worked through the Python and C challenges by reviewing the code, reproducing failures, applying fixes, and checking that normal functionality still worked.

One vulnerability was an out-of-bounds write in the C account-settings code. The program checked whether an index exceeded the array size but did not reject negative indexes. An input of -7 could overwrite the administrator flag and turn a regular account into an administrator. I fixed this by enforcing both index bounds, checking integer-conversion errors, and rejecting nonexistent accounts. I also corrected the account-ID counter so each account receives one valid, consistent identifier.

Another vulnerability was SQL injection in the stock database. User input was concatenated into SQL, and a semicolon could trigger execution of an injected update. I replaced executable query construction with parameterized statements, keeping values separate from SQL instructions. I also restricted the script interfaces to supported read-only lookups. Regression tests confirm that injected input cannot change prices or remove the table.

The remaining fixes addressed payment rounding errors with Decimal arithmetic, directory traversal with canonical path containment, and weak password security with cryptographically secure randomness and salted bcrypt hashing. All five levels passed the verification runner, including additional security regressions. This exercise reinforced that security testing must check hostile inputs and actual system state, rather than relying only on successful output or normal-use tests.

**Completion evidence:** [All five Foundations levels — successful GitHub Actions run](https://github.com/Iamexe999/GitHub-Skills-Secure-Code-Game-Season-1---Foundations-/actions/runs/35631916964).
