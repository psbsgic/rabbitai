

export enum Scoping {
  all,
  specific,
}

/** UI Ant tree type */
export type TreeItem = {
  children: TreeItem[];
  key: string;
  title: string;
};
