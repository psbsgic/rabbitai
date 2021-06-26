
import { getSimpleSQLExpression } from '.';

const params = {
  subject: 'subject',
  operator: 'operator',
  comparator: 'comparator',
};

test('Should return "" if subject is falsy', () => {
  expect(getSimpleSQLExpression('', params.operator, params.comparator)).toBe(
    '',
  );
  expect(getSimpleSQLExpression(null, params.operator, params.comparator)).toBe(
    '',
  );
  expect(
    getSimpleSQLExpression(undefined, params.operator, params.comparator),
  ).toBe('');
});

test('Should return subject if operator is falsy', () => {
  expect(getSimpleSQLExpression(params.subject, '', params.comparator)).toBe(
    params.subject,
  );
  expect(getSimpleSQLExpression(params.subject, null, params.comparator)).toBe(
    params.subject,
  );
  expect(
    getSimpleSQLExpression(params.subject, undefined, params.comparator),
  ).toBe(params.subject);
});

test('Should return correct string when subject and operator are valid values', () => {
  expect(
    getSimpleSQLExpression(params.subject, params.operator, params.comparator),
  ).toBe("subject operator 'comparator'");

  expect(
    getSimpleSQLExpression(params.subject, params.operator, [
      params.comparator,
      'comparator-2',
    ]),
  ).toBe("subject operator 'comparator', 'comparator-2'");
});
