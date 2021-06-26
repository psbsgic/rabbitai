

export function getNestedValue(obj, id, separator = '.') {
  /*
   * Given a nested object and an id, return the nested value.
   *
   * > getNestedValue({a:{b:1}}, 'a.b')
   * < 1
   */
  const index = id.indexOf(separator);
  if (index === -1) {
    return obj[id];
  }
  const name = id.slice(0, index);
  const rest = id.slice(index + separator.length);
  return getNestedValue(obj[name], rest, separator);
}

export function interpolate(str, obj) {
  /*
   * Programmatic template string for interpolation.
   *
   * > interpolate('foo ${a.b}', {a:{b:1}})
   * < "foo 1"
   */
  return str.replace(/\$\{(.+?)\}/g, (match, id) => getNestedValue(obj, id));
}
