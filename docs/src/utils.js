

/* eslint no-undef: "error" */
const getPathName = (path) => path.replace(/[/]+/g, '');

export const getCurrentPath = () => (typeof window !== 'undefined' ? getPathName(window.location.pathname) : '');
// get active menus
export const getActiveMenuItem = (items) => {
  let selectedKey;
  let openKey;
  let headings = [];
  const path = getCurrentPath();
  items.forEach(
    ({
      menu, id: itemId, route: itemRoute, headings: itemHeadings,
    }) => {
      if (menu) {
        menu.forEach(({ id: menuId, route, headings: subHeadings }) => {
          if (getPathName(route) === path) {
            selectedKey = menuId;
            openKey = itemId;
            headings = subHeadings;
          }
        });
      } else if (itemRoute) {
        if (getPathName(itemRoute) === path) {
          selectedKey = itemId;
          openKey = itemId;
          headings = itemHeadings;
        }
      }
    },
  );
  return { openKey, selectedKey, headings };
};

// TODO implement versioned dox?
/* const getVersionedDocs = (v, menus) => {
   //menus.filter(doc =>
  const stack = [...menus];
  while(stack.length > 0) {
    let temp = stack.shift();
    if (Array.isArray(temp.menu)){

    } else newlist.push(temp);
  }
} */

// flattens ordered menu
const listOrderedMenu = (menus) => {
  const newlist = [];
  const stack = [...menus];
  while (stack.length > 0) {
    const temp = stack.shift();
    if (Array.isArray(temp.menu)) {
      const sortedMenu = temp.menu.sort((a, b) => a.index - b.index);
      stack.unshift(...sortedMenu);
    } else newlist.push(temp);
  }
  return newlist;
};

// functionality for prev and next button
export const getPreviousAndNextUrls = (menus) => {
  const items = listOrderedMenu(menus);
  let prevUrl;
  let nextUrl;
  const path = getCurrentPath();

  items.forEach(({ route }, index) => {
    if (getPathName(route) === path) {
      if (items[index - 1]) {
        prevUrl = items[index - 1].route;
      }
      if (items[index + 1]) {
        nextUrl = items[index + 1].route;
      }
    }
  });

  return [prevUrl, nextUrl];
};

export const getCurrentMenu = () => {};

const breakpoints = [576, 768, 992, 1200];

export const mq = breakpoints.map((bp) => `@media (max-width: ${bp}px)`);
