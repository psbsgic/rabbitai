import { JsonObject } from '@rabbitai-ui/core';

type TestWithIdType<T> = T extends string ? string : { 'data-test': string };

// Using bem standard
export const testWithId = <T extends string | JsonObject = JsonObject>(
  prefix?: string,
  idOnly = false,
) => (id?: string): TestWithIdType<T> => {
  if (!id && prefix) {
    return (idOnly ? prefix : { 'data-test': prefix }) as TestWithIdType<T>;
  }
  if (id && !prefix) {
    return (idOnly ? id : { 'data-test': id }) as TestWithIdType<T>;
  }
  if (!id && !prefix) {
    console.warn('testWithId function has missed "prefix" and "id" params');
    return (idOnly ? '' : { 'data-test': '' }) as TestWithIdType<T>;
  }
  const newId = `${prefix}__${id}`;
  return (idOnly ? newId : { 'data-test': newId }) as TestWithIdType<T>;
};
