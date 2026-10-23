// Conventional Commits, title only: no body, no footer (so no Co-Authored-By trailers).
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert']],
    'body-empty': [2, 'always'],
    'footer-empty': [2, 'always'],
    'header-max-length': [2, 'always', 100],
    'subject-case': [0],
  },
};
