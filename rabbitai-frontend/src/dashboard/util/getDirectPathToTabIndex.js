export default function getDirectPathToTabIndex(tabsComponent, tabIndex) {
  const directPathToFilter = (tabsComponent.parents || []).slice();
  directPathToFilter.push(tabsComponent.id);
  directPathToFilter.push(tabsComponent.children[tabIndex]);

  return directPathToFilter;
}
