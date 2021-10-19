export default function isInDifferentFilterScopes({
  dashboardFilters = {},
  source = [],
  destination = [],
}) {
  const sourceSet = new Set(source);
  const destinationSet = new Set(destination);

  const allScopes = [].concat(
    ...Object.values(dashboardFilters).map(({ scopes }) =>
      [].concat(...Object.values(scopes).map(({ scope }) => scope)),
    ),
  );
  return allScopes.some(tab => destinationSet.has(tab) !== sourceSet.has(tab));
}
