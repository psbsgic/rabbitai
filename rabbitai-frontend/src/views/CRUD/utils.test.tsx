import {
  isNeedsPassword,
  isAlreadyExists,
  getPasswordsNeeded,
  getAlreadyExists,
  hasTerminalValidation,
} from 'src/views/CRUD/utils';

const terminalErrors = {
  errors: [
    {
      message: 'Error importing database',
      error_type: 'GENERIC_COMMAND_ERROR',
      level: 'warning',
      extra: {
        'metadata.yaml': { type: ['Must be equal to Database.'] },
        issue_codes: [
          {
            code: 1010,
            message:
              'Issue 1010 - Superset encountered an error while running a command.',
          },
        ],
      },
    },
  ],
};

const overwriteNeededErrors = {
  errors: [
    {
      message: 'Error importing database',
      error_type: 'GENERIC_COMMAND_ERROR',
      level: 'warning',
      extra: {
        'databases/imported_database.yaml':
          'Database already exists and `overwrite=true` was not passed',
        issue_codes: [
          {
            code: 1010,
            message:
              'Issue 1010 - Superset encountered an error while running a command.',
          },
        ],
      },
    },
  ],
};

const passwordNeededErrors = {
  errors: [
    {
      message: 'Error importing database',
      error_type: 'GENERIC_COMMAND_ERROR',
      level: 'warning',
      extra: {
        'databases/imported_database.yaml': {
          _schema: ['Must provide a password for the database'],
        },
        issue_codes: [
          {
            code: 1010,
            message:
              'Issue 1010 - Superset encountered an error while running a command.',
          },
        ],
      },
    },
  ],
};

test('identifies error payloads indicating that password is needed', () => {
  let needsPassword;

  needsPassword = isNeedsPassword({
    _schema: ['Must provide a password for the database'],
  });
  expect(needsPassword).toBe(true);

  needsPassword = isNeedsPassword(
    'Database already exists and `overwrite=true` was not passed',
  );
  expect(needsPassword).toBe(false);

  needsPassword = isNeedsPassword({ type: ['Must be equal to Database.'] });
  expect(needsPassword).toBe(false);
});

test('identifies error payloads indicating that overwrite confirmation is needed', () => {
  let alreadyExists;

  alreadyExists = isAlreadyExists(
    'Database already exists and `overwrite=true` was not passed',
  );
  expect(alreadyExists).toBe(true);

  alreadyExists = isAlreadyExists({
    _schema: ['Must provide a password for the database'],
  });
  expect(alreadyExists).toBe(false);

  alreadyExists = isAlreadyExists({ type: ['Must be equal to Database.'] });
  expect(alreadyExists).toBe(false);
});

test('extracts DB configuration files that need passwords', () => {
  const passwordsNeeded = getPasswordsNeeded(passwordNeededErrors.errors);
  expect(passwordsNeeded).toEqual(['databases/imported_database.yaml']);
});

test('extracts files that need overwrite confirmation', () => {
  const alreadyExists = getAlreadyExists(overwriteNeededErrors.errors);
  expect(alreadyExists).toEqual(['databases/imported_database.yaml']);
});

test('detects if the error message is terminal or if it requires uses intervention', () => {
  let isTerminal;

  isTerminal = hasTerminalValidation(terminalErrors.errors);
  expect(isTerminal).toBe(true);

  isTerminal = hasTerminalValidation(overwriteNeededErrors.errors);
  expect(isTerminal).toBe(false);

  isTerminal = hasTerminalValidation(passwordNeededErrors.errors);
  expect(isTerminal).toBe(false);
});
