export const getFromLocalStorage = (key: string, defaultValue: any) => {
  try {
    const value = localStorage.getItem(key);
    return JSON.parse(value || 'null') || defaultValue;
  } catch {
    return defaultValue;
  }
};

export const setInLocalStorage = (key: string, value: any) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Catch in case localStorage is unavailable
  }
};
