export default function serializeFilterScopes(dashboardFilters) {
  return Object.values(dashboardFilters).reduce((map, { chartId, scopes }) => {
    const scopesById = Object.keys(scopes).reduce(
      (scopesByColumn, column) => ({
        ...scopesByColumn,
        [column]: scopes[column],
      }),
      {},
    );

    return {
      ...map,
      [chartId]: scopesById,
    };
  }, {});
}
