export type Slice = {
  dttm: number;
  id: number;
  url: string;
  title: string;
  creator?: string;
  creator_url?: string;
  viz_type: string;
};

export type Activity = {
  action: string;
  item_title: string;
  item_url: string;
  time: number;
};
